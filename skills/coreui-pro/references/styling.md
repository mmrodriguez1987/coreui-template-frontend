# Theme and styling integration

The visual target (spacing, cards, typography, gradients, icons, sidebar density) is
described in [visual-design.md](visual-design.md); this file covers the mechanics.

The baseline App.vue imports `src/styles/style.scss` and separately `examples.scss`.
The main file uses Sass @use for `@coreui/coreui-pro/scss/coreui`, the CoreUI Chart.js
stylesheet and vendor adaptations. Keep import order and configure supported Sass
variables before their module is loaded; do not mix a second Bootstrap/CoreUI CSS
bundle into the cascade. Never edit node_modules to customize the theme.

Use existing utility spacing, grid, flex, borders and typography. Prefer `text-body`,
`text-body-secondary`, and CSS variables such as `--cui-body-bg`, `--cui-body-color`,
`--cui-border-color`, and `--cui-primary` to fixed light-theme colors. Check variable
availability locally. Logical start/end spacing and sidebar occupancy variables
preserve layout behavior. Vendor SCSS adapts SimpleBar and calendar colors.

App and header share `useColorModes` and its persistence key. Reuse that key and
color-mode mechanism; do not create a separate localStorage toggle. The baseline also
has a Pinia theme default and URL-driven initialization. Preserve the app's actual
precedence without spreading URL/theme logic into pages.

Use a small scoped style only for a gap utilities/theme tokens cannot express, such as
a chart container height. Keep shared theme changes in the existing SCSS layer, and
check both modes. Demo `examples.scss` and Docs components serve documentation displays;
business pages should not depend on them. Removing them globally is a separate cleanup
requiring an actual usage check.

If a widget looks wrong, first verify the correct Pro stylesheet is loaded exactly
once, installed CSS/binding versions, component props, container constraints and CSS
cascade. Adding higher specificity or !important should not be the first repair.
