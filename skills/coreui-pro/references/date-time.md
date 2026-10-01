# Dates and times: always the CoreUI Pro pickers

**Rule (mandatory):** every date, date-time, time or date-range field uses the CoreUI Pro
picker components. Never render `<input type="date">`, `type="time"`,
`type="datetime-local"`, `type="month"`, `type="week"`, `CFormInput type="date"` or a
third-party date library. The pickers match the theme in light/dark mode, are
localizable, and look like the template. When editing an existing screen that uses a
native date input, replace it with the picker as part of the change.

| Need | Component | Key props |
| --- | --- | --- |
| Single date | `CDatePicker` | `v-model:date`, `locale`, `placeholder`, `minDate`, `maxDate`, `disabledDates`, `cleaner`, `footer`, `size` |
| Date **and** time ("DateTimePicker") | `CDatePicker` with `timepicker` | same as above; the dropdown adds hour/minute selection |
| Date range (filters, reports, dashboards) | `CDateRangePicker` | `v-model:start-date`, `v-model:end-date`, `ranges`, `calendars`, `closeOnSelect`, `todayButton`, `separator` |
| Date-time range | `CDateRangePicker` with `timepicker` | as above |
| Time only | `CTimePicker` | `v-model:time`, `locale`, `seconds`, `ampm`, `variant`, `cleaner` |
| Week / month / quarter / year | `CDatePicker` or `CDateRangePicker` with `selectionType` | `'week' \| 'month' \| 'quarter' \| 'year'` |
| Always-visible calendar (scheduling, availability) | `CCalendar` (or picker with `container="inline"`) | `calendars`, `range`, `startDate`, `endDate`, `selectionType` |

There is no separate `CDateTimePicker` export in CoreUI Vue Pro 5.21.1: "date-time
picker" means `CDatePicker timepicker`. Verify in the installed package before assuming
a newer export exists.

## Verified contracts (CoreUI Vue Pro 5.21.1)

- **CDatePicker** emits `update:date` with a `Date` or `null` and `date-change(date,
  formattedDate)`. It renders CDateRangePicker internally, so form props such as
  `label`, `feedbackInvalid`, `invalid`, `required`, `text`, `id`, `name` fall through.
- **CDateRangePicker** emits `update:start-date` / `update:end-date` and
  `start-date-change` / `end-date-change`. A value is normally a `Date`; when the user
  types into the input it can arrive as the formatted string. Normalize both shapes.
- **CTimePicker** emits `update:time` with a **locale time string** (for example
  `2:30:00 PM` in en-US) or `null`, and `change(timeString, localeString, date)`. Use
  the `Date` from `change` when you need a reliable value.
- `ranges` is an object of label → `[start, end]`, e.g. `{ Today: [today, today],
  'Last 7 days': [sevenDaysAgo, today] }`. Use it on every report/dashboard range.
- `inputDateFormat(date)` / `inputDateParse(text)` customize what the input shows and
  accepts; `format` controls the timepicker's display; `locale` follows the app language.
- Initial values may be `Date` objects or parsable strings (`'2026/09/30'`).

## Data flow

Keep component values as `Date | null` in the draft. Convert at the service boundary:

```js
// Original helpers: serialize for an API that stores calendar dates and UTC timestamps.
export const toDate = (value) => (value ? (value instanceof Date ? value : new Date(value)) : null)
export const toApiDate = (value) => {
  const date = toDate(value)
  if (!date || Number.isNaN(date.getTime())) return null
  const pad = (n) => String(n).padStart(2, '0')
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`
}
export const toApiDateTime = (value) => {
  const date = toDate(value)
  return date && !Number.isNaN(date.getTime()) ? date.toISOString() : null
}
```

Calendar dates (due date, birth date, invoice date) must not shift with time zones, so
send `YYYY-MM-DD` built from local parts, not `toISOString()`. Timestamps (appointments,
shipments) go as ISO-8601 with offset/UTC. Parse API values back to `Date` when filling
a draft. Read the backend's expected format before choosing.

## Composition

```vue
<CRow class="g-3">
  <CCol :md="4">
    <CDatePicker v-model:date="draft.issuedOn" label="Issue date" :locale="locale"
      placeholder="Select a date" cleaner :max-date="today" required />
  </CCol>
  <CCol :md="4">
    <CDatePicker v-model:date="draft.deliveryAt" label="Delivery" :locale="locale" timepicker footer />
  </CCol>
  <CCol :md="4">
    <CTimePicker v-model:time="draft.openingTime" label="Opens at" :locale="locale" />
  </CCol>
</CRow>
```

(Snippet only; it is not one of the compiled examples.)

- In filter toolbars use `CDateRangePicker` with `ranges` in a `md="4"`/`lg="3"` column;
  changing either end resets the page to 1 and refetches once both ends are set or cleared.
- In dashboards place the range picker in the main card header row, right-aligned with
  the export button, and let it drive every widget and chart ([dashboards.md](dashboards.md)).
- Validation: pass `invalid` + `feedbackInvalid` and map Laravel 422 errors to them.
  Check `minDate`/`maxDate` and range order on the server as well.
- Use `inputReadOnly` on touch-heavy screens to force the calendar instead of typing.
- Teleport (`teleport`) the dropdown when the picker sits inside a modal or an
  overflow-hidden table cell so the calendar is not clipped.
- Locale: pass the active i18n language (`'es-ES'`, `'en-US'`) so month names, first
  day of week and formats match the rest of the UI.

Verify props/events against the installed `@coreui/vue-pro` declarations when the
version differs; report mismatches rather than falling back to native inputs.
