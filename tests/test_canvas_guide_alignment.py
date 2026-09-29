"""Guide examples remain discoverable after granular skill installation."""

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


MIGRATION = {item["from"]: item for item in json.loads(
    (ROOT / "verification/dreamina-canvas-atomic-migration.json").read_text()
)["retired"]}


class CanvasGuideAlignmentTests(unittest.TestCase):
    def test_setup_is_packaged_and_covers_first_use(self) -> None:
        setup = SKILLS / "dreamina-canvas-cli-setup"
        entry = (setup / "SKILL.md").read_text(encoding="utf-8")
        example = (setup / "examples" / "happy-path.md").read_text(encoding="utf-8")
        manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        self.assertIn("./skills/dreamina-canvas-cli-setup", manifest["skills"])
        for token in ("dreamina-canvas", "dreamina-canvas --help", "dreamina-canvas version", "dreamina-canvas schema", "auth account"):
            self.assertIn(token, entry + example)
        for token in ("install.sh", "install.ps1", "install.bat", "PATH"):
            self.assertIn(token, entry + example)

    def test_guide_command_examples_are_owned_by_canvas_skills(self) -> None:
        expected = {
            "dreamina-canvas-auth": ("auth login", "auth account"),
            "dreamina-canvas-cli": ("dreamina-canvas --help", "dreamina-canvas version"),
            "dreamina-canvas-discover-models": ("model list", "model find", "voice list"),
            "dreamina-canvas-create": ("canvas create", "canvas ls"),
            "dreamina-canvas-download-assets": ("resource upload", "resource get", "resource download"),
            "dreamina-canvas-generate-image": ("node create image", "--mode t2i", "--mode i2i", "node find", "node edit image", "node upscale image"),
            "dreamina-canvas-generate-video": ("node create video", "--mode t2v", "--mode m2v", "--mode first_last_frame"),
            "dreamina-canvas-generate-audio": ("node create audio", "--mode tts", "--mode music"),
            "dreamina-canvas-compose": ("node create text", "node create element"),
            "dreamina-canvas-manage-timeline": ("node create timeline", "--clip", "--audio-clip"),
            "dreamina-canvas-quote-and-run": ("node quote", "node confirm", "node run"),
            "dreamina-canvas-resume-operation": ("operation status", "operation wait"),
            "dreamina-canvas-use": ("--run", "resource download"),
        }
        for name, commands in expected.items():
            with self.subTest(skill=name):
                entry = MIGRATION.get(name)
                owner = entry["to"] if entry else name
                example = "\n".join(p.read_text() for p in (SKILLS / owner / "examples").glob("*.md"))
                self.assertIn("```bash", example)
                for command in commands:
                    self.assertIn(command, example)


if __name__ == "__main__":
    unittest.main()
