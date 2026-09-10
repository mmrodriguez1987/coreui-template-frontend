# Minimal local-collection CRUD alternative

Use this smaller alternative only for an explicitly local collection. For the preferred
customized business screen, see [CRUD](crud-page.md).

This worked example composes the three original teaching components in this directory.
It is not a copied template screen or a complete backend application. Materialize the
Vue blocks as `CustomerTable.vue`, `CustomerForm.vue`, and `DeleteCustomerModal.vue`
next to this `CustomersPage.vue`, adapting names/placement to the existing feature.

The route's existing shell supplies breadcrumbs, header and navigation. Add one h1
here; use the routing/navigation references to expose `/customers` when requested.
The parent feature wrapper passes a real `api` adapter:

| Method | Required behavior |
| --- | --- |
| list() | Resolve the complete small collection, not one server page |
| create(draft) | Resolve a canonical record with stable id, name, email and status |
| update(id, draft) | Resolve that canonical record after successful persistence |
| remove(id) | Resolve only after successful deletion |

Each method rejects with a user-safe Error on failure. Adapt real API responses at
this boundary, including field errors where available. For a UI prototype, an explicit
in-memory adapter can implement this contract; state that it is not persistent.

```vue
<script setup>
import { onMounted, ref } from 'vue'
import CustomerTable from './CustomerTable.vue'
import CustomerForm from './CustomerForm.vue'
import DeleteCustomerModal from './DeleteCustomerModal.vue'

const props = defineProps({ api: { type: Object, required: true } })
const rows = ref([])
const loading = ref(false)
const failure = ref('')
const notice = ref('')
const editing = ref(false)
const initial = ref(null)
const deleting = ref(null)

async function load() {
  if (loading.value) return
  loading.value = true
  failure.value = ''
  try {
    rows.value = await props.api.list()
  } catch (error) {
    failure.value = error instanceof Error ? error.message : 'Unable to load customers.'
  } finally {
    loading.value = false
  }
}
function openForm(record = null) {
  initial.value = record
  notice.value = ''
  editing.value = true
}
function persist(draft) {
  return initial.value ? props.api.update(initial.value.id, draft) : props.api.create(draft)
}
function saved(record) {
  rows.value = initial.value
    ? rows.value.map((row) => row.id === record.id ? record : row)
    : [record, ...rows.value]
  editing.value = false
  notice.value = 'Customer saved.'
}
function removed(id) {
  rows.value = rows.value.filter((row) => row.id !== id)
  deleting.value = null
  notice.value = 'Customer deleted.'
}
onMounted(load)
</script>

<template>
  <h1 class="h3 mb-4">Customers</h1>
  <CAlert v-if="notice" color="success" role="status">{{ notice }}</CAlert>
  <CustomerForm v-if="editing" :initial="initial" :save="persist"
    @saved="saved" @cancel="editing = false" />
  <CustomerTable v-else :items="rows" :loading="loading" :error="failure"
    @create="openForm()" @edit="openForm" @delete="notice = ''; deleting = $event" @retry="load" />
  <DeleteCustomerModal :visible="deleting !== null" :customer="deleting"
    :remove="(id) => api.remove(id)" @close="deleting = null" @deleted="removed" />
</template>
```

The table disables creation while loading or after a list failure, preventing a late
initial list response from overwriting a newly saved record. Retry restores access.
This compact example keeps backend filtering, optimistic concurrency and navigation-away
handling outside its adapter contract; reuse those mechanisms if the actual app has them.

The interaction model is list → create/edit draft → validated save → returned record;
and list → selected stable ID → confirmation → successful delete → feedback. Cancel
leaves original data intact. Request failures preserve context. Use a toast service
instead of the success alert if the project already has one.

Validation scenarios: initial error/retry; empty collection; search/status no match;
invalid form; successful create/edit; rejected save retaining draft; cancel without
mutation; delete cancellation/rejection/success; final-row deletion; mobile/table
keyboard behavior. Never claim persistence until tested with the actual adapter.
