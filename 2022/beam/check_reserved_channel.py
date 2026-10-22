#!/usr/bin/env python3
# Dosya Yolu: 2022/beam/check_reserved_channel.py
# Amac: Ensure the 20220406 BEAM distribution stays disabled until approval
# Modul - Python validation
# Version: 0.1.0-candidate
# Aciklama: Read-only guard, no deploy/network/patch/client writes
# Bagimli Oldugu Katman: 2022/channel.json | 2022/beam/channel-policy.json
"""Fail closed on accidental publication into the reserved Beam 2022 channel."""

import argparse
import json
import sys
from pathlib import Path


class ChannelBlocked(ValueError):
    pass


def require(ok, reason):
    if not ok:
        raise ChannelBlocked(reason)


def plain_file(path, limit=131072):
    require(path.is_file() and not path.is_symlink(), f"REQUIRED_REGULAR_FILE_MISSING: {path}")
    require(path.stat().st_size < limit, f"FILE_TOO_LARGE: {path}")
    return path.read_text(encoding="utf-8-sig")


def audit(root):
    root = Path(root)
    channel = json.loads(plain_file(root / "2022/channel.json"))
    policy = json.loads(plain_file(root / "2022/beam/channel-policy.json"))
    require(channel.get("client_profile") == "2022" and
            channel.get("exact_build") == "20220406" and
            channel.get("ready") is False and
            channel.get("published_patch_count") == 0,
            "2022_CHANNEL_NOT_RESERVED")
    require(policy.get("schema") == "levelupgt.public-beam-distribution-policy.v1" and
            policy.get("client_profile") == "2022" and
            policy.get("exact_client_build") == "20220406" and
            policy.get("ready") is False and
            policy.get("publish_allowed") is False and
            policy.get("published_patch_count") == 0 and
            policy.get("artifact_directory") == "2022/data" and
            policy.get("patch_list") == "2022/beam/patchlist.txt" and
            policy.get("format") == "beam-v1" and
            policy.get("target_grf_candidate") == "tdata1.grf",
            "2022_BEAM_PUBLISH_POLICY_NOT_LOCKED")
    for line in plain_file(root / "2022/beam/patchlist.txt").splitlines():
        require(not line.strip() or line.lstrip().startswith("#"),
                "2022_BEAM_FEED_CONTAINS_ACTIVE_PATCH")
    data = root / "2022/data"
    require(data.is_dir() and not data.is_symlink(), "2022_DATA_DIR_MISSING")
    for entry in data.iterdir():
        require(entry.name == "README.md" and entry.is_file() and
                not entry.is_symlink(), "2022_DATA_HAS_UNAPPROVED_ASSET")
    for file in ("config.yml", "regional-patches.json", "version.json"):
        require(not (root / "2022/beam" / file).exists(),
                "2022_BEAM_ACTIVE_RUNTIME_CONFIG_UNAPPROVED")
    # Compatibility aliases must not accidentally become 2022 BEAM feeds.
    for folder in (root / "data", root / "2015/data"):
        require(folder.is_dir(), "2015_LEGACY_CHANNEL_MISSING")
        require(not any(x.name.lower().endswith(".beam") for x in folder.iterdir()),
                "BEAM_ASSET_IN_LEGACY_2015_FEED")
    return "2022_BEAM_CHANNEL_RESERVED_OK ready=false published=0; 2015 unchanged by validator"


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = cli.parse_args()
    print(audit(args.root))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print("2022_BEAM_CHANNEL_REJECTED: " + str(exc), file=sys.stderr)
        sys.exit(1)
