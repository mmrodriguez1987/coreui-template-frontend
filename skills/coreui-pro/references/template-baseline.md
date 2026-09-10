# Inspected template baseline

This is a factual inspection record, not a required application scaffold. Paths refer
to the licensed application, not files shipped with this skill. The repository is
self-contained; consumers do not need the original inspection machine or conversation.

## Version evidence

Inspected 2026-09-10: local default-theme CoreUI Pro Vue Admin Template, package
version **5.9.0**. Values below come from its manifest, lockfile, and installed
package manifests, not from the directory name alone. The local copy includes
maintenance edits; this is not a claim about every upstream 5.9.0 distribution.

| Technology | Manifest range | Resolved/installed |
| --- | --- | --- |
| Vue | ^3.5.41 | 3.5.42 |
| CoreUI Vue Pro (`@coreui/vue-pro`) | ^5.21.1 | 5.21.1 |
| CoreUI Pro styles (`@coreui/coreui-pro`) | ^5.27.1 | 5.27.1 |
| Vue Router | ^5.2.0 | 5.3.1 |
| Pinia | ^4.0.2 | 4.0.3 |
| Vite | ^8.2.1 | 8.2.2 |
| CoreUI Vue Chart.js | ^3.0.0 | 3.0.0 |
| Chart.js | ^4.5.1 | 4.5.1 |
| CoreUI Chart.js | ^4.2.0 | 4.2.0 |
| CoreUI icons / icons-vue | ^3.1.0 / 2.2.0 | 3.1.0 / 2.2.0 |
| CoreUI utils | ^2.0.2 | 2.0.2 |
| FullCalendar Vue 3 | ^7.0.2 | 7.1.0 |

npm is evidenced by `package-lock.json` and npm-oriented scripts; no `packageManager`
field pins its version. JavaScript Vue single-file components primarily use
`<script setup>`. No React or Angular application exists here; images mentioning
those frameworks are not implementations.

## Architecture inventory

| Area | Observed implementation |
| --- | --- |
| Entry | `index.html` → `src/main.js` → `src/App.vue`; mount at `#app` |
| Registration | Main installs Pinia, router, CoreUI Vue Pro, i18next-vue; registers CIcon and Docs helpers; provides an icon registry |
| Build | `vite.config.mjs`, Vue plugin, relative base, `@/` source alias, Sass and Autoprefixer, development port 3000 |
| Checks | `dev`, `build`, `lint`, `preview`, distribution `zip`; ESLint flat Vue essential config; no test/typecheck script |
| Routes | `src/router/index.js`, hash history with BASE_URL, lazy page imports, nested router-view groups, scroll reset |
| Admin shell | `src/layouts/DefaultLayout.vue`: sidebar, wrapper, header, bounded container/outlet, footer, aside |
| Alternate shell | `src/views/apps/email/EmailApp.vue`: email-specific sidebar and shared header/footer/aside |
| Sidebar | `AppSidebar.vue` consumes Pinia visibility/unfoldable state; `AppSidebarNav.js` recursively renders `_nav.js` through RouterLink/CoreUI nav and SimpleBar |
| Header | Sticky `AppHeader.vue`, togglers, account/message/task/notification dropdowns, language/color controls, search modal, shared breadcrumbs |
| Navigation | `src/_nav.js`: component/name/to/icon/items/badge; external href/target; some labels are translation functions |
| Breadcrumbs | `AppBreadcrumb.vue` maps matched routes, evaluates callable names, updates after navigation and locale changes |
| Theme | `App.vue` and header use `useColorModes` with a shared storage key; URL theme can override; Pinia theme default is light |
| Styles | `src/styles/style.scss` loads Pro Sass, chart Sass, vendor calendar/SimpleBar adaptations; CSS variables, logical sidebar padding, dark mode mixin |
| Demo styling | `src/styles/examples.scss` imported separately by App; supports component documentation displays |
| Components | `src/components/App*.vue/js` for shell; `Docs*` for demos; charts/widgets live near their views |
| Pages | `src/views/` grouped by dashboard, widgets, components, forms, smart-table, charts, authentication, error-pages, apps, plugins |
| Forms | CoreUI controls, grid/input groups/floating labels, Pro pickers/selects/password/OTP/stepper examples |
| Validation | Native checkValidity plus CForm validated/novalidate and valid/invalid feedback; no dedicated validation library in manifest |
| Tables | Semantic CTable demos/invoice/dashboard; CSmartTable local filtering/sorting/paging, custom cells, collapsible details, selection and CSV demos |
| Modals | Ref-controlled visible prop and close event; sizing, scrolling, backdrop and fullscreen examples |
| Notifications | CAlert; CToaster/CToast demos and static header dropdowns; no shared notification service |
| Charts | Explicit imports from @coreui/vue-chartjs; theme colors via getStyle; ColorSchemeChange listeners update chart instances |
| Icons | @coreui/icons named imports collected in src/assets/icons/index.js, globally provided; CIcon renderer from icons-vue |
| Authentication | Standalone login/register, password recovery/change/result, magic-link request/result, email confirmation, OTP screens |
| Dashboards | Responsive CRow/CCol, CWidgetStats families, date-range picker, cards/charts/tables/progress; illustrative metrics |
| Responsive | Breakpoint column props, display/flex/spacing utilities, mobile sidebar close, responsive tables |
| Utilities | @coreui/utils getStyle; local path matching, badge mapping, random demo data; no shared business utility layer |
| State/services | Pinia theme/sidebar/aside stores; package composables useColorModes/useTranslation and Vue Router hooks; no src/composables or API/service layer |
| Localization | src/i18n.js; i18next HTTP backend and language detection; public/locales/{en,es,pl}/translation.json |
| Other config | EditorConfig, Prettier settings, browserslist, Docker/nginx static deployment and GitHub workflow inventory |

## Observed limits to avoid inheriting

The router comment calls admin routes protected, but no authentication guard is
implemented. Some route names are functions; this is a local breadcrumb convention,
not a general route-name contract. Preserve existing behavior when adding a route,
but do not invent callable names for another router or depend on them for named links.

Header search lists static suggestions. Register/magic-link handlers navigate without
performing authentication. Toast creation mutates a plain array. Selection examples
include index-derived identity; CSV output is computed once and lacks a robust export
pipeline. Dashboard numbers are demo data. Some document listeners lack cleanup.
These observations inform safer original guidance; they are not patterns to reproduce.

Inspection covered the source tree inventory, every source file's component/import/
interaction patterns, and detailed reads of entry/router/shell/state/theme, representative
forms and validation, all smart-table variants, modal/toast/tab/pagination demos,
authentication handlers, dashboard/chart/widget composition, icons, localization,
and build/deployment configuration. Assets were inventoried, not exported.
