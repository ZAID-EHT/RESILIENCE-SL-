"""
Baseline models: raw numerical weather prediction and training-only day-of-year climatology.
"""

from typing import Dict, Optional, Union
import numpy as np
import pandas as pd


class RawForecastBaseline:
    """Pass-through raw ECMWF IFS forecast without empirical modification."""

    def predict(self, df: pd.DataFrame, forecast_col: str = "forecast_mm") -> np.ndarray:
        return df[forecast_col].to_numpy(dtype=float)


class ClimatologyBaseline:
    """
    Training-only day-of-year (DOY) climatology.
    Computes mean observed rainfall for each calendar day of year (1-366) in the training fold.
    """

    def __init__(self):
        self.doy_means: Dict[int, float] = {}
        self.global_mean: float = 0.0

    def fit(
        self,
        df_train: pd.DataFrame,
        date_col: str = "valid_date_utc",
        target_col: str = "observed_mm",
    ) -> "ClimatologyBaseline":
        df = df_train.copy()
        df["doy"] = pd.to_datetime(df[date_col]).dt.dayofyear
        means = df.groupby("doy")[target_col].mean().to_dict()
        self.doy_means = means
        self.global_mean = float(df[target_col].mean()) if not df.empty else 0.0
        return self

    def predict(
        self,
        df_test: pd.DataFrame,
        date_col: str = "valid_date_utc",
    ) -> np.ndarray:
        doys = pd.to_datetime(df_test[date_col]).dt.dayofyear
        preds = [self.doy_means.get(d, self.global_mean) for d in doys]
        return np.array(preds, dtype=float)
