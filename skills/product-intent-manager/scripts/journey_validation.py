"""Validation for first-class Product Intent lifecycle journey maps."""

from __future__ import annotations

import re
import stat
from pathlib import Path
from typing import Any, Optional


JOURNEY_TYPES = {
    "customer_relationship",
    "job_task",
    "operational_case",
    "entity_asset",
    "developer_integration",
    "ecosystem_marketplace",
    "service_blueprint",
    "custom",
}
TARGET_VIEWS = {"as_observed", "intended_current", "target_next"}
INTENT_STATUSES = {"observed", "inferred", "proposed", "confirmed"}
STRUCTURAL_VARIANTS = {"single_actor", "role_specific", "multi_actor_coordinated"}
LIFECYCLE_DECISION_DOMAINS = {"product_strategy", "capabilities_and_behavior"}
TIME_AXES = {
    "relationship",
    "task",
    "operation",
    "entity_lifecycle",
    "integration",
    "service_delivery",
    "ecosystem_participation",
}
TOPOLOGIES = {"linear", "cyclical", "branching", "state_based", "recurring", "nested"}
COVERAGE_STATUSES = {"covered", "not_applicable", "out_of_scope", "blocked"}
EXCEPTION_KEYS = {"failure", "pause_resume", "abandonment", "exit", "recovery"}
INTENT_ITEM_TYPES = {"evidence", "assumption", "decision", "question", "contradiction"}
DETAILED_EXPERIENCE_KINDS = {"flow", "screen", "mockup", "component"}
RESPONSE_KINDS = {"flow", "rule", "state_machine", "decision_table"}
EXCEPTION_COVERAGE_KINDS = {
    "flow",
    "rule",
    "state_machine",
    "decision_table",
    "screen",
    "api_contract",
    "event_contract",
    "sequence",
    "acceptance_scenario",
}
SOURCE_PART_RE = re.compile(r"^JOURNEY-[0-9]{3,}\.(?:phase|action)-[0-9]{2,}$")
JOURNEY_ID_RE = re.compile(r"^JOURNEY-[0-9]{3,}$")
MERMAID_FENCE_RE = re.compile(r"(?ms)^```mermaid[ \t]*\n.*?^```[ \t]*(?:\n|$)")
LIFECYCLE_TABLE_RE = re.compile(
    r"(?ims)^\s*\|[^\n]*\b(?:phase|stage)\b[^\n]*\|\s*\n"
    r"\s*\|\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|\s*\n"
    r"(?:\s*\|[^\n]*\|\s*(?:\n|$))+"
)


def _has_lane_table(text: str) -> bool:
    required_lanes = {"actor goal", "actor action", "product response"}
    lines = text.splitlines()
    for index, line in enumerate(lines[:-1]):
        header = [cell.strip().casefold() for cell in line.strip().strip("|").split("|")]
        if len(header) < 2 or header[0] != "lane":
            continue
        separator = [cell.strip() for cell in lines[index + 1].strip().strip("|").split("|")]
        if len(separator) != len(header) or not all(
            re.fullmatch(r":?-{3,}:?", cell) for cell in separator
        ):
            continue
        lane_names: set[str] = set()
        for row in lines[index + 2 :]:
            if not row.strip().startswith("|"):
                break
            cells = [cell.strip().casefold() for cell in row.strip().strip("|").split("|")]
            if cells:
                lane_names.add(cells[0])
        if required_lanes <= lane_names:
            return True
    return False


def _mapping(value: Any, context: str, errors: list[str]) -> Optional[dict[str, Any]]:
    if not isinstance(value, dict):
        errors.append(f"{context}: must be a mapping")
        return None
    return value


def _records(value: Any, context: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{context}: must be a list")
        return []
    return value


def _list_value(value: Any) -> list[Any]:
    """Return a collection only when the input is a list."""
    return value if isinstance(value, list) else []


def _required(value: dict[str, Any], field: str, context: str, errors: list[str]) -> Any:
    if field not in value or value[field] is None:
        errors.append(f"{context}: requires {field}")
        return None
    return value[field]


def _nonempty(value: Any, context: str, errors: list[str]) -> bool:
    if value in (None, "", [], {}):
        errors.append(f"{context}: must not be empty")
        return False
    return True


def _text(value: Any, context: str, errors: list[str]) -> bool:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{context}: must be a non-empty string")
        return False
    return True


def _id_list(value: Any, context: str, errors: list[str]) -> list[str]:
    values = _records(value, context, errors)
    result: list[str] = []
    for index, item in enumerate(values):
        if not isinstance(item, str) or not item:
            errors.append(f"{context}[{index}]: must be a non-empty ID string")
        else:
            result.append(item)
    if len(result) != len(set(result)):
        errors.append(f"{context}: contains duplicate IDs")
    return result


def _validate_lifecycle_decision_scope(
    decision_id: Any,
    decision_map: dict[str, dict[str, Any]],
    affected_ids: set[str],
    context: str,
    label: str,
    affected_label: str,
    required_authority_id: Optional[str],
    errors: list[str],
) -> bool:
    if not isinstance(decision_id, str):
        return False
    decision = decision_map.get(decision_id)
    if decision is None:
        return False
    valid = True
    domain = decision.get("domain")
    if not isinstance(domain, str) or domain not in LIFECYCLE_DECISION_DOMAINS:
        errors.append(
            f"{context}: {label} domain must be product_strategy or "
            "capabilities_and_behavior"
        )
        valid = False
    decision_affects = {
        value for value in _list_value(decision.get("affects")) if isinstance(value, str)
    }
    if not affected_ids & decision_affects:
        errors.append(f"{context}: {label} must affect {affected_label}")
        valid = False
    if (
        required_authority_id is not None
        and decision.get("authority_id") != required_authority_id
    ):
        errors.append(f"{context}: {label} authority must match journey authority")
        valid = False
    return valid


def _check_ref(
    ref_id: Any,
    context: str,
    artifacts: dict[str, dict[str, Any]],
    errors: list[str],
    *,
    kinds: Optional[set[str]] = None,
    build_ready: bool = False,
) -> None:
    if not isinstance(ref_id, str) or not ref_id:
        errors.append(f"{context}: requires an artifact ID")
        return
    artifact = artifacts.get(ref_id)
    if artifact is None:
        errors.append(f"{context}: unknown artifact {ref_id}")
        return
    artifact_kind = artifact.get("kind")
    if kinds is not None and (
        not isinstance(artifact_kind, str) or artifact_kind not in kinds
    ):
        errors.append(
            f"{context}: {ref_id} must reference one of {', '.join(sorted(kinds))}"
        )
    if build_ready and artifact.get("status") != "confirmed":
        errors.append(f"{context}: linked artifact {ref_id} is not confirmed")
    if build_ready and artifact.get("stale"):
        errors.append(f"{context}: linked artifact {ref_id} is stale")


def _source_path(root: Path, value: Any, context: str, errors: list[str]) -> Optional[Path]:
    if not isinstance(value, str) or not value:
        errors.append(f"{context}: source_path is required")
        return None
    declared = Path(value)
    if declared.is_absolute() or ".." in declared.parts:
        errors.append(f"{context}: source_path must stay inside package: {value}")
        return None
    if declared.suffix.lower() != ".md":
        errors.append(f"{context}: source_path must be an editable Markdown .md file")
        return None
    declared_candidate = root / declared
    try:
        declared_is_symlink = declared_candidate.is_symlink()
    except OSError as exc:
        errors.append(f"{context}: source_path cannot be resolved: {exc}")
        return None
    if declared_is_symlink:
        try:
            resolved_link = declared_candidate.resolve()
        except (OSError, RuntimeError) as exc:
            errors.append(f"{context}: source_path cannot be resolved: {exc}")
            return None
        try:
            resolved_link.relative_to(root.resolve())
        except ValueError:
            errors.append(f"{context}: source_path must stay inside package: {value}")
        else:
            errors.append(f"{context}: source_path must be a regular Markdown file")
        return None
    try:
        candidate = (root / declared).resolve()
    except (OSError, RuntimeError) as exc:
        errors.append(f"{context}: source_path cannot be resolved: {exc}")
        return None
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        errors.append(f"{context}: source_path must stay inside package: {value}")
        return None
    try:
        source_stat = candidate.stat()
    except OSError:
        errors.append(f"{context}: source_path does not exist: {value}")
        return None
    if not stat.S_ISREG(source_stat.st_mode) or candidate.is_symlink():
        errors.append(f"{context}: source_path must be a regular Markdown file")
        return None
    try:
        text = candidate.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"{context}: source_path cannot be read: {exc}")
        return None
    if not (
        MERMAID_FENCE_RE.search(text)
        or LIFECYCLE_TABLE_RE.search(text)
        or _has_lane_table(text)
    ):
        errors.append(
            f"{context}: source_path must contain a fenced mermaid block or lifecycle table"
        )
    return candidate


def _validate_intent_items(
    values: Any,
    context: str,
    evidence_ids: set[str],
    decision_ids: set[str],
    confirmed_decision_ids: set[str],
    question_ids: set[str],
    contradiction_ids: set[str],
    build_ready: bool,
    errors: list[str],
) -> None:
    items = _records(values, context, errors)
    ref_sets = {
        "evidence": evidence_ids,
        "decision": decision_ids,
        "question": question_ids,
        "contradiction": contradiction_ids,
    }
    for index, raw_item in enumerate(items):
        item_context = f"{context}[{index}]"
        item = _mapping(raw_item, item_context, errors)
        if item is None:
            continue
        item_type = item.get("type")
        if not isinstance(item_type, str) or item_type not in INTENT_ITEM_TYPES:
            errors.append(f"{item_context}: invalid type {item_type!r}")
            continue
        if item_type == "assumption":
            if not _nonempty(item.get("statement"), item_context + ".statement", errors):
                continue
            if build_ready:
                errors.append(f"{item_context}: contains unresolved assumption")
            continue
        ref_id = item.get("ref_id")
        if ref_id is None and item_type == "evidence":
            legacy_refs = item.get("evidence_refs")
            if isinstance(legacy_refs, list) and len(legacy_refs) == 1:
                ref_id = legacy_refs[0]
        if ref_id is None and item_type == "decision":
            ref_id = item.get("decision_id")
        if not isinstance(ref_id, str) or ref_id not in ref_sets[item_type]:
            errors.append(f"{item_context}: {item_type} requires a matching ledger ref_id")
        if build_ready and item_type == "decision" and ref_id not in confirmed_decision_ids:
            errors.append(f"{item_context}: build-ready decision must be confirmed")
        if build_ready and item_type in {"question", "contradiction"}:
            errors.append(f"{item_context}: contains unresolved {item_type}")


def _validate_exception_coverage(
    value: Any,
    context: str,
    journey_id: str,
    journey_authority_id: Optional[str],
    phase_ids: set[str],
    qualified_targets_by_phase: dict[str, set[str]],
    artifacts: dict[str, dict[str, Any]],
    confirmed_decision_ids: set[str],
    decision_map: dict[str, dict[str, Any]],
    build_ready: bool,
    errors: list[str],
) -> None:
    coverage = _mapping(value, context, errors)
    if coverage is None:
        return
    if set(coverage) != EXCEPTION_KEYS:
        errors.append(
            f"{context} must contain exactly: {', '.join(sorted(EXCEPTION_KEYS))}"
        )
    for name in sorted(EXCEPTION_KEYS & set(coverage)):
        entry_context = f"{context}.{name}"
        entry = _mapping(coverage.get(name), entry_context, errors)
        if entry is None:
            continue
        status = entry.get("status", entry.get("coverage", entry.get("disposition")))
        if not isinstance(status, str) or status not in COVERAGE_STATUSES:
            errors.append(f"{entry_context}: invalid status {status!r}")
            continue
        if status == "covered":
            listed_phase_ids = _id_list(entry.get("phase_ids"), entry_context + ".phase_ids", errors)
            if not listed_phase_ids:
                errors.append(f"{entry_context}: covered requires non-empty phase_ids")
            for phase_id in listed_phase_ids:
                if phase_id not in phase_ids:
                    errors.append(f"{entry_context}: unknown phase_id {phase_id}")
            listed_artifacts = _id_list(
                entry.get("artifact_ids"), entry_context + ".artifact_ids", errors
            )
            if not listed_artifacts:
                errors.append(f"{entry_context}: covered requires non-empty artifact_ids")
            for artifact_id in listed_artifacts:
                _check_ref(
                    artifact_id,
                    entry_context + ".artifact_ids",
                    artifacts,
                    errors,
                    build_ready=build_ready,
                )
            detailed_artifact_ids = {
                artifact_id
                for artifact_id in listed_artifacts
                if artifact_id in artifacts
                and artifacts[artifact_id].get("kind") in EXCEPTION_COVERAGE_KINDS
            }
            if not detailed_artifact_ids:
                errors.append(
                    f"{entry_context}: covered requires a behavior or verification artifact"
                )
            elif not any(
                detailed_artifact_ids & qualified_targets_by_phase.get(phase_id, set())
                for phase_id in listed_phase_ids
            ):
                errors.append(
                    f"{entry_context}: covered artifact requires a qualified link "
                    "from a listed phase or action"
                )
        elif status in {"not_applicable", "out_of_scope"}:
            decision_id = entry.get("decision_id")
            if not isinstance(decision_id, str) or decision_id not in confirmed_decision_ids:
                errors.append(f"{entry_context}: exclusion requires a confirmed decision ID")
            else:
                _validate_lifecycle_decision_scope(
                    decision_id,
                    decision_map,
                    {journey_id},
                    entry_context,
                    "exception exclusion decision",
                    "the journey",
                    journey_authority_id,
                    errors,
                )
        elif build_ready:
            errors.append(f"{entry_context}: blocked coverage is not build-ready")


def _validate_journey(
    root: Path,
    raw_journey: Any,
    index: int,
    artifacts: dict[str, dict[str, Any]],
    evidence_ids: set[str],
    decision_ids: set[str],
    confirmed_decision_ids: set[str],
    decision_map: dict[str, dict[str, Any]],
    question_ids: set[str],
    contradiction_ids: set[str],
    build_ready: bool,
    errors: list[str],
) -> tuple[Optional[dict[str, Any]], set[str], set[str]]:
    context = f"experience/journeys/index.yaml: journeys[{index}]"
    journey = _mapping(raw_journey, context, errors)
    if journey is None:
        return None, set(), set()

    journey_id = journey.get("id")
    if not isinstance(journey_id, str) or not JOURNEY_ID_RE.fullmatch(journey_id):
        errors.append(f"{context}: id must match JOURNEY-###")
        journey_id = f"<journey-{index}>"
    required_fields = (
        "id",
        "title",
        "journey_type",
        "type_rationale",
        "structural_variant",
        "status",
        "actor_ids",
        "scope",
        "target_view",
        "intent_status",
        "initiating_trigger",
        "desired_outcome",
        "success_conditions",
        "terminal_conditions",
        "time_axis",
        "topology",
        "recurrence_model",
        "authority_id",
        "confirmation_decision_id",
        "source_refs",
        "version",
        "source_path",
        "capability_ids",
        "exception_coverage",
        "phases",
        "transitions",
    )
    for field in required_fields:
        _required(journey, field, context, errors)

    journey_type = journey.get("journey_type")
    if not isinstance(journey_type, str) or journey_type not in JOURNEY_TYPES:
        errors.append(f"{context}: invalid journey_type {journey_type!r}")
    _text(journey.get("type_rationale"), context + ".type_rationale", errors)
    structural_variant = journey.get("structural_variant")
    if not isinstance(structural_variant, str) or structural_variant not in STRUCTURAL_VARIANTS:
        errors.append(f"{context}: invalid structural_variant {structural_variant!r}")
    target_view = journey.get("target_view")
    if not isinstance(target_view, str) or target_view not in TARGET_VIEWS:
        errors.append(f"{context}: invalid target_view {target_view!r}")
    intent_status = journey.get("intent_status")
    if not isinstance(intent_status, str) or intent_status not in INTENT_STATUSES:
        errors.append(f"{context}: invalid intent_status {intent_status!r}")
    if not isinstance(journey.get("status"), str) or not journey.get("status"):
        errors.append(f"{context}: status must be a non-empty artifact status")
    time_axis = journey.get("time_axis")
    if not isinstance(time_axis, str) or time_axis not in TIME_AXES:
        errors.append(f"{context}: invalid time_axis {time_axis!r}")
    topology = journey.get("topology")
    topology_values = _id_list(topology, context + ".topology", errors)
    if not topology_values:
        errors.append(f"{context}.topology: must contain at least one topology")
    for topology_value in topology_values:
        if topology_value not in TOPOLOGIES:
            errors.append(f"{context}.topology: invalid topology {topology_value!r}")
    for field in (
        "title",
        "initiating_trigger",
        "desired_outcome",
        "recurrence_model",
    ):
        _text(journey.get(field), context + "." + field, errors)
    for field in ("scope", "success_conditions", "terminal_conditions"):
        _nonempty(journey.get(field), context + "." + field, errors)

    actor_ids = _id_list(journey.get("actor_ids"), context + ".actor_ids", errors)
    if structural_variant == "single_actor" and len(actor_ids) != 1:
        errors.append(f"{context}: single_actor requires exactly one actor_id")
    if structural_variant in {"role_specific", "multi_actor_coordinated"} and len(
        actor_ids
    ) < 2:
        errors.append(
            f"{context}: {structural_variant} requires at least two actor_ids"
        )
    capability_ids = _id_list(journey.get("capability_ids"), context + ".capability_ids", errors)
    source_refs = _id_list(journey.get("source_refs"), context + ".source_refs", errors)
    for field, values in (
        ("actor_ids", actor_ids),
        ("capability_ids", capability_ids),
        ("source_refs", source_refs),
    ):
        if not values:
            errors.append(f"{context}.{field}: must contain at least one ID")
    for source_ref in source_refs:
        if source_ref not in evidence_ids:
            errors.append(f"{context}: unknown evidence source_ref {source_ref}")
    for authority_field in ("authority_id", "confirmation_decision_id"):
        if not isinstance(journey.get(authority_field), str) or not journey.get(authority_field):
            errors.append(f"{context}: {authority_field} must be a non-empty ID")
    confirmation_decision_id = journey.get("confirmation_decision_id")
    if isinstance(confirmation_decision_id, str):
        if intent_status == "confirmed" or build_ready:
            if confirmation_decision_id not in confirmed_decision_ids:
                errors.append(f"{context}: confirmation_decision_id must be confirmed")
        elif confirmation_decision_id not in decision_ids:
            errors.append(f"{context}: confirmation_decision_id must reference a decision")
        decision = decision_map.get(confirmation_decision_id)
        if decision is not None and decision.get("authority_id") != journey.get("authority_id"):
            errors.append(
                f"{context}: confirmation decision authority must match journey authority"
            )
        _validate_lifecycle_decision_scope(
            confirmation_decision_id,
            decision_map,
            {journey_id},
            context,
            "confirmation decision",
            "the journey",
            None,
            errors,
        )
    if not isinstance(journey.get("version"), int) or journey.get("version", 0) < 1:
        errors.append(f"{context}: version must be a positive integer")
    _source_path(root, journey.get("source_path"), context, errors)

    phases = _records(journey.get("phases"), context + ".phases", errors)
    phase_ids: set[str] = set()
    ordered_phase_ids: list[str] = []
    action_ids: set[str] = set()
    qualified_targets_by_phase: dict[str, set[str]] = {}
    for phase_index, raw_phase in enumerate(phases):
        phase_context = f"{context}.phases[{phase_index}]"
        phase = _mapping(raw_phase, phase_context, errors)
        if phase is None:
            continue
        for field in (
            "id",
            "name",
            "product_scope",
            "actor_goal",
            "entry_conditions",
            "exit_conditions",
            "touchpoint_ids",
            "actions",
            "state_data_event_ids",
            "exceptions_recovery",
            "intent_items",
            "linked_artifacts",
        ):
            _required(phase, field, phase_context, errors)
        phase_id = phase.get("id")
        expected_phase_id = (
            isinstance(journey_id, str)
            and re.fullmatch(re.escape(journey_id) + r"\.phase-[0-9]{2,}", str(phase_id))
        )
        if not expected_phase_id:
            errors.append(f"{phase_context}: id must be a local {journey_id}.phase-## ID")
        elif phase_id in phase_ids:
            errors.append(f"{phase_context}: duplicate phase ID {phase_id}")
        else:
            phase_ids.add(phase_id)
            ordered_phase_ids.append(phase_id)
        product_scope = phase.get("product_scope")
        if not isinstance(product_scope, str) or product_scope not in {
            "inside",
            "outside",
            "partial",
        }:
            errors.append(f"{phase_context}: invalid product_scope")
        for field in ("name", "actor_goal"):
            _text(phase.get(field), phase_context + "." + field, errors)
        for field in ("entry_conditions", "exit_conditions", "exceptions_recovery"):
            _nonempty(phase.get(field), phase_context + "." + field, errors)
        touchpoint_ids = _id_list(phase.get("touchpoint_ids"), phase_context + ".touchpoint_ids", errors)
        for touchpoint_id in touchpoint_ids:
            _check_ref(
                touchpoint_id,
                phase_context + ".touchpoint_ids",
                artifacts,
                errors,
                build_ready=build_ready,
            )
        state_data_event_ids = _id_list(
            phase.get("state_data_event_ids"), phase_context + ".state_data_event_ids", errors
        )
        for state_data_event_id in state_data_event_ids:
            _check_ref(
                state_data_event_id,
                phase_context + ".state_data_event_ids",
                artifacts,
                errors,
                build_ready=build_ready,
            )
        _validate_intent_items(
            phase.get("intent_items"),
            phase_context + ".intent_items",
            evidence_ids,
            decision_ids,
            confirmed_decision_ids,
            question_ids,
            contradiction_ids,
            build_ready,
            errors,
        )
        linked_artifacts = _records(
            phase.get("linked_artifacts"), phase_context + ".linked_artifacts", errors
        )
        linked_source_parts: list[tuple[str, str]] = []
        linked_artifact_ids_by_source: dict[str, set[str]] = {}
        for linked_index, raw_link in enumerate(linked_artifacts):
            link_context = f"{phase_context}.linked_artifacts[{linked_index}]"
            link = _mapping(raw_link, link_context, errors)
            if link is None:
                continue
            for field in ("id", "relation", "source_part_id"):
                _required(link, field, link_context, errors)
            _check_ref(
                link.get("id"),
                link_context,
                artifacts,
                errors,
                build_ready=build_ready,
            )
            if link.get("relation") is None or not isinstance(link.get("relation"), str):
                errors.append(f"{link_context}: relation must be a string")
            source_part_id = link.get("source_part_id")
            if not isinstance(source_part_id, str) or not source_part_id:
                errors.append(f"{link_context}: source_part_id must be a non-empty string")
            elif not SOURCE_PART_RE.fullmatch(source_part_id):
                errors.append(f"{link_context}: source_part_id must be a local journey ID")
            else:
                linked_source_parts.append((link_context, source_part_id))
                linked_artifact_id = link.get("id")
                if isinstance(linked_artifact_id, str):
                    linked_artifact_ids_by_source.setdefault(source_part_id, set()).add(
                        linked_artifact_id
                    )

        actions = _records(phase.get("actions"), phase_context + ".actions", errors)
        phase_action_ids: set[str] = set()
        for action_index, raw_action in enumerate(actions):
            action_context = f"{phase_context}.actions[{action_index}]"
            action = _mapping(raw_action, action_context, errors)
            if action is None:
                continue
            for field in ("id", "actor_action", "product_response"):
                _required(action, field, action_context, errors)
            if "response_artifact_ids" not in action:
                errors.append(f"{action_context}: requires response_artifact_ids")
            action_id = action.get("id")
            expected_action_id = (
                isinstance(journey_id, str)
                and re.fullmatch(re.escape(journey_id) + r"\.action-[0-9]{2,}", str(action_id))
            )
            if not expected_action_id:
                errors.append(f"{action_context}: id must be a local {journey_id}.action-## ID")
            elif action_id in action_ids:
                errors.append(f"{action_context}: duplicate action ID {action_id}")
            else:
                action_ids.add(action_id)
                phase_action_ids.add(action_id)
            _text(action.get("actor_action"), action_context + ".actor_action", errors)
            _text(action.get("product_response"), action_context + ".product_response", errors)
            response_ids = _id_list(
                action.get("response_artifact_ids"),
                action_context + ".response_artifact_ids",
                errors,
            )
            for response_id in response_ids:
                _check_ref(
                    response_id,
                    action_context + ".response_artifact_ids",
                    artifacts,
                    errors,
                    build_ready=build_ready,
                )
            exception_decision = action.get("response_exception_decision_id")
            valid_exception_decision = (
                isinstance(exception_decision, str)
                and exception_decision in confirmed_decision_ids
            )
            if exception_decision is not None and not valid_exception_decision:
                errors.append(
                    f"{action_context}: response_exception_decision_id must be confirmed"
                )
            if valid_exception_decision:
                _validate_lifecycle_decision_scope(
                    exception_decision,
                    decision_map,
                    {journey_id},
                    action_context,
                    "response exception decision",
                    "the journey",
                    journey.get("authority_id")
                    if isinstance(journey.get("authority_id"), str)
                    else None,
                    errors,
                )
            response_kinds = {
                artifacts[response_id].get("kind")
                for response_id in response_ids
                if response_id in artifacts
            }
            if not response_kinds & RESPONSE_KINDS and not valid_exception_decision:
                errors.append(
                    f"{action_context}: product response requires a linked behavior artifact"
                )
            if isinstance(action_id, str):
                missing_response_links = set(response_ids) - linked_artifact_ids_by_source.get(
                    action_id, set()
                )
                if missing_response_links and not valid_exception_decision:
                    errors.append(
                        f"{action_context}: response_artifact_ids require same-action "
                        "linked_artifacts entries: "
                        + ", ".join(sorted(missing_response_links))
                    )

        for link_context, source_part_id in linked_source_parts:
            if source_part_id != phase_id and source_part_id not in phase_action_ids:
                errors.append(
                    f"{link_context}: source_part_id must belong to the enclosing phase"
                )

        if isinstance(phase_id, str) and phase_id in phase_ids:
            phase_targets = qualified_targets_by_phase.setdefault(phase_id, set())
            for source_part_id in {phase_id} | phase_action_ids:
                phase_targets.update(
                    linked_artifact_ids_by_source.get(source_part_id, set())
                )

        if build_ready and isinstance(product_scope, str) and product_scope in {
            "inside",
            "partial",
        }:
            if not actions:
                errors.append(
                    f"{phase_context}: build-ready in-scope phase requires at least one action"
                )
            intent_items = _list_value(phase.get("intent_items"))
            if not any(
                isinstance(item, dict)
                and isinstance(item.get("type"), str)
                and item.get("type") in INTENT_ITEM_TYPES
                for item in intent_items
            ):
                errors.append(
                    f"{phase_context}: build-ready in-scope phase requires at least one intent item"
                )
            if not linked_artifacts:
                errors.append(
                    f"{phase_context}: build-ready in-scope phase requires linked artifacts"
                )

    transitions = _records(journey.get("transitions"), context + ".transitions", errors)
    if not phase_ids:
        errors.append(f"{context}: journey requires at least one phase")
    if len(phase_ids) > 1 and not transitions:
        errors.append(f"{context}: journeys with multiple phases require transitions")
    adjacency = {phase_id: set() for phase_id in phase_ids}
    outgoing_transition_counts = {phase_id: 0 for phase_id in phase_ids}
    for transition_index, raw_transition in enumerate(transitions):
        transition_context = f"{context}.transitions[{transition_index}]"
        transition = _mapping(raw_transition, transition_context, errors)
        if transition is None:
            continue
        for field in ("from_phase_id", "to_phase_id", "condition", "complex"):
            _required(transition, field, transition_context, errors)
        if "flow_ids" not in transition:
            errors.append(f"{transition_context}: requires flow_ids")
        from_phase_id = transition.get("from_phase_id")
        to_phase_id = transition.get("to_phase_id")
        for field, value in (
            ("from_phase_id", from_phase_id),
            ("to_phase_id", to_phase_id),
        ):
            if not isinstance(value, str) or value not in phase_ids:
                errors.append(f"{transition_context}: unknown {field} {value!r}")
        if (
            isinstance(from_phase_id, str)
            and from_phase_id in phase_ids
            and isinstance(to_phase_id, str)
            and to_phase_id in phase_ids
        ):
            adjacency[from_phase_id].add(to_phase_id)
            outgoing_transition_counts[from_phase_id] += 1
        _text(transition.get("condition"), transition_context + ".condition", errors)
        if not isinstance(transition.get("complex"), bool):
            errors.append(f"{transition_context}: complex must be true or false")
        flow_ids = _id_list(transition.get("flow_ids"), transition_context + ".flow_ids", errors)
        for flow_id in flow_ids:
            _check_ref(flow_id, transition_context + ".flow_ids", artifacts, errors, kinds={"flow"}, build_ready=build_ready)
        if transition.get("complex") is True and not flow_ids:
            errors.append(f"{transition_context}: complex transition requires flow_ids")

    if ordered_phase_ids:
        reachable = {ordered_phase_ids[0]}
        pending = [ordered_phase_ids[0]]
        while pending:
            current = pending.pop()
            for target in adjacency.get(current, set()) - reachable:
                reachable.add(target)
                pending.append(target)
        unreachable = sorted(phase_ids - reachable)
        if unreachable:
            errors.append(f"{context}: unreachable phase IDs: {', '.join(unreachable)}")

    indegree = {phase_id: 0 for phase_id in phase_ids}
    for targets in adjacency.values():
        for target in targets:
            indegree[target] += 1
    acyclic_pending = [
        phase_id for phase_id, count in indegree.items() if count == 0
    ]
    acyclic_count = 0
    while acyclic_pending:
        current = acyclic_pending.pop()
        acyclic_count += 1
        for target in adjacency.get(current, set()):
            indegree[target] -= 1
            if indegree[target] == 0:
                acyclic_pending.append(target)
    has_directed_cycle = bool(phase_ids) and acyclic_count < len(phase_ids)
    for topology_value in sorted({"cyclical", "recurring"} & set(topology_values)):
        if not has_directed_cycle:
            errors.append(
                f"{context}: {topology_value} topology requires a directed cycle"
            )
    if "branching" in topology_values and not any(
        count >= 2 for count in outgoing_transition_counts.values()
    ):
        errors.append(
            f"{context}: branching topology requires two outgoing transitions "
            "from one phase"
        )

    _validate_exception_coverage(
        journey.get("exception_coverage"),
        context + ".exception_coverage",
        journey_id,
        journey.get("authority_id")
        if isinstance(journey.get("authority_id"), str)
        else None,
        phase_ids,
        qualified_targets_by_phase,
        artifacts,
        confirmed_decision_ids,
        decision_map,
        build_ready,
        errors,
    )
    if (
        build_ready
        and isinstance(intent_status, str)
        and intent_status in {"observed", "inferred", "proposed"}
    ):
        errors.append(f"{context}: build-ready journey must be confirmed (intent_status)")

    return journey, phase_ids, action_ids


def validate_lifecycle_journeys(
    root: Path,
    registry: Any,
    artifacts: dict[str, dict[str, Any]],
    evidence_ids: set[str],
    decision_ids: set[str],
    confirmed_decision_ids: set[str],
    decision_map: dict[str, dict[str, Any]],
    question_ids: set[str],
    contradiction_ids: set[str],
    actor_ids: set[str],
    capability_map: dict[str, dict[str, Any]],
    in_scope_capability_ids: list[str],
    trace_edges: list[dict[str, Any]],
    build_ready: bool,
    errors: list[str],
) -> dict[str, int]:
    """Validate the journey registry and return counts for the readiness report."""
    context = "experience/journeys/index.yaml"
    registry_map = _mapping(registry, context, errors)
    if registry_map is None:
        return {
            "journey_count": 0,
            "phase_count": 0,
            "action_count": 0,
            "uncovered_in_scope_actor_count": 0,
        }
    raw_journeys = _records(registry_map.get("journeys"), context + ".journeys", errors)
    raw_coverage = _records(registry_map.get("actor_coverage"), context + ".actor_coverage", errors)

    journeys: dict[str, dict[str, Any]] = {}
    journey_parts: dict[str, set[str]] = {}
    phase_count = 0
    action_count = 0
    for index, raw_journey in enumerate(raw_journeys):
        journey, phase_ids, action_ids = _validate_journey(
            root,
            raw_journey,
            index,
            artifacts,
            evidence_ids,
            decision_ids,
            confirmed_decision_ids,
            decision_map,
            question_ids,
            contradiction_ids,
            build_ready,
            errors,
        )
        if journey is None:
            continue
        journey_id = journey.get("id")
        phase_count += len(phase_ids)
        action_count += len(action_ids)
        if not isinstance(journey_id, str) or not JOURNEY_ID_RE.fullmatch(journey_id):
            continue
        if journey_id in journeys:
            errors.append(f"{context}: duplicate journey ID {journey_id}")
        else:
            journeys[journey_id] = journey
            journey_parts[journey_id] = phase_ids | action_ids

        artifact = artifacts.get(journey_id)
        if artifact is None:
            errors.append(f"{journey_id}: missing artifact-index record")
        else:
            for field in ("authority_id", "confirmation_decision_id", "version"):
                if artifact.get(field) != journey.get(field):
                    errors.append(
                        f"{journey_id}: {field} does not match artifact-index record"
                    )
            if artifact.get("status") != journey.get("status"):
                errors.append(f"{journey_id}: status must match artifact index")
            expected_path = f"experience/journeys/index.yaml#/journeys/{index}"
            if artifact.get("path") != expected_path:
                errors.append(
                    f"{journey_id}: artifact path must match journey registry slot {expected_path}"
                )
            if build_ready and (artifact.get("status") != "confirmed" or artifact.get("stale")):
                errors.append(f"{journey_id}: build-ready journey artifact must be confirmed and current")

        for actor_id in (
            value for value in _list_value(journey.get("actor_ids")) if isinstance(value, str)
        ):
            if actor_id not in actor_ids:
                errors.append(f"{journey_id}: references unknown actor_id {actor_id}")
            _check_ref(
                actor_id,
                f"{journey_id}.actor_ids",
                artifacts,
                errors,
                kinds={"actor"},
                build_ready=build_ready,
            )
        for capability_id in (
            value
            for value in _list_value(journey.get("capability_ids"))
            if isinstance(value, str)
        ):
            if capability_id not in capability_map:
                errors.append(f"{journey_id}: references unknown capability_id {capability_id}")
            _check_ref(
                capability_id,
                f"{journey_id}.capability_ids",
                artifacts,
                errors,
                kinds={"capability"},
                build_ready=build_ready,
            )

    indexed_journey_ids = {
        artifact_id
        for artifact_id, artifact in artifacts.items()
        if artifact.get("kind") == "lifecycle_journey"
    }
    for artifact_id in sorted(indexed_journey_ids - set(journeys)):
        errors.append(
            f"{artifact_id}: lifecycle journey artifact has no journey registry record"
        )

    required_actor_ids: set[str] = set()
    for capability_id in in_scope_capability_ids:
        capability = capability_map.get(capability_id) or {}
        required_actor_ids.update(
            actor_id
            for actor_id in _list_value(capability.get("actor_ids"))
            if isinstance(actor_id, str)
        )

    coverage_by_actor: dict[str, dict[str, Any]] = {}
    addressed_actor_ids: set[str] = set()
    for index, raw_coverage_entry in enumerate(raw_coverage):
        entry_context = f"{context}.actor_coverage[{index}]"
        entry = _mapping(raw_coverage_entry, entry_context, errors)
        if entry is None:
            continue
        actor_id = entry.get("actor_id")
        status = entry.get("status")
        journey_ids = _id_list(entry.get("journey_ids"), entry_context + ".journey_ids", errors)
        unique_actor_entry = False
        if not isinstance(actor_id, str) or not actor_id:
            errors.append(f"{entry_context}: actor_id is required")
        elif actor_id in coverage_by_actor:
            errors.append(f"{entry_context}: duplicate actor coverage for {actor_id}")
        else:
            coverage_by_actor[actor_id] = entry
            unique_actor_entry = True
        if isinstance(actor_id, str) and actor_id not in actor_ids:
            errors.append(f"{entry_context}: unknown actor_id {actor_id}")
        if not isinstance(status, str) or status not in COVERAGE_STATUSES:
            errors.append(f"{entry_context}: invalid status {status!r}")
            continue
        if status == "covered":
            coverage_is_valid = unique_actor_entry
            decision_id = entry.get("decision_id")
            if not isinstance(decision_id, str) or decision_id not in confirmed_decision_ids:
                errors.append(
                    f"{entry_context}: covered status requires a confirmed decision ID"
                )
                coverage_is_valid = False
            else:
                affected_ids = set(journey_ids)
                if isinstance(actor_id, str):
                    affected_ids.add(actor_id)
                if not _validate_lifecycle_decision_scope(
                    decision_id,
                    decision_map,
                    affected_ids,
                    entry_context,
                    "covered decision",
                    "the actor or a listed journey",
                    None,
                    errors,
                ):
                    coverage_is_valid = False
            if not journey_ids:
                errors.append(f"{entry_context}: covered actor requires journey_ids")
                coverage_is_valid = False
            for journey_id in journey_ids:
                journey = journeys.get(journey_id)
                if journey is None:
                    errors.append(f"{entry_context}: unknown journey_id {journey_id}")
                    coverage_is_valid = False
                    continue
                journey_artifact = artifacts.get(journey_id) or {}
                if (
                    actor_id not in _list_value(journey.get("actor_ids"))
                    or journey.get("intent_status") != "confirmed"
                    or journey.get("status") != "confirmed"
                    or journey_artifact.get("status") != "confirmed"
                    or journey_artifact.get("stale")
                ):
                    errors.append(f"{entry_context}: journey {journey_id} is not a confirmed applicable journey")
                    coverage_is_valid = False
                journey_capability_ids = {
                    value
                    for value in _list_value(journey.get("capability_ids"))
                    if isinstance(value, str)
                }
                if not journey_capability_ids & set(in_scope_capability_ids):
                    errors.append(f"{entry_context}: journey {journey_id} does not cover an in-scope capability")
                    coverage_is_valid = False
            if coverage_is_valid and isinstance(actor_id, str):
                addressed_actor_ids.add(actor_id)
        elif status in {"not_applicable", "out_of_scope"}:
            if journey_ids:
                errors.append(f"{entry_context}: exclusion cannot list journey_ids")
            decision_id = entry.get("decision_id")
            decision_is_valid = (
                isinstance(decision_id, str) and decision_id in confirmed_decision_ids
            )
            if not decision_is_valid:
                errors.append(f"{entry_context}: exclusion requires a confirmed decision ID")
            elif not _validate_lifecycle_decision_scope(
                decision_id,
                decision_map,
                {actor_id} if isinstance(actor_id, str) else set(),
                entry_context,
                "exclusion decision",
                "the actor",
                None,
                errors,
            ):
                decision_is_valid = False
            if (
                unique_actor_entry
                and not journey_ids
                and decision_is_valid
                and isinstance(actor_id, str)
            ):
                addressed_actor_ids.add(actor_id)
        elif build_ready:
            if journey_ids:
                errors.append(f"{entry_context}: blocked coverage cannot list journey_ids")
            errors.append(f"{entry_context}: blocked actor coverage is not build-ready")

    for actor_id in sorted(required_actor_ids):
        if actor_id not in coverage_by_actor:
            errors.append(f"{actor_id}: missing lifecycle journey coverage")

    expected_actor_edges = {
        (actor_id, "performed_by", journey_id)
        for journey_id, journey in journeys.items()
        for actor_id in _list_value(journey.get("actor_ids"))
        if isinstance(actor_id, str)
    }
    expected_capability_edges = {
        (capability_id, "experienced_through", journey_id)
        for journey_id, journey in journeys.items()
        for capability_id in _list_value(journey.get("capability_ids"))
        if isinstance(capability_id, str)
    }
    actual_actor_edges = {
        (edge.get("from"), edge.get("relation"), edge.get("to"))
        for edge in trace_edges
        if edge.get("relation") == "performed_by" and edge.get("to") in journeys
    }
    actual_capability_edges = {
        (edge.get("from"), edge.get("relation"), edge.get("to"))
        for edge in trace_edges
        if edge.get("relation") == "experienced_through" and edge.get("to") in journeys
    }
    for edge in sorted(expected_actor_edges - actual_actor_edges, key=str):
        errors.append(f"{edge[0]}: missing traceability edge {edge[0]} -[performed_by]-> {edge[2]}")
    for edge in sorted(expected_capability_edges - actual_capability_edges, key=str):
        errors.append(
            f"{edge[0]}: missing traceability edge {edge[0]} -[experienced_through]-> {edge[2]}"
        )
    for edge in sorted(actual_actor_edges - expected_actor_edges, key=str):
        errors.append(f"{edge[0]}: extra journey traceability edge {edge[0]} -[performed_by]-> {edge[2]}")
    for edge in sorted(actual_capability_edges - expected_capability_edges, key=str):
        errors.append(
            f"{edge[0]}: extra journey traceability edge {edge[0]} -[experienced_through]-> {edge[2]}"
        )

    for edge in trace_edges:
        source_part_id = edge.get("source_part_id")
        if source_part_id is None:
            continue
        source_id = edge.get("from")
        if source_id not in journeys:
            errors.append("Traceability edge: source_part_id is only valid for journey sources")
            continue
        if source_part_id not in journey_parts.get(source_id, set()):
            errors.append(f"{source_id}: unknown source_part_id {source_part_id}")

    linked_edges: set[tuple[Any, Any, Any, Any]] = set()
    for edge in trace_edges:
        if edge.get("from") in journeys and edge.get("source_part_id") is not None:
            linked_edges.add(
                (edge.get("from"), edge.get("relation"), edge.get("to"), edge.get("source_part_id"))
            )
    for journey_id, journey in journeys.items():
        for phase in _list_value(journey.get("phases")):
            if not isinstance(phase, dict):
                continue
            for linked in _list_value(phase.get("linked_artifacts")):
                if not isinstance(linked, dict):
                    continue
                if not all(
                    isinstance(linked.get(field), str)
                    for field in ("relation", "id", "source_part_id")
                ):
                    continue
                expected = (
                    journey_id,
                    linked.get("relation"),
                    linked.get("id"),
                    linked.get("source_part_id"),
                )
                if expected not in linked_edges:
                    errors.append(
                        f"{journey_id}: missing qualified traceability edge for linked artifact {linked.get('id')}"
                    )

    # A macro journey does not replace detailed experience artifacts.
    for capability_id in in_scope_capability_ids:
        capability = capability_map.get(capability_id) or {}
        requirements = capability.get("coverage_requirements")
        if not isinstance(requirements, dict) or requirements.get("experience") is not True:
            continue
        detailed_targets = {
            edge.get("to")
            for edge in trace_edges
            if edge.get("from") == capability_id and edge.get("relation") == "experienced_through"
        }
        detailed_kinds = {
            artifacts[target].get("kind")
            for target in detailed_targets
            if target in artifacts
        } & DETAILED_EXPERIENCE_KINDS
        if not detailed_kinds:
            errors.append(
                f"{capability_id}: journey coverage cannot replace detailed FLOW/SCREEN/MOCK/COMP experience coverage"
            )

    return {
        "journey_count": len(journeys),
        "phase_count": phase_count,
        "action_count": action_count,
        "uncovered_in_scope_actor_count": len(required_actor_ids - addressed_actor_ids),
    }
