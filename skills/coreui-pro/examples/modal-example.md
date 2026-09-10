# Original delete confirmation

Use as `DeleteCustomerModal.vue`. The parent owns `visible` and `customer`, keeps both
stable during deletion, and passes `remove(id)` which resolves only after deletion
succeeds. It handles `deleted(id)` by removing/refetching the record and closing the
dialog; `close` synchronizes visibility. This is an adapter contract, not a backend.
The installed baseline supports the pending-state backdrop/keyboard/header props below.

```vue
<script setup>
import { ref, useId, watch } from 'vue'

const props = defineProps({
  visible: Boolean,
  customer: { type: Object, default: null },
  remove: { type: Function, required: true },
})
const emit = defineEmits(['close', 'deleted'])
const titleId = useId()
const busy = ref(false)
const error = ref('')
watch(() => props.visible, (visible) => { if (visible) error.value = '' })

function close() {
  if (!busy.value) emit('close')
}
async function confirm() {
  if (busy.value || !props.customer) return
  const id = props.customer.id
  busy.value = true
  error.value = ''
  try {
    await props.remove(id)
    emit('deleted', id)
  } catch (reason) {
    error.value = reason instanceof Error ? reason.message : 'Deletion failed. Please retry.'
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <CModal :visible="visible" :aria-labelledby="titleId" :backdrop="busy ? 'static' : true"
    :keyboard="!busy" @close="close">
    <CModalHeader :close-button="!busy">
      <CModalTitle :id="titleId">Delete customer?</CModalTitle>
    </CModalHeader>
    <CModalBody :aria-busy="busy">
      <p>{{ customer?.name }} will be removed. Confirm this action to continue.</p>
      <CAlert v-if="error" color="danger" role="alert">{{ error }}</CAlert>
      <p v-if="busy" role="status">Deleting customer…</p>
    </CModalBody>
    <CModalFooter>
      <CButton type="button" color="secondary" variant="outline" :disabled="busy" @click="close">Cancel</CButton>
      <CButton type="button" color="danger" :disabled="busy || !customer" @click="confirm">Delete customer</CButton>
    </CModalFooter>
  </CModal>
</template>
```

Test cancel, Escape/backdrop, focus return, repeat clicks, rejection and retry. Do not
nest this dialog inside table rows: mount one dialog at page scope. Only remove the
row and announce success after the promise resolves.
