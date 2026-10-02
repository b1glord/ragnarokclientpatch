# 📄 Dosya Yolu: /README.md
# 📌 Amac: Ragnar Ragnarok Online istemci patch artifactlerini public olarak dagitmak
# 📌 ClientDistribution - Markdown
# Version: 1.0.0
# Aciklama: Private RagnarokClient reposundan uretilen THOR manifest ve patch dosyalarinin public dagitim noktasidir
# Bagimli Oldugu Katman: Tool

# Ragnar Ragnarok Online - Patch Distribution

Bu repo **kaynak kod reposu degildir**. Oyuncu istemcilerinin indirecegi public patch artifactlerini tutar.

Kaynak ve build pipeline:

`LevelUpGT/RagnarokClient` (private)

Dagitim kanallari:

- Thor Legacy
- RPatchur
- Beam

Uc patcher da ilk fazda ayni canonical `.thor` paketlerini kullanir.

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
