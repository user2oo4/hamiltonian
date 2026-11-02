"""Move-graph analysis: components and degrees of the backbite move graph."""

from __future__ import annotations

from collections import deque
from typing import Dict, Iterable, List, Sequence, Tuple

from .backbite import backbite_moves
from .grid import build_adjacency

Path = Tuple[int, ...]


def move_graph_stats(
    n: int,
    paths: Iterable[Path],
    adj=None,
) -> Dict:
    """Analyse the graph whose vertices are Hamiltonian paths and whose edges
    are backbite moves.

    Parameters
    ----------
    n : grid size
    paths : all paths to include as vertices (canonical tuples)

    Returns
    -------
    dict with keys
        n_components   : number of connected components
        component_sizes: component sizes, largest first
        degrees        : dict path -> number of distinct backbite moves
        min_degree, max_degree, avg_degree
    """
    if adj is None:
        adj = build_adjacency(n)

    path_set = set(paths)
    visited = set()
    components: List[int] = []
    degrees: Dict[Path, int] = {}

    for start in path_set:
        if start in visited:
            continue
        queue = deque([start])
        visited.add(start)
        size = 0
        while queue:
            cur = queue.popleft()
            size += 1
            moves = backbite_moves(n, cur, adj)
            degrees[cur] = len(moves)
            for m in moves:
                if m in path_set and m not in visited:
                    visited.add(m)
                    queue.append(m)
        components.append(size)

    deg_values = list(degrees.values()) if degrees else [0]
    return {
        "n_paths": len(path_set),
        "n_components": len(components),
        "component_sizes": sorted(components, reverse=True),
        "degrees": degrees,
        "min_degree": min(deg_values),
        "max_degree": max(deg_values),
        "avg_degree": sum(deg_values) / len(deg_values),
    }
