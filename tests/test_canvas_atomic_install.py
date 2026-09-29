"""Verify command dispatch resolves after helper skills leave the package."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "dreamina-canvas-cli"
ENTRIES = {BASE} | {BASE + "-" + suffix for suffix in (
    "setup", "auth", "text2image", "image2image", "text2video",
    "ref2video", "text2voice", "text2audio",
)}


class AtomicInstallTests(unittest.TestCase):
    def test_command_dispatch_uses_retained_cli_entries(self):
        coverage = json.loads((ROOT / "verification/dreamina-canvas-command-coverage.json").read_text())
        for command in coverage["commands"]:
            with self.subTest(command=command["id"]):
                self.assertIn(command["ownerSkill"], ENTRIES)
                self.assertTrue((ROOT / "skills" / command["ownerSkill"] / "SKILL.md").is_file())

    def test_each_cli_skill_installs_without_sibling_resources(self):
        for name in sorted(ENTRIES):
            with self.subTest(skill=name), tempfile.TemporaryDirectory() as work:
                shutil.copytree(ROOT / "skills" / name, Path(work) / "skills" / name)
                result = subprocess.run(
                    [sys.executable, str(ROOT / "scripts/verify_skill_package.py")],
                    cwd=work, capture_output=True, text=True,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_mode_routes_have_one_owner(self):
        coverage = json.loads((ROOT / "verification/dreamina-canvas-command-coverage.json").read_text())
        expected = {"t2i": "text2image", "i2i": "image2image", "t2v": "text2video",
                    "m2v": "ref2video", "first_last_frame": "ref2video",
                    "tts": "text2voice", "music": "text2audio"}
        self.assertEqual(coverage.get("modeOwners"), {k: BASE + "-" + v for k, v in expected.items()})

    def test_retired_entries_resolve_to_packaged_operation_documents(self):
        migration = json.loads((ROOT / "verification/dreamina-canvas-atomic-migration.json").read_text())
        manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        for item in migration["retired"]:
            with self.subTest(skill=item["from"]):
                self.assertFalse((ROOT / "skills" / item["from"]).exists())
                self.assertNotIn("./skills/" + item["from"], manifest["skills"])
                self.assertIn("./skills/" + item["to"], manifest["skills"])
                self.assertTrue((ROOT / "skills" / item["to"] / item["operationDocument"]).is_file())

    def test_no_duplicate_command_dispatch_keys(self):
        coverage = json.loads((ROOT / "verification/dreamina-canvas-command-coverage.json").read_text())
        ids = [entry["id"] for entry in coverage["commands"]]
        self.assertEqual(len(ids), len(set(ids)), "ambiguous command ownership")
