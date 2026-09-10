# Original customer form

This is an original Vue SFC teaching example, suitable as `CustomerForm.vue` in the
feature directory. It assumes the app registers CoreUI Vue Pro globally. The parent
passes `initial` (or null), and `save(draft)` which resolves to the saved server record
or rejects with an Error containing a user-safe message. Mount a fresh form per edit
session; do not replace initial while saving. No endpoint or persistence is supplied.
For APIs with structured field errors, adapt the catch block to their verified contract.

```vue
<script setup>
import { reactive, ref, useId } from 'vue'

const props = defineProps({
  initial: { type: Object, default: null },
  save: { type: Function, required: true },
})
const emit = defineEmits(['saved', 'cancel'])
const uid = useId()
const draft = reactive({ name: props.initial?.name ?? '', email: props.initial?.email ?? '' })
const attempted = ref(false)
const pending = ref(false)
const failure = ref('')

async function submit(event) {
  if (pending.value) return
  draft.name = draft.name.trim()
  draft.email = draft.email.trim()
  attempted.value = true
  if (!event.currentTarget.checkValidity() || !draft.name) return
  pending.value = true
  failure.value = ''
  try {
    const saved = await props.save({ name: draft.name, email: draft.email })
    emit('saved', saved)
  } catch (error) {
    failure.value = error instanceof Error ? error.message : 'Unable to save. Please retry.'
  } finally {
    pending.value = false
  }
}
</script>

<template>
  <CCard class="mb-4">
    <CCardHeader><h2 class="h5 mb-0">{{ initial ? 'Edit customer' : 'Create customer' }}</h2></CCardHeader>
    <CCardBody>
      <CAlert v-if="failure" color="danger" role="alert">{{ failure }}</CAlert>
      <CForm novalidate :validated="attempted" :aria-busy="pending" @submit.prevent="submit">
        <CFormInput
          :id="`${uid}-name`" v-model="draft.name" label="Customer name" required
          :disabled="pending" :invalid="attempted && !draft.name.trim()"
          feedback-invalid="Enter a customer name." class="mb-3"
        />
        <CFormInput
          :id="`${uid}-email`" v-model="draft.email" type="email" label="Email" required
          autocomplete="email" :disabled="pending" feedback-invalid="Enter a valid email."
          class="mb-3"
        />
        <div class="d-flex gap-2">
          <CButton type="submit" color="primary" :disabled="pending">
            {{ pending ? 'Saving…' : 'Save customer' }}
          </CButton>
          <CButton type="button" color="secondary" variant="outline" :disabled="pending" @click="emit('cancel')">
            Cancel
          </CButton>
        </div>
      </CForm>
    </CCardBody>
  </CCard>
</template>
```

Check empty/whitespace name, invalid email, rejected save, repeated submit, cancellation,
and successful returned data. Translate strings using the target's localization system.
Vue useId is available in the inspected Vue 3.5; use the target's ID convention on older Vue.
