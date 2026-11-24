"""Baseline-only prediction of the synthetic Year-8 cognitive score."""

import numpy as np
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, GroupKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from analysis.cohort import BASELINE, MARKERS, SEED


def design(frame):
    baseline = frame.loc[frame.visit_year.eq(0), ["participant_id", *BASELINE, *MARKERS]]
    endpoint = frame.loc[frame.visit_year.eq(8), ["participant_id", "cognitive_score"]]
    joined = baseline.merge(endpoint, on="participant_id", validate="one_to_one").set_index("participant_id")
    return joined.sort_index(), len(baseline)


def metrics(y, pred):
    return {"mae": mean_absolute_error(y, pred), "rmse": mean_squared_error(y, pred)**.5,
            "r2": r2_score(y, pred)}


def fit(frame, replications=500):
    joined, enrolled = design(frame)
    train, test = train_test_split(joined, test_size=.25, random_state=SEED)
    assert not set(train.index).intersection(test.index)
    y_train, y_test = train.cognitive_score, test.cognitive_score.to_numpy()
    rng = np.random.default_rng(SEED)
    samples = rng.integers(len(test), size=(replications, len(test)))
    model_results = {}
    model_predictions = {}

    def record(name, pred):
        estimates = metrics(y_test, pred)
        draws = [metrics(y_test[i], pred[i]) for i in samples]
        by_sex = {}
        for group in sorted(test.sex.unique()):
            mask = test.sex.eq(group).to_numpy()
            by_sex[group] = {"n": int(mask.sum()), "mae": mean_absolute_error(y_test[mask], pred[mask])}
        model_results[name] = {
            "metrics": {key: {"estimate": value, "ci95": np.quantile([d[key] for d in draws], [.025, .975]).tolist()}
                        for key, value in estimates.items()},
            "by_synthetic_sex": by_sex,
        }
        model_predictions[name] = pred

    dummy = DummyRegressor(strategy="mean").fit(np.zeros((len(train), 1)), y_train)
    record("Training mean", dummy.predict(np.zeros((len(test), 1))))
    for biomarkers in (False, True):
        fields = BASELINE + (MARKERS if biomarkers else [])
        categories = ["sex", "deprivation", "hypertension"]
        numerical = [field for field in fields if field not in categories]
        transform = ColumnTransformer([
            ("number", Pipeline([("impute", SimpleImputer(strategy="median")),
                                 ("scale", StandardScaler())]), numerical),
            ("category", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                                   ("encoder", OneHotEncoder(handle_unknown="ignore"))]), categories),
        ])
        estimators = [
            ("Ridge", Ridge(), {"model__alpha": [.1, 1, 10, 100]}),
            ("Random forest", RandomForestRegressor(n_estimators=100, random_state=SEED),
             {"model__min_samples_leaf": [5, 15, 40]}),
        ]
        for label, estimator, grid in estimators:
            name = label + (" + markers" if biomarkers else " social")
            pipe = Pipeline([("preprocess", transform), ("model", estimator)])
            search = GridSearchCV(pipe, grid, cv=GroupKFold(n_splits=5),
                                  scoring="neg_mean_absolute_error", error_score="raise")
            search.fit(train[fields], y_train, groups=train.index)
            record(name, search.predict(test[fields]))
            model_results[name]["best_parameters"] = search.best_params_
            if biomarkers:
                importance = permutation_importance(search, test[fields], y_test, n_repeats=10,
                                                    random_state=SEED, scoring="neg_mean_absolute_error")
                model_results[name]["permutation_mae_increase"] = dict(zip(fields, importance.importances_mean.tolist()))

    comparisons = {}
    for label in ("Ridge", "Random forest"):
        social = np.abs(y_test - model_predictions[label + " social"])
        augmented = np.abs(y_test - model_predictions[label + " + markers"])
        paired = augmented - social
        comparisons[label] = {"delta_mae": float(paired.mean()),
                              "ci95": np.quantile(paired[samples].mean(axis=1), [.025, .975]).tolist()}
    return {
        "seed": SEED, "sklearn_version": sklearn.__version__, "bootstrap_replications": replications,
        "features_available_through_visit_year": 0, "target_visit_year": 8,
        "enrolled": enrolled, "eligible": len(joined), "n_train": len(train), "n_test": len(test),
        "participant_overlap": len(train.index.intersection(test.index)),
        "features": {"social": BASELINE, "augmented": BASELINE + MARKERS},
        "models": model_results, "paired_marker_comparisons": comparisons,
        "limitations": ["All records are synthetic.", "Eligibility requires observed Year-8 cognition.",
                        "Bootstrap uncertainty is conditional on trained models and the holdout sample."],
    }
