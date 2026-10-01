# Layout composition and responsive behavior

Shell dimensions and spacing rhythm of the template: [visual-design.md](visual-design.md).

The admin shell owns sidebar, sticky header, breadcrumb, footer, aside, and the
container around its router outlet. Page components own feature headings and content.
Do not insert a second AppHeader, AppSidebar, AppBreadcrumb or full-height wrapper
inside a normal admin page.

Use CRow/CCol for page composition and CCard sections for content grouping. Begin at
full width, then use the sibling page's `sm`, `md`, `lg`, `xl`, or `xxl` column props
as content allows. A form can use a narrower desktop column; a dense table often
needs the full row. Use utility gaps and margins for consistent vertical rhythm.

Keep toolbars able to wrap; stack filters and actions on small screens. Preserve
labels and important actions when space narrows. Prefer CTable responsive behavior
to shrinking text or hiding primary data. Check popup clipping within table overflow.

Shell styles use logical padding driven by CoreUI sidebar occupancy CSS variables.
Hardcoding an extra sidebar width in a page causes doubled offsets. Keep logical
start/end spacing (`ms`, `me`, `text-start`) and existing theme variables.

Authentication/error views use standalone containers; the email application shows
an intentional alternate shell. Choose one only when the requested screen belongs
outside the admin shell or in that application. Do not treat an alternate shell as
the default for every new feature.

Validate at a narrow phone width, a medium layout, and a wide desktop; check long
translated labels, keyboard focus order, table overflow, and open sidebar/modals.
