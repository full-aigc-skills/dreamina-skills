#!/usr/bin/env python3
"""Verify portable skill-package structure, links, and granular-install safety."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path.cwd()
SKILLS = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if line and not line.startswith((" ", "-")) and ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def local_markdown_files(skill_dir: Path) -> list[Path]:
    return sorted(path for path in skill_dir.rglob("*.md") if path.is_file())


def main() -> int:
    errors: list[str] = []
    if not SKILLS.is_dir():
        print("ERROR: skills/ directory is missing", file=sys.stderr)
        return 2
    skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir())
    seen: set[str] = set()
    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{skill_dir.name}: missing SKILL.md")
            continue
        text = skill_md.read_text(encoding="utf-8")
        fields = parse_frontmatter(text)
        name = fields.get("name", "")
        description = fields.get("description", "")
        if not NAME_RE.fullmatch(name):
            errors.append(f"{skill_dir.name}: invalid frontmatter name {name!r}")
        if name != skill_dir.name:
            errors.append(f"{skill_dir.name}: frontmatter name does not match directory")
        if name in seen:
            errors.append(f"{skill_dir.name}: duplicate skill name {name!r}")
        seen.add(name)
        if not 20 <= len(description) <= 1024:
            errors.append(f"{skill_dir.name}: description length must be 20..1024")
        line_count = len(text.splitlines())
        if line_count > 500:
            errors.append(f"{skill_dir.name}: SKILL.md has {line_count} lines; maximum is 500")

        for markdown in local_markdown_files(skill_dir):
            body = markdown.read_text(encoding="utf-8")
            for raw_target in LINK_RE.findall(body):
                target = raw_target.strip().split("#", 1)[0]
                if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                resolved = (markdown.parent / target).resolve()
                try:
                    resolved.relative_to(skill_dir.resolve())
                except ValueError:
                    errors.append(
                        f"{markdown.relative_to(ROOT)}: cross-skill or package-relative link is not granular-install safe: {raw_target}"
                    )
                    continue
                if not resolved.exists():
                    errors.append(f"{markdown.relative_to(ROOT)}: missing local target {raw_target}")

        resource_scan = LINK_RE.sub("", text)
        for relative in re.findall(r"`((?:references|examples|scripts)/[^`\s]+)`", resource_scan):
            relative = relative.rstrip(".,;:")
            if any(char in relative for char in "*?["):
                if not list(skill_dir.glob(relative)):
                    errors.append(f"{skill_dir.name}: resource pattern matches nothing: {relative}")
                continue
            target = skill_dir / relative
            if target.suffix.lower() in {".md", ".py", ".sh", ".json", ".yaml", ".yml"} and not target.exists():
                errors.append(f"{skill_dir.name}: referenced resource does not exist: {relative}")

    for error in errors:
        print(f"ERROR: {error}")
    print(f"verify_skill_package: {len(skill_dirs)} skills, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
