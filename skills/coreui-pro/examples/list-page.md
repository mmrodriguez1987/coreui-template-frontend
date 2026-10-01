# Original catalog list: toolbar, quick filters, grid and table

This original example applies [the main-list guidance](../references/list-views.md): a
page-owned toolbar card (search, category, status, stock chips, sort, reset), a
grid/table switch over the same records, server totals and one query state. It is a
read-only list; pair it with the [CRUD page](crud-page.md) for create/edit/delete
modals and with [custom CRUD](../references/custom-crud.md) for conventions.

The page receives an adapter and the shared page-size preference from its feature wrapper:

| Adapter method | Contract |
| --- | --- |
| categories() | Resolve `[{ id, name }]` once for the category select |
| list(query) | Resolve `{ items, page, pages, total }`; page/pages at least 1 even when empty |

Query keys are search/category/status/stock/sort/page/perPage. Items expose
`id`, `name`, `sku`, `category`, `price`, `quantity`, `status`, `imageUrl`. Map these to the
real controller contract inside the service and read the backend allow-lists first.

```vue
<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref, useId, watch } from 'vue'

const props = defineProps({
  api: { type: Object, required: true },
  pageSize: { type: Number, default: 12 },
})

const uid = useId()
const defaults = { search: '', category: '', status: '', stock: '', sort: 'newest', page: 1 }
const criteria = reactive({ ...defaults })
const view = ref('grid')
const categories = ref([])
const records = ref([])
const pages = ref(1)
const total = ref(0)
const loading = ref(true)
const error = ref('')
let timer
let generation = 0

const stockChips = [
  { value: '', label: 'All', color: 'primary' },
  { value: 'low', label: 'Low stock', color: 'warning' },
  { value: 'out', label: 'Out of stock', color: 'danger' },
]
const filtered = computed(() => Boolean(criteria.search || criteria.category || criteria.status || criteria.stock))

function stockState(record) {
  if (record.quantity <= 0) return { label: 'Out of stock', color: 'danger' }
  if (record.quantity <= (record.minimum ?? 0)) return { label: 'Low stock', color: 'warning' }
  return { label: 'In stock', color: 'success' }
}

async function refresh() {
  clearTimeout(timer)
  const request = ++generation
  loading.value = true
  error.value = ''
  const query = {
    search: criteria.search.trim() || undefined,
    category: criteria.category || undefined,
    status: criteria.status || undefined,
    stock: criteria.stock || undefined,
    sort: criteria.sort,
    page: criteria.page,
    perPage: props.pageSize,
  }
  try {
    const result = await props.api.list(query)
    if (request !== generation) return
    if (query.page > result.pages) {
      criteria.page = result.pages
      await refresh()
      return
    }
    records.value = result.items
    pages.value = result.pages
    total.value = result.total
    criteria.page = result.page
  } catch (reason) {
    if (request === generation) error.value = reason instanceof Error ? reason.message : 'Unable to load products.'
  } finally {
    if (request === generation) loading.value = false
  }
}
function schedule(delay = 0) {
  clearTimeout(timer)
  generation++ // Invalidate older responses during the debounce interval too.
  loading.value = true
  error.value = ''
  timer = setTimeout(refresh, delay)
}
function filter(key, value) {
  criteria[key] = value
  criteria.page = 1
  schedule(key === 'search' ? 300 : 0)
}
function reset() {
  Object.assign(criteria, defaults)
  schedule()
}
function go(page) {
  if (loading.value || page < 1 || page > pages.value || page === criteria.page) return
  criteria.page = page
  refresh()
}
function hideBrokenImage(event) {
  event.target.hidden = true
}

watch(() => props.pageSize, () => { criteria.page = 1; schedule() })
onMounted(async () => {
  refresh()
  try { categories.value = await props.api.categories() } catch { categories.value = [] }
})
onBeforeUnmount(() => { clearTimeout(timer); generation++ })
</script>

<template>
  <div class="mb-4">
    <h1 class="h3">Products</h1>
    <p class="text-body-secondary mb-0">Browse the catalog and check availability.</p>
  </div>

  <CCard class="mb-4">
    <CCardBody>
      <CRow class="g-3 align-items-end">
        <CCol :xs="12" :lg="3">
          <CFormInput :id="`${uid}-search`" :model-value="criteria.search" label="Search"
            placeholder="Name, SKU or barcode" @update:model-value="filter('search', $event)" />
        </CCol>
        <CCol :xs="12" :sm="6" :lg="2">
          <CFormSelect :id="`${uid}-category`" :model-value="criteria.category" label="Category"
            @update:model-value="filter('category', $event)">
            <option value="">All categories</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
          </CFormSelect>
        </CCol>
        <CCol :xs="12" :sm="6" :lg="2">
          <CFormSelect :id="`${uid}-status`" :model-value="criteria.status" label="Status"
            @update:model-value="filter('status', $event)">
            <option value="">All statuses</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
            <option value="discontinued">Discontinued</option>
          </CFormSelect>
        </CCol>
        <CCol :xs="12" :sm="6" :lg="2">
          <CFormSelect :id="`${uid}-sort`" :model-value="criteria.sort" label="Order by"
            @update:model-value="filter('sort', $event)">
            <option value="newest">Newest first</option>
            <option value="name">Name</option>
            <option value="price">Price</option>
            <option value="quantity">Stock</option>
          </CFormSelect>
        </CCol>
        <CCol :xs="12" :sm="6" :lg="3">
          <CButton type="button" color="secondary" variant="outline" @click="reset">Reset</CButton>
        </CCol>
        <CCol :xs="12">
          <CButtonGroup role="group" aria-label="Stock level">
            <CButton v-for="chip in stockChips" :key="chip.value" type="button" size="sm"
              :color="criteria.stock === chip.value ? chip.color : 'secondary'"
              :variant="criteria.stock === chip.value ? undefined : 'outline'"
              :aria-pressed="criteria.stock === chip.value" @click="filter('stock', chip.value)">
              {{ chip.label }}
            </CButton>
          </CButtonGroup>
        </CCol>
      </CRow>
    </CCardBody>
  </CCard>

  <div class="d-flex justify-content-between align-items-center mb-3">
    <CButtonGroup role="group" aria-label="Display mode">
      <CButton type="button" :color="view === 'grid' ? 'primary' : 'secondary'"
        :variant="view === 'grid' ? undefined : 'outline'" :aria-pressed="view === 'grid'"
        @click="view = 'grid'">Grid</CButton>
      <CButton type="button" :color="view === 'table' ? 'primary' : 'secondary'"
        :variant="view === 'table' ? undefined : 'outline'" :aria-pressed="view === 'table'"
        @click="view = 'table'">Table</CButton>
    </CButtonGroup>
    <span class="text-body-secondary" role="status">{{ loading || error ? '' : `${total} products found` }}</span>
  </div>

  <p v-if="loading" role="status"><CSpinner size="sm" aria-hidden="true" /> Loading products…</p>
  <CAlert v-else-if="error" color="danger" role="alert">
    {{ error }} <CButton type="button" color="danger" variant="outline" size="sm" @click="refresh">Retry</CButton>
  </CAlert>
  <CCard v-else-if="!records.length">
    <CCardBody class="text-center py-5">
      <h2 class="h5">{{ filtered ? 'No products match' : 'No products yet' }}</h2>
      <p class="text-body-secondary">{{ filtered ? 'Adjust or reset the filters.' : 'Products will appear here once created.' }}</p>
      <CButton v-if="filtered" type="button" color="secondary" variant="outline" @click="reset">Reset filters</CButton>
    </CCardBody>
  </CCard>
  <template v-else>
    <CRow v-if="view === 'grid'" class="g-4">
      <CCol v-for="record in records" :key="record.id" :xs="12" :sm="6" :md="4" :lg="3">
        <CCard class="h-100">
          <img v-if="record.imageUrl" :src="record.imageUrl" :alt="record.name" class="card-img-top"
            style="aspect-ratio: 4 / 3; object-fit: cover" @error="hideBrokenImage" />
          <CCardBody class="d-flex flex-column">
            <div class="d-flex flex-wrap gap-1 mb-2">
              <CBadge :color="record.status === 'active' ? 'success' : 'secondary'">{{ record.status }}</CBadge>
              <CBadge :color="stockState(record).color">{{ stockState(record).label }}</CBadge>
            </div>
            <h2 class="h6">{{ record.name }}</h2>
            <p class="small text-body-secondary mb-2">{{ record.category }} · SKU {{ record.sku }}</p>
            <div class="d-flex justify-content-between mt-auto">
              <strong>{{ record.price }}</strong><span class="small">Stock: {{ record.quantity }}</span>
            </div>
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
    <CCard v-else>
      <CCardBody>
        <CTable responsive hover align="middle">
          <CTableHead><CTableRow>
            <CTableHeaderCell scope="col">Product</CTableHeaderCell>
            <CTableHeaderCell scope="col">SKU</CTableHeaderCell>
            <CTableHeaderCell scope="col">Category</CTableHeaderCell>
            <CTableHeaderCell scope="col">Price</CTableHeaderCell>
            <CTableHeaderCell scope="col">Stock</CTableHeaderCell>
            <CTableHeaderCell scope="col">Status</CTableHeaderCell>
          </CTableRow></CTableHead>
          <CTableBody>
            <CTableRow v-for="record in records" :key="record.id">
              <CTableDataCell class="fw-semibold">{{ record.name }}</CTableDataCell>
              <CTableDataCell>{{ record.sku }}</CTableDataCell>
              <CTableDataCell>{{ record.category }}</CTableDataCell>
              <CTableDataCell>{{ record.price }}</CTableDataCell>
              <CTableDataCell>
                {{ record.quantity }} <CBadge :color="stockState(record).color">{{ stockState(record).label }}</CBadge>
              </CTableDataCell>
              <CTableDataCell><CBadge :color="record.status === 'active' ? 'success' : 'secondary'">{{ record.status }}</CBadge></CTableDataCell>
            </CTableRow>
          </CTableBody>
        </CTable>
      </CCardBody>
    </CCard>
    <CPagination v-if="pages > 1" class="mt-3" aria-label="Product result pages">
      <CPaginationItem as="button" type="button" :disabled="criteria.page <= 1" @click="go(criteria.page - 1)">Previous</CPaginationItem>
      <CPaginationItem as="span" active aria-current="page">{{ criteria.page }} / {{ pages }}</CPaginationItem>
      <CPaginationItem as="button" type="button" :disabled="criteria.page >= pages" @click="go(criteria.page + 1)">Next</CPaginationItem>
    </CPagination>
  </template>
</template>
```

Grid and table render the same server page; switching modes keeps every criterion and
does not refetch. Reuse the project's pagination wrapper, formatters, i18n and toast
conventions instead of the compact controls above. For a stock-level list, drop the
create action, put the warehouse in a select beside search and use external column
sorting as described in the reference. The example has no backend and claims no browser
validation: check delayed responses, reset during search, page 2+, page-size changes,
empty versus no-match, image failures and keyboard/mobile operation.
