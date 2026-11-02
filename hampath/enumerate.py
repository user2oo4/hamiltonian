"""Exhaustive enumeration of Hamiltonian paths on the n x n grid."""

from __future__ import annotations

from typing import Dict, List, Optional, Set, Tuple

from .grid import build_adjacency
from .path import canonical

Path = Tuple[int, ...]


def _unvisited_connected(adj, rem: int) -> bool:
    """True iff the subgraph induced by the vertex set encoded in ``rem``
    (bitmask of *unvisited* vertices) is connected."""
    if rem == 0:
        return True
    lsb = rem & -rem
    start = lsb.bit_length() - 1
    seen = lsb
    stack = [start]
    while stack:
        v = stack.pop()
        for u in adj[v]:
            bit = 1 << u
            if (rem & bit) and not (seen & bit):
                seen |= bit
                stack.append(u)
    return seen == rem


def enumerate_hamiltonian_paths(
    n: int,
    use_connectivity_prune: bool = True,
    verbose: bool = False,
) -> Set[Path]:
    """Enumerate all (undirected) Hamiltonian paths of the n x n grid.

    Returns a set of canonical tuples ``(w1, ..., wN)``.  A path and its
    reverse appear only once.

    Uses DFS with bitmask visited set and a connectivity pruning rule: the
    remaining unvisited vertices must always induce a connected subgraph,
    otherwise no completion is possible.  Feasible for n <= 4 quickly and
    for n = 5 within seconds to a couple of minutes.
    """
    adj = build_adjacency(n)
    N = n * n
    full = (1 << N) - 1
    results: Set[Path] = set()
    path = [0] * N
    conn_cache: Dict[int, bool] = {}

    def dfs(v: int, mask: int, depth: int) -> None:
        if depth == N:
            results.add(canonical(path))
            return

        rem = full ^ mask
        if use_connectivity_prune and rem:
            ok = conn_cache.get(mask)
            if ok is None:
                ok = _unvisited_connected(adj, rem)
                conn_cache[mask] = ok
            if not ok:
                return

        for u in adj[v]:
            bit = 1 << u
            if not (mask & bit):
                path[depth] = u
                dfs(u, mask | bit, depth + 1)

    for s in range(N):
        path[0] = s
        dfs(s, 1 << s, 1)

    if verbose:
        print(f"[enumerate] n={n}: {len(results)} undirected Hamiltonian paths "
              f"(connectivity cache hits on {len(conn_cache)} masks)")
    return results


def count_hamiltonian_paths_dp(n: int) -> Tuple[int, int]:
    """Count Hamiltonian paths by subset DP.

    Returns ``(directed_count, undirected_count)``.  A directed count is a
    sequence ``(w1..wN)`` with start and end distinguished; the undirected
    count divides by 2 (for N >= 2).

    Only practical for n <= 4 in pure Python (2^16 * 16 states for n = 4).
    """
    if n > 4:
        raise ValueError("subset DP counting is only practical for n <= 4")

    adj = build_adjacency(n)
    N = n * n
    size = 1 << N
    dp: List[List[int]] = [[0] * N for _ in range(size)]
    for v in range(N):
        dp[1 << v][v] = 1

    for mask in range(1, size):
        row = dp[mask]
        for v in range(N):
            c = row[v]
            if c:
                for u in adj[v]:
                    bit = 1 << u
                    if not (mask & bit):
                        dp[mask | bit][u] += c

    directed = sum(dp[size - 1])
    undirected = directed if N == 1 else directed // 2
    return directed, undirected
