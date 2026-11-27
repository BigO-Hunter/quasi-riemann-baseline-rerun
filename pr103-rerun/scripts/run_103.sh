#!/bin/bash
# QR #103 rerun driver: materialize deps, patch PNTA/rellich (worker recipe),
# fetch Mathlib cache, Challenge canary, Solution build, axioms probe.
# Detached usage: nohup scripts/run_103.sh > logs/build.log 2>&1 &
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/workspace" || exit 90
export LEAN_NUM_THREADS=2
# LEAN_NUM_THREADS=2 (not the verifier worker's 4): on a shared host under memory
# pressure, host resource management may SIGTERM oversized lean builds; halving
# concurrent lean RSS keeps this build a good citizen. Thread count affects wall
# time only, not compilation results; disclosed in the receipt's tool-pins.json.

# Host sampler (1-min resolution; bounds wall-time claims only).
( while :; do
    printf '%s | %s | ' "$(date -u +%FT%TZ)" "$(uptime | sed 's/.*load averages*/load:/')"
    vm_stat | awk '/Pages free/ {printf "free=%dMB ", $3*4096/1048576}
                   /Swapins/ {printf "swapins=%s ", $3}'
    echo
    sleep 60
  done ) &
SAMPLER=$!
trap 'kill $SAMPLER 2>/dev/null' EXIT

echo "=== ENV $(date -u +%FT%TZ) host=$(hostname -s) arch=$(uname -m) ==="
lean --version; lake --version | head -1; elan show 2>/dev/null | head -3

echo "=== MATHLIB CACHE GET START $(date -u +%FT%TZ) ==="
if lake exe cache get; then
  echo "=== CACHE GET EXIT 0 ==="
else
  echo "=== CACHE GET FAILED (rc=$?) - darwin cache may be absent; " \
       "fallback: APFS-clone warm mathlib build per run notes ==="
  exit 91
fi

echo "=== PATCHES START ==="
P="$ROOT/patches"
for pkg in PrimeNumberTheoremAnd rellich-kondrachov; do
  d=".lake/packages/$pkg"
  if [ -d "$d" ]; then
    if git -C "$d" apply --reverse --check "$P/$pkg-lean4341.patch" 2>/dev/null; then
      echo "patch already applied: $pkg"
    else
      git -C "$d" apply "$P/$pkg-lean4341.patch" && echo "patched: $pkg" || exit 92
    fi
  else
    echo "MISSING package dir: $d"; exit 93
  fi
done
echo "=== PATCHES DONE ==="

echo "=== CHALLENGE START $(date -u +%FT%TZ) ==="
lake build Challenge
rc1=$?
echo "=== CHALLENGE EXIT $rc1 $(date -u +%FT%TZ) ==="
if [ $rc1 -ne 0 ]; then exit $rc1; fi

echo "=== SOLUTION START $(date -u +%FT%TZ) ==="
lake build Solution
rc2=$?
echo "=== SOLUTION EXIT $rc2 $(date -u +%FT%TZ) ==="
if [ $rc2 -ne 0 ]; then exit $rc2; fi

echo "=== AXIOMS PROBE START ==="
lake env lean Axioms103.lean
rc3=$?
echo "=== AXIOMS EXIT $rc3 $(date -u +%FT%TZ) ==="
exit $rc3
