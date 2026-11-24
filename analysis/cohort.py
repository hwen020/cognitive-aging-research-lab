"""Reproduce the browser's fixed-seed synthetic cohort and audit its contract."""

import argparse
import math
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261123
WAVES = (0, 2, 4, 6, 8)
MARKERS = ["crp", "ptau", "nfl"]
BASELINE = ["age_at_baseline", "sex", "deprivation", "education_years", "hypertension"]
COLUMNS = ["participant_id", "visit_year", "age_at_baseline", "age_at_visit",
           "sex", "deprivation", "education_years", "hypertension", *MARKERS,
           "cognitive_score"]


def generate():
    state = SEED

    def uniform():
        nonlocal state
        state = (1664525 * state + 1013904223) % 2**32
        return state / 2**32

    def normal():
        return math.sqrt(-2 * math.log(max(uniform(), 1e-12))) * math.cos(
            2 * math.pi * uniform()
        )

    rows = []
    for index in range(1, 2401):
        age = round(54 + uniform() * 30, 1)
        sex = "Female" if uniform() < .54 else "Male"
        high = uniform() < .49
        education = round(9 + uniform() * 11, 1)
        htn = uniform() < (age - 48) / 65 + .12 * high
        baseline = 111 - .21 * (age - 55) + .43 * (education - 12) - 2.8 * high - 1.5 * htn + normal() * 3.1
        inflammation = max(.15, 1.3 + normal() * .35 + .47 * htn + .38 * high)
        for year in WAVES:
            change = -.52 * year - .033 * year * (age - 55) - .24 * year * high - .12 * year * htn
            crp = max(.1, inflammation + year * .06 + normal() * .25)
            ptau = max(0, 12 + .18 * (age - 55) + .48 * year + normal() * 2.5)
            nfl = max(0, 16 + .26 * (age - 55) + .51 * year + normal() * 3.4)
            score = baseline + change - .2 * crp - .055 * ptau + normal() * .9
            rows.append((f"P{index:04}", year, age, round(age + year, 1), sex,
                         "High" if high else "Low", education, "Yes" if htn else "No",
                         round(crp, 2), round(ptau, 2), round(nfl, 2), round(score, 1)))
    return pd.DataFrame(rows, columns=COLUMNS)


def simulate_incomplete(complete):
    """Monotone dropout and intermittent marker omissions from separate RNG."""
    rng = np.random.default_rng(SEED + 1)
    frame = complete.copy()
    baseline = frame.loc[frame.visit_year.eq(0)].set_index("participant_id")
    keep = pd.Series(True, index=baseline.index)
    for wave in WAVES[1:]:
        probability = .025 + .025 * baseline.deprivation.eq("High") + .02 * baseline.hypertension.eq("Yes")
        keep &= rng.random(len(baseline)) >= probability
        visit = frame.visit_year.eq(wave)
        frame = frame.loc[~visit | frame.participant_id.isin(keep.index[keep])]
    for marker in MARKERS:
        probability = .03 + .02 * frame.deprivation.eq("High") + .03 * frame.visit_year.eq(8)
        frame.loc[rng.random(len(frame)) < probability, marker] = np.nan
    return frame


def validate(frame, complete=True):
    if list(frame.columns) != COLUMNS or frame.duplicated(["participant_id", "visit_year"]).any():
        raise ValueError("Unexpected columns or duplicate participant/wave")
    required = [field for field in COLUMNS if complete or field not in MARKERS]
    if frame[required].isna().any().any():
        raise ValueError("Required fields contain missing values")
    grouped = frame.groupby("participant_id", sort=False)
    if len(grouped) != 2400 or not frame.participant_id.str.fullmatch(r"P\d{4}").all():
        raise ValueError("Unexpected participant keys")
    for visits in grouped.visit_year:
        values = tuple(visits[1])
        if values != (WAVES if complete else WAVES[:len(values)]):
            raise ValueError("Unexpected visit schedule")
    if grouped[BASELINE].nunique().gt(1).any().any():
        raise ValueError("Baseline fields changed within a participant")
    if (not np.allclose(frame.age_at_visit, frame.age_at_baseline + frame.visit_year)
            or not frame.age_at_baseline.between(54, 84).all()
            or not frame.education_years.between(9, 20).all()
            or not frame.cognitive_score.between(0, 150).all()
            or any(not frame[m].dropna().between(0, 100).all() for m in MARKERS)
            or not frame.sex.isin(["Female", "Male"]).all()
            or not frame.deprivation.isin(["Low", "High"]).all()
            or not frame.hypertension.isin(["Yes", "No"]).all()):
        raise ValueError("Invalid cohort values")
    return {
        "participants": len(grouped),
        "rows": len(frame),
        "wave_counts": frame.visit_year.value_counts().sort_index().to_dict(),
        "missing": frame.isna().sum().to_dict(),
    }


def write_cohort(frame, path):
    # Canonical browser-compatible decimals: no trailing zeroes or locale changes.
    frame.to_csv(path, index=False, lineterminator="\n", float_format=lambda value: format(value, "g"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    args.directory.mkdir(parents=True, exist_ok=True)
    cohort = generate()
    for mode, frame in [("complete", cohort), ("incomplete", simulate_incomplete(cohort))]:
        print(mode, validate(frame, mode == "complete"))
        write_cohort(frame, args.directory / f"{mode}.csv")
