"""
Geospatial graph traversal, HydroBASINS watershed derivation, and topological validation.
"""

from typing import Dict, List, Set, Tuple, Any, Optional
import pandas as pd
import numpy as np


def reverse_traverse_hydrobasins(
    subbasins_df: pd.DataFrame,
    outlet_hybas_id: int,
    hybas_id_col: str = "HYBAS_ID",
    next_down_col: str = "NEXT_DOWN",
    endo_col: str = "ENDO",
    sub_area_col: str = "SUB_AREA",
) -> Tuple[List[int], float, int]:
    """
    Performs upstream directed graph traversal across HydroBASINS topological network.
    Starting at the downstream outlet polygon, reverses the NEXT_DOWN pointer to collect
    all contributing upstream sub-basin polygons.

    Enforces:
    - Cycle detection: terminates branches with cycles to prevent infinite loops.
    - Virtual connection rejection: ignores links where ENDO == 2 (virtual endorheic sinks).

    Returns:
        (upstream_hybas_ids, sum_sub_area_km2, virtual_connection_count)
    """
    # Build reverse lookup: target_downstream -> list of upstream_polygons
    upstream_adj: Dict[int, List[int]] = {}
    polygon_rows: Dict[int, Dict[str, Any]] = {}

    for _, row in subbasins_df.iterrows():
        p_id = int(row[hybas_id_col])
        down_id = int(row[next_down_col])
        polygon_rows[p_id] = row.to_dict()

        if down_id not in upstream_adj:
            upstream_adj[down_id] = []
        upstream_adj[down_id].append(p_id)

    visited: Set[int] = set()
    queue: List[int] = [outlet_hybas_id]
    virtual_connections_count = 0

    while queue:
        curr = queue.pop(0)
        if curr in visited:
            continue
        visited.add(curr)

        # Explore immediate upstream neighbors
        for upstream_id in upstream_adj.get(curr, []):
            up_row = polygon_rows.get(upstream_id)
            if up_row is not None:
                # Check for virtual endorheic connection (ENDO == 2)
                if up_row.get(endo_col, 0) == 2:
                    virtual_connections_count += 1
                    continue  # exclude virtual connection
            if upstream_id not in visited:
                queue.append(upstream_id)

    # Compute sum of SUB_AREA
    total_sub_area = 0.0
    for p_id in visited:
        row = polygon_rows.get(p_id)
        if row and sub_area_col in row:
            total_sub_area += float(row[sub_area_col])

    return sorted(list(visited)), float(total_sub_area), virtual_connections_count


def validate_area_closure(
    sum_sub_area_km2: float,
    up_area_km2: float,
    tolerance_pct: float = 1.0,
) -> Tuple[bool, float]:
    """
    Validates that the sum of SUB_AREA across traversed polygons matches the official UP_AREA
    within tolerance percentage (default: 1.0%).
    Returns (is_valid, percentage_difference).
    """
    diff_pct = ((sum_sub_area_km2 - up_area_km2) / up_area_km2) * 100.0
    is_valid = abs(diff_pct) <= tolerance_pct
    return is_valid, diff_pct


def validate_polygon_repair(
    original_area: float,
    repaired_area: float,
    max_area_change_pct: float = 0.01,
) -> Tuple[bool, float]:
    """
    Validates that geometry repair (e.g. ST_MakeValid) did not distort physical area.
    Tolerance: < 0.01% area shift.
    """
    if original_area <= 0:
        return True, 0.0
    change_pct = abs((repaired_area - original_area) / original_area) * 100.0
    is_valid = change_pct <= max_area_change_pct
    return is_valid, change_pct


def validate_raster_vector_agreement(
    raster_area_km2: float,
    vector_area_km2: float,
    tolerance_pct: float = 2.0,
) -> Tuple[bool, float]:
    """
    Validates that rasterized pixel area and polygon vector area agree within 2.0% tolerance.
    """
    diff_pct = abs((raster_area_km2 - vector_area_km2) / vector_area_km2) * 100.0
    is_valid = diff_pct <= tolerance_pct
    return is_valid, diff_pct
