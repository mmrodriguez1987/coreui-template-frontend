# Dashboard composition

Start with metric definitions, units, time interval and data source. The baseline
combines CRow/CCol, CWidgetStats variants, chart cards, CDateRangePicker, CTable,
CProgress and status badges. Reuse existing widget/chart children before creating new
visual primitives. Native widgets are optional when a simple CCard better fits content.

Compose a responsive metric row, a primary trend section, then operational detail
such as a short table or progress group. Keep the shell's heading/breadcrumb ownership.
Use consistent card spacing and clear semantic headings. Avoid reproducing the demo's
branding, images, measurements or random values.

A date/status filter must update every dependent metric, chart and table consistently.
Keep one filter model and derive requests/computed series from it. State whether
comparison is previous interval, previous year or another baseline. Treat missing data
as unavailable, not zero; show real zeros correctly. Bound progress against a defined
target and guard division by zero.

Use placeholder/spinner states per independently loaded region when appropriate.
Show partial errors with retry rather than blanking successful content. Label units
and accessible chart summaries; offer a data table when users need precise values.
Check small-screen stacking and chart sizing in both color modes. See
[charts.md](charts.md) and the original [dashboard example](../examples/dashboard-page.md).
