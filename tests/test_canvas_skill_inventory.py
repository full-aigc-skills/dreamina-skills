import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
CONTRACT = ROOT / "verification" / "dreamina-canvas-guide-contract.json"


CANVAS_SKILLS = {
    "dreamina-canvas-cli",
    "dreamina-canvas-auth",
    "dreamina-canvas-discover-models",
    "dreamina-canvas-create",
    "dreamina-canvas-compose",
    "dreamina-canvas-generate-image",
    "dreamina-canvas-generate-video",
    "dreamina-canvas-generate-audio",
    "dreamina-canvas-manage-timeline",
    "dreamina-canvas-quote-and-run",
    "dreamina-canvas-resume-operation",
    "dreamina-canvas-download-assets",
    "dreamina-canvas-use",
}


class CanvasSkillInventoryTests(unittest.TestCase):
    def test_canvas_skill_inventory_is_complete(self) -> None:
        actual = {
            path.name
            for path in SKILLS.iterdir()
            if path.is_dir() and path.name.startswith("dreamina-canvas-")
        }
        self.assertEqual(actual, CANVAS_SKILLS)

    def test_guide_contract_is_complete_and_seed_only(self) -> None:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        self.assertIn("dreamina-canvas", contract["source"])
        self.assertIn("2026-09-11", contract["source"])
        self.assertEqual(
            set(contract["commandFamilies"]),
            {"auth", "model", "voice", "canvas", "node", "operation", "resource", "schema", "version"},
        )
        self.assertEqual(
            set(contract["exitCodes"]),
            {0, 1, 2, 11, 12, 13, 20, 21, 22},
        )
        self.assertEqual(
            set(contract["requiredActions"]),
            {
                "none",
                "login",
                "confirm",
                "retry",
                "resume",
                "upgrade",
                "human_intervention",
                "contact_support",
            },
        )
        self.assertNotIn("models", contract)
        self.assertNotIn("voices", contract)

    def test_schema_root_fixture_exposes_command_families(self) -> None:
        schema = json.loads(
            (ROOT / "tests" / "fixtures" / "dreamina_canvas" / "schema-root.json").read_text(
                encoding="utf-8"
            )
        )
        for family in ("auth", "model", "voice", "canvas", "node", "operation", "resource"):
            self.assertIn(family, schema["commands"], family)


if __name__ == "__main__":
    unittest.main()
