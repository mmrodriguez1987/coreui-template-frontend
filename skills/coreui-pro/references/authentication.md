# Authentication-related screens

Observed views cover login, registration, reset/change password, email confirmation,
password-change result, magic-link request/result and two-factor code entry. They use
standalone responsive CoreUI containers/cards/forms outside DefaultLayout. Password
and OTP controls are native Pro components; provider branding in the licensed template
is not part of this skill.

These are UI examples. Registration and magic-link submit handlers navigate to result
screens without an API request; login/recovery screens do not establish an authentication
service. The router has no authentication guard despite a comment describing protected
routes. Do not report an authentication feature complete because its screens render.

When asked for UI only, match existing screens and clearly state backend integration
is pending. When asked for working authentication, inspect the project's auth provider,
request/session handling, redirect rules, error contracts and authorization checks.
Use its existing service; if no contract exists, identify that dependency. Never invent
successful verification, store raw passwords, or log codes/tokens.

Bind credentials/codes, label controls, use appropriate autocomplete, disable duplicate
submissions and retain actionable failures. Show result screens only after the relevant
operation succeeds. Handle expired links/code attempts through the real provider's
contract. Preserve authorized destination handling and validate redirect destinations.
Sidebar visibility does not enforce access control; connect routes to the application's
existing guards and server authorization when that is in scope.
