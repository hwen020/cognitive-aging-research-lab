import pandas as pd
import pytest

from analysis.nhanes import KEY, merge_components


def test_cycle_key_and_mec_join():
    demo = pd.DataFrame({"cycle": [2011, 2013, 2013], "SEQN": [1, 1, 2]})
    marker = pd.DataFrame({"cycle": [2013, 2011], "SEQN": [1, 1], "marker": [9, 5]})
    result = merge_components(demo, marker)
    assert result[KEY].equals(demo)
    assert result.marker[:2].tolist() == [5, 9]
    assert pd.isna(result.marker.iloc[2])


def test_duplicate_component_record_fails():
    frame = pd.DataFrame({"cycle": [2011], "SEQN": [1]})
    with pytest.raises(pd.errors.MergeError):
        merge_components(frame, pd.concat([frame, frame]))
