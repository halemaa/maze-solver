# 3 — Big O, actually applied

Most Big O tutorials teach you a list of complexities to memorise.
That gets you through a multiple-choice question but not through a
whiteboard. The real skill is **reading your own code and saying
what it costs**, out loud, correctly.

This note walks through the maze code in `../maze.py` and derives
its complexity step by step. Once you've done this with real code,
you can do it with any code.

## The mental model

For every chunk of code, ask two questions:

1. **How many times does this run** as the input grows?
2. **How much extra memory does it allocate** as the input grows?

That's Big O. Nothing more mysterious than counting.

## The variables that matter

The maze is a grid of `rows × cols` logical cells. As a graph:

- `V` (vertices) = number of open cells ≈ `rows × cols`
- `E` (edges) = number of adjacencies between open cells
  ≤ `2 × rows × cols` (each cell has up to 4 neighbours, each
  edge counted twice)

In Big O we drop constants, so **both V and E are O(rows × cols)**.
I'll call this quantity `n` from here on.

## Walking through `solve_bfs`

```python
def solve_bfs(grid, start, end):
    queue = deque([start])        # (1)
    visited = {start}             # (2)
    parent = {start: None}        # (3)

    while queue:                  # (4)
        cur = queue.popleft()     # (5)
        if cur == end:
            break
        for nxt in _neighbors(grid, *cur):  # (6)
            if nxt not in visited:          # (7)
                visited.add(nxt)            # (8)
                parent[nxt] = cur           # (9)
                queue.append(nxt)           # (10)

    return _reconstruct(parent, end), visited
```

**Line (1)–(3): constant setup.** O(1).

**Line (4): the outer loop.** How many times does it run?

- Each cell is added to the queue at most once (we check `visited`
  before appending).
- Each cell is removed from the queue at most once.
- So the loop runs at most `n` times.

**Line (5): `popleft` on a deque.** O(1). Important detail — if
you used `list.pop(0)` instead, it would be O(n), making the whole
algorithm O(n²). This is why we use `deque`.

**Line (6): looping over neighbours.** Each cell has at most 4
neighbours. That's a constant — O(1) per iteration of the outer
loop, so O(n) in total summed across the whole run.

**Lines (7)–(10): `in` on a set, `add` to a set, `append` to a
deque, assigning to a dict.** Each O(1) average case.

**Total time:** O(n) outer iterations × O(1) work each + O(n)
neighbour work across the run = **O(n) = O(V + E)**.

**Total space:**
- `visited`: up to n entries → O(n)
- `parent`: up to n entries → O(n)
- `queue`: up to n entries at once → O(n)
- **Space: O(n)**

That's the full analysis. Nothing exotic, just counting.

## DFS is the same story

```python
def solve_dfs(grid, start, end):
    stack = [start]               # (1)
    visited = {start}
    parent = {start: None}

    while stack:
        cur = stack.pop()         # (2)
        ...
```

Line (2): `list.pop()` without an index pops the last element —
O(1). (Again, `pop(0)` would wreck this.)

Everything else is identical to BFS. **O(V + E) time, O(V) space.**

## `generate_maze` — nested work

```python
grid = [['#'] * w for _ in range(h)]      # (A)
visited = [[False] * cols for _ in range(rows)]  # (B)
stack = [(0, 0)]
while stack:                               # (C)
    r, c = stack[-1]
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # (D)
        ...
```

- (A) and (B): build 2D arrays of size `h × w` and `rows × cols`.
  O(n) each.
- (C) the carving loop: each cell enters the stack at most once
  and leaves at most once — O(n) iterations.
- (D) inside: 4 neighbours checked = O(1) per iteration.

**Time: O(n). Space: O(n).**

## `_reconstruct` — one path, not the whole graph

```python
while node is not None:
    path.append(node)
    node = parent[node]
path.reverse()
```

The path is at most `n` cells long. So this is O(n) time and O(n)
space.

## Putting it together

The whole program — generate + solve BFS + solve DFS + render — is
a sum of O(n) steps:

- Generate: O(n)
- BFS: O(n)
- DFS: O(n)
- Render: O(n) (we iterate every cell once)

**Overall: O(n), where n = rows × cols.**

The benchmark table in the README confirms this. Going from 100
cells to 6,400 cells (64×) raises runtime by roughly 60× — close
enough to linear once constant overhead (dictionary lookups,
function calls, output formatting) is accounted for.

## The common mistakes

### "It's O(n²) because of the nested loop in render"

The renderer has a nested loop — one over rows, one over columns.
It looks O(n²). But wait: **what is n?** If n is the number of
cells, the nested loop runs n times total, so it's O(n). If n is
the row count, then yes, it's O(n²) in terms of rows — which is
the same thing since columns also scale with rows.

**The lesson: define your n before analysing.** In graph problems,
n almost always means V + E, not the side length of the grid.

### "Python's `in` on a list is O(n), so my code is O(n²)"

Yes — `if x in my_list` is O(len(list)). If you do that inside a
loop over n items, you're at O(n²). This is why we use **sets and
dicts** in the maze code: `x in set` and `x in dict` are both O(1)
average case.

Any time you see `in` inside a loop, check what it's scanning. If
it's a list, you have a bug.

### "Recursive algorithms are always O(2ⁿ)"

Only if they make 2 recursive calls at each step without caching
results (think: naïve Fibonacci). Recursion by itself costs
nothing extra — a recursive BFS/DFS is still O(V + E).

The cost of recursion is **stack space proportional to depth**.
That's why the maze generator in this repo is iterative — a
recursive version blew Python's default recursion limit at 60×60.

### "Amortised constant means it's not really constant"

A `list.append(x)` in Python is **amortised O(1)**: usually O(1),
but occasionally O(n) when the underlying array has to grow. Over
many appends, the average cost is O(1).

Amortised analysis matters for interview questions like "what's
the complexity of building a list of n items with append?" The
answer is O(n), not O(n²), because the occasional O(n) growth
step averages out.

## How to say this in an interview

Don't just state the answer. **Narrate the derivation.**

> "Let n be the number of cells in the maze. The BFS loop runs
> at most once per cell, because I check the visited set before
> adding to the queue. Inside the loop I do constant work — a
> deque popleft, at most 4 neighbour checks, each a set lookup
> which is O(1) average. So time is O(n).
>
> For space, the visited set, the parent dict, and the queue
> each hold at most n cells, so space is O(n).
>
> In graph-theory terms that's O(V + E), which is the standard
> complexity for BFS."

That paragraph is the difference between "memorised the answer"
and "actually understands." It's two minutes of talking. Practice
it out loud.

## A tiny homework

Open `../benchmark.py` and look at the output. The BFS time
roughly doubles when cells quadruple. Does that confirm O(n), or
would you say it suggests O(n log n) or O(n²)? Why?

(Answer: linear scaling, confirming O(n). O(n²) would be 16× for
4× input. O(n log n) would be close to linear but noticeably
steeper. What we see is closest to linear.)
