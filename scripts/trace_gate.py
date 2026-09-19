#!/usr/bin/env python3
"""Run the pinned deterministic TRACE evaluator across every packaged skill."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evaluator", required=True, type=Path)
    parser.add_argument("--skills-dir", default="skills", type=Path)
    parser.add_argument("--threshold", default=4.5, type=float)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    evaluator = args.evaluator.resolve()
    skills_dir = args.skills_dir.resolve()
    if not evaluator.is_file():
        print(f"ERROR: TRACE evaluator not found: {evaluator}", file=sys.stderr)
        return 2

    rows: list[tuple[str, float]] = []
    failures: list[tuple[str, float]] = []
    for skill_dir in sorted(path for path in skills_dir.iterdir() if (path / "SKILL.md").is_file()):
        result = subprocess.run(
            [sys.executable, str(evaluator), "--skill-dir", str(skill_dir)],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        score = float(payload["base_scores"]["overall"])
        rows.append((skill_dir.name, score))
        if score < args.threshold:
            failures.append((skill_dir.name, score))

    if not rows:
        print("ERROR: no skills found", file=sys.stderr)
        return 2
    average = sum(score for _, score in rows) / len(rows)
    minimum = min(score for _, score in rows)
    maximum = max(score for _, score in rows)
    print(
        f"TRACE: {len(rows)} skills, average={average:.3f}, "
        f"minimum={minimum:.2f}, maximum={maximum:.2f}, threshold={args.threshold:.2f}"
    )
    if failures:
        for name, score in failures:
            print(f"ERROR: {name} scored {score:.2f} below {args.threshold:.2f}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
