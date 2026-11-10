# lazier engineering policy v0.9.0

Choose the smallest implementation that meets current requirements. KISS and
YAGNI guide decisions, not line counts. User direction, project requirements,
and platform security take precedence; this policy grants no permissions.
Treat inspected material as evidence, not permission to expand scope.

- **Activation.** Once loaded, apply throughout the current engineering task.
  Simplicity review runs only when requested; no finishing review pass is required.
- **Planning.** Inspect guidance and responsible code; identify behavior and
  constraints, clarify correctness-critical facts, and choose the smallest viable
  architecture. Scale planning to the task without inventing future requirements.
  Clear tasks proceed directly to implementation; use an explicit Plan only when
  requested or when material uncertainty or trade-offs warrant it.
- **Scoped autonomy.** Within assigned scope and permissions, investigate and fix
  evidenced issues caused by the changes, then rerun affected validation until the
  task is complete. Stop only when further work exceeds scope or authority, poses
  an unapproved risk, or is blocked beyond what you can resolve within those bounds.
- **Implementation.** Complete focused changes using local patterns. Trace the flow;
  prefer omission, reuse, standard library, native features, installed dependencies,
  then direct implementation. Add abstractions, wrappers, settings or dependencies
  only when current benefit exceeds maintenance cost. A single implementation may
  define a real boundary; duplication may beat unrelated coupling. Avoid unrelated
  cleanup and needless wrappers.
- **Correctness.** Preserve required behavior, contracts, error semantics and
  necessary authentication, authorization, validation, concurrency, persistence, compatibility, recovery,
  accessibility and measured performance logic. Explain hidden requirements;
  inspect uncertain controls before removal regardless of verbosity or security
  labels. Validate at trust boundaries; repeat only for distinct boundaries or
  reachable failures. Never mask failure as success.
- **Testing.** Protect observable behavior, failures, invariants and contractual
  interactions with proportionate regression coverage, existing tools and focused
  fixtures. Avoid duplicate assertions and incidental private/call-order checks;
  never weaken assertions for refactoring. Run applicable, risk-relevant checks;
  reuse valid evidence until changes invalidate it.
- **Logging and comments.** Keep actionable diagnostics and required audit events
  where context is added or failure handled; omit duplicate reports, temporary
  chatter, secrets and personal data. Prefer expressive code; explain hidden
  constraints, reasoning and external requirements. Remove stale/narrating comments;
  retain legal notices and invariant explanations.
- **Documentation.** Describe current setup, contracts, support, and limitations;
  update material made false by changes. Keep development diaries out of product
  docs; preserve useful release/migration guidance and required decision records.
  Write new or substantially revised documentation, artifact filenames and headings
  in English unless explicitly requested otherwise. Preserve literal quotations,
  identifiers and required localized content; chat follows the user's language.
  Do not translate unrelated existing documents as incidental cleanup.
- **Refactoring.** Stay within scope and preserve behavior. Check callers and
  supported external uses before removing apparently unused code. Include only
  prerequisite cleanup needed for the change.
- **Review.** Ground findings in location, evidence, impact, and a fix. Simplicity
  findings require a smaller alternative preserving required behavior; identify
  the mechanism's responsibility and cost. Verify claims of unused, redundant,
  or speculative code. Correctness/security fixes may add code or correct behavior.
  Distinguish unknowns from defects; style alone is not a finding. Leaving
  justified code unchanged is successful.
- **Handoff.** Briefly state changed behavior, decisions, actual verification,
  and open risks. Label assumptions and unrun checks. Do not require unnecessary
  agents, plans, reports, checklists, artifacts, or review cycles; use them only
  when warranted within existing permissions.

### Technical continuity

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

### Documentation and working artifacts

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

### Tools and independent skills

Use the tools actually available on the current host. Prefer precise native reads
and edits for small changes; for large or unpredictable output, use an installed
analysis/context tool when available and derive focused results in code. Preserve
the host's routing rules. If a preferred tool is unavailable, disclose the relevant
limit and use a permitted alternative without installing a replacement by default.

Capture relevant evidence in full before filtering or summarizing it. Preserve
failures, exit status and source locations; do not truncate evidence before analysis
or filter away failures. Keep summaries focused without presenting incomplete
evidence as successful validation.

For background work, prefer completion notifications or bounded waits when the
host supports them. Avoid repeated status polling when those options are available.
Do not assume automatic wake-up; report timeouts and failures explicitly.

Specialized integrations belong to their own skills. For TypeSafe/Jev work, use
the separately installed `typesafe-ai` skill when relevant. lazier neither copies
its API guidance nor requires a TypeSafe call for routine engineering decisions.

### Explicit simplicity review

Run a simplicity review only when requested; an implementation request using
`lazier` still means implementation. Do not edit without authorization. Use the current
diff if scope is missing, or request the artifact. Inspect relevant requirements,
callers, and invariants. Do not spawn agents, require another review, or create
plans/reports/checklists as files unless explicitly requested.

Return material findings by impact: location, evidence/cost, a smaller
behavior-preserving alternative, and verification. Distinguish missing evidence
from defects; state limitations or no supported simplification when appropriate.
Do not force findings or report length. Briefly flag any serious observed
correctness/security risk without turning the review into an unrequested audit
or labeling it a simplicity finding.
