from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Callable

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("skills/reconstruct-product-intent", "skills/product-intent-manager")
JOURNEY_TYPES = {
    "customer_relationship",
    "operational_case",
    "developer_integration",
}
EVAL_CASE_IDS = {
    "operational-not-marketing-funnel",
    "separate-materially-different-actors",
    "missing-product-response-lane",
    "observed-journey-is-not-confirmed",
    "invented-emotional-insight",
    "missing-failure-exit-recovery",
    "missing-detailed-artifact-links",
    "image-only-journey-source",
    "journey-phase-change-must-mark-dependents-stale",
    "open-lifecycle-question-blocks-build-ready",
}


def run_tool(skill: str, script: str, *args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / skill / "scripts" / script), *(str(arg) for arg in args)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def load(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def write(path: Path, value: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


class LifecycleJourneyTests(unittest.TestCase):
    def mutate_example(
        self,
        skill: str,
        mutate: Callable[[Path, dict[str, Any]], None],
    ) -> tuple[subprocess.CompletedProcess[str], list[str]]:
        source = ROOT / skill / "assets/example-product-intent-package"
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        package = Path(temp_dir.name) / "package"
        shutil.copytree(source, package)
        journey_path = package / "experience/journeys/index.yaml"
        journeys = load(journey_path)
        mutate(package, journeys)
        write(journey_path, journeys)
        stamp = run_tool(skill, "stamp_package_hash.py", package)
        self.assertEqual(0, stamp.returncode, stamp.stderr)
        result = run_tool(skill, "validate_product_intent.py", package, "--no-report")
        return result, yaml.safe_load(result.stdout)["errors"]

    def test_template_and_example_include_first_class_journey_files(self) -> None:
        for skill in SKILLS:
            skill_root = ROOT / skill
            template = skill_root / "assets/product-intent-template"
            example = skill_root / "assets/example-product-intent-package"
            with self.subTest(skill=skill, tree="template"):
                self.assertEqual(
                    {"actor_coverage": [], "journeys": []},
                    load(template / "experience/journeys/index.yaml"),
                )
            with self.subTest(skill=skill, tree="example"):
                index = load(example / "experience/journeys/index.yaml")
                self.assertTrue(index["actor_coverage"])
                self.assertTrue(index["journeys"])
                for journey in index["journeys"]:
                    source_path = example / journey["source_path"]
                    self.assertEqual(".md", source_path.suffix)
                    self.assertTrue(source_path.is_file())

    def test_example_journey_uses_stable_local_ids_and_qualified_edges(self) -> None:
        for skill in SKILLS:
            package = ROOT / skill / "assets/example-product-intent-package"
            journey = load(package / "experience/journeys/index.yaml")["journeys"][0]
            phase_ids = {phase["id"] for phase in journey["phases"]}
            action_ids = {
                action["id"]
                for phase in journey["phases"]
                for action in phase["actions"]
            }
            with self.subTest(skill=skill):
                self.assertTrue(all(value.startswith(f"{journey['id']}.phase-") for value in phase_ids))
                self.assertTrue(all(value.startswith(f"{journey['id']}.action-") for value in action_ids))
                edges = load(package / "verification/traceability.yaml")["edges"]
                qualified = [
                    edge
                    for edge in edges
                    if edge.get("from") == journey["id"] and edge.get("source_part_id")
                ]
                self.assertTrue(qualified)
                self.assertTrue(
                    all(edge["source_part_id"] in phase_ids | action_ids for edge in qualified)
                )

    def test_validator_requires_actor_journey_coverage(self) -> None:
        for skill in SKILLS:
            result, errors = self.mutate_example(
                skill,
                lambda _package, data: data.__setitem__("actor_coverage", []),
            )
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertIn("ACTOR-001: missing lifecycle journey coverage", errors)

    def test_validator_requires_covered_actor_decision(self) -> None:
        def remove_decision(_package: Path, data: dict[str, Any]) -> None:
            data["actor_coverage"][0].pop("decision_id")

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, remove_decision)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any("covered status requires a confirmed decision" in error for error in errors),
                    errors,
                )

    def test_validator_counts_empty_covered_actor_as_uncovered(self) -> None:
        def remove_journeys(_package: Path, data: dict[str, Any]) -> None:
            data["actor_coverage"][0]["journey_ids"] = []

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, remove_journeys)
            report = yaml.safe_load(result.stdout)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(any("covered actor requires journey_ids" in error for error in errors))
                self.assertEqual(1, report["uncovered_in_scope_actor_count"])

    def test_validator_requires_product_response_for_each_action(self) -> None:
        def remove_response(_package: Path, data: dict[str, Any]) -> None:
            del data["journeys"][0]["phases"][0]["actions"][0]["product_response"]

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, remove_response)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any("requires product_response" in error for error in errors),
                    errors,
                )

    def test_validator_requires_behavior_for_each_product_response(self) -> None:
        def remove_behavior(_package: Path, data: dict[str, Any]) -> None:
            data["journeys"][0]["phases"][0]["actions"][0]["response_artifact_ids"] = []

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, remove_behavior)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any("requires a linked behavior artifact" in error for error in errors),
                    errors,
                )

    def test_validator_rejects_unrelated_product_response_exception(self) -> None:
        def use_technical_decision(_package: Path, data: dict[str, Any]) -> None:
            action = data["journeys"][0]["phases"][0]["actions"][0]
            action["response_artifact_ids"] = []
            action["response_exception_decision_id"] = "DEC-004"

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, use_technical_decision)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any("response exception decision domain must be" in error for error in errors),
                    errors,
                )
                self.assertTrue(
                    any(
                        "response exception decision must affect the journey" in error
                        for error in errors
                    ),
                    errors,
                )

    def test_validator_rejects_observed_journey_as_build_ready_intent(self) -> None:
        def mark_observed(_package: Path, data: dict[str, Any]) -> None:
            data["journeys"][0]["intent_status"] = "observed"

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, mark_observed)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any("build-ready journey must be confirmed" in error for error in errors),
                    errors,
                )

    def test_validator_accepts_proposed_journey_before_handoff(self) -> None:
        def make_proposed(package: Path, data: dict[str, Any]) -> None:
            manifest_path = package / "manifest.yaml"
            manifest = load(manifest_path)
            manifest["status"] = "modeled"
            manifest["build_ready"] = False
            write(manifest_path, manifest)

            decisions_path = package / "governance/decisions.yaml"
            decisions = load(decisions_path)
            decisions["decisions"].append(
                {
                    "id": "DEC-999",
                    "statement": "The proposed journey awaits product confirmation.",
                    "status": "proposed",
                    "domain": "capabilities_and_behavior",
                    "authority_id": "AUTH-OWNER",
                    "affects": ["JOURNEY-001"],
                    "supersedes": [],
                }
            )
            write(decisions_path, decisions)

            journey = data["journeys"][0]
            journey["status"] = "proposed"
            journey["intent_status"] = "proposed"
            journey["confirmation_decision_id"] = "DEC-999"
            data["actor_coverage"][0]["status"] = "blocked"
            data["actor_coverage"][0]["journey_ids"] = []

            index_path = package / "governance/artifact-index.yaml"
            index = load(index_path)
            artifact = next(item for item in index["artifacts"] if item["id"] == "JOURNEY-001")
            artifact["status"] = "proposed"
            artifact["confirmation_decision_id"] = "DEC-999"
            write(index_path, index)

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, make_proposed)
            with self.subTest(skill=skill):
                self.assertEqual(0, result.returncode, errors)

    def test_validator_requires_confirmation_from_journey_authority(self) -> None:
        def change_decision_authority(package: Path, _data: dict[str, Any]) -> None:
            authorities_path = package / "governance/authorities.yaml"
            authorities = load(authorities_path)
            authorities["authorities"].append(
                {
                    "id": "AUTH-OTHER",
                    "name": "Other authority",
                    "roles": ["observer"],
                    "contact_ref": "example:other",
                }
            )
            write(authorities_path, authorities)

            decisions_path = package / "governance/decisions.yaml"
            decisions = load(decisions_path)
            decision = next(item for item in decisions["decisions"] if item["id"] == "DEC-001")
            decision["authority_id"] = "AUTH-OTHER"
            write(decisions_path, decisions)

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, change_decision_authority)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any("confirmation decision authority must match journey authority" in error for error in errors),
                    errors,
                )

    def test_validator_rejects_unrelated_journey_confirmation(self) -> None:
        def use_technical_decision(package: Path, data: dict[str, Any]) -> None:
            data["journeys"][0]["confirmation_decision_id"] = "DEC-004"
            index_path = package / "governance/artifact-index.yaml"
            index = load(index_path)
            artifact = next(item for item in index["artifacts"] if item["id"] == "JOURNEY-001")
            artifact["confirmation_decision_id"] = "DEC-004"
            write(index_path, index)

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, use_technical_decision)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any("confirmation decision domain must be" in error for error in errors),
                    errors,
                )
                self.assertTrue(
                    any("confirmation decision must affect the journey" in error for error in errors),
                    errors,
                )

    def test_validator_rejects_unrelated_actor_coverage_decision(self) -> None:
        def use_technical_decision(_package: Path, data: dict[str, Any]) -> None:
            data["actor_coverage"][0]["decision_id"] = "DEC-004"

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, use_technical_decision)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any("covered decision domain must be" in error for error in errors),
                    errors,
                )
                self.assertTrue(
                    any(
                        "covered decision must affect the actor or a listed journey" in error
                        for error in errors
                    ),
                    errors,
                )

    def test_validator_rejects_actor_decision_without_domain_authority(self) -> None:
        def add_wrong_authority_decision(package: Path, data: dict[str, Any]) -> None:
            authorities_path = package / "governance/authorities.yaml"
            authorities = load(authorities_path)
            authorities["authorities"].append(
                {
                    "id": "AUTH-OTHER",
                    "name": "Other authority",
                    "roles": ["observer"],
                    "contact_ref": "example:other",
                }
            )
            write(authorities_path, authorities)

            decisions_path = package / "governance/decisions.yaml"
            decisions = load(decisions_path)
            decisions["decisions"].append(
                {
                    "id": "DEC-999",
                    "status": "confirmed",
                    "domain": "capabilities_and_behavior",
                    "statement": "The actor has lifecycle coverage.",
                    "authority_id": "AUTH-OTHER",
                    "confirmed_at": "2026-08-16T12:00:00Z",
                    "confirmation_ref": "fixture:wrong-authority",
                    "source_refs": ["EVID-001"],
                    "affects": ["ACTOR-001"],
                    "supersedes": [],
                }
            )
            write(decisions_path, decisions)
            data["actor_coverage"][0]["decision_id"] = "DEC-999"

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, add_wrong_authority_decision)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any("has no applicable delegation" in error for error in errors),
                    errors,
                )

    def test_validator_requires_journey_status_to_match_artifact_index(self) -> None:
        def change_status(_package: Path, data: dict[str, Any]) -> None:
            data["journeys"][0]["status"] = "proposed"

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, change_status)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any("status must match artifact index" in error for error in errors),
                    errors,
                )

    def test_validator_requires_journey_artifact_path_to_match_registry_slot(self) -> None:
        def change_path(package: Path, _data: dict[str, Any]) -> None:
            index_path = package / "governance/artifact-index.yaml"
            index = load(index_path)
            journey = next(item for item in index["artifacts"] if item["id"] == "JOURNEY-001")
            journey["path"] = "experience/journeys/index.yaml#/journeys/99"
            write(index_path, index)

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, change_path)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any("artifact path must match journey registry slot" in error for error in errors),
                    errors,
                )

    def test_validator_rejects_journey_artifact_without_registry_record(self) -> None:
        def add_unmodeled_journey(package: Path, _data: dict[str, Any]) -> None:
            index_path = package / "governance/artifact-index.yaml"
            index = load(index_path)
            index["artifacts"].append(
                {
                    "id": "JOURNEY-999",
                    "kind": "lifecycle_journey",
                    "label": "Unmodeled journey",
                    "path": "experience/journeys/index.yaml#/journeys/0",
                    "status": "confirmed",
                    "authority_id": "AUTH-OWNER",
                    "confirmation_decision_id": "DEC-001",
                    "source_refs": ["EVID-001"],
                    "version": 1,
                    "stale": False,
                }
            )
            write(index_path, index)

            trace_path = package / "verification/traceability.yaml"
            trace = load(trace_path)
            trace["edges"].extend(
                [
                    {
                        "from": "ACTOR-001",
                        "relation": "performed_by",
                        "to": "JOURNEY-999",
                    },
                    {
                        "from": "JOURNEY-999",
                        "relation": "experienced_through",
                        "to": "FLOW-001",
                    },
                ]
            )
            write(trace_path, trace)

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, add_unmodeled_journey)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any(
                        "lifecycle journey artifact has no journey registry record" in error
                        for error in errors
                    ),
                    errors,
                )

    def test_validator_requires_failure_exit_and_recovery_dispositions(self) -> None:
        def remove_failure(_package: Path, data: dict[str, Any]) -> None:
            del data["journeys"][0]["exception_coverage"]["failure"]

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, remove_failure)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any("exception_coverage must contain exactly" in error for error in errors),
                    errors,
                )

    def test_validator_does_not_require_decision_for_covered_exceptions(self) -> None:
        def remove_decisions(_package: Path, data: dict[str, Any]) -> None:
            for disposition in data["journeys"][0]["exception_coverage"].values():
                disposition.pop("decision_id", None)

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, remove_decisions)
            with self.subTest(skill=skill):
                self.assertEqual(0, result.returncode, errors)

    def test_validator_requires_covered_exception_links(self) -> None:
        def remove_links(_package: Path, data: dict[str, Any]) -> None:
            failure = data["journeys"][0]["exception_coverage"]["failure"]
            failure["phase_ids"] = []
            failure["artifact_ids"] = []

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, remove_links)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any("covered requires non-empty phase_ids" in error for error in errors),
                    errors,
                )
                self.assertTrue(
                    any("covered requires non-empty artifact_ids" in error for error in errors),
                    errors,
                )

    def test_validator_requires_behavior_or_verification_for_covered_exceptions(self) -> None:
        cases = (
            (
                "wrong_kind",
                ["DOM-001"],
                "covered requires a behavior or verification artifact",
            ),
            (
                "not_qualified",
                ["ACC-003"],
                "covered artifact requires a qualified link from a listed phase or action",
            ),
        )
        for skill in SKILLS:
            for name, artifact_ids, expected in cases:
                result, errors = self.mutate_example(
                    skill,
                    lambda _package, data, ids=artifact_ids: data["journeys"][0][
                        "exception_coverage"
                    ]["failure"].__setitem__("artifact_ids", ids),
                )
                with self.subTest(skill=skill, case=name):
                    self.assertNotEqual(0, result.returncode)
                    self.assertTrue(any(expected in error for error in errors), errors)

    def test_validator_requires_build_ready_phase_content(self) -> None:
        cases = (
            (
                "actions",
                lambda data: data["journeys"][0]["phases"][0].__setitem__("actions", []),
                "build-ready in-scope phase requires at least one action",
            ),
            (
                "intent_items",
                lambda data: data["journeys"][0]["phases"][0].__setitem__("intent_items", []),
                "build-ready in-scope phase requires at least one intent item",
            ),
            (
                "linked_artifacts",
                lambda data: data["journeys"][0]["phases"][0].__setitem__(
                    "linked_artifacts", []
                ),
                "build-ready in-scope phase requires linked artifacts",
            ),
        )

        for skill in SKILLS:
            for name, mutate, expected in cases:
                result, errors = self.mutate_example(
                    skill,
                    lambda _package, data, change=mutate: change(data),
                )
                with self.subTest(skill=skill, field=name):
                    self.assertNotEqual(0, result.returncode)
                    self.assertTrue(any(expected in error for error in errors), errors)

    def test_validator_requires_journey_phases(self) -> None:
        def remove_phases(_package: Path, data: dict[str, Any]) -> None:
            data["journeys"][0]["phases"] = []

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, remove_phases)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any("journey requires at least one phase" in error for error in errors),
                    errors,
                )

    def test_validator_blocks_unresolved_journey_insight_at_handoff(self) -> None:
        def add_assumption(_package: Path, data: dict[str, Any]) -> None:
            data["journeys"][0]["phases"][0]["intent_items"].append(
                {
                    "type": "assumption",
                    "statement": "The actor prefers immediate feedback.",
                }
            )

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, add_assumption)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any("contains unresolved assumption" in error for error in errors),
                    errors,
                )

    def test_validator_requires_confirmed_decision_intent_at_handoff(self) -> None:
        def add_proposed_decision(package: Path, data: dict[str, Any]) -> None:
            decisions_path = package / "governance/decisions.yaml"
            decisions = load(decisions_path)
            decisions["decisions"].append(
                {
                    "id": "DEC-999",
                    "statement": "The actor can skip result review.",
                    "status": "proposed",
                    "authority_id": "AUTH-OWNER",
                    "supersedes": [],
                }
            )
            write(decisions_path, decisions)
            data["journeys"][0]["phases"][0]["intent_items"].append(
                {
                    "type": "decision",
                    "statement": "The actor can skip result review.",
                    "decision_id": "DEC-999",
                }
            )

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, add_proposed_decision)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any("build-ready decision must be confirmed" in error for error in errors),
                    errors,
                )

    def test_validator_requires_detailed_flow_for_complex_branch(self) -> None:
        def remove_flow(_package: Path, data: dict[str, Any]) -> None:
            transition = data["journeys"][0]["transitions"][0]
            transition["complex"] = True
            transition["flow_ids"] = []

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, remove_flow)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any("complex transition requires flow_ids" in error for error in errors),
                    errors,
                )

    def test_validator_rejects_image_only_journey_source(self) -> None:
        def use_image(package: Path, data: dict[str, Any]) -> None:
            data["journeys"][0]["source_path"] = "experience/journeys/rendered/JOURNEY-001.png"
            rendered = package / "experience/journeys/rendered"
            rendered.mkdir(exist_ok=True)
            (rendered / "JOURNEY-001.png").write_bytes(b"not a canonical source")

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, use_image)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any("source_path must be an editable Markdown .md file" in error for error in errors),
                    errors,
                )

    def test_validator_rejects_journey_source_outside_package(self) -> None:
        def escape_package(package: Path, data: dict[str, Any]) -> None:
            data["journeys"][0]["source_path"] = "../outside.md"
            (package.parent / "outside.md").write_text(
                "| Phase | Action |\n| --- | --- |\n| Begin | Open |\n",
                encoding="utf-8",
            )

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, escape_package)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any("source_path must stay inside package" in error for error in errors),
                    errors,
                )

    def test_validator_accepts_markdown_table_as_editable_journey_source(self) -> None:
        def use_table(package: Path, data: dict[str, Any]) -> None:
            source = package / data["journeys"][0]["source_path"]
            source.write_text(
                "# Counter lifecycle\n\n"
                "| Phase | Actor action | Product response |\n"
                "| --- | --- | --- |\n"
                "| Begin | Open counter | Show zero |\n",
                encoding="utf-8",
            )

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, use_table)
            with self.subTest(skill=skill):
                self.assertEqual(0, result.returncode, errors)

    def test_validator_accepts_lane_oriented_journey_table(self) -> None:
        def use_lane_table(package: Path, data: dict[str, Any]) -> None:
            source = package / data["journeys"][0]["source_path"]
            source.write_text(
                "# Counter lifecycle\n\n"
                "| Lane | Begin | Complete |\n"
                "| --- | --- | --- |\n"
                "| Actor Goal | See the value | Finish safely |\n"
                "| Actor Action | Open the screen | Leave |\n"
                "| Product Response | Show the value | Preserve the value |\n",
                encoding="utf-8",
            )

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, use_lane_table)
            with self.subTest(skill=skill):
                self.assertEqual(0, result.returncode, errors)

    def test_validator_requires_matching_qualified_trace_edge(self) -> None:
        def remove_edge(package: Path, data: dict[str, Any]) -> None:
            link = data["journeys"][0]["phases"][0]["linked_artifacts"][0]
            expected = {
                "from": data["journeys"][0]["id"],
                "source_part_id": link["source_part_id"],
                "relation": link["relation"],
                "to": link["id"],
            }
            trace_path = package / "verification/traceability.yaml"
            trace = load(trace_path)
            trace["edges"].remove(expected)
            write(trace_path, trace)

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, remove_edge)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any("missing qualified traceability edge" in error for error in errors),
                    errors,
                )

    def test_validator_links_each_product_response_from_its_action(self) -> None:
        def remove_action_links(package: Path, data: dict[str, Any]) -> None:
            action_id = data["journeys"][0]["phases"][0]["actions"][0]["id"]
            phase = data["journeys"][0]["phases"][0]
            phase["linked_artifacts"] = [
                link
                for link in phase["linked_artifacts"]
                if link["source_part_id"] != action_id
            ]
            trace_path = package / "verification/traceability.yaml"
            trace = load(trace_path)
            trace["edges"] = [
                edge for edge in trace["edges"] if edge.get("source_part_id") != action_id
            ]
            write(trace_path, trace)

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, remove_action_links)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any(
                        "response_artifact_ids require same-action linked_artifacts entries"
                        in error
                        for error in errors
                    ),
                    errors,
                )

    def test_validator_rejects_unknown_qualified_trace_part(self) -> None:
        def corrupt_edge(package: Path, _data: dict[str, Any]) -> None:
            trace_path = package / "verification/traceability.yaml"
            trace = load(trace_path)
            edge = next(edge for edge in trace["edges"] if edge.get("source_part_id"))
            edge["source_part_id"] = "JOURNEY-001.phase-999"
            write(trace_path, trace)

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, corrupt_edge)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any("unknown source_part_id" in error for error in errors),
                    errors,
                )

    def test_validator_rejects_malformed_journey_values_without_crash(self) -> None:
        cases = (
            (
                "journey_type",
                lambda _package, data: data["journeys"][0].__setitem__("journey_type", []),
                "invalid journey_type",
            ),
            (
                "intent_status",
                lambda _package, data: data["journeys"][0].__setitem__(
                    "intent_status", [[]]
                ),
                "invalid intent_status",
            ),
            (
                "source_part_id",
                self._set_list_source_part,
                "source_part_id must be a non-empty string",
            ),
            (
                "capability_ids",
                lambda _package, data: data["journeys"][0].__setitem__(
                    "capability_ids", [[]]
                ),
                "must be a non-empty ID string",
            ),
        )
        for skill in SKILLS:
            for name, mutate, expected in cases:
                result, errors = self.mutate_example(skill, mutate)
                with self.subTest(skill=skill, field=name):
                    self.assertNotEqual(0, result.returncode)
                    self.assertTrue(any(expected in error for error in errors), errors)

    @staticmethod
    def _set_list_source_part(package: Path, _data: dict[str, Any]) -> None:
        trace_path = package / "verification/traceability.yaml"
        trace = load(trace_path)
        edge = next(item for item in trace["edges"] if item.get("source_part_id"))
        edge["source_part_id"] = ["JOURNEY-001.phase-01"]
        write(trace_path, trace)

    def test_validator_rejects_cross_phase_local_link(self) -> None:
        def move_link(_package: Path, data: dict[str, Any]) -> None:
            link = data["journeys"][0]["phases"][0]["linked_artifacts"][0]
            link["source_part_id"] = "JOURNEY-001.action-02"

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, move_link)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any("source_part_id must belong to the enclosing phase" in error for error in errors),
                    errors,
                )

    def test_validator_rejects_unreachable_journey_phases(self) -> None:
        def disconnect(_package: Path, data: dict[str, Any]) -> None:
            data["journeys"][0]["transitions"] = data["journeys"][0]["transitions"][:1]

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, disconnect)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(any("unreachable phase" in error for error in errors), errors)

    def test_validator_requires_a_cycle_for_repeating_topology(self) -> None:
        def remove_cycle(_package: Path, data: dict[str, Any]) -> None:
            journey = data["journeys"][0]
            journey["topology"] = ["cyclical"]
            journey["transitions"] = [
                journey["transitions"][0],
                journey["transitions"][1],
                journey["transitions"][4],
            ]

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, remove_cycle)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any("cyclical topology requires a directed cycle" in error for error in errors),
                    errors,
                )

    def test_validator_requires_a_branch_for_branching_topology(self) -> None:
        def remove_branch(_package: Path, data: dict[str, Any]) -> None:
            journey = data["journeys"][0]
            journey["topology"] = ["branching"]
            journey["transitions"] = [
                journey["transitions"][0],
                journey["transitions"][1],
                journey["transitions"][4],
            ]

        for skill in SKILLS:
            result, errors = self.mutate_example(skill, remove_branch)
            with self.subTest(skill=skill):
                self.assertNotEqual(0, result.returncode)
                self.assertTrue(
                    any(
                        "branching topology requires two outgoing transitions" in error
                        for error in errors
                    ),
                    errors,
                )

    def test_validator_enforces_structural_variant_actor_counts(self) -> None:
        cases = (
            (
                "single_actor",
                lambda data: data["journeys"][0]["actor_ids"].append("ACTOR-999"),
                "single_actor requires exactly one actor_id",
            ),
            (
                "multi_actor_coordinated",
                lambda data: data["journeys"][0].__setitem__(
                    "structural_variant", "multi_actor_coordinated"
                ),
                "multi_actor_coordinated requires at least two actor_ids",
            ),
            (
                "role_specific",
                lambda data: data["journeys"][0].__setitem__(
                    "structural_variant", "role_specific"
                ),
                "role_specific requires at least two actor_ids",
            ),
        )
        for skill in SKILLS:
            for name, change, expected in cases:
                result, errors = self.mutate_example(
                    skill,
                    lambda _package, data, mutate=change: mutate(data),
                )
                with self.subTest(skill=skill, variant=name):
                    self.assertNotEqual(0, result.returncode)
                    self.assertTrue(any(expected in error for error in errors), errors)

    def test_validator_does_not_blacklist_confirmed_common_phase_names(self) -> None:
        def use_common_name(_package: Path, data: dict[str, Any]) -> None:
            data["journeys"][0]["phases"][0]["name"] = "Awareness"

        for skill in SKILLS:
            result, _errors = self.mutate_example(skill, use_common_name)
            with self.subTest(skill=skill):
                self.assertEqual(0, result.returncode, result.stdout)

    def test_manager_impact_analysis_propagates_journey_change(self) -> None:
        package = ROOT / "skills/product-intent-manager/assets/example-product-intent-package"
        result = run_tool(
            "skills/product-intent-manager",
            "impact_analysis.py",
            package,
            "JOURNEY-001",
        )
        self.assertEqual(0, result.returncode, result.stderr)
        affected = set(yaml.safe_load(result.stdout)["affected_ids"])
        self.assertIn("FLOW-001", affected)
        self.assertIn("RULE-001", affected)
        self.assertIn("ACC-001", affected)

    def test_references_demonstrate_three_distinct_journey_types(self) -> None:
        for skill in SKILLS:
            reference = (
                ROOT / skill / "references/lifecycle-journey-maps.md"
            ).read_text(encoding="utf-8")
            with self.subTest(skill=skill):
                for journey_type in JOURNEY_TYPES:
                    self.assertIn(f"`{journey_type}`", reference)

    def test_evals_cover_requested_journey_failures(self) -> None:
        found: set[str] = set()
        for skill in SKILLS:
            cases = load(ROOT / skill / "evals/cases.yaml")["cases"]
            found.update(item["id"] for item in cases)
        self.assertEqual(set(), EVAL_CASE_IDS - found)


if __name__ == "__main__":
    unittest.main()
