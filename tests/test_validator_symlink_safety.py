from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("skills/reconstruct-product-intent", "skills/product-intent-manager")


class ValidatorSymlinkSafetyTests(unittest.TestCase):
    def test_validator_does_not_write_reports_through_a_symlink(self) -> None:
        for skill in SKILLS:
            with self.subTest(skill=skill), tempfile.TemporaryDirectory() as temp_dir:
                temp_root = Path(temp_dir)
                source = ROOT / skill / "assets/example-product-intent-package"
                package = temp_root / "package"
                shutil.copytree(source, package)
                outside = temp_root / "outside"
                outside.mkdir()
                handoff = package / "handoff"
                shutil.rmtree(handoff)
                handoff.symlink_to(outside, target_is_directory=True)

                result = subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / skill / "scripts/validate_product_intent.py"),
                        str(package),
                    ],
                    cwd=ROOT,
                    check=False,
                    capture_output=True,
                    text=True,
                )

                self.assertNotEqual(0, result.returncode)
                self.assertFalse((outside / "readiness-report.generated.yaml").exists())
                self.assertFalse((outside / "readiness-report.generated.md").exists())

    def test_validator_rejects_a_symlink_package_root(self) -> None:
        for skill in SKILLS:
            with self.subTest(skill=skill), tempfile.TemporaryDirectory() as temp_dir:
                temp_root = Path(temp_dir)
                source = ROOT / skill / "assets/example-product-intent-package"
                actual_package = temp_root / "actual-package"
                shutil.copytree(source, actual_package)
                package = temp_root / "package"
                package.symlink_to(actual_package, target_is_directory=True)

                result = subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / skill / "scripts/validate_product_intent.py"),
                        str(package),
                        "--no-report",
                    ],
                    cwd=ROOT,
                    check=False,
                    capture_output=True,
                    text=True,
                )

                self.assertNotEqual(0, result.returncode)
                report = yaml.safe_load(result.stdout)
                self.assertTrue(
                    any("symbolic links are not allowed" in error for error in report["errors"]),
                    report["errors"],
                )

    def test_validator_rejects_symlinks_before_it_reads_their_targets(self) -> None:
        for skill in SKILLS:
            with self.subTest(skill=skill), tempfile.TemporaryDirectory() as temp_dir:
                temp_root = Path(temp_dir)
                source = ROOT / skill / "assets/example-product-intent-package"
                package = temp_root / "package"
                shutil.copytree(source, package)

                outside = temp_root / "outside.md"
                outside.write_text("API-987\n", encoding="utf-8")
                journey_source = package / "experience/journeys/JOURNEY-001.md"
                journey_source.unlink()
                journey_source.symlink_to(outside)

                result = subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / skill / "scripts/validate_product_intent.py"),
                        str(package),
                        "--no-report",
                    ],
                    cwd=ROOT,
                    check=False,
                    capture_output=True,
                    text=True,
                )

                self.assertNotEqual(0, result.returncode)
                report = yaml.safe_load(result.stdout)
                self.assertTrue(
                    any("symbolic links are not allowed" in error for error in report["errors"]),
                    report["errors"],
                )
                self.assertNotIn("API-987", result.stdout)
                self.assertNotIn("API-987", result.stderr)


if __name__ == "__main__":
    unittest.main()
