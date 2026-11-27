#!/bin/bash
# Resume-only driver: deps are materialized + cached + patched (proven by
# earlier full attempts); go straight to the Solution tail + axioms probe.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/workspace" || exit 90
# Footprint reduction: threads=2 was measured at 5.5-6.9 GB per worker and tripped
# a shared host's aggregate lean-RSS ceiling -> freeze -> SIGTERM -> "Lean exited
# with code 143" (exit 1). threads=1 keeps the footprint under the ceiling.
export LEAN_NUM_THREADS=1
# elan must be reachable when launched detached from a clean nohup environment.
export PATH="$HOME/.elan/bin:$PATH"
export ELAN_TOOLCHAIN=leanprover/lean4:v4.34.1

echo "=== RESUME-SOLUTION START $(date -u +%FT%TZ) ==="
# No jobs flag: Lake 5.0.0-src+5045d00 has none (`-j` is rejected: "unknown short
# option"); parallelism is core-count fixed. Footprint control is LEAN_NUM_THREADS=1
# above plus the cache-resuming retry loop.
#
# On a shared host, gate this build through your own admission control: serialise
# against other large builds, admit only when swap headroom allows, and treat an
# external SIGTERM (code 143) as a stolen attempt rather than a compile failure.
# Without admission, attempts start into an exhausted host and are SIGTERM'd early,
# burning retries without progress. See QRT_TRIAGE.md sections 2-3. Plain build
# below; add your own admission gate on a shared host.
lake build Solution
rc2=$?
echo "=== SOLUTION EXIT $rc2 $(date -u +%FT%TZ) ==="
if [ $rc2 -ne 0 ]; then exit $rc2; fi

echo "=== AXIOMS PROBE START ==="
lake env lean Axioms103.lean
rc3=$?
echo "=== AXIOMS EXIT $rc3 $(date -u +%FT%TZ) ==="
exit $rc3
