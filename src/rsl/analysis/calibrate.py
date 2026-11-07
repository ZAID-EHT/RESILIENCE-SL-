"""
Statistical post-processing calibration: seasonal bias adjustment, non-negative ridge regression,
and rolling-origin out-of-sample evaluation.
"""

from typing import Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge

from rsl.clean.time_windows import get_season


class SeasonalAdditiveBiasCalibrator:
    """
    Computes empirical additive bias (forecast - observed) per season and lead day on the training set,
    and corrects test forecasts by subtracting the estimated seasonal bias.
    Enforces non-negative physical precipitation.
    """

    def __init__(self):
        self.biases: Dict[Tuple[str, int], float] = {}

    def fit(
        self,
        df_train: pd.DataFrame,
        season_col: str = "season",
        lead_col: str = "lead_day",
        forecast_col: str = "forecast_mm",
        observed_col: str = "observed_mm",
    ) -> "SeasonalAdditiveBiasCalibrator":
        df = df_train.copy()
        df["error"] = df[forecast_col] - df[observed_col]
        grp = df.groupby([season_col, lead_col])["error"].mean().to_dict()
        self.biases = grp
        return self

    def predict(
        self,
        df_test: pd.DataFrame,
        season_col: str = "season",
        lead_col: str = "lead_day",
        forecast_col: str = "forecast_mm",
    ) -> np.ndarray:
        preds = []
        for _, row in df_test.iterrows():
            s = row[season_col]
            l = int(row[lead_col])
            raw = float(row[forecast_col])
            bias = self.biases.get((s, l), 0.0)
            corrected = max(0.0, raw - bias)
            preds.append(corrected)
        return np.array(preds, dtype=float)


class NonNegativeRidgeCalibrator:
    """
    Fits Ridge regression on forecast features and clips negative predictions to zero.
    """

    def __init__(self, alpha: float = 1.0):
        self.alpha = alpha
        self.model = Ridge(alpha=alpha, positive=True)

    def fit(self, X_train: np.ndarray, y_train: np.ndarray) -> "NonNegativeRidgeCalibrator":
        X = np.atleast_2d(X_train)
        self.model.fit(X, y_train)
        return self

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        X = np.atleast_2d(X_test)
        preds = self.model.predict(X)
        return np.clip(preds, 0.0, None)


def rolling_origin_cross_validation(
    df: pd.DataFrame,
    date_col: str = "valid_date_utc",
    initial_train_days: int = 180,
    test_block_days: int = 30,
    purge_days: int = 3,
) -> List[Tuple[pd.DataFrame, pd.DataFrame]]:
    """
    Generates rolling-origin evaluation folds.
    Purges `purge_days` around boundary to eliminate autocorrelation leakage.
    """
    df_sorted = df.sort_values(date_col).reset_index(drop=True)
    all_dates = pd.to_datetime(df_sorted[date_col].unique())
    all_dates = np.sort(all_dates)

    total_days = len(all_dates)
    folds = []

    curr_idx = initial_train_days
    while curr_idx + test_block_days <= total_days:
        train_end_date = all_dates[curr_idx - 1]
        test_start_date = all_dates[curr_idx + purge_days] if curr_idx + purge_days < total_days else None
        
        if test_start_date is None:
            break

        test_end_idx = min(curr_idx + purge_days + test_block_days - 1, total_days - 1)
        test_end_date = all_dates[test_end_idx]

        train_mask = pd.to_datetime(df_sorted[date_col]) <= train_end_date
        test_mask = (pd.to_datetime(df_sorted[date_col]) >= test_start_date) & (
            pd.to_datetime(df_sorted[date_col]) <= test_end_date
        )

        df_train = df_sorted[train_mask]
        df_test = df_sorted[test_mask]

        if not df_train.empty and not df_test.empty:
            folds.append((df_train, df_test))

        curr_idx += test_block_days

    return folds
