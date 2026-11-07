"""
Atmospheric forecast verification metrics and the Two-Reference Claim Rule.
"""

from typing import Dict, Optional, Tuple, Union
import numpy as np
import pandas as pd


def compute_bias(df: pd.DataFrame, forecast_col: str = "forecast_mm", obs_col: str = "observed_mm") -> float:
    return float(np.mean(df[forecast_col] - df[obs_col]))


def compute_mae(df: pd.DataFrame, forecast_col: str = "forecast_mm", obs_col: str = "observed_mm") -> float:
    return float(np.mean(np.abs(df[forecast_col] - df[obs_col])))


def compute_rmse(df: pd.DataFrame, forecast_col: str = "forecast_mm", obs_col: str = "observed_mm") -> float:
    return float(np.sqrt(np.mean((df[forecast_col] - df[obs_col]) ** 2)))


def calculate_metrics(
    df: pd.DataFrame,
    forecast_col: str = "forecast_mm",
    obs_col: str = "observed_mm",
) -> Dict[str, float]:
    """Calculates bias, MAE, and RMSE in mm/day."""
    valid_mask = (~df[forecast_col].isna()) & (~df[obs_col].isna())
    sub = df[valid_mask]
    if sub.empty:
        return {"bias_mm": np.nan, "mae_mm": np.nan, "rmse_mm": np.nan}

    return {
        "bias_mm": round(compute_bias(sub, forecast_col, obs_col), 2),
        "mae_mm": round(compute_mae(sub, forecast_col, obs_col), 2),
        "rmse_mm": round(compute_rmse(sub, forecast_col, obs_col), 2),
    }


def paired_mae_difference(
    df: pd.DataFrame,
    corrected_col: str = "corrected_mm",
    raw_col: str = "raw_mm",
    obs_col: str = "observed_mm",
) -> float:
    """Calculates paired MAE difference: MAE(corrected) - MAE(raw). Negative is improvement."""
    mae_corr = np.mean(np.abs(df[corrected_col] - df[obs_col]))
    mae_raw = np.mean(np.abs(df[raw_col] - df[obs_col]))
    return float(mae_corr - mae_raw)


def two_reference_claim_status(
    bias_v2: float,
    ci_v2: Tuple[Optional[float], Optional[float]],
    bias_v3: float,
    ci_v3: Tuple[Optional[float], Optional[float]],
) -> str:
    """
    Evaluates the Pre-Registered Two-Reference Claim Rule:
    A bias or skill statement is marked 'supported' ONLY if:
    1. Both references have the same directional sign (bias_v2 * bias_v3 > 0); AND
    2. Both 95% bootstrap intervals exclude zero (ci_low > 0 or ci_high < 0).

    Otherwise, returns 'reference-dependent' or 'inconclusive'.
    """
    low_v2, high_v2 = ci_v2
    low_v3, high_v3 = ci_v3

    # If either interval is not estimable (< 5 clusters)
    if low_v2 is None or high_v2 is None or low_v3 is None or high_v3 is None:
        return "reference-dependent"

    # Check same directional sign
    if (bias_v2 > 0 and bias_v3 > 0) or (bias_v2 < 0 and bias_v3 < 0):
        # Check if v2 CI excludes zero
        v2_excludes_zero = (low_v2 > 0 and high_v2 > 0) or (low_v2 < 0 and high_v2 < 0)
        # Check if v3 CI excludes zero
        v3_excludes_zero = (low_v3 > 0 and high_v3 > 0) or (low_v3 < 0 and high_v3 < 0)

        if v2_excludes_zero and v3_excludes_zero:
            return "supported"

    return "reference-dependent"
