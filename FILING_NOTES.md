# FILING NOTES — why this bundle was NOT filed to GTimG/QuasiRiemannTracker

**Decision (2026-11-08): not filed. The target repo's prior engagement shows a refusal
of this class of unsolicited contribution, and we respect it.**

## What the recon found

The planned channel — a PR adding a rerun receipt under `verifier/standard/receipts/`,
following the repo's own receipt-directory conventions — was already used by this
project yesterday: PR
[#127](https://github.com/GTimG/QuasiRiemannTracker/pull/127) ("Independent rerun
receipt offered for PR #103") was closed unmerged, with the maintainer's only comment:

> "I am genuinely confused what made you think this was a contribution we would be
> asking for. Its the second one, with #124 so there must be something we
> incorrectly/confusingly write somewhere?" — nielstron, 2026-11-07

The issue-route twin, issue
[#124](https://github.com/GTimG/QuasiRiemannTracker/issues/124) — this exact baseline
rerun, filed 2026-11-05 — was closed silently (state "completed", zero comments) the
same day it was filed.

Filing a third unsolicited donation PR/issue after that signal would disregard it. The
README's receipt machinery (`verifier/standard/receipts/`, `receipt-reuse.mjs`)
documents **maintainer-produced** verification receipts and their protected reuse; the
one external receipt the project registered (the PR #55 ETH verification) was
maintainer-initiated and retrieved over SSH. The receipts directory is not a donation
lane, and the maintainers have now said so in effect.

## What this bundle is (for the record)

A complete, independent, from-source rebuild of the vendored OpenAI 7/8 baseline rung
(`openai-baseline`, 2,927 submission modules) on Apple M4 Max / macOS arm64 under Lean
v4.34.1 at byte-verified pins: 0 compile errors, `#print axioms` returning exactly
`[propext, Classical.choice, Quot.sound]` for all eight target declarations, and all
2,926 vendored sources provenance-verified against openai/math@fd4aeeb2. Full logs,
scripts, hashes and host samples: `RECEIPT.md`, `result-local.json`, `SHA256SUMS.txt`.

## Next-best channel (maintainer's call; nothing pushed on them)

- The bundle already lives publicly in this repo, and the links in the prepared
  documents (`darkhipo/quasi-riemann-baseline-rerun`, which redirects here) resolve.
  Anyone — including the maintainers — can review or reuse it without our asking
  anything of them.
- If the maintainers ever want this on the record, the one respectful move is a short
  human-written reply on PR #127 answering nielstron's actual question — what in the
  project's public materials read as an invitation (the board's "No independent rerun"
  notes, the PR #55 precedent) — and leaving the decision entirely with them.
- No issue, PR, comment, or email was filed from this lane.
