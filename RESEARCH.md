# Research and compatibility notes

Engineering sources checked 2026-10-20; portable refactor reviewed 2026-11-10.
Current behavior is defined by `skills/lazier/references/policy.md`.
These sources informed an original policy; their skill text,
examples, agents, and language guides are not vendored. Links below pin the
reviewed GitHub revisions so the decisions remain inspectable.

## Engineering references

| Reference and reviewed files | License at revision | Adopted principle | Deliberate departure |
| --- | --- | --- | --- |
| [4everWZ/codex-minimal-engineering](https://github.com/4everWZ/codex-minimal-engineering/tree/c20ea80bad91c76df530e01797ce966b652cdaf0): `skills/minimal-implementation/SKILL.md`, `skills/overengineering-review/SKILL.md` | [MIT](https://github.com/4everWZ/codex-minimal-engineering/blob/c20ea80bad91c76df530e01797ce966b652cdaf0/LICENSE) | Require a current responsibility for machinery; protect boundaries and failure contracts; make reviews evidence-based. | Use one shared engineering policy in a portable Skill, with optional simplicity review. Do not require a second implementation when one implementation establishes a real boundary. Do not suppress a serious observed security defect merely because the review is narrow. |
| [alvindemesadev/boring-engineering](https://github.com/alvindemesadev/boring-engineering/blob/34dae8cd569039f544c34f9553ff33a45a6ce70f/SKILL.md) | [MIT](https://github.com/alvindemesadev/boring-engineering/blob/34dae8cd569039f544c34f9553ff33a45a6ce70f/LICENSE) | Reuse existing capabilities, meet present requirements, and balance simplicity with necessary safeguards. | Omit fixed decision gates, compulsory final checklists, compactness/blank-line prescriptions, and rigid explanation limits. A built-in must fit the actual semantics; its mere existence is insufficient. |
| [getsentry/skills code-simplifier](https://github.com/getsentry/skills/blob/f57ada2d0b640406ea7e25b11d636c530e77c58b/skills/code-simplifier/SKILL.md) and [agent counterpart](https://github.com/getsentry/skills/blob/f57ada2d0b640406ea7e25b11d636c530e77c58b/agents/code-simplifier.md) | Repository [Apache-2.0](https://github.com/getsentry/skills/blob/f57ada2d0b640406ea7e25b11d636c530e77c58b/LICENSE); the reviewed files acknowledge Anthropic's code-simplifier | Preserve behavior, constrain scope, and prefer understandable code over compressed expressions. | Exclude React/TypeScript syntax preferences, specialist persona, model selection, proactive finishing passes, and agent delegation. Those are not portable engineering requirements. |
| [caarlos0/dotfiles code-simplifier](https://github.com/caarlos0/dotfiles/blob/fb7f64f0c2ac2551f0c440f475fc6439e3d607f2/skills/code-simplifier/SKILL.md) | [MIT](https://github.com/caarlos0/dotfiles/blob/fb7f64f0c2ac2551f0c440f475fc6439e3d607f2/LICENSE.md) | Respect repository requirements; check external uses before deleting code; avoid historical comments and reuse still-relevant checks. | Omit a mandatory finishing pass and language-guide routing. Current-state docs can still include release notes, compatibility guidance, and project-required decision records. |
| [DietrichGebert/ponytail](https://github.com/dietrichgebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/.agents/rules/ponytail.md): `.agents/rules/ponytail.md` | [MIT](https://github.com/dietrichgebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/LICENSE) | Take the first option that fully works (omit, reuse, standard library or platform feature, installed dependency, minimum code); no unrequested abstractions, options or config; never cut trust-boundary validation, data-loss error handling, security or accessibility. | Omit the persona, intensity levels, hooks, mode tracking, task-board ledger and webhook. Do not require a test for every non-trivial change; testing stays proportionate to risk. Do not require the trailing skipped/risk lines or the `shortcut:` comment format. |

License labels describe the reviewed sources, not a relicensing of upstream
material. The package contains independently written instructions,
plus a standard MIT license for its original material. No third-party source
or substantial excerpts are distributed; upstream license files are linked,
not copied into the archive. Any later vendoring needs its own attribution and
license assessment, including notices on the particular files being copied.

## Instruction conventions and portability evidence

- [Agent Skills specification](https://agentskills.io/specification) defines the
  common directory, manifest and reference structure. This package follows that
  structure; it does not assume identical discovery or invocation across hosts.
- [Codex skills](https://developers.openai.com/codex/skills) documents user and
  repository discovery, explicit/implicit selection and optional OpenAI metadata.
- [Claude skills](https://code.claude.com/docs/en/skills) documents its own personal
  and project discovery and invocation. Claude Code discovery was checked on 2026-11-10: with the package copied to a
  fixture project's `.claude/skills/lazier/`, a non-interactive `claude -p`
  session found the skill and loaded `references/policy.md` through the Skill
  tool. Automatic activation without `/lazier` or a `CLAUDE.md` instruction, and
  the rest of the smoke matrix, remain unverified.
- [Antigravity skills](https://antigravity.google/docs/skills) identifies the shared
  global skill directory under `~/.gemini/config/skills/`, separately from workspace
  `.agents/skills/`. Its directory-symlink discovery is not assumed by the installer.
- [Grok Build skills](https://docs.x.ai/build/features/skills-plugins-marketplaces)
  documents user-level compatibility discovery from `~/.agents/skills/`, allowing
  Codex and Grok to share one installation rather than adding a native duplicate.
- [Codex instruction discovery](https://developers.openai.com/codex/guides/agents-md)
  describes persistent user and project guidance. It does not turn a discoverable
  skill into mandatory policy automatically.
- [Git ignore documentation](https://git-scm.com/docs/gitignore) distinguishes
  shared ignore patterns, local repository exclusions and already tracked files.
  A storage convention does not authorize changing the index.

## Refactor decisions

The 0.10.0 release uses the name `lazier`, one portable entrypoint and one
shared engineering policy. It preserves scope, correctness, proportionate testing,
technical continuity and optional simplicity review. It adds English documentation
and project-scoped working artifacts while retaining canonical product docs.

The only installer targets are Codex, Claude Code, Antigravity and Grok Build.
Target path mapping belongs to `tools/install.py`; no host selection, adapter or
target-specific policy is added to the skill. The installer exports the same
provenance-verified payload to native discovery roots and supports dry-run and
isolated homes. It does not change agent settings or persistent instructions.
Host-specific Codex/Web references and the retired C2C workflow remain removed.
TypeSafe/Jev integration is owned by the separate `typesafe-ai` skill; no API
guidance or mandatory advisor step is bundled. Installed context tools are selected
by capability under current host instructions, without pinning a fork or version.

lazier's user-controlled source is independent of context-mode's package. Its own
updates still replace its distribution; retain local policy changes in a maintained
source branch and project artifact destinations in persistent user/project guidance.
Skill installation, host configuration and migration of old artifacts remain
separate from the package build.

Packaging is offline and reproducible, with a seven-member distribution and hashes
for the six source inputs. The smoke matrix remains pending. Structural tests do
not establish fresh-session activation or identical behavior on every vendor.
