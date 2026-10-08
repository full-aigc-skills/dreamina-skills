"""公开入口必须使用调用方版本范围，仍校验真实文件摘要。"""
import hashlib
import tempfile
import unittest
from pathlib import Path
from test_host_neutral_3d_contracts import load_module, ROOT

validator = load_module('handoff_version_validator', ROOT / 'skills/dreamina-3d-from-blender/scripts/handoff_validator.py')

class HandoffVersionRangesTests(unittest.TestCase):
    def test_explicit_and_default_ranges_with_real_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'preview.mp4'
            path.write_bytes(b'local regression fixture')
            receipt = dict(schema_version=validator.SUPPORTED_SCHEMA_VERSION,
                producer_plugin='blender-design', producer_version='1.2.0',
                artifact_id='test', path=str(path), bytes=path.stat().st_size,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                codec=validator.SUPPORTED_CODEC, dimensions=dict(width=1280,height=720),
                fps=24, duration_seconds=2, camera=dict(name='camera'),
                frame_range=dict(start=0,end=47), preview_mode='local_video',
                restoration=dict(status='confirmed'))
            ranges = {'blender-design': [('1.0.0', '1.9.9')]}
            self.assertEqual(validator.validate_artifact(receipt, path, version_ranges=ranges), [])
            self.assertTrue(validator.validate_artifact(receipt, path))
            receipt['producer_version'] = '0.14.1'
            self.assertEqual(validator.validate_artifact(receipt, path), [])
            errors = validator.validate_artifact(receipt, path, version_ranges=ranges)
            self.assertTrue(errors)
            self.assertIn('1.0.0', str(errors))
            self.assertTrue(validator.validate_artifact(receipt, path, version_ranges={}))
            receipt['producer_version'] = '1.2.0'
            path.write_bytes(b'modified')
            self.assertTrue(validator.validate_artifact(receipt, path, version_ranges=ranges))
