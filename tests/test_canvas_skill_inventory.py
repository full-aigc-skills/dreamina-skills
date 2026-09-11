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


def skill_text(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


def skill_openai_yaml(name: str) -> dict:
    import yaml  # type: ignore[import-not-found]

    return yaml.safe_load((SKILLS / name / "agents" / "openai.yaml").read_text(encoding="utf-8"))


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

    def test_cli_skill_owns_cross_cutting_invariants(self) -> None:
        text = skill_text("dreamina-canvas-cli")
        for token in ("--format json", "requiredAction", "submitId", "exit code 20", "stdout", "stderr"):
            self.assertIn(token, text, token)

    def test_cli_skill_is_explicit_only(self) -> None:
        policy = skill_openai_yaml("dreamina-canvas-cli")["policy"]
        self.assertEqual(policy["allow_implicit_invocation"], False)

    def test_auth_distinguishes_local_and_server_identity(self) -> None:
        text = skill_text("dreamina-canvas-auth")
        self.assertIn("auth status", text)
        self.assertIn("auth account", text)
        self.assertIn("local", text.lower())
        self.assertIn("server", text.lower())
        self.assertIn("token", text.lower())
        # The skill must explicitly forbid persisting or echoing tokens
        self.assertIn("never", text.lower())
        # --profile isolation must be present
        self.assertIn("--profile", text)
        # auth wait is the recovery path, not auth login
        self.assertIn("auth wait", text)

    def test_auth_skill_is_explicit_only(self) -> None:
        policy = skill_openai_yaml("dreamina-canvas-auth")["policy"]
        self.assertEqual(policy["allow_implicit_invocation"], False)


if __name__ == "__main__":
    unittest.main()
