"""
Maze generation and solving — BFS vs DFS on a 2D grid.

A small, self-contained demonstration of two graph-traversal algorithms,
with no dependencies beyond the Python standard library.
"""

import random
from collections import deque


Cell = tuple[int, int]


def generate_maze(rows: int, cols: int, seed: int | None = None) -> list[list[str]]:
    """
    Build a maze using recursive backtracking.

    Returns a 2D grid where '#' is a wall and ' ' is a passage. The
    output grid has dimensions (2*rows + 1) x (2*cols + 1) — one row/col
    per cell plus the walls between and around them.
    """
    if seed is not None:
        random.seed(seed)

    h, w = 2 * rows + 1, 2 * cols + 1
    grid = [['#'] * w for _ in range(h)]

    # Iterative recursive-backtracking carve — uses an explicit stack
    # instead of Python recursion so it handles mazes of any size.
    visited = [[False] * cols for _ in range(rows)]
    stack = [(0, 0)]
    visited[0][0] = True
    grid[1][1] = ' '

    while stack:
        r, c = stack[-1]
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                neighbors.append((nr, nc, dr, dc))

        if not neighbors:
            stack.pop()  # dead end — backtrack
            continue

        nr, nc, dr, dc = random.choice(neighbors)
        grid[2 * nr + 1][2 * nc + 1] = ' '
        grid[2 * r + 1 + dr][2 * c + 1 + dc] = ' '   # knock down the wall
        visited[nr][nc] = True
        stack.append((nr, nc))
    # Open a few extra passages so there's more than one route — makes
    # the BFS-vs-DFS comparison interesting.
    for _ in range((rows * cols) // 20):
        r = random.randrange(1, h - 1)
        c = random.randrange(1, w - 1)
        if grid[r][c] == '#':
            grid[r][c] = ' '

    return grid


def _neighbors(grid: list[list[str]], r: int, c: int):
    """Yield walkable neighbors of (r, c)."""
    h, w = len(grid), len(grid[0])
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < h and 0 <= nc < w and grid[nr][nc] == ' ':
            yield nr, nc


def solve_bfs(grid, start: Cell, end: Cell):
    """
    Breadth-first search.

    Finds the shortest path by exploring outward in waves. Returns
    (path, visited) where `path` is a list of cells from start to end
    and `visited` is every cell BFS looked at.
    """
    queue = deque([start])
    visited = {start}
    parent: dict[Cell, Cell | None] = {start: None}

    while queue:
        cur = queue.popleft()
        if cur == end:
            break
        for nxt in _neighbors(grid, *cur):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = cur
                queue.append(nxt)

    return _reconstruct(parent, end), visited


def solve_dfs(grid, start: Cell, end: Cell):
    """
    Depth-first search (iterative).

    Dives deep along one branch before backtracking. Finds *a* path,
    not necessarily the shortest. Returns (path, visited).
    """
    stack = [start]
    visited = {start}
    parent: dict[Cell, Cell | None] = {start: None}

    while stack:
        cur = stack.pop()
        if cur == end:
            break
        for nxt in _neighbors(grid, *cur):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = cur
                stack.append(nxt)

    return _reconstruct(parent, end), visited


def _reconstruct(parent: dict[Cell, Cell | None], end: Cell) -> list[Cell]:
    """Walk the parent chain backwards from `end` to the start."""
    if end not in parent:
        return []  # unreachable
    path: list[Cell] = []
    node: Cell | None = end
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path


def render(grid, visited: set | None = None, path: list | None = None) -> str:
    """
    Render the grid as text.

    '#' = wall, ' ' = open cell, '·' = visited by the search,
    '*' = part of the final path.
    """
    visited = visited or set()
    path_set = set(path) if path else set()

    lines = []
    for r, row in enumerate(grid):
        buf = []
        for c, ch in enumerate(row):
            pos = (r, c)
            if pos in path_set:
                buf.append('*')
            elif pos in visited:
                buf.append('·')
            else:
                buf.append(ch)
        lines.append(''.join(buf))
    return '\n'.join(lines)
