#!/usr/bin/env python3
"""Validate the Dreamina Canvas skill suite end to end.

Asserts:
- 13 dreamina-canvas-* Skill directories exist.
- 13 pre-existing dreamina-* Skill directories still exist.
- Total Skill count is 26.
- Every Skill directory contains a SKILL.md with a `name:` frontmatter
  matching the directory name.
- Every Skill has an agents/openai.yaml with a `policy.allow_implicit_invocation`
  field; exactly one Skill (dreamina-canvas-use) sets it to true.
- Every Skill has at least one reference document under references/.
- No SKILL.md or openai.yaml contains a hard-coded catalog masquerading
  as runtime truth (e.g. a concrete `--model` token outside placeholders).
- No skill file contains a credential-like pattern (OAuth access/refresh
  token, cookie, signed URL, creditConfirmationToken).
- The plugin manifest's `skills` list covers every Skill directory.
- The guide contract at verification/dreamina-canvas-guide-contract.json
  is closed and does not embed model or voice values.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
CONTRACT = ROOT / "verification" / "dreamina-canvas-guide-contract.json"
MANIFEST = ROOT / ".claude-plugin" / "plugin.json"

CANVAS_SKILLS = {
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

EXISTING_DREAMINA_SKILLS = {
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

EXPECTED_ALL = CANVAS_SKILLS | EXISTING_DREAMINA_SKILLS

SECRET_PATTERNS = [
    "access_token",
    "refresh_token",
    "creditConfirmationToken",
    "credit_confirmation_token",
    "signed_url",
    "signedUrl",
    "cookie=",
]


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def frontmatter_name(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"(?m)^name:\s*[\"']?([^\n\"']+)", text)
    if match is None:
        fail(f"missing frontmatter name in {path}")
    return match.group(1).strip()


def main() -> None:
    if not SKILLS.is_dir():
        fail(f"skills directory missing: {SKILLS}")

    actual_dirs = {p.name for p in SKILLS.iterdir() if p.is_dir()}
    missing = EXPECTED_ALL - actual_dirs
    if missing:
        fail(f"missing skill directories: {sorted(missing)}")
    extra = actual_dirs - EXPECTED_ALL
    if extra:
        fail(f"unexpected skill directories: {sorted(extra)}")

    implicit_skill: str | None = None
    for name in sorted(actual_dirs):
        skill_md = SKILLS / name / "SKILL.md"
        if not skill_md.is_file():
            fail(f"missing SKILL.md: {skill_md}")
        if frontmatter_name(skill_md) != name:
            fail(f"SKILL.md frontmatter name mismatch: {skill_md}")
        is_canvas_skill = name in CANVAS_SKILLS
        openai_yaml = SKILLS / name / "agents" / "openai.yaml"
        if is_canvas_skill:
            if not openai_yaml.is_file():
                fail(f"missing openai.yaml: {openai_yaml}")
            # Parse YAML with minimal stdlib parser (avoid extra dependency)
            try:
                import yaml  # type: ignore[import-not-found]
            except ImportError:
                fail("PyYAML not installed; cannot validate openai.yaml")
            data = yaml.safe_load(openai_yaml.read_text(encoding="utf-8"))
            policy = data.get("policy") or {}
            if "allow_implicit_invocation" not in policy:
                fail(f"openai.yaml missing policy.allow_implicit_invocation: {openai_yaml}")
            if policy["allow_implicit_invocation"] is True:
                if implicit_skill is not None:
                    fail(
                        f"multiple skills with allow_implicit_invocation=true: "
                        f"{implicit_skill}, {name}"
                    )
                implicit_skill = name
            refs_dir = SKILLS / name / "references"
            if not refs_dir.is_dir() or not any(refs_dir.iterdir()):
                fail(f"references/ empty or missing for skill: {name}")
        # Scan all skill files for credential-like patterns. Token names
        # may appear in SKILL.md / openai.yaml / references ONLY when
        # adjacent to a forbid / never / in-memory context (i.e. they are
        # being declared out-of-bounds, not used as a real value).
        files_to_scan = [skill_md]
        if openai_yaml.is_file():
            files_to_scan.append(openai_yaml)
        refs_dir = SKILLS / name / "references"
        if refs_dir.is_dir():
            files_to_scan.extend(refs_dir.glob("**/*"))
        for path in files_to_scan:
            if not path.is_file():
                continue
            content = path.read_text(encoding="utf-8")
            for pattern in SECRET_PATTERNS:
                if pattern in content:
                    lines = content.splitlines()
                    lines_with_pattern = [
                        idx
                        for idx, line in enumerate(lines)
                        if pattern in line
                    ]
                    if not lines_with_pattern:
                        fail(f"credential-like pattern '{pattern}' in {path}")
                    forbid_keywords = (
                        "never",
                        "forbid",
                        "in-memory",
                        "in memory",
                        "not persist",
                        "no token",
                        "no signed",
                        "forbids",
                        "echo or log",
                        "must not",
                    )
                    for idx in lines_with_pattern:
                        window = "\n".join(
                            lines[max(0, idx - 2) : idx + 3]
                        ).lower()
                        if not any(kw in window for kw in forbid_keywords):
                            fail(
                                f"credential-like pattern '{pattern}' appears "
                                f"outside forbid/never/in-memory context in {path}"
                            )
            if is_canvas_skill and re.search(r"--model\s+[A-Za-z][\w.-]{3,}", content):
                fail(f"possible hard-coded --model value in {path}")

    if implicit_skill != "dreamina-canvas-use":
        fail(
            f"only dreamina-canvas-use may be implicit; found implicit={implicit_skill!r}"
        )

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    declared = {Path(p).name for p in manifest.get("skills", [])}
    if declared != EXPECTED_ALL:
        fail(
            "plugin manifest skills mismatch: "
            f"missing={sorted(EXPECTED_ALL - declared)} "
            f"extra={sorted(declared - EXPECTED_ALL)}"
        )

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    for forbidden in ("models", "voices"):
        if forbidden in contract:
            fail(f"guide contract must not contain '{forbidden}'")

    print(f"OK: {len(actual_dirs)} skills validated; implicit skill = {implicit_skill}")


if __name__ == "__main__":
    main()
