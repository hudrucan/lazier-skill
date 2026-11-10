import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SCRIPT = TOOLS / "make_smoke_fixtures.py"
ENTRY = ".claude/skills/lazier/SKILL.md"
FAILING = [
    "ordinary",
    "english-artifacts",
    "tracked-destination",
    "chat-only",
    "continuation",
    "project-destination",
]
PASSING = ["implicit", "simplicity", "no-specialized-skill", "canonical-docs", "plan"]


def generate(output, host):
    return subprocess.run(
        [
            sys.executable,
            "-I",
            str(SCRIPT),
            str(output),
            "--host",
            host,
            "--skill-entry",
            ENTRY,
        ],
        capture_output=True,
        text=True,
    )


def run(cwd, *command):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", GIT_CONFIG_GLOBAL=os.devnull)
    return subprocess.run(
        list(command), cwd=str(cwd), env=env, capture_output=True, text=True
    )


class SmokeFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name) / "claude"
        result = generate(cls.root, "claude")
        assert result.returncode == 0, result.stderr
        cls.manifest = json.loads(
            (cls.root / "manifest.json").read_text(encoding="utf-8")
        )

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def case(self, case_id):
        entry = self.manifest[case_id]
        return self.root / entry["directory"], self.root / entry["directory"] / entry[
            "cwd"
        ]

    def test_manifest_matches_the_shared_cases(self):
        cases = json.loads((TOOLS / "smoke-cases.json").read_text(encoding="utf-8"))[
            "cases"
        ]
        self.assertEqual(list(self.manifest), [case["id"] for case in cases])
        for case in cases:
            self.assertEqual(self.manifest[case["id"]]["prompt"], case["prompt"])

    def test_every_fixture_is_a_clean_repository(self):
        for case_id in self.manifest:
            with self.subTest(case=case_id):
                root, _ = self.case(case_id)
                self.assertEqual(run(root, "git", "rev-parse", "HEAD").returncode, 0)
                self.assertEqual(run(root, "git", "status", "--porcelain").stdout, "")

    def test_parser_failures_and_passes(self):
        for case_id in FAILING:
            with self.subTest(failing=case_id):
                _, cwd = self.case(case_id)
                self.assertNotEqual(
                    run(cwd, sys.executable, "-m", "unittest").returncode, 0
                )
        for case_id in PASSING:
            with self.subTest(passing=case_id):
                _, cwd = self.case(case_id)
                self.assertEqual(
                    run(cwd, sys.executable, "-m", "unittest").returncode, 0
                )

    def test_instructions_follow_the_host(self):
        root, _ = self.case("implicit")
        self.assertIn(ENTRY, (root / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertEqual(
            (root / "CLAUDE.md").read_text(encoding="utf-8"), "@AGENTS.md\n"
        )
        other = Path(self.temp.name) / "codex"
        self.assertEqual(generate(other, "codex").returncode, 0)
        self.assertFalse((other / "implicit" / "CLAUDE.md").exists())

    def test_destination_fixtures(self):
        root, _ = self.case("tracked-destination")
        self.assertEqual(
            run(
                root, "git", "ls-files", "reports/parser-investigation.md"
            ).stdout.strip(),
            "reports/parser-investigation.md",
        )
        root, _ = self.case("project-destination")
        self.assertTrue((root / ".local" / "reports").is_dir())
        self.assertEqual(
            run(root, "git", "check-ignore", ".local/reports/x.md").returncode, 0
        )
        root, _ = self.case("continuation")
        self.assertTrue(
            (root / ".agent-artifacts" / "parser-investigation.md").is_file()
        )
        self.assertEqual(
            run(root, "git", "check-ignore", ".agent-artifacts/x.md").returncode, 0
        )

    def test_diff_and_docs_fixtures(self):
        root, _ = self.case("simplicity")
        self.assertIn(
            "PairParserFactory", (root / "change.diff").read_text(encoding="utf-8")
        )
        self.assertEqual(
            run(root, "git", "ls-files", "change.diff").stdout.strip(), "change.diff"
        )
        root, _ = self.case("canonical-docs")
        self.assertIn("key=value", (root / "README.md").read_text(encoding="utf-8"))
        self.assertIn("json.dumps", (root / "cli.py").read_text(encoding="utf-8"))
        self.assertIn(
            "Lỗi: thiếu dấu =", (root / "README.md").read_text(encoding="utf-8")
        )

    def test_refuses_a_non_empty_output_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "keep.txt").write_text("x", encoding="utf-8")
            result = generate(Path(directory), "claude")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must be empty", result.stderr)
            self.assertEqual(
                [item.name for item in Path(directory).iterdir()], ["keep.txt"]
            )


if __name__ == "__main__":
    unittest.main()
