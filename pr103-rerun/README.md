# PR #103 rerun (build-tail triage + resume)

Build-tail triage + resume tooling for QuasiRiemannTracker CI run #103
(`closest-fraction-contact`, rank-1 row; 2026-11-06): exact failure
analysis of the death at job 13,507/13,520
(`Submissions.arvi_selected_leaf.JointDetector.NaturalCellSectorNorm`), the
recovery drivers that brought the 13,520-job build to green, and the offered
rerun receipt.

**Status: SPENT.** Triage complete; resume executed to green; the receipt
was committed to fork branch `receipt/pr103-8b1a0167` @ `2180aadf22` on
[BigO-Hunter/QuasiRiemannTracker](https://github.com/BigO-Hunter/QuasiRiemannTracker)
and offered upstream as PR #127 — **closed unmerged** (maintainer refusal). No open work
remains. That fork branch is the sole surviving PR #103 receipt and is never
pruned.

## Layout

- `QRT_TRIAGE.md` — the triage record: code 143 = external SIGTERM (not a Lean
  compile error), recovery-driver defects and fixes, convergence evidence,
  honest attribution limits, and the receipt's standing disclosure constraint.
- `patches/` — the tracker's `lean4341` patches for PrimeNumberTheoremAnd and
  rellich-kondrachov (the worker's own idempotent reverse-check recipe).
- `scripts/` — workspace staging from tracker git blobs (`stage_103.py`), build
  driver (`run_103.sh`), resume driver (`resume_solution.sh`), cache-resuming
  retry runner, completion watcher, detached-launch daemonizer, and receipt
  assembly (`assemble_receipt.py`).
- `receipt-draft/` — the offered receipt's README (the filed receipt itself lives
  on the fork branch named above).
- `staging-manifest.json` — sha256 of every staged source file (8,552 entries:
  the candidate `Candidate/` tree plus the transitive dependency-closure
  `Submissions/` namespaces, blob-exact at tracker rev `47134867`).

## Provenance note

Imported as a clean snapshot (not raw history): internal process-management
provenance was removed or generalized. All mathematical rerun evidence and the
receipt content are preserved in `receipt-draft/`, `scripts/`, `patches/`, and
`staging-manifest.json`.

## License

Copy-Free/Stays-Free (CFSF) — see [`LICENSE`](LICENSE) and the bundle root
[`LICENSE`](../LICENSE).