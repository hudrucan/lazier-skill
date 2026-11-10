# lazier tools and integrations v0.11.0

Load only when output is large or unpredictable, work runs in the background,
or a specialized skill or integration is relevant. The core policy still applies.

## Tools and independent skills

Use the tools actually available on the current host. Prefer precise native reads
and edits for small changes; for large or unpredictable output, use an installed
analysis/context tool when available and derive focused results in code. Preserve
the host's routing rules. If a preferred tool is unavailable, disclose the relevant
limit and use a permitted alternative without installing a replacement by default.

For background work, prefer completion notifications or bounded waits when the
host supports them. Avoid repeated status polling when those options are available.
Do not assume automatic wake-up; report timeouts and failures explicitly.

Specialized integrations belong to their own skills. For TypeSafe/Jev work, use
the separately installed `typesafe-ai` skill when relevant. lazier neither copies
its API guidance nor requires a TypeSafe call for routine engineering decisions.
