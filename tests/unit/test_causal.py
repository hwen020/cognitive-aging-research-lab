import numpy as np

from analysis.causal import analyze, weighted_difference
from analysis.cohort import generate, simulate_incomplete


def test_weighted_difference_against_hand_calculation():
    assert weighted_difference(np.array([0, 4, 5, 9]), np.array([False, False, True, True]),
                               np.array([3, 1, 1, 3])) == 7


def test_overlap_failure_does_not_publish_a_contrast():
    cohort = generate()
    cohort["deprivation"] = np.where(cohort.age_at_baseline > 69, "High", "Low")
    for frame in (cohort, simulate_incomplete(generate())):
        result = analyze(frame, replications=20)
        assert result["status"] == "withheld"
        assert "weight_sensitivity" not in result


def test_full_cohort_has_balanced_weights_and_repeatable_uncertainty():
    result = analyze(generate(), replications=30)
    assert result["status"] == "computed"
    assert result == analyze(generate(), replications=30)
    assert max(abs(row["smd_after"]) for row in result["diagnostics"]["balance"]) < .10
    assert [row["tail_quantile"] for row in result["weight_sensitivity"]] == [0, .01, .05]
    for row in result["weight_sensitivity"]:
        assert row["ci95"][0] < row["estimate"] < row["ci95"][1]
