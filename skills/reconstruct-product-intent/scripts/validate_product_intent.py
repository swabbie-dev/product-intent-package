#!/usr/bin/env python3
"""Deterministic structural validator for a Product Intent Package.

This validator checks closure mechanics, registry integrity, traceability, and handoff
claims. It cannot determine whether human intent is substantively correct; authority
confirmation and review remain required.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any, Optional

from yaml_io import dump_yaml, load_yaml as load_yaml_file, write_yaml
from journey_validation import validate_lifecycle_journeys

REQUIRED_FILES = [
    "manifest.yaml",
    "governance/authorities.yaml",
    "governance/scope.yaml",
    "governance/coverage-matrix.yaml",
    "governance/artifact-index.yaml",
    "governance/decisions.yaml",
    "governance/questions.yaml",
    "governance/contradictions.yaml",
    "governance/evidence.yaml",
    "governance/glossary.yaml",
    "governance/change-log.yaml",
    "experience/journeys/index.yaml",
    "product/context.md",
    "product/capabilities.yaml",
    "product/domain-model.md",
    "experience/user-flows.md",
    "experience/screen-map.md",
    "experience/screens.yaml",
    "experience/design-tokens.yaml",
    "experience/components.yaml",
    "behavior/state-machines.md",
    "behavior/rules.yaml",
    "behavior/decision-tables.csv",
    "data/erd.dbml",
    "data/schema.yaml",
    "data/lifecycle.yaml",
    "architecture/system-context.md",
    "architecture/containers.md",
    "architecture/components.md",
    "architecture/deployment.md",
    "architecture/decisions.yaml",
    "contracts/openapi.yaml",
    "contracts/events.yaml",
    "contracts/integrations.yaml",
    "sequences/sequences.md",
    "quality/constraints.yaml",
    "verification/acceptance.yaml",
    "verification/traceability.yaml",
    "handoff/implementation-discretion.yaml",
    "handoff/readiness.yaml",
]

AUTHORITY_DOMAINS = {
    "product_strategy",
    "scope_and_priority",
    "capabilities_and_behavior",
    "ux_and_information_architecture",
    "visual_design_and_content",
    "technical_architecture",
    "data_security_privacy",
    "quality_and_operations",
    "legal_and_compliance",
    "release_and_acceptance",
}

STRUCTURES = {
    "product_map",
    "domain_model",
    "user_flow_model",
    "interface_model",
    "design_system",
    "behavior_model",
    "data_model",
    "system_architecture",
    "interface_contracts",
    "runtime_interactions",
    "quality_constraints",
    "verification_model",
    "lifecycle_journey_model",
}

COVERAGE_LENSES = {
    "roles_permissions_tenancy",
    "identity_account_lifecycle",
    "admin_moderation_support_audit",
    "billing_entitlements_quotas",
    "notifications_preferences_delivery",
    "search_filter_sort_pagination",
    "files_import_export_migration",
    "analytics_instrumentation_experiments",
    "localization_time_currency_units",
    "offline_partial_failure_resume",
    "concurrency_duplicates_ordering_idempotency",
    "privacy_retention_deletion_export",
    "accessibility_keyboard_assistive_motion",
    "environments_deploy_rollback_disaster_recovery",
}

ACTIVE_HANDOFF_STATUSES = {"confirmed", "out_of_scope", "not_applicable"}
ALL_ARTIFACT_STATUSES = ACTIVE_HANDOFF_STATUSES | {
    "observed",
    "hypothesis",
    "proposed",
    "blocked",
    "superseded",
}
DECISION_STATUSES = {"proposed", "confirmed", "rejected", "superseded"}
QUESTION_CLOSED_STATUSES = {"resolved", "closed", "superseded"}
CONTRADICTION_CLOSED_STATUSES = {"resolved", "superseded"}
COVERAGE_STATUSES = {"covered", "not_applicable", "out_of_scope", "blocked"}
MANIFEST_STATUSES = {"inventory", "modeled", "confirmed", "validated", "build_ready", "blocked"}

COVERAGE_RELATIONS = {
    "domain": {"uses_domain"},
    "experience": {"experienced_through"},
    "behavior": {"governed_by"},
    "data": {"uses_data", "persists_as"},
    "architecture": {"implemented_by"},
    "contracts": {"exposed_by"},
    "sequence": {"executed_by"},
    "quality": {"constrained_by"},
    "verification": {"verified_by"},
}

ALLOWED_RELATIONS = {
    "performed_by",
    "uses_domain",
    "experienced_through",
    "governed_by",
    "uses_data",
    "persists_as",
    "implemented_by",
    "exposed_by",
    "executed_by",
    "constrained_by",
    "verified_by",
    "depends_on",
    "supersedes",
}

PREFIX_KIND = {
    "ACTOR": "actor",
    "CAP": "capability",
    "DOM": "domain_concept",
    "FLOW": "flow",
    "SCREEN": "screen",
    "MOCK": "mockup",
    "TOKEN": "design_token_set",
    "COMP": "component",
    "RULE": "rule",
    "SM": "state_machine",
    "DT": "decision_table",
    "DATA": "data_model",
    "ARCH": "architecture",
    "API": "api_contract",
    "EVT": "event_contract",
    "INT": "integration_contract",
    "SEQ": "sequence",
    "QC": "quality_constraint",
    "ACC": "acceptance_scenario",
    "JOURNEY": "lifecycle_journey",
    "DIS": "implementation_discretion",
}

ARTIFACT_ID_RE = re.compile(
    r"\b(?:" + "|".join(sorted(PREFIX_KIND, key=len, reverse=True)) + r")-\d{3,}\b"
)
CANONICAL_ID_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9_])([A-Z][A-Z0-9]*)-(\d{3,})([A-Za-z0-9]*)(?![A-Za-z0-9_])"
)
GOVERNANCE_ID_PREFIXES = {"AUTH", "EVID", "DEC", "Q", "CON", "CHANGE"}
PLACEHOLDER_RE = re.compile(
    r"(?:\bTBD\b|\bTODO\b|\bUNSET\b|\bUNKNOWN\b|\?\?\?|<placeholder>|\[placeholder\])",
    re.IGNORECASE,
)
MERMAID_FENCE_RE = re.compile(r"(?ms)^```mermaid[ \t]*\n.*?^```[ \t]*(?:\n|$)")


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def find_package_symlinks(root: Path) -> list[Path]:
    if root.is_symlink():
        return [root]
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("*") if path.is_symlink())


def load_document(path: Path, errors: list[str]) -> Any:
    try:
        return load_yaml_file(path)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"Invalid YAML: {path}: {exc}")
        return {}


def resolve_artifact_file(
    root: Path,
    artifact_id: str,
    path_value: Any,
    errors: list[str],
) -> Optional[Path]:
    if not isinstance(path_value, str) or not path_value:
        errors.append(f"{artifact_id}: artifact path is required")
        return None

    file_part = path_value.split("#", 1)[0]
    declared_path = Path(file_part)
    if not file_part or declared_path.is_absolute() or ".." in declared_path.parts:
        errors.append(f"{artifact_id}: artifact path must stay inside package: {path_value}")
        return None

    declared_candidate = root / declared_path
    if declared_candidate.is_symlink():
        errors.append(f"{artifact_id}: artifact path cannot be a symbolic link: {path_value}")
        return None
    candidate = declared_candidate.resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        errors.append(f"{artifact_id}: artifact path must stay inside package: {path_value}")
        return None

    if not candidate.is_file():
        errors.append(f"{artifact_id}: artifact path does not exist: {path_value}")
        return None
    return candidate


def iter_text_files(root: Path) -> Iterator[Path]:
    for path in sorted(
        p for p in root.rglob("*") if not p.is_symlink() and p.is_file()
    ):
        relative = rel(root, path)
        if path.name.startswith("readiness-report.generated"):
            continue
        if relative == "handoff/readiness.yaml":
            yield path
            continue
        try:
            path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        yield path


def content_hash(root: Path) -> str:
    """Hash product content while excluding mutable readiness/report metadata."""
    digest = hashlib.sha256()
    for path in sorted(
        p for p in root.rglob("*") if not p.is_symlink() and p.is_file()
    ):
        relative = rel(root, path)
        if path.name.startswith("readiness-report.generated") or relative == "handoff/readiness.yaml":
            continue
        digest.update(relative.encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def artifact_ids_in_files(root: Path) -> set[str]:
    found: set[str] = set()
    for path in iter_text_files(root):
        if rel(root, path) == "governance/artifact-index.yaml":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        found.update(ARTIFACT_ID_RE.findall(text))
    return found


def duplicate_ids(records: list[dict[str, Any]]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for record in records:
        record_id = record.get("id")
        if not record_id:
            continue
        if record_id in seen:
            duplicates.add(record_id)
        seen.add(record_id)
    return duplicates


def require_confirmed_decision(
    decision_id: Any,
    confirmed_decision_ids: set[str],
    context: str,
    errors: list[str],
) -> None:
    if decision_id not in confirmed_decision_ids:
        errors.append(f"{context}: requires a confirmed decision ID")


def has_applicable_delegation(
    decision: dict[str, Any],
    accountable_authority_id: str,
    delegations: Any,
    confirmed_decision_ids: set[str],
) -> bool:
    decision_authority_id = decision.get("authority_id")
    affected_ids = {
        value
        for value in (decision.get("affects") or [])
        if isinstance(value, str)
    }
    if not isinstance(delegations, list) or not affected_ids:
        return False
    for delegation in delegations:
        if not isinstance(delegation, dict):
            continue
        if (
            delegation.get("delegator_id") != accountable_authority_id
            or delegation.get("delegate_id") != decision_authority_id
            or delegation.get("decision_id") not in confirmed_decision_ids
        ):
            continue
        scope = delegation.get("scope")
        if not isinstance(scope, str):
            continue
        if affected_ids & set(ARTIFACT_ID_RE.findall(scope)):
            return True
    return False


def validate_canonical_ids(root: Path, errors: list[str]) -> None:
    reported: set[tuple[str, str]] = set()
    for path in iter_text_files(root):
        relative = rel(root, path)
        if "source-evidence" in Path(relative).parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for match in CANONICAL_ID_TOKEN_RE.finditer(text):
            prefix, _digits, suffix = match.groups()
            value = match.group(0)
            if prefix in GOVERNANCE_ID_PREFIXES:
                continue
            key = (relative, value)
            if key in reported:
                continue
            reported.add(key)
            if prefix not in PREFIX_KIND:
                errors.append(
                    f"{relative}: unsupported canonical ID prefix {prefix!r} in {value!r}"
                )
            elif suffix:
                errors.append(f"{relative}: canonical ID {value!r} must end with digits")


def related_trace_edges(
    edges: list[dict[str, Any]],
    record_id: str,
    relation: str,
    other_ids: Optional[set[str]] = None,
) -> set[tuple[Any, Any, Any]]:
    related: set[tuple[Any, Any, Any]] = set()
    for edge in edges:
        if edge.get("source_part_id") is not None:
            continue
        source = edge.get("from")
        target = edge.get("to")
        if edge.get("relation") != relation:
            continue
        if source == record_id and (other_ids is None or target in other_ids):
            related.add((source, relation, target))
        elif target == record_id and (other_ids is None or source in other_ids):
            related.add((source, relation, target))
    return related


def source_trace_edges(
    edges: list[dict[str, Any]],
    source_id: str,
    relation: str,
) -> set[tuple[Any, Any, Any]]:
    return {
        (edge.get("from"), relation, edge.get("to"))
        for edge in edges
        if edge.get("from") == source_id
        and edge.get("relation") == relation
        and edge.get("source_part_id") is None
    }


def compare_declared_traceability(
    record_id: str,
    field: str,
    expected: set[tuple[Any, Any, Any]],
    actual: set[tuple[Any, Any, Any]],
    errors: list[str],
) -> None:
    for source, relation, target in sorted(expected - actual, key=str):
        errors.append(
            f"{record_id}: {field} missing traceability edge "
            f"{source} -[{relation}]-> {target}"
        )
    for source, relation, target in sorted(actual - expected, key=str):
        errors.append(
            f"{record_id}: {field} has extra traceability edge "
            f"{source} -[{relation}]-> {target}"
        )


def validate(root: Path) -> tuple[list[str], list[str], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []

    package_symlinks = find_package_symlinks(root)
    for path in package_symlinks:
        location = "." if path == root else rel(root, path)
        errors.append(
            f"{location}: symbolic links are not allowed in a Product Intent Package"
        )
    if package_symlinks:
        return errors, warnings, {"content_hash": None}

    for item in REQUIRED_FILES:
        if not (root / item).is_file():
            errors.append(f"Missing required file: {item}")

    if errors:
        return errors, warnings, {"content_hash": content_hash(root) if root.exists() else None}

    for item in REQUIRED_FILES:
        if not item.endswith(".md"):
            continue
        text = (root / item).read_text(encoding="utf-8")
        if not MERMAID_FENCE_RE.search(text):
            errors.append(f"{item}: requires a fenced mermaid block")

    parsed = {
        item: load_document(root / item, errors)
        for item in REQUIRED_FILES
        if item.endswith(".yaml")
    }

    artifact_records = (parsed.get("governance/artifact-index.yaml", {}) or {}).get("artifacts") or []
    loaded_yaml_paths = {item for item in parsed}
    checked_markdown_paths = {item for item in REQUIRED_FILES if item.endswith(".md")}
    for artifact in artifact_records:
        artifact_id = artifact.get("id") or "<missing-id>"
        path_value = artifact.get("path")
        artifact_file = resolve_artifact_file(root, artifact_id, path_value, errors)
        if artifact_file is None:
            continue
        file_part = path_value.split("#", 1)[0]
        suffix = Path(file_part).suffix.lower()
        if suffix in {".json", ".mmd"}:
            errors.append(
                f"{artifact_id}: canonical package path cannot use a legacy format: {file_part}"
            )
        elif suffix == ".yml":
            errors.append(f"{artifact_id}: canonical YAML path must use .yaml: {file_part}")
        elif suffix == ".yaml" and file_part not in loaded_yaml_paths:
            parsed[file_part] = load_document(artifact_file, errors)
            loaded_yaml_paths.add(file_part)
        elif suffix == ".md" and file_part not in checked_markdown_paths:
            text = artifact_file.read_text(encoding="utf-8")
            if not MERMAID_FENCE_RE.search(text):
                errors.append(f"{file_part}: requires a fenced mermaid block")
            checked_markdown_paths.add(file_part)

    validate_canonical_ids(root, errors)

    manifest = parsed.get("manifest.yaml", {}) or {}
    build_ready = bool(manifest.get("build_ready"))
    manifest_status = manifest.get("status")
    if manifest.get("schema_version") != "3.0.0":
        errors.append("manifest.yaml: schema_version must be '3.0.0'")
    if manifest_status not in MANIFEST_STATUSES:
        errors.append(f"manifest.yaml: invalid status {manifest_status!r}")
    if build_ready and manifest_status != "build_ready":
        errors.append("manifest.yaml: build_ready=true requires status='build_ready'")
    if not build_ready and manifest_status == "build_ready":
        errors.append("manifest.yaml: status='build_ready' requires build_ready=true")
    if manifest.get("package_id") in (None, "", "PIP-UNSET"):
        errors.append("manifest.yaml: package_id is unset")
    product = manifest.get("product") or {}
    if not product.get("name"):
        errors.append("manifest.yaml: product.name is required")
    if not product.get("target_version"):
        errors.append("manifest.yaml: product.target_version is required")
    if product.get("target_baseline") not in {"greenfield", "as_implemented", "intended_current", "target_next"}:
        errors.append("manifest.yaml: invalid product.target_baseline")

    authorities_data = parsed.get("governance/authorities.yaml", {}) or {}
    authorities = authorities_data.get("authorities") or []
    duplicate_authorities = duplicate_ids(authorities)
    if duplicate_authorities:
        errors.append(f"Duplicate authority IDs: {', '.join(sorted(duplicate_authorities))}")
    authority_ids = {a.get("id") for a in authorities if a.get("id")}
    for authority in authorities:
        aid = authority.get("id", "<missing-id>")
        if not authority.get("name"):
            errors.append(f"{aid}: authority requires name")

    domains = authorities_data.get("domains") or []
    domain_map = {d.get("domain"): d.get("accountable_authority_id") for d in domains}
    missing_domains = sorted(AUTHORITY_DOMAINS - set(domain_map))
    extra_domains = sorted(set(domain_map) - AUTHORITY_DOMAINS)
    if missing_domains:
        errors.append(f"Missing authority domains: {', '.join(missing_domains)}")
    if extra_domains:
        warnings.append(f"Unrecognized authority domains: {', '.join(extra_domains)}")
    for domain in sorted(AUTHORITY_DOMAINS):
        auth_id = domain_map.get(domain)
        if not auth_id:
            errors.append(f"No accountable authority for domain: {domain}")
        elif auth_id not in authority_ids:
            errors.append(f"Authority domain {domain} points to unknown authority: {auth_id}")

    decisions = (parsed.get("governance/decisions.yaml", {}) or {}).get("decisions") or []
    duplicate_decisions = duplicate_ids(decisions)
    if duplicate_decisions:
        errors.append(f"Duplicate decision IDs: {', '.join(sorted(duplicate_decisions))}")
    decision_map = {d.get("id"): d for d in decisions if d.get("id")}
    decision_ids = set(decision_map)
    confirmed_decision_ids = {
        decision_id for decision_id, decision in decision_map.items() if decision.get("status") == "confirmed"
    }
    delegations = authorities_data.get("delegations") or []
    for decision_id, decision in decision_map.items():
        status = decision.get("status")
        if status not in DECISION_STATUSES:
            errors.append(f"{decision_id}: invalid decision status {status!r}")
        authority_id = decision.get("authority_id")
        if authority_id not in authority_ids:
            errors.append(f"{decision_id}: unknown or missing authority_id")
        decision_domain = decision.get("domain")
        if not isinstance(decision_domain, str) or decision_domain not in domain_map:
            errors.append(f"{decision_id}: unknown or missing decision domain")
        else:
            accountable_authority_id = domain_map[decision_domain]
            if (
                authority_id != accountable_authority_id
                and not has_applicable_delegation(
                    decision,
                    accountable_authority_id,
                    delegations,
                    confirmed_decision_ids,
                )
            ):
                errors.append(
                    f"{decision_id}: authority_id has no authority for domain "
                    f"{decision_domain!r} and has no applicable delegation"
                )
        if status == "confirmed":
            if not decision.get("statement"):
                errors.append(f"{decision_id}: confirmed decision requires statement")
            if not decision.get("confirmed_at"):
                errors.append(f"{decision_id}: confirmed decision requires confirmed_at")
            if not decision.get("confirmation_ref"):
                errors.append(f"{decision_id}: confirmed decision requires confirmation_ref")
        for superseded in decision.get("supersedes") or []:
            if superseded not in decision_ids:
                errors.append(f"{decision_id}: supersedes unknown decision {superseded}")

    for delegation in delegations:
        did = delegation.get("id", "<missing-id>")
        if delegation.get("delegator_id") not in authority_ids:
            errors.append(f"{did}: delegation has unknown delegator_id")
        delegate_id = delegation.get("delegate_id")
        if delegate_id not in authority_ids and delegate_id != "AGENT":
            errors.append(f"{did}: delegation has unknown delegate_id")
        if not delegation.get("scope") or not delegation.get("constraints"):
            errors.append(f"{did}: delegation requires explicit scope and constraints")
        require_confirmed_decision(delegation.get("decision_id"), confirmed_decision_ids, did, errors)

    questions = (parsed.get("governance/questions.yaml", {}) or {}).get("questions") or []
    duplicate_questions = duplicate_ids(questions)
    if duplicate_questions:
        errors.append(f"Duplicate question IDs: {', '.join(sorted(duplicate_questions))}")
    open_questions: list[str] = []
    for question in questions:
        qid = question.get("id", "<missing-id>")
        if question.get("requested_authority_id") not in authority_ids:
            errors.append(f"{qid}: question has unknown or missing requested_authority_id")
        if question.get("status") not in QUESTION_CLOSED_STATUSES:
            open_questions.append(qid)
        else:
            resolution = question.get("resolution_decision_id")
            if resolution is not None:
                require_confirmed_decision(resolution, confirmed_decision_ids, qid, errors)
    if build_ready and open_questions:
        errors.append(f"Build-ready package has unresolved questions: {', '.join(open_questions)}")

    contradictions = (parsed.get("governance/contradictions.yaml", {}) or {}).get("contradictions") or []
    duplicate_contradictions = duplicate_ids(contradictions)
    if duplicate_contradictions:
        errors.append(f"Duplicate contradiction IDs: {', '.join(sorted(duplicate_contradictions))}")
    open_contradictions: list[str] = []
    for contradiction in contradictions:
        cid = contradiction.get("id", "<missing-id>")
        if contradiction.get("requested_authority_id") not in authority_ids:
            errors.append(f"{cid}: contradiction has unknown or missing requested_authority_id")
        if not contradiction.get("claims") or len(contradiction.get("claims") or []) < 2:
            errors.append(f"{cid}: contradiction requires at least two conflicting claims")
        if contradiction.get("status") not in CONTRADICTION_CLOSED_STATUSES:
            open_contradictions.append(cid)
        else:
            require_confirmed_decision(
                contradiction.get("resolution_decision_id"), confirmed_decision_ids, cid, errors
            )
    if build_ready and open_contradictions:
        errors.append(
            f"Build-ready package has unresolved contradictions: {', '.join(open_contradictions)}"
        )

    evidence = (parsed.get("governance/evidence.yaml", {}) or {}).get("evidence") or []
    duplicate_evidence = duplicate_ids(evidence)
    if duplicate_evidence:
        errors.append(f"Duplicate evidence IDs: {', '.join(sorted(duplicate_evidence))}")
    evidence_ids = {e.get("id") for e in evidence if e.get("id")}
    for item in evidence:
        eid = item.get("id", "<missing-id>")
        if not item.get("type") or not item.get("location"):
            errors.append(f"{eid}: evidence requires type and location")
        if item.get("confidence") not in {"high", "medium", "low"}:
            errors.append(f"{eid}: evidence confidence must be high, medium, or low")

    duplicate_artifacts = duplicate_ids(artifact_records)
    if duplicate_artifacts:
        errors.append(f"Duplicate artifact IDs: {', '.join(sorted(duplicate_artifacts))}")
    artifacts = {a.get("id"): a for a in artifact_records if a.get("id")}
    for artifact_id, artifact in artifacts.items():
        status = artifact.get("status")
        if status not in ALL_ARTIFACT_STATUSES:
            errors.append(f"{artifact_id}: invalid status {status!r}")
        prefix = artifact_id.split("-", 1)[0]
        expected_kind = PREFIX_KIND.get(prefix)
        if expected_kind is None:
            errors.append(f"{artifact_id}: unsupported artifact ID prefix")
        elif artifact.get("kind") != expected_kind:
            errors.append(
                f"{artifact_id}: kind must be {expected_kind!r}, got {artifact.get('kind')!r}"
            )
        if artifact.get("authority_id") not in authority_ids:
            errors.append(f"{artifact_id}: unknown or missing authority_id")
        if not isinstance(artifact.get("version"), int) or artifact.get("version", 0) < 1:
            errors.append(f"{artifact_id}: version must be a positive integer")
        for source_ref in artifact.get("source_refs") or []:
            if source_ref not in evidence_ids:
                errors.append(f"{artifact_id}: unknown evidence source_ref {source_ref}")
        if status in ACTIVE_HANDOFF_STATUSES:
            require_confirmed_decision(
                artifact.get("confirmation_decision_id"), confirmed_decision_ids, artifact_id, errors
            )
        if build_ready and status not in ACTIVE_HANDOFF_STATUSES and status != "superseded":
            errors.append(f"{artifact_id}: active handoff contains non-final status {status!r}")
        if build_ready and artifact.get("stale"):
            errors.append(f"{artifact_id}: artifact is stale")

    found_artifact_ids = artifact_ids_in_files(root)
    unregistered = sorted(found_artifact_ids - set(artifacts))
    if unregistered:
        errors.append(f"Unregistered stable artifact IDs found in package: {', '.join(unregistered)}")
    orphan_registered = sorted(
        artifact_id
        for artifact_id, artifact in artifacts.items()
        if artifact.get("status") != "superseded" and artifact_id not in found_artifact_ids
    )
    if orphan_registered:
        errors.append(
            "Registered active artifacts are not referenced outside artifact-index.yaml: "
            + ", ".join(orphan_registered)
        )

    coverage = parsed.get("governance/coverage-matrix.yaml", {}) or {}
    for key, expected in (("structures", STRUCTURES), ("lenses", COVERAGE_LENSES)):
        records = coverage.get(key) or []
        record_map = {r.get("name"): r for r in records if r.get("name")}
        missing = sorted(expected - set(record_map))
        extra = sorted(set(record_map) - expected)
        if missing:
            errors.append(f"coverage-matrix.yaml: missing {key}: {', '.join(missing)}")
        if extra:
            warnings.append(f"coverage-matrix.yaml: unrecognized {key}: {', '.join(extra)}")
        for name in sorted(expected & set(record_map)):
            record = record_map[name]
            status = record.get("status")
            if status not in COVERAGE_STATUSES:
                errors.append(f"Coverage {key[:-1]} {name}: invalid status {status!r}")
                continue
            if build_ready and status == "blocked":
                errors.append(f"Build-ready package has blocked coverage {key[:-1]}: {name}")
            if status == "covered":
                artifact_ids = record.get("artifact_ids") or []
                if not artifact_ids:
                    errors.append(f"Coverage {key[:-1]} {name}: covered requires artifact_ids")
                for artifact_id in artifact_ids:
                    if artifact_id not in artifacts:
                        errors.append(
                            f"Coverage {key[:-1]} {name}: unknown artifact_id {artifact_id}"
                        )
                    elif build_ready and artifacts[artifact_id].get("status") != "confirmed":
                        errors.append(
                            f"Coverage {key[:-1]} {name}: artifact {artifact_id} is not confirmed"
                        )
            elif status in {"not_applicable", "out_of_scope"}:
                require_confirmed_decision(
                    record.get("decision_id"), confirmed_decision_ids, f"Coverage {name}", errors
                )

    capabilities_data = parsed.get("product/capabilities.yaml", {}) or {}
    actors = capabilities_data.get("actors") or []
    capabilities = capabilities_data.get("capabilities") or []
    duplicate_actors = duplicate_ids(actors)
    duplicate_capabilities = duplicate_ids(capabilities)
    if duplicate_actors:
        errors.append(f"Duplicate actor IDs: {', '.join(sorted(duplicate_actors))}")
    if duplicate_capabilities:
        errors.append(f"Duplicate capability IDs: {', '.join(sorted(duplicate_capabilities))}")
    actor_ids = {a.get("id") for a in actors if a.get("id")}
    capability_ids = {c.get("id") for c in capabilities if c.get("id")}
    for actor_id in actor_ids:
        if actor_id not in artifacts:
            errors.append(f"Actor missing artifact-index record: {actor_id}")
    for capability_id in capability_ids:
        if capability_id not in artifacts:
            errors.append(f"Capability missing artifact-index record: {capability_id}")

    scope = parsed.get("governance/scope.yaml", {}) or {}
    if build_ready:
        if not scope.get("target_outcome"):
            errors.append("governance/scope.yaml: target_outcome is required at handoff")
        if not scope.get("release_boundary"):
            errors.append("governance/scope.yaml: release_boundary is required at handoff")
        if not scope.get("success_measures"):
            errors.append("governance/scope.yaml: success_measures are required at handoff")
    in_scope_ids = scope.get("in_scope_capability_ids") or []
    if len(in_scope_ids) != len(set(in_scope_ids)):
        errors.append("governance/scope.yaml: duplicate in-scope capability IDs")
    if build_ready and not in_scope_ids:
        errors.append("Build-ready package must contain at least one in-scope capability")
    for cap_id in in_scope_ids:
        if cap_id not in capability_ids:
            errors.append(f"Scope references unknown capability: {cap_id}")
        if cap_id not in artifacts:
            errors.append(f"In-scope capability missing artifact-index record: {cap_id}")
        elif artifacts[cap_id].get("status") != "confirmed":
            errors.append(f"In-scope capability is not confirmed: {cap_id}")
    out_of_scope_cap_ids = {
        item.get("capability_id")
        for item in scope.get("out_of_scope") or []
        if isinstance(item, dict) and item.get("capability_id")
    }
    unscoped_capabilities = sorted(capability_ids - set(in_scope_ids) - out_of_scope_cap_ids)
    if unscoped_capabilities:
        errors.append(
            "Capabilities are neither in scope nor explicitly out of scope: "
            + ", ".join(unscoped_capabilities)
        )
    for item in scope.get("out_of_scope") or []:
        if isinstance(item, dict):
            require_confirmed_decision(
                item.get("decision_id"), confirmed_decision_ids, "Out-of-scope entry", errors
            )

    trace = parsed.get("verification/traceability.yaml", {}) or {}
    if not isinstance(trace, dict):
        errors.append("verification/traceability.yaml: must be a mapping")
        trace = {}
    edges = trace.get("edges") or []
    if not isinstance(edges, list):
        errors.append("verification/traceability.yaml: edges must be a list")
        edges = []
    edge_keys: set[tuple[Any, Any, Any, Any]] = set()
    by_source: dict[str, list[dict[str, Any]]] = {}
    connected_ids: set[str] = set()
    valid_edges: list[dict[str, Any]] = []
    for edge_index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            errors.append(f"verification/traceability.yaml: edges[{edge_index}] must be a mapping")
            continue
        source = edge.get("from")
        relation = edge.get("relation")
        target = edge.get("to")
        source_part_id = edge.get("source_part_id")
        edge_context = f"verification/traceability.yaml: edges[{edge_index}]"
        invalid_edge = False
        for field, value in (("from", source), ("relation", relation), ("to", target)):
            if not isinstance(value, str) or not value:
                errors.append(f"{edge_context}: {field} must be a non-empty string")
                invalid_edge = True
        if source_part_id is not None and (
            not isinstance(source_part_id, str) or not source_part_id
        ):
            errors.append(f"{edge_context}: source_part_id must be a non-empty string")
            invalid_edge = True
        if invalid_edge:
            continue
        key = (source, relation, target, source_part_id)
        if key in edge_keys:
            warnings.append(f"Duplicate traceability edge: {source} -[{relation}]-> {target}")
        edge_keys.add(key)
        valid_edges.append(edge)
        if relation not in ALLOWED_RELATIONS:
            errors.append(f"Invalid traceability relation: {relation!r}")
        if source not in artifacts:
            errors.append(f"Traceability source is not registered: {source}")
        if target not in artifacts:
            errors.append(f"Traceability target is not registered: {target}")
        if source == target:
            errors.append(f"Traceability self-edge is not allowed: {source}")
        by_source.setdefault(source, []).append(edge)
        if source:
            connected_ids.add(source)
        if target:
            connected_ids.add(target)

    edges = valid_edges

    if build_ready:
        unconnected = sorted(
            artifact_id
            for artifact_id, artifact in artifacts.items()
            if artifact.get("status") == "confirmed" and artifact_id not in connected_ids
        )
        if unconnected:
            errors.append(
                "Confirmed artifacts are disconnected from the traceability graph: "
                + ", ".join(unconnected)
            )

    capability_map = {c.get("id"): c for c in capabilities if c.get("id")}
    journey_counts = validate_lifecycle_journeys(
        root,
        parsed.get("experience/journeys/index.yaml", {}),
        artifacts,
        evidence_ids,
        decision_ids,
        confirmed_decision_ids,
        decision_map,
        {q.get("id") for q in questions if isinstance(q, dict) and q.get("id")},
        {c.get("id") for c in contradictions if isinstance(c, dict) and c.get("id")},
        actor_ids,
        capability_map,
        in_scope_ids,
        edges,
        build_ready,
        errors,
    )
    for cap_id, cap in capability_map.items():
        cap_actor_ids = cap.get("actor_ids") or []
        for actor_id in cap_actor_ids:
            if actor_id not in actor_ids:
                errors.append(f"{cap_id}: references unknown actor_id {actor_id}")
        compare_declared_traceability(
            cap_id,
            "actor_ids",
            {
                (actor_id, "performed_by", cap_id)
                for actor_id in cap_actor_ids
            },
            related_trace_edges(edges, cap_id, "performed_by", actor_ids),
            errors,
        )
        cap_dependency_ids = cap.get("dependency_ids") or []
        for dependency_id in cap_dependency_ids:
            if dependency_id not in capability_ids:
                errors.append(f"{cap_id}: references unknown dependency_id {dependency_id}")
        compare_declared_traceability(
            cap_id,
            "dependency_ids",
            {
                (cap_id, "depends_on", dependency_id)
                for dependency_id in cap_dependency_ids
            },
            source_trace_edges(edges, cap_id, "depends_on"),
            errors,
        )

    for cap_id in in_scope_ids:
        cap = capability_map.get(cap_id) or {}
        cap_actor_ids = cap.get("actor_ids") or []
        if not cap_actor_ids:
            errors.append(f"{cap_id}: at least one actor_id is required")
        requirements = cap.get("coverage_requirements")
        exceptions = cap.get("coverage_exceptions") or {}
        if not isinstance(requirements, dict):
            errors.append(f"{cap_id}: coverage_requirements must declare every coverage dimension")
            continue
        if set(requirements) != set(COVERAGE_RELATIONS):
            errors.append(
                f"{cap_id}: coverage_requirements must contain exactly: "
                + ", ".join(sorted(COVERAGE_RELATIONS))
            )
        for dimension, relations in COVERAGE_RELATIONS.items():
            value = requirements.get(dimension)
            if not isinstance(value, bool):
                errors.append(f"{cap_id}: coverage requirement {dimension!r} must be true or false")
                continue
            if dimension == "verification" and value is not True:
                errors.append(f"{cap_id}: verification coverage cannot be waived")
                continue
            if value:
                found = any(e.get("relation") in relations for e in by_source.get(cap_id, []))
                if not found:
                    errors.append(f"{cap_id}: missing traceability for required dimension {dimension}")
            else:
                require_confirmed_decision(
                    exceptions.get(dimension),
                    confirmed_decision_ids,
                    f"{cap_id} coverage exception {dimension}",
                    errors,
                )

    acceptance = (parsed.get("verification/acceptance.yaml", {}) or {}).get("scenarios") or []
    duplicate_acceptance = duplicate_ids(acceptance)
    if duplicate_acceptance:
        errors.append(f"Duplicate acceptance IDs: {', '.join(sorted(duplicate_acceptance))}")
    acceptance_ids = {a.get("id") for a in acceptance if a.get("id")}
    for scenario in acceptance:
        sid = scenario.get("id", "<missing-id>")
        if sid not in artifacts:
            errors.append(f"Acceptance scenario missing artifact-index record: {sid}")
        scenario_caps = scenario.get("capability_ids") or []
        if not scenario_caps:
            errors.append(f"{sid}: acceptance scenario must reference capability_ids")
        for cap_id in scenario_caps:
            if cap_id not in capability_ids:
                errors.append(f"{sid}: references unknown capability_id {cap_id}")
        compare_declared_traceability(
            sid,
            "capability_ids",
            {
                (cap_id, "verified_by", sid)
                for cap_id in scenario_caps
            },
            related_trace_edges(edges, sid, "verified_by", capability_ids),
            errors,
        )
        if not scenario.get("given") or not scenario.get("when") or not scenario.get("then"):
            errors.append(f"{sid}: acceptance scenario requires given, when, and then")

    rules = (parsed.get("behavior/rules.yaml", {}) or {}).get("rules") or []
    for rule in rules:
        rule_id = rule.get("id", "<missing-id>")
        rule_scope_ids = rule.get("scope_ids") or []
        for scope_id in rule_scope_ids:
            if scope_id not in artifacts:
                errors.append(f"{rule_id}: references unknown scope_id {scope_id}")
        compare_declared_traceability(
            rule_id,
            "scope_ids",
            {
                (cap_id, "governed_by", rule_id)
                for cap_id in rule_scope_ids
            },
            related_trace_edges(edges, rule_id, "governed_by", set(artifacts)),
            errors,
        )

    constraints = (parsed.get("quality/constraints.yaml", {}) or {}).get("constraints") or []
    for constraint in constraints:
        constraint_id = constraint.get("id", "<missing-id>")
        constraint_scope_ids = constraint.get("scope_ids") or []
        for scope_id in constraint_scope_ids:
            if scope_id not in artifacts:
                errors.append(f"{constraint_id}: references unknown scope_id {scope_id}")
        compare_declared_traceability(
            constraint_id,
            "scope_ids",
            {
                (cap_id, "constrained_by", constraint_id)
                for cap_id in constraint_scope_ids
            },
            related_trace_edges(edges, constraint_id, "constrained_by", set(artifacts)),
            errors,
        )

    if build_ready:
        for artifact_id, artifact in artifacts.items():
            if artifact.get("status") != "confirmed":
                continue
            if artifact.get("kind") in {"rule", "state_machine", "decision_table", "quality_constraint"}:
                if not any(e.get("relation") == "verified_by" for e in by_source.get(artifact_id, [])):
                    errors.append(f"{artifact_id}: confirmed {artifact.get('kind')} lacks verified_by coverage")

    discretion = parsed.get("handoff/implementation-discretion.yaml", {}) or {}
    if discretion.get("default_policy") != "forbidden_if_behavior_affecting_or_user_observable":
        errors.append("handoff/implementation-discretion.yaml: invalid default_policy")
    grants = discretion.get("grants") or []
    duplicate_grants = duplicate_ids(grants)
    if duplicate_grants:
        errors.append(f"Duplicate discretion IDs: {', '.join(sorted(duplicate_grants))}")
    for grant in grants:
        gid = grant.get("id", "<missing-id>")
        if gid not in artifacts:
            errors.append(f"Implementation-discretion grant missing artifact-index record: {gid}")
        if grant.get("authority_id") not in authority_ids:
            errors.append(f"{gid}: unknown or missing authority_id")
        require_confirmed_decision(
            grant.get("confirmation_decision_id"), confirmed_decision_ids, gid, errors
        )
        for field in ("scope", "allowed_choices", "forbidden_outcomes", "constraints"):
            if not grant.get(field):
                errors.append(f"{gid}: implementation discretion requires {field}")

    readiness = parsed.get("handoff/readiness.yaml", {}) or {}
    gates = readiness.get("gates") or {}
    expected_gates = {
        "governance",
        "structural_coverage",
        "journey_closure",
        "capability_traceability",
        "behavioral_closure",
        "technical_closure",
        "verification_closure",
        "consistency",
        "handoff_approval",
    }
    if set(gates) != expected_gates:
        errors.append("handoff/readiness.yaml: gate set is incomplete or unexpected")
    current_hash = content_hash(root)
    if build_ready:
        for gate_name in sorted(expected_gates):
            gate = gates.get(gate_name) or {}
            if not gate.get("passed"):
                errors.append(f"Build-ready package has failed readiness gate: {gate_name}")
            if not gate.get("evidence_refs"):
                errors.append(f"Readiness gate {gate_name} requires evidence_refs")
        final_decision = readiness.get("final_approval_decision_id")
        require_confirmed_decision(
            final_decision, confirmed_decision_ids, "Final handoff approval", errors
        )
        validator_record = readiness.get("validator") or {}
        if not validator_record.get("command") or not validator_record.get("passed"):
            errors.append("Build-ready package requires a recorded passing validator command")
        if readiness.get("package_hash") != current_hash:
            errors.append("Build-ready package_hash does not match current content hash; restamp package")

    placeholder_hits: list[str] = []
    for path in iter_text_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        match = PLACEHOLDER_RE.search(text)
        if match:
            placeholder_hits.append(f"{match.group(0)!r} in {rel(root, path)}")
    if placeholder_hits:
        message = "Placeholders remain: " + "; ".join(placeholder_hits)
        if build_ready:
            errors.append(message)
        else:
            warnings.append(message)

    report = {
        "root": str(root),
        "build_ready_declared": build_ready,
        "artifact_count": len(artifacts),
        "registered_id_count": len(artifacts),
        "found_id_count": len(found_artifact_ids),
        "journey_count": journey_counts.get("journey_count", 0),
        "phase_count": journey_counts.get("phase_count", 0),
        "action_count": journey_counts.get("action_count", 0),
        "uncovered_in_scope_actor_count": journey_counts.get(
            "uncovered_in_scope_actor_count", 0
        ),
        "in_scope_capability_count": len(in_scope_ids),
        "acceptance_scenario_count": len(acceptance_ids),
        "open_question_count": len(open_questions),
        "open_contradiction_count": len(open_contradictions),
        "stale_artifact_count": sum(1 for a in artifacts.values() if a.get("stale")),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "content_hash": current_hash,
    }
    return errors, warnings, report


def write_reports(root: Path, errors: list[str], warnings: list[str], report: dict[str, Any]) -> None:
    handoff = root / "handoff"
    if handoff.is_symlink() or not handoff.is_dir():
        raise ValueError("handoff must be a regular directory inside the package")
    yaml_path = handoff / "readiness-report.generated.yaml"
    md_path = handoff / "readiness-report.generated.md"
    for path in (yaml_path, md_path):
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise ValueError(f"Report path must be a regular file: {path}")
    write_yaml(yaml_path, {**report, "errors": errors, "warnings": warnings})

    lines = [
        "# Product Intent Readiness Report",
        "",
        f"- Result: **{'PASS' if not errors else 'FAIL'}**",
        f"- Declared build-ready: `{report.get('build_ready_declared')}`",
        f"- Artifacts: `{report.get('artifact_count')}`",
        f"- Lifecycle journeys: `{report.get('journey_count')}`",
        f"- Journey phases: `{report.get('phase_count')}`",
        f"- Journey actions: `{report.get('action_count')}`",
        f"- Uncovered in-scope actors: `{report.get('uncovered_in_scope_actor_count')}`",
        f"- In-scope capabilities: `{report.get('in_scope_capability_count')}`",
        f"- Acceptance scenarios: `{report.get('acceptance_scenario_count')}`",
        f"- Open questions: `{report.get('open_question_count')}`",
        f"- Open contradictions: `{report.get('open_contradiction_count')}`",
        f"- Stale artifacts: `{report.get('stale_artifact_count')}`",
        f"- Content hash: `{report.get('content_hash')}`",
        "",
        "## Errors",
        "",
    ]
    lines.extend([f"- {error}" for error in errors] or ["- None"])
    lines += ["", "## Warnings", ""]
    lines.extend([f"- {warning}" for warning in warnings] or ["- None"])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path)
    parser.add_argument("--no-report", action="store_true")
    args = parser.parse_args()

    if args.package.is_symlink():
        errors, warnings, report = validate(args.package)
        print(dump_yaml({**report, "errors": errors, "warnings": warnings}), end="")
        return 1

    root = args.package.resolve()
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 2

    package_has_symlinks = bool(find_package_symlinks(root))
    errors, warnings, report = validate(root)
    if not args.no_report and not package_has_symlinks:
        write_reports(root, errors, warnings, report)

    print(dump_yaml({**report, "errors": errors, "warnings": warnings}), end="")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
