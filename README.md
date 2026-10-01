# CoreUI Pro Agent Skill

**Build personalized Vue frontends with CoreUI Pro and your application's existing architecture.**

An independent, open-source Agent Skill for coding agents working on CoreUI Pro Vue applications. It teaches agents to inspect the project, reuse its components and services, and build consistent business screens with native CoreUI primitives.

The goal is practical frontend architecture with the visual quality of the CoreUI Pro admin template: custom CRUD interfaces, coherent search and filters, dashboards, forms, navigation, and responsive layouts that belong in your application.

[Explore the skill](skills/coreui-pro/SKILL.md) · [Custom CRUD example](skills/coreui-pro/examples/crud-page.md) · [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md)

## Why this skill?

Coding agents can produce a working page that still ignores the application's conventions: a second search interface, mismatched navigation, unnecessary CSS, or a table that filters only the current server page.

This skill gives agents a project-first workflow and concrete component-selection guidance. Its central principle is **do not reinvent CoreUI Pro**: personalize the screen by composing CoreUI components and existing application wrappers around the business requirements.

## What it covers

| Area | Guidance |
| --- | --- |
| Personalized CRUD | Domain-specific cells and cards, create/edit modals, detail views, deletion confirmation and feedback |
| Search and filters | Consistent custom toolbars, domain filters, ordering, reset behavior and result counts |
| Tables | Local or server processing, pagination ownership, row actions, loading and empty states |
| Forms | Draft state, validation, submission, errors and appropriate native controls |
| Dashboards | Responsive grids, KPI widgets, charts, progress and operational detail |
| Application structure | Existing layouts, routes, sidebar configuration, breadcrumbs and shared services |
| Styling | CoreUI utilities, theme variables, light/dark modes and minimal custom CSS |
| Authentication UI | Existing screen patterns and explicit boundaries between UI and real authentication |

### Personalized CRUD, consistent across modules

Business screens should follow the application's established experience. The preferred pattern uses a dedicated search/filter card, domain-specific table cells or record cards, server-owned results, and modal workflows.

Search, filters, ordering and pagination share one query model. Remote typing is debounced, outdated responses are ignored, and switching presentation should preserve the current criteria. Built-in `CSmartTable` search remains useful for small local lists; a business screen can use its own toolbar while retaining CoreUI components.

See the [personalized CRUD guide](skills/coreui-pro/references/custom-crud.md) and [original worked example](skills/coreui-pro/examples/crud-page.md).

## Supported framework and scope

**Version 1.3.0 focuses on Vue 3 and CoreUI Vue Pro 5.** Its guidance comes from inspection of a licensed Vue template and a customized Laravel/Vue application. The public instructions and examples are original.

| Inspected template | Version or architecture |
| --- | --- |
| CoreUI Pro Vue Admin Template, default theme | 5.9.0 |
| Vue | 3.5.42 |
| `@coreui/vue-pro` | 5.21.1 |
| `@coreui/coreui-pro` styles | 5.27.1 |
| Application architecture | Vite, Vue Router, Pinia, Sass, i18next and CoreUI Chart.js integration |

These are inspection results, not required versions for your application. The additional Laravel/Vue pattern demonstrates how to preserve different service, localization and store conventions. See the [template inventory](skills/coreui-pro/references/template-baseline.md) for detailed evidence.

This repository contains skill guidance and teaching examples. It does not include a runnable admin application, a backend, or the commercial template. React and Angular implementations are outside the current scope.

## Installation

Run installation commands from the **application where you want to use the skill**. Your application needs its own appropriately licensed CoreUI Pro dependencies.

### From GitHub

Replace `OWNER/REPOSITORY` with this repository's GitHub location:

```sh
npx skills add OWNER/REPOSITORY --skill coreui-pro
```

Select your agent interactively, or target Claude Code explicitly:

```sh
npx skills add OWNER/REPOSITORY --skill coreui-pro --agent claude-code
```

The [skills CLI documentation](https://github.com/vercel-labs/skills) describes source formats and agent selection. Running through `npx` requires Node/npm and registry access; installing this skill does not install CoreUI Pro.

### From a local checkout

Replace the path with the location of your cloned skill repository:

```sh
npx skills add /path/to/coreui-pro-agent-skill --skill coreui-pro
```

To check discovery without installing:

```sh
npx skills add /path/to/coreui-pro-agent-skill --list
```

### Manual installation for Claude Code

From the consuming application, if `.claude/skills/coreui-pro` does not already exist:

```sh
mkdir -p .claude/skills
cp -R /path/to/coreui-pro-agent-skill/skills/coreui-pro .claude/skills/coreui-pro
```

Copy the entire folder, including references, examples and its license. Review differences before replacing an existing installation. See the [Claude Code skills guide](https://code.claude.com/docs/en/skills) for discovery and invocation behavior.

## Usage

Start a fresh Claude Code session in your application and invoke the skill:

```text
/coreui-pro Build a customer CRUD screen matching our existing product module.
Use a custom search/filter toolbar, server pagination, and create/edit modals.
Reuse our API service, toast notifications, and CoreUI components.
```

Other example requests:

```text
/coreui-pro Add an inventory page, route, and sidebar item using our existing layout.
```

```text
/coreui-pro Create a responsive service dashboard with KPI widgets and charts.
Follow our theme and show loading, empty, and request-error states.
```

Claude Code, Codex, Cursor, Windsurf and other Agent Skills-compatible clients can consume the `SKILL.md` folder through their supported discovery mechanism. Installation and invocation vary by client version; this project does not claim end-to-end testing in every client.

### What to expect from the agent

1. Inspect package versions, relevant pages, routes, navigation, layouts and reusable components.
2. Find the closest existing implementation and verify the installed component APIs.
3. Present a short plan, then implement using the application's patterns.
4. Run applicable compilation, linting, type checks and relevant tests.
5. Report changed files, validation results and any remaining integration gaps.

When guidance conflicts, the skill prioritizes existing project conventions, installed CoreUI versions, reusable components and established template patterns over its own references or generic knowledge.

## Examples and progressive disclosure

The agent loads only references relevant to the task. A menu change primarily needs routing and navigation; a CRUD screen needs the personalized CRUD, form, table and architecture guidance.

| Example | Purpose |
| --- | --- |
| [Personalized CRUD](skills/coreui-pro/examples/crud-page.md) | Custom toolbar, remote results, modal workflows and request coordination |
| [Dashboard](skills/coreui-pro/examples/dashboard-page.md) | Template dashboard blueprint: gradient KPI widgets, range picker, every chart type, progress groups, detail table |
| [Form](skills/coreui-pro/examples/form-page.md) | Editable draft, validation and an explicit save contract |
| [Local table](skills/coreui-pro/examples/table-page.md) | Built-in filtering and pagination for a complete local collection |
| [Delete modal](skills/coreui-pro/examples/modal-example.md) | Confirmation, stable record identity and error recovery |
| [Main list](skills/coreui-pro/examples/list-page.md) | Toolbar filters, stock chips, sort, grid/table switch and server totals |
| [Minimal local CRUD](skills/coreui-pro/examples/local-crud-page.md) | Smaller alternative for explicitly local datasets |

Examples use synthetic content and documented adapter contracts. Connect them to your application's actual services; they do not supply persistence or authentication.

## Repository structure

```text
.
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── .gitignore
├── skill-validation.md
├── skills/
│   └── coreui-pro/
│       ├── SKILL.md
│       ├── LICENSE
│       ├── references/          # Architecture and task-specific guidance
│       └── examples/            # Six original Vue teaching examples
└── tests/
    ├── requirements.txt
    ├── validate.py
    ├── compile-examples.mjs
    ├── test_validator.py
    └── scenarios.md
```

## Validation

Run the public package checks with Python 3.9+:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r tests/requirements.txt
.venv/bin/python tests/validate.py
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
```

The validator checks metadata, local links, resource reachability, license consistency and common publication hazards. Optional checks compare against local licensed source and compile the original examples using a consuming application's Vue compiler.

For version 1.3, metadata/package checks, seven validator tests and compilation of all seven Vue examples passed. Browser interactions, real backend integration and live-agent scenarios remain separate checks to run in a private consumer application.

See [validation instructions and results](skill-validation.md) and the [behavioral scenario suite](tests/scenarios.md). Heuristic content checks do not replace manual review of publication files and history.

## Contributing

Contributions should improve a concrete agent decision or implementation outcome. Keep references focused, verify component contracts, and use original examples with synthetic data.

Read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting changes. Never include licensed templates, commercial assets, private application source, credentials or copied documentation in issues or pull requests.

## Roadmap

- Record behavioral evaluations across supported coding agents.
- Add executable adapter and request-race tests for server-paginated CRUD.
- Expand accessibility, mobile and color-mode runtime checks.
- Verify additional Vue Pro versions with explicit compatibility evidence.
- Consider separate React and Angular skills after inspecting their respective starters.

## License and CoreUI relationship

This project is an independent Agent Skill designed to assist developers working with CoreUI Pro. It is not maintained, sponsored or endorsed by CoreUI.

The [MIT license](LICENSE) applies only to this project's original skill content and tooling. It does not license CoreUI Pro, its commercial templates, packages, assets, trademarks or documentation. Users must obtain their own appropriate CoreUI Pro license.

No proprietary template source, commercial assets, private packages, credentials or license keys are distributed with this project. CoreUI product names are used descriptively.
