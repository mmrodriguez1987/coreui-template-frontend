#!/usr/bin/env python3
"""Validate the public skill package; optional local overlap audit never prints source."""
import argparse
import hashlib
import re
from pathlib import Path
from urllib.parse import unquote

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', '.venv', '__pycache__'}
BINARY = {'.png', '.jpg', '.jpeg', '.webp', '.svg', '.ico', '.zip', '.tgz', '.gz', '.tar', '.woff', '.woff2', '.pdf', '.pem', '.key', '.p12'}
SECRET_PATTERNS = [
    r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|npm_[A-Za-z0-9]{20,})\b',
    r'(?:_authToken|license[_-]?key)\s*[:=]\s*[\"\']?[A-Za-z0-9+/=_-]{16,}',
    r'https?://[^\s/:]+:[^\s/@]+@',
]

class UniqueLoader(yaml.SafeLoader):
    pass

def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError('duplicate YAML key')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result

UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)

def files_under(root):
    return sorted(p for p in root.rglob('*') if not any(x in SKIP for x in p.relative_to(root).parts) and (p.is_file() or p.is_symlink()))

def links(text):
    text = re.sub(r'```.*?```', '', text, flags=re.S)
    return re.findall(r'\[[^\]]+\]\(([^)]+)\)', text)

def windows(text, size=12):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for start in range(len(lines) - size + 1):
        chunk = '\n'.join(lines[start:start + size])
        if len(chunk) >= 250:
            yield hashlib.sha256(chunk.encode()).digest()

def validate(root, template=None):
    root = root.resolve()
    errors = []
    skill = root / 'skills/coreui-pro'
    entry = skill / 'SKILL.md'
    required = ['README.md', 'LICENSE', 'CHANGELOG.md', 'CONTRIBUTING.md', '.gitignore', 'skill-validation.md', 'skills/coreui-pro/LICENSE']
    for name in required:
        if not (root / name).is_file(): errors.append(f'missing required file: {name}')
    if not entry.is_file(): return errors + ['missing SKILL.md']
    source = entry.read_text()
    try:
        match = re.match(r'\A---\n(.*?)\n---\n(.+)\Z', source, re.S)
        if not match: raise ValueError('frontmatter boundaries or body missing')
        front = yaml.load(match[1], Loader=UniqueLoader)
        if not isinstance(front, dict): raise ValueError('frontmatter must be a mapping')
        allowed = {'name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools'}
        if set(front) - allowed: raise ValueError('unsupported frontmatter field')
        name = front.get('name', '')
        if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64 or name != skill.name:
            raise ValueError('invalid skill name')
        for key, limit in [('description', 1024), ('compatibility', 500)]:
            if key == 'description' or key in front:
                value = front.get(key)
                if not isinstance(value, str) or not 1 <= len(value) <= limit:
                    raise ValueError(f'invalid {key}')
        metadata = front.get('metadata', {})
        if not isinstance(metadata, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in metadata.items()):
            raise ValueError('metadata must contain string keys and values')
        if front.get('license') != 'MIT': raise ValueError('license must match repository MIT scope')
        if len(source.splitlines()) >= 500: raise ValueError('entrypoint exceeds progressive disclosure limit')
    except (ValueError, yaml.YAMLError, TypeError) as exc:
        errors.append(f'frontmatter: {exc}')
    texts = {}
    graph = {}
    for path in files_under(root):
        relative = path.relative_to(root)
        if path.is_symlink():
            errors.append(f'public package contains symlink: {relative}')
            continue
        if path.suffix.lower() in BINARY or path.name in {'.npmrc', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml'} or path.name.startswith('.env') or 'node_modules' in relative.parts:
            errors.append(f'forbidden publication artifact: {relative}')
            continue
        try: text = path.read_text()
        except UnicodeDecodeError:
            errors.append(f'non-text artifact: {relative}')
            continue
        texts[path] = text
        if re.search(r'/Users/[A-Za-z0-9_.-]+/', text) or re.search(r'[A-Z]:\\Users\\', text):
            errors.append(f'personal absolute path: {relative}')
        for pattern in SECRET_PATTERNS:
            if re.search(pattern, text, re.I):
                errors.append(f'possible secret: {relative}')
                break
        if path.suffix != '.md': continue
        graph[path] = []
        for destination in links(text):
            destination = destination.strip('<>')
            if re.match(r'(?:https?://|mailto:|#)', destination): continue
            target = (path.parent / unquote(destination.split('#')[0])).resolve()
            if not target.is_relative_to(root): errors.append(f'link escapes repository: {relative}')
            elif not target.exists(): errors.append(f'broken link in {relative}: {destination}')
            else: graph[path].append(target)
    native_date = re.compile(r'<(?:input|CFormInput)\b[^>]*\btype=["\'](?:date|time|datetime-local|month|week)["\']', re.I)
    for path, text in texts.items():
        if path.suffix != '.md' or not path.is_relative_to(skill): continue
        for block in re.findall(r'```(?:vue|html|js)\n(.*?)```', text, flags=re.S):
            if native_date.search(block):
                errors.append(f'native date/time input in skill code: {path.relative_to(root)}')
                break
    reachable = set()
    queue = [entry]
    while queue:
        current = queue.pop()
        if current in reachable: continue
        reachable.add(current)
        queue.extend(graph.get(current, []))
    for path in list((skill/'references').glob('*.md')) + list((skill/'examples').glob('*.md')):
        if path not in reachable: errors.append(f'unreachable skill resource: {path.relative_to(root)}')
    if (root/'LICENSE').exists() and (skill/'LICENSE').exists() and (root/'LICENSE').read_bytes() != (skill/'LICENSE').read_bytes():
        errors.append('packaged license differs from root license')
    if template:
        template = template.resolve()
        if not (template/'src').is_dir():
            errors.append('template audit path must contain src/')
        else:
            hashes, chunks = set(), set()
            for path in template.rglob('*'):
                if not path.is_file() or any(x in {'.git', 'node_modules'} for x in path.relative_to(template).parts): continue
                hashes.add(hashlib.sha256(path.read_bytes()).digest())
                if path.suffix in {'.vue', '.js', '.scss', '.md', '.json', '.mjs'} and path.name != 'LICENSE':
                    try: chunks.update(windows(path.read_text()))
                    except UnicodeDecodeError: pass
            for path, text in texts.items():
                if path.name == 'LICENSE': continue
                if hashlib.sha256(path.read_bytes()).digest() in hashes:
                    errors.append(f'identical licensed-input file: {path.relative_to(root)}')
                if chunks.intersection(windows(text)):
                    errors.append(f'possible 12-line source overlap: {path.relative_to(root)}')
    return errors

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--template', type=Path, help='optional local licensed source, never copied or printed')
    args = parser.parse_args()
    problems = validate(args.root, args.template)
    for problem in problems: print('FAIL:', problem)
    if not problems: print('PASS: metadata, links, discovery, package boundaries and heuristic content checks' + ('; local overlap audit' if args.template else ''))
    raise SystemExit(bool(problems))
