"""
Unit tests for meteorological event clustering, dry gap sensitivity, and the 20-event refusal gate.
"""

import pytest
import pandas as pd
import numpy as np

from rsl.analysis.events import (
    cluster_rain_events,
    count_independent_heavy_events,
    evaluate_heavy_rain_gate,
)


def test_cluster_rain_events_standard_3day_gap():
    """Tests grouping of wet days separated by <= 3 dry days into identical event clusters."""
    # Day 1: wet (10mm)
    # Day 2: dry (0mm)
    # Day 3: dry (0mm)
    # Day 4: wet (20mm) -> Same cluster (2 dry days <= 3)
    # Day 5-9: dry (5 dry days)
    # Day 10: wet (15mm) -> New cluster (> 3 dry days)
    dates = [f"2025-05-{d:02d}" for d in range(1, 11)]
    rain = [10.0, 0.0, 0.0, 20.0, 0.0, 0.0, 0.0, 0.0, 0.0, 15.0]
    df = pd.DataFrame({"valid_date_utc": dates, "rain_mm": rain})

    clustered = cluster_rain_events(df, dry_gap_days=3)

    c_day1 = clustered.loc[clustered["valid_date_utc"] == "2025-05-01", "cluster_id"].values[0]
    c_day4 = clustered.loc[clustered["valid_date_utc"] == "2025-05-04", "cluster_id"].values[0]
    c_day10 = clustered.loc[clustered["valid_date_utc"] == "2025-05-10", "cluster_id"].values[0]

    assert c_day1 == c_day4  # grouped together
    assert c_day10 != c_day1  # new cluster
    assert c_day1 > 0
    assert c_day10 > 0


def test_cluster_rain_events_sensitivity_2_vs_5_days():
    """Tests that a 3-day dry gap splits under 2-day rule but merges under 5-day rule."""
    dates = ["2025-05-01", "2025-05-02", "2025-05-03", "2025-05-04", "2025-05-05"]
    # Day 1 wet, Days 2, 3, 4 dry (3 dry days), Day 5 wet
    rain = [10.0, 0.0, 0.0, 0.0, 15.0]
    df = pd.DataFrame({"valid_date_utc": dates, "rain_mm": rain})

    # Under dry_gap_days = 2: 3 dry days > 2, so splits into 2 clusters
    c_split = cluster_rain_events(df, dry_gap_days=2)
    c1_split = c_split.loc[0, "cluster_id"]
    c5_split = c_split.loc[4, "cluster_id"]
    assert c1_split != c5_split

    # Under dry_gap_days = 5: 3 dry days <= 5, so merges into 1 cluster
    c_merge = cluster_rain_events(df, dry_gap_days=5)
    c1_merge = c_merge.loc[0, "cluster_id"]
    c5_merge = c_merge.loc[4, "cluster_id"]
    assert c1_merge == c5_merge


def test_count_independent_heavy_events():
    """Tests counting of independent event groups containing a day >= 50 mm."""
    # Two clusters, cluster 1 has a 55mm day, cluster 2 has only 30mm
    dates = ["2025-05-01", "2025-05-02", "2025-05-10", "2025-05-11"]
    rain = [55.0, 10.0, 30.0, 25.0]
    df = pd.DataFrame({"valid_date_utc": dates, "rain_mm": rain})
    clustered = cluster_rain_events(df, dry_gap_days=3)

    heavy_count = count_independent_heavy_events(clustered, heavy_threshold_mm=50.0)
    assert heavy_count == 1


def test_evaluate_heavy_rain_gate_refusal_state():
    """Asserts that < 20 independent heavy clusters triggers the pre-registered refusal banner."""
    # 8 clusters (the actual S1 finding)
    passed, msg = evaluate_heavy_rain_gate(8, gate_threshold=20)
    assert passed is False
    assert "Insufficient evidence" in msg
    assert "8 independent event groups" in msg
    assert "< 20 gate" in msg
    assert "Descriptive cases only" in msg


def test_evaluate_heavy_rain_gate_passed():
    """Asserts that >= 20 independent heavy clusters passes the gate."""
    passed, msg = evaluate_heavy_rain_gate(22, gate_threshold=20)
    assert passed is True
    assert "PASSED" in msg
