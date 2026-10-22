# 20220406 Beam Patcher — reserved channel (NOT LIVE)

This folder reserves the future **2022 / Beam v1** patch feed. It is **not**
the 2015 root alias and is not a player release.

**Current status:** `../channel.json` remains `ready: false`, `published_patch_count: 0`.
No 2022 patch binaries, executables, GRFs, encrypted archives, published URL
or release manifest are authorized.

## Ownership and file layout

- Source of truth: `LevelUpGT/RagnarokClient/maps/data/<dungeon>/`.
  SHA-256 catalog: `RagnarokClient/maps/manifest.json`.
- Offline candidate builder and BEAM v1 format: `LevelUpGT/beam-patcher`.
- Public distribution (this repository): **approved output only**, in
  `2022/data/<approved>.beam`; feed is `2022/beam/patchlist.txt`.
- Proposed client GRF target: `tdata1.grf` (not an archive header field).
- Legacy `2015/` and root `data/`, `beam/`, `plist.txt` are immutable
  compatibility aliases for the 2015 THOR clients.

## Publishing gates

Publishing is blocked until ALL of the following are recorded:

1. Exact real 20220406 Ragexe binary identity (SHA-256 and PE version).
2. Client DATA.INI priority 0 points at a valid, registered `tdata1.grf`,
   and real multi-GRF loading is verified.
3. BEAM runtime's restricted `levelupgt/custom` profile, pinned EXE identity,
   protected (signed/authenticated) patch manifest and patch SHA-256.
4. Isolated real BEAM GRF application, backup, rollback, full 15-entry GRF
   readback, plus game smoke for all five Overlook maps.
5. RagnarokServer approved import/mapcache and live deployment review;
   unrelated NPC/AFK features remain untouched.
6. Explicit owner approval to publish the package into `2022/data/`, update
   `2022/beam/patchlist.txt`, and switch the 2022 channel to ready.

The existing locally validated `custom-maps.beam` (8,784,158 bytes) is a
**candidate only** and must NOT be committed here yet.

The patchlist intentionally contains **no entries**. Do not copy its 2015
counterpart or set `2022/channel.json.ready=true` without the above gates.

Encryption note: BEAM v1 is MD5 + zlib, **not encrypted**. No BEAM v2
encryption format is approved for this channel yet.
