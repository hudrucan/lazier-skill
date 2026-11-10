<div align="center">

<h1>lazier</h1>

<p><strong>One engineering policy. Four coding agents.</strong></p>

<p>Focused changes, useful tests, clear documentation.</p>

<p>
  <a href="https://github.com/hudrucan/lazier-skill/actions/workflows/ci.yml"><img src="https://github.com/hudrucan/lazier-skill/actions/workflows/ci.yml/badge.svg" alt="CI status"></a>
  <a href="https://github.com/hudrucan/lazier-skill/releases/latest"><img src="https://img.shields.io/github/v/release/hudrucan/lazier-skill?style=flat-square&amp;color=64748b" alt="Latest release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-64748b?style=flat-square" alt="MIT license"></a>
  <a href="#development"><img src="https://img.shields.io/badge/python-3.9%2B-64748b?style=flat-square" alt="Python 3.9 or newer"></a>
</p>

<p>
  <a href="#quick-start">Quick start</a> ·
  <a href="#supported-agents">Supported agents</a> ·
  <a href="#what-it-changes">What it changes</a> ·
  <a href="#development">Development</a>
</p>

</div>

**lazier** is a portable [Agent Skill](https://agentskills.io/specification) for
coding, technical investigations, planning, reviews and project documentation.
It gives your agents the same engineering defaults while keeping their native
tools, permissions and workflows.

The skill is plain files: one entrypoint, a core policy and two references loaded
only on demand. Agent discovery is handled by a separate installer in this repository.

## Quick start

Requires **Python 3.9+** and its standard library. Choose only the agents you use.

```sh
git clone https://github.com/hudrucan/lazier-skill.git
cd lazier-skill

# Preview the installation without writing files.
python3 tools/install.py --target codex claude agy grok --dry-run

# Install the same skill payload for the selected agents.
python3 tools/install.py --target codex claude agy grok
```

For a single agent, use `--target claude`, for example. Open a fresh agent session
and confirm that `lazier` appears in its skill list or native invocation interface.

> The installer registers files at documented discovery paths. Seeing a skill in
> the filesystem is separate from confirming that an agent loaded it.

## Supported agents

| Agent | Target | Installation path | Use or inspect |
| --- | --- | --- | --- |
| Codex | `codex` | `~/.agents/skills/lazier/` | `$lazier` |
| Claude Code | `claude` | `~/.claude/skills/lazier/` | `/lazier` |
| Antigravity | `agy` | `~/.gemini/config/skills/lazier/` | Native skill selection; `/skills` in the CLI |
| Grok Build | `grok` | `~/.agents/skills/lazier/` | `/lazier` |

**One payload, three destinations.** Codex and Grok share the user-level
`.agents/skills` location through Grok Build's compatibility discovery. Claude
and Antigravity receive byte-identical copies at their native locations. There
are no agent-specific policy variants or model-loaded host adapters.

Discovery references: [Codex](https://developers.openai.com/codex/skills) ·
[Claude Code](https://code.claude.com/docs/en/skills) ·
[Antigravity](https://antigravity.google/docs/skills) ·
[Grok Build](https://docs.x.ai/build/features/skills-plugins-marketplaces).

### Persistent use

Skills can be selected automatically when relevant. To apply lazier consistently
to engineering work, add a short instruction to the agent's user or project
instructions to read the installed `SKILL.md`, using its actual absolute path.
Preserve existing guidance and follow the host's instruction precedence.

This repository's [AGENTS.md](AGENTS.md) shows a project bootstrap. The installer
does not edit global instructions, settings, hooks or permission controls.

**Claude Code** reads `CLAUDE.md`, not `AGENTS.md`. A project that already keeps
its instructions in `AGENTS.md` can add a `CLAUDE.md` containing `@AGENTS.md`, as
this repository does. For a user-wide setting, add one line to
`~/.claude/CLAUDE.md`, for example:

```text
For engineering tasks, read and apply ~/.claude/skills/lazier/SKILL.md once per session.
```

Without this line, Claude Code makes the skill available but decides on its own
whether to load it; `/lazier` always loads it.

## What it changes

| Default | What it means in practice |
| --- | --- |
| **Focused implementation** | Choose the smallest complete solution that satisfies current requirements. |
| **Preserved behavior** | Protect contracts, boundaries and failure handling when simplifying code. |
| **Proportionate validation** | Test observable behavior and reuse checks that remain valid. |
| **Evidence-based review** | Connect findings to locations, impact and a practical fix. |
| **Explicit simplicity review** | Review for unnecessary complexity when asked, without adding a mandatory finishing pass. |
| **Technical continuity** | Carry useful decisions and evidence forward; inspect current source before editing. |
| **Organized documentation** | Write English docs and keep working artifacts together per project. |

The core behavior lives in the [shared policy](skills/lazier/references/policy.md); [artifacts and continuity](skills/lazier/references/artifacts.md) and [tools and integrations](skills/lazier/references/integrations.md) load only when needed.
User instructions, project requirements and host security rules retain precedence.
lazier provides guidance; it does not grant access or enforce correctness.

### Example requests

Use your agent's native skill invocation, then ask for the work:

```text
Fix this parser regression with the smallest complete change.
Run the relevant existing tests and report what you verified.
```

```text
Investigate why this test fails and save a report.
Do not change the implementation yet.
```

```text
Review this diff for unnecessary complexity.
Report supported simplifications; do not edit.
```

Installing or invoking lazier does not request a simplicity review on its own.
Task-specific skills, including TypeSafe/Jev guidance, remain independent.

## Documentation and artifacts

**Docs in English; conversation in your language.** New or substantially revised
documents, artifact filenames and headings use English unless you request another
language. Literal quotations, identifiers and required localized content are preserved.

Maintained project documentation stays at its canonical path. Working investigations,
plans, reviews and reports use one destination, in this order:

1. The location you explicitly request.
2. The project's documented artifact directory.
3. `<project-root>/.agent-artifacts/`.

Private artifacts inside Git must be untracked and ignored before writing. When
needed, use a narrow local rule in the file resolved by
`git rev-parse --git-path info/exclude`. Ignore rules do not untrack existing files.

Reuse the report for the same topic when practical. A short chat answer does not
need an artifact, and the policy does not authorize moving old docs or changing
the Git index to hide them.

## Updates and installation behavior

Update the checkout, preview the selected targets, then install:

```sh
git pull --ff-only
python3 tools/install.py --target codex claude agy grok --dry-run
python3 tools/install.py --target codex claude agy grok
```

The installer checks all selected destinations before making changes. Identical
installations are left untouched; provenance-verified installations without local
edits can be updated. Locally modified, unmanaged or additional files are preserved
by refusing the update rather than overwriting them.

<details>
<summary><strong>Installation details</strong></summary>

- The installer uses directory copies and does not depend on Antigravity symlink discovery.
- Existing linked skill destinations are preserved. Update their canonical location instead.
- `--home <directory>` supports isolated testing and an explicit alternate home.
- Only default user discovery roots are mapped. Custom configuration roots and existing workspace or plugin copies need separate inspection.
- Each directory replacement rolls back if publishing that candidate fails. Several target directories are not one transaction.
- No persistent backup is created. Keep custom policy changes in your source branch rather than editing installed copies.

</details>

## Development

Build and verify locally using only Python's standard library:

```sh
# Runs packaging and installer tests, matching the CI entrypoint.
python3 tools/test_package.py

# Build the skill archive, checksum and provenance.
python3 tools/package.py --build

# Verify the generated assets against source.
python3 tools/package.py
git diff --check
```

Generated files go into ignored `dist/`:

| Asset | Purpose |
| --- | --- |
| `lazier-<version>.zip` | The portable skill package. |
| `lazier-<version>.sha256` | SHA-256 checksum for the archive. |
| `lazier-<version>.provenance.json` | Version and hashes of the packaged source files. |

The ZIP contains seven files: `SKILL.md`, `references/policy.md`,
`references/artifacts.md`, `references/integrations.md`, `agents/openai.yaml`,
`LICENSE` and `provenance.json`. The installer stays in
`tools/`, outside the skill payload. OpenAI UI metadata does not configure other agents.

The [CI workflow](.github/workflows/ci.yml) tests the project, checks reproducible
builds and validates release assets. Version-matching tags publish the ZIP,
checksum and provenance to [GitHub Releases](https://github.com/hudrucan/lazier-skill/releases).

### Verification scope

Automated checks cover package integrity, links, path containment, stale content,
dry-run, idempotence and preservation of existing installations. Installer tests
use temporary homes. The installer has also been exercised against the maintainer's
local installation, including a second run reporting `unchanged`.

Native agent discovery and behavioral verification remain separate. The
[smoke matrix](tools/smoke-cases.json) defines shared scenarios and pass/fail
conditions. [Agent audits](audits/README.md) keep one latest result per agent, with
the tested version in each file; absent results mean unverified. Passing packaging
tests does not establish activation or equivalent behavior across all agents.

## License

[MIT](LICENSE). See [research and provenance](RESEARCH.md) for the sources behind
the engineering policy.
