"""
NASA GPM IMERG Late V07 half-hourly precipitation parameter handling and unit specifications.
"""

from typing import Dict, Any


class IMERGAcquirer:
    """NASA GPM IMERG half-hourly dataset specifications and query parameters."""

    PRODUCT_NAME = "GPM_3IMERGHH_07"
    VARIABLE_NAME = "precipitationCal"
    UNIT = "mm/hr"
    TIME_INTERVAL_MINUTES = 30
    SCALE_FACTOR = 0.5  # multiply mm/hr by 0.5 to obtain mm per 30-min window

    @classmethod
    def get_spec(cls) -> Dict[str, Any]:
        return {
            "product": cls.PRODUCT_NAME,
            "variable": cls.VARIABLE_NAME,
            "native_units": cls.UNIT,
            "accumulation_factor": cls.SCALE_FACTOR,
            "spatial_resolution_deg": 0.1,
            "temporal_resolution_min": cls.TIME_INTERVAL_MINUTES,
            "doi": "10.5067/GPM/IMERG/3B-HH/07",
        }
