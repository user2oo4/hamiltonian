#!/usr/bin/env python3
"""Analyse the horizontal-edge landscape h(path) = #horizontal edges.

For each n:
  * distribution of h
  * local maxima / strict peaks (every move decreases h)
  * classification of strict peaks by vertical-column pattern
  * detour properties: can a downhill neighbour move back up?  Is there an
    escape hatch to a different h-state?  How many moves to reach h+1?

Usage:
    python3 scripts/horizontal_analysis.py --n 4
    python3 scripts/horizontal_analysis.py --n 6            # exhaustive, ~minutes
    python3 scripts/horizontal_analysis.py --n 7 --sample 30000   # sampled
"""

import argparse
import random
import sys
import time
from collections import Counter, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hampath import (
    backbite_moves,
    build_adjacency,
    enumerate_hamiltonian_paths,
    random_backtracking_path,
    serpentine_path,
)
from hampath.backbite import random_backbite_step


def h_count(n, seq):
    return sum(1 for a, b in zip(seq, seq[1:]) if a // n == b // n)


def vertical_cols(n, seq):
    return [a % n for a, b in zip(seq, seq[1:]) if a // n != b // n]


def draw(n, seq):
    g = [['  '] * n for _ in range(n)]
    for i, (a, b) in enumerate(zip(seq, seq[1:])):
        ra, ca = divmod(a, n)
        rb, cb = divmod(b, n)
        ch = '→' if rb == ra and cb == ca + 1 else '←' if rb == ra else '↓' if rb == ra + 1 else '↑'
        g[ra][ca] = f'{i+1:2d}{ch}'
    r, c = divmod(seq[-1], n)
    g[r][c] = f'{len(seq):2d}·'
    return '\n'.join(' '.join(row) for row in g)


def detour_length(n, start, hp, adj, max_depth=12):
    """Shortest number of moves from start to any state with strictly larger h."""
    h0 = hp[start]
    if h0 is None:
        return None
    seen = {start}
    q = deque([(start, 0)])
    while q:
        cur, d = q.popleft()
        if d >= max_depth:
            continue
        for m in backbite_moves(n, cur, adj):
            if m in seen:
                continue
            hm = hp.get(m)
            if hm is None:
                hm = h_count(n, m)
            if hm > h0:
                return d + 1
            seen.add(m)
            q.append((m, d + 1))
    return None  # not found within max_depth


def analyze_paths(n, paths, adj, full_detour=False):
    N = n * n
    max_h = n * (n - 1)
    hp = {p: h_count(n, p) for p in paths}
    local_max = []
    strict_peaks = []
    moves_cache = {}
    for p in paths:
        h = hp[p]
        if h == max_h:
            continue
        mvs = backbite_moves(n, p, adj)
        moves_cache[p] = mvs
        hs = [h_count(n, m) for m in mvs]
        if not any(x > h for x in hs):
            local_max.append(p)
            if mvs and all(x < h for x in hs):
                strict_peaks.append(p)

    # classify strict peaks by (h, vertical column pattern)
    classes = Counter()
    for p in strict_peaks:
        classes[(hp[p], tuple(vertical_cols(n, p)))] += 1

    # detour properties of strict peaks
    escape_hatch = 0
    two_cycle = 0
    detour_lens = []
    for p in strict_peaks:
        h = hp[p]
        has_hatch = False
        for m in moves_cache[p]:
            hm = h_count(n, m)
            if hm != h - 1:
                continue
            for x in backbite_moves(n, m, adj):
                hx = h_count(n, x)
                if hx > h or (hx == h and x != p):
                    has_hatch = True
                    break
            if has_hatch:
                break
        if has_hatch:
            escape_hatch += 1
        else:
            two_cycle += 1
        dl = detour_length(n, p, hp, adj)
        if dl is not None:
            detour_lens.append(dl)

    return {
        "n": n,
        "n_paths": len(paths),
        "max_h": max_h,
        "h_dist": dict(sorted(Counter(hp.values()).items())),
        "local_max": len(local_max),
        "strict_peaks": len(strict_peaks),
        "peak_classes": classes,
        "escape_hatch": escape_hatch,
        "two_cycle": two_cycle,
        "detour_len_dist": dict(sorted(Counter(detour_lens).items())),
        "peaks_by_h": dict(sorted(Counter(hp[p] for p in strict_peaks).items())),
    }


def print_stats(stats, show_classes=8):
    s = stats
    print(f"=== n={s['n']} : {s['n_paths']} paths, max_h={s['max_h']} ===")
    print("h distribution:", s["h_dist"])
    print(f"local maxima: {s['local_max']}   strict peaks: {s['strict_peaks']}")
    print("strict peaks by h:", s["peaks_by_h"])
    print(f"escape hatch: {s['escape_hatch']}   two-cycle (no hatch): {s['two_cycle']}")
    print("detour length (to h+1) distribution:", s["detour_len_dist"])
    print("peak classes (h, vertical-cols): count")
    for k, v in sorted(s["peak_classes"].items(), key=lambda kv: -kv[1])[:show_classes]:
        print(f"   {k}: {v}")
    if len(s["peak_classes"]) > show_classes:
        print(f"   ... {len(s['peak_classes'])} classes total")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--sample", type=int, default=0,
                    help="if >0, sample this many distinct paths instead of exhaustive")
    ap.add_argument("--show-classes", type=int, default=8)
    args = ap.parse_args()
    n = args.n
    adj = build_adjacency(n)

    t0 = time.time()
    if args.sample == 0:
        paths = list(enumerate_hamiltonian_paths(n))
        print(f"[enumerated {len(paths)} paths in {time.time()-t0:.1f}s]")
        stats = analyze_paths(n, paths, adj)
    else:
        # sampled: backbite chain + random backtracking
        rng = random.Random(42)
        seen = set()
        seq = serpentine_path(n)
        while len(seen) < args.sample:
            for _ in range(20):
                seq = random_backbite_step(n, seq, rng, adj)
            seen.add(seq)
            if len(seen) % 5000 == 0:
                print(f"  sampled {len(seen)}", flush=True)
        # top up with backtracking samples
        while len(seen) < args.sample:
            seen.add(random_backtracking_path(n, seed=random.randrange(10**6)))
        print(f"[sampled {len(seen)} distinct paths in {time.time()-t0:.1f}s]")
        stats = analyze_paths(n, list(seen), adj)

    print_stats(stats, show_classes=args.show_classes)


if __name__ == "__main__":
    main()
