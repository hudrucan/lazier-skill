"""Focused packaging regression; uses only the Python standard library."""

from pathlib import Path
import re
import json
import hashlib
import runpy
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parent.parent
C2C_SOURCE = None


class PackageValidationTests(unittest.TestCase):
    def test_web_prompts_preserve_relevant_context_and_async_routing(self):
        web = (ROOT / "skills/codex-lazier/references/web.md").read_text(encoding="utf-8")
        continuity = web.split("For `[C2C Plan]`, `[C2C Task]` and `[C2C Fix]`", 1)[1]
        continuity = " ".join(continuity.split())
        for intent, required in {
            "Plan": ["goals", "constraints", "checked evidence", "options/trade-offs",
                     "unresolved questions"],
            "Task": ["settled Plan decisions (if any)", "verified findings", "file/line",
                     "repair direction", "validation", "does not require a prior Plan"],
            "Fix": ["latest audit", "file/line", "evidence", "impact", "proposed fix"],
        }.items():
            section = continuity.split(f"**{intent}:**", 1)[1].split(" - **", 1)[0]
            for requirement in required:
                with self.subTest(intent=intent, requirement=requirement):
                    self.assertIn(requirement, section)
        for requirement in [
            "only relevant, still-valid context",
            "separating verified findings, assumptions and open questions",
            "Do not require Codex to re-audit everything Web checked",
            "inspection of current source before editing",
            "Preserve C2C routing and an already-selected `auto=true`",
            "Keep settled decisions/advice unless new evidence invalidates them",
        ]:
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, continuity)

    def test_guidance_reuses_valid_reads_and_routes_transport_to_c2c(self):
        skill = ROOT / "skills/codex-lazier"
        for name in ["SKILL.md", "references/codex.md", "references/web.md"]:
            with self.subTest(name=name):
                content = " ".join((skill / name).read_text(encoding="utf-8").split())
                self.assertIn("guidance already read and still valid in this session", content)
        web = (skill / "references/web.md").read_text(encoding="utf-8")
        for reference in ["workflow.md", "workflow-web.md"]:
            self.assertIn("c2c/references/" + reference, web)
        self.assertIn("automatic `[C2C Handoff]` audits", web)
        for transport_detail in ["C2C_CALLBACK", "capability", "timeoutMs", "callback register"]:
            self.assertNotIn(transport_detail, web)
        codex = " ".join((skill / "references/codex.md").read_text(encoding="utf-8").split())
        self.assertIn("only the active host/mode reference", codex)

    def test_automatic_opt_in_and_manual_fallback_smoke_contract(self):
        skill = ROOT / "skills/codex-lazier"
        for relative in ["SKILL.md", "references/codex.md", "references/web.md"]:
            text = (skill / relative).read_text(encoding="utf-8")
            self.assertIn("auto=true", text)
            self.assertNotRegex(text, r"async=(?:true|false)|permission probe|preflight evidence")
        for host in ["codex", "web"]:
            text = (skill / f"references/{host}.md").read_text(encoding="utf-8")
            self.assertIn("manual fallback", text)
            self.assertIn("C2C's bounded recovery", text)
            self.assertIn("Never resend", text)
            self.assertNotRegex(text, r"without retrying|do not retry or")
            self.assertIn("invent", text)
        matrix = json.loads((ROOT / "tools/smoke-cases.json").read_text())
        cases = {case["id"]: case for case in matrix["cases"]}
        self.assertNotIn("auto=", cases["plan"]["prompt"])
        self.assertIn("auto=false", cases["manual"]["prompt"])
        for case_id in ["auto", "auto-register-failure", "auto-uncertain-send", "auto-callback-failure"]:
            self.assertIn("auto=true", cases[case_id]["prompt"])
        for case_id in ["auto-initial-stale", "auto-verification-read",
                        "auto-mcp-read", "auto-callback-retry"]:
            self.assertIn("auto=true", cases[case_id]["prompt"])
            self.assertIn("deadline", " ".join(cases[case_id]["observe"]).lower())
        for case_id, delivery in [("auto-register-failure", "not_sent"),
                                  ("auto-uncertain-send", "uncertain"),
                                  ("auto-callback-failure", "sent")]:
            observations = " ".join(cases[case_id]["observe"])
            self.assertIn(delivery, observations)
            self.assertIn("outside", observations)
            self.assertIn("handoff", observations.lower())

    def test_skill_links_must_resolve_in_the_installed_package(self):
        with TemporaryDirectory(prefix="codex-lazier-links-") as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "skills", root / "skills")
            shutil.copyfile(ROOT / "LICENSE", root / "LICENSE")
            (root / "tools").mkdir()
            shutil.copyfile(ROOT / "tools/package.py", root / "tools/package.py")
            shutil.copyfile(ROOT / "tools/c2c-source.json", root / "tools/c2c-source.json")
            (root / "README.md").write_text("Repository-only documentation.\n", encoding="utf-8")
            manifest = root / "skills/codex-lazier/SKILL.md"
            original = manifest.read_text(encoding="utf-8")
            for target in ["references/missing.md", "../../README.md"]:
                with self.subTest(target=target):
                    manifest.write_text(original + f"\n[Reference]({target})\n", encoding="utf-8")
                    result = subprocess.run(
                        [sys.executable, str(root / "tools/package.py"), "--c2c-source", str(C2C_SOURCE), "--build"],
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
            shutil.copyfile(ROOT / "tools/c2c-source.json", root / "tools/c2c-source.json")
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
                        [sys.executable, str(root / "tools/package.py"), "--c2c-source", str(C2C_SOURCE), "--build"],
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
            shutil.copyfile(ROOT / "tools/c2c-source.json", root / "tools/c2c-source.json")
            manifest = root / "skills/codex-lazier/SKILL.md"
            manifest.write_text(re.sub(
                r"(?m)^description:.*$",
                "description: Review changes: keep them simple.",
                manifest.read_text(encoding="utf-8"),
            ), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(root / "tools/package.py"), "--c2c-source", str(C2C_SOURCE), "--build"],
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
            shutil.copyfile(ROOT / "tools/c2c-source.json", root / "tools/c2c-source.json")

            def run(*args):
                return subprocess.run(
                    [sys.executable, str(root / "tools/package.py"), "--c2c-source", str(C2C_SOURCE), *args],
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
                    "codex-lazier/provenance.json", "codex-lazier/references/c2c/LICENSE",
                    "codex-lazier/references/c2c/entrypoint.md",
                    "codex-lazier/references/c2c/references/workflow.md",
                    "codex-lazier/references/c2c/references/workflow-web.md",
                    "codex-lazier/references/c2c/references/workflow-async.md",
                    "codex-lazier/references/c2c/references/operations.md",
                    "codex-lazier/references/c2c/references/setup.md",
                    "codex-lazier/references/c2c/references/projects.md",
                    "codex-lazier/references/c2c/references/deprovision.md",
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

            for name in ["codex", "web"]:
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


class PinnedContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(prefix="lazier-pin-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "lazier"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns("dist", ".git", "__pycache__"))
        self.source = C2C_SOURCE

    def run_package(self, *args):
        return subprocess.run([sys.executable, str(self.root / "tools/package.py"),
                               "--c2c-source", str(self.source), *args], capture_output=True, text=True)

    def test_nested_skill_entrypoints_are_rejected(self):
        module = runpy.run_path(str(self.root / "tools/package.py"))
        files = module["source_files"](self.source)
        for name in ["SKILL.md", "skill.md"]:
            with self.subTest(name=name):
                nested = {**files, f"codex-lazier/references/c2c/{name}": b"---\nname: duplicate\n---\n"}
                with self.assertRaisesRegex(ValueError, "only the Lazier skill entrypoint"):
                    module["validate_sources"](nested)

    def rejected(self, message):
        result = self.run_package("--build")
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(message.lower(), result.stderr.lower())
        self.assertFalse((self.root / "dist").exists())

    def test_pin_hash_allowlist_and_repository_are_fail_closed(self):
        manifest = self.root / "tools/c2c-source.json"
        original = json.loads(manifest.read_text())
        for field, value, message in [
            ("revision", "main", "Invalid pinned"),
            ("revision", "0" * 40, "HEAD differs"),
            ("repository", "https://github.com/another/repo", "Invalid pinned"),
            ("files", {"../../secret": "0" * 64}, "Invalid pinned"),
            ("files", {**original["files"], "LICENSE": "0" * 64}, "hash mismatch"),
        ]:
            with self.subTest(field=field, value=value):
                manifest.write_text(json.dumps({**original, field: value}))
                self.rejected(message)

    def test_missing_changed_and_symlinked_source(self):
        source = Path(self.temp.name) / "source"
        subprocess.run(["git", "clone", "--quiet", "--shared", "--no-checkout",
                        "--config", "core.autocrlf=false", str(C2C_SOURCE), str(source)], check=True)
        revision = json.loads((ROOT / "tools/c2c-source.json").read_text())["revision"]
        subprocess.run(["git", "-C", str(source), "checkout", "--quiet", "--detach", revision], check=True)
        subprocess.run(["git", "-C", str(source), "remote", "set-url", "origin",
                        "https://github.com/hudrucan/codex-with-chatgpt.git"], check=True)
        self.source = source
        target = source / "skill/references/workflow.md"
        original = target.read_bytes()
        target.unlink()
        self.rejected("Missing input")
        target.write_bytes(original + b"\nchanged\n")
        self.rejected("differs from pinned commit")
        target.unlink()
        target.symlink_to(C2C_SOURCE / "skill/references/workflow.md")
        self.rejected("input")
        target.unlink()
        target.write_bytes(original)
        refs = source / "skill/references"
        refs.rename(source / "refs-original")
        refs.symlink_to(source / "refs-original", target_is_directory=True)
        self.rejected("Symlinked input")
        refs.unlink()
        (source / "refs-original").rename(refs)
        subprocess.run(["git", "-C", str(source), "remote", "set-url", "origin",
                        "https://github.com/unverified/other"], check=True)
        self.rejected("identity mismatch")
        self.source = source / "missing"
        self.rejected("[WinError 2]" if sys.platform == "win32" else "No such file")

    def test_missing_guidance_links_anchors_and_symlinks(self):
        target = self.root / "skills/codex-lazier/SKILL.md"
        original = target.read_bytes()
        for link in ["references/missing.md", "../../README.md", "references/codex.md#missing",
                     "/etc/passwd", "%2e%2e/%2e%2e/README.md"]:
            with self.subTest(link=link):
                target.write_bytes(original + f"\n[Required]({link})\n".encode())
                self.rejected("Broken package")
        target.unlink()
        self.rejected("Missing input")
        target.symlink_to(ROOT / "skills/codex-lazier/SKILL.md")
        self.rejected("input")

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
        archive = next(dist.glob("*.zip"))
        real = outside / archive.name
        archive.rename(real)
        archive.symlink_to(real)
        for arguments in [(), ("--build",)]:
            result = self.run_package(*arguments)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("escaping output", result.stderr)

    def test_changed_bundled_contract_is_stale_even_with_valid_zip_crcs(self):
        self.assertEqual(self.run_package("--build").returncode, 0)
        archive = next((self.root / "dist").glob("*.zip"))
        with ZipFile(archive) as bundle:
            original = [(info, bundle.read(info.filename)) for info in bundle.infolist()]
        with ZipFile(archive, "w") as bundle:
            for info, content in original:
                if info.filename == "codex-lazier/references/c2c/references/workflow.md":
                    content += b"\nUnpinned rule.\n"
                bundle.writestr(info, content)
        with ZipFile(archive) as bundle:
            self.assertIsNone(bundle.testzip())
        result = self.run_package()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Stale archive content: codex-lazier/references/c2c/references/workflow.md", result.stderr)

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
            shutil.rmtree(self.root / "skills")
            module["validate_links"](files)
            provenance = json.loads(files["codex-lazier/provenance.json"])
            self.assertEqual(provenance["version"], module["VERSION"])
            self.assertEqual(provenance["c2c"], json.loads((ROOT / "tools/c2c-source.json").read_text()))
            self.assertEqual(provenance["c2c_packaging"], {
                "renames": {"skill/SKILL.md": "codex-lazier/references/c2c/entrypoint.md"},
                "link_rewrites": {"skill/references/setup.md": {"../SKILL.md": "../entrypoint.md"}},
            })
            self.assertEqual(set(provenance["sha256"]), set(files) - {"codex-lazier/provenance.json"})
            for name, digest in provenance["sha256"].items():
                self.assertEqual(hashlib.sha256(files[name]).hexdigest(), digest)
            for relative in provenance["c2c"]["files"]:
                member = "codex-lazier/references/c2c/" + relative.removeprefix("skill/")
                expected = (C2C_SOURCE / relative).read_bytes()
                self.assertEqual(hashlib.sha256(expected).hexdigest(), provenance["c2c"]["files"][relative])
                if relative == "skill/SKILL.md":
                    member = "codex-lazier/references/c2c/entrypoint.md"
                elif relative == "skill/references/setup.md":
                    expected = expected.replace(b"(../SKILL.md)", b"(../entrypoint.md)")
                self.assertEqual(files[member], expected)
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

    def test_ci_pin_matches_manifest_and_smoke_matrix_is_not_a_model_pass(self):
        lock = json.loads((ROOT / "tools/c2c-source.json").read_text())
        ci = (ROOT / ".github/workflows/ci.yml").read_text()
        self.assertEqual(re.findall(r"ref: ([0-9a-f]{40})", ci), [lock["revision"]] * 2)
        matrix = json.loads((ROOT / "tools/smoke-cases.json").read_text())
        self.assertEqual(matrix["status"], "pending")
        self.assertEqual(len({case["id"] for case in matrix["cases"]}), 15)
        self.assertTrue(all(case["prompt"] and case["observe"] for case in matrix["cases"]))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--c2c-source", required=True, type=Path)
    args, remaining = parser.parse_known_args()
    C2C_SOURCE = args.c2c_source.resolve(strict=True)
    unittest.main(argv=[sys.argv[0], *remaining])
