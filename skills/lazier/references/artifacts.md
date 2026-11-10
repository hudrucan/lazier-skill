# lazier artifacts and continuity v0.11.0

Load only when a plan, investigation, review or report must persist, or when work
continues across sessions, hosts or review rounds. The core policy still applies.

## Technical continuity

Carry forward only relevant, still-valid context, separating verified findings,
assumptions and open questions, for work across sessions, hosts and review rounds:

- **Planning:** goals, constraints, checked evidence, relevant options/trade-offs
  and unresolved questions.
- **Implementation:** settled Plan decisions (if any), verified findings with
  file/line, repair direction and relevant validation. A Task does not require a
  prior Plan.
- **Repair after review:** concrete findings from the latest audit or review,
  with file/line, evidence, impact and proposed fix.

Do not require a full re-audit of everything already checked; require inspection
of current source before editing. Keep settled decisions/advice unless new
evidence invalidates them. Keep handoffs and review results short without cutting
necessary evidence. This guidance applies independently of any transport.


## Documentation and working artifacts

Keep maintained project documentation at its established canonical paths. Use a
single project artifact directory for working investigations, plans, reviews and
reports that need to persist; do not scatter these through source or product docs.
Create artifacts when requested or needed for the task, not for every chat reply.

- Honor a user-selected destination, then the project's documented artifact
  location. Otherwise use `.agent-artifacts/` at the repository root, or the
  established project root when Git is absent. Do not choose a nested working
  directory merely because the agent started there.
- Use descriptive English filenames and update the existing artifact for the same
  topic when practical. Avoid a new report per turn. Include the relevant project
  context when the configured directory is shared by several projects.
- For private working artifacts inside Git, verify that the destination is ignored
  before writing. If no ignore rule covers it, add a narrowly scoped local rule in
  the file resolved by `git rev-parse --git-path info/exclude`; preserve existing
  entries. Use shared `.gitignore` only when the project wants a team-wide rule.
- Ignore rules do not untrack existing files. Do not alter the index, force-add
  artifacts, relocate tracked documents or rewrite Git history to hide artifacts.
  If a destination is tracked or cannot be configured within current permissions,
  report the constraint and resolve a usable destination before writing there.
- Keep artifacts within the host's permitted write locations. A configured path
  does not grant access. Return the artifact path with a concise result and actual
  verification; no language or storage rule requires an extra artifact.
