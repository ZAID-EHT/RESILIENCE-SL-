"""
Analytical methods: forecast joins, meteorological event grouping, statistical calibration,
cluster bootstrap inference, and historical exposure cross-tabulation.
"""

from rsl.analysis.join import join_forecast_and_references, validate_zero_leakage
from rsl.analysis.events import cluster_rain_events, count_independent_heavy_events
from rsl.analysis.baselines import RawForecastBaseline, ClimatologyBaseline
from rsl.analysis.calibrate import (
    SeasonalAdditiveBiasCalibrator,
    NonNegativeRidgeCalibrator,
    rolling_origin_cross_validation,
)
from rsl.analysis.metrics import (
    calculate_metrics,
    two_reference_claim_status,
    paired_mae_difference,
)
from rsl.analysis.bootstrap import cluster_bootstrap_ci
from rsl.analysis.exposure import (
    calculate_catchment_flood_allocation,
    calculate_product_sensitivity_ranges,
)

__all__ = [
    "join_forecast_and_references",
    "validate_zero_leakage",
    "cluster_rain_events",
    "count_independent_heavy_events",
    "RawForecastBaseline",
    "ClimatologyBaseline",
    "SeasonalAdditiveBiasCalibrator",
    "NonNegativeRidgeCalibrator",
    "rolling_origin_cross_validation",
    "calculate_metrics",
    "two_reference_claim_status",
    "paired_mae_difference",
    "cluster_bootstrap_ci",
    "calculate_catchment_flood_allocation",
    "calculate_product_sensitivity_ranges",
]
