import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

EXPECTED_SKILLS = {
    # Pre-existing 12 Dreamina skills
    "dreamina-cli",
    "dreamina-cli-image2image",
    "dreamina-cli-image2video",
    "dreamina-cli-text2image",
    "dreamina-cli-text2video",
    "dreamina-opencli-image2image",
    "dreamina-opencli-image2video",
    "dreamina-opencli-text2image",
    "dreamina-opencli-text2video",
    "dreamina-prompt-image2image",
    "dreamina-prompt-image2video",
    "dreamina-prompt-text2image",
    "dreamina-prompt-text2video",
    # 13 new Canvas skills (Tasks 2-14)
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

VIDEO_COMMANDS = {
    "text2video",
    "image2video",
    "frames2video",
    "multimodal2video",
}


def frontmatter_name(path: Path) -> str:
    match = re.search(r"(?m)^name:\s*[\"']?([^\n\"']+)", path.read_text(encoding="utf-8"))
    if match is None:
        raise AssertionError(f"missing frontmatter name: {path}")
    return match.group(1).strip()


class DreaminaMigrationTests(unittest.TestCase):
    def test_all_installable_skill_identities_use_dreamina_prefix(self) -> None:
        actual = {path.name for path in SKILLS.iterdir() if path.is_dir()}
        self.assertEqual(actual, EXPECTED_SKILLS)
        for name in sorted(actual):
            self.assertEqual(frontmatter_name(SKILLS / name / "SKILL.md"), name)

    def test_repository_metadata_uses_dreamina_skills_identity(self) -> None:
        for filename in ("README.md", "README.zh-CN.md"):
            text = (ROOT / filename).read_text(encoding="utf-8")
            self.assertIn("full-aigc-skills/dreamina-skills", text)
            self.assertNotIn("full-aigc-skills/jimeng-skills", text)
            self.assertNotRegex(text, r"`jimeng-[a-z0-9-]+`")

    def test_cli_contract_is_v1418_and_video_ratio_is_discovered(self) -> None:
        contract = json.loads(
            (ROOT / "verification" / "dreamina-cli-v1.4.18-contract.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(contract["documentedRelease"], "1.4.18")
        self.assertEqual(contract["commandsWithRatio"], sorted(VIDEO_COMMANDS))
        self.assertEqual(contract["source"], "installed-cli-help")
        self.assertTrue(contract["binaryCommit"])
        behavior = contract["commandBehavior"]
        self.assertFalse(behavior["multiframe2video"]["ratioFlag"])
        self.assertIn("first image", behavior["multiframe2video"]["default"])
        self.assertIn("rejected", behavior["image2video"]["seedance2.5"])
        self.assertIn("rejected", behavior["frames2video"]["seedance2.5"])
        self.assertEqual(behavior["text2video"]["default"], "16:9")
        self.assertEqual(behavior["multimodal2video"]["default"], "16:9")

    def test_video_cli_skills_require_runtime_ratio_discovery(self) -> None:
        targets = (
            "dreamina-cli",
            "dreamina-cli-image2video",
            "dreamina-cli-text2video",
        )
        for name in targets:
            text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("--ratio", text, name)
            self.assertRegex(text, r"运行时|runtime", name)
            self.assertRegex(text, r"--help|schema", name)


if __name__ == "__main__":
    unittest.main()
