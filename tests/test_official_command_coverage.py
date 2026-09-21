import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
CANVAS_COVERAGE = ROOT / "verification" / "dreamina-canvas-command-coverage.json"
CLI_COVERAGE = ROOT / "verification" / "dreamina-cli-command-coverage.json"


CANVAS_COMMANDS = {
    "install-cn", "install-oversea", "help", "version", "schema",
    "auth login", "auth wait", "auth account", "auth status", "auth refresh", "auth logout",
    "model search", "model list", "model detail", "voice list",
    "canvas create", "canvas ls",
    "node create image", "node edit image", "node create video", "node edit video",
    "node create audio", "node edit audio", "node create text", "node edit text",
    "node create element", "node edit element", "node create timeline", "node edit timeline",
    "node find", "node show", "node quote", "node confirm", "node run", "node upscale image",
    "operation status", "operation wait",
    "resource get", "resource download", "resource upload",
}

CLI_COMMANDS = {
    "install", "help", "version", "login", "login headless", "login checklogin",
    "relogin", "logout", "user_credit", "text2image", "image2image", "text2video",
    "image2video", "frames2video", "multiframe2video", "multimodal2video", "image_upscale",
    "query_result", "query_result download", "list_task", "session create", "session list",
    "session search", "session rename", "session delete",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def skill_corpus(name: str) -> str:
    root = SKILLS / name
    parts = [(root / "SKILL.md").read_text(encoding="utf-8")]
    refs = root / "references"
    if refs.is_dir():
        parts.extend(p.read_text(encoding="utf-8") for p in sorted(refs.rglob("*.md")))
    return "\n".join(parts)


class OfficialCommandCoverageTests(unittest.TestCase):
    def assert_coverage(self, path: Path, expected: set[str]) -> None:
        data = load(path)
        entries = data["commands"]
        self.assertEqual({entry["id"] for entry in entries}, expected)
        for entry in entries:
            with self.subTest(command=entry["id"]):
                owner = entry["ownerSkill"]
                self.assertTrue((SKILLS / owner / "SKILL.md").is_file(), owner)
                self.assertIn(entry["evidenceToken"], skill_corpus(owner))
                for support in entry.get("supportingSkills", []):
                    self.assertTrue((SKILLS / support / "SKILL.md").is_file(), support)
                    self.assertIn(support, skill_corpus(owner))

    def test_canvas_official_commands_have_owners_and_evidence(self) -> None:
        self.assert_coverage(CANVAS_COVERAGE, CANVAS_COMMANDS)

    def test_classic_cli_official_commands_have_owners_and_evidence(self) -> None:
        self.assert_coverage(CLI_COVERAGE, CLI_COMMANDS)


if __name__ == "__main__":
    unittest.main()
