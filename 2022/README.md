# Ragnar Ragnarok Online - 20220406 Candidate Channel

Exact build: 20220406
PACKETVER: 20220406
Server compatibility: 20220406-candidate
Status: candidate-audit
Ready: false
Published patches: 0

Server login -> char -> map -> spawn compatibility is already recorded as passed.
This channel intentionally contains no legacy THOR package.
Client artifact audit, patch rebuild and three-patcher smoke tests must complete before publishing is enabled.

## Yeni BEAM v1 dagitim adayi (kilitli)

2022 icin 2015 THOR paketleri tekrar kullanilmaz. 2022 Beam kanalinin
kaynak/paket/depoya yazma sorumluluklari ve release kapilari
[beam/README.md](beam/README.md) altinda kayitli. [beam/patchlist.txt](beam/patchlist.txt)
bilerek bostur. [beam/channel-policy.json](beam/channel-policy.json) dosyasi
`publish_allowed: false` ilan eder.

`ready` hala `false`; Beam paket adayi yerelde test edilmistir ama
kamusal `2022/data/` klasorune **hicbir paket gonderilmemistir**.
