<div align="center">

# codex-lazier 0.7.2

**Small changes. Complete solutions.**

Engineering defaults that keep Codex and ChatGPT focused on simple, correct work.

[![CI](https://github.com/hudrucan/codex-lazier/actions/workflows/ci.yml/badge.svg)](https://github.com/hudrucan/codex-lazier/actions/workflows/ci.yml)
[![Runtime dependencies: none](https://img.shields.io/badge/runtime_dependencies-none-3b82f6)](#why-lazier)
[![License: MIT](https://img.shields.io/badge/license-MIT-64748b)](LICENSE)

[Quick start](#quick-start) · [Examples](#in-practice) · [Integrations](#optional-integrations) · [Development](#development)

</div>

## Why Lazier?

A change should stay proportional to the problem it solves.

Lazier is a portable engineering policy for **Codex Local** and **ChatGPT Web**.
It guides agents to understand the existing system, make a focused change, and
verify the behavior that matters.

- **Keep it simple.** Reuse existing tools and patterns. Add machinery when a
  current requirement justifies its cost.
- **Keep it correct.** Preserve contracts, failure handling, security boundaries,
  and recovery behavior. Necessary safeguards stay.
- **Keep it grounded.** Base decisions and review findings on source evidence.
  Run relevant checks and state what remains unverified.

The package is instructions: one Skill, two host adapters, a pinned C2C Web snapshot, and a
[shared policy](skills/codex-lazier/references/policy.md). No daemon, custom hook,
or runtime dependency. Simplicity reviews run only when you ask.

## Quick start

### 1. Get the package

Download the ZIP and its matching `.sha256` file from
**[GitHub Releases](https://github.com/hudrucan/codex-lazier/releases)**.
Put the two files from the same release in an otherwise empty directory:

```sh
sha256sum --check codex-lazier-*.sha256
```

On macOS, use `shasum -a 256 -c codex-lazier-*.sha256`. No release available yet?
[Build from source](#development).

### 2. Choose your host

#### Codex Local

Use one [host-supported discovery location](https://learn.chatgpt.com/docs/build-skills)
for each Skill; the user scope shown here is `~/.agents/skills`:

```sh
mkdir -p ~/.agents/skills
unzip codex-lazier-*.zip -d ~/.agents/skills
```

For an explicit update, replace the complete Skill directory at the installation
you selected, after verifying the new archive. Inspect existing discovery roots
first; do not install another copy under `~/.codex/skills` or a repository root.
A legacy/custom location may remain when supported by that host: update it in
place and keep any bootstrap bound to its actual path. Do not delete or migrate
legacy copies automatically.

Then start a new session and use `$codex-lazier` in your request.

<details>
<summary><strong>Apply Lazier automatically to coding tasks</strong></summary>

Add an instruction to your repository's `AGENTS.md`, or your Codex home's
`AGENTS.md` (normally `~/.codex/AGENTS.md`), to read and apply the installed
Skill's `references/codex.md` once per chat for every coding task. Use its actual
absolute installed path. That reference loads `references/policy.md` itself;
no manual Skill invocation is needed for this bootstrap.
Preserve existing guidance and check for an active `AGENTS.override.md`.

Start a new session and ask Codex to summarize its loaded instructions.
Installing the Skill alone does not activate persistent instructions.
The [Codex reference](skills/codex-lazier/references/codex.md) owns C2C handoffs
and Context Mode preferences. For a legacy installation that copied Lazier into
`AGENTS.md`, replace only that Lazier block with the bootstrap above. Keep the
installed references together; do not maintain another policy copy.

</details>

#### ChatGPT Web

1. Where Skill uploads are supported, install the release ZIP as a ChatGPT Skill.
2. Start a new conversation and check that `codex-lazier` is available. The Skill
   loads its Web reference for coding and automatic C2C handoff audits.
3. Keep MCP connector, Hub and workspace routing in **Project Instructions**.
   Lazier behavior comes from the installed Skill.

For hosts without Skill support, make the complete extracted reference tree
available offline (including `references/c2c/`), and optionally select the existing
[policy](skills/codex-lazier/references/policy.md) and
[Web reference](skills/codex-lazier/references/web.md) available as Project sources
and instruct the Project to apply them with their task-specific references. Disclose if the
host cannot read them. Preserve existing Project guidance; no Lazier copy in
Project Instructions is needed. Installing the Skill neither connects a repository
nor grants access.

## In practice

### Implement a change

```text
Use $codex-lazier to add pagination to this endpoint.
Follow the existing API conventions and test the relevant behavior.
```

The agent traces the current flow, chooses a focused implementation, and
reports the checks it actually ran. No automatic simplicity-review cycle.

### Ask for a simplicity review

```text
Review this diff for unnecessary complexity.
Report supported simplifications; do not edit.
```

Findings need evidence and a smaller alternative that preserves required
behavior. Justified code can stay unchanged.

### Delegate through C2C

```text
[C2C Task]
Repo: <repository>; workspace: <registered workspace ID>.
Add pagination using the existing API conventions.
Run focused validation. Do not commit or push.
```

With C2C configured, Web plans and audits while Codex implements and tests
against local source. `[C2C Plan]` only plans; `[C2C Task]` implements within
scope. Markers and drafted prompts do not execute work or grant permissions.

## Optional integrations

Lazier works on its own. These integrations reuse tools you already have.

- **[Codex with ChatGPT](https://github.com/hudrucan/codex-with-chatgpt)** connects Web planning
  and audits with Codex implementation. It owns repository access and the
  handoff contract. The Web ZIP bundles its pinned canonical files;
  [source pin](tools/c2c-source.json) records the revision and hashes. Codex uses
  the separately installed native C2C contract.
  The [Web reference](skills/codex-lazier/references/web.md) covers automatic
  handoff audits, manual Fix/Commit prompts and opt-in `auto=true` delivery;
  omitted `auto` or `auto=false` stays manual. Automatic delivery follows C2C's
  manual fallback rules on failure and requires runtime/OAuth support and an
  accepted MCP result received by the terminal; it does not authorize commits,
  pushes or rollout.
- **[codex-context-mode](https://github.com/hudrucan/codex-context-mode) v0.1.1**
  keeps large analysis output out of the conversation. This Codex fork derives
  from [context-mode by Mert Koseoğlu](https://github.com/mksglu/context-mode)
  under Elastic License 2.0. Reuse the existing plugin
  `codex-context-mode@hudrucan`: it bundles six skills (`main`, `doctor`, `index`,
  `search`, `stats`, `purge`), six native hooks (`PreToolUse`, `PostToolUse`,
  `SessionStart`, `PreCompact`, `UserPromptSubmit`, `Stop`) and one stdio MCP
  named `codex-context-mode`, preserving the `ctx_*` tool names. Do not separately
  register an MCP, copy skills, install user hooks or add symlinks. Keep mutable
  runtime data in `~/.codex-context-mode/` (or its configured external root);
  installing Lazier does not migrate, purge or modify that runtime or plugin.
  The Codex reference prefers installed `ctx_*` tools and falls back to bounded
  native tools when unavailable. Small observations and edits can stay direct.
- **[TypeSafe Jev](https://docs.typesafe.ai/introduction/coding-agents)** offers
  a second opinion on substantial C2C decisions with meaningful technical
  trade-offs. Web normally asks once after inspecting constraints and evidence,
  or defers to Codex when fresh local inspection is needed. Reuse the advice;
  skip trivial or settled decisions.

Jev remains advisory. Never automatically forward private source, secrets,
or credentials. Unavailable or abstaining advice does not block the task.

## What to expect

Lazier guides engineering judgment; it does not enforce behavior or guarantee
correctness. User instructions, project requirements, and platform security take
precedence. A successful build or a model probability is not a correctness proof.

Host support determines Skill discovery and invocation. Optional integrations
need their own configuration and permissions; installing Lazier grants neither.
Context Mode installation alone does not prove routing or enforcement.

## Development

Python 3.9+ and its standard library are enough. Supply an explicit local C2C
checkout whose origin, HEAD and allowlisted inputs match [the pin](tools/c2c-source.json).
Builds never fetch or execute C2C code, and never use a different working tree
silently. With that checkout already available, all commands run offline:

```sh
python3 tools/test_package.py --c2c-source /path/to/pinned-c2c
python3 tools/package.py --c2c-source /path/to/pinned-c2c --build
python3 tools/package.py --c2c-source /path/to/pinned-c2c
git diff --check
```

On Windows use `py -3`. ZIP, SHA-256 and provenance sidecar go into ignored
`dist/`; do not commit generated packages. Each ZIP has sixteen files: the six
Lazier files (entrypoint, UI metadata, policy, two adapters, LICENSE), eight
C2C Markdown references under `references/c2c/`, their LICENSE, and
`provenance.json` identifying package version, C2C repository/revision/hashes and
all packaged input hashes. The three C2C workflow contracts are unmodified. To
prevent duplicate Skill discovery, the reference entrypoint is packaged as
`entrypoint.md`, and its setup backlink is adjusted to that filename. Provenance
records both packaging changes alongside the original source hashes and resulting
packaged hashes. The sender's transitive diagnostic links still resolve offline.
The only discoverable `SKILL.md` in the archive is Lazier's root entrypoint.
No protocol copies live in Lazier source. Presence
in the ZIP does not mean a reference should be loaded.

Validation checks metadata/version, full local file/anchor closure, source identity,
pinned bytes, symlinks/containment, CRCs, stale content/sidecars and reproducibility.
Tests extract into an independent directory; reading Web guidance needs no source
checkout, network or MCP. Model smoke cases are in [the smoke matrix](tools/smoke-cases.json);
structural assertions do not prove model behavior. A new session using the actually
installed artifact must observe smoke success before calling it daily-ready.
Live MCP/terminal E2E acceptance is a separate result, never implied by packaging.

The [CI workflow](.github/workflows/ci.yml) checks out C2C at the exact pinned
revision with read-only permissions and no persisted credentials. It builds,
checks reproducibility and validates downloaded release assets. Only the tag-only
release job can publish ZIP, checksum and provenance. Tags must match
`v<VERSION>` in `tools/package.py`; update that value and the three guidance
headings together. Updating the C2C snapshot requires a verified full commit,
allowlist hashes and preserved license; never pin uncommitted changes or mutable
`main`/`latest`.

Contributions should stay focused, preserve the Skill contract, and include
checks appropriate to the change.

## License

[MIT](LICENSE). See [research and provenance](RESEARCH.md) for the references
behind the policy. The pinned C2C text and its MIT notice are bundled; no upstream executable code is bundled.
