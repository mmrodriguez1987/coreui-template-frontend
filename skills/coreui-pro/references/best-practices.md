# Architecture and UI review

Use this for an integration review, not as an instruction to expand every small edit.

- Check the feature follows the application’s existing service and state boundaries;
  no invented API or second shared state system.
- Confirm each behavior has one owner: shell, paging, filters, modal visibility,
  editable draft, theme persistence and route authorization.
- Verify installed exports/events/slots before using remembered APIs from another
  CoreUI framework or major version.
- Keep Vue reactive data reactive, use stable record keys, clean up listeners and
  invalidate stale requests. Avoid mutating incoming props or list records during edits.
- Prefer CoreUI composition for visual structure; extract feature components when
  their responsibility is useful, not merely to shorten a template.
- Ensure actions have explicit button types and accessible labels; errors are readable,
  dialogs are keyboard-operable, and status is not represented by color alone.
- Test the real edge relevant to the change: failed save, last-row delete, stale search,
  deep-link reload, query-bearing breadcrumb, theme switch or mobile sidebar.
- Keep licensed demo content out of public contributions. Small original examples
  should explain their mock data or adapter contract and avoid implied persistence.

Run existing build/lint/type/test scripts appropriate to changed code and state what
was exercised. The baseline only defines build/lint for code validation; passing those
does not prove visual behavior or API integration. Do not upgrade packages or rewrite
the shell solely to satisfy the skill's historical baseline.
