# Original sales dashboard with every chart type

This original example implements [the dashboard blueprint](../references/dashboards.md)
for a fictional retail business: gradient KPI widgets with sparklines, a main area chart
driven by a CDateRangePicker, footer stats, icon widgets, a gallery that uses every
chart type in `@coreui/vue-chartjs` (stacked bar, horizontal bar, mixed bar + line,
doughnut, pie, polar area, radar, bubble, scatter), progress groups and a detail table.
All numbers are deterministic sample data. The shell supplies header and breadcrumbs.

## Theme-aware chart composable

Place beside the page (for example `composables/useChartTheme.js`). Computed chart
configs read `version.value`, so they rebuild when the color mode changes; the chart
wrapper then updates its instance.

```js
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { getStyle } from '@coreui/utils'

export function useChartTheme() {
  const version = ref(0)
  const bump = () => { version.value++ }
  onMounted(() => document.documentElement.addEventListener('ColorSchemeChange', bump))
  onBeforeUnmount(() => document.documentElement.removeEventListener('ColorSchemeChange', bump))

  const color = (name) => getStyle(`--cui-${name}`)
  const tint = (name, alpha) => `rgba(${getStyle(`--cui-${name}-rgb`)}, ${alpha})`
  const palette = ['primary', 'info', 'success', 'warning', 'danger', 'secondary']
  const axes = () => ({
    x: { grid: { color: color('border-color-translucent'), drawOnChartArea: false }, ticks: { color: color('body-color') } },
    y: {
      beginAtZero: true,
      border: { color: color('border-color-translucent') },
      grid: { color: color('border-color-translucent') },
      ticks: { color: color('body-color'), maxTicksLimit: 5 },
    },
  })
  const legend = (display = true) => ({ display, position: 'bottom', labels: { color: color('body-color') } })
  const sparkline = (min, max) => ({
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: { x: { display: false }, y: { display: false, min, max } },
    elements: { line: { borderWidth: 2, tension: 0.4 }, point: { radius: 0, hitRadius: 10, hoverRadius: 4 } },
  })
  return { version, color, tint, palette, axes, legend, sparkline }
}
```

## Page

```vue
<script setup>
import { computed, reactive } from 'vue'
import { CChart } from '@coreui/vue-chartjs'
import { useChartTheme } from './composables/useChartTheme'

const theme = useChartTheme()
const { color, tint, palette, axes, legend, sparkline } = theme

const today = new Date(2026, 8, 30)
const daysAgo = (n) => new Date(today.getFullYear(), today.getMonth(), today.getDate() - n)
const ranges = {
  'Last 7 days': [daysAgo(6), today],
  'Last 30 days': [daysAgo(29), today],
  'This quarter': [new Date(2026, 6, 1), today],
  'This year': [new Date(2026, 0, 1), today],
}
const period = reactive({ start: new Date(2026, 3, 1), end: today })
function setRange(key, value) {
  period[key] = value ? new Date(value) : null
  // A real page refetches every region once both ends are set or both are cleared.
}

const months = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']
const kpis = [
  { title: 'Revenue', value: '$184.2K', delta: '+8.1%', color: 'primary', type: 'line', data: [22, 27, 25, 31, 34, 38] },
  { title: 'Orders', value: '3,415', delta: '+4.6%', color: 'info', type: 'line', data: [480, 530, 510, 590, 640, 665] },
  { title: 'Average ticket', value: '$53.90', delta: '-1.2%', color: 'warning', type: 'bar', data: [56, 55, 54, 55, 54, 53] },
  { title: 'Returns', value: '1.8%', delta: '-0.4 pts', color: 'danger', type: 'line', data: [2.6, 2.4, 2.3, 2.1, 2, 1.8], fill: true },
]
const kpiChart = (kpi) => {
  theme.version.value // Rebuild on color-mode change.
  return {
    labels: months,
    datasets: [{
      label: kpi.title,
      data: kpi.data,
      backgroundColor: kpi.type === 'bar' || kpi.fill ? 'rgba(255,255,255,.2)' : 'transparent',
      borderColor: 'rgba(255,255,255,.55)',
      pointBackgroundColor: color(kpi.color),
      fill: Boolean(kpi.fill),
      barPercentage: 0.6,
    }],
  }
}
const kpiOptions = (kpi) => sparkline(Math.min(...kpi.data) * 0.9, Math.max(...kpi.data) * 1.05)

const mainChart = computed(() => {
  theme.version.value
  return {
    data: {
      labels: months,
      datasets: [
        { label: 'Store sales', data: [118, 126, 131, 140, 152, 161], borderColor: color('info'), backgroundColor: tint('info', 0.1), fill: true, borderWidth: 2 },
        { label: 'Online sales', data: [42, 49, 55, 61, 66, 74], borderColor: color('success'), backgroundColor: 'transparent', borderWidth: 2 },
        { label: 'Target', data: [150, 150, 150, 150, 150, 150], borderColor: color('danger'), backgroundColor: 'transparent', borderWidth: 1, borderDash: [8, 5] },
      ],
    },
    options: {
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: axes(),
      elements: { line: { tension: 0.4 }, point: { radius: 0, hitRadius: 10, hoverRadius: 4, hoverBorderWidth: 3 } },
    },
  }
})
const footerStats = [
  { title: 'Store', value: '$128.4K', percent: 70, color: 'info' },
  { title: 'Online', value: '$55.8K', percent: 30, color: 'success' },
  { title: 'New customers', value: '612', percent: 44, color: 'warning' },
  { title: 'Repeat customers', value: '1,402', percent: 56, color: 'danger' },
  { title: 'Gross margin', value: '$61.7K', percent: 33.5, color: 'primary' },
]
const actionWidgets = [
  { title: 'Pending invoices', value: '27', icon: 'cil-spreadsheet', color: 'primary' },
  { title: 'Low-stock products', value: '14', icon: 'cil-storage', color: 'warning' },
  { title: 'Open purchase orders', value: '9', icon: 'cil-truck', color: 'info' },
  { title: 'Overdue receivables', value: '$8.3K', icon: 'cil-bell', color: 'danger' },
]

const gallery = computed(() => {
  theme.version.value
  const pie = (labels, data) => ({
    data: { labels, datasets: [{ data, backgroundColor: labels.map((_, i) => color(palette[i])), borderColor: color('body-bg') }] },
    options: { maintainAspectRatio: false, plugins: { legend: legend() } },
  })
  const radial = () => ({
    ticks: { display: false },
    grid: { color: color('border-color-translucent') },
    angleLines: { color: color('border-color-translucent') },
    pointLabels: { color: color('body-color') },
  })
  return [
    {
      key: 'stacked', title: 'Orders by channel', note: 'Orders per month', type: 'bar',
      data: { labels: months, datasets: ['Store', 'Web', 'Marketplace'].map((label, i) => ({ label, data: [[300, 320, 310, 350, 370, 380], [120, 140, 135, 160, 180, 190], [60, 70, 65, 80, 90, 95]][i], backgroundColor: color(palette[i]) })) },
      options: { maintainAspectRatio: false, plugins: { legend: legend() }, scales: { x: { ...axes().x, stacked: true }, y: { ...axes().y, stacked: true } } },
    },
    {
      key: 'ranking', title: 'Top products', note: 'Units sold, last 30 days', type: 'bar',
      data: { labels: ['Espresso beans 1 kg', 'Ceramic mug', 'Cold brew pack', 'Pour-over kit', 'Paper filters'], datasets: [{ label: 'Units', data: [412, 356, 298, 214, 187], backgroundColor: color('info'), borderRadius: 4 }] },
      options: { indexAxis: 'y', maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: axes().y, y: { ...axes().x, grid: { display: false } } } },
    },
    {
      key: 'mixed', title: 'Units and margin', note: 'Bars: units · line: margin %', type: 'bar',
      data: {
        labels: months,
        datasets: [
          { type: 'bar', label: 'Units', data: [2100, 2300, 2250, 2500, 2700, 2850], backgroundColor: tint('primary', 0.7), yAxisID: 'y' },
          { type: 'line', label: 'Margin %', data: [31, 32, 30, 33, 34, 35], borderColor: color('success'), backgroundColor: color('success'), tension: 0.4, yAxisID: 'y1' },
        ],
      },
      options: { maintainAspectRatio: false, plugins: { legend: legend() }, scales: { x: axes().x, y: axes().y, y1: { ...axes().y, position: 'right', grid: { drawOnChartArea: false } } } },
    },
    { key: 'doughnut', title: 'Sales by category', note: 'Share of revenue', type: 'doughnut', ...pie(['Coffee', 'Equipment', 'Tea', 'Accessories'], [46, 24, 18, 12]), extra: { cutout: '70%' } },
    { key: 'pie', title: 'Payment methods', note: 'Share of transactions', type: 'pie', ...pie(['Card', 'Cash', 'Transfer', 'Wallet'], [58, 17, 11, 14]) },
    { key: 'polar', title: 'Tickets by priority', note: 'Open support tickets', type: 'polarArea', ...pie(['Low', 'Normal', 'High', 'Urgent'], [18, 32, 11, 4]), extra: { scales: { r: radial() } } },
    {
      key: 'radar', title: 'Supplier scorecard', note: 'Score out of 10', type: 'radar',
      data: {
        labels: ['Price', 'Quality', 'Lead time', 'Accuracy', 'Support', 'Terms'],
        datasets: [
          { label: 'Supplier A', data: [8, 9, 6, 9, 7, 8], borderColor: color('primary'), backgroundColor: tint('primary', 0.2), pointBackgroundColor: color('primary') },
          { label: 'Supplier B', data: [9, 6, 8, 7, 8, 6], borderColor: color('warning'), backgroundColor: tint('warning', 0.2), pointBackgroundColor: color('warning') },
        ],
      },
      options: { maintainAspectRatio: false, plugins: { legend: legend() }, scales: { r: { ...radial(), min: 0, max: 10 } } },
    },
    {
      key: 'bubble', title: 'Product portfolio', note: 'Price × units · size: margin', type: 'bubble',
      data: { datasets: [
        { label: 'Coffee', data: [{ x: 18, y: 412, r: 14 }, { x: 24, y: 298, r: 11 }], backgroundColor: tint('primary', 0.6) },
        { label: 'Equipment', data: [{ x: 65, y: 214, r: 9 }, { x: 120, y: 88, r: 16 }], backgroundColor: tint('success', 0.6) },
        { label: 'Accessories', data: [{ x: 12, y: 356, r: 6 }, { x: 7, y: 187, r: 4 }], backgroundColor: tint('warning', 0.6) },
      ] },
      options: { maintainAspectRatio: false, plugins: { legend: legend() }, scales: axes() },
    },
    {
      key: 'scatter', title: 'Discount vs basket size', note: 'Each point is an order', type: 'scatter',
      data: { datasets: [{ label: 'Orders', data: [[0, 34], [5, 41], [5, 38], [10, 52], [10, 47], [15, 58], [20, 61], [20, 72], [25, 66], [30, 80]].map(([x, y]) => ({ x, y })), backgroundColor: color('info') }] },
      options: { maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: axes() },
    },
  ].map((chart) => ({ ...chart, options: { ...chart.options, ...chart.extra } }))
})

const weekdays = [
  { day: 'Monday', store: 42, online: 61 }, { day: 'Tuesday', store: 55, online: 70 },
  { day: 'Wednesday', store: 48, online: 66 }, { day: 'Thursday', store: 63, online: 74 },
  { day: 'Friday', store: 78, online: 82 }, { day: 'Saturday', store: 91, online: 58 },
]
const regions = [
  { name: 'North', icon: 'cil-location-pin', value: '$62.1K', percent: 34 },
  { name: 'Center', icon: 'cil-location-pin', value: '$71.4K', percent: 39 },
  { name: 'South', icon: 'cil-location-pin', value: '$50.7K', percent: 27 },
]
const topCustomers = [
  { id: 1, name: 'Northwind Cafés', initials: 'NC', status: 'success', since: 'Mar 2024', segment: 'Wholesale', usage: 82, color: 'success', last: '2 hours ago' },
  { id: 2, name: 'Blue Door Bakery', initials: 'BD', status: 'warning', since: 'Jan 2025', segment: 'Retail', usage: 54, color: 'info', last: 'Yesterday' },
  { id: 3, name: 'Harbor Hotel Group', initials: 'HH', status: 'success', since: 'Aug 2023', segment: 'Hospitality', usage: 67, color: 'warning', last: '3 days ago' },
  { id: 4, name: 'Campus Kiosk', initials: 'CK', status: 'secondary', since: 'Jun 2026', segment: 'Retail', usage: 21, color: 'danger', last: 'Last week' },
]
</script>

<template>
  <CRow :xs="{ gutter: 4 }" class="mb-4">
    <CCol v-for="kpi in kpis" :key="kpi.title" :sm="6" :xl="4" :xxl="3">
      <CWidgetStatsA :color="`${kpi.color}-gradient`">
        <template #value>
          {{ kpi.value }}
          <span class="fs-6 fw-normal">({{ kpi.delta }} <CIcon :icon="kpi.delta.startsWith('-') ? 'cil-arrow-bottom' : 'cil-arrow-top'" />)</span>
        </template>
        <template #title>{{ kpi.title }}</template>
        <template #action>
          <CDropdown placement="bottom-end">
            <CDropdownToggle color="transparent" class="p-0 text-white" :caret="false" :aria-label="`${kpi.title} options`">
              <CIcon icon="cil-options" class="text-white" />
            </CDropdownToggle>
            <CDropdownMenu>
              <CDropdownItem as="button" type="button">View report</CDropdownItem>
              <CDropdownItem as="button" type="button">Export CSV</CDropdownItem>
            </CDropdownMenu>
          </CDropdown>
        </template>
        <template #chart>
          <CChart :type="kpi.type" class="mt-3 mx-3" style="height: 70px" :data="kpiChart(kpi)" :options="kpiOptions(kpi)" />
        </template>
      </CWidgetStatsA>
    </CCol>
  </CRow>

  <CCard class="mb-4">
    <CCardBody>
      <CRow>
        <CCol :sm="5">
          <h4 class="card-title mb-0">Sales</h4>
          <div class="small text-body-secondary">April – September 2026</div>
        </CCol>
        <CCol :sm="7" class="d-none d-md-flex align-items-center justify-content-end gap-3">
          <CDateRangePicker :start-date="period.start" :end-date="period.end" :ranges="ranges" locale="en-US"
            cleaner @update:start-date="setRange('start', $event)" @update:end-date="setRange('end', $event)" />
          <CButton color="primary" aria-label="Download sales report"><CIcon icon="cil-cloud-download" /></CButton>
        </CCol>
      </CRow>
      <div style="height: 300px; margin-top: 40px">
        <CChart type="line" :data="mainChart.data" :options="mainChart.options" />
      </div>
    </CCardBody>
    <CCardFooter>
      <CRow :xs="{ cols: 1, gutter: 4 }" :sm="{ cols: 2 }" :lg="{ cols: 4 }" :xl="{ cols: 5 }" class="mb-2 text-center">
        <CCol v-for="(stat, index) in footerStats" :key="stat.title" :class="{ 'd-none d-xl-block': index === footerStats.length - 1 }">
          <div class="text-body-secondary">{{ stat.title }}</div>
          <div class="fw-semibold text-truncate">{{ stat.value }} ({{ stat.percent }}%)</div>
          <CProgress class="mt-2" thin :color="`${stat.color}-gradient`" :value="stat.percent" :aria-label="stat.title" />
        </CCol>
      </CRow>
    </CCardFooter>
  </CCard>

  <CRow :xs="{ gutter: 4 }" class="mb-4">
    <CCol v-for="widget in actionWidgets" :key="widget.title" :sm="6" :xl="3">
      <CWidgetStatsF :color="widget.color" :title="widget.title" :value="widget.value">
        <template #icon><CIcon :icon="widget.icon" size="xl" /></template>
        <template #footer>
          <a class="font-xs fw-semibold text-body-secondary d-flex justify-content-between align-items-center" href="#">
            View all <CIcon icon="cil-arrow-right" width="16" />
          </a>
        </template>
      </CWidgetStatsF>
    </CCol>
  </CRow>

  <CRow :xs="{ gutter: 4 }" class="mb-4">
    <CCol v-for="chart in gallery" :key="chart.key" :md="6" :xl="4">
      <CCard class="h-100">
        <CCardHeader><strong>{{ chart.title }}</strong> <small class="text-body-secondary">{{ chart.note }}</small></CCardHeader>
        <CCardBody>
          <div style="height: 260px"><CChart :type="chart.type" :data="chart.data" :options="chart.options" /></div>
        </CCardBody>
      </CCard>
    </CCol>
  </CRow>

  <CCard class="mb-4">
    <CCardHeader><strong>Sales breakdown</strong> <small class="text-body-secondary">Last 30 days</small></CCardHeader>
    <CCardBody>
      <CRow>
        <CCol :xs="12" :lg="6">
          <CRow>
            <CCol :xs="6">
              <div class="border-start border-start-4 border-start-info py-1 px-3 mb-3">
                <div class="text-body-secondary text-truncate small">Store tickets</div>
                <div class="fs-5 fw-semibold">2,318</div>
              </div>
            </CCol>
            <CCol :xs="6">
              <div class="border-start border-start-4 border-start-danger py-1 px-3 mb-3">
                <div class="text-body-secondary text-truncate small">Online orders</div>
                <div class="fs-5 fw-semibold">1,097</div>
              </div>
            </CCol>
          </CRow>
          <hr class="mt-0" />
          <div v-for="row in weekdays" :key="row.day" class="progress-group mb-4">
            <div class="progress-group-prepend"><span class="text-body-secondary small">{{ row.day }}</span></div>
            <div class="progress-group-bars">
              <CProgress thin color="info-gradient" :value="row.store" :aria-label="`${row.day} store`" />
              <CProgress thin color="danger-gradient" :value="row.online" :aria-label="`${row.day} online`" />
            </div>
          </div>
        </CCol>
        <CCol :xs="12" :lg="6">
          <CRow>
            <CCol :xs="6">
              <div class="border-start border-start-4 border-start-warning py-1 px-3 mb-3">
                <div class="text-body-secondary text-truncate small">Units sold</div>
                <div class="fs-5 fw-semibold">14,702</div>
              </div>
            </CCol>
            <CCol :xs="6">
              <div class="border-start border-start-4 border-start-success py-1 px-3 mb-3">
                <div class="text-body-secondary text-truncate small">Gross margin</div>
                <div class="fs-5 fw-semibold">33.5%</div>
              </div>
            </CCol>
          </CRow>
          <hr class="mt-0" />
          <div v-for="region in regions" :key="region.name" class="progress-group">
            <div class="progress-group-header">
              <CIcon :icon="region.icon" class="me-2" size="lg" />
              <span class="title">{{ region.name }}</span>
              <span class="ms-auto fw-semibold">{{ region.value }} <span class="text-body-secondary small">({{ region.percent }}%)</span></span>
            </div>
            <div class="progress-group-bars"><CProgress thin color="success-gradient" :value="region.percent" :aria-label="region.name" /></div>
          </div>
        </CCol>
      </CRow>
      <br />
      <CTable align="middle" class="mb-0 border" hover responsive>
        <CTableHead class="text-nowrap">
          <CTableRow>
            <CTableHeaderCell class="bg-body-secondary text-center"><CIcon icon="cil-people" /><span class="visually-hidden">Avatar</span></CTableHeaderCell>
            <CTableHeaderCell class="bg-body-secondary">Customer</CTableHeaderCell>
            <CTableHeaderCell class="bg-body-secondary">Credit used</CTableHeaderCell>
            <CTableHeaderCell class="bg-body-secondary">Activity</CTableHeaderCell>
          </CTableRow>
        </CTableHead>
        <CTableBody>
          <CTableRow v-for="customer in topCustomers" :key="customer.id">
            <CTableDataCell class="text-center"><CAvatar size="md" color="secondary" text-color="white" :status="customer.status">{{ customer.initials }}</CAvatar></CTableDataCell>
            <CTableDataCell>
              <div>{{ customer.name }}</div>
              <div class="small text-body-secondary text-nowrap">{{ customer.segment }} | Customer since {{ customer.since }}</div>
            </CTableDataCell>
            <CTableDataCell>
              <div class="d-flex justify-content-between align-items-baseline">
                <div class="fw-semibold">{{ customer.usage }}%</div>
                <div class="text-nowrap small text-body-secondary ms-3">of credit limit</div>
              </div>
              <CProgress thin :color="`${customer.color}-gradient`" :value="customer.usage" :aria-label="`${customer.name} credit used`" />
            </CTableDataCell>
            <CTableDataCell>
              <div class="small text-body-secondary">Last order</div>
              <div class="fw-semibold text-nowrap">{{ customer.last }}</div>
            </CTableDataCell>
          </CTableRow>
        </CTableBody>
      </CTable>
    </CCardBody>
  </CCard>
</template>
```

## Adapting it

- Replace the sample arrays with service calls keyed by `period`; load each card
  independently with CPlaceholder skeletons and an in-card retry alert.
- Format money/percentages with the app's i18n formatters and translate every label.
- Register every icon used (`cil-arrow-top`, `cil-arrow-bottom`, `cil-options`,
  `cil-cloud-download`, `cil-spreadsheet`, `cil-storage`, `cil-truck`, `cil-bell`,
  `cil-arrow-right`, `cil-location-pin`, `cil-people`) in the app's icon set.
- Drop gallery cards whose data the backend cannot supply instead of inventing values;
  wire footer links (`View all`) to the filtered list routes.
- The header range picker is hidden below md as in the template; provide a mobile filter
  if needed. Check light/dark mode: the composable rebuilds chart colors on change.

This is a syntax-checked teaching example, not a browser-validated page.
