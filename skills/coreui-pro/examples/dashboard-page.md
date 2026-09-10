# Original compact dashboard

This original Vue SFC composes CoreUI grid, KPI widgets, a chart card and progress.
It assumes global CoreUI Pro registration and explicitly imports CChart. Its fixed
numbers are fictional, deterministic demonstration data, not live business metrics.
The shell supplies navigation and breadcrumbs. Real date filters must feed every
region consistently; see [dashboards](../references/dashboards.md).

```vue
<script setup>
import { CChart } from '@coreui/vue-chartjs'

const series = {
  labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
  datasets: [{ label: 'Resolved requests', data: [18, 25, 22, 31], borderWidth: 2 }],
}
const options = { responsive: true, maintainAspectRatio: false }
</script>

<template>
  <h1 class="h3 mb-4">Service overview</h1>
  <p class="text-body-secondary">Illustrative four-week reporting period</p>
  <CRow class="g-4 mb-4">
    <CCol :xs="12" :md="6">
      <CWidgetStatsB title="Resolved requests" value="96" :progress="{ value: 80, color: 'success' }"
        text="80% of the period target of 120" />
    </CCol>
    <CCol :xs="12" :md="6">
      <CWidgetStatsB title="Open requests" value="24" :progress="{ value: 40, color: 'warning' }"
        text="40% of the operational threshold of 60" />
    </CCol>
  </CRow>
  <CRow class="g-4">
    <CCol :xs="12" :lg="8">
      <CCard class="h-100">
        <CCardHeader><h2 class="h5 mb-0">Weekly resolutions</h2></CCardHeader>
        <CCardBody>
          <div class="resolution-chart"><CChart type="bar" :data="series" :options="options" /></div>
          <p class="text-body-secondary mt-3 mb-0">Resolved counts by week: 18, 25, 22, and 31.</p>
        </CCardBody>
      </CCard>
    </CCol>
    <CCol :xs="12" :lg="4">
      <CCard class="h-100">
        <CCardHeader><h2 class="h5 mb-0">Target completion</h2></CCardHeader>
        <CCardBody>
          <p>96 of 120 requests resolved</p>
          <CProgress :value="80" color="success" aria-label="Resolution target completion">80%</CProgress>
        </CCardBody>
      </CCard>
    </CCol>
  </CRow>
</template>

<style scoped>
.resolution-chart { height: 16rem; }
</style>
```

The single size rule gives the responsive canvas a bounded parent; it does not create
a competing visual system. This minimal chart uses library default colors. Before
shipping, adapt dataset/axis colors and theme refresh using [charts](../references/charts.md),
replace static metrics with data, and implement loading/error/empty states. Add an
operational CTable beneath the chart if the requested dashboard needs record-level detail.
