# Cycle-land analysis: the 2-opt flip graph of Hamiltonian cycles

Experiment: for even n, enumerate all Hamiltonian cycles of the n×n grid,
then build the graph whose edges are **valid single-cycle 2-opt moves** (the
moves that would take a cycle to a *different* cycle while staying inside
cycle-land).  A backbite move on a closable path that stays closable is
exactly such a 2-opt.

Script: `scripts/cycle_flip_graph.py`

## Results

### n = 4

- Hamiltonian cycles: **6**
- Flip graph components: **6**, each of size 1
- Degree min / avg / max: **0 / 0 / 0**
- Isolated cycles: **all 6**

### n = 6

- Hamiltonian cycles: **1072** (matches the known value, OEIS A003763)
- Flip graph components: **1072**, each of size 1
- Degree min / avg / max: **0 / 0 / 0**
- Isolated cycles: **all 1072**

So the cycle-only flip graph has **zero edges**: no Hamiltonian cycle of the
4×4 or 6×6 grid can be transformed into a *different* Hamiltonian cycle by a
single valid 2-opt / cycle-preserving backbite move.

## Direct check on the path level

Opening any cycle into a closable path (a path whose endpoints are adjacent)
and enumerating its backbite moves:

- every closable path has **exactly 2** moves that stay closable — these are
  the two *rotations* (open the same cycle at the previous / next edge);
- every **other** backbite move leaves cycle-land (produces a path whose
  endpoints are not adjacent).

Verified for all 6×16 = 96 closable paths of n=4 and all 1072×36 = 38,592
closable paths of n=6: zero anomalies (always exactly 2 closable moves).

## Interpretation

Cycle-land has the following structure:

```
each Hamiltonian cycle  =  a ring of N closable paths
                           (connected to each other by rotation moves)

rings are ISOLATED: no move connects two different cycles
                    while staying inside cycle-land
```

Every "interesting" move (one that changes the cycle, or changes the path in
a non-trivial way) necessarily **leaves cycle-land**.  Since the full backbite
graph on all Hamiltonian paths is connected (276 paths for n=4, 229,348 for
n=6), the connectivity is carried entirely by the **non-closable paths** —
the "sea" between the cycle islands.

This reframes the constructive problem: a cycle is a rest stop, not a
workspace.  To change which cycle you're on, you must deliberately dive off
the ring into the sea of non-closable paths, navigate there, and climb back
onto a different ring.

## Why no 2-opt exists (structural reason)

In a grid, the only possible 2-opt move is a **unit-square flip**: replace
two opposite sides of a 2×2 cell with the other two sides.  Such a flip is a
valid single-cycle 2-opt only when the cycle traverses those two opposite
sides in the **same direction** (left-to-right on both top and bottom, or
equivalently top-to-bottom on both left and right).  Empirically, every
Hamiltonian cycle of the 4×4 and 6×6 grid traverses opposite sides of every
used unit square in opposite directions, so no flip is ever legal.

Whether this is a theorem for all even n is an open question worth
investigating — a parity/degree argument may prove it.

## Commands

```bash
python3 scripts/cycle_flip_graph.py --n 4 --show-isolated
python3 scripts/cycle_flip_graph.py --n 6
```
