# Component selection and interaction contracts

The following families were observed in the licensed Vue template. Verify exports
and contracts against the target's installed `@coreui/vue-pro`; availability varies
across versions. A family name here is not a promise that every prop exists everywhere.

| Requirement | Preferred composition | Decision that matters |
| --- | --- | --- |
| Page/grid | CContainer, CRow, CCol | Reuse shell container; choose breakpoint props |
| Card | CCard, CCardHeader, CCardBody, CCardFooter | Semantic heading inside header; footer for actions |
| KPI | CWidgetStatsA–F as available | Match needed slots; do not recreate widget framing |
| Plain table | CTable and head/body/row/cell components | Semantic data; responsive overflow |
| Interactive data grid | CSmartTable | Built-in filters/sorting/paging; see tables reference |
| Form | CForm and CFormInput/Select/Textarea/Check/Switch | Accessible labels and actual model bindings |
| Rich control | CMultiSelect, CAutocomplete, CDatePicker, CDateRangePicker, CTimePicker | Inspect emitted values and locale/date contract |
| Password/OTP | CPasswordInput, COneTimePassword, COneTimePasswordInput | UI controls do not implement authentication |
| Modal | CModal, CModalHeader/Title/Body/Footer | Controlled visible state and close handling |
| Feedback | CAlert, CAlertHeading, CFormFeedback | Persistent request/field errors remain visible |
| Toast | CToaster, CToast, CToastHeader/Body/Close | Reactive queue; remove dismissed entries |
| Status | CBadge | Include text, not color alone |
| Dropdown | CDropdown, CDropdownToggle/Menu/Item | Actions are buttons; destinations are links |
| Navigation | CSidebar family, CNavItem/Group/Title | Integrate existing renderer/config |
| Breadcrumb | CBreadcrumb, CBreadcrumbItem | Reuse shared route-derived breadcrumb |
| Tabs | CTabs, CTabList, CTab, CTabContent, CTabPanel | Match item keys and selected state |
| Legacy/local tab composition | CNav, CNavLink, CTabContent, CTabPane | Preserve sibling pattern; do not mix tab APIs |
| Accordion | CAccordion, CAccordionItem/Header/Body | Stable item identity and library toggle behavior |
| Paging | CPagination, CPaginationItem; CSmartTable paging | Exactly one paging owner |
| Progress | CProgress, CProgressBar | Meaningful bounded value and readable label |
| Loading | CSpinner, CPlaceholder, CLoadingButton | Loading differs from empty or zero |
| Search trigger/results | CSearchButton, CModal, CFormInput, CListGroup | Trigger is not a search engine |

## Modals

Own the selected entity and visibility in the page or an existing controller. Pass
`:visible` and handle `@close`; synchronize all close paths. Associate the dialog
with a unique CModalTitle ID using aria-labelledby. Use explicit button types.
Let CoreUI manage dialog behavior; verify keyboard focus, Escape, backdrop, and
focus restoration in the browser. Do not manipulate Bootstrap modal classes manually.

During a destructive request, prevent repeat submissions and either prevent closing
using verified props or define what closing while pending means. Keep the selected ID
stable for the operation. On failure keep the dialog and error; close only on confirmed
success. See the original [modal example](../examples/modal-example.md).

## Feedback and states

Use a reactive toast array/store, stable message IDs, and dismissal cleanup. Reuse an
existing notification service if present; the baseline does not supply one. Toasts
can acknowledge success; request errors needing action belong near the operation.

Use a spinner/status label or placeholders while loading. After a successful empty
response, show plain explanatory text and a relevant CoreUI action in the existing
card/table region. Distinguish “no records” from “no matches” with a clear-filters action.
There is no observed dedicated empty-state framework to import. Avoid announcing
skeletons individually to assistive technology.
