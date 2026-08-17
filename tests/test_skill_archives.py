from __future__ import annotations

import hashlib
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SKILLS = ("reconstruct-product-intent", "product-intent-manager")


class SkillArchiveTests(unittest.TestCase):
    def test_archives_match_sources_and_checksums(self) -> None:
        checksums = self._checksums()

        for skill in SKILLS:
            archive = DIST / f"{skill}.zip"
            with self.subTest(skill=skill):
                self.assertTrue(archive.is_file())
                self.assertEqual(checksums[archive.name], self._sha256(archive))

                source_root = ROOT / "skills" / skill
                source_files = {
                    path.relative_to(source_root).as_posix(): path.read_bytes()
                    for path in source_root.rglob("*")
                    if path.is_file()
                    and "__pycache__" not in path.parts
                    and path.suffix != ".pyc"
                    and path.name != ".DS_Store"
                }

                with zipfile.ZipFile(archive) as bundle:
                    self.assertIsNone(bundle.testzip())
                    archived_files = {
                        info.filename.removeprefix(f"{skill}/"): bundle.read(info)
                        for info in bundle.infolist()
                        if not info.is_dir()
                    }
                    self.assertTrue(
                        all(info.filename.startswith(f"{skill}/") for info in bundle.infolist())
                    )
                    self.assertFalse(
                        any(
                            "__pycache__" in info.filename
                            or info.filename.endswith(".pyc")
                            or info.filename.endswith(".DS_Store")
                            for info in bundle.infolist()
                        )
                    )

                self.assertEqual(source_files, archived_files)

    def test_archives_are_reproducible(self) -> None:
        for skill in SKILLS:
            with tempfile.TemporaryDirectory() as temp_dir:
                regenerated = Path(temp_dir) / f"{skill}.zip"
                result = subprocess.run(
                    [
                        "git",
                        "archive",
                        "--format=zip",
                        f"--prefix={skill}/",
                        "--mtime=1980-01-01T00:00:00Z",
                        f"--output={regenerated}",
                        f"HEAD:skills/{skill}",
                    ],
                    cwd=ROOT,
                    check=False,
                    capture_output=True,
                    text=True,
                )
                with self.subTest(skill=skill, stderr=result.stderr):
                    self.assertEqual(0, result.returncode)
                    self.assertEqual(
                        (DIST / f"{skill}.zip").read_bytes(),
                        regenerated.read_bytes(),
                    )

    def _checksums(self) -> dict[str, str]:
        checksum_file = DIST / "SHA256SUMS"
        self.assertTrue(checksum_file.is_file())
        checksums: dict[str, str] = {}
        for line in checksum_file.read_text(encoding="utf-8").splitlines():
            digest, name = line.split(maxsplit=1)
            checksums[name.lstrip("* ")] = digest
        self.assertEqual({f"{skill}.zip" for skill in SKILLS}, set(checksums))
        return checksums

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    unittest.main()
