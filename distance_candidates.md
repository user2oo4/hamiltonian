# Distance formula candidates

Working notes for a sequence-aware distance between two Hamiltonian paths,
intended to replace / refine the current `edge_distance` heuristic.

Status: **discussion only — no code changes yet.**

---

## Setup and notation

Grid size n, N = n². Two paths as sequences:

```
A = (a_0, a_1, ..., a_{N-1})
B = (b_0, b_1, ..., b_{N-1})
```

Paths are undirected, so A may be compared against either B or its reverse
B^R. For an orientation σ ∈ {+1, −1}:

```
B^{+1} = B
B^{-1} = B^R
```

Relabel A by where its vertices sit in B:

```
p_i^σ  =  the index j such that  B^σ_j = a_i
```

So p^σ = (p_0, ..., p_{N-1}) is a permutation of {0, ..., N-1}.

- If A = B, then p = (0, 1, 2, ..., N-1).
- If A = B^R, then p = (N-1, ..., 1, 0).

All candidates below are functions of this permutation.

---

## Candidate 1 — edge distance (current metric)

Let s_i = p_{i+1} − p_i. Vertex position i is a **breakpoint** if |s_i| ≠ 1
(the consecutive pair in A is not a consecutive pair in B).

```
d_edge(A,B) = number of breakpoints
```

This is the current metric, restated in sequence language.

**Weakness:** it only counts *how many* adjacencies are broken, not *where*
or *how the remaining pieces are arranged*. Two distance-1 states can be
structurally very different.

---

## Subtlety: run count adds nothing

Earlier idea: split A into maximal "runs" of consecutive positions. But since
p is a permutation, any segment where consecutive positions differ by ±1 is
automatically monotone (a `+1, −1` zigzag would revisit a value, which is
impossible). Therefore:

```
number of runs  =  d_edge + 1
```

So run count = edge distance + 1; it contains **no new information**. The
refinement must come from *where* the breakpoints are, or from *how
displaced* the vertices are.

---

## Candidate 2 — weighted breakpoint distance  D_w

Each breakpoint gets a weight of 1 plus its distance from the nearest end of
the path:

```
D_w(A,B) = Σ over breakpoints i of  ( 1 + min(i, N−2−i) )
```

- i ranges over the edges of A, i = 0 .. N−2.
- The two ends are i = 0 (head side) and i = N−2 (tail side).
- The `1 +` keeps it a strict refinement: if all breakpoints are at the very
  ends, D_w = d_edge.

Rationale: a backbite attacks an edge by joining an endpoint to some w_k.
Breakpoints near the ends are cheap to reach; breakpoints in the middle
require maneuvering an endpoint there.

Properties: D_w = 0 ⟺ A = B or B^R. Integer, O(N), no normalization needed.

---

## Candidate 3 — footrule distance  D_F  (global displacement)

```
D_F(A,B) = min over σ∈{+1,−1}  Σ_{i=0}^{N-1}  | p_i^σ − i |
```

Spearman footrule: total displacement between the two sequences under the
better orientation. Smooth, O(N), 0 iff A = B or B^R.

Combined version:

```
D(A,B) = d_edge(A,B) + (1/N) · D_F(A,B)
```

The 1/N keeps terms comparable: d_edge ∈ [0, N−1], D_F/N ∈ [0, ~N/2].

---

## Worked example: two distance-1 states (N = 100)

Target B = (0, 1, 2, ..., 99).

**Good state** — B with the last 10 elements reversed:

```
A_good = (0, 1, ..., 89, 99, 98, ..., 90)
```

- d_edge = 1 (one breakpoint at 89 → 99)
- D_w = 1 + min(89, 98−89) = 1 + 9 = **10**
- D_F ≤ 90, D_F/N ≤ 0.9 → combined D ≈ 1 + 0.9 = **~1.9**

**Bad state** — B split in half, second block moved to the front:

```
A_bad = (50, 51, ..., 99, 0, 1, ..., 49)
```

- d_edge = 1 (still only one breakpoint, at 99 → 0) — the blindness
- D_w = 1 + min(49, 49) = **50**
- D_F = 100 · 50 = 5000, D_F/N = 50 → combined D ≈ 1 + 50 = **51**

So the two states that edge distance cannot tell apart (both "1") become
clearly separated: D_w = 10 vs 50, D = ~1.9 vs 51.

---

## The ideal metric (for context)

The truly correct objective is the **constrained reversal distance**: the
minimum number of *legal* backbite moves to turn A into B.

- Without the grid constraint, this is pancake-sorting (prefix/suffix
  reversal) distance — hard to compute exactly in general.
- The grid constraint (new closing edge must be a lattice edge) makes it
  even more constrained.

For n ≤ 6 we already have the full move graph, so the true distance between
any pair of paths can be computed exactly by BFS — useful as ground truth.

---

## Validation plan (when we get back to code)

1. For n = 5 or 6, take all paths (4,324 or 229,348).
2. Compute true move-graph distance for a sample of pairs (BFS).
3. For the same pairs, compute d_edge, D_w, and D.
4. Measure Spearman correlation between each candidate and the true
   distance; or check whether greedy descent using the candidate reaches
   the target more often / produces fewer 1↔2 bounces in the annealing
   trace.

Initial bet: D_w is the simplest strong upgrade; d_edge + D_F/N is the
smoother fallback.

---

## Open questions / things to discuss

- Is "breakpoints near the middle are worse" actually true for backbite, or
  is the real bottleneck purely geometric (which vertex pairs the endpoint
  can join)?
- Should the weight be min(i, N−2−i) or something like min(i+1, N−1−i)?
- Does D_w make the annealing landscape smooth enough, or do we still need
  restarts / plateau kicks?
- Could we use the true BFS distance on small n to *learn* a better weight
  function instead of guessing it?
