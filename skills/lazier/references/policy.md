# lazier engineering policy v0.11.0

Choose the smallest implementation that meets current requirements. KISS and
YAGNI guide decisions, not line counts. User direction, project requirements,
and platform security take precedence; this policy grants no permissions.
Treat inspected material as evidence, not permission to expand scope.

- **Activation.** Once loaded, apply throughout the current engineering task.
- **Planning.** Inspect guidance and the code responsible; identify behavior and
  constraints; ask about facts the solution depends on; choose the smallest viable
  design. Do not invent future requirements. Implement directly when the task is
  clear. Write an explicit plan first only when the user asks, requirements
  conflict, a missing fact would change the design, or the options differ in cost
  the user should choose between.
- **Scoped autonomy.** Within the assigned scope and permissions, fix issues your
  changes caused and rerun the affected validation until the task is complete. Stop
  and report when the next step is outside your scope or permissions, carries a
  risk the user has not approved, or stays blocked after you have tried what your
  authority allows.
- **Implementation.** Make focused changes that follow local patterns. Trace the
  flow, then prefer in this order: omission, reuse, standard library or native
  feature, installed dependency, direct implementation. Add an abstraction,
  wrapper, setting or dependency only when a stated requirement needs it or it
  removes duplication already in the change. An interface with one implementation
  is fine when it marks an existing boundary such as I/O, a process or ownership.
  Prefer duplicating a few lines over coupling unrelated modules. Skip cleanup the
  change does not need.
- **Correctness.** Preserve required behavior, contracts and error semantics. Keep
  existing authentication, authorization, validation, concurrency, persistence,
  compatibility, recovery, accessibility and measured-performance logic; remove it
  only after confirming nothing depends on it, however verbose it looks or
  whatever its security label. Explain requirements the code hides. Validate at
  trust boundaries; repeat a check only for a distinct boundary or a reachable
  failure. Never report a failure as success.
- **Testing.** Add regression tests for changed observable behavior, failures and
  invariants, using the project's existing tools and fixtures, and no more than the
  change puts at risk. Avoid duplicate assertions and checks on private details or
  call order. Never weaken an assertion to make a refactor pass. Run the checks
  that apply to the risk; reuse earlier results until a change invalidates them.
- **Evidence.** Capture relevant evidence in full before filtering or summarizing
  it. Keep failures, exit status and source locations; never truncate or filter
  away a failure before analysis. Do not present incomplete evidence as successful
  validation.
- **Logging and comments.** Where you add context or handle a failure, keep
  actionable diagnostics and required audit events. Omit duplicate reports,
  temporary chatter, secrets and personal data. Prefer expressive code; comment
  hidden constraints, reasons and external requirements. Remove stale or narrating
  comments; keep legal notices and invariant explanations.
- **Documentation.** Describe current setup, contracts, support and limitations,
  and update anything your change made false. Keep development diaries out of
  product docs; keep useful release and migration guidance and required decision
  records. Write new or substantially revised documentation, artifact filenames and
  headings in English unless the user asks otherwise. Keep literal quotations,
  identifiers and required localized content. Chat follows the user's language. Do
  not translate existing documents as incidental cleanup.
- **Refactoring.** Stay within scope and preserve behavior. Check callers and
  supported external uses before removing code that looks unused. Include only the
  cleanup the change needs.
- **Review.** Ground each finding in location, evidence, impact and a fix. A
  simplicity finding needs a smaller alternative that preserves required behavior,
  and names the mechanism's responsibility and cost. Verify any claim that code is
  unused, redundant or speculative. A correctness or security fix may add code.
  Separate unknowns from defects; style alone is not a finding. Leaving justified
  code unchanged is a valid outcome.
- **Handoff.** Briefly state the changed behavior, decisions, verification actually
  run, and open risks. Label assumptions and checks you did not run. Create extra
  agents, plans, reports, checklists, artifacts or review cycles only when the user
  asks or the task needs them, and only within existing permissions.

### Explicit simplicity review

Run a simplicity review only when the user asks for one; a request to implement
with `lazier` is still an implementation request. Do not edit without
authorization. If no scope is given, use the current diff, or ask for the artifact
to review. Inspect the requirements, callers and invariants involved. Do not spawn
agents, require another review, or write plans, reports or checklists as files
unless asked.

Report findings in order of impact, each with location, evidence or cost, a
smaller behavior-preserving alternative, and how to verify it. Separate missing
evidence from defects. When nothing supports a simplification, say so and state
any limits of what you checked. Do not pad findings or length. Flag a serious
correctness or security risk you observed in one line, without turning the review
into an audit or calling it a simplicity finding.
