# Routes and breadcrumbs

Inspect `src/router/index.js`, the destination layout, and `AppBreadcrumb.vue` before
adding a route. The baseline uses `createWebHashHistory(import.meta.env.BASE_URL)`.
Admin pages are children of DefaultLayout; authentication and error pages are outside
it. Email has its own shell. Preserve history/base behavior and existing guards.

Add a lazy page import to the relevant children array. Choose a unique path and, when
used, a stable route name consistent with the application. Original route fragment:

```js
{
  path: '/customers',
  name: 'Customers',
  component: () => import('@/views/customers/CustomerList.vue'),
}
```

This fragment belongs inside the admin layout's children, not as a second root shell.
The baseline mixes absolute child paths and relative paths in grouped applications;
check the resolved URL instead of blindly concatenating. Edit/details routes should
use the application's existing parameter convention and load the selected record.

Adding a route does not add a sidebar entry. Read [navigation.md](navigation.md) when
it should be discoverable. A route-only details screen often needs no menu entry.

The inspected breadcrumb derives labels from matched route names and evaluates some
function-valued names for i18next. Do not introduce a `meta.breadcrumb` convention
unless the actual breadcrumb reads it. Function-valued route names are a local quirk:
prefer existing stable-name patterns; use path navigation where appropriate. In an
application already using stable names plus translated metadata, follow that system.
Do not refactor the router globally just to add one route.

Check direct hash URLs, reload, sidebar navigation, nested outlets, back/forward,
active labels with query strings, parameterized breadcrumbs, and locale changes.
The baseline breadcrumb compares fullPath and path, so query-bearing routes deserve
explicit testing. Visible 404/500 demo routes do not imply a catch-all is configured.
Never infer authorization from a layout or from a hidden navigation item.
