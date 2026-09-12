import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
SUITE_JSON = ROOT / "verification" / "dreamina-canvas-skill-suite.json"

EXPECTED_CANVAS = {
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

EXPECTED_EXISTING = {
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
}


class CanvasSuiteValidationTests(unittest.TestCase):
    def test_skill_count_is_26(self) -> None:
        actual = {p.name for p in SKILLS.iterdir() if p.is_dir()}
        self.assertEqual(len(actual), 26)
        self.assertEqual(actual, EXPECTED_CANVAS | EXPECTED_EXISTING)

    def test_implicit_invocation_is_only_use(self) -> None:
        import yaml  # type: ignore[import-not-found]

        for name in EXPECTED_CANVAS:
            policy_path = SKILLS / name / "agents" / "openai.yaml"
            policy = yaml.safe_load(policy_path.read_text(encoding="utf-8"))["policy"]
            self.assertIn("allow_implicit_invocation", policy, name)
            expected = name == "dreamina-canvas-use"
            self.assertEqual(
                policy["allow_implicit_invocation"], expected, name
            )

    def test_runtime_boundary_recorded(self) -> None:
        suite = json.loads(SUITE_JSON.read_text(encoding="utf-8"))
        boundary = suite["runtimeBoundary"]
        self.assertEqual(boundary["cli_runtime"], "PASS")
        self.assertEqual(boundary["auth"], "NOT_RUN")
        self.assertEqual(boundary["paid_canary"], "NOT_RUN")

    def test_canvas_skill_frontmatter_matches_dirname(self) -> None:
        for name in EXPECTED_CANVAS:
            text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
            match = re.search(r"(?m)^name:\s*[\"']?([^\n\"']+)", text)
            self.assertIsNotNone(match, name)
            self.assertEqual(match.group(1).strip(), name)


if __name__ == "__main__":
    unittest.main()
