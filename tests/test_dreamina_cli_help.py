import shutil
import subprocess
import unittest
from pathlib import Path


VIDEO_COMMANDS_WITH_RATIO = (
    "text2video",
    "image2video",
    "frames2video",
    "multimodal2video",
)

REPO_ROOT = Path(__file__).resolve().parents[1]
UMBRELLA_SKILL = REPO_ROOT / "skills" / "dreamina-cli" / "SKILL.md"
OFFICIAL_WORKFLOW = (
    REPO_ROOT
    / "skills"
    / "dreamina-cli"
    / "references"
    / "official-cli-install-to-use.md"
)

OFFICIAL_COMMANDS = (
    "curl -fsSL https://jimeng.jianying.com/cli | bash",
    "dreamina -h",
    "dreamina login",
    "dreamina login --headless",
    "dreamina login checklogin --device_code=<device_code> --poll=30",
    "dreamina relogin",
    "dreamina logout",
    "dreamina user_credit",
    "dreamina text2image",
    "dreamina image2image",
    "dreamina text2video",
    "dreamina image2video",
    "dreamina frames2video",
    "dreamina multiframe2video",
    "dreamina multimodal2video",
    "dreamina image_upscale",
    "dreamina query_result --submit_id=<submit_id>",
    "dreamina query_result --submit_id=<submit_id> --download_dir=./downloads",
    "dreamina list_task --gen_status=success",
    'dreamina session create "<project_name>"',
    "dreamina session list",
    'dreamina session search "<keyword>"',
    'dreamina session rename <session_id> "<new_name>"',
    "dreamina session delete <session_id>",
    "dreamina version",
)


class DreaminaCliSkillCoverageTests(unittest.TestCase):
    def test_umbrella_skill_routes_to_official_install_to_use_reference(self) -> None:
        text = UMBRELLA_SKILL.read_text(encoding="utf-8")
        self.assertIn("references/official-cli-install-to-use.md", text)

    def test_official_install_to_use_reference_covers_every_documented_command(self) -> None:
        text = OFFICIAL_WORKFLOW.read_text(encoding="utf-8")
        for command in OFFICIAL_COMMANDS:
            with self.subTest(command=command):
                self.assertIn(command, text)

    def test_official_workflow_covers_update_logs_and_paid_action_boundaries(self) -> None:
        text = OFFICIAL_WORKFLOW.read_text(encoding="utf-8")
        for required in (
            "~/.dreamina_cli/logs/",
            "AigcComplianceConfirmationRequired",
            "submit_id",
            "积分",
            "明确授权",
            "优先更新 CLI",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)


def command_help(command: str) -> str:
    result = subprocess.run(
        ["dreamina", command, "--help"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout + result.stderr


@unittest.skipUnless(shutil.which("dreamina"), "dreamina CLI is not installed")
class DreaminaCliHelpTests(unittest.TestCase):
    def test_v1418_ratio_surface_matches_documented_contract(self) -> None:
        for command in VIDEO_COMMANDS_WITH_RATIO:
            with self.subTest(command=command):
                self.assertIn("--ratio", command_help(command))

        self.assertNotIn("--ratio", command_help("multiframe2video"))

    def test_v1418_seedance25_help_mentions_current_resolution_set(self) -> None:
        for command in ("text2video", "image2video", "frames2video", "multimodal2video"):
            with self.subTest(command=command):
                help_text = command_help(command)
                self.assertIn("seedance2.5", help_text)
                self.assertIn("480p", help_text)
                self.assertIn("720p", help_text)
                self.assertIn("1080p", help_text)


if __name__ == "__main__":
    unittest.main()
