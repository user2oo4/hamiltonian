#!/usr/bin/env python3
"""Work within the locked-endpoint set L.

L = { Hamiltonian paths whose both endpoints are corners or left/right-edge
      cells, with horizontal first and last edges }.

The point of this script: once Lemmas A/B are proven, connectivity reduces to
studying L, which is far smaller than the full path set.  We enumerate L
directly (constrained DFS, no need for all paths), cache it, and verify:

  * Lemma B: every L-path (except the 2 max-h paths) is a strict peak
    (all backbite moves decrease h).
  * Detour properties of the peaks: can a downhill neighbour move back up?
  * Detour length to h+1 (bounded BFS) for a sample of peaks.

Usage:
    python3 scripts/locked_analysis.py --n 6
    python3 scripts/locked_analysis.py --n 7 --sample-detours 1000
"""

import argparse
import pickle
import random
import sys
import time
from collections import Counter, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hampath import build_adjacency, canonical
from hampath.enumerate import _unvisited_connected
from hampath import backbite_moves

CACHE_DIR = Path("results/locked_cache")


def h_count(n, seq):
    return sum(1 for a, b in zip(seq, seq[1:]) if a // n == b // n)


def enumerate_locked(n, verbose=True):
    adj = build_adjacency(n)
    N = n * n
    full = (1 << N) - 1
    results = set()
    path = [0] * N

    def eligible(v):
        r, c = divmod(v, n)
        return (r in (0, n - 1) and c in (0, n - 1)) or (c in (0, n - 1))

    starts = [v for v in range(N) if eligible(v)]
    cache = {}

    def connected(rem):
        ok = cache.get(rem)
        if ok is None:
            ok = _unvisited_connected(adj, rem)
            cache[rem] = ok
        return ok

    def dfs(v, mask, depth):
        if depth == N:
            tail = path[-1]
            if not eligible(tail):
                return
            if path[-2] // n != tail // n:
                return
            results.add(canonical(path))
            return
        rem = full ^ mask
        if rem and not connected(rem):
            return
        for u in adj[v]:
            bit = 1 << u
            if not (mask & bit):
                if depth == 1 and u // n != v // n:
                    continue
                path[depth] = u
                dfs(u, mask | bit, depth + 1)

    t0 = time.time()
    for si, s in enumerate(starts):
        path[0] = s
        dfs(s, 1 << s, 1)
        if verbose:
            print(f"  start {si+1}/{len(starts)} done, |L|={len(results)}, "
                  f"t={time.time()-t0:.1f}s", flush=True)
    return results


def load_or_enumerate(n):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = CACHE_DIR / f"locked_n{n}.pkl"
    if path.exists():
        print(f"[loading cached L from {path}]", flush=True)
        with open(path, "rb") as f:
            return pickle.load(f)
    print(f"[enumerating L for n={n}]", flush=True)
    L = enumerate_locked(n)
    with open(path, "wb") as f:
        pickle.dump(L, f)
    print(f"[cached {len(L)} paths to {path}]", flush=True)
    return L


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--sample-detours", type=int, default=200,
                    help="number of peaks for which to compute detour length")
    ap.add_argument("--max-depth", type=int, default=16)
    args = ap.parse_args()
    n = args.n
    adj = build_adjacency(n)
    max_h = n * (n - 1)

    t0 = time.time()
    L = load_or_enumerate(n)
    print(f"|L| = {len(L)}  ({time.time()-t0:.1f}s)", flush=True)

    # separate max-h paths
    max_paths = [p for p in L if h_count(n, p) == max_h]
    peaks = [p for p in L if h_count(n, p) < max_h]
    print(f"max-h paths in L: {len(max_paths)} (should be 2: serpentine + mirror)")
    print(f"candidate peaks (L minus max-h): {len(peaks)}", flush=True)

    # Lemma B: every candidate peak must be a strict peak
    t0 = time.time()
    not_strict = 0
    down_return_ok = 0
    down_return_bad = 0
    escape_hatch = 0
    for p in peaks:
        h = h_count(n, p)
        mvs = backbite_moves(n, p, adj)
        hs = [h_count(n, m) for m in mvs]
        if not mvs or not all(x < h for x in hs):
            not_strict += 1
            if not_strict <= 5:
                print("  NOT strict:", p, "h=", h, "move hs=", hs)
            continue
        # down-then-up check
        ok_all = True
        for m in mvs:
            hm = h_count(n, m)
            if hm != h - 1:
                continue
            up = [h_count(n, x) for x in backbite_moves(n, m, adj)]
            if not any(x >= h for x in up):
                ok_all = False
                break
        if ok_all:
            down_return_ok += 1
        else:
            down_return_bad += 1
    print(f"Lemma B check: non-strict candidates = {not_strict} / {len(peaks)}", flush=True)
    print(f"down-then-up holds for {down_return_ok} peaks, fails for {down_return_bad}",
          flush=True)

    # detour length for a sample
    rng = random.Random(0)
    sample = rng.sample(peaks, min(args.sample_detours, len(peaks)))
    lens = []
    for p in sample:
        h0 = h_count(n, p)
        seen = {p}
        q = deque([(p, 0)])
        found = None
        while q:
            cur, d = q.popleft()
            if d >= args.max_depth:
                continue
            for m in backbite_moves(n, cur, adj):
                if m in seen:
                    continue
                hm = h_count(n, m)
                if hm > h0:
                    found = d + 1
                    q.clear()
                    break
                seen.add(m)
                q.append((m, d + 1))
        lens.append(found)
    found = [x for x in lens if x is not None]
    print(f"detour lengths (sample {len(sample)} peaks, depth<={args.max_depth}): "
          f"found {len(found)}/{len(sample)}, dist={dict(sorted(Counter(found).items()))}",
          flush=True)


if __name__ == "__main__":
    main()
