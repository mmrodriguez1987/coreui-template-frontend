# Charts discovered in the Vue baseline

The app uses `@coreui/vue-chartjs` (CChart and typed CChartLine/Bar/Pie/Doughnut/Radar/
PolarArea wrappers), Chart.js 4, `@coreui/chartjs` styles and `@coreui/utils` getStyle.
Chart components are explicitly imported; CoreUI Vue Pro global registration alone
does not register the separate chart package. Do not introduce another chart library
for an ordinary line/bar chart this integration already handles.

Place reusable chart logic in a nearby child component. Derive labels and datasets
from supplied records/computed values, keeping options separate from domain data.
Match series lengths, sort time buckets, define missing observations, and format
labels/units consistently. Do not generate random data in a reactive computation.

Use getStyle to resolve the app's `--cui-*` colors once the DOM/theme is available.
The baseline listens for `ColorSchemeChange` on document.documentElement and accesses
the wrapper's chart instance to update options. In new code, use a named listener,
remove it on unmount, and verify the instance contract. Update dataset colors as well
as axis/grid/legend colors. Use valid Chart.js 4 option paths, not old copied options.

For `maintainAspectRatio: false`, give the chart or its container a deliberate height;
otherwise responsive layout can collapse or grow unexpectedly. Check rendering after
tab/modal visibility changes. Defer to the wrapper's lifecycle rather than creating
and leaking a second Chart.js instance.

Provide a text summary and units; chart color alone cannot communicate a series or
error. An error state and an empty series are different. The original
[dashboard example](../examples/dashboard-page.md) uses deterministic sample data;
real integrations need data fetching and theme-aware options as described here.
