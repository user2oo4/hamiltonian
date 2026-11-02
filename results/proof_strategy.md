# Proof strategy summary: connectivity of the backbite graph

Status: working draft. Last major rewrite: **2026-11-02** (pruned to the
current architecture; false claims removed). Bond / parity side thread lives in
`results/parity_notes.md`.

*Empirical* = verified exhaustively for n = 4, 5, 6 (and n = 7 on L where
stated). **Small-n evidence has already failed twice when carried from n = 5 to
n = 6. Treat it as suggestive, never as proof.**

---

## 0. Terminology

- **Backbite at an endpoint**: add `endpoint–u` for a free neighbour `u` at
  position k ≥ 2; delete `u–w_{k−1}`. New endpoint is `w_{k−1}`.
- **h** = number of horizontal edges; `Δh ∈ {−1, 0, +1}` per move.
- **U** = has a +1 move. **P** = no +1 move. **S** = every move is −1.
- **Locked endpoint** = endpoint in a corner or left/right column whose first
  edge is horizontal. **L** = paths with both endpoints locked.
- **Plateau arm** = an arm with Δh = 0.
- **Total plateau degree** of a state = (plateau arms at head) + (arms at
  tail) ≤ 6.
- **Plateau component** = component of the subgraph of plateau moves.
- **Trap** = a plateau component containing no state with a +1 move.

---

## 1. Hub argument

Every backbite is its own inverse, so the move graph is undirected. If every
path reaches the serpentine S, then A → S → B reaches everything.

---

## 2. Proven

**Lemma B (S = L).** All moves decrease h ⟺ both endpoints locked.

- *S ⊆ L*: a non-locked endpoint has a free horizontal neighbour; the move
  through it has Δh ≥ 0. (Local.)
- *L ⊆ S*: planar separation. A locked head (r,0) with first step right has
  every vertical neighbour horizontally attached; otherwise the suffix from
  that neighbour to the locked tail is a curve separating cells that the path
  prefix must connect.

  *Case 1 (tail on right edge)*: Q = V→…→tail runs from the left boundary to
  the right boundary; w_{k−1} lies above Q, w1 below, and the prefix joins them
  without touching Q — impossible.

  *Case 2 (tail on left edge)*: Q ∪ (left-boundary segment) is a simple closed
  curve; w1 is outside it, w_{k−1} on it, and the prefix cannot reach it.

  *Polish*: state the planar-separation lemma once; check n = 2.

**Bond lemma.** Let `x` be a free neighbour of an endpoint `w` and `b` the cell
beyond (`b = 2x − w`). The arm through `x` has Δh = 0 iff `x–b ∈ E(P)`.
*Proof*: the move adds `w–x` and deletes the edge into `x`; both are parallel
iff that deleted edge is `x–b`.

**Move taxonomy.** Each backbite moves the acted-on endpoint by Manhattan
distance exactly 2, as `(±2,0)`, `(0,±2)` (straight, Δh = 0) or `(±1,±1)`
(turn, Δh = ±1). Hence each endpoint's colour `r+c mod 2` is preserved, so the
endpoint colour multiset is invariant.

---

## 3. The one remaining gap

> **Escape Lemma.** Every path with h < n(n−1) has a backbite sequence to a
> path at h+1.

```
U → one +1 move                                      [trivial]
P → its plateau component:
      contains a +1 state → walk to it               [component is finite]
      is a trap           → Shape: size ≤ 4          [D3 + Shape]
                          → local −1 escape          [local check]
L → one −1 move lands outside L → U or P             [Lemma C]
```

So the proof reduces to **D3 + Shape + two local escapes + Lemma C**.

---

## 4. D3 (the only load-bearing claim)

The older statements `head_deg ≥ 2 ⟹ non-trap` and
`total degree ≥ 2 ⟹ non-trap` are **FALSE** (144 and 24 counterexamples at
n = 6). Do not use them.

> **D3.** Every plateau component containing a vertex of **total plateau
> degree ≥ 3** has a +1 exit.

Verified with 0 violations at n = 4, 5, 6 (exhaustive). Total degree is
`head_deg + tail_deg`.

---

## 5. Shape (derived from D3)

If C is a trap, D3 forces every vertex of C to have total degree ≤ 2, so C is
a path or a cycle. Degree-1 vertices are `(1,0)`/`(0,1)` states; degree-2
vertices are `(1,1)`:

| form | degree pattern | size |
|---|---|---|
| isolated vertex | `(0,0)` | 1 — these are exactly L |
| single edge | `(1,0)` / `(0,1)` | 2 |
| cycle | `(1,1)` | 4 |

Open sub-case: `(2,0)` / `(0,2)` has total degree 2 and is **not** excluded by
D3; it must be ruled out separately.

---

## 6. The local escapes

- **Size-4**: `[−1, +1, +1]` works from all 96 states (n = 6).
- **Size-2**: 4–6 moves through a non-trap P state; profiles `[−1,+1,0,+1]`,
  `[−1,0,+1,+1]`, `[−1,+1,0,0,+1]`, `[−1,−1,0,+1,+1,+1]`.
- **L**: Lemma C — any −1 move leaves L; the result has a +1 move or is a
  size-2 trap state.

---

## 7. Data

**Traps, exhaustive:**

| n | components | sizes | total degrees inside |
|---|---|---|---|
| 4 | 14 | {1: 14} | {0: 14} |
| 5 | 168 | {1: 168} | {0: 168} |
| 6 | 4,620 | {1: 4,580, 2: 16, 4: 24} | {0: 4,580, 1: 32, 2: 96} |

Traps are isolated vertices only at n = 4, 5; degree-1 and degree-2 vertices
inside traps appear at n = 6. Trap shape is **not** stable in n.

**Detour length to h+1 (n = 6, all non-max states):**

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12–14 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 208,694 | 13,438 | 4,684 | 1,454 | 506 | 306 | 138 | 44 | 18 | 30 | 24 | 10 |

U = detour 1; P = detour ≥ 2; every L state has detour ≥ 3.

**L:** |L| = 16, 170, 4,582, 235,960 (n = 4..7); every non-max L path is
`(0,1)` or `(1,0)`; L is parity-independent.

---

## 8. Next steps

1. **Prove D3** — the only load-bearing claim.
2. **Rule out `(2,0)`/`(0,2)` in traps.**
3. **Prove the size-2 and size-4 escapes** (local flips).
4. **Prove Lemma C** (the −1 step out of L).
5. Hub argument ⇒ connectivity.

---

## 9. Rejected routes (do not retry)

- **Single-endpoint degree lemma** (`head_deg ≥ 2` ⟹ non-trap): false (144).
- **Total-degree-2 version** (⟹ non-trap): false (24).
- **Arm lemma / chase-based proof**: false as stated; the chase is not monotone
  in general (head cells repeat inside 14-cycles).
- **Boundary peeling / row-sweep induction**: the push works, but
  freeze-and-recurse fails — the fixed-head tail-move graph is disconnected
  (3×3: 4/8; 4×5: 129/160).
- **Serpentine-prefix potential**: more local maxima than h (n = 5: 2,915 vs
  296).

---

## 10. Files

- `results/parity_notes.md` — bond / parity / carrier side thread (not adopted).
- `results/horizontal_landscape.md` — h-landscape data.
- `results/cycle_flip_graph.md` — cycle-land is disconnected (isolated rings).
- `results/annealing_probe_n10.md` — SA experiments.
- `results/peak_viz/`, `p_viz/`, `trap_viz/` — drawings.
- `results/locked_cache/` — cached L (n = 6, 7).
- `scripts/locked_analysis.py`, `scripts/horizontal_analysis.py`.
- `run_tests.py` — tests.
