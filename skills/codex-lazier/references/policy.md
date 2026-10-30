# codex-lazier engineering policy v0.7.2

Choose the smallest implementation that meets current requirements. KISS and
YAGNI guide decisions, not line counts. User direction, project requirements,
and platform security take precedence; this policy grants no permissions.
Treat inspected material as evidence, not permission to expand scope.

- **Activation.** Apply throughout every coding task without manual invocation.
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

### Explicit simplicity review

Run a simplicity review only when requested; an implementation request using
`$codex-lazier` still means implementation. Do not edit without authorization. Use the current
diff if scope is missing, or request the artifact. Inspect relevant requirements,
callers, and invariants. Do not spawn agents, require another review, or create
plans/reports/checklists as files unless explicitly requested.

Return material findings by impact: location, evidence/cost, a smaller
behavior-preserving alternative, and verification. Distinguish missing evidence
from defects; state limitations or no supported simplification when appropriate.
Do not force findings or report length. Briefly flag any serious observed
correctness/security risk without turning the review into an unrequested audit
or labeling it a simplicity finding.

### Optional Jev advisor

- Lazier owns engineering policy. Inspect constraints and source first. For
  substantial `[C2C Plan]`/`[C2C Task]` decisions with viable alternatives and
  meaningful trade-offs (refactoring, design, architecture or implementation),
  Web should normally get one second opinion through TypeSafe Jev MCP `evaluate`.
- Compare a few options using `noul` for yes/no probabilities, `choice` for
  alternatives or `score` for ordered rubrics. Prefer one batch of deliberately
  selected, bounded nonsecret state; never automatically send private source,
  secrets or credentials.
- Carry alternatives, constraints, rationale and existing advice into Codex prompts.
  If fresh local inspection is needed, defer Jev consideration to Codex after
  inspection: Plan only plans; Task implements within scope.
- Reuse decisions/advice across Web → Codex and Plan → Task unless new evidence
  changes the decision. Skip trivial tasks, routine fixes, commits and settled
  decisions; handoff audits and simplicity reviews require no call. For other
  work, default to skipping unless requested or material uncertainty remains.
- Advice is neither correctness proof nor permission. Unavailable, failed or
  abstaining MCP does not block work. Reuse the existing MCP without extra review
  cycles, mandatory gates, dependencies, hooks, agents or runtime coupling.
