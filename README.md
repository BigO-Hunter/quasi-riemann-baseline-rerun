# Quasi-Riemann baseline rerun — independent verification receipt

> ## 🏁 RACE CLOSED
> **Levent Alpöge proved the quasi-Riemann hypothesis at θ ≤ 1/2 (optimal) on
> 2026-11-20 — Lean Verified.** This is the only officially closed race on the
> [Big O Speedrun board](https://bigospeedrun.com). The target this lane verified
> a baseline for is settled. **This repository is preserved as a verified
> baseline and an independent-rerun reference, and is archived read-only.**

Independent, from-source rebuild and Lean-kernel axiom check of the
[QuasiRiemannTracker](https://github.com/GTimG/QuasiRiemannTracker)'s vendored
OpenAI seven-eighths baseline (`submissions/2026-10-06-openai-baseline`, result id
`openai-baseline`), run outside the tracker's CI on different hardware and OS
(Apple M4 Max, macOS arm64). Offered as freely reusable verification evidence —
not a tracker-registered receipt.

## Board state

- **Race:** quasi-Riemann hypothesis — zero-free half-plane `Re s > θ` for all
  Dirichlet L-functions (lower θ is better; GRH = θ = 1/2).
- **Closed by:** Levent Alpöge, **θ ≤ 1/2 (optimal)**, 2026-11-20, **Lean Verified**.
- **This repo's rung:** the OpenAI **θ = 7/8 = 0.875** baseline — a *weaker* bound
  than the record. The rerun established the baseline row's independent
  "Lean Verified" rebuild tier; it never claimed the record. With the race closed
  at the optimal θ = 1/2, this baseline is of historical/reference interest only.

## Result (PASS — local rebuild)

- `lake build Challenge` + `lake build Solution` (+ Hecke supplement): exit 0,
  **2,927/2,927** submission modules compiled from source, **0 errors**
  (Lean `v4.34.1`, Mathlib `d13f23b7`, 3 h 00 m 51 s wall).
- `#print axioms` (Lean default kernel) for **eight** target declarations returns
  exactly `[propext, Classical.choice, Quot.sound]` — no `sorryAx`, no extras.
- Provenance: all **2,926** vendored `OAI/**.lean` modules blob-verified against
  `openai/math@fd4aeeb2` (0 missing, 0 mismatches modulo two documented packaging
  transforms). The tracker's two `lean4341` patches are byte-identical to upstream's.

Full narrative, pins, and arithmetic cross-checks: [`RECEIPT.md`](RECEIPT.md).

**Honest limits:** Lean *default* kernel only — no `lean4export`/NanoDa/con-ron
triple-kernel pipeline (Linux-pinned binaries), no sandbox replay, nothing
maintainer-registered. macOS arm64 vs the hosted Linux x86-64 worker is the point
of an independent rerun; artifacts are not interchangeable with worker caches.

## Contents

| Path | What it is |
|---|---|
| `RECEIPT.md` | Full receipt: pins, provenance, build phases, axiom receipts, arithmetic |
| `sources/` | Rendered `Challenge.lean`/`Solution.lean`, axiom probes, `lakefile.lean`/`lake-manifest.json`/`lean-toolchain` |
| `scripts/` | The exact recipe: staging, build driver, upstream verification, stats, host monitor |
| `built-modules.txt`, `final-stats.json`, `dep-revs.txt`, `upstream-verification.txt` | Build inventory and verification outputs |
| `SHA256SUMS.txt` | sha256 of every file in this bundle |
| `pr103-rerun/` | Sibling lane: PR #103 build-tail triage + resume tooling and receipt (spent; offered as PR #127, closed unmerged) |
| `LICENSE`, `NOTICE.md` | CFSF license; third-party attribution |

## Reproduce / verify

The recipe rebuilds the workspace from tracker git blobs (conversion-free) and
renders the challenge/solution byte-exactly. Scripts are portable: repo-local
defaults, overridable via environment (`QR_TRACKER`, `QR_WORKSPACE`, `QR_STAGE`,
`QR_UPSTREAM`, `QR_OUT`, `QR_BUILD_LOG`, `QR_HOSTMON_LOG`).

1. Clone the tracker at the pinned revision into `tracker/` (or set `QR_TRACKER`):
   `GTimG/QuasiRiemannTracker @ 47134867e2ce4d4a311d2da93783c2ae721d9bb9`.
2. `python scripts/stage_workspace.py` — stage `Candidate/` + `Submissions/`,
   scaffolding, and rendered `Challenge.lean`/`Solution.lean` (asserts the
   challenge is byte-identical to the pr69 receipt's `BaselineChallenge.lean`).
3. `bash scripts/run_build.sh` — `lake build Challenge` then `lake build Solution`
   (`LEAN_NUM_THREADS=4`; Lake 5 has no `-j`). Requires Lean `v4.34.1` via elan and
   the pinned Mathlib/PNTA/rellich-kondrachov deps (see `sources/lake-manifest.json`).
4. In the workspace, `lake env lean Axioms.lean` (probes preserved in
   `sources/Axioms*.lean`) — re-check the axiom receipts against the built oleans.
5. `python scripts/verify_upstream.py` — blob-verify the vendored tree against an
   `openai/math@fd4aeeb2` checkout (`QR_UPSTREAM`).
6. `python scripts/final_stats.py` — regenerate the build inventory/timing from a
   build log (`QR_BUILD_LOG`).

The full built workspace (~9 GB) is not redistributed; it is reproduced by the
recipe above. See `RECEIPT.md` §6 for environment quirks (notably LF→CRLF host
checkout conversion, hence blob-exact staging).

## License

[Copy-Free/Stays-Free (CFSF)](LICENSE) — copy-free (use for any purpose) and
stays-free (nobody may fence this work). Vendored third-party material keeps its
upstream license (Apache-2.0) — see [NOTICE](NOTICE.md). AI-assisted; disclosed.

Part of [BigO-Hunter](https://github.com/BigO-Hunter) — independent verification
and packaging for [Big O Speedrun](https://bigospeedrun.com) ·
[org profile](https://github.com/BigO-Hunter/.github) ·
[bigo-hunter.github.io](https://bigo-hunter.github.io).
