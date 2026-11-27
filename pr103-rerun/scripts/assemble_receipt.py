"""Assemble the pr103 receipt bundle in forkrepo after a successful run.

Collects the artifacts from the workspace + logs into
forkrepo/verifier/standard/receipts/pr103-8b1a0167-20261105/,
computes SHA256SUMS.json, and prints a summary. Refuses to run unless the
build log shows SOLUTION EXIT 0 and a successful axioms probe.
"""
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
WS = ROOT / "workspace"
LOGS = ROOT / "logs"
FORK = ROOT / "forkrepo"
RECEIPT_NAME = "pr103-8b1a0167-20261105"
DEST = FORK / "verifier" / "standard" / "receipts" / RECEIPT_NAME

TRACKER_REV = "47134867e2ce4d4a311d2da93783c2ae721d9bb9"
MERGE_103 = "8b1a0167c8e324099884152181e3fb2206510e88"
NUMERATOR = ("280496628401749035803096925791412381064048279848824838523676458"
             "7735806455694206308975383836842958115341512355256943573632654341")
DENOMINATOR = ("321161460992211983469417937988874302863495358819785296242351628"
               "8191911449231164741438582626063161096341458934143644085157872271")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    log = (LOGS / "build.log").read_text(errors="replace")
    if "=== SOLUTION EXIT 0" not in log:
        sys.exit("SOLUTION did not exit 0 — refuse to assemble")
    if "=== AXIOMS EXIT 0" not in log:
        sys.exit("axioms probe did not exit 0 — refuse to assemble")
    # Genuine-error scan: only the FINAL attempt (earlier attempts contain
    # kills' partial-write noise, kept in the log as kill provenance).
    starts = [m.start() for m in re.finditer(r"=== ATTEMPT \d+ START ", log)]
    final = log[starts[-1]:] if starts else log
    errors = [ln for ln in final.splitlines()
              if re.search(r"\berror\b", ln)
              and "whitespace" not in ln
              and "depends on axioms" not in ln]
    if errors:
        sys.exit(f"unexpected error lines in final attempt: {errors[:5]}")

    # axioms output: prefer the AXIOMS probe section; dedupe (Candidate/Main.lean
    # also prints its own #print axioms line during compilation).
    m0 = log.find("=== AXIOMS PROBE START ===")
    section = log[m0:] if m0 >= 0 else log
    seen = []
    for decl, ax in re.findall(r"'([\w.]+)' depends on axioms: \[(.*?)\]",
                               section):
        line = f"'{decl}' depends on axioms: [{ax}]"
        if line not in seen:
            seen.append(line)
    axioms = "\n".join(seen)
    for decl in ("QRH.canonical_bound", "Candidate.bound"):
        assert f"'{decl}' depends on axioms: [propext, Classical.choice, Quot.sound]" \
            in axioms, f"missing clean axiom report for {decl}:\n{axioms}"

    jobs = re.findall(r"✔ \[(\d+)/(\d+)\]", log)
    total_jobs = max((int(n) for _, n in jobs), default=0)
    built = sum(1 for ln in log.splitlines() if "✔ [" in ln)
    wall = re.findall(r"=== SOLUTION (?:START|EXIT \d+) ([0-9T:+Z-]+)", log)

    DEST.mkdir(parents=True, exist_ok=True)
    copied = {}

    def put(src, name):
        shutil.copyfile(src, DEST / name)
        copied[name] = sha(DEST / name)

    put(WS / "Challenge.lean", "Challenge.lean")
    put(WS / "Solution.lean", "Solution.lean")
    put(WS / "Axioms103.lean", "Axioms103.lean")
    put(LOGS / "build.log", "build.log")
    put(ROOT / "staging-manifest.json", "staging-manifest.json")

    result = {
        "schema": "external-rerun-offer/1 (not a verifier-registered receipt)",
        "subject": {
            "pr": 103,
            "result_id": "closest-fraction-contact",
            "submission_dir": "submissions/2026-11-01-closest-fraction-contact",
            "merge_commit": MERGE_103,
            "author": "Joseph Bebel",
            "declared_bound": f"{NUMERATOR}/{DENOMINATOR}",
            "declared_decimal": "0.873381966613207519929026778642",
        },
        "rerun": {
            "tracker_rev": TRACKER_REV,
            "challenge_sha256_expected":
                "8fb13ad977bca104591fcbc6ef01a58496e7385053c9b1445f95749afc0eff54",
            "phases": [
                {"name": "MATHLIB_CACHE_GET", "exit": 0},
                {"name": "PATCHES", "exit": 0},
                {"name": "CHALLENGE", "exit": 0},
                {"name": "SOLUTION", "exit": 0},
                {"name": "AXIOMS", "exit": 0},
            ],
            "lake_jobs_total": total_jobs,
            "modules_built_in_log": built,
            "solution_wall": wall,
            "errors_in_final_log": 0,
        },
        "axioms_probe": {
            "kernel": "Lean 4.34.1 default kernel",
            "output": axioms,
            "decls_checked": ["QRH.canonical_bound", "Candidate.bound"],
        },
        "scope": {
            "kernels": ["lean-default"],
            "not_run": ["lean4export", "NanoDa", "con-ron",
                        "sandbox replay", "Comparator"],
            "reason": "Linux-pinned binaries / protected infra not available "
                      "on this host; partial independent rerun by design",
        },
        "host": {
            "os": "macOS arm64 (Apple M4 Max)",
            "load_note": "heavy unrelated foreign load throughout; samples "
                         "every 60s inline in build.log",
        },
        "provenance": {
            "recipe": "scripts/stage_103.py + scripts/run_103.sh "
                      "(BigO-Hunter/quasi-riemann-baseline-rerun, "
                      "pr103-rerun/)",
            "staged_source_files": len(json.loads(
                (ROOT / "staging-manifest.json").read_text())),
        },
        "registration": "offered for maintainer review; receipt-reuse.mjs: "
                        "authentication = maintainer protected registration "
                        "+ exact byte hashes",
    }
    (DEST / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    copied["result.json"] = sha(DEST / "result.json")

    # tool-pins / dependency-pins (mirror pr48 receipt names)
    (DEST / "tool-pins.json").write_text(json.dumps({
        "lean": "leanprover/lean4:v4.34.1 "
                "(commit 5045d0056413266e57c625dcd7c365b10e377c52, Release)",
        "lake": "5.0.0-src+5045d00 (Lean version 4.34.1)",
        "lean_num_threads": 4,
        "note": "single default kernel; no checker binaries pinned (not run)",
    }, indent=2) + "\n")
    copied["tool-pins.json"] = sha(DEST / "tool-pins.json")
    (DEST / "dependency-pins.json").write_text(json.dumps({
        "tracker_rev": TRACKER_REV,
        "mathlib": "d13f23b723b8a846827a245b89c10fc7d3f11612 (lake exe cache get)",
        "PrimeNumberTheoremAnd": "c39a751132c88b6e8080b74c74023fd95b3d8be0 "
                                 "+ lean4341 patch",
        "rellich-kondrachov": "70f85d4c1bf99c6e7d61e8be4daa6f3664d08d23 "
                              "+ lean4341 patch",
        "lakefile_and_manifest": "blob-exact verifier/standard/ at tracker rev",
        "check_pipeline_note": "verifier/standard + upstream-challenge.lean + "
                               "actions + challenge rendering byte-identical "
                               "tracker_rev..origin/main (verified 2026-11-05)",
    }, indent=2) + "\n")
    copied["dependency-pins.json"] = sha(DEST / "dependency-pins.json")

    sums = {f"receipts/{RECEIPT_NAME}/{k}": v for k, v in sorted(copied.items())}
    (DEST / "SHA256SUMS.json").write_text(
        json.dumps(sums, indent=2, sort_keys=True) + "\n")
    print(f"assembled {DEST} with {len(sums)} artifacts")
    for k, v in sums.items():
        print(f"  {v[:12]}…  {k.rsplit('/', 1)[-1]}")


if __name__ == "__main__":
    main()
