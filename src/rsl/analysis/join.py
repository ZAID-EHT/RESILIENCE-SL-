"""
Relational joining of forecast runs and multi-satellite references with temporal leakage verification.
"""

from typing import List, Tuple, Union
import pandas as pd
import numpy as np


def join_forecast_and_references(
    df_forecasts: pd.DataFrame,
    df_chirps_v2: pd.DataFrame,
    df_chirps_v3_sat: pd.DataFrame,
    join_keys: List[str] = ["cell_id", "valid_date_utc", "lead_day"],
) -> pd.DataFrame:
    """
    Performs inner join on forecast and reference datasets.
    Ensures unique composite keys and no duplicate rows.
    """
    # Check duplicate keys in input
    for name, df in [("forecasts", df_forecasts), ("v2", df_chirps_v2), ("v3_sat", df_chirps_v3_sat)]:
        subset_keys = [k for k in join_keys if k in df.columns]
        if df.duplicated(subset=subset_keys).any():
            raise ValueError(f"Duplicate composite keys detected in {name} dataset!")

    merged = pd.merge(df_forecasts, df_chirps_v2, on=[k for k in join_keys if k in df_chirps_v2.columns], how="inner")
    merged = pd.merge(merged, df_chirps_v3_sat, on=[k for k in join_keys if k in df_chirps_v3_sat.columns], how="inner")

    return merged


def validate_zero_leakage(
    train_dates: Union[List[pd.Timestamp], pd.Series],
    test_dates: Union[List[pd.Timestamp], pd.Series],
    purge_days: int = 3,
) -> bool:
    """
    Asserts zero temporal leakage between training and testing evaluation folds.
    Strict condition:
        max(train_dates) + purge_days < min(test_dates)
    """
    train_max = pd.to_datetime(train_dates).max()
    test_min = pd.to_datetime(test_dates).min()

    allowed_boundary = test_min - pd.Timedelta(days=purge_days)
    if train_max > allowed_boundary:
        raise ValueError(
            f"Temporal leakage detected! Train max ({train_max}) violates "
            f"purge boundary ({allowed_boundary}) for test min ({test_min})."
        )
    return True
