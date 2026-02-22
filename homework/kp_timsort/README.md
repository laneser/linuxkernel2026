# kp_timsort — Livepatch Module for list_sort Natural Run Detection

Kernel livepatch module that replaces `list_sort()` with a version that
detects naturally ascending runs in the input, achieving O(n log r)
comparisons where r is the number of runs (vs. the original's O(n log n)
regardless of input order).

## Motivation

The kernel's `lib/list_sort.c` is a bottom-up merge sort that processes
elements one at a time.  It ignores any pre-existing order in the input.
Many kernel callers sort lists that are partially ordered (e.g., inode
lists sorted by creation time, block I/O requests by sector number),
wasting comparisons on already-sorted subsequences.

This module adds **natural run detection** — scanning for maximal
ascending subsequences and merging them as units rather than individual
elements.  The merge scheduling logic (the bit-counting scheme) is
preserved from the original; only the input feeding phase changes.

## Architecture

```
kp_timsort_main.c    Livepatch registration (klp_enable_patch)
kp_timsort_sort.c    klp_list_sort() + copied merge()/merge_final()
kp_timsort_stats.c   debugfs instrumentation
```

The module uses kernel livepatch (`CONFIG_LIVEPATCH`) to transparently
replace the `list_sort` symbol in vmlinux.  No kernel recompilation
needed — `insmod` activates the patch, `rmmod` reverts it.

### Why copy merge() / merge_final()?

These functions are `static` in `lib/list_sort.c` and not exported.
Livepatch can only replace exported/global functions.  Following
livepatch convention, we copy them into the module with a `klp_` prefix
so they are distinguishable in stack traces.

## Prerequisites

The target kernel must have:
- `CONFIG_LIVEPATCH=y`
- `CONFIG_DYNAMIC_FTRACE=y`
- `CONFIG_DEBUG_FS=y` (for instrumentation)

## Build

```bash
make -C /lib/modules/$(uname -r)/build M=$PWD modules
```

## Usage

```bash
# Load — list_sort() is immediately patched
sudo insmod kp_timsort.ko

# Verify livepatch is active
cat /sys/kernel/livepatch/kp_timsort/enabled   # should be 1

# View sorting statistics
cat /sys/kernel/debug/kp_timsort/stats

# Reset counters
echo 1 > /sys/kernel/debug/kp_timsort/reset

# Generate sorting workload (e.g., directory listing triggers list_sort)
ls -la /usr/lib/

# Check updated stats
cat /sys/kernel/debug/kp_timsort/stats

# Disable livepatch (revert to original list_sort)
echo 0 > /sys/kernel/livepatch/kp_timsort/enabled

# Unload module
sudo rmmod kp_timsort
```

## debugfs Interface

| File    | Mode | Description |
|---------|------|-------------|
| `stats` | r    | Sorting statistics: call count, total/avg elements, runs, comparisons |
| `reset` | w    | Write anything to clear all counters |

### Stats output example

```
call_count:       42
total_elements:   15360
total_runs:       890
total_comparisons:51200
already_sorted:   5
avg_elements:     365
avg_runs:         21
avg_comparisons:  1219
```

Key metric: **avg_runs / avg_elements** indicates how ordered typical
inputs are.  A ratio close to 1/avg_elements means nearly sorted; close
to 1 means random.

## Comparison Counting

Comparisons are counted via a thin wrapper around the caller's `cmp`
function.  This adds ~10ns per comparison (one indirect call) — acceptable
for research but removable for a production patch.  The wrapper also counts
the periodic `cmp(b, b)` calls in `merge_final()` that exist for
`cond_resched()` support.

## Research Method

1. Load module on a system running real workloads
2. Collect stats over a representative period
3. Compare avg_comparisons with the theoretical O(n log n) baseline
4. Analyze run distribution to characterize kernel sorting patterns
5. Use findings to justify (or not) an upstream patch

## License

GPL-2.0 — derived from `lib/list_sort.c` in the Linux kernel.
