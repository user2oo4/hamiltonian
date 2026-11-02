"""hampath: Hamiltonian paths on the n x n lattice grid and the backbite move.

Conventions
-----------
* Grid vertices are numbered 0 .. n*n-1 in row-major order.
* A Hamiltonian path is stored as a tuple ``(w1, w2, ..., wN)`` of vertices.
* Paths are treated as *undirected*: a sequence and its reverse are the same
  path.  We always use the lexicographically smaller of the two as the
  canonical key.
* The backbite move is allowed at either end of the path (both ends).
"""

from .grid import build_adjacency, vertex_to_rc, rc_to_vertex, serpentine_path, format_path
from .path import canonical, path_edges, is_hamiltonian_path
from .backbite import backbite_moves, random_backbite_step
from .enumerate import enumerate_hamiltonian_paths, count_hamiltonian_paths_dp
from .connectivity import move_graph_stats
from .random_gen import (
    backbite_walk,
    random_backbite_path,
    random_backtracking_path,
    sample_paths,
)
from .heuristics import edge_distance, search_connection, search_connection_trace, random_walk_hit

__all__ = [
    "build_adjacency",
    "vertex_to_rc",
    "rc_to_vertex",
    "serpentine_path",
    "format_path",
    "canonical",
    "path_edges",
    "is_hamiltonian_path",
    "backbite_moves",
    "random_backbite_step",
    "enumerate_hamiltonian_paths",
    "count_hamiltonian_paths_dp",
    "move_graph_stats",
    "backbite_walk",
    "random_backbite_path",
    "random_backtracking_path",
    "sample_paths",
    "edge_distance",
    "search_connection",
    "search_connection_trace",
    "random_walk_hit",
]
