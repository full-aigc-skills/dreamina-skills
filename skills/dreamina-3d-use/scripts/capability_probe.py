"""Companion capability probe for codex-dreamina-3d.

Discovers compatible codex-blender / codex-maya installations through stable
plugin manifests or an explicit adapter executable on the search roots. Never
crawls unrelated user directories and never installs anything.

Each Companion is a frozen dataclass returned by discover_companions(); the
orchestrator then calls select_companion() to either auto-pick the single
candidate or require an explicit user-provided choice.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

SUPPORTED_PLUGINS: tuple[str, ...] = ("codex-blender", "codex-maya")
SUPPORTED_CONTRACT_VERSIONS: tuple[str, ...] = ("1.0.0",)

DEFAULT_ADAPTER_BINARIES = {
    "codex-blender": ("bin/blender_adapter",),
    "codex-maya": ("bin/maya_adapter",),
}


class MissingCompanionError(RuntimeError):
    """No compatible companion plugin is installed."""


class AmbiguousCompanionError(RuntimeError):
    """Multiple compatible companions are installed and no explicit choice was given."""


class IncompatibleContractError(RuntimeError):
    """A discovered companion advertises an unsupported contract version."""


@dataclass(frozen=True)
class Companion:
    plugin_id: str
    version: str
    executable: Path | None
    contract_versions: tuple[str, ...]
    manifest_path: Path

    @property
    def is_callable(self) -> bool:
        return self.executable is not None and self.executable.is_file() and os.access(self.executable, os.X_OK)


def _load_manifest(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _candidate_dirs(search_root: Path) -> Iterable[Path]:
    """Yield only stable, well-known plugin installation roots.

    We deliberately do NOT crawl arbitrary user directories (Documents, Desktop,
    Projects). The Codex installation model expects companion plugins under
    ``<root>/<plugin_id>/.codex-plugin/plugin.json``.
    """
    if not search_root.is_dir():
        return ()
    for child in sorted(search_root.iterdir()):
        if not child.is_dir():
            continue
        if child.name not in SUPPORTED_PLUGINS:
            continue
        yield child


def _resolve_adapter(plugin_dir: Path, plugin_id: str) -> Path | None:
    for rel in DEFAULT_ADAPTER_BINARIES.get(plugin_id, ()):
        candidate = plugin_dir / rel
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate
    return None


def discover_companions(search_roots: Sequence[Path]) -> list[Companion]:
    """Discover compatible companion plugins under ``search_roots``.

    The first matching installation per plugin id wins; duplicates and stale
    installations (missing adapter executable) are dropped.
    """
    discovered: dict[str, Companion] = {}
    for root in search_roots:
        for plugin_dir in _candidate_dirs(root):
            plugin_id = plugin_dir.name
            if plugin_id in discovered:
                continue
            manifest_path = plugin_dir / ".codex-plugin" / "plugin.json"
            manifest = _load_manifest(manifest_path)
            if manifest is None:
                continue
            if manifest.get("name") != plugin_id:
                continue
            version = str(manifest.get("version", ""))
            contracts = tuple(manifest.get("receipt_contract_versions", ()))
            if not any(c in SUPPORTED_CONTRACT_VERSIONS for c in contracts):
                continue
            executable = _resolve_adapter(plugin_dir, plugin_id)
            if executable is None:
                # Stale installation: manifest present but no adapter.
                continue
            discovered[plugin_id] = Companion(
                plugin_id=plugin_id,
                version=version,
                executable=executable,
                contract_versions=contracts,
                manifest_path=manifest_path,
            )
    return [discovered[pid] for pid in sorted(discovered)]


def install_guidance() -> str:
    """Return the exact installation guidance shown when no companion is found."""
    return (
        "No compatible companion plugin is installed. Install one of:\n"
        "  - codex-blender  (https://github.com/partme-ai/codex-blender-plugin)\n"
        "  - codex-maya     (https://github.com/partme-ai/codex-maya-plugin)\n"
        "Then re-run the workflow. The orchestrator will not install or modify "
        "either companion automatically."
    )


def select_companion(candidates: Sequence[Companion], requested: str | None) -> Companion:
    """Select a single companion from the candidates.

    Behaviour:
      - empty list -> MissingCompanionError carrying install guidance
      - one candidate -> that candidate, regardless of ``requested``
      - two candidates and no explicit request -> AmbiguousCompanionError
      - two candidates with ``requested='blender'|'maya'`` -> matching candidate
      - unknown request -> ValueError
    """
    if not candidates:
        raise MissingCompanionError(install_guidance())
    # Validate the requested id early so unknown DCC names fail fast even when
    # only one companion happens to be installed.
    requested_id: str | None = None
    if requested is not None:
        requested_id = f"codex-{requested.strip().lower()}"
        if requested_id not in SUPPORTED_PLUGINS:
            raise ValueError(
                f"requested companion {requested!r} is not one of "
                f"{[p.removeprefix('codex-') for p in SUPPORTED_PLUGINS]}"
            )
    if len(candidates) == 1:
        if requested_id is None or candidates[0].plugin_id == requested_id:
            return candidates[0]
        available = ", ".join(c.plugin_id for c in candidates)
        raise MissingCompanionError(
            f"requested companion {requested_id!r} is not installed; available: {available}"
        )
    if requested_id is None:
        names = ", ".join(c.plugin_id for c in candidates)
        raise AmbiguousCompanionError(
            f"Multiple compatible companions are installed ({names}); "
            "the user must explicitly choose 'blender' or 'maya'."
        )
    for candidate in candidates:
        if candidate.plugin_id == requested_id:
            return candidate
    available = ", ".join(c.plugin_id for c in candidates)
    raise MissingCompanionError(
        f"requested companion {requested_id!r} is not installed; available: {available}"
    )


__all__ = [
    "SUPPORTED_PLUGINS",
    "SUPPORTED_CONTRACT_VERSIONS",
    "Companion",
    "MissingCompanionError",
    "AmbiguousCompanionError",
    "IncompatibleContractError",
    "discover_companions",
    "select_companion",
    "install_guidance",
]