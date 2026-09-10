# Forms and validation

Use the nearest form as the starting architecture. The baseline uses Vue local state,
CForm, CoreUI controls and native browser constraints; no form validation library is
configured. An existing application may have a schema or form wrapper: reuse that.

| Data | Control/pattern |
| --- | --- |
| Short text, email, number | CFormInput with matching type, ID and label |
| Long text | CFormTextarea |
| Simple single choice | CFormSelect with stable option values |
| Rich/multiple choice | CMultiSelect or CAutocomplete; inspect value/event contract |
| Boolean | CFormCheck or CFormSwitch |
| Mutually exclusive options | CFormCheck type radio, shared name, distinct IDs/values |
| Prefix/suffix | CInputGroup + CInputGroupText; preserve accessible naming |
| Floating label | CFormFloating with properly associated label and control |
| Date/time/range | Installed CDatePicker, CTimePicker, CDateRangePicker |
| Secret or OTP | CPasswordInput / COneTimePassword family |
| Multi-step workflow | Existing wrapper or installed CStepper; validate before advancing |

Bind editable state to a draft, not directly to the list record. Initialize drafts on
create/edit transitions; cancel discards them. Normalize payload types explicitly:
HTML numbers/selects may produce strings, unchecked fields may be absent, and dates
need a deliberate locale/time-zone/API representation. Do not assume every Pro
control supports plain v-model or emits a DOM event; inspect local declarations.

For native validation, handle submit with preventDefault even when valid so an SPA
does not navigate away. CForm `validated` controls feedback styling; it does not save
or validate business rules. Call `event.currentTarget.checkValidity()` before sending.
Use required/type/min/max constraints where useful; trim and check required business
text explicitly. Pair invalid/valid state with CFormFeedback or verified feedback
props and accessible associations. Avoid success styling before interaction.

Track pending, attempted validation, field errors and request errors separately. Map
server field failures to their inputs; retain a visible summary for other failures.
Disable duplicate save actions, preserve the draft on failure, and clear stale errors
when reopening or correcting a field. Save success updates/refetches records before
showing success. Cancel is type button. Preserve focus and announce async feedback.

For checkbox arrays/radios, inspect checked/value update contracts. For input groups,
feedback may need the group's validation class/layout. Validate stepper completion,
not merely the current panel's appearance. See the original
[form component](../examples/form-page.md) and [CRUD flow](../examples/crud-page.md).

For personalized CRUD modal forms, follow [custom-crud.md](custom-crud.md). Reuse
existing form/modal wrappers and API/toast services, map Laravel 422 errors, and preserve
image upload contracts when applicable. Footer buttons outside CForm must target the
form ID or use a validation-aware submit path.
