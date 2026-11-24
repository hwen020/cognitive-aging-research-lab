import pandas as pd
from analysis.vcap import clean
from analysis.vcap_prediction import FEATURES, pairs

def test_occasion_dates_anchor_elapsed_time_without_guessing():
    data = pd.DataFrame({
        "id": ["a", "a", "b", "b"], "occasion": [1, 3, 1, 2],
        "date": ["2000-01-01", "2002-01-01", "2000-01-01", "1999-01-01"],
        "age": [60, 62, 55, 54], "educ": [16] * 4, "sex": [0, 0, 1, 1],
        "score": [75, 70, 66, -99],
    })
    eligible, audit = clean(data, {})
    assert audit["nonincreasing_date_participants"] == 1
    assert audit["missing_score"] == 1
    assert eligible.id.tolist() == ["a", "a"]
    assert eligible.years.tolist() == [0, 731 / 365.2425]

def test_next_observed_score_is_never_a_feature():
    data = pd.DataFrame({
        "id": ["b", "a", "a", "a"], "years": [0, 4, 0, 3],
        "score": [51, 22, 88, 45], "age0": [60]*4, "educ0": [16]*4, "sex0": [1]*4,
    })
    observed = pairs(data)
    assert observed.id.tolist() == ["a"]
    assert observed[FEATURES].iloc[0].score == 88
    assert observed.target.tolist() == [45]
    assert observed.gap.tolist() == [3]
    assert "gap" not in FEATURES and "target" not in FEATURES

def test_public_bundle_contains_no_participant_keys_and_agrees_with_reports():
    import json
    from pathlib import Path

    public = Path("public/vcap")
    data = json.loads((public / "results.json").read_text(encoding="utf8"))
    prohibited = {"id", "subjid", "date", "date0", "occasion", "raw_rows"}

    def check(node):
        if isinstance(node, dict):
            assert not prohibited.intersection(key.lower() for key in node)
            for value in node.values():
                check(value)
        elif isinstance(node, list):
            for value in node:
                check(value)

    check(data)
    assert data["model"]["participants"] == data["audit"]["eligible_people"]
    assert data["model"]["n"] == data["audit"]["eligible_rows"]
    assert data["prediction"]["max_id_overlap"] == 0
    assert sum(data["prediction"][key] for key in ("train", "validation", "test")) == data["audit"]["repeated_people"]
    for report in public.glob("*.md"):
        assert report.read_bytes() == Path(f"reports/VCAP_{report.stem.upper()}.md").read_bytes()
