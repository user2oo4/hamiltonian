# Scratchpad: parity / carrier / bond ideas (open thread)

Status: **thinking in progress, nothing agreed.** Started 2026-11-02.
Purpose: park every idea so none get lost while the parity direction is
explored. Move things into `proof_strategy.md` only once they're settled.

---

## 0. Notation used in this file

- Grid n×n, path P as a vertex sequence; `E(P)` = set of its n²−1 edges.
- `h` = number of horizontal edges.
- A backbite at the head: pick a free neighbour `x` of the head `w1` at
  position k ≥ 2, add `w1–x`, delete `wk−1–wk`.
- Plateau arm = an arm with Δh = 0 (added and deleted edges have the same
  orientation).

---

## 1. The local condition (verified, believed true)

**Setup.** Head `w1 = (r,c)`, jump goes through free neighbour `x`, and the
cell beyond is `b` (`b = 2x − w1`, i.e. `x` is the midpoint of `w1,b`).
So the jump is `w1 → b`, passing over `x`.

**Statement.** The arm through `x` is a *plateau* iff the grid edge `x–b` is
in `E(P)`.

Why: the move adds `w1–x` and deletes the edge into `x`. Both are
`w1–x`-parallel, so Δh = 0 iff the deleted edge is parallel to `w1–x`, which
happens iff `x`'s path-predecessor is `b` — i.e. `x–b ∈ E(P)`.

**Verified** at n = 6 on all plateau arms (59,124 + 59,124 cases, 0
exceptions).

### 1b. Straight vs turn — the complete move taxonomy (verified)

Every **head** move has manhattan distance exactly 2, and there are exactly 8
possible displacements. n = 6, ~1.1M head moves:

| displacement | count each | kind | Δh |
|---|---|---|---|
| `(±2, 0)`, `(0, ±2)` | 59,124 | straight (4 dirs) | **0** (plateau) |
| `(±1, ±1)` | 201,264 | turn (4 combos) | **±1** |

Tail moves leave the head fixed at `(0,0)` (1,500,248 cases).

**Corollary — parity is preserved.** `dr + dc` is always even, so every
backbite preserves `(r+c) mod 2` of the moved endpoint. Straight moves keep
both `r mod 2` and `c mod 2`; turn moves flip both. Hence:

- The head is confined to the two parity classes with its own `r+c` parity.
- **Only straight moves are plateaus**, so the plateau chase never leaves a
  single `(r mod 2, c mod 2)` class, and never leaves a single line.

**Correction note.** An earlier measurement reported displacement `(0,1)`
(manhattan 1). That was a bug: for tail moves the new head is the *old tail*,
so pairing `p`'s head with `q`'s head measured head-to-tail distance. The
correct per-move table is the one above; manhattan distance is always 2.

### 1c. The endpoint-colour invariant (verified — constrains everything below)

A backbite moves only the endpoint it is applied at, and preserves that
endpoint's colour `r+c mod 2` (straight: keeps both parities; turn: flips
both). So the **multiset of endpoint colours is invariant**.

Verified at n = 4, 5, 6: **0 violations**.

| n | endpoint colour pairs realised |
|---|---|
| 4 | `(0,1)` and `(1,0)` only (276 each orientation) |
| 5 | `(0,0)` only — 8,648 paths, **no odd-head path exists** |
| 6 | `(0,1)` and `(1,0)` only |

**Consequence for the chase claims in §1b.** "The plateau chase never leaves
one `(r mod 2, c mod 2)` class" holds **per endpoint**: the head's class is
frozen while chasing the head. Switching to the tail moves to the tail's
class, which for even n is the complementary one. So the chase does alternate
parity classes — via the endpoint switch, not via any single move.

**Consequence for connectivity.** The move graph on *oriented* paths is
disconnected along this invariant (at least two components, one per colour
pair). The **undirected** graph is still connected because `P` and `P^R` are
the same vertex and reversing swaps the roles of the endpoints. Any algorithm
we build must therefore be stated with **both endpoints free and paths
unoriented**; no step is allowed to claim that a single move changes an
endpoint's colour.

Measured (for reference): restricting BFS to even-head paths, n = 4 gives
1/276 reachable, n = 6 gives 113,951/229,348. These are not components of the
real (undirected) move graph — they are artefacts of fixing an orientation.

---

## 2. The bond-count conservation (verified — this is the user's argument)

**Bond.** A bond `B = (e1, e2)` is a pair of consecutive collinear grid edges,
e.g. `e1 = (r,c)–(r,c+1)`, `e2 = (r,c+1)–(r,c+2)`.

**Quantity.** `x(B) = |{e1, e2} ∩ E(P)| ∈ {0,1,2}`.

**Claim (user).** A jump `(r,c) → (r,c+2)` along bond `B` requires `x(B) = 1`,
and leaves `x(B') = 1` for the neighbouring bond `B'` on the far side.

**Verified at n = 6:** every horizontal plateau arm has `x = 1` before and
`x = 1` after — 59,124 / 59,124, no exceptions. Vertical arms likewise
(59,124).

**Why `x = 2` is impossible.** `x` is a *free* neighbour of the head, and the
head is `x`'s other grid neighbour. So in the path, `x`'s path-degree can
only be 1 (if `x` is internal it would need degree 2 through two of
`e1, e2`, but `w1` is the head and not in the path interior). Hence at most
one of `e1, e2` is used, so `x ∈ {0,1}` — never 2.

**Why `x = 0` gives +1.** If `x–b ∉ E(P)`, the arm through `x` deletes a
perpendicular edge, so Δh = +1.

**Conclusion.** Three-way classification at every head:

```
look at the bond just beyond the free neighbour:
  x = 1  → jump (plateau)
  x = 0  → +1 move  (DONE)
  x = 2  → impossible
```

This makes the head chase a *deterministic automaton* driven by the used-edge
set.

---

## 3. Conservation is per-bond AND global — my earlier test was wrong

**Correct statement.** Every plateau move changes `E(P)` by exactly: remove
the used bond edge, add the new one. For every bond the move does not touch,
`x` is unchanged (trivial). For the bond it jumps along, `x` goes 1 → 1.
Therefore `x(B)` is conserved for every bond that isn't at the *endpoints* of
the jump.

**OPEN — must check.** The two bonds at the *endpoints* of a jump (the one
behind the head and the one ahead of the landing cell) have not been verified
yet. This is the one place conservation could break. **Do this before
committing to the lemma.**

**Why my earlier "not invariant" result was bogus.** I bucketed *used edges*
by the parity of their left/top endpoint, and a used edge moves class when
the carrier shifts. That measures something else. The bond-based quantity is
the right one and it is conserved.

---

## 4. The 4-subgrid picture — tried, and it does NOT give an induction

Idea: split the grid by `(r mod 2, c mod 2)` into 4 subgrids, and induct.

**Why it fails:**
- The **head** stays in its parity class: horizontal jumps change `c` by ±2,
  vertical jumps change `r` by ±2. So the head never leaves its class.
- The **carrier edge** does leave: after a jump, the carrier moves from
  `(r,c+1)–(r,c+2)` to `(r,c)–(r,c+1)`, whose endpoints have different
  `c mod 2`.
- So the conserved object moves between parity classes while the head does
  not. An induction on subgrids has nothing coherent to induct on.

**What to keep from this:** "head confined to its parity class" is a real and
useful fact; "4 independent subgrid problems" is not.

---

## 4b. OPEN THREAD: does the parity of n change the trap structure?

Observed 2026-11-02, unexplained. Traps, exhaustive:

| n | parity | trap components | sizes | total degrees inside traps |
|---|---|---|---|---|
| 4 | even | 14 | {1: 14} | {0: 14} |
| 5 | odd | 168 | {1: 168} | **{0: 168}** |
| 6 | even | 4,620 | {1: 4,580, 2: 16, 4: 24} | {0: 4,580, 1: 32, 2: 96} |

At n = 4 and n = 5 **every trap is an isolated vertex** (total degree 0) — the
strict peaks only. At n = 6, degree-1 and degree-2 vertices appear inside traps
for the first time (16 size-2, 24 size-4 components).

Hypothesis to test later: the size-2 / size-4 traps are tied to n being even,
and odd n may have traps of size 1 only. If so, the Shape lemma splits by
parity and the even case carries all the work. **Not checked at n = 7** (would
need sampling, since full enumeration is infeasible).

Related: D3 (`total degree ≥ 3 ⟹ non-trap`) held with 0 violations at n = 4, 5,
6. The weaker degree-≥2 version held at n = 4, 5 and failed at n = 6 — the same
n = 6 transition.

---

## 5. Head-only chase structure (measured data, n = 3..8)

Chase = plateau moves at the head only, never the exact inverse.

| n | states checked | stuck | cycles | cycle lengths | cycle has a +1 | every cycle state has +1 |
|---|---|---|---|---|---|---|
| 3 | 20 (all) | 20 | 0 | — | — | — |
| 4 | 276 (all) | 276 | 0 | — | — | — |
| 5 | 4,324 (all) | 4,324 | 0 | — | — | — |
| 6 | 229,348 (all) | 229,314 | **34** | 14 | 34/34 | **34/34** |
| 7 | 60,000 (sampled) | 59,965 | 35 | 14, 18, 20 | 35/35 | 35/35 |
| 8 | 40,000 (sampled) | 39,992 | 8 | 14, 18 | **8/8** | **0/8** |

Notes:
- Cycles first appear at n = 6; none for n ≤ 5 (exhaustive).
- **Every** cycle contains at least one state with a +1 move (n ≤ 8), but
  "every state on the cycle has +1" fails at n = 8. So the correct cycle
  escape statement is *"walk within the cycle to the +1 state"*, not
  *"any state works"*.
- Cycle head cells all lie in a single parity class; multiplicities along the
  cycle are (2,2,3,3,2,2) at n = 6 (length 14 = Σ multiplicity).
- Max chase length: n=4: 3, n=5: 5, n=6: 15, n=7: 29, n=8: 20.

**Within a cycle, returning to the same head CELL gives a DIFFERENT path**
(checked at n = 6: (3,1) visited 3 times, 3 distinct states). So the cycle is
a walk in a covering of the coarse lattice, not in the coarse lattice itself.

---

## 6. Head-only cycles vs the 2- and 4-cycles from the trap analysis

- The trap 2-cycle / 4-cycle are *pure inverse* structures: one flip and its
  inverse; or head-flip / tail-flip / head-back / tail-back.
- The 14-cycles above are **head-only** and length 14. They are NOT of the
  same species: they genuinely tour several coarse-lattice cells.
- The 2/4-cycles have both states at degree ≤ 1; the 14-cycles do not (they
  have states with several arms, at least one of which has +1).

---

## 7. Open questions to settle before writing anything up

1. **Endpoint bonds.** Verify per-bond conservation for the two bonds at the
   endpoints of a jump (see §3). If it holds, "bond conservation" is a clean
   lemma; if not, it must be stated only for bonds away from the head.
2. **What is monotonically decreasing?** The carrier slides; a candidate
   measure is "position of the carrier along the row". Does it strictly
   decrease under the no-reversal rule? (It should, on a single corridor.)
3. **Does the carrier-sliding picture survive vertical jumps?** A vertical
   jump moves the head to another row; the carrier is then in a new row's
   bond set. What is conserved across that transition?
4. **Does `x(B)` conservation give anything for the non-cycle case?** The
   non-cycle case ends at `x = 0` (= a +1 move) or at degree 1. Conservation
   might help prove the "+1 must appear" direction; unclear yet.
5. **Is there a genuine invariant over the whole path** (not per bond)? E.g.
   `Σ_B x(B) mod something`, or a weighted sum. Worth one experiment.
6. **n = 8 cycles**: do the multiplicities generalise as
   (coarse-lattice walk with covering degree 2/3)? Is there a formula for
   cycle length?

---

## 8. Ideas parked from earlier discussions (not yet adopted)

- Priority rule: horizontal plateau before vertical; chase head; on
  degree 1, switch to tail. Reaches +1 in 13,364 / 18,516 deg-≥2 P states at
  n = 6, stops in 5,152, cycles in 0 (with a vertical-run limit of 2).
- Alternating chase (head until deg 1, then tail): +1 in 34,699 / 34,832,
  stuck in 99, cycle in 34. All 133 failures are within 1 move of an h+1
  state.
- The single-arm "Arm lemma" is **false** (144 counterexamples at n = 6).
  Do not resurrect it in its original form.
- Degree lemma itself is **true** (34,832/34,832) but is a component-level
  fact, not a single-chase fact.

---

## 9. Files produced by this thread

Scripts were exploratory and live in `/tmp` (`bond_exact.py`,
`bond_parity.py`, `head_cycles.py`, `cycles_by_n.py`, `cycles_n7.py`,
`cycles_n8.py`, `cycle_return.py`). Promote to `scripts/` if the direction
survives.
