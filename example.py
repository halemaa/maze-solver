"""
Run the maze generator, solve with BFS and DFS, print both solutions
side by side so you can see the difference in behaviour.

Usage:
    python example.py
    python example.py --rows 10 --cols 20
    python example.py --seed 42
"""

import argparse

from maze import generate_maze, render, solve_bfs, solve_dfs


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate and solve a maze.")
    parser.add_argument("--rows", type=int, default=12)
    parser.add_argument("--cols", type=int, default=24)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    grid = generate_maze(args.rows, args.cols, seed=args.seed)
    h, w = len(grid), len(grid[0])
    start = (1, 1)
    end = (h - 2, w - 2)

    print(f"Maze: {h}x{w}  ·  start {start}  ·  end {end}\n")

    print("Empty maze")
    print("-" * w)
    print(render(grid))
    print()

    bfs_path, bfs_visited = solve_bfs(grid, start, end)
    print(f"BFS  ·  path length {len(bfs_path)}  ·  visited {len(bfs_visited)} cells")
    print("-" * w)
    print(render(grid, bfs_visited, bfs_path))
    print()

    dfs_path, dfs_visited = solve_dfs(grid, start, end)
    print(f"DFS  ·  path length {len(dfs_path)}  ·  visited {len(dfs_visited)} cells")
    print("-" * w)
    print(render(grid, dfs_visited, dfs_path))
    print()

    print("Summary")
    print("-" * w)
    print(f"  BFS path: {len(bfs_path):4d} cells   (shortest guaranteed)")
    print(f"  DFS path: {len(dfs_path):4d} cells   (first found, not shortest)")
    print(f"  BFS explored {len(bfs_visited)} cells to find it")
    print(f"  DFS explored {len(dfs_visited)} cells to find it")


if __name__ == "__main__":
    main()
