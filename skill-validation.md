# Skill validation and release checks

## Reproducible public checks

Requires Python 3.9+ and PyYAML. From the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r tests/requirements.txt
.venv/bin/python tests/validate.py
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
```

The validator parses YAML with duplicate-key rejection, checks Agent Skills metadata
constraints, validates local Markdown links, verifies resource reachability from
SKILL.md and the packaged license, and flags private file types, personal paths and
common credential patterns. It follows the [Agent Skills specification](https://agentskills.io/specification).
Negative controls prove broken links, invalid metadata, orphan references, sensitive
artifacts, token-like strings and synthetic source overlap are detected.

The optional licensed-source audit remains local:

```sh
.venv/bin/python tests/validate.py --template /path/to/licensed-template
```

It compares exact file hashes and runs of 12 nonempty normalized lines (at least 250
characters). It prints only findings about public file paths, never licensed source
or credentials. This catches accidental copying, not every derivative work or secret.
Manual review is still required. It does not inspect Git history or provide legal clearance.

## Original example syntax checks

Use a licensed Vue app that already has @vue/compiler-sfc installed:

```sh
node tests/compile-examples.mjs /path/to/licensed-vue-app
```

This parses and compiles the seven original Vue code blocks, including template and
style syntax, without copying any dependencies or emitting licensed bundles. It does
not resolve every import, type-check component props, call APIs or render a browser.
Materialize the examples only in a private licensed consumer app, supply their documented
adapters, and run that app's build/lint plus relevant interaction checks.

## Manual review

- Read SKILL.md alone: activation, inspection, authority order and task routing must
  make sense without this conversation or the inspected machine.
- Confirm references add distinct decisions and all examples are original.
  Keep the shared authority/reuse workflow in the entrypoint instead of repeating it.
- Check every component/event claim against the installed version or official matching
  documentation. Observe demo shortcomings without prescribing them as conventions.
- Follow [behavioral scenarios](tests/scenarios.md) in a private disposable application.
- Review publication files and any Git history for licensed source/assets, credentials,
  private registries, package archives or documentation copying. MIT covers only original
  project content. Include the skill-local license when distributing only that folder.
- Use `npx skills add /path/to/this-repository --list` to smoke-test CLI discovery when
  network access is available, then install in a disposable consumer application.

## Initial validation record — 2026-09-10

- PASS: YAML/name/description/license checks, all local links and reference reachability.
- PASS: bundled skill-creator quick validator; entrypoint is 105 lines. Environment
  requirements live in the body for compatibility with older validators.
- PASS: all seven positive/negative validator tests.
- PASS: optional audit against the inspected licensed tree found no identical public
  files or matching 12-line source runs; no heuristic credential/artifact findings.
- PASS: all five original Vue SFC blocks parsed and compiled using the locally installed
  Vue compiler; used component contracts were also inspected in the licensed packages.
- PASS: skills CLI local `--list` discovered exactly one skill named `coreui-pro`.
- REVIEWED: progressive disclosure, distinct reference responsibilities, original
  example provenance and repository organization; no repeated long skill paragraphs.
- NOT RUN: consumer browser tests, live Claude Code/other-client behavioral scenarios,
  real backend integration, or a build of a materialized consumer application.

Only the CLI discovery listing ran; no agent installation or publication occurred.
The new repository has no commits to audit for historical content. Repeat the public
checks and review history before a future release.

## 1.1 validation scope

The personalized CRUD revision adds one reference and keeps the former local CRUD as
an alternative, for seven original SFC examples. Validate with the same commands above.
The private application inspection used source and installed component code; it did
not run the application or change its files. Public examples use synthetic customer
content and normalized adapters, not copied private product code.

Revision checks passed: metadata/links/resource discovery, skill-creator quick validation,
all seven validator tests, and compilation of all seven Vue SFC blocks using the inspected
Laravel/Vue application's compiler. A separate 12-line normalized overlap scan against
its frontend and PHP application sources found no matches in the public skill Markdown.
No browser or real-backend execution is claimed for this revision.
