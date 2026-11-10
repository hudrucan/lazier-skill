# Research and compatibility notes

Status reviewed 2026-11-10 for lazier 0.11.0. Sources below are pinned provenance;
they were not all re-audited for this release.

## Policy sources

| Source | License at revision | Adopted principle and limits |
| --- | --- | --- |
| [codex-minimal-engineering](https://github.com/4everWZ/codex-minimal-engineering/tree/c20ea80bad91c76df530e01797ce966b652cdaf0) | MIT | Current responsibilities, boundaries and evidence; no mandatory second implementation. |
| [boring-engineering](https://github.com/alvindemesadev/boring-engineering/blob/34dae8cd569039f544c34f9553ff33a45a6ce70f/SKILL.md) | MIT | Reuse and present requirements; no fixed gates, checklists or formatting prescriptions. |
| [Sentry code-simplifier](https://github.com/getsentry/skills/tree/f57ada2d0b640406ea7e25b11d636c530e77c58b) | Apache-2.0; reviewed files acknowledge Anthropic | Preserve behavior and readability; omit language-specific rules, personas, finishing passes and delegation. |
| [caarlos0 code-simplifier](https://github.com/caarlos0/dotfiles/blob/fb7f64f0c2ac2551f0c440f475fc6439e3d607f2/skills/code-simplifier/SKILL.md) | MIT | Respect scope, check callers and reuse valid verification; no compulsory final review. |
| [ponytail](https://github.com/dietrichgebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/.agents/rules/ponytail.md) | MIT | Prefer omission, reuse and native capabilities; preserve safeguards and proportionate testing. Omit persona, hooks, modes and task ledger. |

The package contains original MIT instructions, not vendored upstream skill text.
License labels apply to the pinned sources; later vendoring requires its own
attribution and license assessment.

## Current design

[SKILL.md](skills/lazier/SKILL.md) loads the shared
[core policy](skills/lazier/references/policy.md), with
[artifacts and continuity](skills/lazier/references/artifacts.md) and
[integrations](skills/lazier/references/integrations.md) loaded when relevant.
English documentation, private project artifacts and explicit-only simplicity
review remain defaults; user direction and host permissions take precedence.

The installer exports the same seven-file payload for Codex, Claude Code,
Antigravity and Grok. It does not edit host settings or persistent instructions.
[CLAUDE.md](CLAUDE.md) imports [AGENTS.md](AGENTS.md) for this repository.
Policy ownership is independent of context-mode; TypeSafe/Jev guidance stays in
`typesafe-ai`. See [README](README.md) for discovery paths and installation.

## Verification status

| Scope | Evidence and limits |
| --- | --- |
| Package and installer | Integrity, reference closure, reproducibility, safe installation and a disposable-home 0.10.0-to-0.11.0 upgrade checked. These do not prove model behavior. |
| Agent behavior | [Latest audits](audits/README.md) keep one record per agent, including [Codex](audits/codex.json). Each record states its tested version, exact payload, scope, results and limits. Missing agent records mean unverified. |

The [smoke matrix](tools/smoke-cases.json) contains shared definitions, not verdicts.
Consult the relevant agent audit for open conditions and replace it after retesting;
do not accumulate audit history or infer results for other agents or integrations.
