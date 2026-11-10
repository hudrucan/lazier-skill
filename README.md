# lazier 0.10.0

Portable engineering defaults for coding agents: focused implementation,
proportionate validation, evidence-based review, English documentation and
project-scoped working artifacts.

lazier is one [Agent Skill](https://agentskills.io/specification), with one
[shared policy](skills/lazier/references/policy.md). It uses the current
host's tools and permissions. There is no daemon, custom hook, advisor requirement,
host adapter. Local discovery registration is handled separately by
[the repository installer](tools/install.py); the model does not load installer rules.

## Scope

Use lazier for coding, technical investigations, planning, reviews and project
documentation. Simplicity review runs only when requested; ordinary implementation
does not trigger a mandatory review pass. Questions unrelated to engineering do
not need this skill.

The policy guides judgment; it does not enforce behavior or guarantee correctness.
User instructions, applicable project requirements and platform security retain
precedence. A skill cannot grant filesystem, network or execution access.

## Build and inspect the release

Python 3.9+ and its standard library are sufficient. No Git, network, other skill
or installed agent is needed to build the distribution:

```sh
python3 -m unittest discover -s tools -p 'test_*.py'
python3 tools/package.py --build
python3 tools/package.py
git diff --check
```

The ignored `dist/` directory contains `lazier-0.10.0.zip`, its SHA-256 file
and provenance sidecar. Each ZIP contains exactly five files: the entrypoint,
OpenAI UI metadata, shared policy, LICENSE and provenance. All local links resolve
inside the extracted package. Packaging tests check archive identity, permissions,
path containment, symlinks, CRCs, checksums, stale bytes and reproducibility.

The [CI workflow](.github/workflows/ci.yml) uses read-only checkout credentials,
checks the package and publishes only from a version-matching tag. Source and
release assets are available at [lazier-skill](https://github.com/hudrucan/lazier-skill).
The 0.10.0 release adds local installation tooling outside the skill payload.
Building the package does not install it; the published 0.9.0 assets remain unchanged.

## Use one source across agents

Keep the complete skill directory together at a user-controlled location. Register
that directory using each agent's supported discovery mechanism; where directory
links are supported, several agents can use the same source. Do not maintain
independently edited policy copies or leave duplicate skill installations active.

The installer supports exactly four local targets:

| Target | Installer destination | Invocation / discovery |
| --- | --- | --- |
| `codex` | `~/.agents/skills/lazier/` | `$lazier` or automatic selection |
| `claude` | `~/.claude/skills/lazier/` | `/lazier` or automatic selection |
| `agy` | `~/.gemini/config/skills/lazier/` | Native skill selection; inspect CLI discovery with `/skills` |
| `grok` | `~/.agents/skills/lazier/` through Grok Build compatibility discovery | `/lazier` or automatic selection |

See the official [Codex skills](https://developers.openai.com/codex/skills) and
[Claude skills](https://code.claude.com/docs/en/skills),
[Antigravity skills](https://antigravity.google/docs/skills) and
[Grok Build skills](https://docs.x.ai/build/features/skills-plugins-marketplaces) documentation. The common
`SKILL.md` and references define behavior. `agents/openai.yaml` supplies optional
OpenAI UI and invocation metadata; it is not a cross-agent configuration file.
Host discovery and behavioral compatibility still need fresh-session verification.

Preview registration from this checkout without writing any files:

```sh
python3 tools/install.py --target codex claude agy grok --dry-run
```

When installation is requested, run the same command without `--dry-run`. The
installer validates the source package and exports identical files to each selected
native directory. Codex and Grok share one destination, so they are installed once.
These are managed copies of one payload, not host-specific skills or policies.

The installer preflights all selected destinations before writing. It updates an
unchanged, provenance-verified lazier installation and leaves identical copies
untouched. It refuses locally modified, unmanaged or additional files, linked skill
destinations and parent paths that resolve outside the selected home. Existing links
are preserved: update their canonical installation separately rather than replacing
the link. No persistent backup is created. A per-directory replacement rolls back
if publishing that candidate fails; applying several destinations is not one transaction.

The installer deliberately uses directory copies so it does not depend on AGY symlink
discovery. `--home <directory>` supports isolated fixture testing. Only default user
discovery roots are mapped; custom configuration roots, workspace/plugin skills and
duplicate registrations there need host-specific inspection. The installer does not
edit settings, global instructions, hooks or permissions and does not start agents.

For persistent application, add a short instruction to each host's user or project
instructions: read and apply the installed lazier entrypoint for engineering
tasks. Use its actual absolute path and preserve existing instructions. A skill
description makes lazier discoverable; it does not guarantee activation on every
task. This repository's [AGENTS.md](AGENTS.md) demonstrates a project bootstrap.

## Documentation and artifacts

New or substantially revised documents, artifact filenames and headings are in
English unless the user explicitly chooses another language. Chat can remain in
the user's language. Preserve quotations, identifiers and localized content.

Maintained documentation stays at its canonical repository path. Working plans,
investigations, reviews and reports use one artifact directory per project:

1. Follow an explicit user destination.
2. Otherwise follow the project's documented artifact destination.
3. Otherwise use `<project-root>/.agent-artifacts/`.

Before writing private working artifacts inside Git, verify that the destination
is untracked and ignored. If necessary, preserve existing entries and add a narrow
local rule in `git rev-parse --git-path info/exclude`; a shared `.gitignore` change
is for an intentional team convention. Ignore rules do not untrack files. lazier
does not authorize index changes, migration of old reports or forced staging.

An external destination must be writable under the current host's permissions.
Reuse an existing artifact for the same topic when practical. A short answer does
not need a report file merely because this policy exists.

These preferences live in the lazier source you control, not in context-mode's
package or generated templates. Updating context-mode does not update this policy.
Updating lazier itself replaces its distribution: maintain custom changes in your
own source branch rather than patching the extracted installation. Keep per-project
destination overrides in project or user instructions so skill updates preserve them.

## Independent skills and tools

Use installed task-specific skills when relevant. TypeSafe/Jev integration belongs
to the separately installed `typesafe-ai` skill. lazier carries no API schemas,
probability thresholds or automatic second-opinion workflow.

Context and analysis tools remain independently configured. Use the tools exposed
by the current host and follow its routing rules; do not pin a plugin fork, install
another MCP server or change hooks just to use lazier.

## Migration from 0.9.0

The skill name and common policy remain the same. The 0.10.0 release adds repository
installation tooling outside the five-file skill payload. Preview the selected
targets, then explicitly install when a rollout is requested. Verify actual discovery
in each host; copying files and packaging success do not prove model activation.

## Migration from codex-lazier 0.8.0

This is a breaking skill rename to `lazier`; invocation names and installation
paths change. Keep a verified old package for rollback. When a cutover is authorized:

- Replace the old skill installation with the complete new directory, avoiding
  stale files and duplicate discovery roots.
- Update existing bootstrap paths from `references/codex.md` or `references/web.md`
  to the new `SKILL.md`. Update explicit invocation names as appropriate for the host.
- Remove only obsolete lazier-specific bootstrap text; preserve unrelated settings.
- Start fresh sessions and verify loaded paths, ordinary implementation, explicit
  review and artifact routing before calling the installation ready.

The Codex/Web adapters, C2C workflow and built-in Jev advice are removed. Existing
independent skills and tools are not reconfigured. No compatibility alias is bundled;
silently retaining two separately selectable policies would obscure which one ran.

## Behavioral verification

[Smoke cases](tools/smoke-cases.json) cover ordinary work, implicit activation,
planning, explicit review, continuity, English artifacts, project overrides,
tracked destinations and canonical docs. Run them in disposable fixtures on each
host actually in use. Record package hash, host/model, loaded paths and observed
file and Git changes. The matrix is pending: archive validation is not a model pass,
and package validation makes no claim of live multi-agent verification. Installer
tests use temporary homes and verify native paths, byte-identical payloads, dry-run,
idempotence and preservation of existing content; they do not launch any agent.

## License

[MIT](LICENSE). [Research notes](RESEARCH.md) record engineering provenance and
the boundaries of the portability claim.
