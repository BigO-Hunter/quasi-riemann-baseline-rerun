"""Verify the vendored openai-baseline tree against openai/math@fd4aeeb2.

For each Submissions/openai_baseline/**.lean file, the upstream counterpart is
lean/**.lean in openai/math; equality is expected modulo the import remap
`import OAI.` -> `import Submissions.openai_baseline.OAI.` (documented tracker
packaging transformation). Main.lean is packaging-only (no upstream file).
"""
import hashlib
import os
import pathlib
import sys

# Portable paths: repo-local defaults, overridable via environment.
# QR_WORKSPACE: the staged rebuild workspace (see stage_workspace.py).
# QR_UPSTREAM: a checkout of openai/math @ fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb (lean/ tree).
ROOT = pathlib.Path(__file__).resolve().parent.parent
WS = pathlib.Path(os.environ.get("QR_WORKSPACE") or ROOT / "workspace") / "Submissions/openai_baseline"
UP = pathlib.Path(os.environ.get("QR_UPSTREAM") or ROOT / "openai-src/lean")

def norm(b: bytes) -> bytes:
    return b.replace(b"\r\n", b"\n").replace(b"import OAI.", b"import Submissions.openai_baseline.OAI.")

mismatch, missing, checked = [], [], 0
for f in sorted(WS.rglob("*.lean")):
    rel = f.relative_to(WS)
    if str(rel) == "Main.lean":
        continue  # tracker packaging entrypoint, not an upstream blob
    up = UP / rel
    if not up.exists():
        missing.append(str(rel))
        continue
    checked += 1
    if norm(up.read_bytes()) != f.read_bytes():
        mismatch.append(str(rel))

print(json_out := {
    "checked": checked,
    "missing_upstream": len(missing),
    "content_mismatch": len(mismatch),
})
for x in (missing + mismatch)[:20]:
    print("  DIFF/MISSING:", x)
sys.exit(0 if not missing and not mismatch else 1)
