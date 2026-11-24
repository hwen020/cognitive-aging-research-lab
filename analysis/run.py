"""Build aggregate, provenance-bearing research artifacts from the synthetic cohort."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

import numpy as np
import pandas as pd

from analysis.cohort import SEED, generate, simulate_incomplete, validate, write_cohort


def records(path):
    return json.loads(pd.read_csv(path).to_json(orient="records", double_precision=12))


def build(phase, rscript):
    cohort = generate()
    bundle = {"schema_version": 1, "source": "deterministic synthetic simulation", "seed": SEED,
              "numpy_version": np.__version__, "pandas_version": pd.__version__, "cohort": {}}
    with tempfile.TemporaryDirectory() as temp:
        directory = Path(temp)
        for mode, frame in (("complete", cohort), ("incomplete", simulate_incomplete(cohort))):
            work = directory / mode
            work.mkdir()
            path = work / "cohort.csv"
            qc = validate(frame, mode == "complete")
            write_cohort(frame, path)
            qc["csv_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
            script = "analysis/r/biological.R" if phase >= 3 else "analysis/r/fit.R"
            command = [rscript, "--vanilla", script, str(path), str(work)]
            subprocess.run(command, check=True, env={**os.environ, "LC_ALL": "C"})
            for name in (["social", "biological"] if phase >= 3 else ["social"]):
                qc[name] = {kind: records(work / f"{name}_{kind}.csv")
                            for kind in ("coefficients", "diagnostics")}
            if phase >= 2:
                from analysis.causal import analyze
                qc["iptw"] = analyze(frame)
            if phase >= 3:
                from analysis.prediction import fit
                qc["prediction"] = fit(frame)
            bundle["cohort"][mode] = qc
    source_files = ["analysis/cohort.py", "analysis/run.py", "analysis/r/fit.R"]
    source_files += ["analysis/causal.py"] if phase >= 2 else []
    source_files += ["analysis/prediction.py", "analysis/r/biological.R"] if phase >= 3 else []
    bundle["source_sha256"] = {
        path: hashlib.sha256(Path(path).read_text(encoding="utf8").encode()).hexdigest()
        for path in source_files
    }
    return bundle


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=[1, 2, 3], type=int, default=1)
    parser.add_argument("--rscript", default="Rscript")
    parser.add_argument("--out", type=Path, default=Path("src/generated/results.json"))
    args = parser.parse_args()
    result = build(args.phase, args.rscript)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    coherent_json = json.dumps(result, indent=2, allow_nan=False, sort_keys=True) + "\n"
    args.out.write_text(coherent_json, encoding="utf8", newline="\n")
    print(f"Wrote {args.out}")
