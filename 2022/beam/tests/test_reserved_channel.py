#!/usr/bin/env python3
# Dosya Yolu: 2022/beam/tests/test_reserved_channel.py
# Amac: Regression tests for blocked 2022 Beam feed and legacy alias isolation
# Modul - Python unittest
# Version: 0.1.0-candidate
# Aciklama: Tests use temporary synthetic fixtures only, never player feeds
# Bagimli Oldugu Katman: ../check_reserved_channel.py

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "check_reserved_channel.py"
SPEC = importlib.util.spec_from_file_location("reserved_beam_channel", SOURCE)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)

REAL_ROOT = SOURCE.parents[2]


class ReservedChannelTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="beam-feed-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for dirname in ["2022/beam", "2022/data", "2015/data", "data"]:
            (self.root / dirname).mkdir(parents=True)
        for filename in ["2022/channel.json", "2022/beam/channel-policy.json",
                         "2022/beam/patchlist.txt"]:
            source = REAL_ROOT / filename
            destination = self.root / filename
            destination.write_bytes(source.read_bytes())
        (self.root / "2022/data/README.md").write_text("no approved assets\n")
        (self.root / "2015/data/old.thor").write_bytes(b"2015")
        (self.root / "data/old.thor").write_bytes(b"2015")

    def test_reserved_empty_feed_passes(self):
        self.assertIn("RESERVED_OK", mod.audit(self.root))

    def test_patchlist_entry_denied(self):
        (self.root / "2022/beam/patchlist.txt").write_text(
            "custom-maps.beam " + "a" * 64 + "\n")
        with self.assertRaisesRegex(mod.ChannelBlocked, "ACTIVE_PATCH"):
            mod.audit(self.root)

    def test_binary_artifact_denied(self):
        (self.root / "2022/data/custom-maps.beam").write_bytes(b"BEAM")
        with self.assertRaisesRegex(mod.ChannelBlocked, "UNAPPROVED_ASSET"):
            mod.audit(self.root)

    def test_ready_flip_denied(self):
        file = self.root / "2022/channel.json"
        value = json.loads(file.read_text())
        value["ready"] = True
        file.write_text(json.dumps(value))
        with self.assertRaisesRegex(mod.ChannelBlocked, "NOT_RESERVED"):
            mod.audit(self.root)

    def test_policy_publish_flip_denied(self):
        file = self.root / "2022/beam/channel-policy.json"
        value = json.loads(file.read_text())
        value["publish_allowed"] = True
        file.write_text(json.dumps(value))
        with self.assertRaisesRegex(mod.ChannelBlocked, "POLICY_NOT_LOCKED"):
            mod.audit(self.root)

    def test_legacy_beam_contamination_denied(self):
        (self.root / "data/map.beam").write_bytes(b"wrong 2015 channel")
        with self.assertRaisesRegex(mod.ChannelBlocked, "LEGACY_2015"):
            mod.audit(self.root)

    def test_live_beam_config_denied(self):
        (self.root / "2022/beam/config.yml").write_text("unsafe: yes")
        with self.assertRaisesRegex(mod.ChannelBlocked, "ACTIVE_RUNTIME_CONFIG"):
            mod.audit(self.root)


if __name__ == "__main__":
    unittest.main()
