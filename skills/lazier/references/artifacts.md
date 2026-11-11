# lazier artifacts and continuity v0.11.0

Load only when a plan, investigation, review or report must persist, or when work
continues across sessions, hosts or review rounds. The core policy still applies.

## Technical continuity

When work continues across sessions, hosts or review rounds, carry forward only
context that is still valid, and keep verified findings, assumptions and open
questions separate:

- **Planning:** goals, constraints, checked evidence, options with their
  trade-offs, and unresolved questions.
- **Implementation:** decisions already settled in a plan (if there is one),
  verified findings with file and line, the repair direction, and the validation
  that applies. A task does not need a prior plan.
- **Repair after review:** the concrete findings from the latest audit or review,
  each with file and line, evidence, impact and proposed fix.

Do not repeat an audit of what was already checked, but read the current source
before editing. Keep settled decisions and advice unless new evidence invalidates
them. Keep handoffs and review results short without cutting the evidence they rely
on.

## Documentation and working artifacts

Keep maintained project documentation at its established canonical paths. Put
working investigations, plans, reviews and reports that must persist in one
project artifact directory, not scattered through source or product docs. Create an
artifact when the user asks or the task needs one, not for every chat reply.

- Choose the destination in this order: the user's choice, the project's
  documented artifact location, then `.agent-artifacts/` at the repository root (or
  the project root when there is no Git). Do not pick a nested directory just
  because the agent started there.
- Write the artifact and its filename in English; the chat reply follows the
  user's language (see the core policy). Update the existing artifact for the same
  topic instead of writing a new report each turn. When the directory is shared by
  several projects, name the project in the artifact.
- Treat working artifacts inside Git as private unless the user says to commit or
  share them. Before writing one, check that the destination is ignored. If no
  rule covers it, add a narrow local rule to the file printed by
  `git rev-parse --git-path info/exclude`, keeping existing entries. Edit the
  shared `.gitignore` only when the project wants a team-wide rule.
- An ignore rule does not untrack a file. Do not change the index, force-add
  artifacts, move tracked documents or rewrite Git history to hide artifacts. If the
  destination is tracked or cannot be configured with your permissions, report the
  constraint and pick a usable destination before writing.
- Write only where the host permits; a configured path does not grant access.
  Return the artifact path with a concise result and the verification actually run.
