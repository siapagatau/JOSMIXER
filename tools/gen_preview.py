#!/usr/bin/env python3
"""preview.svg = skin.svg + overlay hit area + label ID. Pakai: python3 gen_preview.py <dir skin> [...]"""
import re, sys, os

def lines(label, n=13):
    parts, cur, out = label.split("-"), "", []
    for p in parts:
        if cur and len(cur) + 1 + len(p) > n: out.append(cur); cur = p
        else: cur = f"{cur}-{p}" if cur else p
    return out + [cur]

def build(d):
    svg = open(os.path.join(d, "skin.svg"), encoding="utf-8").read()
    ov = []
    for m in re.finditer(r'<rect id="hit-([^"]+)" x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"', svg):
        i, x, y, w, h = m.group(1), *map(float, m.groups()[1:])
        ov.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="#ff2d95" fill-opacity="0.22" stroke="#ff2d95" stroke-width="2"/>')
        ls = lines(i)
        for k, t in enumerate(ls):
            ty = y + h / 2 + (k - (len(ls) - 1) / 2) * 13 + 4
            ov.append(f'<text x="{x + w/2:g}" y="{ty:g}" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="#ffffff" stroke="#000" stroke-width="0.6">{t}</text>')
    out = svg.replace("</svg>", f'<g id="preview-overlay">{"".join(ov)}</g></svg>')
    open(os.path.join(d, "preview.svg"), "w", encoding="utf-8").write(out)
    print("preview", d, len(ov), "elemen overlay")

if __name__ == "__main__":
    for d in sys.argv[1:]: build(d)
