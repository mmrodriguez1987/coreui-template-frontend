# Troubleshooting by symptom

| Symptom | Inspect first | Targeted response |
| --- | --- | --- |
| Unknown component | main registration, imports, installed exports | Use @coreui/vue-pro or the existing wrapper; import chart components separately |
| Blank page after adding route | lazy import path/case, parent outlet, layout placement | Repair route wiring; check console and direct URL |
| Menu missing or inactive | _nav consumer, to/path match, group nesting | Update config and route together; test initial deep link |
| Icon absent | iconsSet imports and provided registry | Register the actual icon; do not add a second icon system |
| Duplicated header or shifted content | parent shell and sidebar padding | Remove page-owned shell/offset duplication |
| Breadcrumb label wrong | matched routes, function labels, locale, fullPath comparison | Follow actual label source and test query/parameter routes |
| Form reloads page | submit handler and button types | Prevent native submit and await explicit save |
| Validation colors but invalid save | validated vs checkValidity/business rules | Gate the request, associate feedback and surface server errors |
| Pro control ignores model | installed update events and value shape | Match declared contract; do not assume DOM event payload |
| Search does nothing | static header suggestions vs real query handler | Connect source/state/navigation within requested scope |
| Missing rows or wrong total | double paging/filtering, remote vs local data | Choose one processing owner |
| Wrong row edited/deleted | index-based selection | Track stable domain ID |
| Table custom cell broken | slot key, supplied item, expected cell wrapper | Match installed slot contract |
| Modal cannot reopen | close event and parent visible state | Synchronize every close path; reset stale draft/error |
| Toast does not appear | plain array mutation | Use ref/reactive or existing notification store |
| Toast accumulation | stable IDs and dismissal cleanup | Remove dismissed messages |
| CSV export outdated | one-time computation and export scope | Derive current rows at export time; escape safely |
| Chart invisible or growing | container height/options/hidden parent | Bound sizing and verify resize after reveal |
| Chart retains light colors | theme event, dataset/axis colors | Refresh colors and clean up event listeners |
| Theme mismatch | shared color-mode key, duplicated CSS, tokens | Reuse root theme mechanism |
| Auth appears successful without session | simulated navigation and missing provider calls | Integrate actual auth contract; do not fabricate success |
| Build/package access fails | installed versions, configured registry, credentials availability | Report dependency blocker; never publish registry config or replace Pro silently |

Local source/declarations and the nearest working page are the first evidence. When
online documentation is needed, use official Vue/CoreUI documentation matching the
installed major version and verify differences locally. Do not copy manuals into this skill.
