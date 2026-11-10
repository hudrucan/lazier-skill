# Agent audits

Store one latest skill audit per agent: `codex.json`, `claude.json`, `agy.json`
or `grok.json`. For example, [Codex](codex.json) or [Antigravity](agy.json). The tested version belongs inside
the file, not in its path.

- Each new audit replaces that agent's file, including when its tested version
  changes. Do not append runs or create version directories, dated copies,
  history directories or audit indexes.
- A missing file means unverified. Do not create placeholder results or carry
  another agent's verdict forward.
- Use the shared [smoke cases](../tools/smoke-cases.json) unchanged, with fixtures from
  `python3 tools/make_smoke_fixtures.py <empty-dir> --host <agent> --skill-entry <path>`. Record the
  definition revision or hash, cases run, omissions and unmet conditions.
- Include the audit date, agent/CLI, model and reasoning setting, exact package
  version, commit and archive SHA-256, scope, summary and per-case results.
- Claim `passed` only when every required case and pass condition is met and no
  fail condition occurs. Use `failed` for unmet conditions and `incomplete` for
  unfinished coverage. Distinguish process failures from behavioral findings.
- Keep raw traces and fixtures in ignored `.agent-artifacts/`, with a local
  evidence pointer in the audit. Do not commit raw logs or private machine data.

These are maintained verification records, outside the installed skill payload.
Use the existing Codex file as a format example, with your own observed results.
