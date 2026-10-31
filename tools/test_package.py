"""Focused packaging regression; uses only the Python standard library."""

from pathlib import Path
import re
import json
import hashlib
import os
import runpy
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parent.parent


class PackageValidationTests(unittest.TestCase):
    def test_shared_continuity_and_separate_c2c_integration(self):
        skill = ROOT / "skills/codex-lazier"
        policy = " ".join((skill / "references/policy.md").read_text(encoding="utf-8").split())
        continuity = policy.split("### Technical continuity", 1)[1].split("###", 1)[0]
        for requirement in ["goals", "constraints", "checked evidence", "options/trade-offs",
                            "unresolved questions", "settled Plan decisions", "file/line",
                            "repair direction", "validation", "latest audit or review",
                            "evidence", "impact", "proposed fix", "assumptions and open questions",
                            "current source before editing", "independently of any transport"]:
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, continuity)
        entry = (skill / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("separately installed `codex-with-chatgpt` Skill", entry)
        self.assertIn("auto=true", entry)
        self.assertIn("ordinary engineering and Lazier packaging remain independent", entry)
        description = re.search(r"^description: (.+)$", entry, re.M)[1]
        self.assertNotRegex(description, r"C2C|callback|submit_audit_result")
        for name in ["SKILL.md", "references/codex.md", "references/web.md"]:
            text = " ".join((skill / name).read_text(encoding="utf-8").split())
            with self.subTest(name=name):
                self.assertIn("guidance already read and still valid in this session", text)
                self.assertNotRegex(text, r"references/c2c/|workflow(?:-web|-async)?\.md|C2C_CALLBACK|submit_audit_result")
        for host in ["codex", "web"]:
            self.assertIn("../SKILL.md#c2c-integration",
                          (skill / f"references/{host}.md").read_text(encoding="utf-8"))
        self.assertIn("policy.md#technical-continuity",
                      (skill / "references/web.md").read_text(encoding="utf-8"))

    def test_skill_links_must_resolve_in_the_installed_package(self):
        with TemporaryDirectory(prefix="codex-lazier-links-") as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "skills", root / "skills")
            shutil.copyfile(ROOT / "LICENSE", root / "LICENSE")
            (root / "tools").mkdir()
            shutil.copyfile(ROOT / "tools/package.py", root / "tools/package.py")
            (root / "README.md").write_text("Repository-only documentation.\n", encoding="utf-8")
            manifest = root / "skills/codex-lazier/SKILL.md"
            original = manifest.read_text(encoding="utf-8")
            for target in ["references/missing.md", "../../README.md"]:
                with self.subTest(target=target):
                    manifest.write_text(original + f"\n[Reference]({target})\n", encoding="utf-8")
                    result = subprocess.run(
                        [sys.executable, str(root / "tools/package.py"), "--build"],
                        capture_output=True, text=True,
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("Broken package link", result.stderr)
                    self.assertFalse((root / "dist").exists())

    def test_interface_text_can_change_without_weakening_validation(self):
        with TemporaryDirectory(prefix="codex-lazier-metadata-") as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "skills", root / "skills")
            shutil.copyfile(ROOT / "LICENSE", root / "LICENSE")
            (root / "tools").mkdir()
            shutil.copyfile(ROOT / "tools/package.py", root / "tools/package.py")
            metadata = root / "skills/codex-lazier/agents/openai.yaml"
            original = metadata.read_text(encoding="utf-8")
            changed = re.sub(r'(?m)^  display_name:.*$', '  display_name: "Codex Lazier"', original)
            changed = re.sub(r'(?m)^  short_description:.*$', '  short_description: "Review engineering complexity"', changed)
            changed = re.sub(r'(?m)^  default_prompt:.*$', '  default_prompt: "Review the supplied design."', changed)
            cases = [("changed UI text", changed, True),
                     ("missing interface", "policy:\n  allow_implicit_invocation: false\n", False),
                     ("explicit-only invocation", original.replace("true", "false"), False)]
            for field in ["display_name", "short_description", "default_prompt"]:
                cases.append((f"missing {field}", re.sub(rf"(?m)^  {field}:.*\n", "", original), False))
                cases.append((f"empty {field}", re.sub(rf"(?m)^  {field}:.*$", f'  {field}: " "', original), False))
            cases.append(("invalid quoted string", re.sub(r'(?m)^  display_name:.*$',
                                                          '  display_name: "Codex "Lazier""', original), False))
            for label, content, valid in cases:
                with self.subTest(label=label):
                    metadata.write_text(content, encoding="utf-8")
                    result = subprocess.run(
                        [sys.executable, str(root / "tools/package.py"), "--build"],
                        capture_output=True, text=True,
                    )
                    self.assertEqual(result.returncode == 0, valid, result.stderr)
                    self.assertEqual("PASS:" in result.stdout, valid)
                    if not valid:
                        self.assertIn("FAIL:", result.stderr)

    def test_description_with_unquoted_colon_is_rejected(self):
        with TemporaryDirectory(prefix="codex-lazier-regression-") as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "skills", root / "skills")
            shutil.copyfile(ROOT / "LICENSE", root / "LICENSE")
            (root / "tools").mkdir()
            shutil.copyfile(ROOT / "tools/package.py", root / "tools/package.py")
            manifest = root / "skills/codex-lazier/SKILL.md"
            manifest.write_text(re.sub(
                r"(?m)^description:.*$",
                "description: Review changes: keep them simple.",
                manifest.read_text(encoding="utf-8"),
            ), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(root / "tools/package.py"), "--build"],
                capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("FAIL:", result.stderr)
            self.assertNotIn("PASS:", result.stdout)

    def test_distribution_includes_current_references_and_rejects_stale_bytes(self):
        with TemporaryDirectory(prefix="codex-lazier-archive-") as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "skills", root / "skills")
            shutil.copyfile(ROOT / "LICENSE", root / "LICENSE")
            (root / "tools").mkdir()
            shutil.copyfile(ROOT / "tools/package.py", root / "tools/package.py")

            def run(*args):
                return subprocess.run(
                    [sys.executable, str(root / "tools/package.py"), *args],
                    capture_output=True, text=True,
                )

            version = runpy.run_path(str(root / "tools/package.py"))["VERSION"]
            for tag in ["v0.0.0", version, f"v{version}-rc.1"]:
                with self.subTest(tag=tag):
                    rejected = run("--build", "--tag", tag)
                    self.assertNotEqual(rejected.returncode, 0)
                    self.assertIn("Release tag mismatch", rejected.stderr)
                    self.assertFalse((root / "dist").exists(), "Reject mismatched tags before building")

            built = run("--build", "--tag", f"v{version}")
            self.assertEqual(built.returncode, 0, built.stderr)
            archive = next((root / "dist").glob("*.zip"))
            before = archive.read_bytes()
            with ZipFile(archive) as bundle:
                self.assertCountEqual(bundle.namelist(), [
                    "codex-lazier/SKILL.md", "codex-lazier/agents/openai.yaml",
                    "codex-lazier/references/policy.md", "codex-lazier/references/web.md",
                    "codex-lazier/references/codex.md", "codex-lazier/LICENSE",
                    "codex-lazier/provenance.json",
                ])
                for reference in ["policy.md", "codex.md", "web.md"]:
                    self.assertEqual(bundle.read("codex-lazier/references/" + reference),
                                     (root / "skills/codex-lazier/references" / reference).read_bytes())
                self.assertEqual(bundle.read("codex-lazier/LICENSE"), (root / "LICENSE").read_bytes())
                installed = root / "installed"
                bundle.extractall(installed)
            skill = (installed / "codex-lazier").resolve()
            self.assertEqual(list(skill.rglob("SKILL.md")), [skill / "SKILL.md"])
            links = re.findall(r"\[[^\]]*\]\(([^)]+)\)",
                               (skill / "SKILL.md").read_text(encoding="utf-8"))
            for reference in ["policy", "codex", "web"]:
                self.assertIn(f"references/{reference}.md", links)
            for source in skill.rglob("*.md"):
                for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", source.read_text(encoding="utf-8")):
                    if "://" not in target and not target.startswith("#"):
                        resolved = (source.parent / target.split("#", 1)[0]).resolve()
                        self.assertTrue(resolved.is_relative_to(skill))
                        self.assertTrue(resolved.is_file(), target)
            self.assertEqual(run("--build").returncode, 0)
            self.assertEqual(archive.read_bytes(), before, "Build must be reproducible")

            for name in ["policy", "codex", "web"]:
                with self.subTest(stale_reference=name):
                    reference = root / f"skills/codex-lazier/references/{name}.md"
                    reference.write_text(reference.read_text(encoding="utf-8") + "\nNew default.\n", encoding="utf-8")
                    stale = run()
                    self.assertNotEqual(stale.returncode, 0)
                    self.assertIn("Stale archive content", stale.stderr)
                    self.assertNotIn("PASS:", stale.stdout)
                    self.assertEqual(run("--build").returncode, 0)
            archive.with_suffix(".sha256").write_text("wrong\n", encoding="utf-8")
            corrupt = run()
            self.assertNotEqual(corrupt.returncode, 0)
            self.assertIn("checksum mismatch", corrupt.stderr)


class ArtifactIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(prefix="lazier-artifact-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "lazier"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns("dist", ".git", "__pycache__"))

    def run_package(self, *args):
        return subprocess.run([sys.executable, str(self.root / "tools/package.py"),
                               *args], capture_output=True, text=True)

    def test_nested_skill_entrypoints_are_rejected(self):
        module = runpy.run_path(str(self.root / "tools/package.py"))
        files = module["source_files"]()
        for name in ["SKILL.md", "skill.md"]:
            with self.subTest(name=name):
                nested = {**files, f"codex-lazier/references/nested/{name}": b"---\nname: duplicate\n---\n"}
                with self.assertRaisesRegex(ValueError, "only the Lazier skill entrypoint"):
                    module["validate_sources"](nested)

    def rejected(self, message):
        result = self.run_package("--build")
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(message.lower(), result.stderr.lower())
        self.assertFalse((self.root / "dist").exists())

    def test_missing_guidance_links_anchors_and_symlinks(self):
        target = self.root / "skills/codex-lazier/SKILL.md"
        original = target.read_bytes()
        for link in ["references/missing.md", "../../README.md", "references/codex.md#missing",
                     "/etc/passwd", "%2e%2e/%2e%2e/README.md", "../codex-with-chatgpt/SKILL.md",
                     "C:/Windows/win.ini", "references\\\\policy.md"]:
            with self.subTest(link=link):
                target.write_bytes(original + f"\n[Required]({link})\n".encode())
                self.rejected("Broken package")
        target.unlink()
        self.rejected("Missing input")
        target.symlink_to(ROOT / "skills/codex-lazier/SKILL.md")
        self.rejected("input")
        target.unlink()
        target.write_bytes(original)
        refs = self.root / "skills/codex-lazier/references"
        moved = refs.with_name("refs-original")
        refs.rename(moved)
        refs.symlink_to(moved, target_is_directory=True)
        self.rejected("Symlinked input")
        refs.unlink()
        moved.rename(refs)
        module = runpy.run_path(str(self.root / "tools/package.py"))
        for relative in ["../LICENSE", str((ROOT / "LICENSE").resolve())]:
            with self.subTest(relative=relative):
                with self.assertRaisesRegex(ValueError, "Input path escape"):
                    module["read_input"](self.root, relative)

    def test_metadata_version_and_license_cannot_disagree(self):
        entry = self.root / "skills/codex-lazier/SKILL.md"
        original = entry.read_text()
        entry.write_text(original.replace("license: MIT", "license: Apache"))
        self.rejected("License must match")
        entry.write_text(original)
        policy = self.root / "skills/codex-lazier/references/policy.md"
        version = runpy.run_path(str(self.root / "tools/package.py"))["VERSION"]
        policy.write_text(policy.read_text().replace(f"v{version}", "v0.0.0", 1))
        self.rejected("Version heading mismatch")

    def test_output_symlinks_cannot_redirect_build_or_check(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        dist = self.root / "dist"
        dist.symlink_to(outside, target_is_directory=True)
        result = self.run_package("--build")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("escaping output", result.stderr)
        self.assertEqual(list(outside.iterdir()), [])
        dist.unlink()
        self.assertEqual(self.run_package("--build").returncode, 0)
        for output in list(dist.iterdir()):
            with self.subTest(output=output.name):
                real = outside / output.name
                before = output.read_bytes()
                output.rename(real)
                output.symlink_to(real)
                for arguments in [(), ("--build",)]:
                    result = self.run_package(*arguments)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("escaping output", result.stderr)
                self.assertEqual(real.read_bytes(), before)
                output.unlink()
                real.rename(output)

    def test_changed_guidance_is_stale_even_with_valid_zip_crcs(self):
        self.assertEqual(self.run_package("--build").returncode, 0)
        archive = next((self.root / "dist").glob("*.zip"))
        with ZipFile(archive) as bundle:
            original = [(info, bundle.read(info.filename)) for info in bundle.infolist()]
        with ZipFile(archive, "w") as bundle:
            for info, content in original:
                if info.filename == "codex-lazier/references/policy.md":
                    content += b"\nChanged rule.\n"
                bundle.writestr(info, content)
        with ZipFile(archive) as bundle:
            self.assertIsNone(bundle.testzip())
        result = self.run_package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Stale archive content: codex-lazier/references/policy.md", result.stderr)

    def test_detached_artifact_closure_identity_license_crc_and_staleness(self):
        result = self.run_package("--build")
        self.assertEqual(result.returncode, 0, result.stderr)
        archive = next((self.root / "dist").glob("*.zip"))
        before = archive.read_bytes()
        module = runpy.run_path(str(self.root / "tools/package.py"))
        with TemporaryDirectory(prefix="web-offline-") as directory:
            with ZipFile(archive) as bundle:
                bundle.extractall(directory)
            installed = Path(directory)
            files = {p.relative_to(installed).as_posix(): p.read_bytes()
                     for p in installed.rglob("*") if p.is_file()}
            # Deliberately remove access to the copied source before validating the extraction.
            fixture_skills = (self.root / "skills").resolve()
            self.assertTrue(fixture_skills.is_relative_to(Path(self.temp.name).resolve()))
            shutil.rmtree(fixture_skills)
            module["validate_links"](files)
            provenance = json.loads(files["codex-lazier/provenance.json"])
            self.assertEqual(provenance["version"], module["VERSION"])
            self.assertEqual(set(provenance), {"name", "version", "sha256"})
            self.assertEqual(provenance["name"], "codex-lazier")
            self.assertEqual(set(provenance["sha256"]), set(files) - {"codex-lazier/provenance.json"})
            for name, digest in provenance["sha256"].items():
                self.assertEqual(hashlib.sha256(files[name]).hexdigest(), digest)
            self.assertEqual(archive.with_suffix(".provenance.json").read_bytes(),
                             files["codex-lazier/provenance.json"])
        shutil.copytree(ROOT / "skills", self.root / "skills")
        self.assertEqual(self.run_package("--build").returncode, 0)
        self.assertEqual(archive.read_bytes(), before)
        archive.with_suffix(".provenance.json").write_text("{}")
        self.assertIn("Stale archive provenance", self.run_package().stderr)
        self.assertEqual(self.run_package("--build").returncode, 0)
        with ZipFile(archive) as bundle:
            info = bundle.infolist()[0]
            offset = info.header_offset + 30 + len(info.filename.encode()) + len(info.extra)
        corrupt = bytearray(archive.read_bytes())
        corrupt[offset + info.compress_size // 2] ^= 1
        archive.write_bytes(corrupt)
        self.assertNotEqual(self.run_package().returncode, 0, "Corrupted payload must fail")

    def test_archive_rejects_extra_duplicate_missing_and_nonregular_members(self):
        self.assertEqual(self.run_package("--build").returncode, 0)
        archive = next((self.root / "dist").glob("*.zip"))
        before = archive.read_bytes()
        for mutation in ["extra", "duplicate", "missing", "symlink"]:
            with self.subTest(mutation=mutation):
                with ZipFile(archive) as bundle:
                    original = [(info, bundle.read(info.filename)) for info in bundle.infolist()]
                with ZipFile(archive, "w") as bundle:
                    for index, (info, content) in enumerate(original):
                        if mutation == "missing" and index == 0:
                            continue
                        if mutation == "symlink" and index == 0:
                            info.external_attr = 0o120777 << 16
                        bundle.writestr(info, content)
                    if mutation == "extra":
                        bundle.writestr("codex-lazier/references/c2c/entrypoint.md", b"Stale receiver")
                    if mutation == "duplicate":
                        with self.assertWarns(UserWarning):
                            bundle.writestr(original[-1][0], original[-1][1])
                result = self.run_package()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Unexpected file type" if mutation == "symlink" else "Archive entries differ", result.stderr)
                archive.write_bytes(before)

    def test_offline_build_without_checkout_git_or_network(self):
        with TemporaryDirectory(prefix="lazier-offline-") as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "skills", root / "skills")
            shutil.copyfile(ROOT / "LICENSE", root / "LICENSE")
            (root / "tools").mkdir()
            shutil.copyfile(ROOT / "tools/package.py", root / "tools/package.py")
            guard = root / "offline.py"
            guard.write_text(
                "import runpy, sys\n"
                "def deny(event, args):\n"
                "    if event in {'subprocess.Popen', 'os.system'} or event.startswith('socket.'):\n"
                "        raise RuntimeError('Offline packaging attempted external I/O: ' + event)\n"
                "sys.addaudithook(deny)\n"
                "sys.argv = [sys.argv[1], *sys.argv[2:]]\n"
                "runpy.run_path(sys.argv[0], run_name='__main__')\n", encoding="utf-8")
            env = {**os.environ, "PATH": "", "HTTP_PROXY": "http://127.0.0.1:1", "HTTPS_PROXY": "http://127.0.0.1:1"}
            for arguments in [("--build",), ()]:
                result = subprocess.run([sys.executable, str(guard), str(root / "tools/package.py"), *arguments],
                                        env=env, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((root / ".git").exists())
            self.assertFalse((root / "tools/c2c-source.json").exists())
            with ZipFile(next((root / "dist").glob("*.zip"))) as bundle:
                self.assertEqual(len(bundle.namelist()), 7)
                self.assertFalse(any("references/c2c/" in name for name in bundle.namelist()))

    def test_ci_is_standalone_and_smoke_matrix_is_not_a_model_pass(self):
        ci = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertNotIn("c2c-source", ci)
        self.assertNotIn("repository: hudrucan/codex-with-chatgpt", ci)
        self.assertIn('python3 tools/package.py --tag "$GITHUB_REF_NAME"', ci)
        self.assertIn("*.provenance.json", ci)
        matrix = json.loads((ROOT / "tools/smoke-cases.json").read_text(encoding="utf-8"))
        self.assertEqual(matrix["status"], "pending")
        cases = {case["id"]: case for case in matrix["cases"]}
        self.assertEqual(len(cases), len(matrix["cases"]))
        self.assertTrue({"ordinary", "implicit", "simplicity", "plan", "manual", "auto", "auto-sender",
                         "missing-c2c", "source-marker", "source-ticket", "auto-fallback"} <= set(cases))
        self.assertTrue(all(case["prompt"] and case["observe"] for case in cases.values()))


if __name__ == "__main__":
    unittest.main()
