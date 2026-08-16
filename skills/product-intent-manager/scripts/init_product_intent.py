#!/usr/bin/env python3
"""Create a new Product Intent Package from this skill's template."""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path

from yaml_io import load_yaml, write_yaml


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("destination", type=Path)
    parser.add_argument("--name", required=True)
    parser.add_argument("--target-version", required=True)
    parser.add_argument(
        "--baseline",
        choices=["greenfield", "as_implemented", "intended_current", "target_next"],
        required=True,
    )
    parser.add_argument("--package-id", default=None)
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parent.parent
    source = skill_root / "assets" / "product-intent-template"
    destination = args.destination.resolve()
    if destination.exists() and any(destination.iterdir()):
        raise SystemExit(f"Destination is not empty: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination, dirs_exist_ok=True)

    manifest_path = destination / "manifest.yaml"
    manifest = load_yaml(manifest_path)
    manifest["package_id"] = args.package_id or f"PIP-{args.name.upper().replace(' ', '-')[:40]}"
    manifest["product"]["name"] = args.name
    manifest["product"]["target_version"] = args.target_version
    manifest["product"]["target_baseline"] = args.baseline
    now = datetime.now(timezone.utc).isoformat()
    manifest["created_at"] = now
    manifest["updated_at"] = now
    write_yaml(manifest_path, manifest)
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
