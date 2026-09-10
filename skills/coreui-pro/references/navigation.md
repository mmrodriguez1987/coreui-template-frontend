# Sidebar, header, and search

In the baseline, edit `src/_nav.js` for menu content; retain `AppSidebarNav.js` for
rendering and `AppSidebar.vue` for the shell. The recursive renderer uses RouterLink,
CoreUI nav components, SimpleBar, icons and badges. It expands matching child groups
on first render. Trace the consumer before adding a config property: comments mention
an external flag, but the renderer actually uses href/target for external links.

Original internal item, assuming the corresponding route exists:

```js
{
  component: 'CNavItem',
  name: 'Customers',
  to: '/customers',
  icon: 'cil-people',
}
```

Use `CNavGroup` with `items` for a real hierarchy; use `CNavTitle` for a section label.
Match existing translation functions and add new keys to supported locale files when
needed. Do not export template translations. Confirm icons are both imported and
included in `src/assets/icons/index.js`; an installed icon package alone does not
populate the app's injected registry. Use router destinations for internal pages and
href for external URLs.

Sidebar visibility/unfoldable state belongs to the existing Pinia sidebar store.
Header toggles and mobile close controls must operate on that same state. Do not
create page-local sidebar state. Verify selected links, initial deep-link group
expansion, collapsed desktop mode, mobile dismissal, and localized labels.

The header owns search-modal visibility and passes it to AppHeaderSearchModal.
CSearchButton emits a trigger in the inspected example. Its suggestions are static;
implementing search needs a real source, query state, result navigation, and separate
loading/no-match/error feedback. Reuse the modal/list/form components, label the input,
and handle keyboard selection if introducing richer interactions. For remote search,
debounce and discard stale responses; for business table search see
[tables.md](tables.md). Do not rebuild the whole header for a page-specific filter.
