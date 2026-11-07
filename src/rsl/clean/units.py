"""
Unit conversions, physical scaling checks, and non-negative rainfall validation.
"""

from typing import Union
import numpy as np
import pandas as pd


def convert_imerg_rate_to_half_hour(rate_mm_per_hr: Union[float, np.ndarray, pd.Series]) -> Union[float, np.ndarray, pd.Series]:
    """
    Converts NASA GPM IMERG calibrated precipitation rate (mm/hr) to accumulated depth (mm)
    over a 30-minute observation window.
    Depth (mm) = Rate (mm/hr) * 0.5 hr.
    """
    return rate_mm_per_hr * 0.5


def validate_non_negative_precipitation(
    values: Union[float, np.ndarray, pd.Series],
    tol: float = 1e-6,
) -> bool:
    """
    Validates that physical precipitation values are strictly non-negative (ignoring NaNs).
    Raises ValueError if any negative precipitation values are found beyond tolerance.
    """
    arr = np.asarray(values, dtype=float)
    valid_mask = ~np.isnan(arr)
    if np.any(arr[valid_mask] < -tol):
        neg_count = np.sum(arr[valid_mask] < -tol)
        min_val = np.min(arr[valid_mask])
        raise ValueError(
            f"Physical precipitation cannot be negative. Found {neg_count} invalid values (minimum: {min_val})."
        )
    return True
