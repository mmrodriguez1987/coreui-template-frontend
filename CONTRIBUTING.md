# Contributing

Contribute original guidance that helps an agent make a better implementation decision.
Start with a reproducible task and inspect the relevant installed framework/CoreUI API.
Describe version evidence as a tested baseline, not a universal requirement. Keep the
existing project's conventions above reference guidance.

Keep SKILL.md focused on activation, shared constraints and reference selection. Put
conditional details in one reference and link it from the task table. Examples must
be small, original, and explicit about their data/adapter contracts. Do not submit
commercial source, screenshots/assets, template archives, docs excerpts, credentials,
registry config or private customer data. Public issue reports should use synthetic data.

Run the checks in [skill-validation.md](skill-validation.md). If you own a licensed
reference tree, run the optional source-overlap audit locally; do not attach that tree
or raw audit source content. Include relevant build/runtime results from a licensed
consumer application and identify checks not run. Review generated artifacts and Git
history before publication; ignore rules and heuristic scanners are not a legal clearance.

A contribution should explain the user-visible behavior it improves, relevant versions,
changed references/examples and validation. Update CHANGELOG.md for release-worthy
changes. Contributions to original content are provided under this repository's MIT
license. Do not imply CoreUI endorsement or extend MIT to CoreUI's products.

For future frameworks, use separate framework-specific skills after inspecting their
licensed starters, rather than adding unverified React/Angular syntax to this Vue skill.
