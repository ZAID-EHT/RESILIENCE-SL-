"""
Time window integration, operational cycle stratum assignment, and seasonal definitions.
"""

from datetime import datetime, timezone
from typing import Optional, Union
import numpy as np
import pandas as pd


CYCLE_49R1_TRANSITION = pd.Timestamp("2024-11-12 06:00:00", tz="UTC")
CYCLE_50R1_TRANSITION = pd.Timestamp("2026-05-12 06:00:00", tz="UTC")
RETROSPECTIVE_START = pd.Timestamp("2024-03-14 00:00:00", tz="UTC")


def parse_utc_timestamp(ts: Union[str, datetime, pd.Timestamp]) -> pd.Timestamp:
    """Normalize any timestamp to UTC-aware pandas Timestamp."""
    t = pd.to_datetime(ts)
    if t.tz is None:
        t = t.tz_localize("UTC")
    else:
        t = t.tz_convert("UTC")
    return t


def stratum_for_run(run_utc: Union[str, datetime, pd.Timestamp]) -> str:
    """
    Assigns ECMWF forecast run to its respective operational or retrospective cycle stratum.

    Stratum Rules:
    - S0 (Retrospective / 49r1 Hindcast): runs strictly before 2024-11-12T06:00Z
    - S1 (Operational Era Cycle 49r1): runs from 2024-11-12T06:00Z up to strictly before 2026-05-12T06:00Z
    - S2 (Operational Era Cycle 50r1): runs from 2026-05-12T06:00Z onward
    """
    t = parse_utc_timestamp(run_utc)

    if t < CYCLE_49R1_TRANSITION:
        return "S0"
    elif t < CYCLE_50R1_TRANSITION:
        return "S1"
    else:
        return "S2"


def get_season(month: int) -> str:
    """
    Returns the monsoon regime in Sri Lanka given a 1-based calendar month:
    - Northeast Monsoon (NE): Dec, Jan, Feb (12, 1, 2)
    - First Inter-Monsoon (IM1): Mar, Apr (3, 4)
    - Southwest Monsoon (SW): May, Jun, Jul, Aug, Sep (5, 6, 7, 8, 9)
    - Second Inter-Monsoon (IM2): Oct, Nov (10, 11)
    """
    if month in (12, 1, 2):
        return "NE"
    elif month in (3, 4):
        return "IM1"
    elif month in (5, 6, 7, 8, 9):
        return "SW"
    elif month in (10, 11):
        return "IM2"
    else:
        raise ValueError(f"Invalid month: {month}. Must be between 1 and 12.")


def integrate_preceding_hour_utc(
    df_hourly: pd.DataFrame,
    target_date_utc: Union[str, datetime, pd.Timestamp],
    time_col: str = "time",
    precip_col: str = "precipitation",
) -> float:
    """
    Integrates 24 hourly values for valid UTC date D under the 'sum of preceding hour' convention.
    Valid UTC day D spans timestamps:
        D 01:00 through (D+1) 00:00 UTC.

    Rejection criteria:
    - If any of the 24 required hours is missing or NaN, returns np.nan (never zero-filled).
    - Index 0 (D 00:00) is ignored / expected to be null in Open-Meteo single runs.
    """
    t0 = parse_utc_timestamp(target_date_utc).floor("D")
    expected_hours = [t0 + pd.Timedelta(hours=h) for h in range(1, 25)]

    df = df_hourly.copy()
    if df[time_col].dtype != "datetime64[ns, UTC]":
        df[time_col] = pd.to_datetime(df[time_col], utc=True)

    df_indexed = df.set_index(time_col)

    # Check presence of all 24 timestamps
    for h in expected_hours:
        if h not in df_indexed.index:
            return np.nan
        val = df_indexed.loc[h, precip_col]
        if pd.isna(val):
            return np.nan

    vals = [float(df_indexed.loc[h, precip_col]) for h in expected_hours]
    return float(np.sum(vals))


def get_lead_slice(
    df_forecast_hourly: pd.DataFrame,
    run_init_utc: Union[str, datetime, pd.Timestamp],
    lead_day: int,
    time_col: str = "time",
    precip_col: str = "precipitation",
) -> float:
    """
    Extracts integrated 24-hour precipitation for a specified forecast lead day:
    - Lead 1: 24-48h from 00 UTC run init (valid day: init + 1 day)
    - Lead 2: 48-72h from 00 UTC run init (valid day: init + 2 days)
    - Lead 3: 72-96h from 00 UTC run init (valid day: init + 3 days)
    """
    if lead_day not in (1, 2, 3):
        raise ValueError(f"Invalid lead_day: {lead_day}. Supported leads are 1, 2, 3.")

    t_init = parse_utc_timestamp(run_init_utc).floor("D")
    target_date = t_init + pd.Timedelta(days=lead_day)
    return integrate_preceding_hour_utc(df_forecast_hourly, target_date, time_col, precip_col)
