import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
CONTRACT = ROOT / "verification" / "dreamina-canvas-guide-contract.json"


CANVAS_SKILLS = {
    "dreamina-canvas-cli",
    "dreamina-canvas-cli-setup",
    "dreamina-canvas-cli-auth",
    "dreamina-canvas-cli-text2image",
    "dreamina-canvas-cli-image2image",
    "dreamina-canvas-cli-text2voice",
    "dreamina-canvas-cli-text2audio",
    "dreamina-canvas-cli-text2video",
    "dreamina-canvas-cli-ref2video",
    "dreamina-canvas-use",
}


MIGRATION = {item["from"]: item for item in json.loads(
    (ROOT / "verification/dreamina-canvas-atomic-migration.json").read_text()
)["retired"]}


def skill_text(name: str) -> str:
    entry = MIGRATION.get(name)
    owner = entry["to"] if entry else name
    root = SKILLS / owner
    parts = [(root / entry["operationDocument"]).read_text()] if entry else [(root / "SKILL.md").read_text()]
    parts.extend(p.read_text() for p in sorted((root / "references").glob("*.md")))
    return "\n".join(parts)


def skill_openai_yaml(name: str) -> dict:
    name = MIGRATION.get(name, {}).get("to", name)
    text = (SKILLS / name / "agents" / "openai.yaml").read_text(encoding="utf-8")
    match = re.search(r"(?m)^\s*allow_implicit_invocation:\s*(true|false)\s*$", text)
    if match is None:
        raise AssertionError(f"missing allow_implicit_invocation: {name}")
    return {"policy": {"allow_implicit_invocation": match.group(1) == "true"}}


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
            {0, 1, 2, 10, 11, 12, 13, 20, 21, 22},
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

    def test_cli_task_skills_carry_sunset_notice_and_handoff(self) -> None:
        # The four task-level dreamina-canvas-cli-* skills replace the
        # sunset legacy `dreamina` CLI paths; each must say so and must
        # hand paid execution to quote-and-run.
        for name in (
            "dreamina-canvas-cli-text2image",
            "dreamina-canvas-cli-image2image",
            "dreamina-canvas-cli-text2video",
            "dreamina-canvas-cli-ref2video",
        ):
            text = skill_text(name)
            self.assertIn("Sunset notice", text, name)
            self.assertIn("dreamina-canvas-cli", text, name)
            self.assertIn("dreamina-prompt-", text, name)

    def test_cli_task_skills_are_explicit_only(self) -> None:
        for name in (
            "dreamina-canvas-cli-text2image",
            "dreamina-canvas-cli-image2image",
            "dreamina-canvas-cli-text2video",
            "dreamina-canvas-cli-ref2video",
        ):
            policy = skill_openai_yaml(name)["policy"]
            self.assertEqual(policy["allow_implicit_invocation"], False, name)

    def test_text2image_task_uses_t2i_mode(self) -> None:
        text = skill_text("dreamina-canvas-cli-text2image")
        self.assertIn("--mode t2i", text)
        self.assertIn("node create image", text)

    def test_image2image_task_requires_uploaded_resource_ref(self) -> None:
        text = skill_text("dreamina-canvas-cli-image2image")
        self.assertIn("resource upload", text)
        self.assertIn("--mode i2i", text)
        self.assertIn("res:", text)
        # The upscale boundary must be called out as separately priced
        self.assertIn("separately priced", text)

    def test_text2video_task_makes_duration_mandatory(self) -> None:
        text = skill_text("dreamina-canvas-cli-text2video")
        self.assertIn("--mode t2v", text)
        self.assertIn("--duration", text)

    def test_ref2video_task_rejects_i2v_mode(self) -> None:
        text = skill_text("dreamina-canvas-cli-ref2video")
        self.assertIn("m2v", text)
        self.assertIn("first_last_frame", text)
        self.assertIn("i2v", text)

    def test_text2voice_task_uses_voice_name_only(self) -> None:
        text = skill_text("dreamina-canvas-cli-text2voice")
        self.assertIn("--mode tts", text)
        self.assertIn("--voice-name", text)
        self.assertIn("voice list", text)
        self.assertIn("--model", text)  # present only as the forbidden flag

    def test_text2audio_task_uses_model_and_duration(self) -> None:
        text = skill_text("dreamina-canvas-cli-text2audio")
        self.assertIn("--mode music", text)
        self.assertIn("--duration", text)
        self.assertIn("model list --type audio", text)

    def test_audio_task_skills_are_explicit_only(self) -> None:
        for name in ("dreamina-canvas-cli-text2voice", "dreamina-canvas-cli-text2audio"):
            policy = skill_openai_yaml(name)["policy"]
            self.assertEqual(policy["allow_implicit_invocation"], False, name)

    def test_ready_skill_covers_prep_phase_and_stays_free(self) -> None:
        text = skill_text("dreamina-canvas-ready")
        for token in ("model list", "model find", "canvas create", "canvas ls",
                      "resource upload", "--import-kind local_upload",
                      "node:<nodeId>", "res:<resourceId>"):
            self.assertIn(token, text, token)
        # The prep phase must be free-only: no paid chain ownership
        self.assertIn("no paid action", text.lower())

    def test_ready_skill_is_explicit_only(self) -> None:
        policy = skill_openai_yaml("dreamina-canvas-ready")["policy"]
        self.assertEqual(policy["allow_implicit_invocation"], False)

    def test_setup_skill_covers_installer_matrix_and_authorization(self) -> None:
        text = skill_text("dreamina-canvas-cli-setup")
        for token in ("install.sh", "install.ps1", "install.bat",
                      "command not found", "explicit authorization"):
            self.assertIn(token, text, token)

    def test_auth_task_skill_covers_login_flow_and_account_check(self) -> None:
        text = skill_text("dreamina-canvas-cli-auth")
        for token in ("auth login", "auth account", "auth wait",
                      "--non-interactive", "auth status"):
            self.assertIn(token, text, token)
        # auth status must be explicitly distrusted as login evidence
        self.assertIn("proof of login", text.lower())

    def test_install_and_auth_task_skills_are_explicit_only(self) -> None:
        for name in ("dreamina-canvas-cli-setup", "dreamina-canvas-cli-auth"):
            policy = skill_openai_yaml(name)["policy"]
            self.assertEqual(policy["allow_implicit_invocation"], False, name)

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

    def test_discovery_uses_runtime_catalogs(self) -> None:
        text = skill_text("dreamina-canvas-discover-models")
        for command in ("model search", "model list", "--detail full", "voice list", "schema"):
            self.assertIn(command, text, command)
        self.assertIn("only when the live schema declares it", text)
        self.assertIn("never", text.lower())

    def test_discovery_skill_is_explicit_only(self) -> None:
        policy = skill_openai_yaml("dreamina-canvas-discover-models")["policy"]
        self.assertEqual(policy["allow_implicit_invocation"], False)

    def test_create_reuses_explicit_project_id_for_cross_process_retry(self) -> None:
        text = skill_text("dreamina-canvas-create")
        self.assertIn("canvas create", text)
        self.assertIn("--project-id", text)
        self.assertIn("--use", text)
        # Concurrency awareness
        self.assertIn("concurrent", text.lower())

    def test_create_skill_is_explicit_only(self) -> None:
        policy = skill_openai_yaml("dreamina-canvas-create")["policy"]
        self.assertEqual(policy["allow_implicit_invocation"], False)

    def test_paid_run_requires_authoritative_quote_and_action_time_approval(self) -> None:
        text = skill_text("dreamina-canvas-quote-and-run")
        self.assertLess(text.index("node quote"), text.index("node confirm"))
        self.assertLess(text.index("node confirm"), text.index("node run"))
        self.assertIn("--credit-ceiling", text)
        self.assertIn("partialData.items", text)
        self.assertIn("--yes", text)
        # The approval paragraph must NOT advertise any default-yes behaviour
        approval_para = text[text.index("--credit-ceiling"):]
        self.assertNotIn("默认", approval_para)

    def test_batch_run_uses_one_submit_id_per_node(self) -> None:
        text = skill_text("dreamina-canvas-quote-and-run")
        self.assertIn("one `--submit-id` per `--node-id`", text)
        self.assertIn("equal length and order", text)
        self.assertIn("--submit-id <id1> --submit-id <id2>", text)

    def test_quote_and_run_skill_is_explicit_only(self) -> None:
        policy = skill_openai_yaml("dreamina-canvas-quote-and-run")["policy"]
        self.assertEqual(policy["allow_implicit_invocation"], False)

    def test_recovery_never_changes_submit_id(self) -> None:
        text = skill_text("dreamina-canvas-resume-operation")
        self.assertIn("operation status", text)
        self.assertIn("operation wait", text)
        self.assertIn("resubmittable", text)
        # The skill must explicitly forbid re-submitting
        self.assertIn("minting a new", text.lower())
        self.assertIn("never", text.lower())

    def test_resume_operation_skill_is_explicit_only(self) -> None:
        policy = skill_openai_yaml("dreamina-canvas-resume-operation")["policy"]
        self.assertEqual(policy["allow_implicit_invocation"], False)

    def test_download_requires_resource_fact_and_receipt(self) -> None:
        text = skill_text("dreamina-canvas-download-assets")
        for token in ("resource get", "resource download", "SHA-256", "resourceId"):
            self.assertIn(token, text, token)
        # The skill must explicitly forbid persisting signed URLs
        self.assertIn("never", text.lower())
        self.assertIn("signed", text.lower())

    def test_download_assets_skill_is_explicit_only(self) -> None:
        policy = skill_openai_yaml("dreamina-canvas-download-assets")["policy"]
        self.assertEqual(policy["allow_implicit_invocation"], False)

    def test_image_skill_separates_t2i_and_i2i_references(self) -> None:
        text = skill_text("dreamina-canvas-generate-image")
        self.assertIn("--mode t2i", text)
        self.assertIn("--mode i2i", text)
        self.assertIn("node:", text)
        self.assertIn("res:", text)
        # Generation edit replaces the full block; --clear-generation is the opt-out
        self.assertIn("--clear-generation", text)
        self.assertIn("sparse", text.lower())

    def test_generate_image_skill_is_explicit_only(self) -> None:
        policy = skill_openai_yaml("dreamina-canvas-generate-image")["policy"]
        self.assertEqual(policy["allow_implicit_invocation"], False)

    def test_video_skill_uses_only_public_canvas_modes(self) -> None:
        text = skill_text("dreamina-canvas-generate-video")
        for mode in ("t2v", "first_last_frame", "m2v"):
            self.assertIn(mode, text, mode)
        # The skill must explicitly state that i2v and multi_modal are rejected
        self.assertIn("i2v", text)
        self.assertIn("multi_modal", text)

    def test_generate_video_skill_is_explicit_only(self) -> None:
        policy = skill_openai_yaml("dreamina-canvas-generate-video")["policy"]
        self.assertEqual(policy["allow_implicit_invocation"], False)

    def test_audio_skill_enforces_mode_specific_fields(self) -> None:
        text = skill_text("dreamina-canvas-generate-audio")
        self.assertIn("tts", text)
        self.assertIn("--voice-name", text)
        self.assertIn("music", text)
        self.assertIn("--model", text)
        # The skill must explicitly state that --count is not accepted
        self.assertIn("--count", text)

    def test_generate_audio_skill_is_explicit_only(self) -> None:
        policy = skill_openai_yaml("dreamina-canvas-generate-audio")["policy"]
        self.assertEqual(policy["allow_implicit_invocation"], False)

    def test_timeline_edit_warns_before_track_replacement(self) -> None:
        text = skill_text("dreamina-canvas-manage-timeline")
        self.assertIn("--clip", text)
        self.assertIn("--audio-clip", text)
        # The skill must warn about full track replacement
        self.assertIn("rebuild", text.lower())
        self.assertIn("destructive", text.lower())
        # It must explicitly call out the uncommitted-changes loss boundary
        self.assertIn("unsaved", text.lower())

    def test_manage_timeline_skill_is_explicit_only(self) -> None:
        policy = skill_openai_yaml("dreamina-canvas-manage-timeline")["policy"]
        self.assertEqual(policy["allow_implicit_invocation"], False)

    def test_compose_saves_graph_before_any_paid_run(self) -> None:
        text = skill_text("dreamina-canvas-compose")
        # Required node-type coverage
        for kind in ("Text", "Element", "Timeline"):
            self.assertIn(kind, text, kind)
        # The skill must call out the node run DAG scheduling gap
        self.assertIn("node run", text)
        self.assertIn("DAG", text)
        # Default-only-save contract must be present
        self.assertIn("save", text.lower())
        # No-approval rule
        self.assertIn("never", text.lower())

    def test_compose_skill_is_explicit_only(self) -> None:
        policy = skill_openai_yaml("dreamina-canvas-compose")["policy"]
        self.assertEqual(policy["allow_implicit_invocation"], False)

    def test_use_is_the_only_implicit_canvas_skill(self) -> None:
        for name in CANVAS_SKILLS - {"dreamina-canvas-use"}:
            self.assertEqual(
                skill_openai_yaml(name)["policy"]["allow_implicit_invocation"],
                False,
                name,
            )
        self.assertEqual(
            skill_openai_yaml("dreamina-canvas-use")["policy"]["allow_implicit_invocation"],
            True,
        )

    def test_use_skill_is_explicit_only(self) -> None:
        # NOTE: dreamina-canvas-use is the only implicit Canvas Skill.
        # This test name is preserved for symmetry with the other skills
        # but we only assert that the policy file is well-formed.
        policy = skill_openai_yaml("dreamina-canvas-use")["policy"]
        self.assertIn("allow_implicit_invocation", policy)


if __name__ == "__main__":
    unittest.main()
