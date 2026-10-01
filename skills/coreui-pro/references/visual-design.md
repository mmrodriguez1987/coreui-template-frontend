# Visual language of the CoreUI Pro admin template

Goal: every screen an agent builds should look like it shipped with the licensed
CoreUI Pro Vue Admin Template (default theme, 5.9.0): calm tertiary background, white
cards with consistent rhythm, gradient accents used sparingly, linear `cil-*` icons,
and the same spacing in light and dark mode. This file describes that visual system
in original words; it is the default unless the target project already has its own.

## Shell geometry

| Region | How it is built | Detail that makes it look right |
| --- | --- | --- |
| Page background | `body { background-color: var(--cui-tertiary-bg) }`; dark mode uses `--cui-dark-bg-subtle` | Cards stand out as white/raised panels; never paint a page container another color |
| Sidebar | CSidebar `colorScheme="dark"`, `position="fixed"`, `class="border-end"`, unfoldable + visible from a store | Brand: full logo and narrow sygnet, both 32 px high; footer holds only CSidebarToggler (hidden below lg); a CCloseButton appears below lg |
| Header | CHeader `position="sticky"`, classes `mb-4 p-0`, adds `shadow-sm` only after scrolling | Two fluid containers with `px-4`: the first is the toolbar row with `border-bottom` (min-height 4 rem + 1 px), the second holds the breadcrumb (min-height 3 rem) |
| Header toolbar | Menu toggler, CSearchButton (hidden on xs), notification/task/message dropdowns (md+), vertical rule separators `vr`, language and color-mode dropdowns, account avatar, aside toggler | Toggler icons are `size="lg"`; dropdowns use `variant="nav-item"` and `placement="bottom-end"` with `:caret="false"` |
| Content | `<div class="body flex-grow-1"><CContainer class="px-4" lg>` around the router outlet | Pages never add their own outer container or horizontal padding |
| Footer | CFooter `class="px-4"`, min-height 3 rem + 1 px; left credit, right "powered by" with `ms-auto` | In dark mode the footer uses the body background |
| Aside | Right CSidebar (`border-start`) with an underline-border CNav of icon tabs and flush list groups | Section labels are list items with `bg-body-secondary text-uppercase small fw-semibold text-center`; entries use `border-start-4 border-start-{color}` |

The wrapper offsets itself with `padding-inline: var(--cui-sidebar-occupy-start) …`; do
not add sidebar widths inside pages.

## Spacing rhythm

- **Between page sections**: `mb-4` on every card and on every widget row.
- **Inside a row of widgets/cards**: `CRow :xs="{ gutter: 4 }"` (or `class="g-4"`).
- **Card content**: default CCardBody padding; avoid extra `p-*` wrappers. Use `mb-3`
  between groups inside a body, `mt-2` between a label and its thin progress.
- **Header to first content**: the header's own `mb-4` provides it; pages start
  directly with a widget row or a card, no top margin.
- **Forms**: `CForm class="row g-3"` (or `gy-3`), each control inside a CCol.
- **Auth pages**: centered `CCol :md="8" :lg="6" :xl="5"`, a `d-flex flex-column gap-4`
  stack, a `CCard class="p-4"` and full-width primary button.

## Cards

- Documentation-style header: `<CCardHeader><strong>Title</strong> <small>context</small></CCardHeader>`.
  Business screens may use a semantic heading instead (`h2 class="h5 mb-0"`), but keep
  the same weight contrast: bold title, muted small subtitle.
- Card titled inside the body (main chart card): `h4 class="card-title mb-0"` plus a
  `small text-body-secondary` period line, with controls aligned right in the same row.
- Footer for summaries: CCardFooter with a responsive `CRow :xs="{cols:1,gutter:4}"
  :sm="{cols:2}" :lg="{cols:4}" :xl="{cols:5}" class="mb-2 text-center"`.
- Equal heights in a row: `class="h-100"` on each card or a CCardGroup for joined panels.
- Help text under a header: `p class="text-body-secondary small"`.

## Typography and emphasis

| Use | Classes |
| --- | --- |
| KPI value inside a card | `fs-5 fw-semibold` (main figures) or `fw-semibold text-truncate` (footer stats) |
| Metric label | `text-body-secondary small text-truncate` |
| Section label in menus/dropdowns | `text-uppercase small fw-semibold` |
| Trend delta next to a value | `span class="fs-6 fw-normal"` with an arrow icon (`cil-arrow-top` / `cil-arrow-bottom`) |
| Secondary line in a table cell | `small text-body-secondary text-nowrap` |
| Muted meta (dates, counts) | `text-body-secondary` — never hard-coded greys |

## Color and accents

- Theme colors only through component `color` props and `--cui-*` variables
  (`getStyle('--cui-info')` in charts). No raw hex in business pages; the only raw
  colors in the template are third-party brand caps on social widgets.
- **Gradients** (`primary-gradient`, `info-gradient`, `warning-gradient`,
  `danger-gradient`, `success-gradient`) are reserved for the hero KPI widgets
  (CWidgetStatsA) and for thin progress bars. Badges in the header use `danger-gradient`.
- **Left-border callouts** for compact metrics: `div class="border-start border-start-4
  border-start-info py-1 px-3 mb-3"` containing a muted label and `fs-5 fw-semibold` value.
- **Progress**: `CProgress thin` with a `-gradient` color for dashboards; `progress-group`
  blocks (`progress-group-header`, `progress-group-prepend`, `progress-group-bars`)
  for paired or labelled bars.
- Status: CBadge with text (success/secondary/warning/danger), CAvatar `status` dot.
- Tables in dashboards: `CTable align="middle" class="mb-0 border" hover responsive`,
  head `class="text-nowrap"`, header cells `class="bg-body-secondary"`.

## Icons

- Sets: `cil-*` (linear UI icons) for everything functional, `cib-*` for brands
  (payment methods, social), `cif-*` for country flags.
- Registration: named imports from `@coreui/icons` collected into one icon set,
  provided globally (`app.provide('icons', icons)`) and rendered with the global
  CIcon. A new icon must be added to that set or it renders empty.
- Sizes: `size="lg"` in header togglers and dropdown rows, `size="xl"` inside
  CWidgetStatsF and flag/payment cells, `height="36"` in CWidgetStatsC, `height="52"`
  in CWidgetStatsD caps, plain inline (`class="me-2"`) inside buttons and menu items.
- Meaning by color class only in addition to text: `text-success`, `text-danger`,
  `text-info`, `text-warning`, `text-primary` on dropdown item icons.
- Icon-only buttons need `aria-label` or `title`.

Suggested domain icons: dashboard `cil-speedometer`, products `cil-tag`, inventory
`cil-storage`/`cil-layers`, sales `cil-cart`, invoices `cil-spreadsheet`, customers
`cil-people`, suppliers `cil-truck`, reports `cil-chart-pie`, settings `cil-settings`,
calendar `cil-calendar`, mail `cil-envelope-closed`, security `cil-lock-locked`.

## Navigation density: fewer collapsibles

The template sidebar is mostly flat. Follow the same shape:

1. A single top-level CNavItem for the dashboard (optionally a `NEW` info badge).
2. CNavTitle section labels ("UI elements", "Extras", "Plugins", "Apps" in the demo;
   in a business app e.g. "Operations", "Catalog", "Finance", "Administration").
3. Primary destinations as top-level CNavItem with an icon (charts, widgets, smart
   table are top-level in the demo even though they are large features).
4. CNavGroup only for a real family of four or more sibling pages (components,
   forms, icons, authentication). Group children have **no icons**; the renderer
   shows a bullet instead. Nest at most two levels.
5. Badges sparingly: `info`/`NEW` for new, `danger`/`PRO` for premium-only modules.

Do not wrap every module in its own collapsible; a group with one or two children
should be flattened into top-level items.

## Light and dark parity

Use `useColorModes` with the application's storage key; never a parallel toggle.
Check every new screen in both modes: no white-on-white text, chart grid/tick colors
updated on `ColorSchemeChange`, vendor widgets (FullCalendar, SimpleBar) mapped to
`--cui-*` variables as the template does.

## Never

- Native browser date/time inputs: use CDatePicker, CDateRangePicker or CTimePicker
  ([date-time.md](date-time.md)).
- Plain `<select multiple>`, hand-made tag inputs or star widgets when CMultiSelect,
  CChipInput or CRating exist.
- Custom box shadows, border radii or font sizes that diverge from the theme.
- Extra containers/padding around the router outlet; page-level background colors.
- Copying demo avatars, brand images, social colors or lorem text into business screens.

See also: [component catalog](component-catalog.md), [dashboards](dashboards.md),
[charts](charts.md), [layouts](layouts.md), [navigation](navigation.md).
