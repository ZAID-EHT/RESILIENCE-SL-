"""
Unit tests for verification metrics, the Two-Reference Claim Rule, and Amendment A5 bootstrap suppression.
"""

import pytest
import numpy as np
import pandas as pd

from rsl.analysis.metrics import (
    compute_bias,
    compute_mae,
    compute_rmse,
    calculate_metrics,
    paired_mae_difference,
    two_reference_claim_status,
)
from rsl.analysis.bootstrap import (
    cluster_bootstrap_ci,
    format_ci_display,
)


def test_basic_metrics_calculation():
    """Validates basic bias, MAE, and RMSE calculations against hand calculations."""
    df = pd.DataFrame({
        "forecast_mm": [10.0, 20.0, 30.0],
        "observed_mm": [8.0, 25.0, 25.0],
    })
    # Errors: +2.0, -5.0, +5.0
    # Mean error (Bias): (+2 - 5 + 5) / 3 = 0.67
    # MAE: (2 + 5 + 5) / 3 = 4.0
    # RMSE: sqrt((4 + 25 + 25) / 3) = sqrt(54/3) = sqrt(18) = 4.24
    m = calculate_metrics(df)
    assert m["bias_mm"] == 0.67
    assert m["mae_mm"] == 4.0
    assert m["rmse_mm"] == 4.24


def test_paired_mae_difference():
    """Validates paired MAE difference (corrected - raw)."""
    df = pd.DataFrame({
        "raw_mm": [15.0, 25.0],
        "corrected_mm": [11.0, 21.0],
        "observed_mm": [10.0, 20.0],
    })
    # Raw errors: |15-10| = 5, |25-20| = 5 -> MAE = 5.0
    # Corrected errors: |11-10| = 1, |21-20| = 1 -> MAE = 1.0
    # Diff = 1.0 - 5.0 = -4.0 (improvement)
    diff = paired_mae_difference(df)
    assert diff == -4.0


def test_two_reference_claim_status_supported():
    """Asserts that identical sign + both CIs excluding zero yields 'supported'."""
    bias_v2 = 8.9
    ci_v2 = (4.99, 11.32)
    bias_v3 = 6.5
    ci_v3 = (2.79, 9.55)

    status = two_reference_claim_status(bias_v2, ci_v2, bias_v3, ci_v3)
    assert status == "supported"


def test_two_reference_claim_status_ci_crosses_zero():
    """Asserts that if either CI spans zero, status becomes 'reference-dependent'."""
    bias_v2 = 5.1
    ci_v2 = (-0.02, 9.53)  # crosses zero
    bias_v3 = 3.5
    ci_v3 = (-6.23, 6.99)  # crosses zero

    status = two_reference_claim_status(bias_v2, ci_v2, bias_v3, ci_v3)
    assert status == "reference-dependent"


def test_two_reference_claim_status_conflicting_signs():
    """Asserts that opposite bias signs yield 'reference-dependent'."""
    bias_v2 = -2.5
    ci_v2 = (-4.0, -1.0)
    bias_v3 = +1.5
    ci_v3 = (0.5, 3.0)

    status = two_reference_claim_status(bias_v2, ci_v2, bias_v3, ci_v3)
    assert status == "reference-dependent"


def test_amendment_a5_small_clusters_suppressed():
    """
    Verifies Amendment A5:
    When clusters < 5, bootstrap interval returns (None, None) and display is 'not estimable (<5 clusters)'.
    """
    # Create dataset with only 3 clusters
    df = pd.DataFrame({
        "cluster_id": [1, 1, 2, 2, 3],
        "err": [1.0, 2.0, -1.0, 0.0, 3.0],
    })

    ci_low, ci_high = cluster_bootstrap_ci(
        df,
        stat_fn=lambda d: float(np.mean(d["err"])),
        cluster_col="cluster_id",
        n_replications=100,
    )

    assert ci_low is None
    assert ci_high is None
    assert format_ci_display(ci_low, ci_high) == "not estimable (<5 clusters)"


def test_cluster_bootstrap_reproducibility():
    """Verifies that fixed seed produces deterministic, reproducible bootstrap intervals."""
    # Create dataset with 10 clusters
    cluster_ids = np.repeat(np.arange(1, 11), 5)
    rng = np.random.default_rng(123)
    errs = rng.normal(loc=5.0, scale=2.0, size=len(cluster_ids))
    df = pd.DataFrame({"cluster_id": cluster_ids, "err": errs})

    ci1 = cluster_bootstrap_ci(df, stat_fn=lambda d: float(np.mean(d["err"])), seed=42)
    ci2 = cluster_bootstrap_ci(df, stat_fn=lambda d: float(np.mean(d["err"])), seed=42)

    assert ci1 == ci2
    assert ci1[0] is not None
