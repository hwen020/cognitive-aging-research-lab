"""Render standalone, aggregate-only Markdown reports from the audited bundle."""

import argparse
import json
from pathlib import Path


def display(value):
    return f"{value:.4f}"


def interval(values):
    return " to ".join(map(display, values))


def context(bundle, title):
    return [
        f"# Cognitive Aging Research Lab — {title}", "",
        "All participants, marker proxies and scores are simulated. Estimates are conditional on this generator and cannot be used for clinical or real-population conclusions.", "",
        f"Dataset seed: {bundle['seed']}. Artifact schema: {bundle['schema_version']}.",
        f"Runtime: NumPy {bundle['numpy_version']}, pandas {bundle['pandas_version']}.",
    ]


def mode_context(mode, result):
    return [
        "", f"## {mode.capitalize()} simulation", "",
        f"{result['participants']:,} participants, {result['rows']:,} observations. CSV SHA-256: `{result['csv_sha256']}`.",
        f"Visit counts: {', '.join(f'Year {year}={count:,}' for year, count in result['wave_counts'].items())}.",
        f"Missing proxy values: {', '.join(f'{marker}={result['missing'][marker]:,}' for marker in ['crp', 'ptau', 'nfl'])}.",
    ]


def social(bundle):
    lines = context(bundle, "Social research")
    lines += [
        "", "The descriptive model uses a REML participant random intercept, linear follow-up time and interactions with deprivation and baseline covariates. IPTW targets the total Year-8 mean contrast under high versus low simulated assignment.",
        "The simulator assigns exposure independently at time zero. The fitted propensity includes age, education and sex. Downstream hypertension and CRP are excluded from the adjustment set.",
        "Intervals for IPTW refit the propensity model across participant resamples. Identification of an observational effect would require assumptions about confounding, consistency, overlap and censoring.",
    ]
    for mode, result in bundle["cohort"].items():
        lines += mode_context(mode, result)
        model = result["social"]
        diagnostic = model["diagnostics"][0]
        term = next(row for row in model["coefficients"] if row["term"] == "visit_year:deprivationHigh")
        bound = interval([term["ci_lower"], term["ci_upper"]])
        lines += [
            f"R {diagnostic['r_version']} / nlme {diagnostic['nlme_version']}, {diagnostic['n']:,} model rows.",
            f"Adjusted annual slope difference: {display(term['estimate'])} points (95% CI {bound}).",
            f"Residual lag-1 ACF: {display(diagnostic['residual_lag1_acf'])}; inspect uncertainty in light of the working covariance assumption.",
        ]
        iptw = result["iptw"]
        if iptw["status"] != "computed":
            lines.append(f"IPTW effect withheld. {iptw['reason']}")
            continue
        audit = iptw["diagnostics"]
        lines += [
            f"IPTW overlap: {audit['fraction_in_common_support']:.2%} of participants; effective sample sizes (low/high): {interval(audit['ess_low_high'])}.",
            "", "| Covariate | Unweighted SMD | Weighted SMD |", "| --- | ---: | ---: |",
        ]
        lines += [f"| {row['covariate']} | {display(row['smd_before'])} | {display(row['smd_after'])} |" for row in audit["balance"]]
        lines += ["", "| Truncation per tail | Contrast | 95% CI |", "| ---: | ---: | --- |"]
        for row in iptw["weight_sensitivity"]:
            label = f"{row['tail_quantile']:.0%}"
            value = f"{display(row['estimate'])} | {interval(row['ci95'])}" if row["diagnostics"]["passes"] else "Withheld | Withheld"
            lines.append(f"| {label} | {value} |")
    return lines


def biological(bundle):
    lines = context(bundle, "Biological research")
    lines += [
        "", "R random-intercept models estimate separate associations for each marker's baseline level and its change from baseline, using marker-specific complete rows. Each mode adjusts six marker-term p-values with Benjamini–Hochberg.",
        "Prediction uses only baseline data and an observed Year-8 target, one row per eligible participant. Preprocessing and validation stay within training folds. The held-out intervals are conditional on the trained models.",
    ]
    for mode, result in bundle["cohort"].items():
        lines += mode_context(mode, result)
        model = result["biological"]
        diagnostics = {row["model"]: row for row in model["diagnostics"]}
        lines += ["", "| Marker | Term | Rows | Estimate | 95% CI | BH q |", "| --- | --- | ---: | ---: | --- | ---: |"]
        for row in model["coefficients"]:
            if row["q_bh"] is None:
                continue
            n = diagnostics[row["model"]]["n"]
            bound = interval([row["ci_lower"], row["ci_upper"]])
            lines.append(f"| {row['model']} | {row['term']} | {n:,} | {display(row['estimate'])} | {bound} | {row['q_bh']:.3g} |")
        prediction = result["prediction"]
        lines += [
            "", f"scikit-learn {prediction['sklearn_version']}. Train/test: {prediction['n_train']:,}/{prediction['n_test']:,}. Participant overlap: {prediction['participant_overlap']}.",
            "", "| Prediction model | MAE (95% CI) | RMSE (95% CI) | R² (95% CI) |", "| --- | --- | --- | --- |",
        ]
        for name, model in prediction["models"].items():
            cells = [f"{display(model['metrics'][key]['estimate'])} ({interval(model['metrics'][key]['ci95'])})" for key in ("mae", "rmse", "r2")]
            lines.append(f"| {name} | {' | '.join(cells)} |")
        lines += [
            "", "Marker contribution (paired marker-augmented minus social MAE):",
            *[f"- {model}: {display(row['delta_mae'])} ({interval(row['ci95'])})." for model, row in prediction["paired_marker_comparisons"].items()],
        ]
    return lines


def render(bundle, directory):
    directory.mkdir(parents=True, exist_ok=True)
    for filename, generate in [("social.md", social), ("biological.md", biological)]:
        lines = generate(bundle)
        lines += ["", "## Analysis source fingerprints", ""]
        lines += [f"- `{path}` — `{digest}`" for path, digest in bundle["source_sha256"].items()]
        (directory / filename).write_text("\n".join(lines) + "\n", encoding="utf8", newline="\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("src/generated/results.json"))
    parser.add_argument("--directory", type=Path, default=Path("public/reports"))
    args = parser.parse_args()
    render(json.loads(args.input.read_text(encoding="utf8")), args.directory)
