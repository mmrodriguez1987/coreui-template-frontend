# Original personalized customer CRUD

This is the preferred business-screen example: a custom, consistent search/filter
card, server-owned results, contextual cells, modal editing and deletion. It applies
[the inspected personalized CRUD pattern](../references/custom-crud.md) using original
code. CoreUI supplies visual primitives; the application owns the business composition.
For a tiny complete local collection, see [the minimal alternative](local-crud-page.md).

Place the original [CustomerForm](form-page.md) and
[DeleteCustomerModal](modal-example.md) beside this page. The shell provides breadcrumbs.
The existing feature wrapper must supply api and its shared pageSize preference:

| Adapter method | Contract |
| --- | --- |
| list(query) | Resolve { items, page, pages, total }; page/pages are at least 1 even when empty |
| create(draft), update(id, draft) | Persist and resolve the canonical record |
| remove(id) | Resolve only after successful deletion |

Query keys here are search/status/sort/page/perPage. Map them to the actual Laravel
controller contract in your service; do not copy imaginary endpoints. Rejections expose
user-safe Error messages. Production adapters also map 422 errors to form fields.
Use the existing toast service instead of the inline success alert when available.

```vue
<script setup>
import { onMounted, onBeforeUnmount, reactive, ref, useId, watch } from 'vue'
import CustomerForm from './CustomerForm.vue'
import DeleteCustomerModal from './DeleteCustomerModal.vue'

const props = defineProps({
  api: { type: Object, required: true },
  pageSize: { type: Number, default: 15 },
})
const uid = useId()
const criteria = reactive({ search: '', status: '', sort: 'name', page: 1 })
const records = ref([])
const pages = ref(1)
const total = ref(0)
const loading = ref(true)
const error = ref('')
const notice = ref('')
const editorOpen = ref(false)
const initial = ref(null)
const saving = ref(false)
const detail = ref(null)
const deletion = ref(null)
let timer
let generation = 0

async function refresh() {
  clearTimeout(timer)
  const request = ++generation
  loading.value = true
  error.value = ''
  const query = { ...criteria, search: criteria.search.trim(), perPage: props.pageSize }
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
    if (request === generation) error.value = reason instanceof Error ? reason.message : 'Unable to load customers.'
  } finally {
    if (request === generation) loading.value = false
  }
}
function schedule(delay = 0) {
  clearTimeout(timer)
  generation++ // Invalidate an old response even during the debounce interval.
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
  Object.assign(criteria, { search: '', status: '', sort: 'name', page: 1 })
  schedule()
}
function go(page) {
  if (loading.value || page < 1 || page > pages.value || page === criteria.page) return
  criteria.page = page
  refresh()
}
function edit(record = null) {
  initial.value = record
  detail.value = null
  notice.value = ''
  editorOpen.value = true
}
async function persist(draft) {
  saving.value = true
  try {
    return await (initial.value ? props.api.update(initial.value.id, draft) : props.api.create(draft))
  } finally {
    saving.value = false
  }
}
function saved() {
  editorOpen.value = false
  notice.value = 'Customer saved.'
  refresh()
}
function removed() {
  deletion.value = null
  notice.value = 'Customer deleted.'
  refresh()
}
watch(() => props.pageSize, () => { criteria.page = 1; schedule() })
onMounted(refresh)
onBeforeUnmount(() => { clearTimeout(timer); generation++ })
</script>

<template>
  <div class="d-flex flex-wrap justify-content-between align-items-center gap-3 mb-4">
    <div><h1 class="h3">Customers</h1><p class="text-body-secondary mb-0">Manage customer profiles and availability.</p></div>
    <CButton type="button" color="primary" :disabled="loading || !!error" @click="edit()">Create customer</CButton>
  </div>
  <CCard class="mb-4">
    <CCardBody>
      <CRow class="g-3 align-items-end">
        <CCol :xs="12" :lg="5">
          <CFormInput :id="`${uid}-search`" :model-value="criteria.search" label="Search customers"
            placeholder="Name or email" @update:model-value="filter('search', $event)" />
        </CCol>
        <CCol :xs="12" :sm="6" :lg="3">
          <CFormSelect :id="`${uid}-status`" :model-value="criteria.status" label="Status"
            @update:model-value="filter('status', $event)">
            <option value="">All statuses</option><option value="active">Active</option><option value="paused">Paused</option>
          </CFormSelect>
        </CCol>
        <CCol :xs="12" :sm="6" :lg="3">
          <CFormSelect :id="`${uid}-sort`" :model-value="criteria.sort" label="Order by"
            @update:model-value="filter('sort', $event)">
            <option value="name">Name</option><option value="newest">Newest first</option>
          </CFormSelect>
        </CCol>
        <CCol :xs="12" :lg="1"><CButton type="button" color="secondary" variant="outline" @click="reset">Reset</CButton></CCol>
      </CRow>
    </CCardBody>
  </CCard>
  <CAlert v-if="notice" color="success" role="status">{{ notice }}</CAlert>
  <CCard>
    <CCardBody :aria-busy="loading">
      <p v-if="loading" role="status"><CSpinner size="sm" aria-hidden="true" /> Loading customers…</p>
      <CAlert v-else-if="error" color="danger" role="alert">
        {{ error }} <CButton type="button" color="danger" variant="outline" @click="refresh">Retry</CButton>
      </CAlert>
      <template v-else>
        <p class="text-body-secondary" role="status">{{ total }} customers found</p>
        <p v-if="!records.length">{{ criteria.search || criteria.status ? 'No matches. Adjust or reset filters.' : 'No customers yet. Create the first profile.' }}</p>
        <CTable v-else responsive hover>
          <CTableHead><CTableRow>
            <CTableHeaderCell scope="col">Customer</CTableHeaderCell>
            <CTableHeaderCell scope="col">Status</CTableHeaderCell>
            <CTableHeaderCell scope="col">Actions</CTableHeaderCell>
          </CTableRow></CTableHead>
          <CTableBody>
            <CTableRow v-for="record in records" :key="record.id">
              <CTableDataCell><div class="fw-semibold">{{ record.name }}</div><div class="small text-body-secondary">{{ record.email }}</div></CTableDataCell>
              <CTableDataCell><CBadge :color="record.status === 'active' ? 'success' : 'secondary'">{{ record.status }}</CBadge></CTableDataCell>
              <CTableDataCell><div class="d-flex flex-wrap gap-2">
                <CButton type="button" color="info" variant="outline" size="sm" :aria-label="`View ${record.name}`" @click="detail = record">View</CButton>
                <CButton type="button" color="primary" variant="outline" size="sm" :aria-label="`Edit ${record.name}`" @click="edit(record)">Edit</CButton>
                <CButton type="button" color="danger" variant="outline" size="sm" :aria-label="`Delete ${record.name}`" @click="notice = ''; deletion = record">Delete</CButton>
              </div></CTableDataCell>
            </CTableRow>
          </CTableBody>
        </CTable>
        <CPagination v-if="pages > 1" aria-label="Customer result pages">
          <CPaginationItem as="button" type="button" :disabled="criteria.page <= 1" @click="go(criteria.page - 1)">Previous</CPaginationItem>
          <CPaginationItem as="span" active aria-current="page">{{ criteria.page }} / {{ pages }}</CPaginationItem>
          <CPaginationItem as="button" type="button" :disabled="criteria.page >= pages" @click="go(criteria.page + 1)">Next</CPaginationItem>
        </CPagination>
      </template>
    </CCardBody>
  </CCard>
  <CModal :visible="editorOpen" :aria-labelledby="`${uid}-editor`" :backdrop="saving ? 'static' : true"
    :keyboard="!saving" @close="editorOpen = false">
    <CModalHeader :close-button="!saving"><CModalTitle :id="`${uid}-editor`">Customer profile</CModalTitle></CModalHeader>
    <CModalBody>
      <CustomerForm v-if="editorOpen" :initial="initial" :save="persist" @saved="saved" @cancel="editorOpen = false" />
    </CModalBody>
  </CModal>
  <CModal :visible="detail !== null" :aria-labelledby="`${uid}-detail`" @close="detail = null">
    <CModalHeader><CModalTitle :id="`${uid}-detail`">Customer details</CModalTitle></CModalHeader>
    <CModalBody v-if="detail"><h2 class="h5">{{ detail.name }}</h2><p>{{ detail.email }}</p><p>{{ detail.status }}</p></CModalBody>
  </CModal>
  <DeleteCustomerModal :visible="deletion !== null" :customer="deletion" :remove="(id) => api.remove(id)"
    @close="deletion = null" @deleted="removed" />
</template>
```

The table deliberately displays one complete server page with no second slicing,
filtering or sorting. Reuse an existing AppPagination wrapper instead of this compact
previous/next composition. CSmartTable with verified server processing is also suitable;
its stock search UI is not required. A product grid can display these same records
with CRow/CCol/CCard without changing the query, totals or current page.

The form is a standalone teaching component nested here for composition. In a real
project, reuse its modal form wrapper or extract form-only content to avoid duplicate
card headings. Adapt strings, money/date formatting and permissions to the target.
The adapter must enforce server authorization and return only records allowed to the user.

Check delayed/out-of-order responses, reset during search, page 2+, page-size changes,
last-page deletion, no matches vs no records, rejected save, modal cancellation and
keyboard/mobile operation. A successful mutation followed by failed refresh must show
both the saved/deleted notice and the retryable list error. These examples do not
provide a backend or claim browser validation.
