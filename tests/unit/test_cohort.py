import hashlib

import pytest

from analysis.cohort import generate, simulate_incomplete, validate, write_cohort

COMPLETE_HASH = "5104d2c3ca510a4f0ac537652c3f4b76f6b4e567d42cad9029c3b24b5297de74"


def test_known_csv_digest_matches_frontend(tmp_path):
    path = tmp_path / "cohort.csv"
    cohort = generate()
    assert validate(cohort)["rows"] == 12000
    write_cohort(cohort, path)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == COMPLETE_HASH


def test_incomplete_mode_and_duplicate_rejection():
    cohort = generate()
    incomplete = simulate_incomplete(cohort)
    audit = validate(incomplete, complete=False)
    assert audit["wave_counts"][0] == 2400
    assert audit["wave_counts"][8] < audit["wave_counts"][0]
    assert audit["missing"]["ptau"] > 0
    with pytest.raises(ValueError, match="duplicate"):
        validate(cohort.iloc[[0, 0]])
