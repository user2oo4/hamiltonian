"""Heuristic tools for larger grids, where exhaustive enumeration is
impossible.

* ``edge_distance``            -- how many path edges differ from a target.
* ``search_connection``        -- simulated annealing over backbite moves to
                                 try to transform one path into another
                                 (heuristic reachability in the move graph).
* ``random_walk_hit``          -- plain backbite random walk that reports
                                 whether it hits a target path within a
                                 budget (useful for moderate n).
"""

from __future__ import annotations

import math
import random
from typing import List, Optional, Sequence, Tuple

from .backbite import backbite_moves, random_backbite_step
from .grid import build_adjacency
from .path import canonical, path_edges

Path = Tuple[int, ...]


def edge_distance(seq_a: Sequence[int], seq_b: Sequence[int]) -> int:
    """Number of edges of ``seq_a`` that are not edges of ``seq_b``.

    Both paths have N-1 edges, so this equals (N-1) - |E(a) ∩ E(b)| and is a
    metric (half the symmetric difference of the edge sets).
    """
    ea = path_edges(seq_a)
    eb = path_edges(seq_b)
    return len(ea) - len(ea & eb)


def _anneal(
    n: int,
    start: Sequence[int],
    target: Sequence[int],
    steps: int,
    seed: Optional[int],
    T0: Optional[float],
    T_min: float,
    cooling: float,
    restart_every: Optional[int],
    trace: bool,
):
    """Core simulated-annealing loop shared by the public wrappers.

    Returns ``(success, best_path, steps_used, events)``.  ``events`` is a
    list of ``(step, distance, kind)`` tuples where kind is one of
    ``"move"`` (a proposed backbite move was accepted), ``"restart"`` (the
    walk jumped back to the best state seen so far) or ``"hit"`` (the target
    was reached).  It is empty unless ``trace=True``.
    """
    rng = random.Random(seed)
    adj = build_adjacency(n)
    N = n * n
    cur = canonical(start)
    tgt = canonical(target)
    tgt_edges = path_edges(tgt)

    def dist(seq: Path) -> int:
        return (N - 1) - len(path_edges(seq) & tgt_edges)

    d = dist(cur)
    events: List[Tuple[int, int, str]] = []
    if d == 0:
        if trace:
            events.append((0, 0, "hit"))
        return True, cur, 0, events

    best = (d, cur)
    T = T0 if T0 is not None else max(1.0, float(d))
    since_improve = 0

    for step in range(1, steps + 1):
        moves = list(backbite_moves(n, cur, adj))
        if not moves:
            break
        nxt = rng.choice(moves)
        dn = dist(nxt)

        if dn <= d or rng.random() < math.exp((d - dn) / T):
            cur, d = nxt, dn
            if trace:
                events.append((step, d, "move"))

        if d < best[0]:
            best = (d, cur)
            since_improve = 0
            if d == 0:
                if trace:
                    events.append((step, 0, "hit"))
                return True, cur, step, events
        else:
            since_improve += 1

        # Optional: jump back to the best state seen so far after a long
        # plateau, to escape local minima.
        if restart_every is not None and since_improve >= restart_every:
            cur = best[1]
            d = best[0]
            since_improve = 0
            if trace:
                events.append((step, d, "restart"))

        T = max(T * cooling, T_min)

    return False, best[1], steps, events


def search_connection(
    n: int,
    start: Sequence[int],
    target: Sequence[int],
    steps: int = 200_000,
    seed: Optional[int] = None,
    T0: Optional[float] = None,
    T_min: float = 1e-3,
    cooling: float = 0.99995,
    restart_every: Optional[int] = None,
) -> Tuple[bool, Path, int]:
    """Heuristically try to reach ``target`` from ``start`` via backbite moves.

    Uses simulated annealing on ``edge_distance`` to the target.  If the two
    paths lie in the same connected component this often succeeds for modest
    n; failure only means the heuristic did not find a path, not a proof of
    disconnectedness.

    Returns ``(success, best_path_found, steps_used)``.
    """
    ok, best, used, _ = _anneal(
        n, start, target, steps, seed, T0, T_min, cooling, restart_every, False
    )
    return ok, best, used


def search_connection_trace(
    n: int,
    start: Sequence[int],
    target: Sequence[int],
    steps: int = 200_000,
    seed: Optional[int] = None,
    T0: Optional[float] = None,
    T_min: float = 1e-3,
    cooling: float = 0.99995,
    restart_every: Optional[int] = None,
) -> Tuple[bool, Path, int, List[Tuple[int, int, str]]]:
    """Like :func:`search_connection`, but also returns the trajectory.

    Returns ``(success, best_path_found, steps_used, events)`` where
    ``events`` is a list of ``(step, distance, kind)`` with kind in
    ``{"move", "restart", "hit"}`` (only accepted moves are recorded).
    """
    return _anneal(
        n, start, target, steps, seed, T0, T_min, cooling, restart_every, True
    )


def random_walk_hit(
    n: int,
    start: Sequence[int],
    target: Sequence[int],
    steps: int,
    seed: Optional[int] = None,
) -> Tuple[bool, int]:
    """Plain backbite random walk; returns True if it hits ``target``.

    Only useful when the component is small enough to be hit by chance
    (e.g. n <= 4, or with a very large ``steps`` budget).
    """
    rng = random.Random(seed)
    adj = build_adjacency(n)
    cur = canonical(start)
    tgt = canonical(target)
    if cur == tgt:
        return True, 0
    for i in range(1, steps + 1):
        cur = random_backbite_step(n, cur, rng, adj)
        if cur == tgt:
            return True, i
    return False, steps
