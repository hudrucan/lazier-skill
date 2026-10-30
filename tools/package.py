#!/usr/bin/env python3
"""Build or check the local skill archive; no installation or network access."""

import argparse
import hashlib
import json
from pathlib import Path
import posixpath
import re
import sys
import subprocess
from urllib.parse import unquote
from zipfile import BadZipFile, ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "codex-lazier"
VERSION = "0.7.2"
ARCHIVE = ROOT / "dist" / f"codex-lazier-{VERSION}.zip"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def source_paths():
    return {
        "codex-lazier/SKILL.md": SKILL / "SKILL.md",
        "codex-lazier/agents/openai.yaml": SKILL / "agents/openai.yaml",
        "codex-lazier/references/policy.md": SKILL / "references/policy.md",
        "codex-lazier/references/codex.md": SKILL / "references/codex.md",
        "codex-lazier/references/web.md": SKILL / "references/web.md",
        "codex-lazier/LICENSE": ROOT / "LICENSE",
    }


C2C_PATHS = ("skill/SKILL.md", "skill/references/workflow.md", "skill/references/workflow-web.md",
             "skill/references/workflow-async.md", "skill/references/operations.md",
             "skill/references/setup.md", "skill/references/projects.md",
             "skill/references/deprovision.md", "LICENSE")

# Keep the upstream entrypoint as documentation without making it discoverable.
C2C_PACKAGING = {
    "renames": {"skill/SKILL.md": "codex-lazier/references/c2c/entrypoint.md"},
    "link_rewrites": {"skill/references/setup.md": {"../SKILL.md": "../entrypoint.md"}},
}


def read_input(root, relative):
    source = root / relative
    require(not Path(relative).is_absolute() and ".." not in Path(relative).parts,
            f"Input path escape: {relative}")
    require(source.resolve().is_relative_to(root.resolve()), f"Input path escape: {relative}")
    require(all(not part.is_symlink() for part in [source, *source.parents]
                if part != root and part.is_relative_to(root)),
            f"Symlinked input: {relative}")
    require(source.is_file(), f"Missing input: {relative}")
    return source.read_bytes()


def git(root, *args):
    result = subprocess.run(["git", "-c", "core.fsmonitor=false", "-C", str(root), *args],
                            capture_output=True, check=False)
    require(result.returncode == 0, f"C2C source verification failed: {args[0]}")
    return result.stdout


def c2c_files(source):
    lock = json.loads(read_input(ROOT, "tools/c2c-source.json"))
    require(set(lock) == {"repository", "revision", "files"}
            and lock["repository"] == "https://github.com/hudrucan/codex-with-chatgpt"
            and re.fullmatch(r"[0-9a-f]{40}", lock["revision"])
            and set(lock["files"]) == set(C2C_PATHS)
            and all(re.fullmatch(r"[0-9a-f]{64}", h) for h in lock["files"].values()),
            "Invalid pinned C2C source manifest")
    require(not source.is_symlink(), "Symlinked C2C checkout")
    source = source.resolve(strict=True)
    require(Path(git(source, "rev-parse", "--show-toplevel").decode().strip()).resolve() == source,
            "C2C source must be an explicit checkout root")
    origin = git(source, "remote", "get-url", "origin").decode().strip().removesuffix(".git")
    require(origin in {lock["repository"], "git@github.com:hudrucan/codex-with-chatgpt"},
            "C2C source repository identity mismatch")
    require(git(source, "rev-parse", "HEAD").decode().strip() == lock["revision"],
            "C2C source HEAD differs from pinned revision")
    files = {}
    for relative, expected in lock["files"].items():
        content = read_input(source, relative)
        require(git(source, "ls-tree", lock["revision"], "--", relative).startswith(b"100644 blob "),
                f"C2C source is not a regular pinned file: {relative}")
        require(content == git(source, "show", f"{lock['revision']}:{relative}"),
                f"C2C working input differs from pinned commit: {relative}")
        require(hashlib.sha256(content).hexdigest() == expected, f"C2C hash mismatch: {relative}")
        for old, new in C2C_PACKAGING["link_rewrites"].get(relative, {}).items():
            original = f"({old})".encode()
            require(content.count(original) == 1, f"Unexpected C2C reference link: {relative}")
            content = content.replace(original, f"({new})".encode())
        member = C2C_PACKAGING["renames"].get(
            relative, "codex-lazier/references/c2c/" + relative.removeprefix("skill/"))
        files[member] = content
    return files, lock


def source_files(c2c_source):
    files = source_paths()
    content = {name: read_input(ROOT, str(source.relative_to(ROOT))) for name, source in files.items()}
    bundled, lock = c2c_files(c2c_source)
    content.update(bundled)
    provenance = {"name": "codex-lazier", "version": VERSION, "c2c": lock,
                  "c2c_packaging": C2C_PACKAGING,
                  "sha256": {name: hashlib.sha256(data).hexdigest()
                             for name, data in sorted(content.items())}}
    content["codex-lazier/provenance.json"] = (json.dumps(provenance, indent=2, sort_keys=True) + "\n").encode()
    return content


def anchors(content):
    seen, result = {}, set()
    for heading in re.findall(r"^#{1,6} (.+)$", content, re.M):
        slug = re.sub(r"[^\w -]", "", heading.lower()).replace(" ", "-")
        count = seen.get(slug, 0)
        result.add(slug if not count else f"{slug}-{count}")
        seen[slug] = count + 1
    return result


def validate_links(files):
    for name, data in files.items():
        if not name.endswith(".md"):
            continue
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", data.decode()):
            if "://" in target or target.startswith("mailto:"):
                continue
            target = unquote(target)
            path, _, fragment = target.partition("#")
            member = posixpath.normpath(posixpath.join(posixpath.dirname(name), path)) if path else name
            require(not path.startswith("/") and "\\" not in path
                    and member.startswith("codex-lazier/") and member in files,
                    f"Broken package link in {name}: {target}")
            if fragment:
                require(fragment in anchors(files[member].decode()),
                        f"Broken package anchor in {name}: {target}")


def validate_sources(files):
    require([name for name in files if posixpath.basename(name).lower() == "skill.md"]
            == ["codex-lazier/SKILL.md"], "Package must expose only the Lazier skill entrypoint")
    content = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n(.+)\Z", content, re.S)
    require(match is not None, "Missing manifest frontmatter or body")
    # Accept a restricted subset of plain YAML strings, not general YAML syntax.
    fields = {}
    for line in match[1].splitlines():
        key, separator, value = line.partition(": ")
        require(separator and key not in fields and value.strip() and line.isprintable(),
                "Invalid or duplicate metadata field")
        value = value.strip()
        require(re.match(r"[A-Za-z]", value)
                and ":" not in value and "#" not in value
                and value.lower() not in {"null", "true", "false", "yes", "no", "on", "off", "y", "n"},
                "Metadata values must be plain single-line strings starting with an ASCII letter, without ':' or '#'")
        fields[key] = value
    name = fields.get("name", "")
    require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) and len(name) <= 64,
            "Invalid skill name")
    require(name == SKILL.name, "Skill name must match its directory")
    require(0 < len(fields.get("description", "")) <= 1024, "Invalid description length")
    require(set(fields) == {"name", "description", "license"}, "Unexpected manifest fields")
    require(fields["license"] == "MIT", "License must match the bundled license")
    metadata = (SKILL / "agents/openai.yaml").read_text(encoding="utf-8")
    interface = re.fullmatch(
        r'interface:\n'
        r'  display_name: ("[^\n]*")\n'
        r'  short_description: ("[^\n]*")\n'
        r'  default_prompt: ("[^\n]*")\n'
        r'\npolicy:\n  allow_implicit_invocation: true\n', metadata,
    )
    require(interface is not None, "Required interface metadata or implicit invocation policy is missing")
    # JSON-quoted strings are a YAML subset; validate values without duplicating UI text.
    require(all(json.loads(value).strip() for value in interface.groups()),
            "Interface metadata strings must not be empty")

    for name in ["policy", "codex", "web"]:
        heading = files[f"codex-lazier/references/{name}.md"].decode().splitlines()[0]
        require(f"v{VERSION}" in heading.split(), f"Version heading mismatch: {name}")
    validate_links(files)
    packaged_paths = set(source_paths().values())
    for source in ROOT.rglob("*.md"):
        if ".git" in source.relative_to(ROOT).parts or source in packaged_paths:
            continue
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", source.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            resolved = (source.parent / target.split("#", 1)[0]).resolve()
            require(resolved.is_relative_to(ROOT) and resolved.is_file(),
                    f"Broken or external local link in {source.relative_to(ROOT)}: {target}")


def validate_output_paths():
    for path in [ARCHIVE.parent, ARCHIVE, ARCHIVE.with_suffix(".sha256"),
                 ARCHIVE.with_suffix(".provenance.json")]:
        require(not path.is_symlink() and path.resolve().is_relative_to(ROOT),
                f"Symlinked or escaping output: {path.name}")


def build(files):
    validate_output_paths()
    ARCHIVE.parent.mkdir(exist_ok=True)
    with ZipFile(ARCHIVE, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content in sorted(files.items()):
            info = ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = ZIP_DEFLATED
            archive.writestr(info, content, compresslevel=9)
    ARCHIVE.with_suffix(".provenance.json").write_bytes(files["codex-lazier/provenance.json"])
    digest = hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
    ARCHIVE.with_suffix(".sha256").write_text(f"{digest}  {ARCHIVE.name}\n", encoding="utf-8")


def validate_archive(files):
    validate_output_paths()
    with ZipFile(ARCHIVE) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)) and set(names) == set(files),
                "Archive entries differ from the allowed distribution files")
        require(archive.testzip() is None, "Archive CRC validation failed")
        for name, expected in files.items():
            require(archive.read(name) == expected, f"Stale archive content: {name}")
            require(archive.getinfo(name).external_attr >> 16 == 0o100644,
                    f"Unexpected file type or permissions: {name}")
    digest = hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
    require(ARCHIVE.with_suffix(".sha256").read_text(encoding="utf-8") == f"{digest}  {ARCHIVE.name}\n",
            "Archive checksum mismatch")
    require(ARCHIVE.with_suffix(".provenance.json").read_bytes() == files["codex-lazier/provenance.json"],
            "Stale archive provenance")
    print(f"PASS: metadata, local links, {len(files)} archive files, CRCs, source identity, SHA-256\n{digest}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c2c-source", required=True, type=Path, help="Explicit offline C2C checkout at the pinned revision")
    parser.add_argument("--build", action="store_true", help="Rebuild the ZIP, checksum and provenance in dist/")
    parser.add_argument("--tag", help="Require an exact v<package version> release tag")
    args = parser.parse_args()
    if args.tag is not None:
        require(args.tag == f"v{VERSION}",
                f"Release tag mismatch: expected v{VERSION}, got {args.tag}")
    files = source_files(args.c2c_source)
    validate_sources(files)
    if args.build:
        build(files)
    validate_archive(files)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, BadZipFile) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
