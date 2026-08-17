from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = (
    "skills/reconstruct-product-intent",
    "skills/product-intent-manager",
)


def run_stamp(skill: str, package: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / skill / "scripts/stamp_package_hash.py"),
            str(package),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


class StampSymlinkSafetyTests(unittest.TestCase):
    def test_rejects_symlink_to_outside_file_before_reading_or_hashing(self) -> None:
        for skill in SKILLS:
            source = ROOT / skill / "assets/example-product-intent-package"
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_root = Path(temp_dir)
                package = temp_root / "package"
                shutil.copytree(source, package)
                (package / "source-evidence").mkdir()
                outside = temp_root / "outside.yaml"
                outside.write_text("sentinel: MUST_NOT_BE_READ\n", encoding="utf-8")
                link = package / "source-evidence" / "outside.yaml"
                link.symlink_to(outside)
                readiness = package / "handoff/readiness.yaml"
                original_readiness = readiness.read_bytes()

                result = run_stamp(skill, package)

                with self.subTest(skill=skill, stderr=result.stderr):
                    self.assertNotEqual(0, result.returncode)
                    self.assertIn("symbolic link", result.stderr.lower())
                    self.assertNotIn("MUST_NOT_BE_READ", result.stdout + result.stderr)
                    self.assertEqual(original_readiness, readiness.read_bytes())

    def test_rejects_symlink_to_outside_directory_anywhere_in_package(self) -> None:
        for skill in SKILLS:
            source = ROOT / skill / "assets/example-product-intent-package"
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_root = Path(temp_dir)
                package = temp_root / "package"
                shutil.copytree(source, package)
                (package / "source-evidence").mkdir()
                outside = temp_root / "outside-directory"
                outside.mkdir()
                (outside / "sentinel.txt").write_text(
                    "MUST_NOT_BE_READ\n",
                    encoding="utf-8",
                )
                link = package / "source-evidence" / "outside-directory"
                link.symlink_to(outside, target_is_directory=True)
                readiness = package / "handoff/readiness.yaml"
                original_readiness = readiness.read_bytes()

                result = run_stamp(skill, package)

                with self.subTest(skill=skill, stderr=result.stderr):
                    self.assertNotEqual(0, result.returncode)
                    self.assertIn("symbolic link", result.stderr.lower())
                    self.assertNotIn("MUST_NOT_BE_READ", result.stdout + result.stderr)
                    self.assertEqual(original_readiness, readiness.read_bytes())


if __name__ == "__main__":
    unittest.main()
