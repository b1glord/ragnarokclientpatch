<!--
Dosya Yolu: REPO_ROOT/README.md
Amac: Ragnar patch dagitiminin kaynak sinirlarini belgeler
Modul - Markdown
Version: 1.0.1
Aciklama: Public installer QA sahiplik referanslari
Bagimli Oldugu Katman: Documentation
-->

# Ragnar Ragnarok Online - Patch Distribution

Bu repo **kaynak kod reposu degildir**. Oyuncu istemcilerinin indirecegi public patch artifactlerini tutar.

Kaynak ve build pipeline:

`LevelUpRagnarok/RagnarokClient` (private)

Dagitim kanallari:

- Thor Legacy
- RPatchur
- Beam

**Bu ortak THOR akisi sadece 2015/legacy uyumluluk kanali icindir.** 20220406 profili farkli ve su an kilitlidir (`2022/channel.json`: `ready: false`). Yeni BEAM v1 adaylari, kaynagi `LevelUpRagnarok/RagnarokClient`, olusturucusu `LevelUpRagnarok/beam-patcher` olacak sekilde ayri bir 2022/beam dagitim kanali uzerinden, yalnizca onaydan sonra yayimlanabilir.

## Public yapi

```text
/
  plist.txt
  channel.json
  data/
    *.thor
  rpatchur/
  beam/
    patchlist.txt
```

`plist.txt` Thor Legacy ve RPatchur tarafindan kullanilir.

`beam/patchlist.txt` Beam tarafindan kullanilir ve ayni THOR paketlerinin SHA-256 degerlerini tasir.

Bu repoya patch artifactleri elle duzenlenmek yerine private kaynak repodaki GitHub Actions pipeline'i tarafindan yayinlanir.

## 20220406 icin ayrilmis BEAM dagitim kanali

- [2022/beam/README.md](2022/beam/README.md) — kaynak, sahiplik ve onay kapilari.
- [2022/beam/channel-policy.json](2022/beam/channel-policy.json) — yayina kapali kanal sozlesmesi.
- [2022/beam/patchlist.txt](2022/beam/patchlist.txt) — bilerek bos; oyunculara paket yonlendirmez.

**Dikkat:** `data/`, `beam/`, `plist.txt` kok aliaslari 2015'e aittir, yeni haritalar bu yollara eklenmez. `2022/data/` altinda su anda onaylanmis `.beam` paketi bulunmaz. Patch dosyalarini hazirlamak, yayin izni verildigi anlamina gelmez.

## Ragnar kurulum EXE - public QA

Tek pencereli Turkuaz temali Ragnar **gorunum onizlemesi** kurulumunun
kaynak derlemesi public `LevelUpRagnarok/beam-patcher` commit'inden yapilir;
QA artifact indirme noktasi bu public dagitim deposunun Actions sayfasidir.
Private `LevelUpRagnarok/RagnarokClient` oyuncu istemcisinden istenmez.
Ayrintilar: [installer/qa/README.md](installer/qa/README.md).
Bu akista release/aktif yama kanali yayinlanmaz.
