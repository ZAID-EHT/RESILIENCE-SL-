"""
May 2010 World Bank / ESA flood map specifications and geometry cleaning criteria.
"""

from typing import Dict, Any


class FloodMapAcquirer:
    """Metadata, filtering criteria, and area audit figures for the May 2010 flood footprint."""

    TARGET_SHAPEFILE = "Max_flood_EventMay2010.shp"
    TARGET_CLASS = "(flood) water"

    AUDIT_STATS = {
        "total_polygons": 22813,
        "floodwater_polygons": 12734,
        "repaired_invalid_polygons": 298,
        "repair_area_shift_percent": 0.00,
        "full_frame_vector_km2": 432.24,
        "full_frame_raster_km2": 432.14,
        "raster_vector_diff_percent": 0.023,  # < 2% tolerance
        "kelani_clipped_floodwater_km2": 100.40,
        "kelani_clipped_share_percent": 23.23,
        "adjacent_coastal_floodwater_km2": 47.60,
        "adjacent_coastal_share_percent": 11.01,
        "outside_other_basins_km2": 284.24,
        "outside_other_basins_share_percent": 65.76,
    }

    @classmethod
    def get_audit_stats(cls) -> Dict[str, Any]:
        return cls.AUDIT_STATS.copy()
