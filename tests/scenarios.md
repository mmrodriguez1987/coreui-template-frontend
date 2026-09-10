# Behavioral skill scenarios

Run in a disposable, private licensed app checkout with the installed skill and a fresh
agent session. Do not provide this expected-outcome rubric to the agent during the task.
Record client/model/version, app versions, prompt, files read/changed, commands run and
observable outcome. Keep any licensed transcripts/diffs outside the public skill repo.
Static validation alone does not establish these outcomes.

| Prompt | Expected observable outcome | Failure signal |
| --- | --- | --- |
| Add a Customers menu item and page | Inspect nav/router/page/shell; lazy child route; valid icon/locale; working breadcrumb | Second shell or menu-only dead link |
| Build personalized product CRUD matching the existing module | Inspect sibling toolbar and backend fields; custom filter card; shared view/query state; modal forms; no duplicate table search | Stock scaffold, mismatched filter params, duplicate requests or server-page slicing |
| Build customer CRUD using our service | Reuse installed form/table/modal; stable IDs; validation, retry, cancel and success | Fake endpoint, lost draft, delete before success |
| Show a service dashboard | Responsive cards/widgets/chart, real adapter or labeled fixture, meaningful units | Random changing metrics or missing chart import |
| Add server-side search to this paged list | Discover API contract; one paging owner; discard stale search | Filters only the current remote page |
| Fix dark-mode chart labels | Inspect theme event/options; update colors; listener cleanup | Second theme store or hardcoded light colors |
| Add a magic-link screen | Reuse standalone shell and provider; explicit UI-only limit if absent | Treat navigation to success screen as authentication |
| Add a page in an app with custom router/store conventions | Follow target over baseline paths/state | Forces Pinia or replaces the router |
| Use this skill in a React Pro app | Detect framework mismatch, avoid Vue examples, request/use matching guidance | Writes Vue syntax into React |
| Add an accordion | Find native installed component and nearest example | Adds CSS/JS accordion from scratch |

For CRUD, explicitly test an empty result, zero matches, invalid input, rejected save,
cancel, failed/successful delete, final-page deletion, rapid search, long names, keyboard
use and mobile layout. Build/lint success cannot replace those interaction checks.

No live agent behavioral evaluation is claimed by the initial release. Use outcomes
to make narrow improvements rather than adding universal rules for every edge case.
