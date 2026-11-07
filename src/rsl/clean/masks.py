"""
Missing value masks and sensor nodata sanitization.
"""

from typing import Tuple, Union
import numpy as np
import pandas as pd


CHIRPS_NODATA_VAL = -9999.0


def mask_chirps_nodata(
    series_or_array: Union[pd.Series, np.ndarray],
    nodata_value: float = CHIRPS_NODATA_VAL,
) -> Tuple[Union[pd.Series, np.ndarray], int]:
    """
    Identifies and masks CHIRPS nodata sentinel values (-9999) to np.nan.
    Returns:
        (sanitized_series_or_array, count_of_masked_cells)
    """
    if isinstance(series_or_array, pd.Series):
        mask = (series_or_array == nodata_value) | (series_or_array < -9000.0)
        count = int(mask.sum())
        clean_s = series_or_array.copy()
        clean_s[mask] = np.nan
        return clean_s, count
    else:
        arr = np.array(series_or_array, dtype=float, copy=True)
        mask = (arr == nodata_value) | (arr < -9000.0)
        count = int(np.sum(mask))
        arr[mask] = np.nan
        return arr, count


def validate_clean_series(arr: Union[pd.Series, np.ndarray]) -> bool:
    """Verifies that no -9999 nodata values remain in the series."""
    vals = np.asarray(arr, dtype=float)
    valid_vals = vals[~np.isnan(vals)]
    if np.any(valid_vals < -9000.0):
        raise ValueError("Sanitization failure: nodata values (-9999) detected in numerical series!")
    return True
