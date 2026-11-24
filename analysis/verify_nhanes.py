"""Compare a regenerated NHANES aggregate against the audited release."""
import argparse
import json
import math
from pathlib import Path


def verify(expected, actual):
    if isinstance(expected, dict):
        assert expected.keys() == actual.keys()
        for name in expected:
            verify(expected[name], actual[name])
    elif isinstance(expected, list):
        assert len(expected) == len(actual)
        for pair in zip(expected, actual, strict=True):
            verify(*pair)
    elif isinstance(expected, float):
        assert math.isclose(expected, actual, rel_tol=1e-6, abs_tol=1e-8), (expected, actual)
    else:
        assert expected == actual, (expected, actual)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", type=Path, default=Path(".analysis-work/nhanes/results.json"))
    args = parser.parse_args()
    expected = json.loads(Path("public/nhanes/results.json").read_text(encoding="utf8"))
    expected.pop("sources")
    actual = json.loads(args.output.read_text(encoding="utf8"))
    verify(expected, actual)
    print("NHANES aggregate verified.")
