"""
Unit tests for historical flood exposure calculations, land cover product sensitivity,
and Copernicus EMSR851 quality gates.
"""

import pytest
import pandas as pd
import numpy as np

from rsl.analysis.exposure import (
    calculate_catchment_flood_allocation,
    calculate_product_sensitivity_ranges,
    validate_emsr851_quality_gates,
)


def test_catchment_flood_allocation_totals():
    """Validates exact flood area allocation across Kelani, coastal, and outside basins."""
    df = calculate_catchment_flood_allocation()
    assert len(df) == 4

    inside_row = df[df["spatial_unit"].str.contains("Inside Verified Kelani")].iloc[0]
    coastal_row = df[df["spatial_unit"].str.contains("Adjacent Coastal")].iloc[0]
    outside_row = df[df["spatial_unit"].str.contains("Other Basins Outside")].iloc[0]
    total_row = df[df["spatial_unit"].str.contains("Full 2010 Map Frame")].iloc[0]

    assert inside_row["area_km2"] == 100.40
    assert coastal_row["area_km2"] == 47.60
    assert outside_row["area_km2"] == 284.24
    assert total_row["area_km2"] == 432.24

    # Check sum consistency
    np.testing.assert_almost_equal(
        inside_row["area_km2"] + coastal_row["area_km2"] + outside_row["area_km2"],
        total_row["area_km2"],
        decimal=2,
    )


def test_product_sensitivity_ranges():
    """Validates land-cover exposure ranges and urban aggregation proof."""
    df = calculate_product_sensitivity_ranges()

    urban_row = df[df["land_cover_category"].str.contains("Built-up")].iloc[0]
    cropland_row = df[df["land_cover_category"].str.contains("Cropland")].iloc[0]
    tree_row = df[df["land_cover_category"].str.contains("Tree Cover")].iloc[0]

    assert urban_row["worldcover_2021_10m_km2"] == 5.90
    assert urban_row["cci_2010_300m_km2"] == 21.70
    assert "45%" in urban_row["aggregation_diagnostic"]

    assert cropland_row["worldcover_2021_10m_km2"] == 21.90
    assert cropland_row["cci_2010_300m_km2"] == 6.30

    assert tree_row["worldcover_2021_10m_km2"] == 61.00
    assert "gewathu" in tree_row["aggregation_diagnostic"]


def test_validate_emsr851_quality_gates_planetscope():
    """Validates that PlanetScope Nov 30 (2.7% not-analysed) passes the < 50% quality gate."""
    passed, msg = validate_emsr851_quality_gates(not_analysed_pct=2.7, max_not_analysed_pct=50.0)
    assert passed is True
    assert "passed" in msg.lower()


def test_validate_emsr851_quality_gates_failure():
    """Asserts that scenes with >= 50% not-analysed area fail quality gate."""
    passed, msg = validate_emsr851_quality_gates(not_analysed_pct=58.2, max_not_analysed_pct=50.0)
    assert passed is False
    assert "failed" in msg.lower()
