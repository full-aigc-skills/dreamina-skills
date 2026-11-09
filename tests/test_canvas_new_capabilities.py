"""Guard the routing and command ownership added by the Canvas CLI updates."""

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def corpus(name: str) -> str:
    root = SKILLS / name
    return "\n".join(path.read_text(encoding="utf-8") for path in sorted(root.rglob("*.md")))


class CanvasNewCapabilityTests(unittest.TestCase):
    def test_new_command_families_have_owners(self) -> None:
        coverage = json.loads(
            (ROOT / "verification/dreamina-canvas-command-coverage.json").read_text(encoding="utf-8")
        )
        owners = {row["id"]: row["ownerSkill"] for row in coverage["commands"]}
        expected = {
            "team ls": "dreamina-canvas-cli",
            "space use": "dreamina-canvas-cli",
            "space current": "dreamina-canvas-cli",
            "node promote video-sample": "dreamina-canvas-cli-ref2video",
            "node cutout image": "dreamina-canvas-cli-image2image",
            "node upscale video": "dreamina-canvas-cli-ref2video",
            "node interpolate video": "dreamina-canvas-cli-ref2video",
            "node delete": "dreamina-canvas-cli",
            "director": "dreamina-canvas-cli",
            "workflow capabilities": "dreamina-canvas-cli",
            "workflow quote": "dreamina-canvas-cli",
            "workflow confirm": "dreamina-canvas-cli",
            "workflow run": "dreamina-canvas-cli",
            "workflow template instantiate": "dreamina-canvas-cli",
        }
        for command, owner in expected.items():
            with self.subTest(command=command):
                self.assertEqual(owners.get(command), owner)
                self.assertIn(command, corpus(owner))

    def test_v13_workflow_is_version_gated(self) -> None:
        entry = (SKILLS / "dreamina-canvas-cli" / "SKILL.md").read_text(encoding="utf-8")
        guide = (SKILLS / "dreamina-canvas-cli" / "references" / "new-capabilities.md").read_text(encoding="utf-8")
        self.assertIn("new-capabilities.md", entry)
        for token in ("1.3.0", "schema", "--help", "工作流", "模板", "workflow-and-templates.md"):
            self.assertIn(token, guide)
        self.assertIn("1.2.0", guide)
        self.assertIn("不得", guide)


if __name__ == "__main__":
    unittest.main()
