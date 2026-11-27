# Independent rerun receipt for PR #103 (`closest-fraction-contact`)

This directory describes an externally produced rerun of tracker PR #103's
rank-1 row. It is independent verification evidence, freely reusable; it is
not a tracker-registered receipt and claims no registration. The filed receipt
itself lives on fork branch `receipt/pr103-8b1a0167` (see `../README.md`).

## What was rerun

The merged PR #103 submission (`submissions/2026-11-01-closest-fraction-contact`,
merge commit `8b1a0167`, tree pinned at tracker revision
`47134867e2ce4d4a311d2da93783c2ae721d9bb9`, which contains it) was rebuilt
**from source, end to end, outside CI**, on hardware and OS different from the
hosted workers: Apple M4 Max (macOS arm64), under heavy unrelated host load
(samples in the host log).

- Workspace staged per `verifier/standard/prepare.mjs` semantics from git
  blobs: the candidate `Candidate/` tree (237 modules) plus the transitive
  dependency closure's `Submissions/` namespaces (openai-baseline,
  hailey-collet-1252270103, arvi-repeated-marks-on-sil-face-20261025,
  sil-density-split-20261026, density-split-fine-chain, arvi-density,
  arvi-selected-leaf; NNNN files). `lakefile.lean` and `lake-manifest.json`
  are blob-exact copies of `verifier/standard/`.
- `Challenge.lean` and `Solution.lean` rendered per
  `core/standard-challenge.mjs` + `core/exact-bound.mjs` at the row's declared
  bound `2804966…4341 / 3211614…2271` (asserted normalized, rendered `n / d`);
  the challenge template byte-hash matches `verifier/pins.json`
  (`challenge_sha256`).
- `lake build Challenge`: exit 0 (canary; validates the Mathlib cache).
- `lake build Solution`: exit 0, NNNN/NNNN jobs, 0 errors — every module in
  the solution closure compiled from source in this workspace.
- `#print axioms` (Lean 4.34.1 default kernel): `QRH.canonical_bound` and
  `Candidate.bound` each return exactly
  `[propext, Classical.choice, Quot.sound]`. No `sorryAx`, no extras.
  (`Candidate/Main.lean` itself carries a `#print axioms Candidate.bound`;
  its output is in the build log.)

Pins: Lean `v4.34.1` / Lake 5.0.0-src+5045d00, `LEAN_NUM_THREADS=4` (the
mechanism `verifier/actions/setup.py` uses); Mathlib `d13f23b7…` olean cache
(fetched via `lake exe cache get`, the verifier's own recipe);
PrimeNumberTheoremAnd `c39a751…` and rellich-kondrachov `70f85d4…` with the
tracker's `lean4341` patches applied by the worker's own idempotent
reverse-check recipe. The standard check pipeline
(`verifier/standard/`, `upstream-challenge.lean`, `verifier/actions/`,
challenge rendering) is **byte-identical** between the pinned revision and
current main (verified on 2026-11-05), so this evidence binds the pipeline
main runs.

## Honest limits

- **Lean default kernel only.** No lean4export freeze, no NanoDa, no con-ron
  (Linux-pinned binaries not run here), no Palomar-style sandbox replay, no
  `contract.json`/`controls.json` analogues. This is a *partial* independent
  rerun; PR #48's registered verification (PR #55) was triple-kernel.
  Whether that meets the registration tier is entirely the maintainer's call;
  a decline costs nothing and this bundle remains freely reusable evidence.
- Platform difference (macOS arm64, heavy foreign load) is the point of an
  independent rerun; artifacts are not interchangeable with worker caches.
- Wall-time numbers bound scheduling noise only (host log samples included);
  compilation is per-module and every module compiled from source here.
- The board-side rank-1 row's leanNote reads "No independent rerun"; credit
  for the result remains Joseph Bebel's (and the #143-ruling position on the
  board side: evidence lives in the tracker, credit with the author). This
  receipt adds evidence only — no board row, no score claim.

## Files (assembled by `../scripts/assemble_receipt.py`)

- `result.json` — structured outcome (phases, exits, counts, axioms, pins)
- `Challenge.lean`, `Solution.lean` — the rendered files actually built
- `build.log` — full build log (Challenge + Solution + axioms probe)
- `staging-manifest.json` — sha256 of every staged source file
- `tool-pins.json`, `dependency-pins.json` — toolchain and dependency revs
- `SHA256SUMS.json` — hashes of this bundle's artifacts
