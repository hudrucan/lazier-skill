# Research and compatibility notes

Sources checked 2026-10-20; current behavior is defined by the shared policy and
host references in `skills/codex-lazier/references/`.
These sources informed an original policy; their skill text,
examples, agents, and language guides are not vendored. Links below pin the
reviewed GitHub revisions so the decisions remain inspectable.

## Engineering references

| Reference and reviewed files | License at revision | Adopted principle | Deliberate departure |
| --- | --- | --- | --- |
| [4everWZ/codex-minimal-engineering](https://github.com/4everWZ/codex-minimal-engineering/tree/c20ea80bad91c76df530e01797ce966b652cdaf0): `skills/minimal-implementation/SKILL.md`, `skills/overengineering-review/SKILL.md` | [MIT](https://github.com/4everWZ/codex-minimal-engineering/blob/c20ea80bad91c76df530e01797ce966b652cdaf0/LICENSE) | Require a current responsibility for machinery; protect boundaries and failure contracts; make reviews evidence-based. | Use one shared engineering policy and two host references in an installable Skill, with optional simplicity review. Do not require a second implementation when one implementation establishes a real boundary. Do not suppress a serious observed security defect merely because the review is narrow. |
| [alvindemesadev/boring-engineering](https://github.com/alvindemesadev/boring-engineering/blob/34dae8cd569039f544c34f9553ff33a45a6ce70f/SKILL.md) | [MIT](https://github.com/alvindemesadev/boring-engineering/blob/34dae8cd569039f544c34f9553ff33a45a6ce70f/LICENSE) | Reuse existing capabilities, meet present requirements, and balance simplicity with necessary safeguards. | Omit fixed decision gates, compulsory final checklists, compactness/blank-line prescriptions, and rigid explanation limits. A built-in must fit the actual semantics; its mere existence is insufficient. |
| [getsentry/skills code-simplifier](https://github.com/getsentry/skills/blob/f57ada2d0b640406ea7e25b11d636c530e77c58b/skills/code-simplifier/SKILL.md) and [agent counterpart](https://github.com/getsentry/skills/blob/f57ada2d0b640406ea7e25b11d636c530e77c58b/agents/code-simplifier.md) | Repository [Apache-2.0](https://github.com/getsentry/skills/blob/f57ada2d0b640406ea7e25b11d636c530e77c58b/LICENSE); the reviewed files acknowledge Anthropic's code-simplifier | Preserve behavior, constrain scope, and prefer understandable code over compressed expressions. | Exclude React/TypeScript syntax preferences, specialist persona, model selection, proactive finishing passes, and agent delegation. Those are not portable engineering requirements. |
| [caarlos0/dotfiles code-simplifier](https://github.com/caarlos0/dotfiles/blob/fb7f64f0c2ac2551f0c440f475fc6439e3d607f2/skills/code-simplifier/SKILL.md) | [MIT](https://github.com/caarlos0/dotfiles/blob/fb7f64f0c2ac2551f0c440f475fc6439e3d607f2/LICENSE.md) | Respect repository requirements; check external uses before deleting code; avoid historical comments and reuse still-relevant checks. | Omit a mandatory finishing pass and language-guide routing. Current-state docs can still include release notes, compatibility guidance, and project-required decision records. |

License labels describe the reviewed sources, not a relicensing of upstream
material. The package contains independently written instructions,
plus a standard MIT license for its original material. No third-party source
or substantial excerpts are distributed; upstream license files are linked,
not copied into the archive. Any later vendoring needs its own attribution and
license assessment, including notices on the particular files being copied.

## Instruction conventions and platform evidence

- [AGENTS.md conventions](https://agents.md/) support concise project context
  and local instructions. Examples of test commands or style rules are examples,
  not universal mandates. Keep the repository's concrete requirements rather
  than importing another project's process.
- [Official global instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
  establishes Codex-home overrides and more specific project guidance. A package
  cannot redefine the platform instruction hierarchy or bypass its permissions.
- [Official skill documentation](https://learn.chatgpt.com/docs/build-skills)
  establishes `SKILL.md`, local discovery, and invocation metadata. Implicit
  discovery does not replace persistent instructions. Web skill upload and
  metadata handling have not been verified on this account.
- [Official Project documentation](https://learn.chatgpt.com/docs/projects)
  establishes shared Project instructions and sources, without automatic local
  filesystem access. With the installed Skill, Project Instructions retain routing.
  Legacy hosts may explicitly load the same policy and Web reference as Project
  sources; attaching `AGENTS.md` alone does not activate them. UI labels and account
  availability are untested.
- [Agent Skills specification](https://agentskills.io/specification) supplies
  manifest/name constraints. [Official API skill packaging](https://developers.openai.com/api/docs/guides/tools-skills)
  documents one top-level folder in a ZIP. API ZIP acceptance does not establish
  ChatGPT Web ZIP installation. No upload, plugin registration, or installation
  was performed for this package.

## Synthesis

Engineering defaults apply throughout coding tasks; simplicity review stays
optional. Required behavior, boundaries, and project requirements determine
necessary complexity, not line or implementation counts.

The shared policy owns engineering, reusable technical continuity, simplicity
review and optional Jev guidance. The Skill loads only the current host reference:
Codex retains Context Mode preferences; Web adds engineering prompt guidance.
Both delegate C2C work through the entrypoint's concise integration reference to
the separately installed `codex-with-chatgpt` Skill. That project owns handoff
markers, workflow, routing, sender/receiver, callback and recovery. Native Local
integration uses the existing `hudrucan` marketplace plugin (v0.4.0 integration
baseline); this is compatibility context, not a source pin or build requirement.
Lazier distributes no C2C contracts and needs no C2C checkout to build or test.
Its seven-member artifact records only Lazier input hashes in provenance.
Codex's automatic `AGENTS.md` bootstrap loads the same reference and policy. Legacy setup
uses these canonical files without separate source copies. No generator, custom
hook, or policy-loading service is added. Live Skill-only activation remains
unverified; package validation does not establish host behavior. Fresh-session
standalone C2C and combined Lazier/C2C observations, plus accepted callbacks with
matching terminal receipts, are required before a production cutover. Preserve
verified v0.7.3 assets for whole-package rollback; never retain a receiver fallback
inside the new package. See the README's migration and acceptance criteria.
