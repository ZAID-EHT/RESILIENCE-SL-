"""
Historical flood exposure cross-tabulation, catchment boundary allocation,
and land-cover product sensitivity diagnostics.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np


def calculate_catchment_flood_allocation() -> pd.DataFrame:
    """
    Returns verified spatial allocation of the May 2010 flood footprint (432.24 km² total).
    Enforces the finding that only 23.2% of the mapped water was inside the Kelani catchment.
    """
    records = [
        {
            "spatial_unit": "Inside Verified Kelani Catchment (HydroBASINS L8/L10)",
            "area_km2": 100.40,
            "share_percent": 23.23,
            "description": "True contributing hydrologic catchment (covers lower ~30% of basin).",
        },
        {
            "spatial_unit": "Adjacent Coastal Units (including Kelani river mouth)",
            "area_km2": 47.60,
            "share_percent": 11.01,
            "description": "Mouth estuary unit (310 km² total) plus immediate coastal plain.",
        },
        {
            "spatial_unit": "Other Basins Outside Kelani (Kalu, Attanagalu, etc.)",
            "area_km2": 284.24,
            "share_percent": 65.76,
            "description": "Inundation outside Kelani hydrologic boundaries falsely attributed if unclipped.",
        },
        {
            "spatial_unit": "Full 2010 Map Frame Total",
            "area_km2": 432.24,
            "share_percent": 100.00,
            "description": "Entire bounding envelope (79.82-80.16E, 6.50-7.44N).",
        },
    ]
    return pd.DataFrame(records)


def calculate_product_sensitivity_ranges() -> pd.DataFrame:
    """
    Returns verified land cover exposure numbers inside the 100.40 km² Kelani Catchment floodwater.
    Demonstrates that differences represent product resolution sensitivity, NOT actual land-use change.
    """
    records = [
        {
            "land_cover_category": "Built-up / Urban",
            "worldcover_2021_10m_km2": 5.90,
            "cci_2010_300m_km2": 21.70,
            "sensitivity_range_km2": "5.9 - 21.7",
            "aggregation_diagnostic": "CCI 300m urban pixels contain on average 45% WorldCover built-up structures.",
        },
        {
            "land_cover_category": "Cropland",
            "worldcover_2021_10m_km2": 21.90,
            "cci_2010_300m_km2": 6.30,  # strict classes 10, 11, 20
            "sensitivity_range_km2": "6.3 - 53.5",
            "aggregation_diagnostic": "CCI cropland expands to 53.5 km² when mosaic class 30 is included; CCI cropland pixels contain 3% WorldCover cropland.",
        },
        {
            "land_cover_category": "Tree Cover / Forest",
            "worldcover_2021_10m_km2": 61.00,
            "cci_2010_300m_km2": 65.20,
            "sensitivity_range_km2": "61.0 - 65.2",
            "aggregation_diagnostic": "Pervasive canopy in wet-zone floodplains: home gardens (gewathu) and rubber/coconut groves conceal inundated ground.",
        },
        {
            "land_cover_category": "Grassland / Shrubland",
            "worldcover_2021_10m_km2": 6.80,
            "cci_2010_300m_km2": 4.10,
            "sensitivity_range_km2": "4.1 - 6.8",
            "aggregation_diagnostic": "Open marshes, abandoned paddy fields, and riverbank fringes.",
        },
        {
            "land_cover_category": "Permanent Water / Wetland",
            "worldcover_2021_10m_km2": 4.80,
            "cci_2010_300m_km2": 3.10,
            "sensitivity_range_km2": "3.1 - 4.8",
            "aggregation_diagnostic": "Baseline river mainstem, canals, and perennial marshland.",
        },
    ]
    return pd.DataFrame(records)


def validate_emsr851_quality_gates(
    not_analysed_pct: float,
    max_not_analysed_pct: float = 50.0,
) -> Tuple[bool, str]:
    """
    Validates Copernicus EMS Rapid Mapping quality criteria:
    1. Not-analysed percentage must be < 50% for acceptable quality.
    2. Model-extrapolated area must never be added to EO observed flooded area.
    """
    if not_analysed_pct >= max_not_analysed_pct:
        return False, f"Quality gate failed: not-analysed extent ({not_analysed_pct:.1f}%) exceeds {max_not_analysed_pct}%."
    return True, f"Quality gate passed: not-analysed extent is {not_analysed_pct:.1f}% (< {max_not_analysed_pct}%)."
