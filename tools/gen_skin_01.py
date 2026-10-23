#!/usr/bin/env python3
"""Generator skin-01 'Mixer Studio' (1600x720). Pakai: python3 gen_skin_01.py [out_dir]
Menulis skin.svg + skin.json (PROMPT_SKIN_MIXER). Default out: ../skins/skin-01 (relatif skrip)."""
import json, math, sys, os

W, H = 1600, 720
HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "skins", "skin-01")
os.makedirs(out, exist_ok=True)

NAME, VER, AUTH = "Mixer Studio", "1.0", "Mixer"
bg, deco, ctrl, hit = [], [], [], []
controls, mapping = [], {}
ACC = "#ffa05c"                                   # aksen global (header, tombol)
C_MIC, C_REV, C_ECHO, C_EQM, C_EQA = "#ffa05c", "#5cc8ff", "#c792ff", "#6fe39a", "#ffd43b"
FONT = 'font-family="sans-serif"'

def panel(x1, y1, x2, y2, title, tx, col, sep=True):
    deco.append(f'<rect x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" rx="18" fill="url(#panelGrad)" stroke="#2a2e38" stroke-width="2"/>')
    deco.append(f'<rect x="{x1+2}" y="{y1+2}" width="{x2-x1-4}" height="8" rx="4" fill="{col}" fill-opacity="0.85"/>')
    deco.append(f'<circle cx="{tx-16}" cy="{y1+46}" r="6" fill="{col}"/>')
    deco.append(f'<text x="{tx}" y="{y1+55}" {FONT} font-size="26" font-weight="bold" fill="#e5e7eb">{title}</text>')
    if sep:
        deco.append(f'<line x1="{x1+20}" y1="{y1+80}" x2="{x2-20}" y2="{y1+80}" stroke="#2a2e38" stroke-width="2"/>')

def label(cx, y, t):
    deco.append(f'<text x="{cx}" y="{y}" text-anchor="middle" {FONT} font-size="20" font-weight="bold" fill="#9aa0b0">{t}</text>')

def hitrect(i, x, y, w, h):
    hit.append(f'<rect id="hit-{i}" x="{x}" y="{y}" width="{w}" height="{h}" fill="#000" fill-opacity="0"/>')

def toggle(name, x, y, fn, col):
    i = f"tg-{name}"
    ctrl.append(f'<g id="{i}" data-type="toggle">'
        f'<g id="{i}-off"><rect x="{x}" y="{y}" width="120" height="44" rx="22" fill="#20232d" stroke="#3a3f4b" stroke-width="2"/>'
        f'<circle cx="{x+24}" cy="{y+22}" r="8" fill="#3a3f4b"/>'
        f'<text x="{x+74}" y="{y+30}" text-anchor="middle" {FONT} font-size="20" font-weight="bold" fill="#8a90a0">OFF</text></g>'
        f'<g id="{i}-on" display="none"><rect x="{x}" y="{y}" width="120" height="44" rx="22" fill="{col}" stroke="#ffffff" stroke-opacity="0.55" stroke-width="2"/>'
        f'<circle cx="{x+24}" cy="{y+22}" r="8" fill="#ffffff"/>'
        f'<text x="{x+74}" y="{y+30}" text-anchor="middle" {FONT} font-size="20" font-weight="bold" fill="#101218">ON</text></g></g>')
    hitrect(i, x, y, 120, 44)
    controls.append({"id": i, "type": "toggle", "hit": f"hit-{i}", "states": {"off": f"{i}-off", "on": f"{i}-on"}})
    mapping[i] = {"function": fn}

def button(name, x, y, w, h, text, fn):
    i = f"btn-{name}"
    def body(fill, stroke, col):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
                f'<text x="{x+w/2}" y="{y+h/2+8}" text-anchor="middle" {FONT} font-size="22" font-weight="bold" fill="{col}">{text}</text>')
    ctrl.append(f'<g id="{i}" data-type="button"><g id="{i}-normal">{body("#252936","#3a3f4b","#e5e7eb")}</g>'
                f'<g id="{i}-active" display="none">{body(ACC,"#ffd2b0","#101218")}</g></g>')
    hitrect(i, x, y, w, h)
    controls.append({"id": i, "type": "button", "hit": f"hit-{i}", "states": {"normal": f"{i}-normal", "active": f"{i}-active"}})
    mapping[i] = {"function": fn}

def pt(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.sin(a), cy - r * math.cos(a)

def knob(name, cx, cy, text, fn, col, default=0.5):
    i = f"knob-{name}"
    r = 36
    x0, y0 = pt(cx, cy, r + 11, -135); x1, y1 = pt(cx, cy, r + 11, 135)
    ticks = "".join('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#5a6072" stroke-width="3" stroke-linecap="round"/>'
                    % (*pt(cx, cy, r + 15, -135 + 45 * k), *pt(cx, cy, r + 19, -135 + 45 * k)) for k in range(7))
    deco.append(f'<g>{ticks}</g>')
    ctrl.append(f'<g id="{i}" data-type="rotary" data-cx="{cx}" data-cy="{cy}" data-angle-min="-135" data-angle-max="135" data-value-default="{default}">'
        f'<path id="{i}-track" d="M {x0:.1f} {y0:.1f} A {r+11} {r+11} 0 1 1 {x1:.1f} {y1:.1f}" fill="none" stroke="#3a3f4b" stroke-width="5" stroke-linecap="round"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r+4}" fill="#0b0d12"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#knobGrad)" stroke="#2a2e38" stroke-width="2"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r-13}" fill="#151821" stroke="#2a2e38" stroke-width="2"/>'
        f'<g id="{i}-handle"><line x1="{cx}" y1="{cy-6}" x2="{cx}" y2="{cy-r+5}" stroke="{col}" stroke-width="6" stroke-linecap="round"/></g></g>')
    label(cx, cy + 74, text)
    hitrect(i, cx - 48, cy - 48, 96, 96)
    controls.append({"id": i, "type": "rotary", "hit": f"hit-{i}", "track": f"{i}-track", "handle": f"{i}-handle",
                     "angleMin": -135, "angleMax": 135, "defaultValue": default})
    mapping[i] = {"function": fn}

def slider(name, cx, yb, yt, text, fn, col, default=0.5):
    i = f"sl-{name}"
    ym = yb + (yt - yb) * default
    ticks = "".join(f'<line x1="{cx-38}" y1="{yb+(yt-yb)*k/4:.1f}" x2="{cx-30}" y2="{yb+(yt-yb)*k/4:.1f}" stroke="#5a6072" stroke-width="3" stroke-linecap="round"/>'
                    f'<line x1="{cx+30}" y1="{yb+(yt-yb)*k/4:.1f}" x2="{cx+38}" y2="{yb+(yt-yb)*k/4:.1f}" stroke="#5a6072" stroke-width="3" stroke-linecap="round"/>'
                    for k in range(5))
    deco.append(f'<g>{ticks}</g>')
    ctrl.append(f'<g id="{i}" data-type="slider" data-x1="{cx}" data-y1="{yb}" data-x2="{cx}" data-y2="{yt}" data-value-default="{default}">'
        f'<line id="{i}-track" x1="{cx}" y1="{yb}" x2="{cx}" y2="{yt}" stroke="#0b0d12" stroke-width="12" stroke-linecap="round"/>'
        f'<line x1="{cx}" y1="{yb}" x2="{cx}" y2="{yt}" stroke="#3a3f4b" stroke-width="3" stroke-linecap="round"/>'
        f'<g id="{i}-handle"><rect x="{cx-26}" y="{ym-15}" width="52" height="30" rx="8" fill="url(#knobGrad)" stroke="{col}" stroke-width="2"/>'
        f'<line x1="{cx-17}" y1="{ym-6}" x2="{cx+17}" y2="{ym-6}" stroke="#2a2e38" stroke-width="3" stroke-linecap="round"/>'
        f'<line x1="{cx-17}" y1="{ym+6}" x2="{cx+17}" y2="{ym+6}" stroke="#2a2e38" stroke-width="3" stroke-linecap="round"/>'
        f'<line x1="{cx-20}" y1="{ym}" x2="{cx+20}" y2="{ym}" stroke="{col}" stroke-width="4" stroke-linecap="round"/></g></g>')
    label(cx, yb + 40, text)
    hitrect(i, cx - 32, yt - 20, 64, yb - yt + 40)
    controls.append({"id": i, "type": "slider", "hit": f"hit-{i}", "track": f"{i}-track", "handle": f"{i}-handle", "defaultValue": default})
    mapping[i] = {"function": fn}

def meter(name, x, y, text, fn, n=18):
    i = f"meter-{name}"
    segs, dims = [], []
    for k in range(n):
        c = "#3ddc6b" if k < 11 else ("#ffd43b" if k < 15 else "#ff4b4b")
        sx = x + k * 22
        dims.append(f'<rect x="{sx}" y="{y}" width="18" height="22" rx="3" fill="{c}" fill-opacity="0.16"/>')
        segs.append(f'<rect id="{i}-seg-{k+1}" x="{sx}" y="{y}" width="18" height="22" rx="3" fill="{c}" display="none"/>')
    deco.append(f'<rect x="{x-8}" y="{y-6}" width="{n*22+2}" height="34" rx="8" fill="#0b0d12" stroke="#2a2e38" stroke-width="2"/>')
    deco.append(f'<g id="deco-{i}-dim">{"".join(dims)}</g>')
    deco.append(f'<text x="{x-18}" y="{y+18}" text-anchor="end" {FONT} font-size="20" font-weight="bold" fill="#9aa0b0">{text}</text>')
    ctrl.append(f'<g id="{i}" data-type="meter">{"".join(segs)}</g>')
    controls.append({"id": i, "type": "meter", "segments": [f"{i}-seg-{k+1}" for k in range(n)]})
    mapping[i] = {"function": fn}

# ---- latar, header, sekrup ----
bg.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#bgGrad)"/>')
deco.append(f'<rect x="0" y="0" width="{W}" height="130" fill="#161922"/>')
deco.append(f'<rect x="0" y="126" width="{W}" height="4" fill="{ACC}" fill-opacity="0.8"/>')
deco.append(f'<g id="deco-logo"><text x="40" y="76" {FONT} font-size="44" font-weight="bold" fill="{ACC}">MIXER</text>'
            f'<text x="42" y="106" {FONT} font-size="18" font-weight="bold" fill="#6b7186">KARAOKE STUDIO</text></g>')
for sx, sy in ((14, 14), (1586, 14), (14, 706), (1586, 706)):
    deco.append(f'<circle cx="{sx}" cy="{sy}" r="6" fill="#2a2e38" stroke="#0b0d12" stroke-width="2"/>')
ctrl.append('<g id="slot-display"><rect x="230" y="25" width="410" height="80" rx="10" fill="#1b2310" stroke="#2f3a0c" stroke-width="3"/>'
            '<text x="244" y="58" font-family="monospace" font-size="24" fill="#b8f27c">MIC OFF</text></g>')
controls.append({"id": "slot-display", "type": "display", "lines": 2})
mapping["slot-display"] = {"function": "display.status",
    "template": ["MIC {mic:ONOFF}  REV {reverb:ONOFF}", "ECHO {echo:ONOFF}  EQ {eqmic:ONOFF}"], "textColor": "#b8f27c"}
meter("mic", 760, 40, "MIC", "meter.mic")
meter("output", 760, 84, "OUT", "meter.output")
button("floating", 1170, 35, 120, 60, "FLOAT", "floating.toggle")
button("theme", 1300, 35, 120, 60, "TEMA", "theme.open")
button("skin", 1430, 35, 120, 60, "SKIN", "skin.pick")

# ---- baris 1 ----
panel(30, 150, 380, 430, "MIC", 214, C_MIC)
toggle("mic", 60, 175, "mic.toggle", C_MIC)
knob("mic-volume", 105, 320, "VOLUME", "mic.volume", C_MIC)
knob("mic-gate", 245, 320, "GATE", "mic.gate", C_MIC)

panel(395, 150, 1095, 430, "REVERB", 565, C_REV)
toggle("reverb", 425, 175, "reverb.toggle", C_REV)
for k, (n, t, f, d) in enumerate([("wet","WET","reverb.wet",0.35),("dry","DRY","reverb.dry",0.85),("width","WIDTH","reverb.width",1.0),
                                  ("damp","DAMP","reverb.damp",0.3),("room","ROOM","reverb.room",0.6),("cess","CESS","reverb.cess",0.6)]):
    knob(f"reverb-{n}", 455 + 114 * k, 320, t, f, C_REV, d)

panel(1110, 150, 1570, 430, "ECHO", 1280, C_ECHO)
toggle("echo", 1140, 175, "echo.toggle", C_ECHO)
for k, (n, t, f) in enumerate([("delay","DELAY","echo.delay"),("feedback","REPEAT","echo.feedback"),("mix","MIX","echo.mix")]):
    knob(f"echo-{n}", 1200 + 120 * k, 320, t, f, C_ECHO)

# ---- baris 2 ----
panel(30, 450, 480, 700, "EQ MIC", 214, C_EQM)
toggle("eqmic", 60, 475, "eqmic.toggle", C_EQM)
for k, (n, t) in enumerate([("low","LOW"),("mid","MID"),("high","HIGH")]):
    knob(f"eqmic-{n}", 105 + 130 * k, 612, t, f"eqmic.{n}", C_EQM)

panel(495, 450, 1570, 700, "EQ AUDIO", 665, C_EQA)
toggle("eqaudio", 525, 475, "eqaudio.toggle", C_EQA)
for k, (n, t) in enumerate([("gain","GAIN"),("sub","SUB"),("low","LOW"),("mid","MID"),("high","HIGH")]):
    slider(f"eqaudio-{n}", 700 + 190 * k, 646, 548, t, f"eqaudio.{n}", C_EQA)

defs = ('<defs>'
        '<radialGradient id="knobGrad" cx="40%" cy="35%" r="75%"><stop offset="0" stop-color="#4a5064"/><stop offset="1" stop-color="#1d2029"/></radialGradient>'
        '<linearGradient id="panelGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e2230"/><stop offset="1" stop-color="#161922"/></linearGradient>'
        '<linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d0f14"/><stop offset="1" stop-color="#171a24"/></linearGradient>'
        '</defs>')
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" data-skin-name="{NAME}" data-skin-version="{VER}" data-skin-author="{AUTH}" '
       f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">{defs}'
       f'<g id="layer-bg">{"".join(bg)}</g><g id="layer-deco">{"".join(deco)}</g>'
       f'<g id="layer-controls">{"".join(ctrl)}</g><g id="layer-hit">{"".join(hit)}</g></svg>')
open(os.path.join(out, "skin.svg"), "w", encoding="utf-8").write(svg)

js = {"schemaVersion": 1, "kind": "mixer", "name": NAME, "version": VER, "author": AUTH,
      "svg": "skin.svg", "viewBox": f"0 0 {W} {H}", "layout": {"zone": f"0 0 {W} {H}"},
      "controls": controls, "mapping": mapping,
      "unsupportedInReference": [{"id": "deco-logo", "kind": "decorative", "label": "LOGO", "reason": "tanpa fungsi"}]}
open(os.path.join(out, "skin.json"), "w", encoding="utf-8").write(json.dumps(js, indent=1, ensure_ascii=False))
print("ok", out, len(controls), "kontrol")
