#!/usr/bin/env python3
"""Stamp the Product Intent Package content hash into handoff/readiness.json.

The hash excludes handoff/readiness.json and generated readiness reports so the stamp
is reproducible. Run final validation after stamping.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def content_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        relative = rel(root, path)
        if path.name.startswith("readiness-report.generated") or relative == "handoff/readiness.json":
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

    root = args.package.resolve()
    readiness_path = root / "handoff" / "readiness.json"
    if not readiness_path.is_file():
        raise SystemExit(f"Missing readiness file: {readiness_path}")

    readiness = json.loads(readiness_path.read_text(encoding="utf-8"))
    digest = content_hash(root)
    readiness["package_hash"] = digest
    readiness_path.write_text(json.dumps(readiness, indent=2) + "\n", encoding="utf-8")
    print(digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
