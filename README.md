<div align="center">

# codex-lazier 0.8.0

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

The package is instructions: one Skill, two host adapters, and a
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
The [Codex reference](skills/codex-lazier/references/codex.md) applies engineering
policy, delegates C2C to its separate Skill, and retains Context Mode preferences.
For a legacy installation that copied Lazier into
`AGENTS.md`, replace only that Lazier block with the bootstrap above. Keep the
installed references together; do not maintain another policy copy.

</details>

#### ChatGPT Web

1. Where Skill uploads are supported, install the release ZIP as a ChatGPT Skill.
2. Start a new conversation and check that `codex-lazier` is available. The Skill
   loads its Web reference for engineering work. C2C work uses the separately
   installed `codex-with-chatgpt` Web Skill.
3. Keep MCP connector, Hub and workspace routing in **Project Instructions**.
   Lazier behavior comes from the installed Skill.

For hosts without Skill support, make the complete extracted reference tree
available offline, and optionally select the existing
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
  entire handoff workflow, routing, sender/receiver, callback and recovery.
  Install its Web Skill separately; for Codex Local, reuse the native C2C plugin
  (`codex-with-chatgpt@hudrucan`, v0.4.0 integration baseline) and its own setup
  guidance. Lazier's [integration reference](skills/codex-lazier/SKILL.md#c2c-integration)
  delegates to the installed C2C entrypoint without bundling, fetching or pinning
  its contracts. Missing C2C blocks only C2C work; ordinary engineering and
  packaging remain usable. C2C preserves selected routing and `auto=true` under
  its own contract; installing Lazier grants no connection or delivery permission.
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

## Upgrading from v0.7.3

v0.8.0 removes the bundled C2C receiver. Before a production cutover, verify the
separate C2C Web Skill and native Local integration. Retain the verified v0.7.3
ZIP, checksum and provenance as rollback assets. New builds use versioned
filenames and leave those assets unchanged.

When an installation update is authorized, replace the complete Lazier package
at its existing location; do not overlay it or add a second discovery root.
This removes stale `references/c2c/` files. Keep the existing AGENTS bootstrap,
Project routing, C2C/Context Mode installations and host configuration. Start a
fresh session so cached receiver instructions cannot conceal a missing C2C Skill.
Rollback restores the complete verified v0.7.3 package at that same location,
then starts a fresh session; the new ZIP contains no fallback contract.

Production acceptance requires separate evidence for standalone C2C without the
old Lazier receiver and for the candidate Lazier plus C2C in fresh sessions.
Record artifact hashes, independent C2C versions, loaded paths and tool traces.
An Auto C2C E2E pass requires correctly routed MCP source review, an unchanged
source fingerprint, `submit_audit_result` returning `accepted:true`, and the
matching terminal result for the same Hub/workspace/task/attempt/handoff within
the original deadline. Required audits must end in PASS; unresolved FIX,
BLOCKED, ERROR, drift, timeout or a missing receipt blocks cutover. A plan-only
audit need not produce a code diff. A chat PASS, MCP READY, packaging success or
callback acceptance without its terminal receipt is insufficient. Recovery and
fallback remain C2C's responsibility. No fresh-session or live E2E PASS is
established by the package tests.

## Development

Python 3.9+ and its standard library are enough. Builds and tests run offline
from Lazier source alone, without Git, a C2C checkout, network or installed C2C:

```sh
python3 tools/test_package.py
python3 tools/package.py --build
python3 tools/package.py
git diff --check
```

On Windows use `py -3`. ZIP, SHA-256 and provenance sidecar go into ignored
`dist/`; do not commit generated packages. Each ZIP has exactly seven files:
the six Lazier files (entrypoint, UI metadata, policy, two adapters, LICENSE) and
`provenance.json`. Provenance contains only `name`, `version` and `sha256` hashes
for the six packaged inputs; the sidecar must match its embedded bytes.
The only discoverable `SKILL.md` is Lazier's root entrypoint. All local links
resolve within the package; the external C2C installation reference is not a
build dependency or an offline receiver. No C2C contracts or source pin are bundled.

Validation checks metadata/version, full local file/anchor closure, source bytes,
symlinks/containment, member allowlist and types, CRCs, stale content/sidecars and
reproducibility. Negative regression includes missing/duplicate/extra members,
path escapes, missing inputs, symlinked inputs/outputs and corrupted payloads.
Tests extract into an independent directory; reading Web guidance needs no source
checkout, network or MCP. Reading the independent C2C contracts requires that
Skill to be installed separately. Model smoke cases are in [the smoke matrix](tools/smoke-cases.json);
structural assertions do not prove model behavior. A new session using the actually
installed artifact must observe smoke success before calling it daily-ready.
Live MCP/terminal E2E acceptance is a separate result, never implied by packaging.

The [CI workflow](.github/workflows/ci.yml) checks out only Lazier with read-only
permissions and no persisted credentials. It builds,
checks reproducibility and validates downloaded release assets. Only the tag-only
release job can publish ZIP, checksum and provenance. Tags must match
`v<VERSION>` in `tools/package.py`; update that value and the three guidance
headings and README version together. C2C versions and protocol validation are
owned by that separate project, not by Lazier's packaging or CI.

Contributions should stay focused, preserve the Skill contract, and include
checks appropriate to the change.

## License

[MIT](LICENSE). See [research and provenance](RESEARCH.md) for the references
behind the policy. No upstream C2C text or executable code is bundled.
