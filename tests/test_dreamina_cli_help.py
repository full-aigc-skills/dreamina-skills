import shutil
import subprocess
import unittest


VIDEO_COMMANDS_WITH_RATIO = (
    "text2video",
    "image2video",
    "frames2video",
    "multimodal2video",
)


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
