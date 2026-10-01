# Complete CoreUI Pro catalog (UI elements, forms, widgets, plugins, extras, apps)

Inventory of everything the licensed Vue Admin Template 5.9.0 demonstrates, with the
installed CoreUI Vue Pro 5.21.1 contract and when to use it in a business screen.
Descriptions are original; consult the target's installed package for exact props.
**PRO** marks components that exist only in the commercial package.

Before building anything by hand, find it here. Style rules live in
[visual-design.md](visual-design.md).

## Base components

| Component(s) | Use it for | Contract / idiom worth knowing |
| --- | --- | --- |
| CAccordion, CAccordionItem/Header/Body | FAQ, grouped settings, long detail sections | `item-key` per item; `always-open` for independent panels; `flush` inside cards |
| CAlert, CAlertHeading, CAlertLink | Persistent page/form messages | `color`, `dismissible` + `@close`; keep request errors visible with a retry |
| CAvatar | User/customer identity in tables, dropdowns, aside | `src` or initials text, `size` sm/md/lg/xl, `status` dot color, `color`+`text-color` for initials |
| CBadge | Status, counters | Always text; `shape="rounded-pill"`; `position-absolute top-0 end-0` on header icons |
| CBreadcrumb, CBreadcrumbItem | Shell breadcrumb only | Pages do not render their own; routes provide names |
| CButton | Actions | `color`, `variant="outline" \| "ghost"`, `size`, `shape="rounded-pill"`, `square`; icon + text with `me-2` |
| CButtonGroup, CButtonToolbar | View switches, segmented filters, toolbars | `role="group"` + `aria-label`; toolbar wraps groups with `gap-2` |
| CCalendar **PRO** | Inline calendar, availability, range preview | `calendars`, `range`, `startDate`/`endDate`, `selectionType`, `@start-date-change`; style `class="bg-body border rounded"` |
| CCard family (Header/Body/Footer/Title/Subtitle/Text/Link/Image/Group) | Every content section | `mb-4`; `h-100` for equal heights; CCardGroup for joined stats; image top cards for catalogs |
| CCarousel, CCarouselItem, CCarouselCaption | Product galleries, onboarding | `controls`, `indicators`, `transition="crossfade"`, `dark` |
| CChip **PRO** | Removable/selectable token | `@remove`, `@select`; `selectable`, `removable` |
| CChipSet **PRO** | Group of chips (filters, tags) | `v-model:chips`, `v-model:selected`, `selection-mode`, `filter` |
| CCloseButton | Dismiss panels | `dark`/`white` on dark backgrounds |
| CCollapse | Show/hide details (table row details, advanced filters) | `:visible`; pair with an `aria-expanded` button |
| CDropdown family (Toggle/Menu/Item/Header/Divider) | Row actions, header menus | `placement="bottom-end"`, `variant="nav-item"` in header, `:caret="false"` for icon toggles; items `as="button"` for actions |
| CListGroup, CListGroupItem | Activity feeds, settings lists, search results | `flush` inside cards; `border-start-4 border-start-{color}` accents; `active`, `disabled`, `as="button"` |
| CLoadingButton **PRO** | Submit/save with progress | `:loading`, `disabled-on-loading`, `spinner-type="grow"`, optional `timeout` |
| CModal family | Create/edit/detail/confirm | `:visible` + `@close`, `size` sm/lg/xl, `fullscreen`, `scrollable`, `alignment="center"`, `backdrop="static"` while saving |
| CNav, CNavItem, CNavLink | Underlined/pill navigation, card header tabs | `variant="tabs" \| "pills" \| "underline" \| "underline-border"`, `layout="fill" \| "justified"` |
| COffcanvas | Side filter panel, detail drawer on mobile | `placement="end"`, `:visible`, `@hide` |
| CPagination, CPaginationItem | Paging controls | `align="center" \| "end"`, `size`; items are rendered by you (no pages prop) |
| CPlaceholder | Skeletons while loading cards | `animation="glow" \| "wave"`, `:xs` widths; one per loading region |
| CPopover, CTooltip (directives `v-c-popover`, `v-c-tooltip`) | Contextual hints | Keep text short; icon-only buttons still need `aria-label` |
| CProgress, CProgressBar | Quotas, completion, distributions | `thin`, `:value`, `color` incl. `-gradient`, `variant="striped"`, `animated`, stacked bars inside one CProgress |
| CSearchButton **PRO** | Header/global search trigger with shortcut hint | Emits `trigger`; opens a CModal with CFormInput + CListGroup results |
| CSpinner | Small inline loading | `size="sm"`, `variant="grow"`, `aria-hidden` + status text |
| CTable family | Semantic tables, invoices, dashboard tables | `align="middle"`, `hover`, `striped`, `small`, `bordered`, `responsive`, `caption="top"`; header `bg-body-secondary` |
| CTabs, CTabList, CTab, CTabContent, CTabPanel | Modern tabs | `active-item-key`, `item-key` on tab and panel; `variant="tabs" \| "pills" \| "underline-border"` on CTabList |
| CToaster, CToast family | Success/info notifications | `placement="top-end"`, reactive array with stable IDs, `autohide`, `delay`, `color` + `class="text-white"` |
| CVirtualScroller **PRO** | Thousands of rows in a list | `:visible-items`; children are the items |
| CCallout | Inline notes and tips | `color` (info/warning/danger) and `small` text |
| CLink | Styled anchor | Prefer RouterLink for internal navigation |

## Forms

| Component | Use it for | Contract |
| --- | --- | --- |
| CForm | Wrap every form | `class="row g-3"`, `novalidate` + `:validated` for native validation, `@submit.prevent` |
| CFormInput, CFormTextarea | Text, email, number, password (simple) | `label`, `floating-label`, `text`, `feedback-invalid`, `invalid`, `v-model` |
| CFormSelect | Short single choice | `:options` or option children; stable values |
| CFormCheck, CFormSwitch | Booleans, radios | `v-model`, `inline`, `button` variant for toggle buttons; `size="lg"` switches |
| CFormRange | Simple numeric slider | `min`, `max`, `step` |
| CFormFloating | Floating labels | Control + CFormLabel inside |
| CInputGroup, CInputGroupText | Prefix/suffix ($, %, @, units, buttons) | Feedback placement needs `has-validation` |
| CAutocomplete **PRO** | Searching one value in a large list (customer, product) | `v-model`, `:options`, `search` (`'external'` for server search with `@input`), `cleaner`, `indicator`, `show-hints`, `highlight-options-on-search`, `allow-only-defined-options`, `loading` |
| CMultiSelect **PRO** | Choosing many (or one, `:multiple="false"`) from options | No v-model: preselect with `value` or `selected: true` on options, read `@change(selectedOptions)`; `selection-type="tags" \| "counter" \| "text"`, option groups, `search`, `select-all`, `virtual-scroller`, `loading`, `allow-create-options` |
| CChipInput **PRO** | Free-form tags, emails, keywords | `v-model` (array), `separator`, `max-chips`, `chip-class-name`, `create-on-blur` |
| CDatePicker / CDateRangePicker / CTimePicker **PRO** | Every date or time | Mandatory; see [date-time.md](date-time.md) |
| CPasswordInput **PRO** | Passwords with show/hide | `v-model`, `label`, `floating-label`, `invalid`; in 5.21.1 its `feedback-invalid` text renders outside the input wrapper and stays hidden — render `div.invalid-feedback.d-block` yourself |
| COneTimePassword + COneTimePasswordInput **PRO** | 2FA codes | `v-model`, `@complete`; one input child per digit |
| CRangeSlider **PRO** | Price ranges, thresholds, multi-handle | `v-model` (number or array), `labels`, `distance`, `step`, `vertical`, `tooltips-format` |
| CRating **PRO** | Reviews, satisfaction, priority | `v-model`, `precision`, `item-count`, `tooltips` array, `read-only`, custom icon slots |
| CStepper **PRO** | Multi-step wizards (onboarding, checkout, imports) | `:steps`, `layout="horizontal" \| "vertical"`, `step-button-layout`, `linear`, `validation`; slots `#step-N="{ formRef }"` bind a native form for per-step validation; `@step-change`, `@finish`, `@reset`; methods via ref (next/prev/finish/reset) |

Layout idioms from the template: horizontal forms with `CCol :sm="2"` labels and
`:sm="10"` controls; inline forms with `CCol xs="auto"`; validation tooltips with
`tooltip-feedback`. Always prefer a Pro control over hand-made widgets.

## Icons

CoreUI Icons free set: `cil-*` linear, `cib-*` brands, `cif-*` flags. Register each
used icon in the app's icon set (named imports from `@coreui/icons`) and render with
CIcon (`icon="cil-user"` or `:icon="cilUser"`). Sizes: `sm`, `lg`, `xl`, `xxl`, `3xl`…
See icon conventions in [visual-design.md](visual-design.md#icons).

## Widgets

| Widget | Look | Slots / props | Typical use |
| --- | --- | --- | --- |
| CWidgetStatsA | Solid gradient card, big value, delta, dropdown, sparkline/bar chart at the bottom | `color` (e.g. `primary-gradient`), slots `#value`, `#title`, `#action`, `#chart` | Hero KPIs (revenue, orders, customers, conversion) |
| CWidgetStatsB | White or `inverse` colored card with value, title, progress and helper text | `title`, `value`, `text`, `progress: { value, color }`, `color` + `inverse` | Goal completion KPIs |
| CWidgetStatsC | Icon top-right, value, uppercase title, progress | `#icon` (`height="36"`), `progress`, `color` + `inverse`; join several in CCardGroup | Compact stat strips |
| CWidgetStatsD | Colored cap with icon and background sparkline, two value/title pairs below | `values: [{ title, value }, …]`, `#icon` (`height="52"`), `#chart` with `position-absolute w-100 h-100`, `color` or `--cui-card-cap-bg` | Paired metrics per channel/branch |
| CWidgetStatsE | Small centered title/value with a tiny bar/line chart | `title`, `value`, default slot chart `style="height:40px;width:80px"` | Dense micro-trends grids (`:sm="4" :md="3" :xl="2"`) |
| CWidgetStatsF | Colored icon square + value + title, optional footer link | `color`, `title`, `value`, `#icon` (`size="xl"`), `#footer`, `:padding="false"` for edge-to-edge icon | Navigation KPIs ("12 pending invoices →") |

Widget rows: `CRow :xs="{ gutter: 4 }"`, columns `:sm="6" :xl="4" :xxl="3"` (four per
row on very wide screens), `class="mb-4"` on the row.

## Smart Table **PRO**

CSmartTable features shown: `table-filter`, `column-filter`, `column-sorter`, `cleaner`,
`pagination`, `items-per-page` + `items-per-page-select`, `clickable-rows`, `header`,
`footer`, `selectable` (+ `@selected-items-change`), `loading`, `no-items-label`,
custom cells via column-key slots, `#details` slot with CCollapse, column `_style` /
`_props`, `filter: false`, `sorter: false`, CSV download computed from filtered items.
Events: `active-page-change`, `sorter-change`, `table-filter-change`,
`column-filter-change`, `filtered-items-change`, `items-per-page-change`, `row-click`.
For business lists prefer the page-owned toolbar and server paging described in
[list-views.md](list-views.md) and [tables.md](tables.md).

## Charts

`@coreui/vue-chartjs`: CChart (`type`) and CChartLine, CChartBar, CChartPie,
CChartDoughnut, CChartRadar, CChartPolarArea, CChartBubble, CChartScatter. Mixed,
stacked, horizontal and area variants are Chart.js options. Full guidance in
[charts.md](charts.md).

## Extras (standalone pages)

| Page | Composition |
| --- | --- |
| Login | Centered column, logo above, `CCard class="p-4"`, form `row gy-3`, CPasswordInput, remember-me CFormCheck, full-width primary button, "or" divider, outline social buttons |
| Register | Same frame; name/email/password/confirm; terms CFormCheck |
| Magic-link login / sent, check email, reset/change password, password changed | Same frame; one message, one primary action |
| Two-factor authentication | COneTimePassword with six inputs, auto-submit on complete |
| 404 / 500 | Large number heading, message, search CInputGroup with icon prefix |

Background `bg-body-tertiary min-vh-100 d-flex align-items-center`. Exact frames, per-screen
anatomy and flows are in [authentication.md](authentication.md); the screens are UI only
until wired to the backend.

## Plugins

**FullCalendar** (`@fullcalendar/vue3` with day-grid, time-grid, interaction and the
classic theme plugin) inside a CCard. Header toolbar: prev/next/today, title, month/
week/day. Theme it by mapping `--fc-classic-*` variables to `--cui-*` variables in a
vendor SCSS partial (body background/color, border color, tertiary/secondary bgs,
primary for events, a translucent warning for today) with enough specificity to win
over the lazily loaded plugin CSS. Use it for appointments, deliveries, staff shifts.

## Apps

| App | Pattern to reuse |
| --- | --- |
| Invoice | CCard header with document number and right-floated small Save/Print buttons; three `:sm="4"` columns From/To/Details with `h6 class="mb-3"`; striped CTable with centered quantities and `text-end` money; totals table in a `:lg="4" :sm="5" class="ms-auto"` column; `window.print()` for print |
| Email (inbox, message, compose) | Alternate shell with its own CSidebar (folders with badges, labels) inside the standard header/footer; CButtonToolbar of CButtonGroups (archive, spam, delete, move, tag) above a message list; message rows with star action, from, date with attachment icon, subject `fs-5 fw-semibold` when unread, preview text, `border-bottom` separators |

Use the Invoice pattern for any printable document (quotes, orders, receipts) and the
Email pattern for inbox-like modules (tickets, approvals, notifications).
