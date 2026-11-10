"""Exercise native discovery installation using temporary homes only."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

import install


ROOT = Path(__file__).resolve().parent.parent


class LocalInstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(prefix="lazier-install-test-")
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / "home"

    def run_install(self, *arguments):
        return subprocess.run([sys.executable, str(ROOT / "tools/install.py"),
                               "--home", str(self.home), *arguments],
                              capture_output=True, text=True)

    def test_all_targets_receive_the_same_complete_payload(self):
        result = self.run_install("--target", "codex", "claude", "agy", "grok")
        self.assertEqual(result.returncode, 0, result.stderr)
        expected = install.payload()
        destinations = [self.home / path / "lazier" for path in set(install.TARGETS.values())]
        self.assertEqual(len(destinations), 3)
        for destination in destinations:
            actual = {p.relative_to(destination): p.read_bytes()
                      for p in destination.rglob("*") if p.is_file()}
            self.assertEqual(actual, expected)
        self.assertFalse((self.home / ".grok").exists())
        self.assertFalse(any(self.home.rglob("AGENTS.md")))
        self.assertFalse(any(self.home.rglob("settings.json")))

    def test_dry_run_creates_no_home_or_skill_files(self):
        result = self.run_install("--target", "codex", "claude", "agy", "grok", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PLAN:", result.stdout)
        self.assertFalse(self.home.exists())

    def test_reinstall_is_idempotent(self):
        self.assertEqual(self.run_install("--target", "claude").returncode, 0)
        policy = self.home / ".claude/skills/lazier/references/policy.md"
        timestamp = policy.stat().st_mtime_ns
        result = self.run_install("--target", "claude")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("unchanged", result.stdout)
        self.assertEqual(policy.stat().st_mtime_ns, timestamp)

    def test_owned_old_installation_can_update(self):
        self.assertEqual(self.run_install("--target", "codex").returncode, 0)
        destination = self.home / ".agents/skills/lazier"
        policy = destination / "references/policy.md"
        policy.write_bytes(policy.read_bytes() + b"\nPrevious release guidance.\n")
        proof_path = destination / "provenance.json"
        proof = json.loads(proof_path.read_text(encoding="utf-8"))
        proof["version"] = "0.9.0"
        proof["sha256"]["lazier/references/policy.md"] = hashlib.sha256(policy.read_bytes()).hexdigest()
        proof_path.write_text(json.dumps(proof), encoding="utf-8")
        result = self.run_install("--target", "codex")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("update", result.stdout)
        self.assertEqual(policy.read_bytes(), install.payload()[Path("references/policy.md")])

    def test_modified_installation_blocks_the_whole_plan(self):
        self.assertEqual(self.run_install("--target", "codex").returncode, 0)
        policy = self.home / ".agents/skills/lazier/references/policy.md"
        policy.write_bytes(policy.read_bytes() + b"\nUser edit.\n")
        before = policy.read_bytes()
        result = self.run_install("--target", "claude", "codex")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(policy.read_bytes(), before)
        self.assertFalse((self.home / ".claude").exists())

    def test_unmanaged_content_and_extra_files_are_preserved(self):
        destination = self.home / ".claude/skills/lazier"
        destination.mkdir(parents=True)
        note = destination / "notes.md"
        note.write_text("Keep this file.", encoding="utf-8")
        self.assertNotEqual(self.run_install("--target", "claude").returncode, 0)
        self.assertEqual(note.read_text(encoding="utf-8"), "Keep this file.")
        note.unlink()
        destination.rmdir()
        self.assertEqual(self.run_install("--target", "claude").returncode, 0)
        note.write_text("Keep this file.", encoding="utf-8")
        self.assertNotEqual(self.run_install("--target", "claude").returncode, 0)
        self.assertTrue(note.exists())

    def test_linked_destination_and_escaping_parent_are_preserved(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        parent = self.home / ".claude/skills"
        parent.mkdir(parents=True)
        destination = parent / "lazier"
        destination.symlink_to(outside, target_is_directory=True)
        self.assertNotEqual(self.run_install("--target", "claude").returncode, 0)
        self.assertTrue(destination.is_symlink())
        self.assertEqual(list(outside.iterdir()), [])
        destination.unlink()
        parent.rmdir()
        (self.home / ".claude").rmdir()
        (self.home / ".claude").symlink_to(outside, target_is_directory=True)
        self.assertNotEqual(self.run_install("--target", "claude").returncode, 0)
        self.assertEqual(list(outside.iterdir()), [])

    def test_unknown_target_is_rejected_without_writes(self):
        result = self.run_install("--target", "other")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.home.exists())


if __name__ == "__main__":
    unittest.main()
