#!/usr/bin/env python3
"""Find transitive Product Intent Package artifacts affected by changed IDs."""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

from yaml_io import dump_yaml, load_yaml


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path)
    parser.add_argument("changed_ids", nargs="+")
    parser.add_argument("--reverse", action="store_true", help="Also follow incoming dependency edges")
    args = parser.parse_args()

    root = args.package.resolve()
    trace_path = root / "verification" / "traceability.yaml"
    index_path = root / "governance" / "artifact-index.yaml"
    data = load_yaml(trace_path)
    index = load_yaml(index_path)
    edges = data.get("edges", [])

    registered_ids = {item.get("id") for item in index.get("artifacts", []) if item.get("id")}
    unknown_ids = sorted(set(args.changed_ids) - registered_ids)
    if unknown_ids:
        raise SystemExit(
            "Unknown changed ID(s): " + ", ".join(unknown_ids)
            + ". Use stable IDs registered in governance/artifact-index.yaml."
        )

    outgoing: dict[str, set[str]] = {}
    incoming: dict[str, set[str]] = {}
    for edge in edges:
        source, target = edge.get("from"), edge.get("to")
        if not source or not target:
            continue
        outgoing.setdefault(source, set()).add(target)
        incoming.setdefault(target, set()).add(source)

    seen = set(args.changed_ids)
    queue = deque(args.changed_ids)
    while queue:
        current = queue.popleft()
        neighbors = set(outgoing.get(current, set()))
        if args.reverse:
            neighbors |= incoming.get(current, set())
        for neighbor in sorted(neighbors):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)

    result = {
        "changed_ids": args.changed_ids,
        "affected_ids": sorted(seen - set(args.changed_ids)),
        "instruction": "Mark affected active artifacts stale, review them with the relevant authorities, then reconfirm or supersede them.",
    }
    print(dump_yaml(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
