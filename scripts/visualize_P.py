#!/usr/bin/env python3
"""Visualize P-paths (plateau local maxima) of the h-landscape.

A P path has no Δh = +1 move but at least one Δh = 0 move.  We collect them,
classify by endpoint-type pair and h, and draw a diverse subset:

  * results/p_viz/p_paths_n{n}.html   -- browsable SVG gallery
  * results/p_viz/p_paths_n{n}.md     -- text arrow-grid drawings

Usage:
    python3 scripts/visualize_P.py --n 5
    python3 scripts/visualize_P.py --n 6 --max-peaks 40
"""

import argparse
import random
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hampath import backbite_moves, build_adjacency, enumerate_hamiltonian_paths
from hampath.backbite import random_backbite_step
from hampath import serpentine_path, random_backtracking_path
from visualize_peaks import h_count, text_draw, svg_draw


def etype2(n, v):
    r, c = divmod(v, n)
    if r in (0, n - 1) and c in (0, n - 1):
        return 'corner'
    if r in (0, n - 1):
        return 'TB-edge'
    if c in (0, n - 1):
        return 'LR-edge'
    return 'interior'


def collect_P(n, paths, adj):
    out = []
    for p in paths:
        h = h_count(n, p)
        hs = [h_count(n, m) for m in backbite_moves(n, p, adj)]
        if not any(x > h for x in hs) and any(x == h for x in hs):
            out.append((h, p))
    return out


def select_diverse(items, max_pick):
    classes = defaultdict(list)
    for h, p in items:
        n = int(len(p) ** 0.5)
        key = (h, etype2(n, p[0]), etype2(n, p[-1]))
        classes[key].append(p)
    picked = []
    for h in sorted({k[0] for k in classes}):
        for k in [kk for kk in classes if kk[0] == h][:3]:
            picked.append((k[0], classes[k][0]))
            if len(picked) >= max_pick:
                return picked
    for k in sorted(classes):
        for p in classes[k][1:]:
            picked.append((k[0], p))
            if len(picked) >= max_pick:
                return picked
    return picked


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--max-peaks", type=int, default=36)
    ap.add_argument("--sample", type=int, default=0)
    args = ap.parse_args()
    n = args.n
    adj = build_adjacency(n)
    outdir = Path("results/p_viz")
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
    print(f"[{len(paths)} paths collected in {time.time()-t0:.1f}s]", flush=True)

    t0 = time.time()
    P = collect_P(n, paths, adj)
    print(f"[{len(P)} P-paths found in {time.time()-t0:.1f}s]", flush=True)

    # endpoint-type distribution of P
    dist = defaultdict(int)
    for h, p in P:
        dist[(etype2(n, p[0]), etype2(n, p[-1]))] += 1
    print("P endpoint-type distribution:")
    for k, v in sorted(dist.items(), key=lambda kv: -kv[1]):
        print(f"   {str(k):>28}: {v}")

    picked = select_diverse(P, args.max_peaks)
    print(f"[visualizing {len(picked)} P-paths]", flush=True)

    md = [f"# P-paths (plateau local maxima) of the h-landscape, n = {n}",
          "",
          "Each grid shows step numbers and arrows. Blue = horizontal, "
          "red = vertical in the SVG version.",
          ""]
    html = [f"<html><head><meta charset='utf-8'><title>P-paths n={n}</title>",
            "<style>",
            "body{font-family:Arial;margin:20px;background:#f9fafb}",
            "h1{color:#111827}",
            ".grid{display:flex;flex-wrap:wrap;gap:24px}",
            ".card{background:#fff;border:1px solid #e5e7eb;border-radius:8px;",
            "padding:12px;box-shadow:0 1px 3px rgba(0,0,0,.1)}",
            ".cap{font-size:13px;color:#374151;margin-bottom:6px}",
            "</style></head><body>",
            f"<h1>P-paths (plateau local maxima), n = {n}</h1>",
            "<p>Blue = horizontal, red = vertical. Green = start, orange = end.</p>",
            "<div class='grid'>"]

    for idx, (h, p) in enumerate(picked):
        et = (etype2(n, p[0]), etype2(n, p[-1]))
        md.append(f"\n## P-path {idx}: h = {h} (max {n*(n-1)}), endpoints = {et}")
        md.append("```")
        md.append(text_draw(n, p))
        md.append("```")
        html.append("<div class='card'>")
        html.append(f"<div class='cap'>h = {h} / {n*(n-1)}, endpoints = {et}</div>")
        html.append(svg_draw(n, p))
        html.append("</div>")

    html.append("</div></body></html>")

    md_path = outdir / f"p_paths_n{n}.md"
    html_path = outdir / f"p_paths_n{n}.html"
    md_path.write_text("\n".join(md))
    html_path.write_text("\n".join(html))
    print(f"wrote {md_path}")
    print(f"wrote {html_path}")


if __name__ == "__main__":
    main()
