# Personalized CRUD with consistent search

Use this reference for business CRUD and custom list/search requests. Personalization
means composing CoreUI primitives around the domain and the established application
experience. Native components do not require the template's stock screen layout or
CSmartTable's built-in search bar. Prefer the user's established personalized CRUD.

## Additional inspected application pattern

A privately inspected Laravel + Vue 3 application implements its product screen in
`resources/js/pages/sales/Products.vue`, alongside a similarly structured orders page.
Its manifest declares Vue ^3.5.32, Vue Router ^4.5.1, CoreUI Vue Pro ^5.21.1,
CoreUI Pro styles ^5.27.1, Pinia ^3.0.3 and vue-i18n ^10.0.8. These are declared
ranges, not a new mandatory version baseline. Inspection covered the product page,
orders toolbar, shared pagination, API/toast composables, settings store, product
service, Laravel controller/response envelope and backend filtering service.

The product pattern consists of:

- A feature title/subtitle and primary create action above the list.
- A separate CoreUI card holding custom search, category/status/stock filters,
  ordering and a reset action. Filtering lives outside the table.
- A result count and grid/table switch; both presentations consume the same records.
- Product cards and custom table cells with imagery, identity, category, money,
  stock/status badges and contextual actions.
- Create/edit and read-only detail modals, plus shared toast feedback.
- Server search/pagination, shared page-size settings, AppPagination for cards and
  CSmartTable pagination for the table presentation.
- Form image previews, existing/new upload state, primary image and cleanup of object URLs.

The toolbar markup is currently page-local; no shared search-toolbar component was
found in the product page's imports. Homogeneity comes from repeated visual composition,
shared controls and services. Reuse an existing toolbar when one exists in the target.
If several modules need the same new toolbar, extract a small shared component with
filter/action slots; do not invent a universal CRUD engine or copy the whole page.

The full toolbar catalogue, quick-filter chips, view switch, sorting and state order
are in [list-views.md](list-views.md); the [list example](../examples/list-page.md) shows them together.

## Compose the requested screen

Maintain common toolbar placement, field sizes, spacing, reset behavior, result count,
button hierarchy, row-action style and modal conventions across sibling CRUDs. Keep
filter definitions, columns, record cards and form fields specific to each domain.
Use CCard/CRow/CCol/CFormInput/CFormSelect/CButton to build the search surface and
CTable or CSmartTable for rows. Leave table-filter/column-filter off when the toolbar
already owns those queries. Add grid mode only when visual records benefit from it.

Use one query state for search, domain filters, sort, page and page size. Search across
the backend's approved fields; do not imply a field is searchable just because it is
visible. Bind to the model or use update:modelValue's value directly: a plain input
handler reading the model can observe the previous character in the inspected control.
Debounce remote typing, reset page on criteria changes, invalidate stale responses
immediately, and make reset one coherent update/request. Keep filters when switching
views. A per-page setting is a preference, not an independent second paginator.

The inspected Laravel response provides records under data and counts under pagination
(current_page, last_page, per_page, total). Reuse the real HTTP client/auth/CSRF setup
and normalize that envelope in the service. Read the backend for exact parameter names.
Use server pagination totals, not current-page length, for result counts. After a
mutation, refetch with the current criteria and recover if the last page disappears.

## Distinguish visual patterns from implementation gaps

The inspected product frontend sends stock_filter while the service reads stock_status;
new integrations must reconcile such contracts. Its watcher requests on every search
change without debounce or stale-response protection; reset can trigger duplicate
requests. These are observations to improve, not requirements to reproduce.

CSmartTable's external pagination event mode alone may still slice input records in
the installed implementation. Verify page 2+ renders the complete server page. Use a
verified external/no-slicing configuration or CTable with the existing AppPagination.
Do not guess that CPagination itself accepts pages/active-page/page-change: those
belong to the inspected application wrapper, not that CoreUI primitive.

For new modal forms, use real submit semantics: a footer save button outside a form
must target its ID or call a validation-aware submit path. Keep drafts on failure,
map Laravel 422 field errors, prevent duplicate saves and close only after success.
The inspected delete flow uses browser confirm; prefer the project's CoreUI confirmation
wrapper (or a CModal) for newly designed homogeneous CRUDs. Existing image mutations
can persist immediately, so define whether Cancel discards only the draft or all edits.

Reuse the actual vue-i18n/API/toast/settings/auth conventions instead of replacing them
with the commercial starter's i18next paths or UI-only stores. Preserve permission-gated
actions and server checks; domain side effects require their own explicit action.

Minimal custom CSS is appropriate for thumbnails, image overlays or domain layout gaps.
Use existing theme variables; keep hover actions keyboard/touch accessible. Do not copy
private images, domain datasets, source code or branding into the public skill.

See the original [custom CRUD example](../examples/crud-page.md). Its small customer
domain illustrates the composition; product-specific fields and grid mode above are
optional adaptations, not mandatory elements of every CRUD.
