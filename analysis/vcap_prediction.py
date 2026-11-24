"""Participant-disjoint prediction of the next observed Digit Symbol score."""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

FEATURES = ["score", "age0", "educ0", "sex0"]


def pairs(data):
    ordered = data.sort_values(["id", "years"]).copy()
    group = ordered.groupby("id")
    ordered["target"] = group.score.shift(-1)
    ordered["gap"] = group.years.shift(-1) - ordered.years
    return ordered.loc[ordered.gap.gt(0)].groupby("id").head(1)


def analyze(frame):
    train, pool = train_test_split(frame, test_size=.4, random_state=312)
    validation, test = train_test_split(pool, test_size=.5, random_state=313)
    overlap = max(len(set(a.id) & set(b.id)) for a,b in [(train, validation),(train, test),(validation,test)])
    if overlap:
        raise ValueError("Participant overlap")
    candidates = []
    for leaf in [5, 15, 30]:
        model = RandomForestRegressor(n_estimators=150, min_samples_leaf=leaf, random_state=314, n_jobs=1)
        model.fit(train[FEATURES], train.target)
        candidates.append((np.abs(validation.target-model.predict(validation[FEATURES])).mean(), leaf, model))
    _, leaf, fitted = min(candidates, key=lambda row: row[0])
    y = test.target.to_numpy()
    res = {}
    diffs = {}
    rng = np.random.default_rng(315)
    ix = rng.integers(len(test), size=(1000, len(test)))
    for name, prediction in {"carry_forward": test.score.to_numpy(), "random_forest": fitted.predict(test[FEATURES])}.items():
        errors = prediction - y
        diffs[name] = abs(errors)
        res[name] = {"mae": float(abs(errors).mean()), "rmse": float((errors**2).mean()**.5),
                     "mae_ci": np.quantile(abs(errors[ix]).mean(axis=1), [.025,.975]).tolist(),
                     "rmse_ci": np.quantile((errors[ix]**2).mean(axis=1)**.5, [.025,.975]).tolist()}
    difference = diffs["random_forest"] - diffs["carry_forward"]
    groups = {}
    for name, mask in {"up_to_3_years": test.gap.le(3), "over_3_years": test.gap.gt(3)}.items():
        if mask.sum() >= 30:
            groups[name] = {"n": int(mask.sum()), **{k: float(v[mask].mean()) for k,v in diffs.items()}}
    return {"train": len(train), "validation": len(validation), "test": len(test), "max_id_overlap": overlap,
            "selected_min_leaf": leaf, "metrics": res, "paired_delta_mae": float(difference.mean()),
            "paired_delta_ci": np.quantile(difference[ix].mean(axis=1), [.025,.975]).tolist(),
            "gap_groups": groups}


if __name__ == "__main__":
    root = Path(".analysis-work/vcap")
    result = analyze(pairs(pd.read_csv(root / "analysis-private.csv")))
    (root / "prediction.json").write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf8")
