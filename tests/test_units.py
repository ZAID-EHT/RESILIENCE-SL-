"""
Unit tests for physical unit conversions and non-negative rainfall validation.
"""

import pytest
import numpy as np
import pandas as pd

from rsl.clean.units import (
    convert_imerg_rate_to_half_hour,
    validate_non_negative_precipitation,
)


def test_convert_imerg_rate_to_half_hour_scalar():
    """Validates that calibrated rate mm/hr multiplied by 0.5 yields mm accumulation."""
    rate = 10.0  # mm/hr
    accum = convert_imerg_rate_to_half_hour(rate)
    assert accum == 5.0


def test_convert_imerg_rate_to_half_hour_vector():
    """Validates vector conversion for pandas Series and numpy ndarray."""
    rates = np.array([0.0, 2.4, 12.0, 50.0])
    expected = np.array([0.0, 1.2, 6.0, 25.0])
    np.testing.assert_allclose(convert_imerg_rate_to_half_hour(rates), expected)

    series = pd.Series([10.0, 20.0])
    np.testing.assert_allclose(convert_imerg_rate_to_half_hour(series), [5.0, 10.0])


def test_validate_non_negative_precipitation_valid():
    """Validates that non-negative arrays (including zeros and NaNs) pass validation."""
    valid_data = [0.0, 1.5, 45.2, np.nan, 120.0]
    assert validate_non_negative_precipitation(valid_data) is True


def test_validate_non_negative_precipitation_invalid():
    """Asserts that physical precipitation values below zero raise ValueError."""
    invalid_data = [10.0, -0.5, 25.0]
    with pytest.raises(ValueError, match="Physical precipitation cannot be negative"):
        validate_non_negative_precipitation(invalid_data)
