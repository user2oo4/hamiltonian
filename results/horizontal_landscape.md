# The horizontal-edge landscape (progress toward the serpentine)

## Objective

The serpentine path uses every **row (horizontal) edge** plus exactly n−1
vertical edges to jump between rows.  A natural first milestone for
"serpentine-ization" is:

```
h(path) = number of horizontal edges
max h  = n(n−1)
```

A path with h = n(n−1) is a **maximum-horizontal path**: every row is a full
left-to-right (or right-to-left) traversal, rows joined at the ends.  There
are exactly **2** such paths: the serpentine and its mirror.

A backbite move changes h by exactly **−1, 0, or +1** (deletes one edge, adds
one edge).

## Results (n = 4, 5, 6 exhaustive; n = 7 sampled)

| n | paths | max h | local maxima | strict peaks | escape hatch | two-cycle | max detour to h+1 | detour-length distribution |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 4 | 276 | 12 | 38 | 14 | 8 | 6 | 5 | {3:4, 4:6, 5:4} |
| 5 | 4,324 | 20 | 296 | 168 | 84 | 84 | 9 | {3:84, 4:20, 5:38, 6:18, 8:4, 9:4} |
| 6 | 229,348 | 30 | 20,652 | 4,580 | 2,762 | 1,818 | 12 | {3:2242, 4:1338, 5:470, 6:266, 7:138, 8:44, 9:18, 10:30, 11:24, 12:2} |
| 7* | 30,000 sampled | 42 | 1,300 | 262 | 171 | 91 | 10 | {3:170, 4:62, 5:17, 6:7, 7:3, 8:1, 10:2} |

Definitions:

- **local maximum**: no single move increases h.
- **strict peak**: every move *decreases* h (all moves go to h−1).
- **escape hatch**: from a strict peak, some downhill neighbour can move to a
  *different* h-state or to h+1.
- **two-cycle peak**: every downhill neighbour can only move back to the peak
  itself — needs a deeper detour.
- **detour length**: shortest number of moves to reach any state with h+1.

## Observations

1. **h-distribution is symmetric** around (N−1)/2 (transpose symmetry), with
   exactly 2 paths at max h and 2 at min h.
2. **Greedy "always increase h" fails** — there are strict peaks at every
   scale (14 / 168 / 4,580).
3. **But every strict peak escapes within a short bounded detour**:
   - n=4: ≤ 5 moves
   - n=5: ≤ 9 moves
   - n=6: ≤ 12 moves
   - n=7 (sample): ≤ 10 moves
   Most peaks escape in just 3–4 moves.  Detour length grows slowly with n
   (roughly ≤ 2n).
4. **Strict peaks are diverse** — distinct vertical-column patterns:
   13 (n=4), 141 (n=5), 3,997 (n=6).  The "single-twist snake" picture is
   too simple; there are many peak shapes.  So a proof should not rely on
   a full classification, only on the bounded-detour property.
5. For all strict peaks checked, a downhill neighbour can always move back up
   to ≥ h; but no downhill neighbour can jump straight to h+1 — the escape
   always goes sideways or via a second downhill step first.

## Example peak (n=4, h=10)

```
 4↓  3←  2←  1←
 5→  6↓ 15→ 16·
 8↓  7← 14↑ 13←
 9→ 10→ 11→ 12↑
```

Shortest detour profile: `[10, 9, 10, 10, 10, 11, 12]`.

## Endpoint characterization (exact, empirical for n ≤ 6)

The peaks are exactly the paths with **both endpoints locked**.  Define the
danger zone B:

```
endpoint is locked  :=  endpoint is a corner or a left/right-edge cell
                        AND the path's first/last edge is horizontal
                        (i.e. the endpoint's single horizontal neighbour
                         is already its neighbour in the path)
path ∈ B  :=  BOTH endpoints locked
```

Counts (exhaustive):

| n | paths in B | local maxima | strict peaks |
|---|---:|---:|---:|
| 4 | 14 | 14 | 14 |
| 5 | 168 | 168 | 168 |
| 6 | 4,580 | 4,580 | 4,580 |

So empirically: **B = local maxima = strict peaks**, exactly.  Every path in
B has *all* moves decreasing h; every path outside B has an improving move.

### Why strict peaks must lie in B (proved)

If an endpoint has a horizontal neighbour that is NOT adjacent to it in the
path, take the backbite that adds that horizontal edge.  It deletes some
edge, so Δh = +1 − [deleted edge horizontal] ∈ {0, +1} ≥ 0 — not a strict
peak.  Such a "free horizontal neighbour" exists whenever the endpoint is:

- an interior cell (2 horizontal neighbours, only one can be the path
  neighbour), or
- a top/bottom-edge cell (also 2 horizontal neighbours), or
- a corner / left-right-edge cell whose end-edge is vertical.

Therefore a strict peak's endpoints must be corners or left/right-edge cells
with horizontal end-edges — i.e. B.  (The converse — every path in B is a
strict peak — is verified exhaustively for n ≤ 6; a short case analysis
should prove it.)

This is exactly the "wrong place to start/end" intuition: the serpentine
starts and ends at corners with horizontal end-edges, and the trapped states
are precisely the paths whose endpoints are stuck on the left/right boundary
with their only horizontal move already used.

## Proof plan (updated)

1. **Potential**: h changes by exactly −1/0/+1 per move; max h = n(n−1).
2. **Lemma 1 (proved)**: any path outside B has a move with Δh ≥ 0.
   **Lemma 1′ (empirical)**: actually every path outside B has Δh = +1.
3. **Lemma 2 (empirical)**: every path in B is a strict peak, and from every
   B-path there is a path of at most ~2n moves to a state with h+1
   (the bounded detour).
4. **Induction**: while h < max: if outside B, take an improving move; if in
   B, run the bounded detour.  Total moves ≤ ~2n · n(n−1) = O(n³).
5. This yields a deterministic algorithm to a maximum-horizontal path
   (serpentine or its mirror); a final small step converts mirror →
   serpentine.  Combined with the hub argument (backbite moves are their own
   inverse), this proves the whole backbite graph is connected.

## The reduction to L (locked-endpoint set)

Since L is defined by simple endpoint conditions, it can be enumerated
**directly** with a constrained DFS — no need for the full path set.

| n | all paths | |L| (incl. the 2 max-h paths) | reduction |
|---|---:|---:|---|
| 4 | 276 | 16 | 5.8% |
| 5 | 4,324 | 170 | 3.9% |
| 6 | 229,348 | 4,582 | 2.0% |
| 7 | infeasible (likely 10M+) | **235,960** | — |

Cache: `results/locked_cache/locked_n6.pkl`, `locked_n7.pkl`.
Script: `scripts/locked_analysis.py`.

### Lemma B verified on the whole of L(7)

- |L(7)| = 235,960; 2 max-h paths + 235,958 candidates.
- **All 235,958 candidates are strict peaks** (every move decreases h):
  0 violations.
- **Down-then-up holds for all 235,958 peaks**: every downhill neighbour
  can immediately move back to ≥ h.
- Detour length to h+1 (sample of 500 peaks, depth ≤ 16): all found,
  `{3: 295, 4: 130, 5: 38, 6: 22, 7: 6, 8: 5, 9: 3, 12: 1}` — max 12,
  most 3–4.

So the equivalence **L = strict peaks** now holds exhaustively for
n = 4, 5, 6, 7.  Proving Lemmas A and B therefore reduces the connectivity
proof to the study of L, which is enumerable one or two sizes further than
the full path set.

## Open next steps

- Prove **Lemma A** (outside L ⟹ an improving move) — partially proved
  (Δh ≥ 0); the Δh = +1 strengthening is a small case analysis.
- Prove **Lemma B** (inside L ⟹ strict peak) — verified for all of L(4..7),
  needs a formal case analysis around a locked endpoint.
- Extract the actual detour **rule** from the BFS shortest paths (currently
  we only know the detours exist).  E.g. analyse the first move of shortest
  detours and test simple rules.
- Test the resulting deterministic algorithm on **every** path for n ≤ 6.

## Reproduce

```bash
python3 scripts/horizontal_analysis.py --n 4
python3 scripts/horizontal_analysis.py --n 5
python3 scripts/horizontal_analysis.py --n 6            # ~1-2 min
python3 scripts/horizontal_analysis.py --n 7 --sample 30000
```
