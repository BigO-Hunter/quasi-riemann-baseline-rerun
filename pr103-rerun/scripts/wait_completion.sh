#!/bin/bash
# Block until logs/build.log shows the SOLUTION+AXIOMS outcome, then report.
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$ROOT/logs/build.log"
for i in $(seq 1 720); do   # 720 x 30s = 6h max
  if grep -q "=== ALL PHASES COMPLETE ===" "$LOG" 2>/dev/null; then
    echo "BUILD COMPLETE:"
    grep "' depends on axioms" "$LOG" | sort -u
    grep -E "=== (CHALLENGE|SOLUTION|AXIOMS) EXIT" "$LOG" | tail -3
    exit 0
  fi
  if grep -q "=== RETRY RUNNER EXHAUSTED" "$LOG" 2>/dev/null; then
    echo "RETRY RUNNER EXHAUSTED 40 ATTEMPTS. Last lines:"
    tail -20 "$LOG"
    exit 1
  fi
  # Track the retry RUNNER (not the per-attempt driver — it legitimately
  # pauses between attempts). Require 3 consecutive misses over ~90s.
  misses=0
  for j in 1 2 3; do
    pgrep -f "retry_runner" >/dev/null 2>&1 || misses=$((misses+1))
    [ "$misses" -ge 3 ] && break
    sleep 30
  done
  if [ "$misses" -ge 3 ]; then
    if ! grep -q "=== ALL PHASES COMPLETE ===" "$LOG" 2>/dev/null; then
      echo "RUNNER DIED (3 consecutive misses). Last lines:"
      tail -20 "$LOG"
      exit 2
    fi
  fi
  sleep 30
done
echo "WATCHER TIMED OUT (6h) — build still running"
grep -c "✔" "$LOG"
exit 3
