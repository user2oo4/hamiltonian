#!/usr/bin/env python3
"""Analyse Hamiltonian paths and the backbite move graph for small grids.

Usage:
    python scripts/analyze.py --min-n 2 --max-n 4 [--no-connectivity] [--no-dp]

For each n in [min_n, max_n]:
  1. enumerate all undirected Hamiltonian paths
  2. cross-check the count with subset DP (n <= 4)
  3. compute connected components of the backbite move graph
"""

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hampath import (
    count_hamiltonian_paths_dp,
    enumerate_hamiltonian_paths,
    move_graph_stats,
)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-n", type=int, default=2)
    ap.add_argument("--max-n", type=int, default=4)
    ap.add_argument("--no-connectivity", action="store_true",
                    help="skip move-graph component analysis")
    ap.add_argument("--no-dp", action="store_true", help="skip DP cross-check")
    args = ap.parse_args()

    for n in range(args.min_n, args.max_n + 1):
        print(f"=== n = {n}  ({n}x{n} grid, N = {n*n} vertices) ===")

        t0 = time.time()
        paths = enumerate_hamiltonian_paths(n, verbose=True)
        t_enum = time.time() - t0
        print(f"enumerated {len(paths)} undirected Hamiltonian paths in {t_enum:.3f}s")

        if not args.no_dp and n <= 4:
            t0 = time.time()
            directed, undirected = count_hamiltonian_paths_dp(n)
            t_dp = time.time() - t0
            match = "OK" if undirected == len(paths) else "MISMATCH"
            print(f"DP cross-check: directed={directed}, undirected={undirected} "
                  f"({t_dp:.3f}s) -> {match}")

        if not args.no_connectivity:
            t0 = time.time()
            stats = move_graph_stats(n, paths)
            t_conn = time.time() - t0
            comps = stats["component_sizes"]
            print(f"move graph: {stats['n_components']} component(s), "
                  f"sizes = {comps}")
            print(f"degrees: min={stats['min_degree']}, max={stats['max_degree']}, "
                  f"avg={stats['avg_degree']:.2f}  ({t_conn:.3f}s)")
        print()


if __name__ == "__main__":
    main()
