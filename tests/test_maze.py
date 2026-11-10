"""Tests for the maze algorithms."""

from maze import generate_maze, solve_bfs, solve_dfs, _neighbors


def _ends(grid):
    h, w = len(grid), len(grid[0])
    return (1, 1), (h - 2, w - 2)


def test_maze_has_odd_dimensions():
    grid = generate_maze(5, 7, seed=1)
    assert len(grid) == 11       # 2*5 + 1
    assert len(grid[0]) == 15    # 2*7 + 1


def test_maze_borders_are_walls():
    grid = generate_maze(5, 7, seed=1)
    h, w = len(grid), len(grid[0])
    for c in range(w):
        assert grid[0][c] == '#'
        assert grid[h - 1][c] == '#'
    for r in range(h):
        assert grid[r][0] == '#'
        assert grid[r][w - 1] == '#'


def test_bfs_finds_shortest_path():
    """BFS's path must be at most as long as DFS's path, for any seed."""
    for seed in range(20):
        grid = generate_maze(8, 8, seed=seed)
        start, end = _ends(grid)
        bfs_path, _ = solve_bfs(grid, start, end)
        dfs_path, _ = solve_dfs(grid, start, end)
        assert len(bfs_path) <= len(dfs_path), (
            f"seed={seed}: BFS path ({len(bfs_path)}) was longer than "
            f"DFS path ({len(dfs_path)}) — BFS should always be optimal"
        )


def test_bfs_path_is_connected():
    """Every step in the BFS path must be a valid grid neighbor."""
    grid = generate_maze(10, 10, seed=3)
    start, end = _ends(grid)
    path, _ = solve_bfs(grid, start, end)
    assert path[0] == start
    assert path[-1] == end
    for a, b in zip(path, path[1:]):
        assert b in set(_neighbors(grid, *a)), f"{a} -> {b} is not adjacent"


def test_dfs_reaches_end():
    """DFS should still find the end, even if the path is suboptimal."""
    for seed in range(10):
        grid = generate_maze(6, 6, seed=seed)
        start, end = _ends(grid)
        path, _ = solve_dfs(grid, start, end)
        assert path[-1] == end
        assert path[0] == start


def test_unreachable_returns_empty_path():
    """If the end is a wall, there should be no path."""
    grid = generate_maze(5, 5, seed=0)
    start, end = _ends(grid)
    # Wall off the end cell's only neighbours
    h, w = len(grid), len(grid[0])
    grid[end[0] - 1][end[1]] = '#'
    grid[end[0]][end[1] - 1] = '#'
    grid[end[0] + 1][end[1]] = '#'
    grid[end[0]][end[1] + 1] = '#'
    path, _ = solve_bfs(grid, start, end)
    assert path == []
