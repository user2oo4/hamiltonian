# Annealing probe results — n = 10

## Setup

- **Grid:** 10×10 (N = 100 vertices, 99 edges per path)
- **Start path:** `random_backtracking_path(10, seed=101)`
- **Target path:** `random_backtracking_path(10, seed=202)`
- **Initial distance** start→target: **31** (31 of 99 edges differ)
- **Search:** simulated annealing over backbite moves, minimizing
  `edge_distance(current, target)`
- **Parameters:** `steps = 300000`, `restart_every = 500`, `T0 = 5.0`,
  `cooling = 0.99999`
- **Metric recorded:** distance after every *accepted* move (plus restart
  jumps)

Reproduce with:

```bash
python3 scripts/probe_annealing.py --n 10 --steps 300000 --restart 500 \
    --first-seed 11 --num-seeds 10
```

## Result table

```
seed |  ok   |   steps | final | peak |  peak@  | tail (last 40 accepted distances)
-----+-------+---------+-------+------+---------+------------------------------------------
 11  | True  |  149757 |   0   |   2  | 149753  | 7 8 9 9 9 8 9 10 11 10 9 8 9 8 9 8 8 7 8 7 8 8 7 8 7 7 7 6 5 4 5 4 3 2 1 2 1 2 1 0
 12  | True  |  179442 |   0   |   2  | 179434  | 7 7 7 6 7 8 7 6 5 6 7 6 5 4 5 6 5 4 5 4 5 6 5 6 7 6 5 4 3 2 1 2 1 2 1 2 1 2 1 0
 13  | True  |   66845 |   0   |   2  |  66843  | 21 22 21 20 19 20 19 18 18 19 19 20 21 22 21 22 23 23 24 25 24 23 24 23 24 23 22 23 22 21 22 23 24 23 22 23 1 2 1 0
 14  | True  |   96457 |   0   |   2  |  96454  | 1 2 1 2 3 4 5 4 5 6 5 4 3 4 5 4 3 4 5 6 5 4 3 4 3 4 3 4 5 4 3 4 3 2 1 2 1 2 1 0
 15  | True  |  186757 |   0   |   2  | 186751  | 5 5 4 5 5 5 5 6 7 6 7 6 5 6 7 8 8 8 8 9 9 9 9 9 9 9 9 8 7 8 7 6 5 4 3 2 1 2 1 0
 16  | True  |  206209 |   0   |   2  | 206206  | 4 3 3 3 4 3 4 4 5 4 3 4 5 5 6 5 6 7 6 5 6 5 6 7 7 8 7 8 7 6 5 4 3 2 1 2 1 2 1 0
 17  | False |  300000 |   2   |   3  | 300000  | 2 2 2 2 2 2 2 2 2 2 2 2 2 2 3 2 2 2 2 3 3 3 2 2 2 2 3 2 2 2 2 2 2 2 3 2 2 3 2 3
 18  | True  |  114700 |   0   |   4  | 114695  | 26 27 28 28 27 27 28 27 26 25 25 4 5 6 7 8 7 6 7 6 5 6 5 4 3 4 3 2 3 4 3 4 3 4 3 4 3 2 1 0
 19  | False |  300000 |   3   |   4  | 299794  | 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
 20  | True  |  156769 |   0   |   3  | 156761  | 7 6 7 8 9 8 7 6 7 6 7 8 9 10 9 8 9 8 9 10 9 8 7 8 7 6 7 6 5 4 3 2 3 2 1 2 3 2 1 0
```

**Success rate: 8/10.** Two runs froze: seed 17 at distance 2, seed 19 at
distance 3.

Column meanings:

- `ok` — whether the target was reached
- `steps` — moves used (300000 = budget exhausted, i.e. failure)
- `final` — best distance to target at the end (0 = success)
- `peak` — distance reached by the last *uphill* accepted move before the end
  (for successes: where the final descent started; for failures: the last
  climb before settling)
- `peak@` — step at which that uphill move happened
- `tail` — the last 40 accepted distances, reading left to right

## Observations

### 1. The last move before success is always from distance 1

A backbite move deletes one edge and adds one edge, so the distance to the
target can change by at most **±1 per move**. Reaching distance 0 therefore
always happens from distance 1. Every successful tail ends `... 2 1 0` or
`... 1 0`. This part is guaranteed; the interesting question is how the walk
gets into a *good* distance-1 state.

### 2. The final descent starts from a tiny peak

In every successful run, `peak` (the last uphill move before the end) is only
**2, 3, or 4**. The walk never needed to scramble far away right before
finishing — it needed to be in the right low-distance state.

### 3. Successful endgames bounce in the {1, 2} zone

Typical ending: `... 3 2 1 2 1 2 1 0`. The walk reaches distance 1, sometimes
gets kicked back to 2, returns to 1, and eventually finds a distance-1 state
that has a downhill move to 0. Not every distance-1 state has one — some are
themselves traps (all available backbites go back to 2).

### 4. Stuck runs are flat plateaus at distance 2 or 3

- Seed 17: froze at **distance 2** — the tail is almost all `2`s with an
  occasional `3`.
- Seed 19: froze at **distance 3** — 40 consecutive `3`s. Every available
  move from that state is neutral or uphill.

Traps are **state-specific, not distance-specific**: seeds 11, 15, and 20
pass straight through distance 3 with no plateau (`... 5 4 3 2 1 0`). Being at
distance 3 does not automatically mean being stuck.

### 5. Restarts act as teleports to the best state

Seed 13's tail contains the jump `... 22 23 1 2 1 0` — from distance 23 to 1
in one "step". That is a **restart**: the walk had earlier found a distance-1
state, wandered up to distance 25, and the restart teleported it back to that
promising state. Two moves later it finished. This is the main reason
`restart_every=500` works: it keeps re-exploring the promising low-distance
zone.

## Implications for improving the search

1. **Detect plateaus and force local scrambles.** When the distance hasn't
   improved for ~500 steps, take a few *random* (non-annealed) backbite
   moves to break out of distance-2/3 traps — a small, deliberate scramble.
2. **Keep a temperature floor.** Don't cool below roughly 0.3–0.5 for n=10,
   so a `d → d+1` move stays acceptably likely and traps can't freeze the
   walk.
3. **Keep an elite pool of low-distance states** instead of a single best,
   and on plateau teleport to a random one — a richer version of the current
   restart.

## Earlier example of a distance-3 trap

From a stuck run with different parameters, the frozen state differed from the
target in exactly 3 edges:

```
wrong (in stuck path, not target):   (6, 16), (7, 17), (13, 23)
missing (in target, not stuck path): (6, 7), (16, 17), (12, 13)
```

These form two small patches: a 2×2 square at rows 0–1 / cols 6–7 (stuck path
uses the two vertical sides, target uses the two horizontal sides) and a small
corner at (1,2)-(1,3)-(2,3). All 5 backbite moves available from that state
led to distances `[3, 4, 4, 4, 4]` — zero improving moves.
