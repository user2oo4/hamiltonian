#!/usr/bin/env python3
"""Visualize the trap cycles of P paths (plateau cycles under the chase).

A trap is a plateau cycle reached by the no-reversal chase from a P path.
We collect DISTINCT cycles, grouped by length (2/4/6), and draw every state
of each cycle:

  * results/trap_viz/traps_n{n}.html  -- SVG gallery
  * results/trap_viz/traps_n{n}.md    -- text arrow-grid drawings

Usage:
    python3 scripts/visualize_traps.py --n 6 --max-cycles 6
"""

import argparse
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hampath import backbite_moves, build_adjacency, enumerate_hamiltonian_paths
from visualize_peaks import h_count, text_draw, svg_draw


def etype2(n, v):
    r, c = divmod(v, n)
    if r in (0, n - 1) and c in (0, n - 1):
        return 'corner'
    if r in (0, n - 1):
        return 'TB'
    if c in (0, n - 1):
        return 'LR'
    return 'int'


def find_trap_cycles(n, paths, adj):
    """Distinct plateau cycles found by the no-reversal chase."""
    cycles = defaultdict(list)   # length -> list of cycle-state-lists
    seen_cycles = set()
    for p in paths:
        h = h_count(n, p)
        hs = [h_count(n, m) for m in backbite_moves(n, p, adj)]
        if any(x > h for x in hs) or not any(x == h for x in hs):
            continue
        cur = p
        prev = None
        pos = {cur: 0}
        steps = 0
        while True:
            h = h_count(n, cur)
            mvs = backbite_moves(n, cur, adj)
            if any(h_count(n, m) > h for m in mvs):
                break  # non-trap
            plates = [m for m in mvs if h_count(n, m) == h]
            nxt = None
            for m in plates:
                if m != prev:
                    nxt = m
                    break
            if nxt is None:
                nxt = plates[0] if plates else None
            if nxt is None:
                break
            if nxt in pos:
                cyc = _trace_cycle(nxt, adj)
                # a TRUE trap: no state of the cycle has a +1 move
                # (otherwise the chase would have escaped there)
                ok = True
                for s in cyc:
                    hs = h_count(n, s)
                    if any(h_count(n, m) > hs for m in backbite_moves(n, s, adj)):
                        ok = False
                        break
                if not ok:
                    break
                key = frozenset(cyc)
                if key not in seen_cycles:
                    seen_cycles.add(key)
                    cycles[len(cyc)].append(cyc)
                break
            prev, cur = cur, nxt
            steps += 1
            pos[cur] = steps
            if steps > 200:
                break
    return cycles


def _trace_cycle(start, adj):
    """Follow the no-reversal chase from start until the first repeat."""
    cur = start
    prev = None
    cyc = [cur]
    while True:
        h = h_count(int(len(cur) ** 0.5), cur)
        mvs = backbite_moves(int(len(cur) ** 0.5), cur, adj)
        plates = [m for m in mvs if h_count(int(len(m) ** 0.5), m) == h]
        nxt = None
        for m in plates:
            if m != prev:
                nxt = m
                break
        if nxt is None:
            nxt = plates[0] if plates else None
        if nxt is None:
            break
        if nxt in cyc:
            # cut the prefix before the cycle entry
            i = cyc.index(nxt)
            return cyc[i:]
        prev, cur = cur, nxt
        cyc.append(cur)
        if len(cyc) > 200:
            break
    return cyc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--max-cycles", type=int, default=5)
    args = ap.parse_args()
    n = args.n
    adj = build_adjacency(n)
    outdir = Path("results/trap_viz")
    outdir.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    paths = list(enumerate_hamiltonian_paths(n))
    print(f"[{len(paths)} paths collected in {time.time()-t0:.1f}s]", flush=True)

    t0 = time.time()
    cycles = find_trap_cycles(n, paths, adj)
    print(f"[distinct trap cycles found in {time.time()-t0:.1f}s]", flush=True)
    for L in sorted(cycles):
        print(f"  length {L}: {len(cycles[L])} distinct cycles", flush=True)

    md = [f"# Trap cycles (plateau cycles) of the chase, n = {n}", "",
          "Each cycle is a set of states connected by plateau moves that the",
          "no-reversal chase loops through forever.  Blue = horizontal, red = vertical.",
          ""]
    html = [f"<html><head><meta charset='utf-8'><title>Trap cycles n={n}</title>",
            "<style>",
            "body{font-family:Arial;margin:20px;background:#f9fafb}",
            ".grid{display:flex;flex-wrap:wrap;gap:24px}",
            ".card{background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:12px}",
            ".cap{font-size:13px;color:#374151;margin-bottom:6px}",
            "</style></head><body>",
            f"<h1>Trap cycles of the chase, n = {n}</h1>",
            "<p>States of each plateau cycle. Green = start, orange = end.</p>",
            "<div class='grid'>"]

    for L in sorted(cycles):
        md.append(f"\n## Cycles of length {L} (showing up to {args.max_cycles})")
        for ci, cyc in enumerate(cycles[L][:args.max_cycles]):
            md.append(f"\n### length-{L} cycle #{ci}, h = {h_count(n, cyc[0])}")
            html.append(f"<div class='card'><div class='cap'>length-{L} cycle #{ci}, "
                        f"h = {h_count(n, cyc[0])}</div>")
            for si, s in enumerate(cyc):
                et = (etype2(n, s[0]), etype2(n, s[-1]))
                cl = 'closable' if s[-1] in adj[s[0]] else 'open'
                md.append(f"state {si}: endpoints={et}, {cl}")
                md.append("```")
                md.append(text_draw(n, s))
                md.append("```")
                html.append(f"<div style='margin:6px 0'>state {si}: {et}, {cl}</div>")
                html.append(svg_draw(n, s))
            html.append("</div>")

    html.append("</div></body></html>")
    md_path = outdir / f"traps_n{n}.md"
    html_path = outdir / f"traps_n{n}.html"
    md_path.write_text("\n".join(md))
    html_path.write_text("\n".join(html))
    print(f"wrote {md_path}")
    print(f"wrote {html_path}")


if __name__ == "__main__":
    main()
