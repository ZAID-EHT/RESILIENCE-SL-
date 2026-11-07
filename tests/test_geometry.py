"""
Unit tests for HydroBASINS reverse topological traversal, cycle detection, and area closure.
"""

import pytest
import pandas as pd
import numpy as np

from rsl.clean.geometry import (
    reverse_traverse_hydrobasins,
    validate_area_closure,
    validate_polygon_repair,
    validate_raster_vector_agreement,
)


def test_reverse_traverse_hydrobasins_simple_tree():
    """Tests upstream traversal on a standard tree-like drainage network."""
    # Graph: Outlet 1 <- Sub 2 <- Sub 4
    #               1 <- Sub 3
    data = [
        {"HYBAS_ID": 1, "NEXT_DOWN": 0, "ENDO": 0, "SUB_AREA": 500.0},
        {"HYBAS_ID": 2, "NEXT_DOWN": 1, "ENDO": 0, "SUB_AREA": 300.0},
        {"HYBAS_ID": 3, "NEXT_DOWN": 1, "ENDO": 0, "SUB_AREA": 200.0},
        {"HYBAS_ID": 4, "NEXT_DOWN": 2, "ENDO": 0, "SUB_AREA": 150.0},
        {"HYBAS_ID": 5, "NEXT_DOWN": 99, "ENDO": 0, "SUB_AREA": 400.0},  # Unrelated basin
    ]
    df = pd.DataFrame(data)

    upstream_ids, total_sub_area, virtual_count = reverse_traverse_hydrobasins(df, outlet_hybas_id=1)

    assert sorted(upstream_ids) == [1, 2, 3, 4]
    assert total_sub_area == 1150.0
    assert virtual_count == 0


def test_reverse_traverse_cycle_detection():
    """Verifies that cycles in the network do not cause infinite loops."""
    # Cyclic graph: 1 <- 2 <- 3 <- 2
    data = [
        {"HYBAS_ID": 1, "NEXT_DOWN": 0, "ENDO": 0, "SUB_AREA": 500.0},
        {"HYBAS_ID": 2, "NEXT_DOWN": 1, "ENDO": 0, "SUB_AREA": 300.0},
        {"HYBAS_ID": 3, "NEXT_DOWN": 2, "ENDO": 0, "SUB_AREA": 200.0},
    ]
    df = pd.DataFrame(data)
    # Add cycle: node 2 points to node 3 as well
    df.loc[len(df)] = {"HYBAS_ID": 2, "NEXT_DOWN": 3, "ENDO": 0, "SUB_AREA": 0.0}

    upstream_ids, total_sub_area, _ = reverse_traverse_hydrobasins(df, outlet_hybas_id=1)
    assert 1 in upstream_ids
    assert 2 in upstream_ids
    assert 3 in upstream_ids


def test_reverse_traverse_excludes_virtual_endorheic():
    """Asserts that virtual endorheic links (ENDO == 2) are excluded from upstream traversal."""
    data = [
        {"HYBAS_ID": 1, "NEXT_DOWN": 0, "ENDO": 0, "SUB_AREA": 500.0},
        {"HYBAS_ID": 2, "NEXT_DOWN": 1, "ENDO": 0, "SUB_AREA": 300.0},
        {"HYBAS_ID": 3, "NEXT_DOWN": 1, "ENDO": 2, "SUB_AREA": 250.0},  # Virtual connection
    ]
    df = pd.DataFrame(data)

    upstream_ids, total_sub_area, virtual_count = reverse_traverse_hydrobasins(df, outlet_hybas_id=1)
    assert sorted(upstream_ids) == [1, 2]
    assert total_sub_area == 800.0
    assert virtual_count == 1


def test_validate_area_closure_kelani_benchmark():
    """Validates that Kelani Level 10 subbasins sum to 2325.2 km² vs UP_AREA 2325.3 km² (-0.004%)."""
    is_valid, diff_pct = validate_area_closure(2325.2, 2325.3, tolerance_pct=1.0)
    assert is_valid is True
    assert round(diff_pct, 3) == -0.004


def test_validate_polygon_repair_tolerance():
    """Validates that geometry repair area shift is well within 0.01% tolerance."""
    is_valid, change_pct = validate_polygon_repair(432.24, 432.24, max_area_change_pct=0.01)
    assert is_valid is True
    assert change_pct == 0.0


def test_validate_raster_vector_agreement():
    """Validates agreement between rasterized (432.14 km²) and vector (432.24 km²) within 2%."""
    is_valid, diff_pct = validate_raster_vector_agreement(432.14, 432.24, tolerance_pct=2.0)
    assert is_valid is True
    assert diff_pct < 0.05  # actual is 0.023%
