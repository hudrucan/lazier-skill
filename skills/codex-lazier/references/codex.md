## codex-lazier v0.8.0 — Codex

Read and apply the [shared policy](policy.md), including its optional Jev
guidance, to every coding task without a manual skill call.

For C2C work, follow the [C2C integration](../SKILL.md#c2c-integration)
with the separately installed native C2C Skill.

Reuse guidance already read and still valid in this session, including policy
and this adapter; reread changed guidance or after missing/uncertain context.
Guidance reuse never replaces fresh repository evidence.

- Prefer `rg` for precise, bounded searches; consider `ast-grep` for structural
  AST queries that `rg` cannot express well.
- Avoid repeated background-job polling with `sleep`, `ps`, `pgrep`, or `top`.
  Prefer completion notifications when the runtime supports them, or a bounded
  wait. Do not assume automatic wake-up; report timeouts and failures explicitly.

### Context Mode

- Reuse the installed `codex-context-mode` v0.1.1 plugin
  (`codex-context-mode@hudrucan`), derived from Mert Koseoğlu's upstream
  `context-mode`. It bundles six skills (`main`, `doctor`, `index`, `search`,
  `stats`, `purge`), six native hooks (`PreToolUse`, `PostToolUse`, `SessionStart`,
  `PreCompact`, `UserPromptSubmit`, `Stop`) and one MCP named `codex-context-mode`.
  Preserve `ctx_*` tool names and external runtime data in `~/.codex-context-mode/`
  (or its configured external root). Do not add standalone MCP registrations,
  copied skills, user hooks or symlinks. Inspect Windows installations read-only
  when diagnosing bindings; report mismatches without changing installations.
- Use native tools for precise bounded searches/reads and edits; prefer installed
  `ctx_*` tools for large/unpredictable output and verbose tests.
- Discover as needed: `ctx_execute_file` analyzes files, `ctx_execute` handles one
  operation, `ctx_batch_execute` captures related output. Index/search only when
  repeated retrieval helps; avoid redundant indexing and capability/size probes.
- Capture full evidence; report exit status, failures and paths/lines. Never
  truncate before capture, filter away failures or re-index existing context.
  Preserve access and secret boundaries.
- Reuse the plugin without duplicate servers/hooks or copied code. Verify MCP,
  hook trust and actual routing separately; honor deny/rewrite decisions.
  Advisory instructions are not hard enforcement.
- If unavailable/failing, disclose once and use bounded native tools under the
  same evidence/permission rules; no endless retries or dependency installation
  merely to complete ordinary work.
