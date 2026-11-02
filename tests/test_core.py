"""Core correctness tests for hampath."""

import random

from hampath import (
    backbite_moves,
    build_adjacency,
    canonical,
    count_hamiltonian_paths_dp,
    edge_distance,
    enumerate_hamiltonian_paths,
    format_path,
    is_hamiltonian_path,
    move_graph_stats,
    path_edges,
    random_backbite_path,
    random_backtracking_path,
    search_connection,
    serpentine_path,
)
from hampath.backbite import _head_move


def test_canonical():
    assert canonical((1, 2, 3)) == (1, 2, 3)
    assert canonical((3, 2, 1)) == (1, 2, 3)
    assert canonical((0, 1)) == (0, 1)


def test_serpentine_is_valid():
    for n in range(1, 8):
        p = serpentine_path(n)
        assert is_hamiltonian_path(n, p)


def test_backbite_head_move_involution():
    seq = (0, 1, 2, 5, 4, 3, 6, 7, 8)  # a path on 3x3
    adj = build_adjacency(3)
    pos = {v: i for i, v in enumerate(seq)}
    for u in adj[seq[0]]:
        p = pos[u]
        if p >= 2:
            new = _head_move(seq, p)
            assert is_hamiltonian_path(3, new)
            pos2 = {v: i for i, v in enumerate(new)}
            back = _head_move(new, pos2[u])
            assert back == seq


def test_backbite_moves_are_valid_paths():
    rng = random.Random(0)
    for n in (3, 4):
        p = random_backbite_path(n, steps=200, seed=1)
        for _ in range(50):
            moves = backbite_moves(n, p)
            assert moves, "expected at least one move"
            for m in moves:
                assert is_hamiltonian_path(n, m)
            p = rng.choice(list(moves))


def test_enumeration_counts_small():
    # 1x1: single vertex path
    assert len(enumerate_hamiltonian_paths(1)) == 1
    # 2x2: the 4-cycle minus any one edge -> 4 paths
    assert len(enumerate_hamiltonian_paths(2)) == 4
    # DP cross-check for n <= 4
    for n in (1, 2, 3, 4):
        directed, undirected = count_hamiltonian_paths_dp(n)
        enum = len(enumerate_hamiltonian_paths(n))
        assert undirected == enum, (n, undirected, enum)
        if n >= 2:
            assert directed == 2 * enum


def test_move_graph_n2_connected():
    paths = enumerate_hamiltonian_paths(2)
    stats = move_graph_stats(2, paths)
    assert stats["n_components"] == 1
    assert stats["component_sizes"] == [4]


def test_random_generators():
    for n in (1, 2, 3, 4, 5, 10):
        p = random_backbite_path(n, steps=200, seed=n)
        assert is_hamiltonian_path(n, p)
        q = random_backtracking_path(n, seed=n)
        assert is_hamiltonian_path(n, q)


def test_search_connection_trivial():
    p = serpentine_path(4)
    ok, hit, _ = search_connection(4, p, p, steps=10, seed=0)
    assert ok and hit == p


def test_edge_distance():
    a = (0, 1, 2, 3)
    b = (2, 1, 0, 3)
    assert edge_distance(a, a) == 0
    assert edge_distance(a, b) == edge_distance(b, a)
    assert 0 < edge_distance(a, b) <= 3


def test_format_path_smoke():
    s = format_path(3, serpentine_path(3))
    assert len(s.splitlines()) == 3
