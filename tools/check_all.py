#!/usr/bin/env python3
"""Validasi akhir proyek mixer (tahap 7). Pakai (dari root proyek): python3 tools/check_all.py [PROMPT_SKIN_MIXER.md]
Cek: (1) validate.py semua skin + skin default, (2) index.json cocok, (3) skin default == skin-01, (4) skins-repo tanpa kode APK,
(5) katalog fungsi: FunctionRegistry.kt == validate.py (== PROMPT bila diberikan), semua fungsi punya penanganan di dispatcher/binding,
(6) semua skin.svg bebas elemen terlarang. Exit 1 bila ada yang gagal."""
import glob, hashlib, json, os, re, subprocess, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import validate as V
SK = os.path.join(ROOT, "app/src/main/java/com/karaoke/reverbmic/skin")
fails = []
def check(name, ok, detail=""):
    print(("OK    " if ok else "GAGAL ") + name + (f"  {detail}" if detail and not ok else ""))
    if not ok: fails.append(name)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

# 1. validate semua skin
dirs = sorted(glob.glob(os.path.join(ROOT, "skins-repo/skins/*"))) + [os.path.join(ROOT, "app/src/main/assets/skins/default")]
for d in dirs:
    e, w = V.check(d)
    check("validate " + os.path.relpath(d, ROOT), not e, "; ".join(e[:3]))
# 2. index
r = subprocess.run([sys.executable, os.path.join(ROOT, "tools/index.py"), os.path.join(ROOT, "skins-repo"), "--check"], capture_output=True, text=True)
check("index.json cocok (sha256+size)", r.returncode == 0, r.stdout.strip())
# 3. default == skin-01
dflt = os.path.join(ROOT, "app/src/main/assets/skins/default"); s01 = os.path.join(ROOT, "skins-repo/skins/skin-01")
check("skin default == skin-01", all(sha(os.path.join(dflt, f)) == sha(os.path.join(s01, f)) for f in ("skin.svg", "skin.json")))
# 4. tanpa kode APK di skins-repo
bad = [p for p in glob.glob(os.path.join(ROOT, "skins-repo/**/*"), recursive=True) if re.search(r"\.(kt|java|gradle|kts|cpp|h|xml|apk)$", p)]
check("skins-repo tanpa kode APK", not bad, str(bad))
# 5. katalog fungsi
reg = set(re.findall(r'"([a-z]+\.[a-z]+)"', open(os.path.join(SK, "FunctionRegistry.kt")).read()))
val = set(V.TOGGLE) | set(V.VALUE) | set().union(*V.ALLOWED.values())
check("FunctionRegistry == validate.py", reg == val, str(reg ^ val))
if len(sys.argv) > 1:
    sec = open(sys.argv[1], encoding="utf-8").read().split("## 5.")[1].split("## 6.")[0]
    cat = {t for l in sec.splitlines() if re.match(r"\|\s*`", l) for t in re.findall(r"`([a-z]+\.[a-z]+)`", l.split("|")[1])}
    check("katalog PROMPT_SKIN_MIXER §5 == registry", cat == reg, str(cat ^ reg))
handled = set(re.findall(r'"([a-z]+\.[a-z]+)"', open(os.path.join(SK, "SkinActionDispatcher.kt")).read()))
handled |= {"meter.mic", "meter.output", "display.status"}   # ditangani SkinBinding (meter) & displayText
check("semua function punya penanganan", reg <= handled, str(reg - handled))
# 6. elemen terlarang di semua skin.svg & preview.svg
forb = re.compile(r"<(script|foreignObject|image|use|audio|video|iframe|metadata|filter)\b|\son\w+=|href=|https?://(?!www\.w3\.org)", re.I)
badsvg = [os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "**/*.svg"), recursive=True) if forb.search(open(p, encoding="utf-8").read())]
check("svg bebas elemen/atribut terlarang", not badsvg, str(badsvg))
print("\nSEMUA LOLOS" if not fails else f"\n{len(fails)} GAGAL: {fails}")
sys.exit(1 if fails else 0)
