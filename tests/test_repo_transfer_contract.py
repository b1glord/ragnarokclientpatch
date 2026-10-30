#!/usr/bin/env python3
# Dosya Yolu: REPO_ROOT/tests/test_repo_transfer_contract.py
# Amac: Public patch dagitim URL'leri ile 2015/2022 sahiplik ve butunluk kontrati
# Modul - Python unittest
# Version: 1.0.0
# Aciklama: Network/yayinlama yok; kanonik adres, legacy paket ve yayin kilidi dogrulama
# Bagimli Oldugu Katman: Testing
"""Offline checks for public patch repo transfer and channel isolation."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OWNER = "LevelUpRagnarok"
DISTRIBUTION = f"{OWNER}/ragnarokclientpatch"
RAW_URL = f"https://raw.githubusercontent.com/{DISTRIBUTION}/main/"
IDENTITIES = {
    "source_repository": f"{OWNER}/RagnarokClient",
    "package_builder_repository": f"{OWNER}/beam-patcher",
    "distribution_repository": DISTRIBUTION,
}
CONFIGS = (
    "rpatchur/config.yml",
    "2015/rpatchur/config.yml",
    "beam/config.yml",
    "2015/beam/config.yml",
    "2022/beam/config.yml.template",
)
TEXT_PATHS = CONFIGS + (
    "README.md", "2022/beam/README.md",
    "2022/beam/channel-policy.json", "2022/server-compatibility.yml",
)


class PublicPatchTransferTests(unittest.TestCase):
    def test_no_retired_owner_in_active_config_or_docs(self):
        retired = (
            "LevelUpGT/RagnarokClient", "LevelUpGT/RagnarokServer",
            "LevelUpGT/beam-patcher", "b1glord/ragnarokclientpatch",
        )
        for path in TEXT_PATHS:
            with self.subTest(path=path):
                content = (ROOT / path).read_text(encoding="utf-8")
                for obsolete in retired:
                    self.assertNotIn(obsolete, content)

    def test_all_patch_configs_use_canonical_raw_owner(self):
        for path in CONFIGS:
            with self.subTest(path=path):
                content = (ROOT / path).read_text(encoding="utf-8")
                self.assertIn(RAW_URL, content)
                self.assertNotIn("raw.githubusercontent.com/b1glord/", content)
                if "rpatchur/config.yml" in path:
                    self.assertIn("plist_url:", content)
                    self.assertIn("patch_url:", content)
                else:
                    self.assertIn("patch_list_url:", content)
                    self.assertIn("verify_checksums: true", content)

    def test_reserved_2022_identity_not_published(self):
        policy = json.loads((ROOT / "2022/beam/channel-policy.json").read_text(encoding="utf-8"))
        channel = json.loads((ROOT / "2022/channel.json").read_text(encoding="utf-8"))
        for key, value in IDENTITIES.items():
            self.assertEqual(policy[key], value)
        # Public JSON schema is intentionally stable across organization transfer.
        self.assertEqual(policy["schema"], "levelupgt.public-beam-distribution-policy.v1")
        self.assertIs(policy["ready"], False)
        self.assertIs(policy["publish_allowed"], False)
        self.assertEqual(policy["published_patch_count"], 0)
        self.assertIs(channel["ready"], False)
        self.assertEqual(channel["published_patch_count"], 0)
        feed = (ROOT / "2022/beam/patchlist.txt").read_text(encoding="utf-8")
        self.assertTrue(all(not line.strip() or line.lstrip().startswith("#")
                            for line in feed.splitlines()))
        self.assertEqual({p.name for p in (ROOT / "2022/data").iterdir()}, {"README.md"})
        self.assertFalse((ROOT / "2022/beam/config.yml").exists())

    def test_2015_root_and_2015_payload_aliases_remain_identical(self):
        legacy = {p.name: p for p in (ROOT / "2015/data").glob("*.thor")}
        root = {p.name: p for p in (ROOT / "data").glob("*.thor")}
        self.assertEqual(len(legacy), 26)
        self.assertEqual(set(legacy), set(root))
        self.assertEqual((ROOT / "2015/plist.txt").read_bytes(),
                         (ROOT / "plist.txt").read_bytes())
        for name in sorted(legacy):
            with self.subTest(asset=name):
                with legacy[name].open("rb") as left, root[name].open("rb") as right:
                    self.assertEqual(
                        hashlib.file_digest(left, "sha256").digest(),
                        hashlib.file_digest(right, "sha256").digest(),
                    )


if __name__ == "__main__":
    unittest.main()
