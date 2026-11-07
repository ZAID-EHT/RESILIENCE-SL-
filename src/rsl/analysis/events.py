"""
Meteorological event grouping, dry gap clustering, and heavy-rain gate evaluation.
"""

from typing import Dict, List, Tuple, Union
import numpy as np
import pandas as pd


def cluster_rain_events(
    df: pd.DataFrame,
    date_col: str = "valid_date_utc",
    rain_col: str = "rain_mm",
    wet_threshold_mm: float = 1.0,
    dry_gap_days: int = 3,
) -> pd.DataFrame:
    """
    Groups serially-correlated rainfall days into independent meteorological event clusters.

    Algorithm:
    1. Identify wet days: rain_mm >= wet_threshold_mm.
    2. Sort dates chronologically.
    3. If two consecutive wet days have a dry gap <= dry_gap_days (i.e. date_diff <= dry_gap_days + 1),
       they belong to the same event group.
    4. When date_diff > dry_gap_days + 1, a new event group is initiated.
    5. Dry days between wet days within the gap window receive the cluster ID of the event.

    Returns:
        DataFrame with added integer column 'cluster_id'.
    """
    df_sorted = df.copy()
    df_sorted[date_col] = pd.to_datetime(df_sorted[date_col])
    df_sorted = df_sorted.sort_values(date_col).reset_index(drop=True)

    df_sorted["is_wet"] = df_sorted[rain_col] >= wet_threshold_mm

    cluster_ids = np.zeros(len(df_sorted), dtype=int)
    current_cluster = 0
    last_wet_date = None

    for i, row in df_sorted.iterrows():
        curr_date = row[date_col]
        is_wet = row["is_wet"]

        if is_wet:
            if last_wet_date is None:
                current_cluster = 1
            else:
                gap = (curr_date - last_wet_date).days - 1
                if gap > dry_gap_days:
                    current_cluster += 1
            last_wet_date = curr_date
            cluster_ids[i] = current_cluster
        else:
            # Check if this dry day is within an active event gap
            # Will be resolved in a second forward/backward fill pass
            cluster_ids[i] = 0

    # Fill dry days that fall strictly between wet days of the same cluster
    df_sorted["cluster_id"] = cluster_ids
    
    # Consolidate intermediate dry days into the adjacent cluster
    for i in range(1, len(df_sorted) - 1):
        if df_sorted.loc[i, "cluster_id"] == 0 and last_wet_date is not None:
            # check previous wet and next wet
            prev_cluster = df_sorted.loc[i-1, "cluster_id"]
            if prev_cluster > 0:
                # check if there is a subsequent wet day in the same window
                future_wet = df_sorted.iloc[i+1:][df_sorted.iloc[i+1:]["is_wet"]]
                if not future_wet.empty:
                    next_wet_idx = future_wet.index[0]
                    next_date = df_sorted.loc[next_wet_idx, date_col]
                    curr_date = df_sorted.loc[i, date_col]
                    if (next_date - curr_date).days <= dry_gap_days + 1:
                        df_sorted.loc[i, "cluster_id"] = prev_cluster

    # For standalone dry days outside any cluster, give cluster_id = -1 or separate cluster
    df_sorted["cluster_id"] = df_sorted["cluster_id"].replace(0, -1)
    return df_sorted


def count_independent_heavy_events(
    df_with_clusters: pd.DataFrame,
    rain_col: str = "rain_mm",
    heavy_threshold_mm: float = 50.0,
    cluster_id_col: str = "cluster_id",
) -> int:
    """
    Counts the number of independent event clusters that contain at least one day
    with rainfall >= heavy_threshold_mm.
    """
    heavy_rows = df_with_clusters[df_with_clusters[rain_col] >= heavy_threshold_mm]
    valid_clusters = heavy_rows[heavy_rows[cluster_id_col] > 0][cluster_id_col].unique()
    return len(valid_clusters)


def evaluate_heavy_rain_gate(
    cluster_count: int,
    gate_threshold: int = 20,
) -> Tuple[bool, str]:
    """
    Enforces the pre-registered 20-event gate.
    If cluster_count < 20, triggers explicit refusal banner.
    """
    passed = cluster_count >= gate_threshold
    if passed:
        msg = f"PASSED: {cluster_count} independent event groups (>= {gate_threshold} gate)."
    else:
        msg = (
            f"Insufficient evidence: {cluster_count} independent event groups "
            f"(< {gate_threshold} gate). Descriptive cases only."
        )
    return passed, msg
