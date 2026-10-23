# CHECKPOINT SKIN (repo SKIN-MIXER-HP)
Tujuan: repo skin mixer sesuai PROMPT_SKIN_MIXER.md; diunduh APK (index.json, sha256, size).
Skin selesai: skin-01 "Mixer Studio" 1.0 (1600x720, 30 kontrol, validate.py OK, index.py --check OK).
Skin berikutnya: belum ada (1 gambar = 1 skin = 1 sesi; buat tools/gen_skin_XX.py baru turunan gen_skin_01.py).
Alat: tools/gen_skin_01.py, gen_preview.py, validate.py, index.py (pakai ulang).
Catatan: skin-01 identik dengan APK assets/skins/default (salinan). Ubah satu -> regenerasi + salin ke yang lain.
index.json format: {schemaVersion, repo, kind, updated, skins[{id,name,version,author,path,files{...}}]}.
Masalah: preview.svg belum dilihat visual (sandbox tanpa renderer SVG); validasi hanya struktural.
