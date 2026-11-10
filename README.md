# Maze Solver — BFS vs DFS

A small, self-contained demonstration of two classic graph-traversal
algorithms on a 2D grid. Generates a maze with recursive backtracking
(iterative), solves it with both **breadth-first search** and
**depth-first search**, and shows you the difference.

```
BFS  ·  path length 117  ·  visited 253 cells
---------------------------------
#################################
#***#     #           *****#    #
###*##### # ###########*###*# ###
# #*#***#       *******#   #*#  #
# #*#*#*####### #*#######  #*#  #
# #***#***#   # #*#   # #  ***  #
# #######*# ### #*# # # #  #####
#       #*#     #*# # #     *****#
# ##### #*#######*# # ##########*#
# # #   #*****#*****#     #   # *#
# # # ########*#  ########*#  ###*
# #   #       #*#   #     *#    *#
# # ##### #####*#  ### #####   *##
# #       #   #*#      # #      *#
# ######### # #*###### # #####   *
#           #  ********#        *#
#################################
```

**Why this exists.** Anyone can memorise "BFS finds the shortest path."
Fewer people can show it on a real input. This repo makes it tangible —
you can see the paths, see how many cells each algorithm explored, and
change the maze to see the trade-off change with it.

## What's in the box

```
maze.py         # core: maze generation, BFS, DFS, rendering
example.py      # run both algorithms on one maze and print both paths
benchmark.py    # measure runtime and path quality across maze sizes
tests/          # pytest tests for the algorithms
theory/         # written notes — the "why" alongside the "how"
```

Pure Python 3.10+, standard library only.

## Read the theory

The code is the lab. The [`theory/`](theory/) folder is where the
*why* lives — short, plain-language notes on:

1. [Grids as graphs](theory/01-grids-as-graphs.md) — the reframe that
   unlocks every grid problem
2. [BFS vs DFS](theory/02-bfs-vs-dfs.md) — the one-line difference
   that creates two different algorithms
3. [Big O, actually applied](theory/03-big-o.md) — deriving the
   complexity of this code, line by line
4. [When to use what](theory/04-when-to-use-what.md) — a decision
   tree for interviews and real systems

## Run it

```bash
# See a maze solved by both algorithms, side by side
python example.py

# Larger maze, a specific random seed
python example.py --rows 15 --cols 30 --seed 42

# Run the benchmark across maze sizes
python benchmark.py

# Run the tests
pytest
```

## The point this repo makes

### 1. BFS always finds the shortest path. DFS doesn't.

BFS expands outward in waves, so the first time it reaches the exit,
it has arrived by the shortest possible route. DFS dives deep along
one branch before backing up, so it often reaches the exit through a
long, winding path that bears no resemblance to the shortest one.

**Measured on this repo's benchmark (6400-cell maze, mean of 5 runs):**

| Cells | BFS path | DFS path | DFS / BFS |
|------:|---------:|---------:|----------:|
| 100   | 66.6     | 83.0     | 1.25x     |
| 400   | 287.4    | 327.4    | 1.14x     |
| 1,600 | 453.0    | 881.8    | 1.95x     |
| 3,600 | 788.2    | 1,117.0  | 1.42x     |
| 6,400 | 979.0    | 2,118.6  | **2.16x** |

DFS's "shortcut" is often twice as long as the real shortest path.

### 2. DFS sometimes explores fewer cells. That's not a win if path quality matters.

| Cells | BFS visited | DFS visited |
|------:|------------:|------------:|
| 6,400 | ~6,000      | ~3,500      |

DFS visits fewer cells because it commits to a branch early. In this
maze it got lucky and headed towards the exit. In other mazes it gets
unlucky and heads the opposite way. **Faster-but-wrong is rarely a
win in pathfinding.**

### 3. Both algorithms are O(V + E) in time.

Every cell gets visited at most once (checked via a `visited` set).
Every edge gets traversed at most twice (once from each side). So:

- **Time: O(V + E)** — in a grid, V and E both scale with
  `rows * cols`, so the practical complexity is linear in the area.
- **Space: O(V)** — the visited set and the queue/stack both bound
  at the number of cells.

The benchmark table confirms: 100 → 6400 cells (64x) raises runtime
from ~0.1ms → ~14ms (~130x — close enough to linear given overhead).

### 4. The real difference is the data structure.

The two algorithms are the *same code* except for one line:

```python
# BFS uses a queue — FIFO, oldest cell explored first
queue = deque([start])
cur = queue.popleft()

# DFS uses a stack — LIFO, newest cell explored first
stack = [start]
cur = stack.pop()
```

That is the entire difference. Swap FIFO for LIFO and "find the
shortest path" becomes "wander until you arrive."

## When to use which

| You want... | Use |
|---|---|
| Shortest path in unweighted graph | **BFS** |
| Any path, memory-constrained | **DFS** (smaller frontier on tall/narrow graphs) |
| Topological sort / cycle detection | **DFS** |
| Level-by-level exploration (friends-of-friends) | **BFS** |
| Weighted shortest path | Dijkstra (BFS generalised) |
| Heuristic-guided shortest path | A\* (BFS + priority queue + heuristic) |

## Extending this

- Add **A\*** with Manhattan-distance heuristic. Compare path quality and cells visited against BFS on the same maze.
- Add **Dijkstra** by giving cells random traversal costs (mud, water, open ground).
- Generate mazes with **Kruskal's** or **Prim's** instead of recursive backtracking — you get a different distribution of corridors.
- Replace the ASCII renderer with a Pygame or Tkinter one so you can watch the search animate in real time.
