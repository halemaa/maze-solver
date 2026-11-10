# The theory, in plain language

These notes sit next to the code so you can read the *why* separately
from the *how*. Each one is short, written as if explaining to a
friend who understands programming but hasn't touched graph theory
in years.

Read in this order:

1. [`01-grids-as-graphs.md`](01-grids-as-graphs.md) — what a graph
   actually is, and why a 2D grid is one in disguise
2. [`02-bfs-vs-dfs.md`](02-bfs-vs-dfs.md) — the one data-structure
   difference that creates two entirely different algorithms
3. [`03-big-o.md`](03-big-o.md) — how to analyse what the code
   above actually costs, with worked examples
4. [`04-when-to-use-what.md`](04-when-to-use-what.md) — a decision
   tree for picking the right traversal in an interview or a
   real system

The code in `../maze.py` is the lab where you can run everything
these notes describe. Change a seed, watch the path change, watch
the numbers in `benchmark.py` move.
