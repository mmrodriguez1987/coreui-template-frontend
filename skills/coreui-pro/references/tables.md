# Tables, filtering, and data ownership

The baseline's rich data table is **CSmartTable**, not a separate DataTables/jQuery
integration. Its examples live in `src/views/smart-table`; plain tables appear in
component demos, invoices and dashboards. Choose CTable for straightforward semantic
rows, or CSmartTable when its filtering, sorting, paging or detail slots fit the task.

In observed CSmartTable usage, `items` holds records; `columns` contains keys or
objects with key/label/filter/sorter options; `table-props` configures responsive,
striped and hover behavior. Built-in `table-filter`, `column-filter`, `column-sorter`,
`pagination`, `items-per-page`, and `items-per-page-select` serve local collections.
Column-named slots receive `{ item }` and provide the table cell. The details slot
supports expansion composed with CCollapse. Verify slots/events in the installed API.

## Choose one processing owner

For a complete small local collection, let CSmartTable own sorting/filtering/paging.
A domain filter (such as account status) can derive its input items, but do not also
slice those items into pages. Reset the active page when filters/page size change;
clamp or reset it when a mutation removes the final row on a page.

For server paging, the API owns query, sorting, page size, current page and total count.
A server page is not the full dataset. Inspect installed external-processing settings
and change events before wiring CSmartTable, or use CTable plus CPagination with
explicit state. Do not enable a second internal filter/paginator over one server page.
Preserve URL query conventions if present. Debounce remote text search and cancel or
ignore stale responses; whitelist sortable API fields and handle request errors.

## Business interactions

Use immutable backend IDs for selection and editing/deleting, never row indices.
Keep action columns unsortable/unfilterable. Use CButton or CDropdown for actions,
accessible names for icon buttons, and stop row-click propagation when needed.
Define whether selection spans pages and how filters affect selected records.

Render loading before empty; after success distinguish an empty collection from no
matches. Keep retry errors visible. For large tables, select meaningful columns and
responsive overflow; virtualization is a separate choice and not a substitute for
correct server paging. Keep headers semantic and statuses readable without color.

CSV export must declare its scope (current page, filtered results, or all records).
Compute it from current state, escape quotes/newlines/separators and address spreadsheet
formula interpretation for untrusted cells. The baseline download demo is not a
production export service. The [table example](../examples/table-page.md) demonstrates
local ownership; [CRUD](../examples/crud-page.md) describes persistence boundaries.

## Personalized search takes precedence

For business CRUD, consult [custom-crud.md](custom-crud.md): a dedicated, homogeneous
filter card can own search/status/domain filters and sorting outside the table. Keep
built-in table search/filter controls off when they duplicate that toolbar. The
[primary CRUD example](../examples/crud-page.md) uses server paging and custom cells;
the small local table example is an alternative for complete local datasets only.

For primary module lists (toolbar controls, quick-filter chips, grid/table switch,
external column sorting and state order) read [list-views.md](list-views.md).
