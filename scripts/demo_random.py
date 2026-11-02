#!/usr/bin/env python3
"""Demo: random generation and heuristic reachability on bigger grids.

Usage:
    python scripts/demo_random.py --n 6 --samples 200 --search-steps 100000
"""

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hampath import (
    edge_distance,
    format_path,
    is_hamiltonian_path,
    random_backbite_path,
    random_backtracking_path,
    sample_paths,
    search_connection,
    serpentine_path,
)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=6, help="grid size")
    ap.add_argument("--samples", type=int, default=200,
                    help="number of backbite-chain samples")
    ap.add_argument("--search-steps", type=int, default=100_000,
                    help="simulated-annealing budget for search_connection")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    n = args.n

    print(f"--- {n}x{n} grid ---")

    # 1. fast biased generator
    t0 = time.time()
    a = random_backtracking_path(n, seed=args.seed)
    print(f"random_backtracking_path: valid={is_hamiltonian_path(n, a)} "
          f"({time.time()-t0:.3f}s)")

    # 2. approximately uniform backbite sampler
    t0 = time.time()
    b = random_backbite_path(n, seed=args.seed)
    print(f"random_backbite_path:     valid={is_hamiltonian_path(n, b)} "
          f"({time.time()-t0:.3f}s)")

    # 3. distinct states visited by the backbite chain
    t0 = time.time()
    seen = sample_paths(n, num_samples=args.samples, steps_between=50,
                        seed=args.seed)
    print(f"backbite chain visited {len(seen)} distinct paths in "
          f"{args.samples} samples (gap 50) ({time.time()-t0:.3f}s)")

    # 4. heuristic: can we transform the serpentine path into a random
    #    backtracking path using only backbite moves?
    start = serpentine_path(n)
    target = random_backtracking_path(n, seed=args.seed + 1)
    d0 = edge_distance(start, target)
    print(f"search_connection: start=serpentine, target=random (distance {d0})")
    t0 = time.time()
    ok, best, used = search_connection(n, start, target,
                                       steps=args.search_steps,
                                       seed=args.seed)
    d1 = edge_distance(best, target)
    print(f"  success={ok}, best_distance={d1}, steps_used={used}, "
          f"elapsed={time.time()-t0:.3f}s")

    # 5. visualise a small path
    if n <= 8:
        print("\nA random backbite path (step numbers 1..N):")
        print(format_path(n, b))


if __name__ == "__main__":
    main()
