#!/usr/bin/env python3
"""Stamp the Product Intent Package content hash into handoff/readiness.yaml.

The hash excludes handoff/readiness.yaml and generated readiness reports so the stamp
is reproducible. Run final validation after stamping.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path

from yaml_io import load_yaml, write_yaml


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def symlink_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for directory, directories, files in os.walk(root, followlinks=False):
        base = Path(directory)
        for name in (*directories, *files):
            path = base / name
            if path.is_symlink():
                paths.append(path)
    return sorted(paths)


def regular_files(root: Path) -> list[Path]:
    paths: list[Path] = []
    for directory, directories, files in os.walk(root, followlinks=False):
        base = Path(directory)
        directories[:] = [
            name for name in directories if not (base / name).is_symlink()
        ]
        for name in files:
            path = base / name
            if not path.is_symlink() and path.is_file():
                paths.append(path)
    return paths


def content_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(regular_files(root)):
        relative = rel(root, path)
        if path.name.startswith("readiness-report.generated") or relative == "handoff/readiness.yaml":
            continue
        digest.update(relative.encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path)
    args = parser.parse_args()

    if args.package.is_symlink():
        raise SystemExit(
            f"Symbolic links are not allowed in a Product Intent Package: {args.package}"
        )
    root = args.package.resolve()
    links = symlink_paths(root)
    if links:
        raise SystemExit(
            "Symbolic links are not allowed in a Product Intent Package: "
            f"{rel(root, links[0])}"
        )
    readiness_path = root / "handoff" / "readiness.yaml"
    if not readiness_path.is_file():
        raise SystemExit(f"Missing readiness file: {readiness_path}")

    readiness = load_yaml(readiness_path)
    digest = content_hash(root)
    readiness["package_hash"] = digest
    write_yaml(readiness_path, readiness)
    print(digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
