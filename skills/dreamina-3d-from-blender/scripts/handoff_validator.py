"""Receipt-driven handoff validator for codex-dreamina-3d.

Validates that an incoming ArtifactReceipt is structurally sound, was produced
by a known good plugin within its supported version range, and that the
on-disk artifact still matches the receipt (path exists, size matches, hash
matches). Re-checks the hash across the validation window so a file that is
mutated while validation runs is detected and rejected.

This module is intentionally pure stdlib so the plugin can run offline.
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

SUPPORTED_SCHEMA_VERSION = "1.0.0"
SUPPORTED_PRODUCERS: tuple[str, ...] = ("codex-blender", "codex-maya")
SUPPORTED_CODEC = "h264"
SUPPORTED_CONTAINER = "mp4"
MAX_DURATION_SECONDS = 60.0
MAX_DIMENSION = 4096
MIN_DIMENSION = 16
MAX_FPS = 120.0
MIN_FPS = 1.0

DEFAULT_VERSION_RANGES: dict[str, Sequence[tuple[str, str]]] = {
    # codex-blender's adapter emits its own plugin version as producer_version
    # (scripts/dreamina_adapter.py), and that plugin is published at 0.3.0. A
    # range stopping at 0.2.99 rejects every current receipt, so track the
    # published 0.1.x-0.3.x series.
    "codex-blender": [("0.1.0", "0.3.99")],
    "codex-maya": [("0.1.0", "0.1.99")],
}


@dataclass(frozen=True)
class ValidatorError(Exception):
    code: str
    message: str

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.code}: {self.message}"


def _parse_version(value: str) -> tuple[int, ...]:
    parts: list[int] = []
    for chunk in value.split("."):
        try:
            parts.append(int(chunk))
        except ValueError:
            parts.append(0)
    return tuple(parts) if parts else (0,)


def compatible_producer(
    producer_plugin: str,
    producer_version: str,
    supported_versions: dict[str, Sequence[tuple[str, str]]] | None = None,
) -> bool:
    """Return True when ``producer_plugin`` is supported and ``producer_version`` falls
    inside at least one of the ``[low, high]`` ranges for that plugin."""
    ranges = supported_versions if supported_versions is not None else DEFAULT_VERSION_RANGES
    if producer_plugin not in ranges:
        return False
    candidate = _parse_version(producer_version)
    for low, high in ranges[producer_plugin]:
        if _parse_version(low) <= candidate <= _parse_version(high):
            return True
    return False


def _sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _check_path(value: object, errors: list[str]) -> Path | None:
    if not isinstance(value, str) or not value:
        errors.append("receipt.path must be a non-empty string")
        return None
    path = Path(value)
    if not path.is_file():
        errors.append(f"receipt.path missing on disk: {value}")
        return None
    return path


def _validate_structural(receipt: dict, errors: list[str]) -> None:
    if not isinstance(receipt, dict):
        errors.append("receipt must be an object")
        return

    schema_version = receipt.get("schema_version")
    if schema_version != SUPPORTED_SCHEMA_VERSION:
        errors.append(
            f"receipt.schema_version must equal {SUPPORTED_SCHEMA_VERSION!r} "
            f"(got {schema_version!r})"
        )

    producer_plugin = receipt.get("producer_plugin")
    if producer_plugin not in SUPPORTED_PRODUCERS:
        errors.append(
            f"receipt.producer_plugin must be one of {SUPPORTED_PRODUCERS} "
            f"(got {producer_plugin!r})"
        )

    producer_version = receipt.get("producer_version")
    if not isinstance(producer_version, str) or not producer_version:
        errors.append("receipt.producer_version must be a non-empty string")
    elif producer_plugin in SUPPORTED_PRODUCERS and not compatible_producer(producer_plugin, producer_version):
        ranges = DEFAULT_VERSION_RANGES.get(producer_plugin, [])
        errors.append(
            f"receipt.producer_version {producer_version!r} is outside supported "
            f"ranges {list(ranges)} for {producer_plugin}"
        )

    artifact_id = receipt.get("artifact_id")
    if not isinstance(artifact_id, str) or not artifact_id:
        errors.append("receipt.artifact_id must be a non-empty string")

    sha = receipt.get("sha256")
    if not isinstance(sha, str) or len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha.lower()):
        errors.append("receipt.sha256 must be 64 lowercase hex characters")

    codec = receipt.get("codec")
    if codec != SUPPORTED_CODEC:
        errors.append(f"receipt.codec must equal {SUPPORTED_CODEC!r} (got {codec!r})")

    container = receipt.get("container", "mp4")
    if container != SUPPORTED_CONTAINER:
        errors.append(f"receipt.container must equal {SUPPORTED_CONTAINER!r} (got {container!r})")

    dimensions = receipt.get("dimensions") or {}
    if not isinstance(dimensions, dict):
        errors.append("receipt.dimensions must be an object")
    else:
        width = dimensions.get("width")
        height = dimensions.get("height")
        if not isinstance(width, int) or not isinstance(height, int):
            errors.append("receipt.dimensions.width/height must be integers")
        else:
            if not (MIN_DIMENSION <= width <= MAX_DIMENSION):
                errors.append(f"receipt.dimensions.width {width} outside [{MIN_DIMENSION},{MAX_DIMENSION}]")
            if not (MIN_DIMENSION <= height <= MAX_DIMENSION):
                errors.append(f"receipt.dimensions.height {height} outside [{MIN_DIMENSION},{MAX_DIMENSION}]")

    fps = receipt.get("fps")
    if not isinstance(fps, (int, float)) or not (MIN_FPS <= fps <= MAX_FPS):
        errors.append(f"receipt.fps must be in [{MIN_FPS},{MAX_FPS}] (got {fps!r})")

    duration = receipt.get("duration_seconds")
    if not isinstance(duration, (int, float)) or duration <= 0 or duration > MAX_DURATION_SECONDS:
        errors.append(f"receipt.duration_seconds must be in (0,{MAX_DURATION_SECONDS}] (got {duration!r})")

    bytes_value = receipt.get("bytes")
    if not isinstance(bytes_value, int) or bytes_value <= 0:
        errors.append("receipt.bytes must be a positive integer")

    camera = receipt.get("camera")
    if not isinstance(camera, dict) or not isinstance(camera.get("name"), str) or not camera["name"]:
        errors.append("receipt.camera.name must be a non-empty string")

    frame_range = receipt.get("frame_range") or {}
    if not isinstance(frame_range, dict):
        errors.append("receipt.frame_range must be an object")
    else:
        start = frame_range.get("start")
        end = frame_range.get("end")
        if not (isinstance(start, int) and isinstance(end, int) and 0 <= start <= end):
            errors.append("receipt.frame_range.start/end must be integers with 0 <= start <= end")

    preview_mode = receipt.get("preview_mode")
    if preview_mode not in ("camera_render", "local_video"):
        errors.append(
            "receipt.preview_mode must be 'camera_render' or 'local_video' "
            f"(got {preview_mode!r})"
        )

    restoration = receipt.get("restoration") or {}
    if not isinstance(restoration, dict) or restoration.get("status") != "confirmed":
        errors.append("receipt.restoration.status must equal 'confirmed'")


def validate_artifact(
    receipt: dict,
    current_file: Path,
    *,
    version_ranges: dict[str, Sequence[tuple[str, str]]] | None = None,
) -> list[str]:
    """Validate the receipt and the on-disk artifact.

    Returns a list of human-readable error strings. Empty list means accepted.
    """
    errors: list[str] = []
    _validate_structural(receipt, errors)
    if errors:
        return errors

    expected_path = _check_path(receipt.get("path"), errors)
    if expected_path is None:
        return errors

    try:
        expected_path = expected_path.resolve()
        current_file = current_file.resolve()
    except OSError:
        pass
    if expected_path != current_file:
        errors.append(
            f"receipt.path {expected_path} does not match supplied current_file {current_file}"
        )

    declared_bytes = receipt.get("bytes")
    try:
        on_disk_bytes = current_file.stat().st_size
    except OSError as exc:
        errors.append(f"could not stat artifact {current_file}: {exc}")
        return errors

    if declared_bytes != on_disk_bytes:
        errors.append(
            f"receipt.bytes {declared_bytes} != on-disk bytes {on_disk_bytes}"
        )

    declared_hash = receipt.get("sha256")
    actual_hash = _sha256_of(current_file)
    if declared_hash != actual_hash:
        errors.append(
            f"receipt.sha256 mismatch (expected {declared_hash}, got {actual_hash})"
        )

    # Re-validate immediately to detect mutation during validation.
    try:
        on_disk_bytes_again = current_file.stat().st_size
        actual_hash_again = _sha256_of(current_file)
    except OSError as exc:
        errors.append(f"artifact became unreadable during validation: {exc}")
        return errors

    if on_disk_bytes_again != on_disk_bytes:
        errors.append(
            f"artifact size changed during validation: {on_disk_bytes} -> {on_disk_bytes_again}"
        )
    if actual_hash_again != actual_hash:
        errors.append(
            f"artifact sha256 changed during validation: {actual_hash} -> {actual_hash_again}"
        )

    return errors


def is_acceptable(errors: Iterable[str]) -> bool:
    return not any(errors)


__all__ = [
    "SUPPORTED_SCHEMA_VERSION",
    "SUPPORTED_PRODUCERS",
    "DEFAULT_VERSION_RANGES",
    "ValidatorError",
    "compatible_producer",
    "validate_artifact",
    "is_acceptable",
]
