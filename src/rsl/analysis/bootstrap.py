"""
Cluster-bootstrap resampling and Amendment A5 small-cluster suppression guard.
"""

from typing import Callable, Optional, Tuple, Union
import numpy as np
import pandas as pd


AMENDMENT_A5_MIN_CLUSTERS = 5


def cluster_bootstrap_ci(
    df: pd.DataFrame,
    stat_fn: Callable[[pd.DataFrame], float],
    cluster_col: str = "cluster_id",
    n_replications: int = 2000,
    alpha: float = 0.05,
    seed: int = 42,
) -> Tuple[Optional[float], Optional[float]]:
    """
    Computes (1 - alpha) * 100% confidence interval using cluster-bootstrap resampling.

    Amendment A5 Enforced:
    If the number of unique clusters is fewer than 5, the procedure suppresses estimation
    and returns (None, None) to prevent spuriously narrow or degenerate intervals.
    """
    clusters = df[df[cluster_col] > 0][cluster_col].unique()
    n_clusters = len(clusters)

    # Amendment A5 Guard
    if n_clusters < AMENDMENT_A5_MIN_CLUSTERS:
        return None, None

    rng = np.random.default_rng(seed)
    boot_stats = []

    # Map clusters to row indexes for fast resampling
    cluster_to_indices = {c: df[df[cluster_col] == c].index.to_numpy() for c in clusters}

    for _ in range(n_replications):
        sampled_clusters = rng.choice(clusters, size=n_clusters, replace=True)
        sampled_indices = np.concatenate([cluster_to_indices[c] for c in sampled_clusters])
        df_resampled = df.loc[sampled_indices]
        try:
            val = stat_fn(df_resampled)
            if not np.isnan(val):
                boot_stats.append(val)
        except Exception:
            continue

    if len(boot_stats) < 100:
        return None, None

    low_pct = (alpha / 2.0) * 100.0
    high_pct = (1.0 - alpha / 2.0) * 100.0

    ci_low = float(np.percentile(boot_stats, low_pct))
    ci_high = float(np.percentile(boot_stats, high_pct))

    return round(ci_low, 2), round(ci_high, 2)


def format_ci_display(ci_low: Optional[float], ci_high: Optional[float]) -> str:
    """Format confidence interval for display, respecting Amendment A5."""
    if ci_low is None or ci_high is None or np.isnan(ci_low) or np.isnan(ci_high):
        return "not estimable (<5 clusters)"
    return f"{ci_low:+.2f} to {ci_high:+.2f}"
