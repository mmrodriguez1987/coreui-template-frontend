---
name: coreui-pro
description: >
  Build and extend CoreUI Pro Vue frontends using the application's existing
  architecture and native components. Use for CoreUI Pro pages, dashboards,
  CRUD, forms, tables, modals, search, navigation, routes, charts, and styling,
  or an explicitly requested migration to CoreUI Pro.
license: MIT
metadata:
  version: "1.1.0"
  framework: "vue"
---

# CoreUI Pro frontend architecture

Extend the application as its frontend architect: compose established components,
keep state and integration responsibilities clear, and preserve the existing UI.
This skill contains original guidance, not a licensed template or a package installer.
It requires access to the target Vue source and legitimately installed CoreUI Pro
packages. References cover Vue 3 and CoreUI Vue Pro 5.

## Authority and scope

Resolve conflicts in this order:

1. Existing project conventions.
2. Existing installed CoreUI Pro version.
3. Existing reusable components.
4. Existing template patterns.
5. These skill references.
6. Generic CoreUI knowledge.

Do not force the inspected template's directories, router, language, or state library
onto another application. This release specializes in Vue. If detection finds React
or Angular, retain the reuse principles but do not apply Vue syntax or invent an API.
For a new application, inspect the user's licensed starter first; if none is available,
identify the missing framework/package access before attempting template scaffolding.

## Inspect before writing code

1. Read project instructions, `package.json`, lockfile, build/lint configuration,
   and installed package versions. Distinguish template, CSS, and Vue binding versions.
2. Locate entry points, relevant pages, router, navigation configuration, layouts,
   reusable components, styling, and any existing data/auth services.
3. Read the closest working implementation. Determine component registration,
   event/slot contracts, state ownership, localization, and responsive behavior.
4. Check which installed CoreUI Pro components solve the requirement; verify uncertain
   props, exports, slots, and events in local package declarations/source or matching
   official documentation. Never print registry credentials while inspecting config.
5. Give a short implementation plan identifying files, reuse choices, state/data flow,
   and validation. Then implement within the requested scope.
6. Run the project's applicable build, lint, type checks, and relevant tests. Do not
   invent a type-check script in a JavaScript project. Exercise affected routes and
   UI states where a browser is available; report anything not actually tested.
7. Report files changed, behavior, validation results, and remaining integration gaps.

## Do not reinvent CoreUI Pro

Before hand-building cards, navigation, modals, accordions, tables, alerts, tabs,
pagination, badges, sidebars, dropdowns, or form controls, check for an appropriate
installed component. Prefer it when practical. Use custom logic for domain behavior;
use a custom visual component only for a demonstrated gap and explain the reason.

Style in this order: existing project components → CoreUI Pro components → CoreUI
utilities → existing theme variables → existing SCSS conventions → minimal custom CSS.
Do not introduce a new design system unless requested. Do not add Bootstrap's JS
or a second UI library to operate components already managed by Vue/CoreUI.

For business CRUD, prefer a personalized screen consistent with sibling modules:
a dedicated search/filter toolbar, domain-specific cells/cards and modal workflows.
Compose CoreUI primitives to achieve it; do not default to a stock CSmartTable search
bar or generic scaffold. Read [personalized CRUD](references/custom-crud.md) first.

## Load only the relevant documents

Paths below are relative to this skill directory. Start with the smallest relevant
set; add references only when the implementation needs them.

| Task | Read |
| --- | --- |
| Understand a project or add a page | [architecture](references/architecture.md), [layouts](references/layouts.md), [routing](references/routing.md) |
| Add a menu item | [navigation](references/navigation.md), [routing](references/routing.md) |
| Personalized business CRUD | [personalized CRUD](references/custom-crud.md), [architecture](references/architecture.md), [components](references/components.md), [forms](references/forms.md), [tables](references/tables.md), [layouts](references/layouts.md); routing/navigation if exposed in the menu |
| Dashboard | [dashboards](references/dashboards.md), [charts](references/charts.md), [layouts](references/layouts.md), [components](references/components.md) |
| Form or validation | [forms](references/forms.md) |
| Table, filters, or search | [personalized CRUD](references/custom-crud.md), [tables](references/tables.md); [navigation](references/navigation.md) for header search |
| Modal, toast, tabs, or other UI primitive | [components](references/components.md) |
| Theme or responsive styling | [styling](references/styling.md), [layouts](references/layouts.md) |
| Authentication screens | [authentication](references/authentication.md), [forms](references/forms.md), [routing](references/routing.md) |
| Integration review | [best practices](references/best-practices.md) |
| Broken behavior | [troubleshooting](references/troubleshooting.md) |
| Historical inspection evidence | [template baseline](references/template-baseline.md) |

Original worked examples: [CRUD](examples/crud-page.md),
[dashboard](examples/dashboard-page.md), [form](examples/form-page.md),
[table](examples/table-page.md), [modal](examples/modal-example.md).
They illustrate decisions and small Vue components; adapt their contracts to the target.

## Completion checks and common mistakes

Verify loading, empty, validation, request-error, and success states relevant to the
feature. Check keyboard operation, labels, mobile overflow, and light/dark appearance.
Routes and menu entries must resolve under the right shell; breadcrumbs must still work.
Never treat a demo click handler as persistence, a sidebar item as authorization, or
`DefaultLayout` as an authentication guard. Do not copy demo datasets, branding,
`Docs*` wrappers, or random metrics into business features.

Inspect licensed material only in the user's authorized environment. Public skill
changes must be original explanations or small original examples. Do not redistribute
commercial source, assets, package archives, credentials, or documentation excerpts.
