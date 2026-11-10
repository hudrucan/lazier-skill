#!/usr/bin/env python3
"""Install the same lazier package into selected local discovery directories."""

import argparse
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import sys

import package as bundle


TARGETS = {
    "codex": Path(".agents/skills"),
    "claude": Path(".claude/skills"),
    "agy": Path(".gemini/config/skills"),
    # Grok Build documents compatibility discovery at the shared user path.
    "grok": Path(".agents/skills"),
}


def payload():
    files = bundle.source_files()
    bundle.validate_sources(files)
    return {Path(name).relative_to(bundle.NAME): content
            for name, content in files.items()}


def installation_state(destination, home, files):
    if destination.is_symlink():
        raise ValueError(f"Preserve linked installation {destination}; update its canonical location instead")
    if not destination.resolve().is_relative_to(home):
        raise ValueError(f"Destination resolves outside the selected home: {destination}")
    for parent in destination.parents:
        if parent.exists() and not parent.is_dir():
            raise ValueError(f"Installation parent is not a directory: {parent}")
        if parent == home:
            break
    if not destination.exists():
        return "install"
    if not destination.is_dir():
        raise ValueError(f"Preserve non-directory destination: {destination}")

    actual = set()
    for item in destination.rglob("*"):
        if item.is_symlink() or not (item.is_file() or item.is_dir()):
            raise ValueError(f"Preserve unsupported installed entry: {item}")
        if item.is_file():
            actual.add(item.relative_to(destination))
    if actual == set(files) and all((destination / p).read_bytes() == data
                                    for p, data in files.items()):
        return "unchanged"

    proof_path = destination / "provenance.json"
    if not proof_path.is_file():
        raise ValueError(f"Preserve unmanaged installation: {destination}")
    proof = json.loads(proof_path.read_text(encoding="utf-8"))
    hashes = proof.get("sha256")
    if proof.get("name") != bundle.NAME or not isinstance(hashes, dict) or not hashes:
        raise ValueError(f"Preserve unrecognized installation: {destination}")
    owned = {Path("provenance.json")}
    for name, expected in hashes.items():
        relative = Path(name).relative_to(bundle.NAME)
        if ".." in relative.parts or "\\" in str(relative):
            raise ValueError(f"Unsafe installed provenance path: {name}")
        owned.add(relative)
        path = destination / relative
        if relative not in actual or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f"Preserve locally modified installation: {destination}")
    if actual != owned:
        raise ValueError(f"Preserve installation with additional files: {destination}")
    return "update"


def install(destination, state, files):
    if state == "unchanged":
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".lazier-install-", dir=destination.parent) as directory:
        candidate = Path(directory) / "candidate"
        candidate.mkdir()
        for relative, content in files.items():
            target = candidate / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        previous = Path(directory) / "previous"
        if state == "update":
            destination.rename(previous)
        try:
            candidate.rename(destination)
        except OSError:
            if previous.exists():
                previous.rename(destination)
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", nargs="+", choices=TARGETS, required=True,
                        help="Explicit local targets; codex and grok share one destination")
    parser.add_argument("--dry-run", action="store_true", help="Show the plan without filesystem writes")
    parser.add_argument("--home", type=Path, default=Path.home(),
                        help="Home directory to use, including for isolated fixture testing")
    args = parser.parse_args()
    home = args.home.expanduser().resolve()
    files = payload()
    destinations = {}
    for target in dict.fromkeys(args.target):
        destination = home / TARGETS[target] / bundle.NAME
        destinations.setdefault(destination, []).append(target)
    # Check every destination before changing any installation.
    plan = [(path, targets, installation_state(path, home, files))
            for path, targets in destinations.items()]
    for destination, targets, state in plan:
        if not args.dry_run:
            install(destination, state, files)
        mode = "PLAN" if args.dry_run else "APPLY"
        print(f"{mode}: {','.join(targets)} {state} {destination}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
