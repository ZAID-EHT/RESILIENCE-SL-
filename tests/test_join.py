"""
Unit tests for relational joins, duplicate prevention, and zero temporal leakage verification.
"""

import pytest
import pandas as pd
import numpy as np

from rsl.analysis.join import (
    join_forecast_and_references,
    validate_zero_leakage,
)


def test_join_forecast_and_references_clean():
    """Validates inner join between forecast runs and dual references."""
    dates = ["2025-05-01", "2025-05-02", "2025-05-03"]
    df_fc = pd.DataFrame({
        "cell_id": ["C1", "C1", "C1"],
        "valid_date_utc": dates,
        "lead_day": [1, 1, 1],
        "forecast_mm": [10.0, 20.0, 30.0],
    })
    df_v2 = pd.DataFrame({
        "cell_id": ["C1", "C1", "C1"],
        "valid_date_utc": dates,
        "chirps_v2_mm": [12.0, 18.0, 35.0],
    })
    df_v3 = pd.DataFrame({
        "cell_id": ["C1", "C1", "C1"],
        "valid_date_utc": dates,
        "chirps_v3_sat_mm": [11.0, 22.0, 31.0],
    })

    joined = join_forecast_and_references(df_fc, df_v2, df_v3)
    assert len(joined) == 3
    assert "forecast_mm" in joined.columns
    assert "chirps_v2_mm" in joined.columns
    assert "chirps_v3_sat_mm" in joined.columns


def test_join_detects_duplicate_composite_keys():
    """Asserts that duplicate composite keys in input tables raise ValueError."""
    df_fc_dupe = pd.DataFrame({
        "cell_id": ["C1", "C1"],
        "valid_date_utc": ["2025-05-01", "2025-05-01"],
        "lead_day": [1, 1],
        "forecast_mm": [10.0, 15.0],
    })
    df_v2 = pd.DataFrame({
        "cell_id": ["C1"],
        "valid_date_utc": ["2025-05-01"],
        "chirps_v2_mm": [12.0],
    })
    df_v3 = pd.DataFrame({
        "cell_id": ["C1"],
        "valid_date_utc": ["2025-05-01"],
        "chirps_v3_sat_mm": [11.0],
    })

    with pytest.raises(ValueError, match="Duplicate composite keys detected"):
        join_forecast_and_references(df_fc_dupe, df_v2, df_v3)


def test_validate_zero_leakage_valid():
    """Verifies that non-overlapping train and test dates with purge buffer pass validation."""
    train_dates = pd.date_range("2024-11-13", "2025-05-12")
    # Test starts 5 days after train ends (purge buffer is 3 days)
    test_dates = pd.date_range("2025-05-18", "2025-06-18")

    assert validate_zero_leakage(train_dates, test_dates, purge_days=3) is True


def test_validate_zero_leakage_catches_temporal_leakage():
    """Asserts that training data bleeding into the test period or purge buffer raises ValueError."""
    train_dates = pd.date_range("2024-11-13", "2025-05-15")
    # Test starts only 1 day after train end, violating 3-day purge buffer
    test_dates = pd.date_range("2025-05-16", "2025-06-16")

    with pytest.raises(ValueError, match="Temporal leakage detected"):
        validate_zero_leakage(train_dates, test_dates, purge_days=3)
