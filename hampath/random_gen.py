"""Random generation of Hamiltonian paths.

Two generators are provided:

1. ``random_backbite_path`` -- start from a known path (serpentine) and run
   the backbite random walk.  Because every backbite move is its own inverse,
   the walk's stationary distribution is uniform on each connected component
   of the move graph.  If (as conjectured / to be tested) the move graph is
   connected, this is an approximately uniform sampler.

2. ``random_backtracking_path`` -- randomized DFS with the Warnsdorff
   heuristic (visit the neighbour with the fewest onward options first).
   This is biased but very fast, even for large grids.
"""

from __future__ import annotations

import random
from typing import Iterator, Optional, Sequence, Set, Tuple

from .backbite import random_backbite_step
from .enumerate import _unvisited_connected
from .grid import build_adjacency, serpentine_path
from .path import canonical

Path = Tuple[int, ...]


def backbite_walk(
    n: int,
    steps: int,
    seed: Optional[int] = None,
    start: Optional[Sequence[int]] = None,
) -> Iterator[Path]:
    """Yield the state after each backbite step (``steps`` states total)."""
    rng = random.Random(seed)
    adj = build_adjacency(n)
    seq = tuple(start) if start is not None else serpentine_path(n)
    for _ in range(steps):
        seq = random_backbite_step(n, seq, rng, adj)
        yield seq


def random_backbite_path(
    n: int,
    steps: Optional[int] = None,
    seed: Optional[int] = None,
    start: Optional[Sequence[int]] = None,
) -> Path:
    """Approximately uniform random Hamiltonian path via the backbite chain.

    ``steps`` defaults to ``max(10000, 1000 * N)`` which is plenty for small
    grids; for serious sampling increase it or use ``sample_paths`` with
    decorrelation gaps.
    """
    N = n * n
    if steps is None:
        steps = max(10_000, 1000 * N)
    rng = random.Random(seed)
    adj = build_adjacency(n)
    seq = tuple(start) if start is not None else serpentine_path(n)
    for _ in range(steps):
        seq = random_backbite_step(n, seq, rng, adj)
    return seq


def sample_paths(
    n: int,
    num_samples: int,
    steps_between: int = 100,
    seed: Optional[int] = None,
    start: Optional[Sequence[int]] = None,
) -> Set[Path]:
    """Collect ``num_samples`` states from a backbite walk, one every
    ``steps_between`` moves.  Returns the set of distinct paths seen."""
    rng = random.Random(seed)
    adj = build_adjacency(n)
    seq = tuple(start) if start is not None else serpentine_path(n)
    seen: Set[Path] = set()
    for _ in range(num_samples):
        for _ in range(steps_between):
            seq = random_backbite_step(n, seq, rng, adj)
        seen.add(seq)
    return seen


def random_backtracking_path(
    n: int,
    seed: Optional[int] = None,
    max_attempts: int = 200,
    max_nodes_per_attempt: int = 200_000,
) -> Path:
    """Fast biased random Hamiltonian path via randomized Warnsdorff DFS.

    At each step the neighbours of the current endpoint are ordered by the
    number of *their* unvisited neighbours (fewest first), with ties broken
    randomly.  Connectivity pruning (the remaining unvisited vertices must
    induce a connected subgraph) cuts off dead branches, which makes the
    search fast and reliable even for large grids.
    """
    rng = random.Random(seed)
    adj = build_adjacency(n)
    N = n * n
    full = (1 << N) - 1

    def onward_count(u: int, mask: int) -> int:
        cnt = 0
        for w in adj[u]:
            if not (mask & (1 << w)):
                cnt += 1
        return cnt

    def dfs(v: int, mask: int, path: list, nodes: list) -> bool:
        if len(path) == N:
            return True
        nodes[0] += 1
        if nodes[0] > max_nodes_per_attempt:
            return False

        rem = full ^ mask
        if rem and not _unvisited_connected(adj, rem):
            return False

        cands = []
        for u in adj[v]:
            if not (mask & (1 << u)):
                cands.append((onward_count(u, mask), rng.random(), u))
        cands.sort()
        for _, _, u in cands:
            path.append(u)
            if dfs(u, mask | (1 << u), path, nodes):
                return True
            path.pop()
        return False

    for _ in range(max_attempts):
        start = rng.randrange(N)
        path = [start]
        if dfs(start, 1 << start, path, [0]):
            return canonical(tuple(path))
    raise RuntimeError(
        f"failed to find a Hamiltonian path on {n}x{n} in {max_attempts} attempts"
    )
