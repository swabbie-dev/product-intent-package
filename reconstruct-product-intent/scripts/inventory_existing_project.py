#!/usr/bin/env python3
"""Inventory an existing project without treating files as product intent.

Sensitive credential files and common generated/vendor directories are excluded.
The output is evidence inventory, not a semantic or authority decision.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

IGNORED_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "vendor", "dist", "build", "coverage",
    ".next", ".nuxt", ".venv", "venv", "__pycache__", ".idea", ".vscode",
}
SENSITIVE_NAMES = {
    ".env", ".env.local", ".env.production", "id_rsa", "id_ed25519",
    "credentials.json", "service-account.json", "secrets.json",
}
SENSITIVE_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}
TEXT_SUFFIXES = {
    ".md", ".mdx", ".txt", ".rst", ".py", ".js", ".jsx", ".ts", ".tsx",
    ".java", ".kt", ".swift", ".go", ".rs", ".rb", ".php", ".cs", ".cpp",
    ".c", ".h", ".html", ".css", ".scss", ".sql", ".graphql", ".gql",
    ".json", ".yaml", ".yml", ".toml", ".xml", ".dbml", ".mmd", ".feature",
}
MEDIA_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".pdf", ".mov", ".mp4", ".fig"}


def classify(path: Path) -> str:
    name = path.name.lower()
    parts = {p.lower() for p in path.parts}
    if path.suffix.lower() in MEDIA_SUFFIXES:
        return "media_or_design"
    if "test" in name or "tests" in parts or "spec" in name:
        return "test"
    if name.startswith("readme") or "docs" in parts or path.suffix.lower() in {".md", ".mdx", ".rst"}:
        return "documentation"
    if path.suffix.lower() in {".sql", ".dbml"} or "migrations" in parts:
        return "data_or_migration"
    if path.suffix.lower() in TEXT_SUFFIXES:
        return "source_or_configuration"
    return "other"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-file-bytes", type=int, default=25_000_000)
    args = parser.parse_args()

    root = args.project.resolve()
    if not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")

    files = []
    skipped = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in IGNORED_DIRS for part in relative.parts):
            continue
        if path.name.lower() in SENSITIVE_NAMES or path.suffix.lower() in SENSITIVE_SUFFIXES:
            skipped.append({"path": relative.as_posix(), "reason": "sensitive_name_or_suffix"})
            continue
        size = path.stat().st_size
        if size > args.max_file_bytes:
            skipped.append({"path": relative.as_posix(), "reason": "over_size_limit", "size_bytes": size})
            continue
        files.append({
            "path": relative.as_posix(),
            "size_bytes": size,
            "sha256": sha256(path),
            "classification": classify(relative),
            "classification_basis": "heuristic",
        })

    classification_counts: dict[str, int] = {}
    for item in files:
        classification = item["classification"]
        classification_counts[classification] = classification_counts.get(classification, 0) + 1

    output = {
        "root": str(root),
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "warning": "Inventory is evidence only; classifications are heuristic and no item is confirmed product intent.",
        "summary": {
            "file_count": len(files),
            "total_bytes": sum(item["size_bytes"] for item in files),
            "skipped_count": len(skipped),
            "classification_counts": dict(sorted(classification_counts.items())),
        },
        "files": files,
        "skipped": skipped,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
