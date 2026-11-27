#!/bin/bash
# Resume-only driver: deps are materialized + cached + patched (proven by
# earlier full attempts); go straight to the Solution tail + axioms probe.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/workspace" || exit 90
# Footprint reduction: threads=2 was measured at 5.5-6.9 GB per worker and tripped
# the host's 16384 MB aggregate lean-RSS ceiling shared with peer campaigns ->
# freeze -> SIGTERM -> "Lean exited with code 143" (exit 1).
export LEAN_NUM_THREADS=1
# elan must be reachable when launched detached from a clean nohup environment.
export PATH="$HOME/.elan/bin:$PATH"
export ELAN_TOOLCHAIN=leanprover/lean4:v4.34.1

echo "=== RESUME-SOLUTION START $(date -u +%FT%TZ) ==="
# No jobs flag: Lake 5.0.0-src+5045d00 has none (`-j` is rejected: "unknown short
# option"); parallelism is core-count fixed. Footprint control is LEAN_NUM_THREADS=1
# above plus the cache-resuming retry loop.
#
# The original run gated this build through a host-wide build arbiter (internal
# tooling, not published here): host-wide flock serialisation, visible denial, swap
# admission, and 143 reported as STOLEN (signal) rather than as a build failure.
# Measured 2026-11-06: this host ran 4 concurrent Lean campaigns (one sibling forked
# 20 `lean` processes) and swap sat at 15.0/16.4 GB (~92%); without admission every
# attempt started into an exhausted host and was SIGTERM'd ~70 s in (exit 143), so
# attempts burned without progress. Swap admission was calibrated to 95% (an 85%
# default would deadlock at the measured steady state). See QRT_TRIAGE.md sections
# 2-3. Plain build below; add your own admission gate on a shared host.
lake build Solution
rc2=$?
echo "=== SOLUTION EXIT $rc2 $(date -u +%FT%TZ) ==="
if [ $rc2 -ne 0 ]; then exit $rc2; fi

echo "=== AXIOMS PROBE START ==="
lake env lean Axioms103.lean
rc3=$?
echo "=== AXIOMS EXIT $rc3 $(date -u +%FT%TZ) ==="
exit $rc3
