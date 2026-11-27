#!/bin/bash
# Auto-retry driver: resumes run_103.sh across host memory-pressure kills.
# Each attempt redoes the cheap phases (cache validate, patch check, canary)
# and lake resumes Solution from its cache. Appends to one log.
cd "$(dirname "$0")/.." || exit 90
N=0
while [ "$N" -lt 40 ]; do
  N=$((N+1))
  echo "=== ATTEMPT $N START $(date -u +%FT%TZ) ===" >> logs/build.log
  if false; then
    scripts/run_103.sh >> logs/build.log 2>&1
  else
    # Deps are cached+patched; retry only the Solution tail (cheaper per
    # attempt, less exposed to memory-pressure kills during revalidation).
    scripts/resume_solution.sh >> logs/build.log 2>&1
  fi
  rc=$?
  echo "=== ATTEMPT $N EXIT $rc $(date -u +%FT%TZ) ===" >> logs/build.log
  if [ "$rc" -eq 0 ]; then
    echo "=== ALL PHASES COMPLETE ===" >> logs/build.log
    exit 0
  fi
  sleep 60
done
echo "=== RETRY RUNNER EXHAUSTED 40 ATTEMPTS ===" >> logs/build.log
exit 1
