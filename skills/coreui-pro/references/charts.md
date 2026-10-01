# Charts with @coreui/vue-chartjs

The template uses `@coreui/vue-chartjs` 3 (Chart.js 4 with every controller registered),
`@coreui/chartjs` styles (CoreUI-styled custom tooltips, on by default through the
`customTooltips` prop) and `getStyle` from `@coreui/utils`. Import chart components
explicitly; global CoreUI Vue Pro registration does not include them. Never add a
second chart library.

## Every available chart and when to use it

| Chart | Component / config | Answer it gives | Business examples |
| --- | --- | --- | --- |
| Line | `CChartLine` or `CChart type="line"` | Trend over time | Daily sales, weekly orders |
| Area | line + `fill: true` + translucent `rgba(var(--cui-info-rgb), .1)` background | Trend with volume emphasis | Revenue this month (main dashboard chart) |
| Multi-line with target | several line datasets; target as flat dataset with `borderDash: [8, 5]`, `borderWidth: 1` | Actual vs goal | Sales vs quota |
| Sparkline | line/bar with hidden axes, legend off, no grid, `maintainAspectRatio: false`, 40–70 px tall | Micro trend inside a KPI | CWidgetStatsA/D/E charts |
| Bar | `CChartBar` | Compare categories or periods | Sales per month, per branch |
| Stacked bar | `scales.x.stacked` and `scales.y.stacked` = true | Composition per period | Orders by channel per month |
| Horizontal bar | `indexAxis: 'y'` | Ranked list with long labels | Top 10 products, top customers |
| Mixed bar + line | `CChart type="bar"` with one dataset `type: 'line'` (optionally second y axis `yAxisID`) | Volume and rate together | Units sold (bars) + margin % (line) |
| Doughnut | `CChartDoughnut`, `cutout` 60–75 % | Share of a whole, few slices (≤ 6) | Sales by category, payment methods |
| Pie | `CChartPie` | Share of a whole when the center label is not needed | Stock by warehouse |
| Polar area | `CChartPolarArea` | Magnitude per category with equal angles | Tickets by priority |
| Radar | `CChartRadar` | Multi-dimension profile, compare 2–3 entities | Supplier scorecard, branch KPIs |
| Bubble | `CChartBubble`, points `{ x, y, r }` | Three variables at once | Products: price × units × margin |
| Scatter | `CChartScatter`, points `{ x, y }` | Correlation/outliers | Discount vs order size |

Pick by question, not decoration, but **dashboards should exercise the full range** when
the domain has the data: a trend (area/line), a comparison (bar/stacked/horizontal), a
composition (doughnut/pie/polar), a profile (radar) and a relation (bubble/scatter),
plus sparklines in the KPI widgets. Progress groups and CWidgetStatsB/C cover ratios
that do not need a chart. See [dashboards.md](dashboards.md).

## Template styling conventions

- Colors only from theme variables: `getStyle('--cui-primary')`, `--cui-info`,
  `--cui-success`, `--cui-warning`, `--cui-danger`, `--cui-secondary`; translucent fills
  `rgba(${getStyle('--cui-info-rgb')}, .1)`. Category palettes cycle through those six.
- Axes: x grid `drawOnChartArea: false`; y `beginAtZero`, grid and border
  `--cui-border-color-translucent`; ticks `--cui-body-color`, y `maxTicksLimit: 5`.
- Lines: `tension: 0.4`, `borderWidth: 2`, points `radius: 0`, `hitRadius: 10`,
  `hoverRadius: 4`, `hoverBorderWidth: 3`.
- Legend hidden on the main chart (the card footer explains series); visible
  (`position: 'bottom'`) on composition charts.
- Inside gradient widgets: white translucent lines `rgba(255,255,255,.55)`, point
  color equal to the widget color, axes hidden.
- Main chart height 300 px with `margin-top: 40px`; gallery charts 240–280 px;
  sparklines 70 px (StatsA), full cap (StatsD), 40×80 px (StatsE).
- `maintainAspectRatio: false` always paired with a container or style height.

## Theme switching

The template listens for `ColorSchemeChange` on `document.documentElement` and updates
the chart instance exposed by the component ref (`chartRef.value.chart`). In new code:

1. Build options/datasets in a function that reads `getStyle` at call time.
2. Add a **named** listener on mount, remove it on unmount.
3. On change, recompute colors (axes **and** dataset colors) and call `chart.update()`
   or replace the reactive data/options so the wrapper re-renders.

A reusable composable for this is in the [dashboard example](../examples/dashboard-page.md).

## Data rules

Derive labels/datasets from records in computed properties; keep options separate.
Sort time buckets, align series lengths, use `null` for missing points (not 0), format
ticks/tooltips with the app's number/currency formatter (`ticks.callback`,
`plugins.tooltip.callbacks.label`). Never call `Math.random()` inside a computed.
Events `getElementAtEvent`, `getElementsAtEvent`, `getDatasetAtEvent` support
drill-down (click a bar → filtered list). Provide a visible text summary or a toggle
to a table for precise values; color alone must not carry meaning. Distinguish
loading (CPlaceholder/spinner), error (alert + retry) and empty (message) per chart card.
Check rendering after a hidden tab/modal becomes visible.
