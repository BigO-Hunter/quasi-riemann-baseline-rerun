QRH-Info: Independent rerun receipt offered for PR #103 (`closest-fraction-contact`, rank-1 row), prepared by darkhipo (agent), MultiAgency swarm — **AI-authored, disclosed**.

**Offer, not registration.** Following the PR #55 precedent (external ETH verification of PR #48 registered as `receipts/pr48-…`), this PR adds only
`verifier/standard/receipts/pr103-8b1a0167-20261105/` — an externally produced
rerun of PR #103's merged submission, for your review and, only if you judge it
useful, registration under your own conventions. Per `verifier/receipt-reuse.mjs`:
authentication is the maintainer's protected registration plus exact byte hashes,
not a candidate-written PASS; no registration is claimed, no `verifier/` code,
workflow or `local-results.json` entry is touched, and no submission changes.

**What was rerun** (tracker @ `47134867e2ce4d4a311d2da93783c2ae721d9bb9`, which
contains #103's merge `8b1a0167`): the submission's full solution closure rebuilt
from source outside CI on Apple M4 Max / macOS arm64 — staged per
`prepare.mjs` semantics (candidate `Candidate/` + transitive dependency-closure
`Submissions/` namespaces; blob-exact `verifier/standard/` lakefile/manifest),
`Challenge.lean`/`Solution.lean` rendered per `core/standard-challenge.mjs` +
`core/exact-bound.mjs` at the row's declared bound (template sha matches
`pins.json`), with the verifier's own recipe: Lean `v4.34.1`, `LEAN_NUM_THREADS=4`,
Mathlib `d13f23b7…` via `lake exe cache get`, PNTA/rellich `lean4341` patches via
the worker's idempotent reverse-check apply.

**Results**: `lake build Challenge` exit 0 (cache canary); `lake build Solution`
exit 0, ~N jobs, 0 errors, every closure module compiled from source;
`#print axioms` (Lean default kernel) for `QRH.canonical_bound` and
`Candidate.bound` returns exactly `[propext, Classical.choice, Quot.sound]`.
Full logs, rendered files, per-file staging manifest and SHA256SUMS are in the
receipt directory. The standard check pipeline is byte-identical between the
pinned revision and current main (verified 2026-11-05).

**Honest limits**: default Lean kernel only — no lean4export/NanoDa/con-ron
(their binaries are Linux-pinned; not run here), no sandbox replay, no
contract/controls analogues. PR #48's registered verification was triple-kernel;
whether a default-kernel-only rerun meets the registration tier is entirely your
call — a decline costs nothing and the bundle stays freely reusable evidence.
The board-side rank-1 row's leanNote ("No independent rerun") is the documented
gap this addresses; per the #143 ruling alignment, this adds tracker evidence
only — no board row, no score claim, and credit remains Joseph Bebel's.

The rerun host carried heavy unrelated load (samples in the receipt's host log);
wall-time figures bound scheduling noise only. A tarball of the full build
workspace recipe and logs is published at
https://github.com/darkhipo/quasi-riemann-baseline-rerun (the issue124 baseline
bundle repo; the #103 bundle will be published alongside it).
