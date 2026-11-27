#!/bin/bash
# QR baseline rebuild: Challenge canary (Mathlib-only; validates warm-cache
# traces) then Solution (full OAI closure). Bounded by external watchdog.
# Usage: run_build.sh [workspace-dir]   (default: $QR_WORKSPACE or <repo>/workspace)
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WS="${1:-${QR_WORKSPACE:-$ROOT/workspace}}"
cd "$WS" || exit 90
export LEAN_NUM_THREADS="${LEAN_NUM_THREADS:-4}"
echo "=== CHALLENGE START $(date -u +%FT%TZ) lake=$(lake --version 2>&1 | head -1) ==="
lake build Challenge
rc1=$?
echo "=== CHALLENGE EXIT $rc1 $(date -u +%FT%TZ) ==="
if [ $rc1 -ne 0 ]; then exit $rc1; fi
echo "=== SOLUTION START $(date -u +%FT%TZ) ==="
lake build Solution
rc2=$?
echo "=== SOLUTION EXIT $rc2 $(date -u +%FT%TZ) ==="
exit $rc2
