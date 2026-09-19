import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class HostNeutralDreamina3dContracts(unittest.TestCase):
    def test_installable_skill_content_has_no_legacy_plugin_identity(self) -> None:
        legacy = ("codex-dreamina-3d", "codex-blender", "codex-maya")
        for path in sorted((ROOT / "skills").glob("dreamina-3d*/**/*")):
            if not path.is_file() or path.suffix not in {".md", ".py"}:
                continue
            text = path.read_text(encoding="utf-8")
            for value in legacy:
                self.assertNotIn(value, text, f"{path} still contains {value}")

    def test_probe_discovers_all_host_manifests_with_neutral_ids(self) -> None:
        probe = load_module(
            "capability_probe",
            ROOT / "skills/dreamina-3d-use/scripts/capability_probe.py",
        )
        self.assertEqual(probe.SUPPORTED_PLUGINS, ("blender-design", "maya-design"))
        fixtures = (
            ("blender-design", ".codex-plugin/plugin.json", "bin/blender_adapter"),
            ("maya-design", ".zcode-plugin/plugin.json", "bin/maya_adapter"),
            ("maya-design", "kimi.plugin.json", "bin/maya_adapter"),
        )
        for plugin_id, manifest_rel, binary_rel in fixtures:
            with self.subTest(manifest=manifest_rel), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                plugin = root / plugin_id
                manifest = plugin / manifest_rel
                manifest.parent.mkdir(parents=True)
                manifest.write_text(
                    json.dumps(
                        {
                            "name": plugin_id,
                            "version": "0.1.0",
                        }
                    ),
                    encoding="utf-8",
                )
                binary = plugin / binary_rel
                binary.parent.mkdir(parents=True, exist_ok=True)
                binary.write_text("#!/bin/sh\n", encoding="utf-8")
                binary.chmod(0o755)
                companions = probe.discover_companions([root])
                self.assertEqual([item.plugin_id for item in companions], [plugin_id])
                self.assertEqual(companions[0].contract_versions, ("1.0.0",))

    def test_handoff_accepts_current_producer_ids(self) -> None:
        validator = load_module(
            "handoff_validator",
            ROOT / "skills/dreamina-3d-from-blender/scripts/handoff_validator.py",
        )
        self.assertEqual(validator.SUPPORTED_PRODUCERS, ("blender-design", "maya-design"))
        self.assertTrue(validator.compatible_producer("blender-design", "0.11.0"))
        self.assertTrue(validator.compatible_producer("maya-design", "0.1.3"))


if __name__ == "__main__":
    unittest.main()
