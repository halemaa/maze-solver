"""
Benchmark BFS vs DFS over many maze sizes.

Measures two things:
1. Path quality — how much longer is DFS's path than BFS's?
2. Time complexity — how does runtime scale with maze area?

Both algorithms are O(V + E) in theory. V and E both scale with
rows * cols, so we expect roughly linear scaling in the area.

Usage:
    python benchmark.py
"""

import time
import statistics
from maze import generate_maze, solve_bfs, solve_dfs


def bench_one(rows: int, cols: int, trials: int = 10) -> dict:
    bfs_times, dfs_times = [], []
    bfs_lens, dfs_lens = [], []

    for seed in range(trials):
        grid = generate_maze(rows, cols, seed=seed)
        h, w = len(grid), len(grid[0])
        start, end = (1, 1), (h - 2, w - 2)

        t0 = time.perf_counter()
        bp, _ = solve_bfs(grid, start, end)
        bfs_times.append(time.perf_counter() - t0)
        bfs_lens.append(len(bp))

        t0 = time.perf_counter()
        dp, _ = solve_dfs(grid, start, end)
        dfs_times.append(time.perf_counter() - t0)
        dfs_lens.append(len(dp))

    return {
        "cells": rows * cols,
        "bfs_ms": statistics.mean(bfs_times) * 1000,
        "dfs_ms": statistics.mean(dfs_times) * 1000,
        "bfs_path": statistics.mean(bfs_lens),
        "dfs_path": statistics.mean(dfs_lens),
    }


def main() -> None:
    sizes = [(10, 10), (20, 20), (40, 40), (60, 60), (80, 80)]

    print(f"{'Cells':>7}  {'BFS (ms)':>10}  {'DFS (ms)':>10}  "
          f"{'BFS path':>10}  {'DFS path':>10}  {'DFS/BFS':>8}")
    print("-" * 70)

    rows = []
    for r, c in sizes:
        res = bench_one(r, c, trials=5)
        rows.append(res)
        ratio = res["dfs_path"] / res["bfs_path"]
        print(f"{res['cells']:>7}  "
              f"{res['bfs_ms']:>10.2f}  "
              f"{res['dfs_ms']:>10.2f}  "
              f"{res['bfs_path']:>10.1f}  "
              f"{res['dfs_path']:>10.1f}  "
              f"{ratio:>7.2f}x")

    print()
    print("Takeaways")
    print("-" * 70)
    print("  * Both algorithms scale linearly with cells (O(V + E)).")
    print("  * BFS always finds the shortest path.")
    print("  * DFS finds *a* path, often much longer than optimal.")
    print("  * DFS can be faster (fewer cells visited) but the path is worse.")


if __name__ == "__main__":
    main()
