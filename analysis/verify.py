"""Compare regenerated results with the release bundle using declared tolerances."""

import argparse
import hashlib
import json
from math import isclose
from pathlib import Path


def verify(reference, regenerated):
    def exact(left, right, label):
        if left != right:
            raise ValueError(f"Mismatch in {label}")

    def close(left, right, label, tolerance=1e-6):
        if not isclose(left, right, rel_tol=0, abs_tol=tolerance):
            raise ValueError(f"Mismatch in {label}: {left} vs {right}")

    exact(reference["source_sha256"], regenerated["source_sha256"], "analysis fingerprints")
    for path, digest in reference["source_sha256"].items():
        actual = hashlib.sha256(Path(path).read_text(encoding="utf8").encode()).hexdigest()
        exact(digest, actual, path)
    runtime = json.loads(Path("analysis/r/runtime.json").read_text(encoding="utf8"))
    for mode, expected in reference["cohort"].items():
        actual = regenerated["cohort"][mode]
        for field in ("csv_sha256", "participants", "rows", "missing", "wave_counts"):
            exact(expected[field], actual[field], f"{mode} {field}")
        for track in ("social", "biological"):
            for audit in actual[track]["diagnostics"]:
                exact(audit["r_version"], runtime["R"], "R version")
                exact(audit["nlme_version"], runtime["nlme"], "nlme version")
            truth = {(row["model"], row["term"]): row for row in expected[track]["coefficients"]}
            updated = {(row["model"], row["term"]): row for row in actual[track]["coefficients"]}
            exact(truth.keys(), updated.keys(), f"{mode} {track} term list")
            for key, row in truth.items():
                for field in ("estimate", "ci_lower", "ci_upper"):
                    close(row[field], updated[key][field], f"{mode} {track} {key} {field}", 1e-4)
        exact(expected["iptw"]["status"], actual["iptw"]["status"], f"{mode} IPTW gate")
        if actual["iptw"]["status"] == "computed":
            for row, change in zip(expected["iptw"]["weight_sensitivity"], actual["iptw"]["weight_sensitivity"], strict=True):
                close(row["estimate"], change["estimate"], "IPTW estimate")
                for bound, other in zip(row["ci95"], change["ci95"], strict=True):
                    close(bound, other, "IPTW CI")
        first, second = expected["prediction"], actual["prediction"]
        for field in ("n_train", "n_test", "features", "target_visit_year", "features_available_through_visit_year"):
            exact(first[field], second[field], f"{mode} prediction {field}")
        exact(second["participant_overlap"], 0, "participant overlap")
        exact(first["models"].keys(), second["models"].keys(), "prediction model list")
        for name, model in first["models"].items():
            for metric, record in model["metrics"].items():
                # Split points in tree models can differ across numeric libraries.
                tolerance = .04 if name.startswith("Random forest") else 1e-6
                close(record["estimate"], second["models"][name]["metrics"][metric]["estimate"],
                      f"{mode} {name} {metric}", tolerance)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("regenerated", type=Path)
    parser.add_argument("--reference", type=Path, default=Path("src/generated/results.json"))
    args = parser.parse_args()
    verify(*(json.loads(path.read_text(encoding="utf8")) for path in (args.reference, args.regenerated)))
    print("Verified release fingerprints, cohort QC, R estimates, IPTW and prediction audit.")
