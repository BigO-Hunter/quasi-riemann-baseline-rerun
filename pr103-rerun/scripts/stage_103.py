"""Stage the QR #103 (closest-fraction-contact) rerun workspace from tracker git blobs.

Mirrors verifier/standard/prepare.mjs semantics for PR #103: stage the candidate
Candidate/ tree plus the transitive dependency-closure Submissions/ namespaces,
assemble the QRH lake workspace per verifier/standard/lakefile.lean, and render
Challenge.lean/Solution.lean per core/standard-challenge.mjs + core/exact-bound.mjs
at the row's declared bound (a normalized fraction, so exactBound renders "n / d").

Pinned tracker revision: 47134867e2ce4d4a311d2da93783c2ae721d9bb9 (2026-11-03,
contains merged PR #103 = 8b1a0167; the rev the issue124 baseline bundle pinned).
"""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
from math import gcd

ROOT = pathlib.Path(__file__).resolve().parent.parent
TRACKER = ROOT / "tracker"
WS = ROOT / "workspace"
STAGE = ROOT / "stage"

REV = "47134867e2ce4d4a311d2da93783c2ae721d9bb9"
CANDIDATE_DIR = "submissions/2026-11-01-closest-fraction-contact"
# Transitive dependency closure of #103's metadata.json `dependencies`,
# resolved to submission directories (id = slug after the date prefix).
DEP_DIRS = [
    "2026-10-06-openai-baseline",
    "2026-10-21-hailey-collet-1252270103",
    "2026-10-25-arvi-repeated-marks-on-sil-face",
    "2026-10-26-sil-density-split",
    "2026-10-28-density-split-fine-chain",
    "2026-10-29-arvi-density",
    "2026-10-30-arvi-selected-leaf",
]
# PR #103 QRH-Bound field (127/127-digit fraction).
NUMERATOR = ("280496628401749035803096925791412381064048279848824838523676458"
             "7735806455694206308975383836842958115341512355256943573632654341")
DENOMINATOR = ("321161460992211983469417937988874302863495358819785296242351628"
               "8191911449231164741438582626063161096341458934143644085157872271")
CHALLENGE_SHA = "8fb13ad977bca104591fcbc6ef01a58496e7385053c9b1445f95749afc0eff54"


def git(*args, binary=False):
    r = subprocess.run(["/usr/bin/git", "-C", str(TRACKER), *args],
                       capture_output=True, check=True)
    return r.stdout if binary else r.stdout.decode()


def blob(path):
    return git("cat-file", "blob", f"{REV}:{path}", binary=True)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    if gcd(int(NUMERATOR), int(DENOMINATOR)) != 1:
        sys.exit("bound fraction not normalized (rational() would reject)")
    bound_lean = f"{NUMERATOR} / {DENOMINATOR}"  # core/exact-bound.mjs rendering

    if WS.exists():
        sys.exit(f"workspace already exists: {WS}")
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    WS.mkdir(parents=True)
    manifest = {}

    # 1. Candidate/ from #103.
    src_prefix = CANDIDATE_DIR + "/src"
    with open(STAGE / "cand.tar", "wb") as f:
        subprocess.run(["/usr/bin/git", "-C", str(TRACKER), "archive", REV,
                        src_prefix], stdout=f, check=True)
    subprocess.run(["tar", "-xf", str(STAGE / "cand.tar"), "-C", str(STAGE)],
                   check=True)
    shutil.copytree(STAGE / src_prefix / "Candidate", WS / "Candidate")

    # 2. Submissions/ union over the dependency closure (disjoint namespaces).
    (WS / "Submissions").mkdir()
    for d in DEP_DIRS:
        prefix = f"submissions/{d}/src/Submissions"
        t = STAGE / f"dep-{d}.tar"
        with open(t, "wb") as f:
            subprocess.run(["/usr/bin/git", "-C", str(TRACKER), "archive", REV,
                            prefix], stdout=f, check=True)
        x = STAGE / f"dep-{d}"
        x.mkdir()
        subprocess.run(["tar", "-xf", str(t), "-C", str(x)], check=True)
        for ns in sorted((x / prefix).iterdir()):
            dest = WS / "Submissions" / ns.name
            if dest.exists():
                sys.exit(f"namespace collision: {ns.name}")
            shutil.copytree(ns, dest)

    # 3. Worker scaffolding (blob bytes of verifier/standard files).
    for name, path in [("lakefile.lean", "verifier/standard/lakefile.lean"),
                       ("lake-manifest.json",
                        "verifier/standard/lake-manifest.json")]:
        b = blob(path)
        (WS / name).write_bytes(b)
        manifest[name] = sha(b)
    (WS / "lean-toolchain").write_bytes(b"leanprover/lean4:v4.34.1\n")

    # 4. Render Challenge.lean (standard-challenge.mjs recipe at #103's bound).
    tpl = blob("verifier/upstream-challenge.lean").decode()
    assert sha(tpl.encode()) == CHALLENGE_SHA, \
        "template sha != pins.json challenge_sha256"
    assert tpl.count("(7 / 8 : \u211d)") == 1
    challenge = (tpl
                 .replace("namespace OAI\n\nnamespace DirichletCharacter",
                          "namespace QRH")
                 .replace("LFunction_ne_zero_of_seven_eighths_lt_re",
                          "canonical_bound")
                 .replace("(7 / 8 : \u211d)", f"({bound_lean} : \u211d)")
                 .replace("end DirichletCharacter\n\nend OAI", "end QRH"))
    assert "(7 / 8 : \u211d)" not in challenge
    (WS / "Challenge.lean").write_bytes(challenge.encode())

    # 5. Solution.lean: challenge wrapper proven by the candidate's bound.
    solution = ("import Candidate.Main\n\n"
                + challenge.replace("import Mathlib\n", "")
                .replace("  sorry", "  exact Candidate.bound \u03c7 hs hpole"))
    (WS / "Solution.lean").write_bytes(solution.encode())

    # 6. Axioms probe (Lean 4.34.1 default kernel).
    (WS / "Axioms103.lean").write_bytes(
        b"import Solution\n\n#print axioms QRH.canonical_bound\n"
        b"#print axioms Candidate.bound\n")

    # 7. Hash every staged file.
    for p in sorted(WS.rglob("*")):
        if p.is_file() and ".lake" not in p.parts:
            manifest[str(p.relative_to(WS))] = sha(p.read_bytes())
    out = ROOT / "staging-manifest.json"
    out.write_text(json.dumps(manifest, indent=1, sort_keys=True))
    n_cand = sum(1 for p in (WS / "Candidate").rglob("*") if p.is_file())
    n_subs = sum(1 for p in (WS / "Submissions").rglob("*") if p.is_file())
    print(f"staged: Candidate files={n_cand} Submissions files={n_subs} "
          f"total hashed={len(manifest)} -> {out}")


if __name__ == "__main__":
    main()
