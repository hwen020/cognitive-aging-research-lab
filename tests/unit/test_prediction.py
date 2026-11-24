import pandas as pd
import pytest

from analysis.cohort import BASELINE, MARKERS, generate
from analysis.prediction import design, fit, metrics


def test_exact_metrics_on_known_fixture():
    actual = metrics([1, 2, 3], [0, 2, 4])
    assert actual == pytest.approx({"mae": 2 / 3, "rmse": (2 / 3)**.5, "r2": 0})


def test_features_use_only_baseline_and_preserve_unique_participants():
    cohort = generate()
    expected, enrolled = design(cohort)
    cohort.loc[cohort.visit_year.gt(0), MARKERS] = 999
    cohort.loc[cohort.visit_year.lt(8), "cognitive_score"] = -999
    actual, _ = design(cohort)
    pd.testing.assert_frame_equal(actual, expected)
    assert actual.columns.tolist() == BASELINE + MARKERS + ["cognitive_score"]
    assert actual.index.is_unique and len(actual) == enrolled == 2400


def test_heldout_evaluation_is_repeatable_and_reports_paired_comparison():
    cohort = generate()
    subset = cohort.loc[cohort.participant_id.le("P0220")]
    result = fit(subset, replications=20)
    assert result == fit(subset, replications=20)
    assert result["participant_overlap"] == 0
    assert result["n_train"] == 165 and result["n_test"] == 55
    assert len(result["models"]) == 5
    assert result["features_available_through_visit_year"] == 0
    assert set(result["paired_marker_comparisons"]) == {"Ridge", "Random forest"}
