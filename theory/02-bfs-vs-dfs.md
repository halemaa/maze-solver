# 2 — BFS vs DFS: the one-line difference

## The claim

BFS and DFS are the *same algorithm* except for one line of code —
and that line is the difference between "find the shortest path"
and "find any path, probably a long one."

Let me show you.

## The shared skeleton

Both algorithms do the same four things in a loop:

1. Take a cell from a collection of cells-to-visit
2. If it's the goal, we're done
3. Add each of its unvisited neighbours to the collection
4. Mark the cell as visited

Written in Python, with the data structure left abstract:

```python
def traverse(grid, start, end):
    frontier = Collection([start])    # ← the one thing that differs
    visited = {start}
    parent = {start: None}

    while frontier:
        cur = frontier.take()         # ← and this
        if cur == end:
            break
        for nxt in neighbors(grid, cur):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = cur
                frontier.add(nxt)

    return reconstruct_path(parent, end)
```

The `Collection` is the only choice to make. The rest is boilerplate.

## The choice

**BFS uses a queue** — first in, first out (FIFO).

```python
from collections import deque
frontier = deque([start])
cur = frontier.popleft()   # oldest cell first
```

**DFS uses a stack** — last in, first out (LIFO).

```python
frontier = [start]
cur = frontier.pop()       # newest cell first
```

That's it. That's the entire difference.

## Why the data structure changes everything

Imagine standing at a cell with three unvisited neighbours — North,
East, South. You add all three to the frontier.

### BFS (queue)

You're going to visit N, then E, then S, in that order — the order
you added them. Before you dive deeper from any of them, their other
neighbours join the queue behind. So you explore **in layers**:

```
Step 1: visit start (layer 0)
Step 2: visit everything 1 step from start (layer 1)
Step 3: visit everything 2 steps from start (layer 2)
...
```

When BFS first reaches the end cell, it did so from layer `k`. No
cell in a lower layer touched the end. So no shorter path exists.
**BFS is optimal by construction.**

### DFS (stack)

You added N, E, S to the stack. The next cell you visit is S (newest
on the stack). From S you add more cells, and the newest of *those*
gets visited next. You dive deep down one branch — N and E sit on
the stack, forgotten — until you hit a dead end. Only then do you
back up to N and E.

So DFS's path to the end depends entirely on *which direction it
explored first*. It might be going the wrong way for 500 steps
before it stumbles into the exit from the long side.

**DFS finds a path. BFS finds the shortest one.**

## A picture of the behaviour

Suppose we have a tiny graph:

```
      start
      /  |  \
     A   B   C
    /|   |
   D E   F
         |
        end
```

**BFS order:** `start, A, B, C, D, E, F, end`
**DFS order (if children processed left-to-right from the stack):** `start, C, B, F, end`

Different orders — but notice:
- BFS visits more cells before finding `end`
- DFS gets there faster, *in this particular example*

That's the trade-off. On this tiny graph DFS looks like the winner.
On the full maze it's often not — its path can be 2× longer, and
sometimes it visits most of the graph trying to backtrack out of a
blind alley.

## The complexity

Both BFS and DFS visit every vertex at most once (the `visited` set
sees to that). For each vertex, we scan its neighbours — in total
across the whole run, that's each edge considered at most twice
(once from each side).

- **Time: O(V + E)** — linear in the size of the graph
- **Space: O(V)** — the `visited` set, plus the frontier, each
  bounded by the number of vertices

BFS and DFS have the **same asymptotic complexity**. Choosing one
over the other is about *behaviour*, not speed.

## Where DFS wins on space

In a very deep, narrow graph (think: a tree where every node has
one child), the frontier only holds a few things at a time —
whatever's on the current path downward. DFS's space usage is
proportional to the *depth*, not the *size*.

BFS in the same shape must hold an entire layer at once. If the
graph is wide (every node has many children), that layer can be
huge.

Rule of thumb:
- **Tall and narrow?** DFS uses less memory.
- **Wide and shallow?** BFS uses less memory.
- **Mixed?** Space is comparable; pick based on what answer you need.

## Why you'd use DFS even when BFS exists

DFS is the right tool when the problem is **structural, not
distance-based**:

- **Cycle detection** — are there any loops in this dependency
  graph? DFS with a "currently being explored" set catches cycles
  naturally.
- **Topological sort** — in what order can we build these packages
  so every dependency is built first? DFS gives you the answer in
  post-order.
- **Connected components** — how many separate islands are there?
  Loop over vertices, DFS from each unvisited one, count.
- **Backtracking** — generate all valid configurations (n-queens,
  sudoku, permutations). DFS *is* backtracking.
- **Deeply nested JSON walking** — the structure is a tree, you
  want to see leaves; DFS visits leaves naturally.

BFS is the right tool when the problem is **about distance**:

- Shortest path in an unweighted graph
- Minimum number of moves (chess knight to a square, word ladder)
- "How many hops from me to this person?"
- Level-order processing (tree level by level)

## The short answer for interviews

> "BFS and DFS have the same O(V + E) complexity. I use BFS when
> I need the shortest path in an unweighted graph or when I'm
> exploring level by level. I use DFS when I need to explore
> structure — detecting cycles, topological sorting, counting
> components, or doing backtracking search."

That one sentence covers 90% of what you'll ever be asked.
