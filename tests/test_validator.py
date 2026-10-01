"""Negative controls: verify that malformed packages actually fail validation."""
import shutil
import tempfile
import unittest
from pathlib import Path
from validate import ROOT, validate

class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'package'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '.venv', '__pycache__'))

    def test_clean_package(self):
        self.assertEqual(validate(self.root), [])

    def test_missing_reference(self):
        (self.root/'skills/coreui-pro/references/forms.md').unlink()
        self.assertTrue(any('broken link' in p for p in validate(self.root)))

    def test_duplicate_yaml_key(self):
        path = self.root/'skills/coreui-pro/SKILL.md'
        path.write_text(path.read_text().replace('name: coreui-pro', 'name: coreui-pro\nname: other'))
        self.assertTrue(any('frontmatter' in p for p in validate(self.root)))

    def test_unreachable_reference(self):
        (self.root/'skills/coreui-pro/references/orphan.md').write_text('# Orphan\n')
        self.assertTrue(any('unreachable' in p for p in validate(self.root)))

    def test_private_artifact(self):
        (self.root/'.npmrc').write_text('synthetic registry configuration')
        self.assertTrue(any('forbidden' in p for p in validate(self.root)))

    def test_secret_detection(self):
        (self.root/'accidental.txt').write_text('ghp_' + 'a' * 30)
        self.assertTrue(any('possible secret' in p for p in validate(self.root)))

    def test_native_date_input_rejected(self):
        path = self.root/'skills/coreui-pro/examples/form-page.md'
        path.write_text(path.read_text() + '\n```vue\n<template><CFormInput type="date" /></template>\n```\n')
        self.assertTrue(any('native date/time input' in p for p in validate(self.root)))

    def test_overlap_detection(self):
        template = Path(self.temp.name)/'private-template'
        (template/'src').mkdir(parents=True)
        content = '\n'.join(f'original synthetic fixture statement number {i}' for i in range(20))
        (template/'src/fixture.js').write_text(content)
        (self.root/'accidental.md').write_text('Preface\n' + content + '\nAfterword')
        self.assertTrue(any('source overlap' in p for p in validate(self.root, template)))

if __name__ == '__main__':
    unittest.main()
