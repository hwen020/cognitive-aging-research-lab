"""Publish only audited VCAP summaries, never the derived visit table."""
import hashlib
import json
from pathlib import Path
from analysis.vcap import BOOK, ROOT

EXPECTED = "9388aa0d6afed2f75528b4978e0fba98371fbc3af44322fd83c8b54c9dac2b0a"

def read(name):
    return json.loads((ROOT / f"{name}.json").read_text(encoding="utf8"))

def write(path, text):
    Path(path).write_text(text, encoding="utf8", newline="\n")

def coefficients(rows):
    return "\n".join(f"| {r['term']} | {r['estimate']:.3f} | {r['lower']:.3f} to {r['upper']:.3f} |" for r in rows)

def publish():
    with BOOK.open("rb") as file:
        sha = hashlib.file_digest(file, "sha256").hexdigest()
    if sha != EXPECTED:
        raise ValueError("Workbook version mismatch")
    a, m, p = (read(name) for name in ("audit", "model", "prediction"))
    assert p["max_id_overlap"] == 0 and m["participants"] == a["eligible_people"]
    out = Path("public/vcap")
    out.mkdir(exist_ok=True)
    cite = "Source: [Salthouse (2024), VCAP, University of Virginia Dataverse, V1.0](https://doi.org/10.18130/V3/QRCQ08).\n\n"
    flow = (
        f"Demographic extract after excluding ambiguous keys: {a['participants']:,} participants, "
        f"{a['two_occasions']:,} with 2+ and {a['three_occasions']:,} with 3+ occasions. "
        f"The eligible Digit Symbol cohort has {a['eligible_people']:,} participants and {a['eligible_rows']:,} observations. "
        f"{a['repeated_people']:,} participants have repeated scores; {a['eligible_three']:,} have 3+. "
        f"Median maximum follow-up among returners is {a['followup_years_quantiles'][2]:.2f} years "
        f"(range {a['followup_years_quantiles'][0]:.2f} to {a['followup_years_quantiles'][-1]:.2f})."
    )
    table = "| Term | Estimate | 95% CI |\n| --- | ---: | --- |\n"
    methods = (
        "Join Demographics, Test Dates and DigSym1 on SubjID and Occasion. Collapse identical selected rows and exclude conflicting keys. "
        "Require occasion 1, a documented baseline date, baseline test and complete baseline covariates. Require a valid date and score on each included occasion. "
        "Time is actual elapsed days divided by 365.2425. Digit Symbol is the number of correct matches in 120 seconds (0–133). "
        "The analysis retains raw score units and models baseline age centered at 60, education centered at 16, recorded sex and age-by-time interaction. "
        "Compare participant random intercept and correlated intercept/slope by ML AIC. Coefficient intervals use nlme's t approximation."
    )
    pred = [
        f"One baseline-to-next observed eligible score pair per returning participant. Train {p['train']:,}, validation {p['validation']:,}, test {p['test']:,}. "
        f"Maximum participant overlap across partitions: {p['max_id_overlap']}. Horizon is unknown at baseline and is excluded as a feature. "
        "Candidate forest leaf sizes were selected by validation MAE. The test set compares the selected forest with the carry-forward baseline. "
        "Intervals use 1,000 bootstrap resamples of held-out participants conditional on fitted models.",
        "| Model | MAE (95% CI) | RMSE (95% CI) |\n| --- | ---: | ---: |",
    ]
    for name, row in p["metrics"].items():
        pred.append(f"| {name} | {row['mae']:.3f} ({row['mae_ci'][0]:.3f}, {row['mae_ci'][1]:.3f}) | {row['rmse']:.3f} ({row['rmse_ci'][0]:.3f}, {row['rmse_ci'][1]:.3f}) |")
    pred.append(f"Paired forest-minus-baseline MAE {p['paired_delta_mae']:.3f} (95% CI {p['paired_delta_ci'][0]:.3f} to {p['paired_delta_ci'][1]:.3f}).")
    for name, row in p["gap_groups"].items():
        pred.append(f"- {name.replace('_', ' ')}: n = {row['n']}; carry-forward MAE {row['carry_forward']:.3f}; forest MAE {row['random_forest']:.3f}.")
    diagnosis = (
        f"Random slope convergence: {m['slope_converged']}. Intercept AIC {m['intercept_aic']:.2f}; slope AIC {m['slope_aic']}. "
        f"Slope SD {m['slope_sd']}; normalized residual lag-one ACF {m['residual_lag1']:.3f}. "
        f"The negative residual autocorrelation warrants caution about the conditional covariance specification. Normalized residual quantiles (2.5%, 50%, 97.5%): {', '.join(f'{v:.3f}' for v in m['residual_quantiles'])}."
    )
    quality = flow + "\n\n" + "\n".join(
        f"- {name}: {value:,}" for name, value in a.items() if name.startswith("missing_") or name.endswith("_unmatched")
    ) + "\n\n" + "\n".join(
        f"- {name}: {counts['conflicting_key_rows']} conflicting-key rows excluded."
        for name, counts in a["key_audit"].items()
    ) + "\n\n" + "\n".join(
        f"- {label} (n = {row['n']:,}): mean baseline age {row['age0']:.1f}, education {row['educ0']:.1f}, and Digit Symbol score {row['score0']:.1f}."
        for label, row in (("Baseline-only", a["baseline_profiles"]["False"]), ("Observed repeat", a["baseline_profiles"]["True"]))
    )
    limitations = (
        "This volunteer cohort and observed-follow-up sample are susceptible to selection. A baseline-only record does not establish withdrawal, death or ineligibility. "
        "The retest indicator probes a discrete first-retest shift; it cannot isolate practice from aging or other visit differences. "
        "Observational associations do not identify causal effects. The prediction applies only to subsequent observed Digit Symbol scores, with heterogeneous time intervals, and has no clinical diagnostic interpretation."
    )
    repro = (
        f"Workbook SHA-256: `{sha}`. R {m['runtime']['R']} and nlme {m['runtime']['nlme']}. "
        "From the repository root with the authorized workbook in .analysis-work/vcap, install openpyxl, pandas, scikit-learn and NumPy, plus R nlme and jsonlite. The verified Windows environment used Python 3.11.7, pandas 2.1.4, NumPy 1.26.4, scikit-learn 1.2.2, and openpyxl 3.0.10.\n\n"
        "```sh\npython -m analysis.vcap\nRscript analysis/r/vcap.R .analysis-work/vcap/analysis-private.csv .analysis-work/vcap/model.json\n"
        "python -m analysis.vcap_prediction\npython -m analysis.vcap_release\n```\n\n"
        "Keep all row-level inputs and derived records local and untracked."
    )
    reports = {
        "LONGITUDINAL": flow + "\n\n" + methods + "\n\n" + table + coefficients(m["coefficients"]),
        "METHODS": methods,
        "DATA_QUALITY": quality,
        "MODEL_DIAGNOSTICS": diagnosis + "\n\n## Retest shift sensitivity\n\n" + table + coefficients(m["practice"])
            + "\n\n## Repeat-participant sensitivity\n\n" + table + coefficients(m["returning"]),
        "PREDICTION": "\n\n".join(pred[:1]) + "\n\n" + "\n".join(pred[1:]),
        "LIMITATIONS": limitations,
        "REPRODUCIBILITY": repro,
    }
    for key, body in reports.items():
        title = key.replace("_", " ").title()
        content = f"# VCAP {title}\n\n{cite}{body}\n"
        if key in ("LONGITUDINAL", "PREDICTION"):
            content += "\n## Limitations\n\n" + limitations + "\n"
        write(f"reports/VCAP_{key}.md", content)
        write(out / f"{key.lower()}.md", content)
    release = {"source": "VCAP Dataverse V1.0", "doi": "10.18130/V3/QRCQ08",
               "workbook_sha256": sha, "audit": a, "model": m, "prediction": p}
    write(out / "results.json", json.dumps(release, indent=2, allow_nan=False) + "\n")

if __name__ == "__main__":
    publish()
