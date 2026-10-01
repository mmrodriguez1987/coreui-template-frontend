# Authentication and standalone pages

The template ships nine authentication screens plus 404/500, all outside the admin
shell. They share two visual frames; reproduce those frames exactly so every auth
screen looks native to the template. Wording below is original; strings belong in i18n.

## Routing

Register these routes as siblings of the `DefaultLayout` route (no sidebar, header or
breadcrumb), lazy-loaded, e.g. under `/authentication/*` (or the project's existing
`/login`, `/register` paths) and `/404`, `/500`, with a catch-all redirect to the 404
page. Guards belong to the target app: redirect guests to login with a validated
`redirect` query and send authenticated users away from guest-only pages.

## Shared page background

```
div.bg-body-tertiary.min-vh-100.d-flex.flex-row.align-items-center
  CContainer
    CRow.justify-content-center
      CCol (frame width)
```

## Frame A — primary form card (login, register)

| Part | Composition |
| --- | --- |
| Column | `CCol :md="8" :lg="6" :xl="5"` |
| Stack | `div.d-flex.flex-column.gap-4` (register adds `text-center` and resets the form with `text-start`) |
| Logo | Centered brand logo (`CIcon :icon="logo" height="48"`) above the card |
| Card | `CCard class="p-4"` → `CCardBody class="d-flex flex-column gap-4"` |
| Title | `h2 class="h5 text-center mb-0"` ("Sign in to your account", "Create a new account") |
| Form | `CForm class="row gy-3"`, each field in `CCol :xs="12"` with CFormLabel + control |
| Password row | Label and "Forgot password?" RouterLink in `d-flex justify-content-between` above a CPasswordInput |
| Options | CFormCheck (remember device; register: terms with a link in the `#label` slot) |
| Submit | `CButton color="primary" type="submit" class="w-100"` |
| Divider | `div.position-relative` with `hr` and a centered label `position-absolute top-50 start-50 translate-middle bg-body px-2 text-body-tertiary text-uppercase small` ("or") |
| Providers | `CRow` of `CCol`s with `CButton variant="outline" class="w-100"` and a brand icon `class="me-1"` — only for providers the backend supports; omit the divider otherwise |
| Below card | `div.text-center.text-body-secondary` with the switch link (Need an account? Sign up / Already registered? Sign in) |

Autocomplete: `email`, `current-password` on login, `name`, `email`, `new-password` on register.

## Frame B — compact message card (everything else)

| Part | Composition |
| --- | --- |
| Column | `CCol :md="6"` (two-factor uses `:md="5"`) |
| Card | `CCard class="mx-4"`, add `text-center` for pure message screens |
| Body | `CCardBody class="p-4"` |
| Title | `h2 class="h5"` (`mb-0` when followed directly by the paragraph) |
| Lead | `p class="text-body-secondary"`; highlight the email with `span.fw-semibold` |
| Form | `CForm class="text-start"`; each field in `div.mb-4` (`mb-3` between consecutive passwords) |
| Action | `div.d-grid` with a primary button; secondary action as `color="secondary" variant="outline"` inside `d-grid gap-2` |
| Footer line | `p class="text-body-secondary mt-3 mb-0"` with a RouterLink (resend, try another method, back to sign in) |

## Screens and flows

| Screen | Frame | Content | Next step on success |
| --- | --- | --- | --- |
| Login | A | Email, password + forgot link, remember, submit, providers | Dashboard / redirect target, or Two-factor |
| Register | A | Name, email, password, terms, submit, providers | Check email |
| Magic-link login | B | Lead, email, button with `cil-envelope-closed` icon, link back to password sign-in | Magic link sent |
| Magic link sent | B, centered | Title, lead with email, primary continue + outline "send another link", footer link | — |
| Check email (verification) | B, centered | Title, lead with email, primary back-home, resend link | — |
| Reset password (request) | B | Title, lead, email, "send instructions" | Check email |
| Change password (from link) | B | Two CPasswordInput with `label` (new, confirm), "set new password" | Password changed |
| Password changed | B, centered | Title, lead, primary back-to-login | Login |
| Two-factor | B (`md 5`), centered | Title, lead, `COneTimePassword type="number" class="justify-content-between"` with six COneTimePasswordInput in `div.mb-4`, d-grid verify button, "try another method" link | Dashboard |

## Error pages (404, 500)

`div.min-vh-100.d-flex.flex-row.align-items-center` → centered `CCol :md="6"`:
`div.clearfix` with `h1 class="float-start display-3 me-4"` (code), `h4 class="pt-3"`
(short title) and `p class="text-body-secondary float-start"` (explanation), then a
CInputGroup: CInputGroupText with `cil-magnifying-glass`, CFormInput, `CButton color="info"`.
In a business app make the search real or replace it with "Go to dashboard".

## Behaviour (what the template does not do)

The template screens are UI only: submit handlers navigate without calling an API and
the router has no guard. Never report authentication as complete because the screens
render. For working auth:

- Use the project's auth service/store (e.g. Laravel Sanctum: CSRF cookie, login,
  user fetch). If none exists, identify the dependency instead of inventing one.
- Bind every field (`v-model`), submit with `@submit.prevent`, disable the button while
  pending (or use CLoadingButton), keep the values on failure.
- Map 422 field errors to `invalid` + `feedbackInvalid` on the control; show a
  credential/lockout/throttle error in a `CAlert color="danger"` at the top of the card
  body; never reveal whether an email exists on reset/magic-link screens.
- Show result screens only after the operation succeeds; handle expired links and
  wrong/expired codes with the provider's contract; offer resend with a cooldown.
- Two-factor: submit on `@complete`, clear the inputs after a failed attempt.
- Validate redirect targets (internal paths only). Never log passwords, codes or tokens.
- Translate every string; keep the logo from the target app, not the template brand.

The original [login example](../examples/login-page.md) implements Frame A with
bound state, pending/error handling and a provider-agnostic adapter.
