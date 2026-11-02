"""Hamiltonian path representation (undirected convention)."""

from __future__ import annotations

from typing import FrozenSet, Sequence, Tuple

Path = Tuple[int, ...]


def canonical(seq: Sequence[int]) -> Path:
    """Return the canonical representative of an undirected path.

    ``min(seq, reversed(seq))`` with lexicographic order, so a path and its
    reverse map to the same tuple.
    """
    t = tuple(seq)
    r = t[::-1]
    return t if t <= r else r


def path_edges(seq: Sequence[int]) -> FrozenSet[Tuple[int, int]]:
    """Return the set of undirected edges of the path."""
    return frozenset((min(a, b), max(a, b)) for a, b in zip(seq, seq[1:]))


def is_hamiltonian_path(n: int, seq: Sequence[int], adj=None) -> bool:
    """Check that ``seq`` is a Hamiltonian path of the n x n grid."""
    from .grid import build_adjacency

    N = n * n
    if len(seq) != N:
        return False
    if len(set(seq)) != N or any(not (0 <= v < N) for v in seq):
        return False
    if adj is None:
        adj = build_adjacency(n)
    return all(b in adj[a] for a, b in zip(seq, seq[1:]))
