# Dashboard blueprint (template layout, rich charts)

A dashboard must look like the template's main dashboard: dense, colorful but calm,
every region in a card, and many visualization types. Start with metric definitions,
units, time interval and data source; then fill this blueprint. Visual rules are in
[visual-design.md](visual-design.md), chart rules in [charts.md](charts.md).

## Section order (top to bottom)

1. **Hero KPI row** — four `CWidgetStatsA` with gradient colors (`primary-gradient`,
   `info-gradient`, `warning-gradient`, `danger-gradient`). `#value` shows the figure
   plus a `fs-6 fw-normal` delta with an arrow icon; `#title` the metric; `#action` a
   CDropdown (`cil-options`, white, `placement="bottom-end"`) with drill-down links;
   `#chart` a sparkline (line for the first two/last, bar for the third, area for one).
   Columns `:sm="6" :xl="4" :xxl="3"`, row `:xs="{ gutter: 4 }" class="mb-4"`.
2. **Main trend card** (`CCard class="mb-4"`):
   - Body header row: left `CCol :sm="5"` with `h4 class="card-title mb-0"` and a small
     muted period; right `CCol :sm="7" class="d-none d-md-flex align-items-center
     justify-content-end gap-3"` with a **CDateRangePicker** (with `ranges`) and a
     primary icon button (`cil-cloud-download`) for export.
   - Area/multi-line chart, 300 px, `margin-top: 40px`, series from theme colors,
     target as dashed line.
   - CCardFooter with 4–5 summary stats in a responsive row-cols grid: muted label,
     `fw-semibold text-truncate` value with percentage, `CProgress thin` with a
     `-gradient` color; hide the fifth below xl.
3. **Secondary KPI row** — choose one family per row: `CWidgetStatsD` (paired values with
   a background sparkline; use theme colors via `color`, not social brand hex),
   `CWidgetStatsF` (icon square + footer link to the filtered list), `CWidgetStatsB`
   (goal progress) or a `CCardGroup` of `CWidgetStatsC`.
4. **Chart gallery** — a `CRow :xs="{ gutter: 4 }" class="mb-4"` of chart cards
   (`:md="6" :xl="4"`, `h-100`), each with a CCardHeader title + muted small context and
   a fixed-height chart. Cover the shapes the data supports:
   stacked bar, horizontal bar (top N), mixed bar + line, doughnut, polar area or pie,
   radar, bubble or scatter. Each card states its unit and period.
5. **Breakdown card** ("Traffic & sales" pattern): two `:lg="6"` columns, each starting
   with two `border-start border-start-4 border-start-{color}` metric callouts, an
   `hr class="mt-0"`, then `progress-group` lists (paired thin bars per day, or icon +
   label + value + percentage rows).
6. **Detail table** at the bottom of that card or its own card:
   `CTable align="middle" class="mb-0 border" hover responsive`, `bg-body-secondary`
   header cells, CAvatar with status, two-line identity cells, usage column with value,
   period and thin gradient progress, icon cells (flags/payment/status), last activity.
7. Optional: CCalendar/FullCalendar card for schedules, CListGroup activity feed with
   `border-start-4` accents, CWidgetStatsE micro-trend grid for many small metrics.

## Choosing visuals per metric

| Metric question | Visual |
| --- | --- |
| Headline number + recent direction | CWidgetStatsA with sparkline |
| Progress toward a goal | CWidgetStatsB / CProgress / footer stat |
| Count with a link to act | CWidgetStatsF with footer |
| Trend over the selected range | Area/line main chart |
| Composition over time | Stacked bar |
| Ranking | Horizontal bar |
| Two scales (amount + rate) | Mixed bar + line |
| Share of total | Doughnut (≤ 6 slices) / pie / polar area |
| Multi-criteria comparison | Radar |
| Relationship between variables | Bubble / scatter |
| Per-record detail | Dashboard table |

A typical ERP dashboard (sales, inventory, finance) therefore shows 8–10 chart types.
If the backend lacks data for a shape, omit that card rather than inventing numbers.

## Behaviour

- One filter model (range, branch, etc.) drives every widget, chart and table. The
  CDateRangePicker updates `start`/`end`; requests are issued once both are set.
- Each card loads independently: CPlaceholder or spinner inside the card, partial
  errors with retry in the card, successful cards stay visible.
- Missing data is "not available", real zero is 0. Guard division by zero; bound
  progress values to a defined target.
- State comparison baselines (previous period, previous year) in the delta text.
- Charts refresh colors on theme change; test light and dark.
- Mobile: widgets stack two per row then one; chart cards stack; the header range
  picker is hidden below md in the template, so provide the filter elsewhere (e.g.
  above the cards) when mobile users need it.

The original [dashboard example](../examples/dashboard-page.md) implements this blueprint
with deterministic sample data and a theme-aware chart composable.
