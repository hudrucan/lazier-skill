---
name: lazier
description: Apply portable engineering policy to coding, technical investigations, planning, reviews and project documentation. Simplicity review only when requested. Excludes unrelated work.
license: MIT
---

# lazier

Read and apply the [core policy](references/policy.md): engineering judgment,
validation, review and handoff. Load the other references only when their trigger
applies:

- [artifacts and continuity](references/artifacts.md): a plan, investigation,
  review or report must be saved, or work continues across sessions or review
  rounds.
- [tools and integrations](references/integrations.md): you expect long output
  (logs, test suites, large files), work runs in the background, or a specialized
  skill applies.

Do not reread guidance you already read in this session unless it changed or
context is missing. Guidance never replaces fresh evidence from the repository.

Use the current agent's tools, instruction hierarchy and permission model. Do not
assume another agent's tool names, modes or installed integrations. Follow
task-specific skills alongside lazier; their integrations stay independently
configured. lazier does not install tools or require an advisor.

Follow the user's task; invoking this skill does not request a simplicity review.
Discovery only makes the skill available. To apply it on every task, the agent's
user or project instructions must load this entrypoint.
