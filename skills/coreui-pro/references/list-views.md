# Main list screens: search, filters, views and sorting

Use this reference when the request is a primary module list: products, inventory/stock,
customers, orders, invoices, warehouses or any collection users search daily. It
describes the screen anatomy observed in a privately inspected Laravel + Vue 3 ERP
(product catalog and stock listing) as original guidance. Read
[custom-crud.md](custom-crud.md) for the CRUD/modal conventions and
[tables.md](tables.md) for processing ownership. The worked
[list example](../examples/list-page.md) applies everything below.

## Screen anatomy (top to bottom)

1. **Header row**: title + muted subtitle on the left, primary create action on the right
   (omit the action on read-only lists such as stock or kardex).
2. **Toolbar card** (CCard > CCardBody > CRow): one row of homogeneous controls, owned
   by the page, not by the table.
3. **Result strip**: view switch (grid/table) on the left, "N found" on the right.
4. **Results**: grid of cards or a table card, never both. Loading, error, empty and
   no-match states replace the results area, not the whole page.
5. **Pagination** under the results, sized by the shared page-size preference.
6. **Modals** for create/edit/detail/delete and toasts for feedback.

## Toolbar control catalogue

Compose only the controls the domain needs, in this order. Reuse the same widths in
sibling lists so screens feel identical.

| Control | Component | Typical column | Notes |
| --- | --- | --- | --- |
| Text search | CFormInput | md 3 | Debounced; searches only fields the API approves (name, SKU, barcode…). Placeholder names them. |
| Category / parent | CFormSelect | md 2 | First option "All categories"; options loaded once from a lookup endpoint. |
| Status | CFormSelect | md 2 | Record lifecycle: active, inactive, discontinued. |
| Stock / health | CFormSelect **or** quick-filter chips | md 2 / md 6 | Computed state: in stock, low stock, out of stock. |
| Secondary scope | CFormSelect / CMultiSelect | md 3 | Warehouse, branch, owner. Changes the numbers, not just the rows. |
| Date / period | CDateRangePicker with `ranges` | md 3–4 | Never native date inputs ([date-time.md](date-time.md)); refetch once both ends are set or cleared. |
| Sort | CFormSelect | md 2 | Few approved keys (created, name, price, stock). Add a direction toggle if both are useful. |
| Reset | CButton secondary outline | md 1 | One coherent update: clears every control and requests once. |

On narrow screens controls stack (`xs=12`, `sm=6`, then `md`/`lg` widths); add `gy-2`
or `g-3` to the row. Give every control an accessible label (CoreUI `label` prop or a
visually hidden label); a placeholder alone is not a label.

### Quick-filter chips (stock style)

For a short, mutually exclusive health filter, a CButtonGroup of toggles is faster than
a select: All / Below minimum / Out of stock. The active chip uses the semantic color
(`primary` for All, `warning` for low, `danger` for out) and the others
`secondary` + `variant="outline"`. Expose state with `aria-pressed`. Chips and the select
variant bind the same `stock` query key; do not render both for one key.

## Query contract

Keep **one query object** for the whole list: `search`, each domain filter, `sort`
(and `direction`), `page`, `perPage`. Every criteria change sets `page = 1`, invalidates
older responses and refetches; switching grid/table changes presentation only and must
keep the query. Map names to the backend in the service (one place) and verify them:
mismatched names such as a UI `stock_filter` versus an API `stock_status` silently
drop the filter. Read the controller/service for the exact allow-list of sortable
columns and filter values; never forward free-form sort fields.

Send `undefined` (not empty strings) for inactive filters so they do not appear in the
URL. Preserve filters in the route query when the project already does so.

## Views: grid and table share records

- A grid/table switch is a CButtonGroup of icon buttons with accessible names
  (`aria-label`, `aria-pressed`). Default to the presentation the module's users scan
  fastest (grid for visual catalogs, table for operational stock).
- **Card**: image (with fallback on error), name, short description clamp, price/money,
  category, key quantity, SKU, status and stock badges, then compact icon actions
  (view, edit, delete) with names. Badges overlay the image corner; text must not rely
  on color alone.
- **Table**: first column combines thumbnail + name + muted description; then SKU,
  category, money, quantity with badge, status, actions. Use column slots for cells.
  Keep the actions column unsortable.
- Both views render the same `records` array and the same empty/no-match messages.
- Money, quantity and date formatting use the project's formatters/locale, not
  string concatenation.

## Sorting

Two valid owners; choose one per list:

1. **Toolbar sort select** (catalog style): simple, mobile-friendly, few keys.
2. **Column header sorting** (operational tables): enable the sorter only on columns the
   API supports. With CSmartTable use external sorter mode (`column-sorter` with
   `external`, a controlled `sorter-value`, and the sorter-change event) and map the
   event to `sort`/`direction`. Do not leave the internal sorter on over a server page.

Never offer both for the same key. Document any column that is intentionally unsorted.

## Pagination and page size

The server owns count, page and size. Read `perPage` from the shared settings store (the
inspected app exposes a default page size) before the first request, and refetch from
page 1 when it changes. Show totals from the pagination envelope, not the length of the
current page. For grids use the project's pagination wrapper under the cards; for tables
use either CSmartTable external pagination (verify page 2+ renders the full server page)
or CTable + the same wrapper. Do not combine both.

## States

Render in this priority: **loading → error with retry → empty collection (with create
call-to-action) → no matches (message to adjust or reset filters) → results**. The empty
state shows an icon, a title, a hint and the create action only when the user may create.
Disable or hide create/edit/delete according to permissions and enforce them on the server.

## Debounce, stale responses and the CFormInput event order

Debounce text search (about 300 ms), apply select/chip changes immediately, and ignore
responses from superseded requests with a generation counter or abort signal. Bind the
search input through its model value (`v-model` plus a watcher, or the
`update:model-value` payload). A plain `@input` handler that reads the bound ref can see
the previous keystroke in the inspected CoreUI control because that native event fires
before the model update.

## Variants by module

| Module | Toolbar | Default view | Extras |
| --- | --- | --- | --- |
| Product catalog | search, category, status, stock, sort, reset | grid + table | image upload, announce/export actions |
| Stock / inventory levels | search, warehouse, stock chips | table | header sorting on quantities, kardex/history modal, no create |
| Categories, brands, warehouses | search, status | table | small forms in modals; tree/parent select if hierarchical |
| Documents (orders, invoices) | search, status, date range, customer | table | status badges, row navigation to detail |

## Checklist

Controls labelled and keyboard reachable; one query state; page resets on criteria
change; reset requests once; totals from the server; views share records; unsortable
action column; loading/error/empty/no-match states; permission-gated actions;
translations through the project's i18n; mobile stacking verified.
