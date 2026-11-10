# lazier 0.9.0

Portable engineering defaults for coding agents: focused implementation,
proportionate validation, evidence-based review, English documentation and
project-scoped working artifacts.

lazier is one [Agent Skill](https://agentskills.io/specification), with one
[shared policy](skills/lazier/references/policy.md). It uses the current
host's tools and permissions. There is no daemon, custom hook, advisor requirement,
host adapter or integration installer.

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
python3 tools/test_package.py
python3 tools/package.py --build
python3 tools/package.py
git diff --check
```

The ignored `dist/` directory contains `lazier-0.9.0.zip`, its SHA-256 file
and provenance sidecar. Each ZIP contains exactly five files: the entrypoint,
OpenAI UI metadata, shared policy, LICENSE and provenance. All local links resolve
inside the extracted package. Packaging tests check archive identity, permissions,
path containment, symlinks, CRCs, checksums, stale bytes and reproducibility.

The [CI workflow](.github/workflows/ci.yml) uses read-only checkout credentials,
checks the package and publishes only from a version-matching tag. Source and
release assets are available at [lazier-skill](https://github.com/hudrucan/lazier-skill).

## Use one source across agents

Keep the complete skill directory together at a user-controlled location. Register
that directory using each agent's supported discovery mechanism; where directory
links are supported, several agents can use the same source. Do not maintain
independently edited policy copies or leave duplicate skill installations active.

| Host | Documented user discovery location | Invocation |
| --- | --- | --- |
| Codex | `~/.agents/skills/lazier/` | `$lazier` or automatic selection |
| Claude Code | `~/.claude/skills/lazier/` | `/lazier` or automatic selection |
| Other Agent Skills hosts | Use the host's documented discovery location | Use its native invocation |

See the official [Codex skills](https://developers.openai.com/codex/skills) and
[Claude skills](https://code.claude.com/docs/en/skills) documentation. The common
`SKILL.md` and references define behavior. `agents/openai.yaml` supplies optional
OpenAI UI and invocation metadata; it is not a cross-agent configuration file.
Host discovery and behavioral compatibility still need fresh-session verification.

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
and package validation makes no claim of live multi-agent verification.

## License

[MIT](LICENSE). [Research notes](RESEARCH.md) record engineering provenance and
the boundaries of the portability claim.
