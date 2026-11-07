"""
Unit tests for sensor nodata sanitization and missing value masking.
"""

import pytest
import numpy as np
import pandas as pd

from rsl.clean.masks import (
    mask_chirps_nodata,
    validate_clean_series,
    CHIRPS_NODATA_VAL,
)


def test_mask_chirps_nodata_series():
    """Verifies that -9999 sentinel values in pandas Series are replaced with NaN."""
    s = pd.Series([12.5, -9999.0, 0.0, -9999.0, 45.2])
    clean_s, mask_count = mask_chirps_nodata(s)

    assert mask_count == 2
    assert np.isnan(clean_s.iloc[1])
    assert np.isnan(clean_s.iloc[3])
    assert clean_s.iloc[0] == 12.5
    assert clean_s.iloc[2] == 0.0
    assert clean_s.iloc[4] == 45.2


def test_mask_chirps_nodata_numpy():
    """Verifies that -9999 sentinel values in numpy ndarrays are masked to NaN."""
    arr = np.array([0.0, -9999.0, 100.5, -9999.0])
    clean_arr, count = mask_chirps_nodata(arr)

    assert count == 2
    assert np.isnan(clean_arr[1])
    assert np.isnan(clean_arr[3])
    assert clean_arr[0] == 0.0
    assert clean_arr[2] == 100.5


def test_validate_clean_series_success():
    """Asserts that sanitized series with no -9999 passes validation."""
    clean_data = pd.Series([0.0, 15.2, np.nan, 88.0])
    assert validate_clean_series(clean_data) is True


def test_validate_clean_series_failure_on_unmasked_nodata():
    """Asserts that unmasked -9999 values trigger sanitization failure."""
    dirty_data = pd.Series([0.0, -9999.0, 15.2])
    with pytest.raises(ValueError, match="Sanitization failure: nodata values"):
        validate_clean_series(dirty_data)
