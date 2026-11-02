# Hamiltonian Paths on the n×n Grid and the Backbite Move

## 1. The problem

We study **Hamiltonian paths** on the **n×n square lattice grid** (4-neighbour
adjacency). A Hamiltonian path visits every one of the `N = n*n` vertices
exactly once.

The central research question: take one Hamiltonian path, repeatedly apply a
local operation called the **backbite move**, and ask

> **Can we reach every other Hamiltonian path from any starting path?**

Equivalently: *is the graph of Hamiltonian paths (edges = one backbite move)
connected?*

We built a Python package that can

1. **enumerate all Hamiltonian paths** for small n,
2. **test connectivity** of the backbite move graph exactly,
3. **generate random Hamiltonian paths** (approximately uniform via a Markov
   chain, or fast-but-biased via backtracking), and
4. run **heuristics** for bigger grids where exhaustive enumeration is
   impossible.

---

## 2. The backbite move

Given a Hamiltonian path as a sequence of vertices

```
w1 - w2 - ... - w_{k-1} - wk - w_{k+1} - ... - wN
```

pick an index `k >= 3` such that `wk` is a lattice neighbour of `w1`. Then:

* **add** the edge `(w1, wk)`,
* **delete** the edge `(w_{k-1}, wk)`.

The new path is

```
w_{k-1}, w_{k-2}, ..., w1, wk, w_{k+1}, ..., wN
```

i.e. the first `k-1` vertices are reversed and the old tail `wk..wN` is
appended. The same operation is allowed at **both ends** of the path.

Two important facts, both tested:

* The result is always again a Hamiltonian path (no vertex repeats, all
  consecutive vertices are adjacent in the grid).
* **Each backbite move is its own inverse.** Applying the same move again
  returns the original path. Consequently the move graph is *undirected*,
  and the random walk that picks a uniformly random valid backbite move at
  each step has **uniform stationary distribution on each connected
  component** of the move graph.

---

## 3. Conventions used by the code

* Vertices are numbered `0 .. n*n-1` in **row-major** order.
* A path is a tuple `(w1, ..., wN)`.
* Paths are **undirected**: `(w1..wN)` and `(wN..w1)` are the same path. The
  canonical representative is the lexicographically smaller of the two.
* The backbite move is considered at **both ends**.

---

## 4. What was implemented

```
hamiltonian/
├── hampath/
│   ├── grid.py          # grid graph, serpentine path, ASCII visualization
│   ├── path.py          # canonical path keys, edge sets, validation
│   ├── backbite.py      # backbite move (both ends), random backbite step
│   ├── enumerate.py     # exhaustive enumeration + subset-DP count
│   ├── connectivity.py  # BFS connected components of the move graph
│   ├── random_gen.py    # backbite Markov chain sampler, Warnsdorff backtracking
│   └── heuristics.py    # edge distance, simulated annealing, random-walk hit
├── scripts/
│   ├── analyze.py       # exhaustive analysis for small n
│   └── demo_random.py   # random generation / heuristic demo for larger n
├── tests/test_core.py   # 10 correctness tests
├── run_tests.py         # pytest-free test runner
└── pyproject.toml
```

### Key functions

| Function | What it does |
|---|---|
| `enumerate_hamiltonian_paths(n)` | all undirected Hamiltonian paths (DFS with connectivity pruning) |
| `count_hamiltonian_paths_dp(n)` | subset-DP count, cross-check for n ≤ 4 |
| `move_graph_stats(n, paths)` | number/sizes of connected components + degrees of the move graph |
| `backbite_moves(n, seq)` | all paths reachable by one backbite move |
| `random_backbite_path(n)` | ~uniform sample via the backbite chain (start: serpentine) |
| `random_backtracking_path(n)` | fast biased sample via randomized Warnsdorff DFS |
| `sample_paths(n, ...)` | distinct states visited by the backbite chain |
| `edge_distance(a, b)` | `(N-1) - |E(a) ∩ E(b)|`, objective for the heuristic |
| `search_connection(n, start, target)` | simulated annealing over backbite moves |
| `random_walk_hit(n, start, target)` | plain backbite walk, reports if it hits the target |

---

## 5. The heuristics, explained

### 5.1 Backbite Markov chain sampler (`random_backbite_path`, `sample_paths`)

Start from the deterministic serpentine path, then repeatedly apply a
**uniformly random valid backbite move**.

Why this is a good sampler: the move is its own inverse, so the chain is
symmetric; on each connected component the stationary distribution is
**uniform**. If the move graph is connected (which our small-n results show),
this is an approximately uniform sampler over *all* Hamiltonian paths.
Practical details: default run length `max(10000, 1000*N)` moves, or sample
every `steps_between` moves to decorrelate.

### 5.2 Fast biased generator (`random_backtracking_path`)

Randomized depth-first search with the **Warnsdorff heuristic**: at each
step, order the unvisited neighbours of the current endpoint by the number of
*their* unvisited neighbours (fewest first), with random tie-breaking.

Two extra safeguards:

* **Connectivity pruning** — the remaining unvisited vertices must induce a
  connected subgraph, otherwise the partial path can never be completed and
  the branch is abandoned.
* **Node budget** — each attempt gives up after 200,000 explored nodes and
  restarts from a new random vertex.

This is biased (not uniform), but extremely fast: it finds a path for grids
well beyond n = 30 in a fraction of a second.

### 5.3 Simulated annealing reachability (`search_connection`)

Heuristic answer to "are these two paths in the same connected component?"
Define the objective

```
edge_distance(a, b) = (N - 1) - |E(a) ∩ E(b)|
```

which counts how many edges of `a` are missing from `b` (0 means same path).
The algorithm:

1. Start at `start`.
2. Propose a uniformly random backbite move.
3. Accept it if it improves the distance, or with Metropolis probability
   `exp((d_old - d_new) / T)` otherwise.
4. Cool the temperature geometrically (`T *= 0.99995`, floor `1e-3`).
5. Optional restarts: after a plateau, jump back to the best state seen so
   far to escape local minima.

It returns `(success, best_path_found, steps_used)`. **A failure only means
the heuristic did not find a path — it is not a proof of disconnectedness.**

### 5.4 Plain random-walk hit (`random_walk_hit`)

Run the backbite random walk and report whether it hits a specific target
within a step budget. Only useful when the component is small enough to be
hit by chance (roughly n ≤ 6).

---

## 6. Results

### 6.1 Exact results (exhaustive)

| n | N | # Hamiltonian paths (undirected) | Move graph components | Degree min / avg / max |
|---|---:|---:|---|---|
| 1 | 1 | 1 | 1 (trivial) | 0 / 0 / 0 |
| 2 | 4 | 4 | **1** | 2 / 2.00 / 2 |
| 3 | 9 | 20 | **1** | 2 / 2.80 / 4 |
| 4 | 16 | 276 | **1** | 2 / 3.77 / 6 |
| 5 | 25 | 4,324 | **1** | 2 / 4.02 / 6 |
| 6 | 36 | 229,348 | **1** | 2 / 4.54 / 6 |

DP cross-check (subset DP) confirms the enumeration counts for n ≤ 4:
directed/undirected = 8/4 (n=2), 40/20 (n=3), 552/276 (n=4).

**Conclusion:** for every n ≤ 6, the backbite move graph on Hamiltonian paths
is **connected** — from any Hamiltonian path one can reach every other using
only backbite moves. This also means the backbite Markov chain is a valid
uniform sampler on these grids.

Timings (this machine): n=6 enumeration ≈ 15 s, move-graph BFS ≈ 3 s. n=7+
is not feasible to enumerate exhaustively with the current in-memory
representation.

### 6.2 Heuristic results (bigger grids)

`search_connection` between two independent `random_backtracking_path`s:

| n | initial distance | success | steps used | notes |
|---|---:|---|---|---|
| 7 | 20 | yes | ~58,000 | ~1.1 s |
| 8 | 25 | yes | ~63,000 | ~1.4 s |
| 10 | 31 | yes* | ~179,000 | seed-dependent; some seeds get stuck at distance 3 |

\* n=10 needed restarts (`restart_every=500`) and a lucky seed; other seeds
plateau at distance 3. This is expected behaviour for simulated annealing,
not evidence of disconnected components.

---

## 7. How to run everything

All commands run from the project root
`/home/hieppham/Documents/projects/hamiltonian`.

### Run the tests

Option A — plain Python (no extra dependencies):

```bash
python3 run_tests.py
```

Option B — if you have pytest installed:

```bash
pip install pytest          # only needed once, if at all
python3 -m pytest tests/ -q
```

Expected output of `run_tests.py`:

```
PASS test_canonical
PASS test_serpentine_is_valid
PASS test_backbite_head_move_involution
PASS test_backbite_moves_are_valid_paths
PASS test_enumeration_counts_small
PASS test_move_graph_n2_connected
PASS test_random_generators
PASS test_search_connection_trivial
PASS test_edge_distance
PASS test_format_path_smoke

10 passed, 0 failed
```

### Exhaustive analysis for small n

```bash
# n = 2..5: instant
python3 scripts/analyze.py --min-n 2 --max-n 5

# include n = 6 (takes ~15-20 s and some memory)
python3 scripts/analyze.py --min-n 6 --max-n 6 --no-dp
```

### Random generation / heuristic demo for larger n

```bash
python3 scripts/demo_random.py --n 8
python3 scripts/demo_random.py --n 10 --samples 200 --search-steps 200000
```

### Library usage

```python
from hampath import (
    enumerate_hamiltonian_paths, move_graph_stats,
    random_backbite_path, random_backtracking_path,
    search_connection, edge_distance, format_path,
)

# exact enumeration + connectivity (small n)
paths = enumerate_hamiltonian_paths(5)
stats = move_graph_stats(5, paths)
print(stats["n_components"], stats["component_sizes"])   # 1, [4324]

# approximately uniform random path
p = random_backbite_path(8, seed=42)

# fast biased random path
q = random_backtracking_path(50)

# heuristic: try to transform q into p using only backbite moves
ok, best, steps = search_connection(8, q, p, steps=100_000, seed=1)

# pretty print
print(format_path(8, p))
```

---

## 8. Known limitations / possible next steps

* **n ≥ 7 exhaustive enumeration** needs a more compact representation
  (e.g. pack a path into a single Python int, 5-6 bits per vertex) and
  probably C++ for speed.
* The simulated-annealing connection search is seed/temperature sensitive;
  a best-first search with a priority queue over `edge_distance` could be a
  stronger deterministic heuristic.
* No formal proof of connectivity yet — only empirical evidence for n ≤ 6
  plus heuristic successes for n = 7, 8, 10.
