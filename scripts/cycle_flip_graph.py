#!/usr/bin/env python3
"""Cycle-land analysis: the 2-opt flip graph of Hamiltonian cycles.

For an even n, enumerate all Hamiltonian cycles of the n x n grid and build
the graph whose vertices are cycles and whose edges are valid 2-opt moves
(the moves that stay inside cycle-land).  Reports components and degrees.

Usage:
    python scripts/cycle_flip_graph.py --n 4
    python scripts/cycle_flip_graph.py --n 6
"""

import argparse
import sys
import time
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hampath import build_adjacency
from hampath.enumerate import _unvisited_connected


def canonical_cycle(seq) -> tuple:
    """Canonical key of an undirected cycle: rotate to start at 0, then take
    the lexicographically smaller of the two orientations."""
    n = len(seq)
    idx = seq.index(0)
    rot = tuple(seq[idx:] + seq[:idx])
    rev = (rot[0],) + tuple(reversed(rot[1:]))
    return min(rot, rev)


def enumerate_hamiltonian_cycles(n: int, verbose: bool = False) -> set:
    """Enumerate all Hamiltonian cycles of the n x n grid (even n only).

    Returns a set of canonical cycle tuples.  Fixes vertex 0 as the start of
    the DFS, so each undirected cycle is found exactly once.
    """
    adj = build_adjacency(n)
    N = n * n
    full = (1 << N) - 1
    cycles = set()
    path = [0] * N
    path[0] = 0

    def dfs(v: int, mask: int, depth: int) -> None:
        if depth == N:
            if 0 in adj[v]:          # can close back to the start
                cycles.add(canonical_cycle(path))
            return

        rem = full ^ mask
        if rem and not _unvisited_connected(adj, rem):
            return

        for u in adj[v]:
            bit = 1 << u
            if not (mask & bit):
                path[depth] = u
                dfs(u, mask | bit, depth + 1)

    dfs(0, 1, 1)
    if verbose:
        print(f"[cycles] n={n}: {len(cycles)} Hamiltonian cycles")
    return cycles


def cycle_edges(seq) -> set:
    n = len(seq)
    return {tuple(sorted((seq[i], seq[(i + 1) % n]))) for i in range(n)}


def two_opt_neighbors(seq, adj, eset) -> set:
    """All cycles reachable from ``seq`` by one valid (single-cycle) 2-opt."""
    n = len(seq)
    out = set()
    for i in range(n):
        a = seq[i]
        b = seq[(i + 1) % n]
        for j in range(i + 1, n):
            c = seq[j]
            d = seq[(j + 1) % n]
            if len({a, b, c, d}) < 4:
                continue  # removed edges share a vertex -> not a 2-opt

            for e1, e2 in [((a, c), (b, d)), ((a, d), (b, c))]:
                s1 = tuple(sorted(e1))
                s2 = tuple(sorted(e2))
                if s1 == s2 or s1 in eset or s2 in eset:
                    continue  # duplicate or already-used edge
                if e2[1] not in adj[e2[0]] or e1[1] not in adj[e1[0]]:
                    continue  # cross edges must be grid edges

                # build candidate edge set
                new_edges = []
                ok = True
                for k in range(n):
                    if k == i or k == j:
                        continue
                    x = seq[k]
                    y = seq[(k + 1) % n]
                    new_edges.append((x, y))
                new_edges.append(e1)
                new_edges.append(e2)

                # must be a single Hamiltonian cycle (all degrees 2, connected)
                if _is_single_cycle(new_edges, n):
                    out.add(canonical_cycle(_seq_from_edges(new_edges, n)))
    return out


def _is_single_cycle(edge_list, N) -> bool:
    deg = [0] * N
    g = {v: [] for v in range(N)}
    for a, b in edge_list:
        deg[a] += 1
        deg[b] += 1
        g[a].append(b)
        g[b].append(a)
    if any(d != 2 for d in deg):
        return False
    # connected?
    seen = {0}
    stack = [0]
    while stack:
        v = stack.pop()
        for u in g[v]:
            if u not in seen:
                seen.add(u)
                stack.append(u)
    return len(seen) == N


def _seq_from_edges(edge_list, N) -> tuple:
    g = {v: [] for v in range(N)}
    for a, b in edge_list:
        g[a].append(b)
        g[b].append(a)
    seq = [0]
    prev = -1
    cur = 0
    while len(seq) < N:
        nxts = [u for u in g[cur] if u != prev]
        if not nxts:
            break
        nxt = nxts[0]
        seq.append(nxt)
        prev, cur = cur, nxt
    return tuple(seq)


def analyze(n: int, cycles) -> dict:
    adj = build_adjacency(n)
    key_to_idx = {c: i for i, c in enumerate(cycles)}
    visited = set()
    components = []
    degrees = {}

    for start in cycles:
        if start in visited:
            continue
        queue = deque([start])
        visited.add(start)
        size = 0
        while queue:
            cur = queue.popleft()
            size += 1
            eset = cycle_edges(cur)
            nbrs = two_opt_neighbors(cur, adj, eset)
            degrees[cur] = len(nbrs)
            for nb in nbrs:
                if nb in key_to_idx and nb not in visited:
                    visited.add(nb)
                    queue.append(nb)
        components.append(size)

    deg_values = list(degrees.values()) if degrees else [0]
    isolated = [c for c, d in degrees.items() if d == 0]
    return {
        "n_cycles": len(cycles),
        "n_components": len(components),
        "component_sizes": sorted(components, reverse=True),
        "degrees": degrees,
        "min_degree": min(deg_values),
        "max_degree": max(deg_values),
        "avg_degree": sum(deg_values) / len(deg_values),
        "isolated_cycles": isolated,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--show-isolated", action="store_true",
                    help="print the isolated cycles")
    args = ap.parse_args()
    n = args.n
    if n % 2 == 1:
        print(f"n={n} is odd: no Hamiltonian cycles exist (bipartite imbalance)")
        return

    t0 = time.time()
    cycles = enumerate_hamiltonian_cycles(n, verbose=True)
    t_enum = time.time() - t0
    print(f"enumerated in {t_enum:.3f}s")

    t0 = time.time()
    stats = analyze(n, cycles)
    t_an = time.time() - t0
    print(f"flip graph built in {t_an:.3f}s")
    print(f"n_cycles          : {stats['n_cycles']}")
    print(f"n_components      : {stats['n_components']}")
    print(f"component_sizes   : {stats['component_sizes']}")
    print(f"degree min/avg/max: {stats['min_degree']} / "
          f"{stats['avg_degree']:.2f} / {stats['max_degree']}")
    print(f"isolated cycles   : {len(stats['isolated_cycles'])}")
    if args.show_isolated and stats["isolated_cycles"]:
        for c in stats["isolated_cycles"]:
            print("  ", c)


if __name__ == "__main__":
    main()
