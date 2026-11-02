"""The backbite move for Hamiltonian paths.

Definition (at the ``w1`` end)
------------------------------
Given a path ``(w1, w2, ..., wN)`` and an index k >= 3 such that ``wk`` is a
lattice neighbour of ``w1``:

    * add the edge  ``(w1, wk)``
    * delete the edge ``(w_{k-1}, wk)``

The new path is

    ``(w_{k-1}, w_{k-2}, ..., w1, wk, w_{k+1}, ..., wN)``

i.e. the first k-1 vertices are reversed and then the old tail ``wk..wN`` is
appended.  The same operation is allowed at the other end (``wN``) by
symmetry.  Each backbite move is its own inverse, so the move graph is
undirected and the uniform distribution is stationary for the random walk.
"""

from __future__ import annotations

import random
from typing import Dict, Iterable, Optional, Sequence, Set, Tuple

from .grid import build_adjacency
from .path import canonical

Path = Tuple[int, ...]


def _head_move(seq: Sequence[int], pos: int) -> Path:
    """Apply a backbite at the head.

    ``pos`` is the index (0-based) of ``wk`` in ``seq``, with ``pos >= 2``
    and ``seq[pos]`` adjacent to ``seq[0]`` in the lattice.
    """
    return tuple(seq[pos - 1 :: -1]) + tuple(seq[pos:])


def backbite_moves(n: int, seq: Sequence[int], adj=None) -> Set[Path]:
    """All distinct paths reachable from ``seq`` by one backbite move.

    Moves at both ends are considered.  Results are canonical (undirected)
    tuples.
    """
    if adj is None:
        adj = build_adjacency(n)
    N = n * n
    seq = tuple(seq)
    pos: Dict[int, int] = {v: i for i, v in enumerate(seq)}
    results: Set[Path] = set()

    # ---- moves at the w1 end ----
    head = seq[0]
    for u in adj[head]:
        p = pos[u]
        if p >= 2:
            results.add(canonical(_head_move(seq, p)))

    # ---- moves at the wN end (apply to reversed sequence, reverse back) ----
    rev = seq[::-1]
    tail = seq[-1]
    for u in adj[tail]:
        p = pos[u]           # position of u in the original sequence
        pr = N - 1 - p       # position of u in the reversed sequence
        if pr >= 2:
            results.add(canonical(_head_move(rev, pr)[::-1]))

    return results


def random_backbite_step(
    n: int,
    seq: Sequence[int],
    rng: Optional[random.Random] = None,
    adj=None,
) -> Path:
    """Apply one uniformly random valid backbite move.

    Returns the input path unchanged if no move is available (only possible
    for tiny degenerate cases).
    """
    if rng is None:
        rng = random
    moves = list(backbite_moves(n, seq, adj))
    if not moves:
        return canonical(seq)
    return rng.choice(moves)
