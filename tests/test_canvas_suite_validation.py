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

EXPECTED_ORCHESTRATION = {
    "dreamina-3d-auto-seedance",
    "dreamina-3d-from-blender",
    "dreamina-3d-from-maya",
    "dreamina-3d-jimeng-web",
    "dreamina-3d-resume",
    "dreamina-3d-use",
    "dreamina-design-use",
    "dreamina-shot-annotator",
    "dreamina-video-evaluator",
    "dreamina-video-production",
}


def implicit_invocation_policy(name: str) -> bool:
    text = (SKILLS / name / "agents" / "openai.yaml").read_text(encoding="utf-8")
    match = re.search(r"(?m)^\s*allow_implicit_invocation:\s*(true|false)\s*$", text)
    if match is None:
        raise AssertionError(f"missing allow_implicit_invocation: {name}")
    return match.group(1) == "true"


class CanvasSuiteValidationTests(unittest.TestCase):
    def test_skill_count_is_36(self) -> None:
        actual = {p.name for p in SKILLS.iterdir() if p.is_dir()}
        self.assertEqual(len(actual), 36)
        self.assertEqual(actual, EXPECTED_CANVAS | EXPECTED_EXISTING | EXPECTED_ORCHESTRATION)

    def test_implicit_invocation_is_only_use(self) -> None:
        for name in EXPECTED_CANVAS:
            expected = name == "dreamina-canvas-use"
            self.assertEqual(
                implicit_invocation_policy(name), expected, name
            )

    def test_runtime_boundary_recorded(self) -> None:
        suite = json.loads(SUITE_JSON.read_text(encoding="utf-8"))
        boundary = suite["runtimeBoundary"]
        # cli_runtime is always required: every Canvas Skill depends on a
        # discoverable installed artifact.
        self.assertEqual(boundary["cli_runtime"], "PASS")
        # auth and paid_canary are separate approval boundaries. They are
        # PASS only when credentials and action-time approval were actually
        # supplied; otherwise they must be explicitly NOT_RUN. Both are
        # valid recorded states — silently omitting the key is not.
        for gate in ("auth", "paid_canary"):
            self.assertIn(boundary[gate], {"PASS", "NOT_RUN"}, gate)
        # A PASS must carry its evidence string.
        for gate in ("auth", "paid_canary"):
            if boundary[gate] == "PASS":
                self.assertTrue(
                    boundary.get(f"{gate}_evidence"),
                    f"{gate}=PASS requires an evidence string",
                )

    def test_canvas_skill_frontmatter_matches_dirname(self) -> None:
        for name in EXPECTED_CANVAS:
            text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
            match = re.search(r"(?m)^name:\s*[\"']?([^\n\"']+)", text)
            self.assertIsNotNone(match, name)
            self.assertEqual(match.group(1).strip(), name)


if __name__ == "__main__":
    unittest.main()
