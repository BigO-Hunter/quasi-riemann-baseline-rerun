# QRT_TRIAGE.md — PR #103 build-tail failure, 2026-11-06

> **Provenance note.** This is the public version of the triage record. Internal
> process-management provenance has been removed or generalized. All mathematical
> and build-engineering content is preserved unchanged.

## 1. Exact failure

Last build log lines before death:

```
✖ [13507/13520] Building Submissions.arvi_selected_leaf.JointDetector.NaturalCellSectorNorm (2.1s)
error: Lean exited with code 143
Some required targets logged failures:
- Submissions.arvi_selected_leaf.JointDetector.NaturalCellSectorNorm
error: build failed
=== SOLUTION EXIT 1 2026-11-06T15:45:32Z ===
```

**`code 143` = 128 + 15 = SIGTERM.** Not a Lean compile error: the module
(`Submissions/arvi_selected_leaf/JointDetector/NaturalCellSectorNorm.lean`, 248 lines)
was mid-elaboration and emitted no `error:` of its own. Disk is fine (172 GB free);
`.lake/packages` is intact (the build log's `LEAN_PATH` resolves all 16 packages and
~13,500 modules replay from cache), so this is neither the missing-package rebuild class
nor a banked-Lean-landmine parse error.

### Difference from the earlier deaths (correcting the brief's premise)

Earlier deaths were **whole-build** SIGTERM (`SOLUTION EXIT 143`, lake itself the victim).
Here `lake` survived and one **child `lean`** was killed, so lake reported per-target
failure and exited **1**. Same class, different victim scope — not a new failure mode.

### Who signalled — proven for the original failure

The host ran a memory-pressure manager enforcing an **aggregate host-wide lean-RSS
ceiling of 16384 MB**, shared with concurrent Lean builds. Host resource-management
records show two freeze events against our build tree on the day of the failure:

```
2026-11-06T12:24:02Z  freeze (SIGSTOP): lean tree 16776 MB, over the 16384 MB ceiling
2026-11-06T14:03:44Z  freeze (SIGSTOP): lean tree 16477 MB, over the 16384 MB ceiling
```

The manager picks the top-RSS lean/lake victim, **freezes it (SIGSTOP)**, then resolves
the freeze within its TTL — SIGTERM under sustained pressure.

The 16384 MB ceiling is **aggregate host-wide**, shared with concurrent builds. Measured
concurrently: one build compiling a large Lean module at 5.5–6.9 GB, another forking
**20** `lean` processes, and a third staging loop — four Lean builds on one host, swap
at **15.0/16.4 GB (92%)**. Our own workers ran at `LEAN_NUM_THREADS=2` (3.7–5.8 GB each),
so the tree crossed 16 GB and our module became the freeze victim.

## 2. Defects found and fixed in the recovery drivers

1. **`scripts/resume_solution.sh` exported `LEAN_NUM_THREADS=2`**, overriding the retry
   loop's `=1`. The stated footprint reduction was never in effect. → `=1`.
2. **The retry driver could never detect success.** It decided green by
   `tail -5 | grep -qiE "green|complete|BUILD_OK|success"` — words `resume_solution.sh`
   never prints. It would burn all 15 attempts and print `GAVE_UP` *even after a green
   build*. → replaced with exit-code detection (`rc==0` covers both `SOLUTION EXIT 0`
   and `AXIOMS EXIT 0`).
3. **The loop was not detached.** `nohup` alone did not survive the parent session's
   process-group cleanup; the log was silent 07:45→12:09 local (~4 h) with no
   `GAVE_UP`, which is why the tail looked abandoned. → launched detached
   (`subprocess.Popen(..., start_new_session=True)`) and verified to survive across
   tool calls.
4. **Attempts were consuming themselves into a saturated host.** Retries died ~70 s in,
   after ~60 s of cache validation, so almost no real work landed per attempt. →
   each attempt now goes through host-wide admission control: serialisation against
   other large builds, visible admission/denial, swap admission, and SIGTERM reported
   as a stolen attempt rather than as a build failure.

Tried and **reverted**: `lake build Solution -j2`. Lake 5.0.0-src+5045d00 rejects it
(`error: unknown short option '-j'`) and exposes no jobs knob at all. Parallelism is
core-count fixed; footprint control is `LEAN_NUM_THREADS=1` plus arbitration.

## 3. Fix applied

`scripts/resume_solution.sh`:
```bash
export LEAN_NUM_THREADS=1                 # was 2 (measured 3.7-5.8 GB/worker)
export PATH="$HOME/.elan/bin:$PATH"       # elan reachable from a detached clean env
export ELAN_TOOLCHAIN=leanprover/lean4:v4.34.1
lake build Solution                       # original run gated this through
                                          # host-wide admission control (see §2.4)
```

Swap admission was calibrated to measurement: the host sat at 92% swap with concurrent
builds grinding, so an 85% default (and even 90%) would deadlock the build forever.
95% still refuses at true critical but permits the measured steady state.

The retry driver — time-bounded (8 h) rather than count-bounded, exit-code green
detection, admission refusals do **not** consume an attempt, 20 s backoff. Launched
detached; output appended to the retry log.

One orphan was cleaned up: a pre-restart `bash scripts/resume_solution.sh` child
survived the pattern-based cleanup of the old retry driver and contended for the
admission lock; it and its child were terminated so exactly one build runs.

## 4. Evidence — the tail is converging

| Point in time | `[built/total]` | Remaining |
|---|---|---|
| Build death (15:45:32Z) | `13507/13520` | 13 |
| First re-armed attempt | `13140/13150` | 10 |
| After arbiter gating (20:38Z) | `13144/13150` | **6** |

Modules banked during this rerun, each previously a kill victim:

```
⚠ [13140/13150] Built ...NaturalCellSectorNorm (57s)   <- THE original failing module
ℹ [13141/13150] Built ...NaturalUniformNear (33s)
✔ [13142/13150] Built ...R1.Main (40s)
✔ [13143/13150] Built ...R1.Final (64s)
⚠ [13144/13150] Built ...R1.Body (67s)
```

`NaturalCellSectorNorm` — the module whose SIGTERM opened this lane — now **builds**.
Each retry resumes from cache and banks the modules the previous attempt completed, which
is why the remaining count falls monotonically despite recurring kills.

## 5. Honest limit of the attribution

The kills that continue during retries are **not** fully attributed. Established:

* The host's lean-RSS manager was reconfigured to a higher per-tree ceiling
  (24576 MB) and reported no kills or freezes in its recent cycles, so it is not
  killing the retries.
* The host's test-process monitor only SIGTERMs `python -m pytest` hogs, never lake.
* The arbiter's flock does not stop the killer, so it is not an arbiter peer.
* A signed process faked as argv[0] `lean` survived 100 s, so it is not a name-pattern
  reaper — the killer selects **top-RSS** lean processes, consistent with the host's
  memory-pressure manager class, but this is **not proven per-process** for the
  retry-phase kills (the raw signal path bypassed the kill log for the attempt-2
  victim).

An earlier `pkill -f "lake build"` hypothesis was checked and **not confirmed** — no
`pkill`/`killall` exists in the build's `.sh` or `.py` drivers.

## 6. Standing constraint for the receipt (must be disclosed)

The receipt MUST state: the tail was built on a host running **four concurrent Lean
builds** with swap at ~92%, under a host-wide lean-RSS manager whose aggregate
ceiling was crossed by sibling campaigns; that the build converged by cache-resuming
retries after external SIGTERMs (visible in the retry log as `code 143` / `rc=241`),
serialised through a host-wide build arbiter, with `LEAN_NUM_THREADS=1` (not the
verifier recipe's 4). This is a disclosed footprint reduction.

## 7. What remained (approval-gated)

1. Wait for `QRT BUILD GREEN` in the retry log (loop runs up to 8 h; re-arm with the
   detached launcher if the box reboots).
2. Extract facts: wall time, module count, `grep -c 'error'` = 0, axioms probe output.
3. Assemble `receipts/pr103-8b1a0167-20261105/` in `forkrepo/`.
4. **Draft PR is approval-gated** — no pushes, no PR actions performed in this lane.

---

**Outcome (2026-11-26):** the resume completed; the receipt was committed to fork
branch `receipt/pr103-8b1a0167` @ `2180aadf22` and offered upstream as PR #127, which
was **closed unmerged** (maintainer refusal). See `README.md` and `receipt-draft/`.