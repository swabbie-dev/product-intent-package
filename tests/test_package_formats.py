from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("skills/reconstruct-product-intent", "skills/product-intent-manager")
PACKAGE_TREES = ("assets/product-intent-template", "assets/example-product-intent-package")
SHARED_REFERENCES = (
    "authority-and-evidence-policy.md",
    "coverage-and-handoff-gates.md",
    "example-capability-slice.md",
    "lifecycle-journey-maps.md",
    "product-intent-package-standard.md",
    "questioning-protocol.md",
    "registry-schemas.md",
    "source-safety.md",
)
SHARED_SCRIPTS = (
    "init_product_intent.py",
    "journey_validation.py",
    "stamp_package_hash.py",
    "validate_product_intent.py",
    "yaml_io.py",
)

STRUCTURED_PATHS = (
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
    "product/capabilities.yaml",
    "experience/journeys/index.yaml",
    "experience/screens.yaml",
    "experience/design-tokens.yaml",
    "experience/components.yaml",
    "behavior/rules.yaml",
    "data/schema.yaml",
    "data/lifecycle.yaml",
    "architecture/decisions.yaml",
    "contracts/openapi.yaml",
    "contracts/events.yaml",
    "contracts/integrations.yaml",
    "quality/constraints.yaml",
    "verification/acceptance.yaml",
    "verification/traceability.yaml",
    "handoff/implementation-discretion.yaml",
    "handoff/readiness.yaml",
)

DIAGRAM_PATHS = (
    "product/context.md",
    "product/domain-model.md",
    "experience/user-flows.md",
    "experience/screen-map.md",
    "behavior/state-machines.md",
    "architecture/system-context.md",
    "architecture/containers.md",
    "architecture/components.md",
    "architecture/deployment.md",
    "sequences/sequences.md",
)


def run_tool(skill: str, script: str, *args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / skill / "scripts" / script), *(str(arg) for arg in args)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def load_yaml_io(skill: str) -> ModuleType:
    path = ROOT / skill / "scripts" / "yaml_io.py"
    spec = importlib.util.spec_from_file_location(f"{skill}_yaml_io", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PackageFormatTests(unittest.TestCase):
    def test_skill_trees_use_human_readable_extensions(self) -> None:
        for skill in SKILLS:
            skill_root = ROOT / skill
            with self.subTest(skill=skill):
                self.assertFalse((skill_root / "evals/cases.json").exists())
                self.assertTrue((skill_root / "evals/cases.yaml").is_file())

            for tree in PACKAGE_TREES:
                package = skill_root / tree
                with self.subTest(skill=skill, tree=tree):
                    for relative in STRUCTURED_PATHS:
                        self.assertTrue((package / relative).is_file(), relative)
                        legacy = relative.removesuffix(".yaml") + ".json"
                        self.assertFalse((package / legacy).exists(), legacy)
                    for relative in DIAGRAM_PATHS:
                        self.assertTrue((package / relative).is_file(), relative)
                        legacy = relative.removesuffix(".md") + ".mmd"
                        self.assertFalse((package / legacy).exists(), legacy)

    def test_diagram_files_contain_mermaid_fences(self) -> None:
        for skill in SKILLS:
            for tree in PACKAGE_TREES:
                package = ROOT / skill / tree
                for relative in DIAGRAM_PATHS:
                    path = package / relative
                    with self.subTest(skill=skill, tree=tree, path=relative):
                        text = path.read_text(encoding="utf-8")
                        self.assertEqual(1, text.count("```mermaid\n"))
                        self.assertTrue(text.rstrip().endswith("```"))

    def test_markdown_fences_are_balanced(self) -> None:
        for skill in SKILLS:
            skill_root = ROOT / skill
            for path in skill_root.rglob("*.md"):
                with self.subTest(skill=skill, path=path.relative_to(skill_root)):
                    self.assertEqual(
                        0,
                        path.read_text(encoding="utf-8").count("```") % 2,
                    )

    def test_all_authored_yaml_is_safe_loadable(self) -> None:
        for skill in SKILLS:
            skill_root = ROOT / skill
            for path in skill_root.rglob("*.yaml"):
                with self.subTest(skill=skill, path=path.relative_to(skill_root)):
                    yaml.safe_load(path.read_text(encoding="utf-8"))

    def test_no_legacy_package_paths_remain(self) -> None:
        legacy_paths = tuple(
            path.removesuffix(".yaml") + ".json" for path in STRUCTURED_PATHS
        ) + tuple(path.removesuffix(".md") + ".mmd" for path in DIAGRAM_PATHS)
        for skill in SKILLS:
            skill_root = ROOT / skill
            paths = (
                list(skill_root.glob("*.md"))
                + list((skill_root / "references").rglob("*.md"))
                + list((skill_root / "scripts").rglob("*.py"))
                + list((skill_root / "evals").rglob("*.md"))
                + list((skill_root / "assets").rglob("README.md"))
            )
            for path in paths:
                text = path.read_text(encoding="utf-8")
                for legacy_path in legacy_paths:
                    with self.subTest(skill=skill, path=path.relative_to(skill_root), legacy=legacy_path):
                        self.assertNotIn(legacy_path, text)

    def test_package_schema_version_is_3(self) -> None:
        for skill in SKILLS:
            for tree in PACKAGE_TREES:
                manifest = yaml.safe_load(
                    (ROOT / skill / tree / "manifest.yaml").read_text(encoding="utf-8")
                )
                with self.subTest(skill=skill, tree=tree):
                    self.assertEqual("3.0.0", manifest["schema_version"])
            self.assertIn(
                "Product Intent Package format 3.0.0",
                (ROOT / skill / "SKILL.md").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "Product Intent Package format `3.0.0`",
                (
                    ROOT
                    / skill
                    / "references/product-intent-package-standard.md"
                ).read_text(encoding="utf-8"),
            )

    def test_yaml_loader_rejects_duplicate_keys_and_custom_tags(self) -> None:
        for skill in SKILLS:
            yaml_io = load_yaml_io(skill)
            with tempfile.TemporaryDirectory() as temp_dir:
                path = Path(temp_dir) / "input.yaml"
                for content in (
                    "value: 1\nvalue: 2\n",
                    "value: !!python/object/apply:os.system ['echo unsafe']\n",
                    "base: &base {value: 1}\ncopy: *base\n",
                    "- not\n- a\n- mapping\n",
                    "1: numeric key\n",
                    "? [complex, key]\n: value\n",
                ):
                    path.write_text(content, encoding="utf-8")
                    with self.subTest(skill=skill, content=content):
                        with self.assertRaises(yaml.YAMLError):
                            yaml_io.load_yaml(path)

    def test_yaml_loader_uses_yaml_1_2_boolean_rules(self) -> None:
        for skill in SKILLS:
            yaml_io = load_yaml_io(skill)
            with tempfile.TemporaryDirectory() as temp_dir:
                path = Path(temp_dir) / "input.yaml"
                path.write_text(
                    "values: [yes, no, on, off, true, false]\n",
                    encoding="utf-8",
                )
                with self.subTest(skill=skill):
                    self.assertEqual(
                        ["yes", "no", "on", "off", True, False],
                        yaml_io.load_yaml(path)["values"],
                    )

    def test_yaml_loader_keeps_dates_as_strings(self) -> None:
        for skill in SKILLS:
            yaml_io = load_yaml_io(skill)
            with tempfile.TemporaryDirectory() as temp_dir:
                path = Path(temp_dir) / "input.yaml"
                path.write_text(
                    "date: 2026-08-15\ntimestamp: 2026-08-15T12:00:00Z\n",
                    encoding="utf-8",
                )
                with self.subTest(skill=skill):
                    self.assertEqual(
                        {
                            "date": "2026-08-15",
                            "timestamp": "2026-08-15T12:00:00Z",
                        },
                        yaml_io.load_yaml(path),
                    )

    def test_yaml_dumper_indents_lists_for_people(self) -> None:
        for skill in SKILLS:
            yaml_io = load_yaml_io(skill)
            with self.subTest(skill=skill):
                self.assertIn(
                    "items:\n  - value\n",
                    yaml_io.dump_yaml({"items": ["value"]}),
                )

    def test_example_packages_validate_and_generate_yaml_reports(self) -> None:
        for skill in SKILLS:
            source = ROOT / skill / "assets/example-product-intent-package"
            with tempfile.TemporaryDirectory() as temp_dir:
                package = Path(temp_dir) / "package"
                shutil.copytree(source, package)
                result = run_tool(skill, "validate_product_intent.py", package)
                with self.subTest(skill=skill, stderr=result.stderr):
                    self.assertEqual(0, result.returncode, result.stdout)
                    self.assertEqual(0, yaml.safe_load(result.stdout)["error_count"])
                    self.assertTrue((package / "handoff/readiness-report.generated.yaml").is_file())
                    self.assertTrue((package / "handoff/readiness-report.generated.md").is_file())
                    self.assertFalse((package / "handoff/readiness-report.generated.json").exists())

    def test_validator_rejects_markdown_without_mermaid_fence(self) -> None:
        for skill in SKILLS:
            source = ROOT / skill / "assets/example-product-intent-package"
            with tempfile.TemporaryDirectory() as temp_dir:
                package = Path(temp_dir) / "package"
                shutil.copytree(source, package)
                diagram = package / "product/context.md"
                diagram.write_text("flowchart LR\n  A --> B\n", encoding="utf-8")
                result = run_tool(skill, "validate_product_intent.py", package, "--no-report")
                with self.subTest(skill=skill):
                    self.assertNotEqual(0, result.returncode)
                    self.assertIn("fenced mermaid block", result.stdout.lower())

    def test_validator_rejects_old_schema_version(self) -> None:
        for skill in SKILLS:
            source = ROOT / skill / "assets/example-product-intent-package"
            with tempfile.TemporaryDirectory() as temp_dir:
                package = Path(temp_dir) / "package"
                shutil.copytree(source, package)
                manifest_path = package / "manifest.yaml"
                manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
                manifest["schema_version"] = "2.0.0"
                manifest_path.write_text(
                    yaml.safe_dump(manifest, sort_keys=False),
                    encoding="utf-8",
                )
                result = run_tool(skill, "validate_product_intent.py", package, "--no-report")
                with self.subTest(skill=skill):
                    self.assertNotEqual(0, result.returncode)
                    self.assertIn(
                        "manifest.yaml: schema_version must be '3.0.0'",
                        yaml.safe_load(result.stdout)["errors"],
                    )

    def test_validator_preserves_external_source_evidence_formats(self) -> None:
        for skill in SKILLS:
            source = ROOT / skill / "assets/example-product-intent-package"
            with tempfile.TemporaryDirectory() as temp_dir:
                package = Path(temp_dir) / "package"
                shutil.copytree(source, package)
                evidence = package / "source-evidence"
                evidence.mkdir()
                (evidence / "original.yaml").write_text(
                    "- &item source\n- *item\n",
                    encoding="utf-8",
                )
                (evidence / "original.json").write_text("[\"source\"]\n", encoding="utf-8")
                (evidence / "original.mmd").write_text("flowchart LR\n  A --> B\n", encoding="utf-8")
                stamp = run_tool(skill, "stamp_package_hash.py", package)
                result = run_tool(skill, "validate_product_intent.py", package, "--no-report")
                with self.subTest(skill=skill, stderr=stamp.stderr + result.stderr):
                    self.assertEqual(0, stamp.returncode)
                    self.assertEqual(0, result.returncode, result.stdout)

    def test_validator_rejects_invalid_registered_split_yaml(self) -> None:
        for skill in SKILLS:
            source = ROOT / skill / "assets/example-product-intent-package"
            with tempfile.TemporaryDirectory() as temp_dir:
                package = Path(temp_dir) / "package"
                shutil.copytree(source, package)

                index_path = package / "governance/artifact-index.yaml"
                index = yaml.safe_load(index_path.read_text(encoding="utf-8"))
                index["artifacts"].append(
                    {
                        "id": "DOM-999",
                        "kind": "domain_concept",
                        "label": "DOM-999",
                        "path": "product/DOM-999.yaml",
                        "status": "confirmed",
                        "authority_id": "AUTH-OWNER",
                        "confirmation_decision_id": "DEC-001",
                        "source_refs": ["EVID-001"],
                        "version": 1,
                        "stale": False,
                    }
                )
                index_path.write_text(yaml.safe_dump(index, sort_keys=False), encoding="utf-8")

                trace_path = package / "verification/traceability.yaml"
                trace = yaml.safe_load(trace_path.read_text(encoding="utf-8"))
                trace["edges"].append(
                    {"from": "CAP-001", "relation": "uses_domain", "to": "DOM-999"}
                )
                trace_path.write_text(yaml.safe_dump(trace, sort_keys=False), encoding="utf-8")

                (package / "product/DOM-999.yaml").write_text(
                    "id: DOM-999\nbroken: [unterminated\n",
                    encoding="utf-8",
                )
                stamp = run_tool(skill, "stamp_package_hash.py", package)
                result = run_tool(skill, "validate_product_intent.py", package, "--no-report")
                errors = yaml.safe_load(result.stdout)["errors"]
                with self.subTest(skill=skill, stderr=stamp.stderr + result.stderr):
                    self.assertEqual(0, stamp.returncode)
                    self.assertNotEqual(0, result.returncode)
                    self.assertTrue(
                        any("Invalid YAML" in error and "DOM-999.yaml" in error for error in errors),
                        errors,
                    )

    def test_validator_rejects_registered_split_mermaid_without_fence(self) -> None:
        for skill in SKILLS:
            source = ROOT / skill / "assets/example-product-intent-package"
            with tempfile.TemporaryDirectory() as temp_dir:
                package = Path(temp_dir) / "package"
                shutil.copytree(source, package)

                index_path = package / "governance/artifact-index.yaml"
                index = yaml.safe_load(index_path.read_text(encoding="utf-8"))
                index["artifacts"].append(
                    {
                        "id": "ARCH-999",
                        "kind": "architecture",
                        "label": "ARCH-999",
                        "path": "architecture/ARCH-999.md",
                        "status": "confirmed",
                        "authority_id": "AUTH-OWNER",
                        "confirmation_decision_id": "DEC-001",
                        "source_refs": ["EVID-001"],
                        "version": 1,
                        "stale": False,
                    }
                )
                index_path.write_text(yaml.safe_dump(index, sort_keys=False), encoding="utf-8")

                trace_path = package / "verification/traceability.yaml"
                trace = yaml.safe_load(trace_path.read_text(encoding="utf-8"))
                trace["edges"].append(
                    {"from": "CAP-001", "relation": "implemented_by", "to": "ARCH-999"}
                )
                trace_path.write_text(yaml.safe_dump(trace, sort_keys=False), encoding="utf-8")

                (package / "architecture/ARCH-999.md").write_text(
                    "flowchart LR\n  A --> B\n",
                    encoding="utf-8",
                )
                stamp = run_tool(skill, "stamp_package_hash.py", package)
                result = run_tool(skill, "validate_product_intent.py", package, "--no-report")
                errors = yaml.safe_load(result.stdout)["errors"]
                with self.subTest(skill=skill, stderr=stamp.stderr + result.stderr):
                    self.assertEqual(0, stamp.returncode)
                    self.assertNotEqual(0, result.returncode)
                    self.assertIn(
                        "architecture/ARCH-999.md: requires a fenced mermaid block",
                        errors,
                    )

    def test_validator_rejects_registered_legacy_canonical_formats(self) -> None:
        cases = (
            (
                "CAP-001",
                "product/CAP-001.json",
                "{\"id\": \"CAP-001\"}\n",
                "CAP-001: canonical package path cannot use a legacy format: product/CAP-001.json",
            ),
            (
                "ARCH-001",
                "architecture/ARCH-001.mmd",
                "flowchart LR\n  ARCH-001 --> B\n",
                "ARCH-001: canonical package path cannot use a legacy format: architecture/ARCH-001.mmd",
            ),
            (
                "DOM-001",
                "product/DOM-001.yml",
                "id: DOM-001\n",
                "DOM-001: canonical YAML path must use .yaml: product/DOM-001.yml",
            ),
        )
        for skill in SKILLS:
            source = ROOT / skill / "assets/example-product-intent-package"
            for artifact_id, relative, content, expected_error in cases:
                with tempfile.TemporaryDirectory() as temp_dir:
                    package = Path(temp_dir) / "package"
                    shutil.copytree(source, package)
                    index_path = package / "governance/artifact-index.yaml"
                    index = yaml.safe_load(index_path.read_text(encoding="utf-8"))
                    artifact = next(
                        item for item in index["artifacts"] if item["id"] == artifact_id
                    )
                    artifact["path"] = relative
                    index_path.write_text(
                        yaml.safe_dump(index, sort_keys=False),
                        encoding="utf-8",
                    )
                    (package / relative).write_text(content, encoding="utf-8")
                    stamp = run_tool(skill, "stamp_package_hash.py", package)
                    result = run_tool(skill, "validate_product_intent.py", package, "--no-report")
                    errors = yaml.safe_load(result.stdout)["errors"]
                    with self.subTest(skill=skill, path=relative):
                        self.assertEqual(0, stamp.returncode, stamp.stderr)
                        self.assertNotEqual(0, result.returncode)
                        self.assertIn(expected_error, errors)

    def test_validator_requires_declared_traceability_edges(self) -> None:
        cases = (
            (
                "actor_ids",
                "CAP-001",
                {"from": "ACTOR-001", "relation": "performed_by", "to": "CAP-001"},
                {"from": "CAP-001", "relation": "performed_by", "to": "ACTOR-001"},
            ),
            (
                "dependency_ids",
                "CAP-001",
                {"from": "CAP-001", "relation": "depends_on", "to": "CAP-001"},
                {"from": "CAP-001", "relation": "depends_on", "to": "ARCH-001"},
            ),
            (
                "capability_ids",
                "ACC-001",
                {"from": "CAP-001", "relation": "verified_by", "to": "ACC-001"},
                {"from": "ACC-001", "relation": "verified_by", "to": "CAP-001"},
            ),
            (
                "scope_ids",
                "RULE-001",
                {"from": "CAP-001", "relation": "governed_by", "to": "RULE-001"},
                {"from": "RULE-001", "relation": "governed_by", "to": "CAP-001"},
            ),
            (
                "scope_ids",
                "QC-001",
                {"from": "CAP-001", "relation": "constrained_by", "to": "QC-001"},
                {"from": "QC-001", "relation": "constrained_by", "to": "CAP-001"},
            ),
        )
        for skill in SKILLS:
            source = ROOT / skill / "assets/example-product-intent-package"
            for field, record_id, expected_edge, extra_edge in cases:
                with tempfile.TemporaryDirectory() as temp_dir:
                    package = Path(temp_dir) / "package"
                    shutil.copytree(source, package)
                    if field == "dependency_ids":
                        capabilities_path = package / "product/capabilities.yaml"
                        capabilities = yaml.safe_load(
                            capabilities_path.read_text(encoding="utf-8")
                        )
                        capabilities["capabilities"][0]["dependency_ids"] = ["CAP-001"]
                        capabilities_path.write_text(
                            yaml.safe_dump(capabilities, sort_keys=False), encoding="utf-8"
                        )
                    trace_path = package / "verification/traceability.yaml"
                    trace = yaml.safe_load(trace_path.read_text(encoding="utf-8"))
                    if field == "dependency_ids":
                        trace["edges"].append(expected_edge)
                    trace["edges"].remove(expected_edge)
                    trace_path.write_text(yaml.safe_dump(trace, sort_keys=False), encoding="utf-8")
                    result = run_tool(skill, "validate_product_intent.py", package, "--no-report")
                    errors = yaml.safe_load(result.stdout)["errors"]
                    with self.subTest(skill=skill, field=field, record=record_id, kind="missing"):
                        self.assertNotEqual(0, result.returncode)
                        self.assertIn(
                            f"{record_id}: {field} missing traceability edge "
                            f"{expected_edge['from']} -[{expected_edge['relation']}]-> "
                            f"{expected_edge['to']}",
                            errors,
                        )

                with tempfile.TemporaryDirectory() as temp_dir:
                    package = Path(temp_dir) / "package"
                    shutil.copytree(source, package)
                    trace_path = package / "verification/traceability.yaml"
                    trace = yaml.safe_load(trace_path.read_text(encoding="utf-8"))
                    trace["edges"].append(extra_edge)
                    trace_path.write_text(yaml.safe_dump(trace, sort_keys=False), encoding="utf-8")
                    result = run_tool(skill, "validate_product_intent.py", package, "--no-report")
                    errors = yaml.safe_load(result.stdout)["errors"]
                    with self.subTest(skill=skill, field=field, record=record_id, kind="extra"):
                        self.assertNotEqual(0, result.returncode)
                        self.assertIn(
                            f"{record_id}: {field} has extra traceability edge "
                            f"{extra_edge['from']} -[{extra_edge['relation']}]-> "
                            f"{extra_edge['to']}",
                            errors,
                        )

    def test_validator_rejects_unknown_and_malformed_canonical_ids(self) -> None:
        cases = (
            (
                "product/capabilities.yaml",
                lambda document, _index: document["actors"].__setitem__(0, {
                    **document["actors"][0],
                    "id": "PATTERN-001",
                }),
                "product/capabilities.yaml: unsupported canonical ID prefix 'PATTERN' in 'PATTERN-001'",
            ),
            (
                "governance/artifact-index.yaml",
                lambda _document, index: next(
                    artifact for artifact in index["artifacts"] if artifact["id"] == "ARCH-003"
                ).__setitem__("label", "ARCH-003A"),
                "governance/artifact-index.yaml: canonical ID 'ARCH-003A' must end with digits",
            ),
        )
        for skill in SKILLS:
            source = ROOT / skill / "assets/example-product-intent-package"
            for relative, mutate, expected_error in cases:
                with tempfile.TemporaryDirectory() as temp_dir:
                    package = Path(temp_dir) / "package"
                    shutil.copytree(source, package)
                    document_path = package / relative
                    document = yaml.safe_load(document_path.read_text(encoding="utf-8"))
                    index_path = package / "governance/artifact-index.yaml"
                    index = yaml.safe_load(index_path.read_text(encoding="utf-8"))
                    mutate(document, index)
                    document_path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
                    index_path.write_text(yaml.safe_dump(index, sort_keys=False), encoding="utf-8")
                    result = run_tool(skill, "validate_product_intent.py", package, "--no-report")
                    errors = yaml.safe_load(result.stdout)["errors"]
                    with self.subTest(skill=skill, path=relative):
                        self.assertNotEqual(0, result.returncode)
                        self.assertIn(expected_error, errors)

    def test_validator_allows_governance_ids_and_external_source_evidence(self) -> None:
        for skill in SKILLS:
            source = ROOT / skill / "assets/example-product-intent-package"
            with tempfile.TemporaryDirectory() as temp_dir:
                package = Path(temp_dir) / "package"
                shutil.copytree(source, package)
                evidence_path = package / "governance/evidence.yaml"
                evidence = yaml.safe_load(evidence_path.read_text(encoding="utf-8"))
                evidence["evidence"][0]["claims"].extend(
                    [
                        "AUTH-001",
                        "EVID-001",
                        "DEC-001",
                        "Q-001",
                        "CON-001",
                        "CHANGE-001",
                    ]
                )
                evidence_path.write_text(yaml.safe_dump(evidence, sort_keys=False), encoding="utf-8")
                source_evidence = package / "source-evidence"
                source_evidence.mkdir()
                (source_evidence / "original.yaml").write_text(
                    "id: PATTERN-001\nlabel: ARCH-003A\n", encoding="utf-8"
                )
                stamp = run_tool(skill, "stamp_package_hash.py", package)
                result = run_tool(skill, "validate_product_intent.py", package, "--no-report")
                with self.subTest(skill=skill):
                    self.assertEqual(0, stamp.returncode, stamp.stderr)
                    self.assertEqual(0, result.returncode, result.stdout)

    def test_validator_rejects_unknown_ids_in_canonical_text_tokens(self) -> None:
        cases = (
            (
                "product/context.md",
                "The canonical package must reject PATTERN-001 in prose.\n",
                "product/context.md: unsupported canonical ID prefix 'PATTERN' in 'PATTERN-001'",
            ),
            (
                "governance/evidence.yaml",
                "ARCH-003A",
                "governance/evidence.yaml: canonical ID 'ARCH-003A' must end with digits",
            ),
        )
        for skill in SKILLS:
            source = ROOT / skill / "assets/example-product-intent-package"
            for relative, token_or_addition, expected_error in cases:
                with tempfile.TemporaryDirectory() as temp_dir:
                    package = Path(temp_dir) / "package"
                    shutil.copytree(source, package)
                    path = package / relative
                    if relative.endswith(".yaml"):
                        document = yaml.safe_load(path.read_text(encoding="utf-8"))
                        document["evidence"][0]["claims"].append(
                            f"Embedded YAML text contains {token_or_addition}."
                        )
                        path.write_text(
                            yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
                        )
                    else:
                        path.write_text(
                            path.read_text(encoding="utf-8") + token_or_addition,
                            encoding="utf-8",
                        )
                    result = run_tool(skill, "validate_product_intent.py", package, "--no-report")
                    errors = yaml.safe_load(result.stdout)["errors"]
                    with self.subTest(skill=skill, path=relative):
                        self.assertNotEqual(0, result.returncode)
                        self.assertIn(expected_error, errors)

    def test_validator_requires_non_capability_scope_traceability(self) -> None:
        cases = (
            (
                "behavior/rules.yaml",
                "rules",
                "RULE-001",
                "governed_by",
                "API-001",
                "scope_ids",
            ),
            (
                "quality/constraints.yaml",
                "constraints",
                "QC-001",
                "constrained_by",
                "API-001",
                "scope_ids",
            ),
        )
        for skill in SKILLS:
            source = ROOT / skill / "assets/example-product-intent-package"
            for relative, collection, record_id, relation, scope_id, field in cases:
                with tempfile.TemporaryDirectory() as temp_dir:
                    package = Path(temp_dir) / "package"
                    shutil.copytree(source, package)
                    declaration_path = package / relative
                    declaration = yaml.safe_load(declaration_path.read_text(encoding="utf-8"))
                    record = next(item for item in declaration[collection] if item["id"] == record_id)
                    if scope_id not in record[field]:
                        record[field].append(scope_id)
                    declaration_path.write_text(
                        yaml.safe_dump(declaration, sort_keys=False), encoding="utf-8"
                    )
                    trace_path = package / "verification/traceability.yaml"
                    trace = yaml.safe_load(trace_path.read_text(encoding="utf-8"))
                    expected_edge = {
                        "from": scope_id,
                        "relation": relation,
                        "to": record_id,
                    }
                    quality_edge = {
                        "from": "API-001",
                        "relation": "constrained_by",
                        "to": "QC-001",
                    }
                    if quality_edge not in trace["edges"]:
                        trace["edges"].append(quality_edge)
                    if expected_edge not in trace["edges"]:
                        trace["edges"].append(expected_edge)
                    trace_path.write_text(yaml.safe_dump(trace, sort_keys=False), encoding="utf-8")
                    stamp = run_tool(skill, "stamp_package_hash.py", package)
                    with self.subTest(skill=skill, record=record_id, phase="complete"):
                        self.assertEqual(0, stamp.returncode, stamp.stderr)
                    complete = run_tool(skill, "validate_product_intent.py", package, "--no-report")
                    with self.subTest(skill=skill, record=record_id, phase="complete"):
                        self.assertEqual(0, complete.returncode, complete.stdout)

                    trace = yaml.safe_load(trace_path.read_text(encoding="utf-8"))
                    trace["edges"].remove(expected_edge)
                    trace_path.write_text(yaml.safe_dump(trace, sort_keys=False), encoding="utf-8")
                    stamp = run_tool(skill, "stamp_package_hash.py", package)
                    result = run_tool(skill, "validate_product_intent.py", package, "--no-report")
                    errors = yaml.safe_load(result.stdout)["errors"]
                    with self.subTest(skill=skill, record=record_id, phase="missing"):
                        self.assertEqual(0, stamp.returncode, stamp.stderr)
                        self.assertNotEqual(0, result.returncode)
                        self.assertIn(
                            f"{record_id}: {field} missing traceability edge "
                            f"{scope_id} -[{relation}]-> {record_id}",
                            errors,
                        )

    def test_validator_rejects_artifact_paths_outside_package(self) -> None:
        for skill in SKILLS:
            source = ROOT / skill / "assets/example-product-intent-package"
            with tempfile.TemporaryDirectory() as temp_dir:
                package = Path(temp_dir) / "package"
                shutil.copytree(source, package)
                index_path = package / "governance/artifact-index.yaml"
                index = yaml.safe_load(index_path.read_text(encoding="utf-8"))
                artifact = next(item for item in index["artifacts"] if item["id"] == "DOM-001")
                artifact["path"] = "../DOM-001.yaml"
                index_path.write_text(yaml.safe_dump(index, sort_keys=False), encoding="utf-8")
                (package.parent / "DOM-001.yaml").write_text("id: DOM-001\n", encoding="utf-8")
                stamp = run_tool(skill, "stamp_package_hash.py", package)
                result = run_tool(skill, "validate_product_intent.py", package, "--no-report")
                errors = yaml.safe_load(result.stdout)["errors"]
                with self.subTest(skill=skill):
                    self.assertEqual(0, stamp.returncode, stamp.stderr)
                    self.assertNotEqual(0, result.returncode)
                    self.assertIn(
                        "DOM-001: artifact path must stay inside package: ../DOM-001.yaml",
                        errors,
                    )

    def test_initializer_writes_yaml_manifest(self) -> None:
        for skill in SKILLS:
            with tempfile.TemporaryDirectory() as temp_dir:
                destination = Path(temp_dir) / "new-package"
                result = run_tool(
                    skill,
                    "init_product_intent.py",
                    destination,
                    "--name",
                    "Example Product",
                    "--target-version",
                    "2.3.4",
                    "--baseline",
                    "greenfield",
                )
                with self.subTest(skill=skill, stderr=result.stderr):
                    self.assertEqual(0, result.returncode)
                    manifest = yaml.safe_load(
                        (destination / "manifest.yaml").read_text(encoding="utf-8")
                    )
                    self.assertEqual("Example Product", manifest["product"]["name"])
                    self.assertEqual("2.3.4", manifest["product"]["target_version"])
                    self.assertEqual("3.0.0", manifest["schema_version"])

    def test_hash_stamping_preserves_valid_example(self) -> None:
        for skill in SKILLS:
            source = ROOT / skill / "assets/example-product-intent-package"
            with tempfile.TemporaryDirectory() as temp_dir:
                package = Path(temp_dir) / "package"
                shutil.copytree(source, package)
                stamp = run_tool(skill, "stamp_package_hash.py", package)
                validate = run_tool(skill, "validate_product_intent.py", package, "--no-report")
                with self.subTest(skill=skill, stderr=stamp.stderr + validate.stderr):
                    self.assertEqual(0, stamp.returncode)
                    self.assertEqual(0, validate.returncode, validate.stdout)

    def test_manager_impact_analysis_emits_yaml(self) -> None:
        package = ROOT / "skills/product-intent-manager/assets/example-product-intent-package"
        result = run_tool(
            "skills/product-intent-manager",
            "impact_analysis.py",
            package,
            "CAP-001",
            "--reverse",
        )
        self.assertEqual(0, result.returncode, result.stderr)
        output = yaml.safe_load(result.stdout)
        self.assertEqual(["CAP-001"], output["changed_ids"])
        self.assertIn("ACC-001", output["affected_ids"])

    def test_inventory_emits_yaml_and_keeps_legacy_source_types(self) -> None:
        skill = "skills/reconstruct-product-intent"
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            project = root / "project"
            project.mkdir()
            (project / "source.json").write_text("{}\n", encoding="utf-8")
            (project / "diagram.mmd").write_text("flowchart LR\n", encoding="utf-8")
            output_path = root / "inventory.yaml"
            result = run_tool(
                skill,
                "inventory_existing_project.py",
                project,
                "--output",
                output_path,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            inventory = yaml.safe_load(output_path.read_text(encoding="utf-8"))
            paths = {item["path"] for item in inventory["files"]}
            self.assertEqual({"diagram.mmd", "source.json"}, paths)

    def test_inventory_rejects_non_yaml_output_name(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            project = root / "project"
            project.mkdir()
            result = run_tool(
                "skills/reconstruct-product-intent",
                "inventory_existing_project.py",
                project,
                "--output",
                root / "inventory.json",
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn(".yaml", result.stderr)

    def test_shared_package_assets_stay_identical(self) -> None:
        left = ROOT / SKILLS[0] / "assets"
        right = ROOT / SKILLS[1] / "assets"
        left_files = {path.relative_to(left) for path in left.rglob("*") if path.is_file()}
        right_files = {path.relative_to(right) for path in right.rglob("*") if path.is_file()}
        self.assertEqual(left_files, right_files)
        for relative in sorted(left_files):
            with self.subTest(path=relative):
                self.assertEqual((left / relative).read_bytes(), (right / relative).read_bytes())

    def test_shared_skill_files_stay_identical(self) -> None:
        left = ROOT / SKILLS[0]
        right = ROOT / SKILLS[1]
        for folder, names in (
            ("references", SHARED_REFERENCES),
            ("scripts", SHARED_SCRIPTS),
        ):
            for name in names:
                relative = Path(folder) / name
                with self.subTest(path=relative):
                    self.assertTrue((left / relative).is_file())
                    self.assertEqual(
                        (left / relative).read_bytes(),
                        (right / relative).read_bytes(),
                    )


if __name__ == "__main__":
    unittest.main()
