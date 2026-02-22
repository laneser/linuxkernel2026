#!/usr/bin/env python3
"""
analyze_bench.py — Parse and visualize list_sort benchmark results.

Usage:
    uv run python scripts/analyze_bench.py \\
        --vanilla results/vanilla.csv \\
        --patched results/patched.csv \\
        [--output results/]

Produces:
    - Comparison count bar chart (vanilla vs patched, grouped by pattern)
    - Speedup summary table (stdout)
    - Time comparison chart
"""

import argparse
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_csv(path: Path) -> pd.DataFrame:
    """Load benchmark CSV from dmesg output."""
    lines = path.read_text().strip().split("\n")
    # Skip header line if present
    data_lines = [l for l in lines if l and not l.startswith("pattern,")]
    records = []
    for line in data_lines:
        parts = line.strip().split(",")
        if len(parts) != 5:
            continue
        records.append(
            {
                "pattern": parts[0],
                "n": int(parts[1]),
                "iter": int(parts[2]),
                "comparisons": int(parts[3]),
                "time_ns": int(parts[4]),
            }
        )
    return pd.DataFrame(records)


def compute_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Compute mean and std for each (pattern, n) group."""
    grouped = df.groupby(["pattern", "n"]).agg(
        cmp_mean=("comparisons", "mean"),
        cmp_std=("comparisons", "std"),
        time_mean=("time_ns", "mean"),
        time_std=("time_ns", "std"),
    )
    return grouped.reset_index()


def theoretical_nlogn(n: int) -> float:
    """Theoretical n*log2(n) comparison count."""
    if n <= 1:
        return 0
    return n * math.log2(n)


def theoretical_nlogr(n: int, r: int) -> float:
    """Theoretical n*log2(r) comparison count."""
    if r <= 1:
        return n - 1  # single run, just traversal
    return n * math.log2(r)


# Expected run counts for each pattern
EXPECTED_RUNS = {
    "sorted": 1,
    "reverse": 1,
    "random": None,  # ~n/2, computed dynamically
    "partial_8": 8,
    "pipe_organ": 2,
    "push_front": 2,
}


def plot_comparisons(
    van: pd.DataFrame, pat: pd.DataFrame, output_dir: Path
) -> None:
    """Bar chart of comparison counts: vanilla vs patched."""
    patterns = van["pattern"].unique()

    for n_val in sorted(van["n"].unique()):
        fig, ax = plt.subplots(figsize=(10, 6))

        van_n = van[van["n"] == n_val].set_index("pattern")
        pat_n = pat[pat["n"] == n_val].set_index("pattern")

        x = np.arange(len(patterns))
        width = 0.35

        van_vals = [van_n.loc[p, "cmp_mean"] if p in van_n.index else 0 for p in patterns]
        pat_vals = [pat_n.loc[p, "cmp_mean"] if p in pat_n.index else 0 for p in patterns]
        van_err = [van_n.loc[p, "cmp_std"] if p in van_n.index else 0 for p in patterns]
        pat_err = [pat_n.loc[p, "cmp_std"] if p in pat_n.index else 0 for p in patterns]

        ax.bar(x - width / 2, van_vals, width, yerr=van_err, label="vanilla", capsize=3)
        ax.bar(x + width / 2, pat_vals, width, yerr=pat_err, label="patched", capsize=3)

        # Theoretical lines
        nlogn = theoretical_nlogn(n_val)
        ax.axhline(y=nlogn, color="gray", linestyle="--", alpha=0.5, label=f"n·log₂(n) = {nlogn:.0f}")

        ax.set_xlabel("Pattern")
        ax.set_ylabel("Comparisons")
        ax.set_title(f"Comparison Count: vanilla vs patched (n={n_val})")
        ax.set_xticks(x)
        ax.set_xticklabels(patterns, rotation=45, ha="right")
        ax.legend()
        ax.grid(axis="y", alpha=0.3)

        fig.tight_layout()
        fig.savefig(output_dir / f"comparisons_n{n_val}.png", dpi=150)
        plt.close(fig)
        print(f"  Saved comparisons_n{n_val}.png")


def plot_time(
    van: pd.DataFrame, pat: pd.DataFrame, output_dir: Path
) -> None:
    """Bar chart of wall-clock time."""
    patterns = van["pattern"].unique()

    for n_val in sorted(van["n"].unique()):
        fig, ax = plt.subplots(figsize=(10, 6))

        van_n = van[van["n"] == n_val].set_index("pattern")
        pat_n = pat[pat["n"] == n_val].set_index("pattern")

        x = np.arange(len(patterns))
        width = 0.35

        van_vals = [van_n.loc[p, "time_mean"] / 1000 if p in van_n.index else 0 for p in patterns]
        pat_vals = [pat_n.loc[p, "time_mean"] / 1000 if p in pat_n.index else 0 for p in patterns]

        ax.bar(x - width / 2, van_vals, width, label="vanilla", capsize=3)
        ax.bar(x + width / 2, pat_vals, width, label="patched", capsize=3)

        ax.set_xlabel("Pattern")
        ax.set_ylabel("Time (µs)")
        ax.set_title(f"Wall-clock Time: vanilla vs patched (n={n_val})")
        ax.set_xticks(x)
        ax.set_xticklabels(patterns, rotation=45, ha="right")
        ax.legend()
        ax.grid(axis="y", alpha=0.3)

        fig.tight_layout()
        fig.savefig(output_dir / f"time_n{n_val}.png", dpi=150)
        plt.close(fig)
        print(f"  Saved time_n{n_val}.png")


def print_speedup_table(van: pd.DataFrame, pat: pd.DataFrame) -> None:
    """Print a summary table of comparison reduction per pattern."""
    print("\n=== Speedup Summary (comparison count reduction) ===")
    print(f"{'pattern':<12} {'n':>6} {'vanilla':>12} {'patched':>12} {'reduction':>10} {'n·lg(n)':>10} {'n·lg(r)':>10}")
    print("-" * 74)

    for _, vrow in van.iterrows():
        p, n = vrow["pattern"], vrow["n"]
        prow = pat[(pat["pattern"] == p) & (pat["n"] == n)]
        if prow.empty:
            continue
        prow = prow.iloc[0]

        v_cmp = vrow["cmp_mean"]
        p_cmp = prow["cmp_mean"]
        reduction = (1 - p_cmp / v_cmp) * 100 if v_cmp > 0 else 0

        nlogn = theoretical_nlogn(n)

        r = EXPECTED_RUNS.get(p)
        if r is None:
            r = n // 2  # approximate for random
        nlogr = theoretical_nlogr(n, r)

        print(
            f"{p:<12} {n:>6} {v_cmp:>12.0f} {p_cmp:>12.0f} "
            f"{reduction:>9.1f}% {nlogn:>10.0f} {nlogr:>10.0f}"
        )


def main():
    parser = argparse.ArgumentParser(description="Analyze list_sort benchmark results")
    parser.add_argument("--vanilla", required=True, type=Path, help="Path to vanilla.csv")
    parser.add_argument("--patched", required=True, type=Path, help="Path to patched.csv")
    parser.add_argument("--output", type=Path, default=None, help="Output directory for charts")
    args = parser.parse_args()

    if args.output is None:
        args.output = args.vanilla.parent
    args.output.mkdir(parents=True, exist_ok=True)

    print("Loading data...")
    van_df = load_csv(args.vanilla)
    pat_df = load_csv(args.patched)

    print(f"  vanilla: {len(van_df)} rows")
    print(f"  patched: {len(pat_df)} rows")

    van_summary = compute_summary(van_df)
    pat_summary = compute_summary(pat_df)

    print("\nGenerating comparison charts...")
    plot_comparisons(van_summary, pat_summary, args.output)

    print("\nGenerating time charts...")
    plot_time(van_summary, pat_summary, args.output)

    print_speedup_table(van_summary, pat_summary)

    print(f"\nAll charts saved to {args.output}/")


if __name__ == "__main__":
    main()
