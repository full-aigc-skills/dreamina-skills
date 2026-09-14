#!/usr/bin/env python3
"""Validate the five-plugin suite's 30 bilingual documents.

Implements the gates in
`docs/superpowers/specs/2026-09-11-dreamina-five-plugin-suite-documentation-design.md`
§11 (文档质量门禁) across the five plugin repositories.

Usage:
    python3 scripts/validate_five_plugin_docs.py [--root <workspace-root>] [--format json]

Each plugin contributes six documents:
    README.md
    README.zh-CN.md
    docs/<Stem>-Architecture.md
    docs/<Stem>-Architecture.zh_CN.md
    docs/<Stem>-Technical-Solution.md
    docs/<Stem>-Technical-Solution.zh_CN.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PLUGINS = (
    "codex-blender-plugin",
    "codex-maya-plugin",
    "codex-dreamina-canvas-plugin",
    "codex-dreamina-design-plugin",
    "codex-dreamina-3d-plugin",
)

SECRET_PATTERNS = (
    (r"/Users/[A-Za-z]", "local absolute path"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key"),
    (r"sk-[A-Za-z0-9]{16,}", "API key"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY", "private key"),
    (r"access_token|refresh_token", "credential name"),
    (r"cookie\s*=", "cookie value"),
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


# Gate 6 compares only the token classes the specification enumerates:
# identifiers, commands, schema fields, versions, and statuses. Comparing
# every inline code span produces false positives because prose wraps code
# spans across lines and across markdown structure.
_INLINE_CODE = re.compile(r"`([^`\n]{1,60})`")

_IDENTIFIER_CLASSES = (
    ("flag", re.compile(r"--[A-Za-z][A-Za-z0-9-]*")),
    ("version", re.compile(r"\d+\.\d+\.\d+[^\s]*")),
    ("path", re.compile(r"[A-Za-z_][\w.-]*/[\w./-]+")),
    ("schema-type", re.compile(r"[A-Z][A-Za-z0-9]*([A-Z][A-Za-z0-9]*)+")),
    ("exit-code", re.compile(r"exit\s*code\s*\d+|\d{1,2}")),
)


def classified_tokens(path: Path) -> dict[str, set[str]]:
    classes: dict[str, set[str]] = {}
    for m in _INLINE_CODE.finditer(read(path)):
        span = m.group(1).strip()
        for name, pattern in _IDENTIFIER_CLASSES:
            if pattern.fullmatch(span):
                classes.setdefault(name, set()).add(span)
                break
    return classes


def code_tokens(path: Path) -> dict[str, set[str]]:
    return classified_tokens(path)


def doc_set(root: Path) -> dict[str, Path]:
    """Locate the six documents, whether at docs/ or in a docs/archive/* dir."""
    found: dict[str, Path] = {}
    readme = root / "README.md"
    readme_zh = root / "README.zh-CN.md"
    if readme.is_file():
        found["README.md"] = readme
    if readme_zh.is_file():
        found["README.zh-CN.md"] = readme_zh
    candidates = list(root.glob("docs/*-Architecture.md")) + list(
        root.glob("docs/*-Architecture.zh_CN.md")
    )
    candidates += list(root.glob("docs/*-Technical-Solution.md")) + list(
        root.glob("docs/*-Technical-Solution.zh_CN.md")
    )
    for p in candidates:
        found[p.name] = p
    return found


def archived_docs(root: Path) -> list[Path]:
    return sorted(root.glob("docs/archive/**/*-Architecture*.md")) + sorted(
        root.glob("docs/archive/**/*-Technical-Solution*.md")
    )


def gate_filename(docs: dict[str, Path]) -> list[str]:
    errors: list[str] = []
    for name in docs:
        if name.startswith("README"):
            continue
        if re.fullmatch(r"[^\s/]+-Architecture(\.zh_CN)?\.md", name) is None and re.fullmatch(
            r"[^\s/]+-Technical-Solution(\.zh_CN)?\.md", name
        ) is None:
            errors.append(f"non-conforming filename: {name}")
    for stem in ("Architecture", "Technical-Solution"):
        en = any(n.endswith(f"-{stem}.md") for n in docs)
        zh = any(n.endswith(f"-{stem}.zh_CN.md") for n in docs)
        if en != zh:
            errors.append(f"{stem}: bilingual pair incomplete (en={en} zh={zh})")
    return errors


def gate_structure(docs: dict[str, Path]) -> list[str]:
    errors: list[str] = []
    for name, path in sorted(docs.items()):
        text = read(path)
        h1 = len(re.findall(r"^# ", text, re.M))
        if h1 != 1:
            errors.append(f"{name}: {h1} H1 headings (expected 1)")
        fences = re.findall(r"^```(\w*)", text, re.M)
        if len(fences) % 2 != 0:
            errors.append(f"{name}: unbalanced code fences")
        untagged = [f for f in fences[0::2] if not f]
        if untagged:
            errors.append(f"{name}: {len(untagged)} untagged code fences")
    return errors


def gate_placeholders(docs: dict[str, Path]) -> list[str]:
    return [
        f"{name}: unresolved placeholder"
        for name, path in sorted(docs.items())
        if re.search(r"\{\{[^}]+\}\}", read(path))
    ]


def gate_secrets(docs: dict[str, Path]) -> list[str]:
    errors: list[str] = []
    for name, path in sorted(docs.items()):
        text = read(path)
        for pattern, label in SECRET_PATTERNS:
            if re.search(pattern, text):
                errors.append(f"{name}: {label}")
    return errors


def _pair(docs: dict[str, Path], stem: str) -> tuple[Path, Path] | None:
    en = docs.get(f"{stem}.md")
    zh = docs.get(f"{stem}.zh_CN.md")
    if en and zh:
        return en, zh
    return None


def bilingual_pairs(docs: dict[str, Path]) -> list[tuple[Path, Path]]:
    out: list[tuple[Path, Path]] = []
    if "README.md" in docs and "README.zh-CN.md" in docs:
        out.append((docs["README.md"], docs["README.zh-CN.md"]))
    for stem in ("Architecture", "Technical-Solution"):
        for name in docs:
            if name.endswith(f"-{stem}.md"):
                pair = _pair(
                    {p.name: p for p in docs.values()},
                    name[: -len(f"-{stem}.md")] + f"-{stem}",
                )
                if pair:
                    out.append(pair)
    return out


def gate_sections(pairs: list[tuple[Path, Path]]) -> list[str]:
    errors: list[str] = []
    for en, zh in pairs:
        a = [l for l in read(en).splitlines() if l.startswith("## ")]
        b = [l for l in read(zh).splitlines() if l.startswith("## ")]
        if len(a) != len(b):
            errors.append(f"{en.name}/{zh.name}: section count {len(a)} vs {len(b)}")
    return errors


def gate_tokens(pairs: list[tuple[Path, Path]]) -> list[str]:
    errors: list[str] = []
    for en, zh in pairs:
        ce, cz = classified_tokens(en), classified_tokens(zh)
        for kind in sorted(set(ce) | set(cz)):
            only_en = ce.get(kind, set()) - cz.get(kind, set())
            only_zh = cz.get(kind, set()) - ce.get(kind, set())
            if only_en:
                errors.append(f"{en.name}: {kind} absent from zh: {sorted(only_en)}")
            if only_zh:
                errors.append(f"{zh.name}: {kind} absent from en: {sorted(only_zh)}")
    return errors


def gate_links(docs: dict[str, Path]) -> list[str]:
    errors: list[str] = []
    for name, path in sorted(docs.items()):
        for m in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", read(path)):
            link = m.group(1).split("#")[0].strip()
            if not link or link.startswith(("http://", "https://", "mailto:")):
                continue
            if not (path.parent / link).resolve().exists():
                errors.append(f"{name}: broken link {link}")
    return errors


def gate_mermaid(docs: dict[str, Path]) -> list[str]:
    arch = [p for n, p in docs.items() if "-Architecture" in n]
    if not arch:
        return ["no Architecture document to check for diagrams"]
    joined = "\n".join(read(p) for p in arch)
    blocks = re.findall(r"```mermaid(.*?)```", joined, re.S)
    if not blocks:
        return ["no mermaid block in the Architecture document"]
    if not any("flowchart" in b or "graph " in b for b in blocks):
        return ["no flowchart diagram in the Architecture document"]
    return []


GATES = (
    ("1-filenames", lambda d, p: gate_filename(d)),
    ("2-structure", lambda d, p: gate_structure(d)),
    ("3-placeholders", lambda d, p: gate_placeholders(d)),
    ("4-secrets", lambda d, p: gate_secrets(d)),
    ("5-section-parity", lambda d, p: gate_sections(p)),
    ("6-token-parity", lambda d, p: gate_tokens(p)),
    ("7-links", lambda d, p: gate_links(d)),
    ("8-mermaid", lambda d, p: gate_mermaid(d)),
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        default="/Users/wandl/workspaces/workspace-partme-ai",
        help="Directory containing the five plugin repositories",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    root = Path(args.root)

    report: dict = {"root": str(root), "plugins": {}, "totals": {}}
    present_total = 0
    failing_total = 0

    for plugin in PLUGINS:
        plugin_root = root / plugin
        if not plugin_root.is_dir():
            report["plugins"][plugin] = {"error": "repository not found"}
            continue
        docs = doc_set(plugin_root)
        pairs = bilingual_pairs(docs)
        entry: dict = {
            "documents": sorted(docs),
            "documentCount": len(docs),
            "archivedDocuments": [
                str(p.relative_to(plugin_root)) for p in archived_docs(plugin_root)
            ],
            "gates": {},
        }
        for gate_name, fn in GATES:
            entry["gates"][gate_name] = fn(docs, pairs)
        present_total += len(docs)
        failing_total += sum(1 for v in entry["gates"].values() if v)
        report["plugins"][plugin] = entry

    report["totals"] = {
        "documentsPresent": present_total,
        "documentsExpected": 30,
        "gatesFailing": failing_total,
    }

    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        for plugin, entry in report["plugins"].items():
            if "error" in entry:
                print(f"{plugin}: {entry['error']}")
                continue
            marks = []
            for gate_name, errs in entry["gates"].items():
                marks.append(f"{gate_name}={'PASS' if not errs else 'FAIL'}")
            print(f"{plugin}: {entry['documentCount']}/6 docs")
            print("   " + "  ".join(marks))
            for gate_name, errs in entry["gates"].items():
                for e in errs:
                    print(f"     [{gate_name}] {e}")
            if entry["archivedDocuments"]:
                print(f"     archived: {entry['archivedDocuments']}")
        print()
        print(
            f"TOTAL {report['totals']['documentsPresent']}/30 documents; "
            f"{report['totals']['gatesFailing']} failing gate results"
        )

    return 0 if failing_total == 0 and present_total == 30 else 1


if __name__ == "__main__":
    raise SystemExit(main())
