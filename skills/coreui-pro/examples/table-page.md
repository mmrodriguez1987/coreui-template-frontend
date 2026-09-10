# Original local customer table

This local alternative uses built-in search; prefer the custom toolbar and remote
paging in [the main CRUD example](crud-page.md) for personalized business screens.

Use as `CustomerTable.vue` with a complete local collection of `{ id, name, email,
status }`. The parent owns loading/error/data and handles emitted actions. CSmartTable
owns free-text search, sorting and pagination; a domain status filter supplies its
input collection. There is no second manual slice. For server data, replace this
ownership model using [tables](../references/tables.md), not just the items prop.

```vue
<script setup>
import { computed, ref, useId, watch } from 'vue'

const props = defineProps({
  items: { type: Array, default: () => [] },
  loading: Boolean,
  error: { type: String, default: '' },
})
const emit = defineEmits(['create', 'edit', 'delete', 'retry'])
const status = ref('')
const page = ref(1)
const filterId = useId()
const filtered = computed(() => props.items.filter((item) => !status.value || item.status === status.value))
watch([status, () => props.items], () => { page.value = 1 })
const columns = [
  { key: 'name', label: 'Customer' },
  { key: 'email', label: 'Email' },
  { key: 'status', label: 'Status' },
  { key: 'actions', label: 'Actions', filter: false, sorter: false },
]
</script>

<template>
  <CCard class="mb-4">
    <CCardHeader class="d-flex flex-wrap align-items-center justify-content-between gap-2">
      <h2 class="h5 mb-0">Customer directory</h2>
      <CButton color="primary" type="button" :disabled="loading || !!error" @click="emit('create')">Create customer</CButton>
    </CCardHeader>
    <CCardBody>
      <CFormSelect :id="filterId" v-model="status" label="Status filter" class="mb-3">
        <option value="">All statuses</option>
        <option value="active">Active</option>
        <option value="paused">Paused</option>
      </CFormSelect>
      <div v-if="loading" role="status"><CSpinner size="sm" aria-hidden="true" /> Loading customers…</div>
      <CAlert v-else-if="error" color="danger" role="alert">
        {{ error }} <CButton type="button" color="danger" variant="outline" @click="emit('retry')">Retry</CButton>
      </CAlert>
      <p v-else-if="items.length === 0">No customers yet. Use Create customer to add one.</p>
      <CSmartTable v-else :items="filtered" :columns="columns" table-filter column-sorter cleaner
        pagination :items-per-page="10" :active-page="page"
        @active-page-change="page = $event" :table-props="{ responsive: true, hover: true }"
        no-items-label="No matching customers. Clear search or choose All statuses.">
        <template #status="{ item }">
          <td><CBadge :color="item.status === 'active' ? 'success' : 'secondary'">{{ item.status }}</CBadge></td>
        </template>
        <template #actions="{ item }">
          <td>
            <div class="d-flex gap-2">
              <CButton type="button" color="primary" variant="outline" size="sm" :aria-label="`Edit ${item.name}`"
                @click.stop="emit('edit', item)">Edit</CButton>
              <CButton type="button" color="danger" variant="outline" size="sm" :aria-label="`Delete ${item.name}`"
                @click.stop="emit('delete', item)">Delete</CButton>
            </div>
          </td>
        </template>
      </CSmartTable>
    </CCardBody>
  </CCard>
</template>
```

Check search plus status filter, no matches, last-page deletion, keyboard actions,
responsive overflow, and API failure supplied by the parent. The page shown in the
[local CRUD example](local-crud-page.md) replaces items after mutations so page state resets.
