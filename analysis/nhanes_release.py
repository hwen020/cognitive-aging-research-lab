"""Build aggregate-only public reports from the real R output."""
import json
from pathlib import Path

from analysis.nhanes import PIN, ROOT

SOURCE = Path("public/nhanes")


def report(data, track):
    methods = (
        "Survey-weighted DSST models adjust for age, recorded sex, race/Hispanic-origin category, and cycle. "
        "Education is coded as five levels, with college graduate or above as the reference; "
        "PIR is a poverty-income ratio point."
    )
    if track == "biological":
        methods += " The joint model adds HbA1c per percentage point and systolic pressure per 10 mm Hg."
    lines = [
        f"# NHANES 2011–2014 | {track.capitalize()} research", "",
        "Public CDC/NCHS data from two independent survey cycles. Outcomes are measured cognitive test scores. "
        "The results describe cross-sectional associations and concurrent prediction.", "",
        methods, "",
        "MEC examination weight divided by two; cycle-nested masked strata and PSUs. "
        "The full examined sample defines the survey design before the age-60+ domain restriction. "
        "Models use complete cases.", "",
        f"R {data['runtime']['r']}; survey {data['runtime']['survey']}.", "",
        "## Sample flow", "",
        *[f"- {label.replace('_', ' ')}: {n:,}" for label, n in data["counts"].items()],
        "", "## Missingness in the examined age-60+ domain", "",
        *[f"- {label}: {value:.2%}" for label, value in data["missing_fraction"].items()],
        "", "## Model results", "",
    ]
    for label, model in data[track].items():
        lines.extend([f"### {label.upper()} (n = {model['n']:,})", "", f"`{model['formula']}`", "",
                      f"Residual RMSE: {model['weighted_residual_rmse']:.3f}; residual df: {model['df']}.", "",
                      "| Exposure | Estimate | 95% CI | BH q |", "| --- | ---: | --- | ---: |"])
        for row in model["coefficients"]:
            if row["q_bh"] is not None:
                lines.append(f"| {row['term']} | {row['estimate']:.3f} | {row['lower']:.3f} to {row['upper']:.3f} | {row['q_bh']:.4g} |")
        lines.append("")
    lines.extend(["## Sensitivity", ""])
    summary = data["sensitivity"]
    if track == "social":
        for key in ("social_on_bio_complete", "social_age_70_plus"):
            model = summary[key]
            row = next(row for row in model['coefficients'] if row['term'] == 'pir')
            lines.append(f"- {key}: n = {model['n']:,}, PIR coefficient {row['estimate']:.3f} (95% CI {row['lower']:.3f} to {row['upper']:.3f}).")
    else:
        lines.append(f"- Joint quadratic-term p-value: {summary['bio_quadratic_joint_p']:.4g}.")
        lines.append(f"- Unweighted clinical predictor correlation: {summary['predictor_correlation']:.3f}.")
        for key, terms in (("unadjusted_hba1c", ["hba1c"]), ("unadjusted_sbp", ["sbp10"]),
                           ("bio_two_bp_readings", ["hba1c", "sbp10"])):
            model = summary[key]
            for row in model["coefficients"]:
                if row["term"] in terms:
                    lines.append(f"- {key}, {row['term']}: n = {model['n']:,}, estimate {row['estimate']:.3f} (95% CI {row['lower']:.3f} to {row['upper']:.3f}).")
        p = data["prediction"]
        lines.extend(["", "## Predictive performance", "",
                      f"Train 2011–2012: {p['train']:,}. Test 2013–2014: {p['test']:,}. Overlap: {p['overlap']}.",
                      "Metrics are unweighted in the holdout complete cases.", "",
                      "| Model | MAE | RMSE | R² |", "| --- | ---: | ---: | ---: |"])
        for label, row in p["metrics"].items():
            lines.append(f"| {label} | {row['mae']:.3f} | {row['rmse']:.3f} | {row['r2']:.3f} |")
        lo, hi = p["paired_ci95"]
        lines.extend(["", f"Paired augmented-minus-social MAE = {p['paired_mae_difference']:.3f} "
                          f"(95% masked-PSU bootstrap interval {lo:.3f} to {hi:.3f}). "
                          "Negative values favor the augmented model. The interval conditions on fitted models."])
    lines.extend(["", "## Interpretation and reproduction", "",
                  "Residual summaries are model checks. Selection into cognitive test completion and missing predictors can alter the modeled domain. "
                  "Test language, age top coding, omitted confounding and measurement limitations can affect associations. These cycles cannot identify cognitive decline or treatment effects.", "",
                  "Run `python -m analysis.nhanes`, then `Rscript --vanilla analysis/r/nhanes.R` from the repository root. "
                  "The source list is also available in the downloadable aggregate JSON.", "",
                  "### Official source versions and hashes", ""])
    for name, entry in data["sources"].items():
        lines.append(f"- {name}, {entry.get('First Published', 'version pinned by hash')}. "
                     f"XPT SHA-256 `{entry['XPT']['sha256']}`. [CDC codebook]({entry['htm']['url']})")
    return "\n".join(lines) + "\n"


def publish():
    data = json.loads((ROOT / "results.json").read_text(encoding="utf8"))
    data["sources"] = json.loads(PIN.read_text(encoding="utf8"))
    SOURCE.mkdir(exist_ok=True)
    for track in ("social", "biological"):
        (SOURCE / f"{track}.md").write_text(report(data, track), encoding="utf8", newline="\n")
    Path("src/generated/nhanes.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf8", newline="\n")
    (SOURCE / "results.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf8", newline="\n")


if __name__ == "__main__":
    publish()
