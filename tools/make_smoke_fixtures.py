#!/usr/bin/env python3
"""Create disposable Git fixtures for tools/smoke-cases.json; no network access."""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

CASES = Path(__file__).resolve().parent / "smoke-cases.json"
HOSTS = ("claude", "codex", "agy", "grok")

KVPARSE = '''def parse_pairs(line):
    """Parse 'a=1, b=2' into {'a': '1', 'b': '2'}; whitespace is trimmed."""
    result = {}
    for item in line.split(","):
        key, value = item.split("=", 1)
        result[key.strip()] = value.strip()
    return result
'''
KVPARSE_BUG = KVPARSE.replace("value.strip()", "value")
KVPARSE_TEST = """import unittest

from kvparse import parse_pairs


class ParsePairsTests(unittest.TestCase):
    def test_trims_whitespace(self):
        self.assertEqual(parse_pairs("a=1, b = 2"), {"a": "1", "b": "2"})

    def test_single_pair(self):
        self.assertEqual(parse_pairs("k=v"), {"k": "v"})


if __name__ == "__main__":
    unittest.main()
"""
README = """# kvparse

A tiny key=value parser. `parse_pairs("a=1, b=2")` returns a dict; whitespace
around keys and values is trimmed.

Run the tests with `python3 -m unittest`.
"""
GITIGNORE = "__pycache__/\n*.pyc\n"

FACTORY = '''class PairParser:
    def parse(self, line):
        return {key: value for key, value in self._pairs(line)}

    def _pairs(self, line):
        for item in line.split(","):
            key, value = item.split("=", 1)
            yield self._trim(key), self._trim(value)

    @staticmethod
    def _trim(text):
        return text.strip()


class PairParserFactory:
    def create(self):
        return PairParser()


def parse_pairs(line):
    """Parse 'a=1, b=2' into {'a': '1', 'b': '2'}; whitespace is trimmed."""
    return PairParserFactory().create().parse(line)
'''

STORAGE = """import json
from pathlib import Path


def load(path):
    file = Path(path)
    return json.loads(file.read_text()) if file.exists() else {}


def save(path, records):
    Path(path).write_text(json.dumps(records))
"""
STORAGE_TEST = """import tempfile
import unittest
from pathlib import Path

import storage


class StorageTests(unittest.TestCase):
    def test_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "db.json"
            storage.save(path, {"a": 1})
            self.assertEqual(storage.load(path), {"a": 1})


if __name__ == "__main__":
    unittest.main()
"""
NOTES = """# Storage notes

`storage.py` keeps all records in one JSON file. A CLI and a nightly cron job both
read and write it, and the file is expected to reach about 10,000 records.

We are considering moving to SQLite. Constraints: no new runtime dependencies,
existing JSON files must keep working, and the cron job must never see a half
written file.
"""

CLI = """import json
import sys

from kvparse import parse_pairs


def main(argv):
    if len(argv) != 2:
        print("usage: kvparse 'a=1, b=2'", file=sys.stderr)
        return 2
    try:
        pairs = parse_pairs(argv[1])
    except ValueError:
        print("Lỗi: thiếu dấu =", file=sys.stderr)
        return 2
    print(json.dumps(pairs, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
"""
CLI_OLD = CLI.replace(
    "print(json.dumps(pairs, sort_keys=True))",
    'for key, value in sorted(pairs.items()):\n        print(f"{key}={value}")',
)
CLI_README = """# kvparse

A tiny key=value parser with a command line.

`python3 cli.py 'a=1, b=2'` prints one `key=value` line per pair, sorted by key.
When a pair has no `=` it prints `Lỗi: thiếu dấu =` to stderr and exits with 2.
"""

REPORT = """# Parser investigation

## Checked evidence
- `python3 -m unittest` fails in `test_trims_whitespace`: the value ` 2` keeps its
  leading space.
- `parse_pairs` strips keys but not values (`kvparse.py`).

## Agreed repair
Strip the value as well, then rerun the existing tests.

## Validation
Not run yet.
"""
OLD_REPORT = "# Parser investigation\n\nEarlier notes: the parser trims keys only.\n"


def git(cwd, *args):
    env = dict(
        os.environ,
        GIT_CONFIG_GLOBAL=os.devnull,
        GIT_CONFIG_SYSTEM=os.devnull,
        GIT_AUTHOR_NAME="fixture",
        GIT_AUTHOR_EMAIL="fixture@example.invalid",
        GIT_COMMITTER_NAME="fixture",
        GIT_COMMITTER_EMAIL="fixture@example.invalid",
        GIT_AUTHOR_DATE="2026-01-01T00:00:00Z",
        GIT_COMMITTER_DATE="2026-01-01T00:00:00Z",
    )
    done = subprocess.run(
        ["git", *args], cwd=str(cwd), env=env, capture_output=True, text=True
    )
    if done.returncode:
        raise RuntimeError(
            f"git {' '.join(args)} failed in {cwd}: {done.stderr.strip()}"
        )
    return done.stdout


def write(root, files):
    for name, content in files.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


def commit(root, message):
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", message)


def instructions(entry, host, extra=""):
    text = (
        f"For engineering tasks in this repository, read and apply the lazier "
        f"entrypoint at {entry} once per session.\n{extra}"
    )
    files = {"AGENTS.md": text}
    if host == "claude":
        files["CLAUDE.md"] = "@AGENTS.md\n"
    return files


def new_repo(root, files, message="Initial fixture"):
    root.mkdir(parents=True)
    git(root, "init", "-q", "-b", "main")
    write(root, files)
    commit(root, message)


def exclude(root, line):
    path = Path(git(root, "rev-parse", "--git-path", "info/exclude").strip())
    path = path if path.is_absolute() else root / path
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def base(entry, host, extra="", parser=KVPARSE_BUG, readme=README):
    files = {
        "kvparse.py": parser,
        "test_kvparse.py": KVPARSE_TEST,
        "README.md": readme,
        ".gitignore": GITIGNORE,
    }
    files.update(instructions(entry, host, extra))
    return files


def build_ordinary(root, entry, host):
    new_repo(root, base(entry, host))


def build_implicit(root, entry, host):
    new_repo(
        root,
        base(
            entry,
            host,
            parser=KVPARSE,
            readme=README.replace("whitespace", "whitespaec"),
        ),
    )


def build_diff(root, entry, host):
    new_repo(root, base(entry, host, parser=KVPARSE))
    write(root, {"kvparse.py": FACTORY})
    commit(root, "Add parser factory")
    write(root, {"change.diff": git(root, "diff", "HEAD~1", "HEAD")})
    commit(root, "Add change.diff")


def build_plan(root, entry, host):
    files = {
        "storage.py": STORAGE,
        "test_storage.py": STORAGE_TEST,
        "NOTES.md": NOTES,
        ".gitignore": GITIGNORE,
    }
    files.update(instructions(entry, host))
    new_repo(root, files)


def build_tracked(root, entry, host):
    files = base(entry, host, "Save investigation reports under reports/.\n")
    files["reports/parser-investigation.md"] = OLD_REPORT
    new_repo(root, files)


def build_project(root, entry, host):
    extra = "Save investigation reports under .local/reports at the repository root.\n"
    files = {
        "packages/kvparse/kvparse.py": KVPARSE_BUG,
        "packages/kvparse/test_kvparse.py": KVPARSE_TEST,
        "packages/kvparse/README.md": README,
        ".gitignore": GITIGNORE + ".venv/\n*.log\n.local/\n",
    }
    files.update(instructions(entry, host, extra))
    new_repo(root, files)
    (root / ".local" / "reports").mkdir(parents=True)


def build_docs(root, entry, host):
    files = base(entry, host, parser=KVPARSE, readme=CLI_README)
    files["cli.py"] = CLI_OLD
    new_repo(root, files)
    write(root, {"cli.py": CLI})
    commit(root, "Print JSON instead of key=value lines")


def build_continuation(root, entry, host):
    new_repo(root, base(entry, host))
    exclude(root, ".agent-artifacts/")
    write(root, {".agent-artifacts/parser-investigation.md": REPORT})


BUILDERS = {
    "ordinary": (build_ordinary, "."),
    "implicit": (build_implicit, "."),
    "simplicity": (build_diff, "."),
    "plan": (build_plan, "."),
    "english-artifacts": (build_ordinary, "."),
    "project-destination": (build_project, "packages/kvparse"),
    "tracked-destination": (build_tracked, "."),
    "canonical-docs": (build_docs, "."),
    "continuation": (build_continuation, "."),
    "no-specialized-skill": (build_diff, "."),
    "chat-only": (build_ordinary, "."),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "output", type=Path, help="Empty or missing directory for the fixtures"
    )
    parser.add_argument(
        "--host",
        choices=HOSTS,
        required=True,
        help="claude also gets a CLAUDE.md that imports AGENTS.md",
    )
    parser.add_argument(
        "--skill-entry",
        required=True,
        help="Path of the installed lazier SKILL.md named in the project instructions",
    )
    args = parser.parse_args()
    if args.output.exists() and any(args.output.iterdir()):
        sys.exit("FAIL: output directory must be empty")
    cases = json.loads(CASES.read_text(encoding="utf-8"))["cases"]
    missing = {case["id"] for case in cases} - set(BUILDERS)
    if missing:
        sys.exit(f"FAIL: no fixture builder for {sorted(missing)}")
    args.output.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for case in cases:
        build, cwd = BUILDERS[case["id"]]
        build(args.output.resolve() / case["id"], args.skill_entry, args.host)
        manifest[case["id"]] = {
            "directory": case["id"],
            "cwd": cwd,
            "prompt": case["prompt"],
        }
    (args.output / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Created {len(manifest)} fixtures in {args.output}")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError) as error:
        sys.exit(f"FAIL: {error}")
