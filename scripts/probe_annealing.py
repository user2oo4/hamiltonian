#!/usr/bin/env python3
"""Probe the simulated-annealing connection search.

Runs several seeds of ``search_connection_trace`` for a fixed start/target
pair and prints, for each run, the tail of the distance trajectory.  This
shows what the endgame looks like for successful runs (the final descent to
0) and for stuck runs (the plateau at some small distance).

Usage:
    python scripts/probe_annealing.py --n 10 --steps 300000 \
        --restart 500 --first-seed 11 --num-seeds 10
"""

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hampath import (
    edge_distance,
    random_backtracking_path,
    search_connection_trace,
)

TAIL_LEN = 40


def analyze(events, initial_d: int):
    """Extract summary metrics from a trace.

    events: list of (step, distance, kind); kind in {"move", "restart", "hit"}.
    Returns (peak_before_final, peak_step, tail_string).
    """
    # Combined distance sequence: accepted moves + restarts, in order.
    seq = [(s, d) for s, d, k in events if k in ("move", "restart")]

    # Last uphill move before the end = the peak from which the final
    # descent (if any) started.
    peak, peak_step = initial_d, 0
    prev = None
    for s, d in seq:
        if prev is not None and d > prev:
            peak, peak_step = d, s
        prev = d

    tail = " ".join(str(d) for _, d in seq[-TAIL_LEN:])
    return peak, peak_step, tail


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--steps", type=int, default=300_000)
    ap.add_argument("--restart", type=int, default=500)
    ap.add_argument("--first-seed", type=int, default=11)
    ap.add_argument("--num-seeds", type=int, default=10)
    ap.add_argument("--start-seed", type=int, default=101,
                    help="seed for generating the start path")
    ap.add_argument("--target-seed", type=int, default=202,
                    help="seed for generating the target path")
    ap.add_argument("--T0", type=float, default=5.0)
    ap.add_argument("--cooling", type=float, default=0.99999)
    args = ap.parse_args()

    n = args.n
    start = random_backtracking_path(n, seed=args.start_seed)
    target = random_backtracking_path(n, seed=args.target_seed)
    d0 = edge_distance(start, target)
    print(f"n={n}  start=random_backtracking(seed={args.start_seed})  "
          f"target=random_backtracking(seed={args.target_seed})  "
          f"initial distance={d0}")
    print(f"annealing: steps={args.steps}, restart_every={args.restart}, "
          f"T0={args.T0}, cooling={args.cooling}")
    print()
    header = (f"{'seed':>4} | {'ok':>3} | {'steps':>7} | {'final':>5} | "
              f"{'peak':>4} | {'peak@':>7} | tail (last {TAIL_LEN} accepted distances)")
    print(header)
    print("-" * len(header))

    for seed in range(args.first_seed, args.first_seed + args.num_seeds):
        t0 = time.time()
        ok, best, used, events = search_connection_trace(
            n, start, target,
            steps=args.steps,
            seed=seed,
            T0=args.T0,
            cooling=args.cooling,
            restart_every=args.restart,
        )
        dt = time.time() - t0
        final_d = edge_distance(best, target)
        peak, peak_step, tail = analyze(events, d0)
        print(f"{seed:>4} | {str(ok):>3} | {used:>7} | {final_d:>5} | "
              f"{peak:>4} | {peak_step:>7} | {tail}   ({dt:.1f}s)")

    print()
    print("peak = distance at the last uphill accepted move before the end")
    print("(for successful runs: where the final descent to 0 started;")
    print(" for stuck runs: the last time it climbed before settling)")


if __name__ == "__main__":
    main()
