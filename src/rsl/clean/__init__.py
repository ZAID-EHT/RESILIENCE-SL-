"""
Data cleaning, validation, time-window integration, and geospatial rectification.
"""

from rsl.clean.time_windows import (
    stratum_for_run,
    integrate_preceding_hour_utc,
    get_lead_slice,
    get_season,
)
from rsl.clean.units import (
    convert_imerg_rate_to_half_hour,
    validate_non_negative_precipitation,
)
from rsl.clean.masks import (
    mask_chirps_nodata,
    validate_clean_series,
)
from rsl.clean.geometry import (
    reverse_traverse_hydrobasins,
    validate_polygon_repair,
    validate_area_closure,
)

__all__ = [
    "stratum_for_run",
    "integrate_preceding_hour_utc",
    "get_lead_slice",
    "get_season",
    "convert_imerg_rate_to_half_hour",
    "validate_non_negative_precipitation",
    "mask_chirps_nodata",
    "validate_clean_series",
    "reverse_traverse_hydrobasins",
    "validate_polygon_repair",
    "validate_area_closure",
]
