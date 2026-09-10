# Analyze and extend the application

Create a compact working model before editing: framework and installed versions;
entry and component registration; route → layout → page; navigation → route;
page → existing data service/store; global theme → page utilities. Record unknowns
instead of assuming a template provides persistence or authentication.

In the inspected Vue baseline, `src/main.js` installs CoreUI globally, while charts
are imported separately. `src/App.vue` owns root routing and theme initialization.
Pages belong under feature directories in `src/views`; shared shell components are
under `src/components`; `src/stores` holds small Pinia UI stores. The concrete
version evidence and inventory are in [template-baseline.md](template-baseline.md).

For a page, find the nearest feature sibling and trace how it becomes reachable.
Place feature-only form/chart/dialog children near that page; promote a component
only when it has a stable responsibility shared across features. Reuse existing
business wrappers before introducing a new wrapper around every CoreUI component.
Use the current JavaScript/TypeScript and Composition/Options API conventions.

Keep domain records separate from display state (loading, filter, selected record,
modal visibility). Local state is usually sufficient for one screen. Use the project's
existing service or store for shared data. The baseline has no API layer to copy:
if a backend contract is missing, define a narrow explicit adapter and label demo
behavior instead of manufacturing a working endpoint.

Use the requested scope to decide whether route, menu, locale and test files also
change. A child page rendered inside an existing layout must not recreate the shell.
A wrapper group needs a router outlet; a leaf needs its own page. Read actual code
when comments or architectural prose disagree with it.

For new projects, first inspect the supplied licensed starter and its installation
requirements. Never generate a replacement commercial template from this skill.

For Laravel/Vue applications, inspect resources/js, the existing HTTP service, API
response envelopes and backend filter/validation contracts. Reuse the actual localization
and stores. The additional [personalized CRUD pattern](custom-crud.md) demonstrates
how an application can legitimately differ from the commercial starter.
