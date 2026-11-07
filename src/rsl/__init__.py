"""
RESILIENCE SL: Evidence-Based Rainfall-Forecast Reliability and Historical Flood Exposure
for the Kelani Catchment, Sri Lanka.

ModelX 2.0 Open Research Workbench.
"""

__version__ = "2.0.0"
__author__ = "RESILIENCE SL Research Team"

from rsl.clean.time_windows import stratum_for_run, integrate_preceding_hour_utc, get_season
from rsl.clean.masks import mask_chirps_nodata
from rsl.clean.units import convert_imerg_rate_to_half_hour
from rsl.clean.geometry import reverse_traverse_hydrobasins
from rsl.analysis.events import cluster_rain_events
from rsl.analysis.metrics import calculate_metrics, two_reference_claim_status

__all__ = [
    "stratum_for_run",
    "integrate_preceding_hour_utc",
    "get_season",
    "mask_chirps_nodata",
    "convert_imerg_rate_to_half_hour",
    "reverse_traverse_hydrobasins",
    "cluster_rain_events",
    "calculate_metrics",
    "two_reference_claim_status",
]
