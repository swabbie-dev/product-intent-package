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
