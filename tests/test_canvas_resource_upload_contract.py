"""Contract tests for `resource upload` (canvas CLI 1.0.0).

Task 2.1: contract coverage for `resource upload` and its flags
(`--file` / `--source-url` / `--type` / `--project-id` / `--resource-id` /
`--name` / `--import-kind`).

Task 2.3: a live-schema compatibility check proving the managed Skill's
declarations match what the installed CLI actually declares. The schema is the
runtime authority; a Skill text must not contradict it. When the CLI is absent
the check is skipped rather than silently passing.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
OWNER = "dreamina-canvas-download-assets"
CLI = shutil.which("dreamina-canvas")

REQUIRED_FLAGS = (
    "file",
    "source-url",
    "type",
    "project-id",
    "resource-id",
    "name",
    "import-kind",
)

# Phrases a Skill must never use again: the CLI's `resource` family is not
# read/download only, so this is a regression guard, not a style preference.
RETIRED_CLAIMS = (
    "read / download only",
    "read/download only",
    "uploads use a different flow",
    "upload … is out of scope",
    "upload is out of scope",
)


def skill_corpus(name: str) -> str:
    root = SKILLS / name
    parts = [(root / "SKILL.md").read_text(encoding="utf-8")]
    refs = root / "references"
    if refs.is_dir():
        parts.extend(p.read_text(encoding="utf-8") for p in sorted(refs.rglob("*.md")))
    return "\n".join(parts)


def live_schema() -> dict | None:
    if not CLI:
        return None
    proc = subprocess.run([CLI, "schema"], capture_output=True, text=True, timeout=30)
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout)["data"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return None


def find_command(schema: dict, *path: str) -> dict | None:
    node = schema
    for name in path:
        node = next(
            (c for c in node.get("subcommands", []) if c.get("name") == name), None
        )
        if node is None:
            return None
    return node


class ResourceUploadContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.corpus = skill_corpus(OWNER)

    # ---- 2.1 documented contract ---------------------------------------
    def test_every_flag_is_documented(self) -> None:
        for flag in REQUIRED_FLAGS:
            with self.subTest(flag=flag):
                self.assertIn(f"--{flag}", self.corpus)

    def test_mutual_exclusion_is_stated(self) -> None:
        self.assertIn("mutually exclusive", self.corpus.lower())

    def test_idempotency_rule_is_stated(self) -> None:
        lowered = self.corpus.lower()
        self.assertIn("idempotency", lowered)
        self.assertIn("reuse", lowered)
        # The dangerous anti-pattern must be named, not merely implied.
        self.assertIn("fresh uuid", lowered)

    def test_import_kind_is_a_declaration_not_a_permission(self) -> None:
        lowered = self.corpus.lower()
        self.assertIn("external_generated", lowered)
        self.assertIn("declaration, not a permission", lowered)

    def test_retired_read_download_only_claim_is_gone(self) -> None:
        """The CLI ships `resource upload`; the Skill must never say otherwise.

        The phrase may legitimately appear **negated** — the Skill states the
        family is *not* read/download only. Only an un-negated claim is a
        regression, so each occurrence is checked against its lead-in.
        """
        # Strip markdown emphasis so that `**not**` reads as `not`.
        normalized = self.corpus.lower().replace("*", " ").replace("`", " ")
        lowered = " ".join(normalized.split())
        negations = ("not ", "never ", "no longer ", "isn't ", "is not ", "aren't ")
        for retired in RETIRED_CLAIMS:
            start = 0
            while (index := lowered.find(retired, start)) != -1:
                lead = lowered[max(0, index - 40):index]
                start = index + 1
                with self.subTest(retired=retired, at=index):
                    self.assertTrue(
                        any(n in lead for n in negations),
                        f"un-negated retired claim {retired!r} near: ...{lead}{retired}...",
                    )

    def test_uri_vid_boundary_is_honest(self) -> None:
        """`uri:`/`vid:` are declared reference forms without locked evidence of
        server acceptance. The Skill must not promise they resolve, and must not
        claim the schema rejects them either."""
        lowered = self.corpus.lower()
        self.assertIn("uri:", lowered)
        self.assertIn("vid:", lowered)
        self.assertIn("unevidenced", lowered)

    # ---- 2.3 live-schema compatibility ---------------------------------
    @unittest.skipUnless(CLI, "dreamina-canvas CLI not installed")
    def test_skill_flags_match_the_live_schema(self) -> None:
        schema = live_schema()
        if schema is None:
            self.skipTest("dreamina-canvas schema did not return machine-readable JSON")
        command = find_command(schema, "resource", "upload")
        self.assertIsNotNone(command, "live schema has no `resource upload`")
        declared = {f["name"] for f in command.get("flags", [])}
        self.assertTrue(
            declared.issuperset(REQUIRED_FLAGS),
            f"live schema flags {sorted(declared)} do not cover {sorted(REQUIRED_FLAGS)}",
        )
        # Every live flag is documented; a new flag appearing upstream must
        # force a Skill update rather than silently going undocumented.
        for flag in sorted(declared):
            with self.subTest(flag=flag):
                self.assertIn(f"--{flag}", self.corpus)

    @unittest.skipUnless(CLI, "dreamina-canvas CLI not installed")
    def test_live_schema_declares_the_write_semantics(self) -> None:
        schema = live_schema()
        if schema is None:
            self.skipTest("dreamina-canvas schema did not return machine-readable JSON")
        command = find_command(schema, "resource", "upload")
        self.assertIsNotNone(command)
        self.assertTrue(command.get("writes"), "resource upload must declare writes=true")
        self.assertFalse(command.get("reads"), "resource upload must declare reads=false")


if __name__ == "__main__":
    unittest.main()
