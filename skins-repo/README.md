# SKIN-MIXER-HP
Repo skin untuk APK Mixer Karaoke (`com.karaoke.reverbmic`). Hanya berisi skin, tanpa kode APK.
Aturan skin: `PROMPT_SKIN_MIXER.md`.

```
index.json                      daftar skin + sha256 + size (dibaca APK)
skins/<id>/skin.svg skin.json preview.svg
tools/                          gen_skin_01.py gen_preview.py validate.py index.py
```

## Skin
| id | nama | kontrol |
|---|---|---|
| skin-01 | Mixer Studio 1.0 | 30 (mic, reverb 6 knob, echo, EQ mic, EQ audio 5 slider, 2 meter LED, display, 3 tombol) |

## Alur membuat / mengubah skin
```
python3 tools/gen_skin_01.py skins/skin-01      # skin.svg + skin.json
python3 tools/gen_preview.py skins/skin-01      # preview.svg (overlay hit area)
python3 tools/validate.py skins/skin-01         # harus OK
python3 tools/index.py .                        # index.json (setelah file final)
python3 tools/index.py . --check                # verifikasi sha256/size
```
URL unduhan APK: `https://raw.githubusercontent.com/siapagatau/SKIN-MIXER-HP/main/index.json`.
Salah satu sha256/size tidak cocok = unduhan ditolak APK.
