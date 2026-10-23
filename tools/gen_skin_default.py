#!/usr/bin/env python3
"""Generator skin mixer default (1600x720). Pakai: python3 gen_skin_default.py [out_dir]
Menulis skin.svg + skin.json. Dipakai ulang di tahap 4 (skin-01)."""
import json, math, sys, os

W, H = 1600, 720
out = sys.argv[1] if len(sys.argv) > 1 else "../app/src/main/assets/skins/default"
os.makedirs(out, exist_ok=True)

bg, deco, ctrl, hit = [], [], [], []
controls, mapping = [], {}
ACC = "#ffa05c"

def panel(x1, y1, x2, y2, title, tx):
    deco.append(f'<rect x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" rx="18" fill="#1a1d26" stroke="#2a2e38" stroke-width="2"/>')
    deco.append(f'<text x="{tx}" y="{y1+55}" font-family="sans-serif" font-size="26" font-weight="bold" fill="#e5e7eb">{title}</text>')

def label(cx, y, t):
    deco.append(f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="20" fill="#9aa0b0">{t}</text>')

def hitrect(i, x, y, w, h):
    hit.append(f'<rect id="hit-{i}" x="{x}" y="{y}" width="{w}" height="{h}" fill="#000" fill-opacity="0"/>')

def toggle(name, x, y, fn):
    i = f"tg-{name}"
    ctrl.append(f'<g id="{i}" data-type="toggle">'
        f'<g id="{i}-off"><rect x="{x}" y="{y}" width="120" height="44" rx="22" fill="#2a2e38" stroke="#3a3f4b" stroke-width="2"/>'
        f'<text x="{x+60}" y="{y+30}" text-anchor="middle" font-family="sans-serif" font-size="20" font-weight="bold" fill="#8a90a0">OFF</text></g>'
        f'<g id="{i}-on" display="none"><rect x="{x}" y="{y}" width="120" height="44" rx="22" fill="#2e7d32" stroke="#6fe39a" stroke-width="2"/>'
        f'<text x="{x+60}" y="{y+30}" text-anchor="middle" font-family="sans-serif" font-size="20" font-weight="bold" fill="#ffffff">ON</text></g></g>')
    hitrect(i, x, y, 120, 44)
    controls.append({"id": i, "type": "toggle", "hit": f"hit-{i}", "states": {"off": f"{i}-off", "on": f"{i}-on"}})
    mapping[i] = {"function": fn}

def button(name, x, y, w, h, text, fn):
    i = f"btn-{name}"
    def body(fill, stroke, col):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
                f'<text x="{x+w/2}" y="{y+h/2+8}" text-anchor="middle" font-family="sans-serif" font-size="22" font-weight="bold" fill="{col}">{text}</text>')
    ctrl.append(f'<g id="{i}" data-type="button"><g id="{i}-normal">{body("#2a2e38","#3a3f4b","#e5e7eb")}</g>'
                f'<g id="{i}-active" display="none">{body(ACC,"#ffd2b0","#101218")}</g></g>')
    hitrect(i, x, y, w, h)
    controls.append({"id": i, "type": "button", "hit": f"hit-{i}", "states": {"normal": f"{i}-normal", "active": f"{i}-active"}})
    mapping[i] = {"function": fn}

def pt(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.sin(a), cy - r * math.cos(a)

def knob(name, cx, cy, text, fn, default=0.5):
    i = f"knob-{name}"
    r = 36
    x0, y0 = pt(cx, cy, r + 11, -135); x1, y1 = pt(cx, cy, r + 11, 135)
    ctrl.append(f'<g id="{i}" data-type="rotary" data-cx="{cx}" data-cy="{cy}" data-angle-min="-135" data-angle-max="135" data-value-default="{default}">'
        f'<path id="{i}-track" d="M {x0:.1f} {y0:.1f} A {r+11} {r+11} 0 1 1 {x1:.1f} {y1:.1f}" fill="none" stroke="#3a3f4b" stroke-width="5" stroke-linecap="round"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r+4}" fill="#0b0d12"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#knobGrad)" stroke="#2a2e38" stroke-width="2"/>'
        f'<g id="{i}-handle"><line x1="{cx}" y1="{cy-8}" x2="{cx}" y2="{cy-r+6}" stroke="{ACC}" stroke-width="6" stroke-linecap="round"/></g></g>')
    label(cx, cy + 70, text)
    hitrect(i, cx - 48, cy - 48, 96, 96)
    controls.append({"id": i, "type": "rotary", "hit": f"hit-{i}", "track": f"{i}-track", "handle": f"{i}-handle",
                     "angleMin": -135, "angleMax": 135, "defaultValue": default})
    mapping[i] = {"function": fn}

def slider(name, cx, yb, yt, text, fn, default=0.5):
    i = f"sl-{name}"
    ym = yb + (yt - yb) * default
    ctrl.append(f'<g id="{i}" data-type="slider" data-x1="{cx}" data-y1="{yb}" data-x2="{cx}" data-y2="{yt}" data-value-default="{default}">'
        f'<line id="{i}-track" x1="{cx}" y1="{yb}" x2="{cx}" y2="{yt}" stroke="#0b0d12" stroke-width="10" stroke-linecap="round"/>'
        f'<line x1="{cx}" y1="{yb}" x2="{cx}" y2="{yt}" stroke="#3a3f4b" stroke-width="3" stroke-linecap="round"/>'
        f'<g id="{i}-handle"><rect x="{cx-24}" y="{ym-13}" width="48" height="26" rx="7" fill="url(#knobGrad)" stroke="{ACC}" stroke-width="2"/>'
        f'<line x1="{cx-16}" y1="{ym}" x2="{cx+16}" y2="{ym}" stroke="{ACC}" stroke-width="3" stroke-linecap="round"/></g></g>')
    label(cx, yb + 44, text)
    hitrect(i, cx - 32, yt - 20, 64, yb - yt + 40)
    controls.append({"id": i, "type": "slider", "hit": f"hit-{i}", "track": f"{i}-track", "handle": f"{i}-handle", "defaultValue": default})
    mapping[i] = {"function": fn}

def meter(name, x, y, text, fn, n=16):
    i = f"meter-{name}"
    segs, dims = [], []
    for k in range(n):
        c = "#3ddc6b" if k < 10 else ("#ffd43b" if k < 13 else "#ff4b4b")
        sx = x + k * 24
        dims.append(f'<rect x="{sx}" y="{y}" width="20" height="22" rx="3" fill="{c}" fill-opacity="0.16"/>')
        segs.append(f'<rect id="{i}-seg-{k+1}" x="{sx}" y="{y}" width="20" height="22" rx="3" fill="{c}" display="none"/>')
    deco.append(f'<g id="deco-{i}-dim">{"".join(dims)}</g>')
    deco.append(f'<text x="{x-14}" y="{y+18}" text-anchor="end" font-family="sans-serif" font-size="20" fill="#9aa0b0">{text}</text>')
    ctrl.append(f'<g id="{i}" data-type="meter">{"".join(segs)}</g>')
    controls.append({"id": i, "type": "meter", "segments": [f"{i}-seg-{k+1}" for k in range(n)]})
    mapping[i] = {"function": fn}

# ---- latar & header ----
bg.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#101218"/>')
deco.append(f'<rect x="0" y="0" width="{W}" height="130" fill="#161922"/>')
deco.append(f'<g id="deco-logo"><text x="40" y="82" font-family="sans-serif" font-size="40" font-weight="bold" fill="{ACC}">MIXER</text></g>')
ctrl.append('<g id="slot-display"><rect x="220" y="25" width="420" height="80" rx="10" fill="#1b2310" stroke="#2f3a0c" stroke-width="2"/>'
            '<text x="232" y="58" font-family="monospace" font-size="24" fill="#b8f27c">MIC OFF</text></g>')
controls.append({"id": "slot-display", "type": "display", "lines": 2})
mapping["slot-display"] = {"function": "display.status",
    "template": ["MIC {mic:ONOFF}  REV {reverb:ONOFF}", "ECHO {echo:ONOFF}  EQ {eqmic:ONOFF}"], "textColor": "#b8f27c"}
meter("mic", 740, 40, "MIC", "meter.mic")
meter("output", 740, 84, "OUT", "meter.output")
button("floating", 1160, 35, 120, 60, "FLOAT", "floating.toggle")
button("theme", 1290, 35, 120, 60, "TEMA", "theme.open")
button("skin", 1420, 35, 120, 60, "SKIN", "skin.pick")

# ---- baris 1 ----
panel(30, 150, 380, 430, "MIC", 200)
toggle("mic", 60, 175, "mic.toggle")
knob("mic-volume", 105, 320, "VOLUME", "mic.volume")
knob("mic-gate", 245, 320, "GATE", "mic.gate")

panel(395, 150, 1095, 430, "REVERB", 565)
toggle("reverb", 425, 175, "reverb.toggle")
for k, (n, t, f, d) in enumerate([("wet","WET","reverb.wet",0.35),("dry","DRY","reverb.dry",0.85),("width","WIDTH","reverb.width",1.0),
                                  ("damp","DAMP","reverb.damp",0.3),("room","ROOM","reverb.room",0.6),("cess","CESS","reverb.cess",0.6)]):
    knob(f"reverb-{n}", 460 + 110 * k, 320, t, f, d)

panel(1110, 150, 1570, 430, "ECHO", 1280)
toggle("echo", 1140, 175, "echo.toggle")
for k, (n, t, f) in enumerate([("delay","DELAY","echo.delay"),("feedback","REPEAT","echo.feedback"),("mix","MIX","echo.mix")]):
    knob(f"echo-{n}", 1200 + 120 * k, 320, t, f)

# ---- baris 2 ----
panel(30, 450, 480, 700, "EQ MIC", 200)
toggle("eqmic", 60, 475, "eqmic.toggle")
for k, (n, t) in enumerate([("low","LOW"),("mid","MID"),("high","HIGH")]):
    knob(f"eqmic-{n}", 105 + 130 * k, 600, t, f"eqmic.{n}")

panel(495, 450, 1570, 700, "EQ AUDIO", 665)
toggle("eqaudio", 525, 475, "eqaudio.toggle")
for k, (n, t) in enumerate([("gain","GAIN"),("sub","SUB"),("low","LOW"),("mid","MID"),("high","HIGH")]):
    slider(f"eqaudio-{n}", 700 + 190 * k, 650, 530, t, f"eqaudio.{n}")

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" data-skin-name="Mixer Default" data-skin-version="1.0" data-skin-author="Mixer" '
       f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
       '<defs><radialGradient id="knobGrad" cx="40%" cy="35%" r="75%"><stop offset="0" stop-color="#4a5064"/><stop offset="1" stop-color="#1d2029"/></radialGradient></defs>'
       f'<g id="layer-bg">{"".join(bg)}</g><g id="layer-deco">{"".join(deco)}</g>'
       f'<g id="layer-controls">{"".join(ctrl)}</g><g id="layer-hit">{"".join(hit)}</g></svg>')
open(os.path.join(out, "skin.svg"), "w", encoding="utf-8").write(svg)

js = {"schemaVersion": 1, "kind": "mixer", "name": "Mixer Default", "version": "1.0", "author": "Mixer",
      "svg": "skin.svg", "viewBox": f"0 0 {W} {H}", "layout": {"zone": f"0 0 {W} {H}"},
      "controls": controls, "mapping": mapping,
      "unsupportedInReference": [{"id": "deco-logo", "kind": "decorative", "label": "LOGO", "reason": "tanpa fungsi"}]}
open(os.path.join(out, "skin.json"), "w", encoding="utf-8").write(json.dumps(js, indent=1, ensure_ascii=False))
print("ok", out, len(controls), "kontrol")
