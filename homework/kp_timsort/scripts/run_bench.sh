#!/usr/bin/env bash
# run_bench.sh — Automate A/B benchmark on lab-x86
#
# Usage:
#   ./run_bench.sh <kernel-src-dir> <label>
#
# Example:
#   ./run_bench.sh /tmp/linux-6.12 vanilla
#   ./run_bench.sh /tmp/linux-6.12 patched
#
# The script:
#   1. Compiles the bench_list_sort module against the given kernel tree
#   2. Copies it to lab-x86
#   3. Loads it and captures dmesg output
#   4. Saves results to ../results/<label>.csv

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BENCH_DIR="${SCRIPT_DIR}/../bench"
RESULTS_DIR="${SCRIPT_DIR}/../results"
REMOTE="lab-x86"

if [ $# -lt 2 ]; then
    echo "Usage: $0 <kernel-src-dir> <label>"
    echo "  kernel-src-dir: path to compiled kernel source (e.g., /tmp/linux-6.12)"
    echo "  label: tag for results file (e.g., vanilla, patched)"
    exit 1
fi

KSRC="$1"
LABEL="$2"

mkdir -p "${RESULTS_DIR}"

echo "=== Building bench_list_sort.ko against ${KSRC} ==="
make -C "${KSRC}" M="${BENCH_DIR}" modules

if [ ! -f "${BENCH_DIR}/bench_list_sort.ko" ]; then
    echo "ERROR: bench_list_sort.ko not found after build"
    exit 1
fi

echo "=== Copying module to ${REMOTE} ==="
scp "${BENCH_DIR}/bench_list_sort.ko" "${REMOTE}:~/bench_list_sort.ko"

echo "=== Clearing dmesg and loading module on ${REMOTE} ==="
ssh "${REMOTE}" 'sudo dmesg -C'

# insmod returns non-zero because the module returns -EAGAIN
ssh "${REMOTE}" 'sudo insmod ~/bench_list_sort.ko' || true

# Wait a moment for all output to flush
sleep 2

echo "=== Collecting results ==="
OUTPUT="${RESULTS_DIR}/${LABEL}.csv"
ssh "${REMOTE}" 'dmesg | grep "^.*bench_list_sort:"' | \
    sed 's/.*bench_list_sort: //' > "${OUTPUT}"

LINES=$(wc -l < "${OUTPUT}")
echo "=== Saved ${LINES} lines to ${OUTPUT} ==="

echo "=== Done (${LABEL}) ==="
