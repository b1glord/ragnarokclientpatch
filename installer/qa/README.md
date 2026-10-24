<!--
Dosya Yolu: installer/qa/README.md
Amac: Public Ragnar test installerinin Beam build ve dagitim sinirini kaydetmek
Modul - Markdown
Version: 1.0.0-qa
Aciklama: Public source-only reusable workflow; no private repo fetch or gameplay publication
Bagimli Oldugu Katman: GitHub Actions | LevelUpGT/beam-patcher | Turkuaz QA
-->

# Public Ragnar Windows Installer (QA)

The public installer artifact is **built and downloaded from the public
distribution repository**: `b1glord/ragnarokclientpatch`. The source
repository `LevelUpGT/beam-patcher` remains the source of Rust/Windows
installer code. The private `LevelUpGT/RagnarokClient` repository is not
contacted by this QA build or by the installed preview executable.

## Provenance and reproducible build

- Workflow: `.github/workflows/public-ragnar-installer-qa.yml`
- Pinned Beam source workflow and source commit:
  `4ac038f09235b6824941a7313668125e3c78fb29`
- Turkuaz Installer Community upstream dependency is separately pinned
  within the Beam QA reusable workflow.
- GitHub Actions executes the reusable workflow **in the public
  distribution repository context**, so its temporary Windows EXE
  artifact appears on the run under `b1glord/ragnarokclientpatch`.
- Client downloads only the resulting `RagnarClassic-Turkuaz-Setup.exe`,
  not a source repo, PAT, development SDK, private git checkout, or
  embedded Turkuaz .NET/WinUI distribution.
- All upstream code inputs are readable public repos; the workflow
  requests `contents: read` only. No cross-repo write secret required.

## Download and publish boundaries

This initial integration intentionally creates **GitHub Actions QA
artifacts**, not a production release, tag, Pages deployment or active
patch feed. GitHub may require login to retrieve Actions artifacts.
A stable anonymous public `download_url` requires a separate,
explicitly approved production publication design (for example a
signed GitHub Release in this public repo) after client compatibility
and signing checks.

The private game content is not included. This is the read-only Beam
visual preview, **not** a working private Ragnarok game client. The
product installer may use a public HTTPS endpoint in production, but
must never attempt to clone a private repository at the player's PC.

The `2015` channel aliases (`/data`, `/beam`, `plist.txt`)
remain unchanged. The `2022` patch channel remains `ready: false`
and `publish_allowed: false`. No `2022/data` patch, active
`version.json`, or client runtime settings may be created by this
installer QA workflow.

## Upgrade path after explicit approval

1. Build and review **signed release candidates** from trusted commits.
2. Complete client loader, GRF/backups/rollback and network tests.
3. Publish final artifacts to a dedicated public distribution channel,
   using a narrowly scoped deploy identity under a separate release
   workflow. Never expose a private code-repo token to the player.
4. Publish a signed metadata file with HTTPS address, version, SHA-256
   and source commit for the launcher to verify before update/install.
5. Preserve the existing 2015 channel and do not change 2022 policy
   without explicit user approval and matching compatibility evidence.

Reference standard look:
https://github.com/TurkuazLabs/TurkuazInstaller/pull/60

## Tests

`python3 -B -m unittest discover -s tests -p test_public_installer_contract.py -v`
confirms repository ownership, immutability and the absence of an
unapproved deployment. The called Windows CI builds and exercises the
real QA installer (including TurkuazInstaller CLI install/uninstall).
A green Actions build is not a real Windows 10 GUI smoke.
