# PR #103 rerun lane (`qrt-exec`, folded)

Build-tail triage + resume tooling for QuasiRiemannTracker CI run #103
(`closest-fraction-contact`, rank-1 row; lane F3, 2026-11-06): exact failure
analysis of the death at job 13,507/13,520
(`Submissions.arvi_selected_leaf.JointDetector.NaturalCellSectorNorm`), the
recovery drivers that brought the 13,520-job build to green, and the offered
rerun receipt. Folded from the former private `qrt-exec` repo on 2026-11-26
(consolidation E4, redact-then-merge).

**Status: lane SPENT.** Triage complete; resume executed to green; the receipt
was committed to fork branch `receipt/pr103-8b1a0167` @ `2180aadf22` on
[BigO-Hunter/QuasiRiemannTracker](https://github.com/BigO-Hunter/QuasiRiemannTracker)
and offered upstream as PR #127 — **closed unmerged** (maintainer refusal; see
the sibling bundle's [`FILING_NOTES.md`](../FILING_NOTES.md)). No open work
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
- `receipt-draft/` — the offered receipt's README and PR body (draft shape; the
  filed receipt itself lives on the fork branch named above).
- `staging-manifest.json` — sha256 of every staged source file (8,552 entries:
  the candidate `Candidate/` tree plus the transitive dependency-closure
  `Submissions/` namespaces, blob-exact at tracker rev `47134867`).

## Redaction note

Imported as a **redacted snapshot** (clean import, not raw history): the original
commit messages and the triage/operations documents carried body-internal
process-management provenance (internal kill-log excerpts, memory-management tool
names, process ids, internal workspace paths), which was removed or generalized.
The internal operations log (`RESUME.md`) is excluded from the public import
entirely; its mathematical pins survive in `receipt-draft/`, `scripts/`, and
`staging-manifest.json`. All mathematical rerun evidence and the receipt content
are preserved. The full unredacted history is preserved in the org's private
campaign archive.

## License

Copy-Free/Stays-Free (CFSF) — see [`LICENSE`](LICENSE) and the bundle root
[`LICENSE`](../LICENSE).