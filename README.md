# Independent local rerun — OpenAI 7/8 baseline rung (openai-baseline)

Independent, from-source rebuild and Lean-kernel axiom check of the tracker's vendored
OpenAI seven-eighths baseline (`submissions/2026-10-06-openai-baseline`), run outside
the tracker's CI on different hardware and a different OS. Offered as evidence for the
maintainer-approved reuse flow in the tracker README ("Reuse an independently verified
receipt", L207-244). Scope: Lean default kernel only — see Limits below.

## Run identity

- Date: 2026-11-04 (UTC). Successful build window 19:31:39Z → 22:32:30Z (3 h 00 m 51 s);
  axiom probes and Hecke supplement through ~23:39Z.
- Host: Apple M4 Max, 128 GB unified memory, macOS (darwin arm64), chronically loaded by
  concurrent foreign workloads (1-min loadavg 54–435 peaks; swap free dipped to 592 MB).
  No OOM, no abort, no wedge in this lane. Samples: `logs/hostmon.log` (120 s cadence).
- Toolchain: `leanprover/lean4:v4.34.1` (elan), Lake 5.0.0-src+5045d00,
  parallelism `LEAN_NUM_THREADS=4` (Lake 5 has no `-j` flag; this is the same mechanism
  the tracker worker uses in `verifier/actions/setup.py`).
- Source pins: GTimG/QuasiRiemannTracker @ `47134867e2ce4d4a311d2da93783c2ae721d9bb9`;
  baseline tree `e82378d33de178f616b8a03c972caabbf2d874501`; upstream openai/math @
  `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`; Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`;
  PrimeNumberTheoremAnd `c39a751132c88b6e8080b74c74023fd95b3d8be0` + tracker lean4341 patch;
  rellich-kondrachov `70f85d4c1bf99c6e7d61e8be4daa6f3664d08d23` + tracker lean4341 patch.
  Workspace scaffolding = blob-exact copies of `verifier/standard/lakefile.lean` and
  `verifier/standard/lake-manifest.json` (`sources/`).
- Mathlib came from a warm exact-pin olean build APFS-cloned from an unrelated prior
  workspace on the same host (same Lean, same Mathlib revision): **zero Mathlib
  recompiles** — lake trace validation accepted all 8.9 GB.

## What was built and checked

- `lake build Challenge` — exit 0, 8,925 jobs. Rendered canonical challenge
  (`sources/Challenge.lean`, θ = 7/8) is **byte-identical to `BaselineChallenge.lean`
  in `verifier/standard/receipts/pr69-ac76d5ef-20261023/`**
  (sha256 `a9d290c74920624ba06f66da0a56b633876e2a0ac230613add78b61370fbfe12`).
  Only warning: the template's intentional `sorry`.
- `lake build Solution` — exit 0, 7,065 jobs, **0 error lines**. Solution.lean is the
  README/challenge.mjs `solutionWrapper` rendering (`exact Candidate.bound χ hs hpole`).
- `lake build Submissions` supplement — the 2 Hecke-statement modules outside the
  Dirichlet entrypoint closure. Final: **2,927/2,927 submission modules** +
  Candidate.Main + Solution + Challenge = 2,930 root-package oleans
  (`built-modules.txt`, `final-stats.json`).
- `#print axioms` (Lean 4.34.1 default kernel, local oleans; logs `logs/axioms*.log`,
  probes `sources/Axioms*.lean`) — all eight declarations depend on exactly
  `[propext, Classical.choice, Quot.sound]`, no `sorryAx`:
  `QRH.canonical_bound`; `Submissions.openai_baseline.bound`;
  `OAI.DirichletCharacter.LFunction_ne_zero_of_seven_eighths_lt_re`;
  `OAI.riemannZeta_ne_zero_of_seven_eighths_lt_re`;
  `OAI.SevenEighths.HeckeFamily.LFunction_ne_zero_of_seven_eighths_lt_re`;
  `OAI.SevenEighths.HeckeFamily.LFunction_ofResidue_ne_zero_of_seven_eighths_lt_re`;
  `OAI.SevenEighths.HeckeRayFamily.LFunction_ne_zero_of_seven_eighths_lt_re`;
  `OAI.SevenEighths.HeckeFamily.LFunction_ne_zero_of_certified_bands`.
  This matches the `allowed_axioms` set in the tracker's own receipts.
- Provenance: all 2,926 vendored `OAI/**.lean` modules blob-verified against
  openai/math@`fd4aeeb2` (`upstream-verification.txt`, harness `scripts/verify_upstream.py`):
  0 missing, 0 mismatches modulo exactly two documented transforms (upstream CRLF→LF;
  `import OAI.` → `import Submissions.openai_baseline.OAI.`). The two tracker lean4341
  patches applied here are byte-identical to upstream's own `lean/patches/` copies
  (LF-normalized).
- Negative control preserved: `logs/build.log.rkfail` — unpatched rellich-kondrachov
  `70f85d4` fails elaboration against Mathlib `d13f23b7` under Lean 4.34.1 (type
  mismatches in `L2Compactness/Kernels.lean`, `LpSpace/Restrict.lean`, `Euclidean/H1.lean`).
  The build only proceeds after applying the tracker/upstream patches, evidencing that
  the real pinned dependency path was exercised rather than a cache.

## Limits (honest scope)

- **Lean default kernel only.** This rerun did NOT produce the frozen lean4export
  exports nor run NanoDa/con-ron (Linux-pinned protected binaries). It is therefore not
  a substitute for, and does not claim, the triple-kernel acceptance recorded in
  `verifier/standard/receipts/`. It has no `contract.json`/`controls.json`/
  `kernel-check-phases.json`/`tool-pins.json` analogues, and nothing here is
  maintainer-registered; per README L219 a candidate-written PASS is not
  authentication, and this bundle does not ask to be treated as one.
- The host ran foreign workloads throughout (peaks reflected in `hostmon.log`); this
  affects wall-time only, not build determinism — Lean compilation is per-module and
  every module compiled from source in this workspace.
- Platform is macOS arm64 vs the hosted Linux x86-64 worker. That difference is the
  point of an independent rerun, and it also means olean-level artifacts are not
  interchangeable with the worker's caches.
- `#print axioms` runs through Lean elaboration of the probe files against locally
  built oleans; it is the same trust class as the receipts' "Lean default" kernel
  check, but performed here without sandbox isolation.

## Reproducibility

Recipe scripts are in `scripts/` (staging from git blobs, byte-exact challenge/solution
rendering, build driver, stats, upstream verification). The full built workspace
(~9 GB incl. cloned packages) was retained on the rerun host at `/tmp/qr_rebuild/workspace`
at time of writing and can revalidate incrementally (`lake build Solution` → up-to-date).
Environment quirks recorded in `RECEIPT.md` §6 (notably: host git checkout applies
LF→CRLF conversion, so all staging used blob extraction, matching the worker's
"read submission Git blobs as data" semantics).

## File map

- `RECEIPT.md` — full receipt narrative (pins, provenance, phases, arithmetic checks)
- `result-local.json` — machine-readable local result (explicitly named `-local`; not
  the tracker `result.json` schema)
- `DRAFT.md` — draft issue body for the coordinator/maintainer conversation
- `SHA256SUMS.txt` — sha256 of every file in this bundle (+ the distribution tarball)
- `sources/` — rendered Challenge/Solution, axiom probes, lakefile/manifest/toolchain
- `logs/` — build phases, axiom outputs, host monitor
- `scripts/` — the exact recipe
- `built-modules.txt`, `final-stats.json`, `dep-revs.txt`, `upstream-verification.txt`

Prepared by an AI-authored lane of the darkhipo swarm (disclosed per the draft);
no fork, commit, PR, issue or comment was made against the tracker by this lane.

## Notes

- The frozen `donation-bundle.tar.gz` is the receipt as assembled at rebuild time and
  retains the original tree-sha transcription; the corrected baseline tree sha
  `e82378d33de178f616b8a03c972caabbf2d874501` (Run identity above) is the correction
  of record. Tarball sha256:
  `b416bbdfa58c68b91705400084249923183c054c01cc1266a66f682a425732e6` (SHA256SUMS passes).
- `.gitattributes` (`* -text`) keeps checkouts byte-stable under `core.autocrlf=true`.
- Tracker issue #124 was closed (completed) by the maintainer on 2026-11-05; the
  donation lane is closed.

## Sibling lane: PR #103 rerun (`pr103-rerun/`)

A second independent QRT rerun — build-tail triage + resume for tracker CI run #103
(`closest-fraction-contact`, rank-1 row). Its receipt was offered as upstream PR #127,
**closed unmerged**; the sole surviving copy is fork branch `receipt/pr103-8b1a0167`
@ `2180aadf22` on
[BigO-Hunter/QuasiRiemannTracker](https://github.com/BigO-Hunter/QuasiRiemannTracker),
never pruned (see `FILING_NOTES.md`). Lane spent; no open work.

## What work can be done here

The receipt stands. Open work: reruns on further platforms/OSes; tracker-side integration of the reuse flow.

## License

Licensed under the Copy-Free/Stays-Free (CFSF) License — see [LICENSE](LICENSE). CFSF: copy-free (use for any purpose) and stays-free (nobody may fence this work). Vendored third-party material keeps its upstream license — see [NOTICE](NOTICE.md).

Part of [BigO-Hunter](https://github.com/BigO-Hunter) — independent verification and packaging for [Big O Speedrun](https://bigospeedrun.com) · [org profile](https://github.com/BigO-Hunter/.github) · [bigo-hunter.github.io](https://bigo-hunter.github.io).
