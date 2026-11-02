#!/usr/bin/env python3
"""Visualize strict peaks of the horizontal-edge landscape.

For a given n, find the strict peaks (paths where every backbite move
decreases the number of horizontal edges), pick a diverse subset, and draw
them:

  * results/peak_viz/peaks_n{n}.html   -- browsable SVG gallery
  * results/peak_viz/peaks_n{n}.md     -- text arrow-grid drawings

Usage:
    python3 scripts/visualize_peaks.py --n 4
    python3 scripts/visualize_peaks.py --n 6 --max-peaks 30
    python3 scripts/visualize_peaks.py --n 7 --sample 30000 --max-peaks 24
"""

import argparse
import random
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hampath import backbite_moves, build_adjacency, enumerate_hamiltonian_paths
from hampath.backbite import random_backbite_step
from hampath import serpentine_path, random_backtracking_path

BLUE = "#2563eb"
RED = "#dc2626"


def h_count(n, seq):
    return sum(1 for a, b in zip(seq, seq[1:]) if a // n == b // n)


def vertical_cols(n, seq):
    return tuple(a % n for a, b in zip(seq, seq[1:]) if a // n != b // n)


def text_draw(n, seq):
    g = [['  '] * n for _ in range(n)]
    for i, (a, b) in enumerate(zip(seq, seq[1:])):
        ra, ca = divmod(a, n)
        rb, cb = divmod(b, n)
        ch = ('→' if cb == ca + 1 else '←' if cb == ca - 1
              else '↓' if rb == ra + 1 else '↑')
        g[ra][ca] = f'{i+1:2d}{ch}'
    r, c = divmod(seq[-1], n)
    g[r][c] = f'{len(seq):2d}·'
    return '\n'.join(' '.join(row) for row in g)


def svg_draw(n, seq):
    N = n * n
    s = 72
    pad = 46
    W = n * s + 2 * pad
    H = n * s + 2 * pad

    def pos(v):
        r, c = divmod(v, n)
        return (pad + c * s + s / 2, pad + r * s + s / 2)

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" font-family="Arial">')
    parts.append(
        f'<defs>'
        f'<marker id="arrB" viewBox="0 0 10 10" refX="8" refY="5" '
        f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{BLUE}"/></marker>'
        f'<marker id="arrR" viewBox="0 0 10 10" refX="8" refY="5" '
        f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{RED}"/></marker>'
        f'</defs>')
    # faint grid
    for r in range(n + 1):
        y = pad + r * s
        parts.append(f'<line x1="{pad}" y1="{y}" x2="{pad + n * s}" y2="{y}" '
                     f'stroke="#e5e7eb" stroke-width="1"/>')
    for c in range(n + 1):
        x = pad + c * s
        parts.append(f'<line x1="{x}" y1="{pad}" x2="{x}" y2="{pad + n * s}" '
                     f'stroke="#e5e7eb" stroke-width="1"/>')
    # edges with arrows (shortened at the target)
    for a, b in zip(seq, seq[1:]):
        x1, y1 = pos(a)
        x2, y2 = pos(b)
        dx, dy = x2 - x1, y2 - y1
        import math
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        x2s, y2s = x2 - 14 * ux, y2 - 14 * uy
        color = BLUE if a // n == b // n else RED
        marker = "arrB" if color == BLUE else "arrR"
        parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2s:.1f}" '
                     f'y2="{y2s:.1f}" stroke="{color}" stroke-width="4" '
                     f'marker-end="url(#{marker})"/>')
    # vertices + step numbers
    for step, v in enumerate(seq, 1):
        x, y = pos(v)
        fill = "#16a34a" if step == 1 else "#f97316" if step == N else "#ffffff"
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="{fill}" '
                     f'stroke="#111827" stroke-width="2"/>')
        parts.append(f'<text x="{x:.1f}" y="{y + 4:.1f}" font-size="10" '
                     f'text-anchor="middle" fill="#111827">{step}</text>')
    parts.append('</svg>')
    return '\n'.join(parts)


def collect_peaks(n, paths, adj):
    max_h = n * (n - 1)
    peaks = []
    for p in paths:
        h = h_count(n, p)
        if h == max_h:
            continue
        mvs = backbite_moves(n, p, adj)
        if mvs and all(h_count(n, m) < h for m in mvs):
            peaks.append((h, p))
    return peaks


def select_diverse(peaks, max_peaks):
    """One representative per (h, vertical-cols) class, capped per h."""
    classes = defaultdict(list)
    for h, p in peaks:
        n = int(len(p) ** 0.5)
        classes[(h, vertical_cols(n, p))].append(p)
    # sort classes by h, take up to 2 per h, then fill remaining by h variety
    picked = []
    for h in sorted({k[0] for k in classes}):
        hs = [k for k in classes if k[0] == h]
        for k in hs[:2]:
            picked.append((k[0], classes[k][0]))
            if len(picked) >= max_peaks:
                return picked
    # if still room, add more diverse ones
    if len(picked) < max_peaks:
        for k in sorted(classes):
            for p in classes[k][1:]:
                picked.append((k[0], p))
                if len(picked) >= max_peaks:
                    return picked
    return picked


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--max-peaks", type=int, default=30)
    ap.add_argument("--sample", type=int, default=0)
    args = ap.parse_args()
    n = args.n
    adj = build_adjacency(n)
    outdir = Path("results/peak_viz")
    outdir.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    if args.sample == 0:
        paths = list(enumerate_hamiltonian_paths(n))
    else:
        rng = random.Random(42)
        seen = set()
        seq = serpentine_path(n)
        while len(seen) < args.sample:
            for _ in range(20):
                seq = random_backbite_step(n, seq, rng, adj)
            seen.add(seq)
        while len(seen) < args.sample:
            seen.add(random_backtracking_path(n, seed=random.randrange(10**6)))
        paths = list(seen)
    print(f"[{len(paths)} paths collected in {time.time()-t0:.1f}s]")

    t0 = time.time()
    peaks = collect_peaks(n, paths, adj)
    print(f"[{len(peaks)} strict peaks found in {time.time()-t0:.1f}s]")

    picked = select_diverse(peaks, args.max_peaks)
    print(f"[visualizing {len(picked)} peaks]")

    # markdown text drawings
    md = [f"# Strict peaks of the h-landscape, n = {n}",
          "",
          "Each grid shows step numbers and arrows (→←↓↑). Blue = horizontal, "
          "red = vertical in the SVG version.",
          ""]
    html = [f"<html><head><meta charset='utf-8'><title>Strict peaks n={n}</title>",
            "<style>",
            "body{font-family:Arial;margin:20px;background:#f9fafb}",
            "h1{color:#111827}",
            ".grid{display:flex;flex-wrap:wrap;gap:24px}",
            ".card{background:#fff;border:1px solid #e5e7eb;border-radius:8px;",
            "padding:12px;box-shadow:0 1px 3px rgba(0,0,0,.1)}",
            ".cap{font-size:13px;color:#374151;margin-bottom:6px}",
            "</style></head><body>",
            f"<h1>Strict peaks of the h-landscape, n = {n}</h1>",
            "<p>Blue arrows = horizontal edges, red arrows = vertical edges. "
            "Green = start, orange = end. Numbers = step order.</p>",
            "<div class='grid'>"]

    for idx, (h, p) in enumerate(picked):
        md.append(f"\n## peak {idx}: h = {h} (max {n*(n-1)}), "
                  f"vertical cols = {vertical_cols(n, p)}")
        md.append("```")
        md.append(text_draw(n, p))
        md.append("```")
        html.append("<div class='card'>")
        html.append(f"<div class='cap'>h = {h} / {n*(n-1)}, "
                    f"verticals = {list(vertical_cols(n, p))}</div>")
        html.append(svg_draw(n, p))
        html.append("</div>")

    html.append("</div></body></html>")

    md_path = outdir / f"peaks_n{n}.md"
    html_path = outdir / f"peaks_n{n}.html"
    md_path.write_text("\n".join(md))
    html_path.write_text("\n".join(html))
    print(f"wrote {md_path}")
    print(f"wrote {html_path}")


if __name__ == "__main__":
    main()
