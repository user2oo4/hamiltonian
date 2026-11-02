"""Grid graph utilities for the n x n lattice."""

from __future__ import annotations

from typing import List, Sequence, Tuple

Vertex = int


def vertex_to_rc(n: int, v: Vertex) -> Tuple[int, int]:
    """Return (row, col) of vertex v on an n x n grid."""
    return divmod(v, n)


def rc_to_vertex(n: int, r: int, c: int) -> Vertex:
    """Return vertex id of cell (r, c) on an n x n grid."""
    return r * n + c


def build_adjacency(n: int) -> List[Tuple[int, ...]]:
    """Adjacency lists of the n x n grid graph (4-neighbour lattice)."""
    adj: List[Tuple[int, ...]] = []
    for v in range(n * n):
        r, c = divmod(v, n)
        ns = []
        if r > 0:
            ns.append(v - n)
        if r < n - 1:
            ns.append(v + n)
        if c > 0:
            ns.append(v - 1)
        if c < n - 1:
            ns.append(v + 1)
        adj.append(tuple(ns))
    return adj


def serpentine_path(n: int) -> Tuple[int, ...]:
    """A guaranteed Hamiltonian path on the n x n grid (snake order).

    Row 0 left->right, row 1 right->left, etc.  This is a spanning path for
    every n >= 1, and is the default starting point for the backbite chain.
    """
    seq = []
    for r in range(n):
        row = [r * n + c for c in range(n)]
        if r % 2 == 1:
            row.reverse()
        seq.extend(row)
    return tuple(seq)


def format_path(n: int, seq: Sequence[int]) -> str:
    """Pretty-print a path as an n x n table of step numbers (1..N)."""
    order = [0] * (n * n)
    for i, v in enumerate(seq):
        order[v] = i + 1
    lines = []
    for r in range(n):
        lines.append(" ".join(f"{order[r * n + c]:3d}" for c in range(n)))
    return "\n".join(lines)
