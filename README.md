<!--
Dosya Yolu: REPO_ROOT/README.md
Amac: Ragnar Ragnarok Online istemci patch artifactlerini public olarak dagitmak
Modul - Markdown
Version: 1.0.1
Aciklama: Yeni organizasyonun kanonik URL'leri ve kilitli 2022 dagitim siniri
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

## Organizasyon transferi ve indirme URL'leri

Kanonik public patch root:
`https://raw.githubusercontent.com/LevelUpRagnarok/ragnarokclientpatch/main/`.

Eski raw indirme URL'lerinin transfer sonrasinda calistigini varsaymayin.
Kurulu istemcide onceden kayitli URL, burada bir template degisince otomatik
guncellenmez. Oyuncuya yeni config gondermeden once izole 2015 istemcide
gercek HTTP indirme, paket SHA-256 ve rollback testleri gereklidir.

`2022/channel.json.ready=false` ve
`2022/beam/channel-policy.json.publish_allowed=false` tutulur.
Bu sahiplik duzeltmesi bir release veya patch yayin izni degildir.
