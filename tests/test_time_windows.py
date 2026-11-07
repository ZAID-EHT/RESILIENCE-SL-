"""
Unit tests for time window integration, preceding-hour UTC summation, and operational cycle strata.
"""

import pytest
import pandas as pd
import numpy as np

from rsl.clean.time_windows import (
    stratum_for_run,
    integrate_preceding_hour_utc,
    get_lead_slice,
    get_season,
)


def test_stratum_for_run_exact_boundaries():
    """Verifies cycle 49r1 and 50r1 operational boundary transitions at 06:00 UTC."""
    # S0: strictly before 2024-11-12 06:00 UTC
    assert stratum_for_run("2024-03-14T00:00:00Z") == "S0"
    assert stratum_for_run("2024-11-12T00:00:00Z") == "S0"
    assert stratum_for_run("2024-11-12 00:00:00") == "S0"

    # S1: from 2024-11-12 06:00 UTC up to strictly before 2026-05-12 06:00 UTC
    assert stratum_for_run("2024-11-12T06:00:00Z") == "S1"
    assert stratum_for_run("2024-11-13T00:00:00Z") == "S1"
    assert stratum_for_run("2025-06-01T00:00:00Z") == "S1"
    assert stratum_for_run("2026-05-12T00:00:00Z") == "S1"

    # S2: from 2026-05-12 06:00 UTC onward
    assert stratum_for_run("2026-05-12T06:00:00Z") == "S2"
    assert stratum_for_run("2026-05-13T00:00:00Z") == "S2"
    assert stratum_for_run("2026-08-30T00:00:00Z") == "S2"


def test_stratum_for_run_datetime_types():
    """Ensures stratum_for_run handles string, pd.Timestamp, and datetime interchangeably."""
    ts_pd = pd.Timestamp("2024-11-12 06:00:00", tz="UTC")
    ts_naive = pd.Timestamp("2024-11-12 06:00:00")
    assert stratum_for_run(ts_pd) == "S1"
    assert stratum_for_run(ts_naive) == "S1"


def test_integrate_preceding_hour_utc_complete_day():
    """Tests 24-hour summation using the D 01:00 through D+1 00:00 UTC convention."""
    base_date = pd.Timestamp("2025-05-15 00:00:00", tz="UTC")
    # Hours from D 00:00 to D+1 01:00
    times = [base_date + pd.Timedelta(hours=h) for h in range(26)]
    
    # Preceding hour values: 1.0 mm for every hour
    precip = [np.nan] + [1.0] * 24 + [5.0]  # index 0 is nan, next 24 are 1.0, 25th is 5.0
    
    df = pd.DataFrame({"time": times, "precipitation": precip})

    daily_sum = integrate_preceding_hour_utc(df, "2025-05-15")
    # Expected: exactly 24.0 mm (summing 01:00 to next day 00:00)
    assert daily_sum == 24.0


def test_integrate_preceding_hour_utc_index_0_null_ignored():
    """Tests that Index 0 (D 00:00) null value in Open-Meteo single runs does not corrupt summation."""
    base_date = pd.Timestamp("2025-05-15 00:00:00", tz="UTC")
    times = [base_date + pd.Timedelta(hours=h) for h in range(25)]
    # Index 0 is explicitly NaN
    precip = [np.nan] + [2.0] * 24
    df = pd.DataFrame({"time": times, "precipitation": precip})

    daily_sum = integrate_preceding_hour_utc(df, "2025-05-15")
    assert daily_sum == 48.0


def test_integrate_preceding_hour_missing_hour_dropped_never_zero_filled():
    """Asserts that if any of the 24 required hours is missing or NaN, np.nan is returned."""
    base_date = pd.Timestamp("2025-05-15 00:00:00", tz="UTC")
    times = [base_date + pd.Timedelta(hours=h) for h in range(25)]
    precip = [np.nan] + [2.0] * 24
    # Corrupt hour 14 to NaN
    precip[14] = np.nan
    df = pd.DataFrame({"time": times, "precipitation": precip})

    daily_sum = integrate_preceding_hour_utc(df, "2025-05-15")
    assert np.isnan(daily_sum)


def test_get_lead_slice_leads():
    """Verifies that lead slices 1, 2, 3 correctly extract 24h windows from run initialization."""
    init_date = pd.Timestamp("2025-05-15 00:00:00", tz="UTC")
    # Create 96 hours of hourly forecast (Hours 1 to 96 from init)
    times = [init_date + pd.Timedelta(hours=h) for h in range(1, 97)]
    # Hours 1-24 (0-24h): 1.0mm
    # Hours 25-48 (24-48h, Lead 1): 2.0mm -> sum = 48.0mm
    # Hours 49-72 (48-72h, Lead 2): 3.0mm -> sum = 72.0mm
    # Hours 73-96 (72-96h, Lead 3): 4.0mm -> sum = 96.0mm
    precip = [1.0] * 24 + [2.0] * 24 + [3.0] * 24 + [4.0] * 24
    df = pd.DataFrame({"time": times, "precipitation": precip})

    # Lead 1: valid day 2025-05-16 (hours 25 to 48)
    assert get_lead_slice(df, init_date, lead_day=1) == 48.0
    # Lead 2: valid day 2025-05-17 (hours 49 to 72)
    assert get_lead_slice(df, init_date, lead_day=2) == 72.0
    # Lead 3: valid day 2025-05-18 (hours 73 to 96)
    assert get_lead_slice(df, init_date, lead_day=3) == 96.0

    # Invalid lead raises error
    with pytest.raises(ValueError):
        get_lead_slice(df, init_date, lead_day=4)


def test_get_season_mapping():
    """Tests Sri Lankan seasonal monsoon and inter-monsoon month assignments."""
    assert get_season(12) == "NE"
    assert get_season(1) == "NE"
    assert get_season(2) == "NE"
    assert get_season(3) == "IM1"
    assert get_season(4) == "IM1"
    assert get_season(5) == "SW"
    assert get_season(9) == "SW"
    assert get_season(10) == "IM2"
    assert get_season(11) == "IM2"

    with pytest.raises(ValueError):
        get_season(13)
