# Original login page (template Frame A)

This original page reproduces the template's primary authentication frame described in
[authentication.md](../references/authentication.md) and makes it functional: bound
fields, explicit field validation, pending state, field and form errors, and a safe redirect.
Register it outside the admin layout. The same frame serves the register page
(name/email/password/terms) with the switch link reversed.

The parent route or wrapper supplies an adapter:

| Adapter member | Contract |
| --- | --- |
| login({ email, password, remember }) | Resolves `{ twoFactor: boolean }` on success; rejects with `{ message, fields }` where `fields` maps names to messages (from Laravel 422) |
| providers | Optional array `[{ id, label, icon }]`; omit to hide the divider and provider buttons |
| startProvider(id) | Begins an OAuth/SSO redirect for that provider |

```vue
<script setup>
import { reactive, ref, useId } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const props = defineProps({
  auth: { type: Object, required: true },
  logo: { type: [Array, String], default: null },
})

const uid = useId()
const route = useRoute()
const router = useRouter()
const form = reactive({ email: '', password: '', remember: false })
const fieldErrors = reactive({ email: '', password: '' })
const error = ref('')
const pending = ref(false)

// Explicit per-field errors: no green "valid" styling before submit, and the same
// invalid/feedbackInvalid path serves client checks and Laravel 422 messages.
function clientErrors() {
  return {
    email: /^\S+@\S+\.\S+$/.test(form.email.trim()) ? '' : 'Enter a valid email address.',
    password: form.password ? '' : 'Enter your password.',
  }
}

function safeRedirect() {
  const target = typeof route.query.redirect === 'string' ? route.query.redirect : ''
  return target.startsWith('/') && !target.startsWith('//') ? target : '/dashboard'
}

async function submit() {
  if (pending.value) return
  Object.assign(fieldErrors, clientErrors())
  if (fieldErrors.email || fieldErrors.password) return
  pending.value = true
  error.value = ''
  try {
    const result = await props.auth.login({ email: form.email.trim(), password: form.password, remember: form.remember })
    await router.replace(result?.twoFactor ? { name: 'two-factor', query: route.query } : safeRedirect())
  } catch (reason) {
    form.password = ''
    Object.assign(fieldErrors, reason?.fields ?? {})
    error.value = reason?.message || 'We could not sign you in. Check your details and try again.'
  } finally {
    pending.value = false
  }
}
</script>

<template>
  <div class="bg-body-tertiary min-vh-100 d-flex flex-row align-items-center">
    <CContainer>
      <CRow class="justify-content-center">
        <CCol :md="8" :lg="6" :xl="5">
          <div class="d-flex flex-column gap-4">
            <div v-if="logo" class="text-center"><CIcon :icon="logo" height="48" /></div>
            <CCard class="p-4">
              <CCardBody class="d-flex flex-column gap-4">
                <h1 class="h5 text-center mb-0">Sign in to your account</h1>
                <CAlert v-if="error" color="danger" class="mb-0" role="alert">{{ error }}</CAlert>
                <CForm class="row gy-3" novalidate @submit.prevent="submit">
                  <CCol :xs="12">
                    <CFormLabel :for="`${uid}-email`">Email address</CFormLabel>
                    <CFormInput :id="`${uid}-email`" v-model="form.email" type="email" required
                      placeholder="name@company.com" autocomplete="email"
                      :invalid="!!fieldErrors.email" :feedback-invalid="fieldErrors.email" />
                  </CCol>
                  <CCol :xs="12">
                    <div class="d-flex justify-content-between">
                      <CFormLabel :for="`${uid}-password`">Password</CFormLabel>
                      <RouterLink :to="{ name: 'reset-password' }">Forgot password?</RouterLink>
                    </div>
                    <CPasswordInput :id="`${uid}-password`" v-model="form.password" required
                      placeholder="Your password" autocomplete="current-password"
                      :invalid="!!fieldErrors.password" :aria-describedby="`${uid}-password-error`" />
                    <!-- CPasswordInput renders its feedback outside the input wrapper, so the
                         Bootstrap sibling rule never reveals it; show the message explicitly. -->
                    <div v-if="fieldErrors.password" :id="`${uid}-password-error`" class="invalid-feedback d-block">
                      {{ fieldErrors.password }}
                    </div>
                  </CCol>
                  <CCol :xs="12">
                    <CFormCheck :id="`${uid}-remember`" v-model="form.remember" label="Keep me signed in on this device" />
                  </CCol>
                  <CCol :xs="12">
                    <CLoadingButton color="primary" type="submit" class="w-100" :loading="pending" disabled-on-loading>
                      Sign in
                    </CLoadingButton>
                  </CCol>
                </CForm>
                <template v-if="auth.providers?.length">
                  <div class="position-relative">
                    <hr />
                    <div class="position-absolute top-50 start-50 translate-middle bg-body px-2 text-body-tertiary text-uppercase small">or</div>
                  </div>
                  <CRow class="g-2">
                    <CCol v-for="provider in auth.providers" :key="provider.id" :xs="12" :sm="true">
                      <CButton type="button" variant="outline" class="w-100" :disabled="pending" @click="auth.startProvider(provider.id)">
                        <CIcon v-if="provider.icon" :icon="provider.icon" class="me-1" /> Continue with {{ provider.label }}
                      </CButton>
                    </CCol>
                  </CRow>
                </template>
              </CCardBody>
            </CCard>
            <div class="text-center text-body-secondary">
              New here? <RouterLink :to="{ name: 'register' }">Create an account</RouterLink>
            </div>
          </div>
        </CCol>
      </CRow>
    </CContainer>
  </div>
</template>
```

Adapt route names, strings (i18n) and the logo to the target. With Laravel Sanctum the
adapter requests the CSRF cookie, posts credentials, maps 422 `errors` to `fields`,
maps 429/throttle to `message`, and loads the user into the existing auth store before
resolving. The example has no backend and claims no browser validation: test wrong
credentials, field errors, throttling, double submit, redirect handling, keyboard use,
mobile width and dark mode.
