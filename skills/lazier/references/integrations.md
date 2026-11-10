# lazier tools and integrations v0.11.0

Load only when you expect long output (logs, test suites, large files), work runs
in the background, or a specialized skill or integration applies. The core policy
still applies.

## Tools and independent skills

Use the tools the current host actually provides. Use native reads and edits for
small changes. For long or unpredictable output, use an installed analysis or
context tool when there is one, and derive a focused result in code. Follow the
host's routing rules. If a preferred tool is unavailable, say what that limits and
use a permitted alternative; do not install a replacement by default.

For background work, use completion notifications or bounded waits when the host
supports them, and avoid repeated status polling. Do not assume the agent will wake
up on its own; report timeouts and failures explicitly.

Specialized integrations belong to their own skills. For TypeSafe/Jev work, use the
separately installed `typesafe-ai` skill. lazier does not copy its API guidance and
does not require a TypeSafe call for routine engineering decisions.
