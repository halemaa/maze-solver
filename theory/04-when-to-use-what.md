# 4 — When to use what: a decision tree

A practical guide for picking the right traversal in interviews and
real systems. Not comprehensive — just the decisions that come up
over and over.

## The decision tree

```
Is the graph weighted (edges cost different amounts)?
│
├── YES — use Dijkstra (non-negative weights) or
│         Bellman-Ford (negative weights allowed)
│
└── NO — use BFS or DFS
        │
        Do you need the SHORTEST path (fewest edges)?
        │
        ├── YES — use BFS, always
        │
        └── NO — do you need to explore STRUCTURE?
                 (cycles, components, ordering, backtracking)
                │
                ├── YES — use DFS
                │
                └── NO — either works; pick by memory
                        │
                        Is the graph deep and narrow?
                        │
                        ├── YES — DFS uses less space
                        └── NO — BFS uses less space
```

## Common problem patterns and which traversal fits

### Shortest path in unweighted graph → BFS

- **Number of Islands** — use BFS or DFS to flood-fill each island;
  either works since we only count, not measure
- **Word Ladder** — fewest word transformations → BFS
- **Rotting Oranges** — minutes until all oranges rot → BFS, because
  "minutes" = edge distance
- **Shortest Path in Binary Matrix** → BFS, by definition
- **01 Matrix** (distance to nearest 0) → multi-source BFS from
  every 0 at once

**Giveaway language**: "shortest," "fewest," "minimum steps,"
"minimum moves," "level order."

### Structure / exploration → DFS

- **Course Schedule** — can all courses be taken given
  prerequisites? → DFS with cycle detection
- **Course Schedule II** — in what order? → DFS post-order =
  topological sort
- **Clone Graph** — walk every vertex and copy it → DFS
- **Number of Connected Components** — DFS from each unvisited
  vertex, counting starts
- **Validate Binary Search Tree** — DFS with min/max bounds
- **Word Search** — find a word by walking the grid → DFS with
  backtracking

**Giveaway language**: "detect cycle," "topological order,"
"connected components," "can you reach," "generate all paths,"
"backtrack."

### Weighted shortest path → Dijkstra

- **Network Delay Time** — signal reaches all nodes, when does
  the last one receive? → Dijkstra
- **Cheapest Flights Within K Stops** → modified Dijkstra or BFS
  with cost tracking
- **Path With Minimum Effort** → Dijkstra, "effort" is the weight

**Giveaway language**: "weighted," "cost," "distance" (with
non-uniform distances).

### Heuristic-guided shortest path → A\*

A\* = Dijkstra + a heuristic that estimates distance to the goal.
Used when:

- The graph is huge and you don't want to expand uniformly in
  every direction
- You have a sensible estimate of "how far is this cell from the
  goal?" (Manhattan distance, Euclidean distance, straight-line
  distance)

Common in: game AI, pathfinding in maps, puzzle solvers (15-puzzle,
Rubik's cube with pattern databases).

## Real systems — not just interview puzzles

### BFS in production

- **Web crawlers** often use BFS to stay close to the seed URL
  rather than diving deep into one site
- **Social networks** — "people you may know (friends of friends)"
  is BFS at depth 2
- **Network broadcast** — flood a packet outward from a source
- **Garbage collection** — mark-and-sweep marks reachable objects
  via BFS from roots

### DFS in production

- **Compilers** do DFS on the AST for codegen, optimisation, type
  checking
- **Build systems** (Make, Bazel, Gradle) topologically sort the
  dependency graph via DFS
- **Package managers** (npm, pip, apt) detect conflicting
  dependencies with DFS cycle detection
- **Filesystem walkers** (`os.walk`, `find`) are DFS by default

### Dijkstra and A\* in production

- **Google Maps, Waze, OpenStreetMap routing** — Dijkstra with
  graph preprocessing (Contraction Hierarchies, Highway
  Hierarchies) at scale
- **Network routing protocols** (OSPF, IS-IS) use Dijkstra to
  compute shortest-path trees
- **Game pathfinding** — A\* in almost every major game engine

## The interview heuristic

If the problem involves a grid, a graph, or a tree, the first
question I ask myself is:

> "Am I being asked for a **distance** or a **structure**?"

- Distance → BFS (or Dijkstra if weighted)
- Structure → DFS

That gets you to the right algorithm in 90% of cases in under 5
seconds.

## When the choice doesn't matter

Many problems can be solved with either BFS or DFS and nobody
cares which you pick:

- Counting connected components
- Flood fill
- Clone a graph
- Detect if a path exists (not the shortest one)

For these, pick whichever is more natural to write. Recursive DFS
is often shorter. Iterative BFS is often clearer.

## When to reach for something else entirely

- **Union-Find (Disjoint Set Union)** when you need to merge groups
  and query "are these two in the same group?" — much faster than
  BFS/DFS per query
- **Topological sort via Kahn's algorithm** (BFS variant) when you
  want the order itself, not the cycles-or-not answer
- **Tarjan's / Kosaraju's** for strongly connected components in
  directed graphs
- **Bidirectional BFS** when you know both start and end — searches
  from both ends and meets in the middle, cutting the search space
  roughly in half

Don't learn these all at once. They come up naturally once you've
done enough BFS/DFS problems.

## The honest meta-advice

You will see 200+ graph problems in interview prep. They almost all
reduce to **BFS or DFS with a small twist**. The twist is usually
one of:

- Count something during traversal
- Record something in the parent dict
- Check a condition before adding a neighbour
- Start from multiple sources at once
- Run the traversal in reverse

Once you can write BFS and DFS in your sleep, learning each new
problem is learning the twist, not the algorithm. That's why it's
worth building this maze from scratch — you internalise the
template so hard that it becomes muscle memory.

Then the twists are easy.
