# CHECKPOINT
Tujuan Utama: ubah APK mic karaoke (com.karaoke.reverbmic) jadi APK mixer landscape ala DTX:
1) landscape penuh + tema (ThemeState/ColorPickerDialog DTX); 2) Skin Engine dari skin/ DTX (SVG+skin.json+hit area);
3) skin diunduh dari github.com/siapagatau/SKIN-MIXER-HP (index.json, sha256, cache offline, fallback default);
4) engine audio Oboe/C++ (reverb, echo, EQ, gate, EQ global, floating, meter LED) tetap, tidak ditulis ulang;
5) aturan skin: PROMPT_SKIN_MIXER.md.
Tahap selesai: 0,1,2,3,4,5,6,7 (SEMUA)   Tahap berikutnya: tidak ada — proyek final menunggu build & uji perangkat.
File penting: README.md (final); docs/{peta,skin-engine,mapping-table}.md; skin/*.kt; skins-repo/ (isi repo SKIN-MIXER-HP);
  tools/{gen_skin_01,gen_preview,index,validate,check_all}.py; assets/skins/default (= skin-01); app/proguard-rules.pro; versi 2.0 (code 6).
Keputusan: Kotlin 1.9.24 + Compose compiler 1.5.14 dipertahankan (kode port DTX disesuaikan); jalur floating/EQ global skin = jalur UI klasik;
  fallback skin: terunduh -> bawaan -> UI klasik; katalog fungsi 30 buah identik di PROMPT §5, FunctionRegistry.kt, validate.py (dicek check_all.py).
Validasi tahap 7: `python3 tools/check_all.py PROMPT_SKIN_MIXER.md` -> SEMUA LOLOS (validate skin-01 & default, index sha256/size, default==skin-01,
  skins-repo tanpa kode APK, katalog konsisten, SVG bebas elemen terlarang).
Masalah/belum dibuild: BELUM PERNAH dikompilasi atau dijalankan di perangkat (sandbox tanpa Android SDK/Kotlin/jaringan) -> hanya review statis.
  Kemungkinan error kompilasi kecil tersisa; render AndroidSVG, preview.svg, unduh nyata, floating & EQ global di HP belum teruji;
  repo SKIN-MIXER-HP belum di-push (isi = skins-repo/ atau SKIN-MIXER-HP.zip).
Next Update (setelah tahap 7, di luar rencana awal):
 1. Push proyek -> jalankan Actions -> bila gagal kirim log/artefak build-reports; perbaiki hanya file yang disebut.
 2. Push skins-repo/ ke github.com/siapagatau/SKIN-MIXER-HP (branch main, index.json di root).
 3. Uji di HP: skin tampil & stretch, knob/slider/toggle, meter, mic ON, floating, EQ global, SKIN -> UNDUH -> PAKAI -> restart offline.
 4. Skin tambahan: 1 gambar = 1 skin = 1 sesi (turunan gen_skin_01.py), lalu check_all.py.
Perintah untuk AI berikutnya: "Baca CHECKPOINT.md. Perbaiki error build/uji dari log berikut: <tempel>."
