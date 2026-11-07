"""
Open-Meteo Single Runs API parameter builder and request manager for ECMWF IFS HRES.
"""

from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional
import pandas as pd


PILOT_CELLS = {
    "C1": {"lat": 6.924429, "lon": 79.90725, "name": "Coastal / Colombo mouth"},
    "C2": {"lat": 6.924429, "lon": 80.05902, "name": "Mid-basin / Hanwella"},
    "C3": {"lat": 6.9947276, "lon": 80.35442, "name": "Upland / Kitulgala"},
}

KNOWN_MISSING_DATES = [
    "2025-08-05",
    "2025-08-06",
    "2025-08-08",
    "2025-08-09",
]


class OpenMeteoAcquirer:
    """Builds and manages request parameters for ECMWF IFS single runs."""

    def __init__(self, base_url: str = "https://archive-api.open-meteo.com/v1/archive"):
        self.base_url = base_url

    @staticmethod
    def build_request_params(
        cell_id: str,
        run_date: str,
        forecast_days: int = 8,
    ) -> Dict[str, Any]:
        """Construct standard parameters for ECMWF IFS HRES single run."""
        if cell_id not in PILOT_CELLS:
            raise ValueError(f"Unknown pilot cell ID: {cell_id}. Must be C1, C2, or C3.")

        coords = PILOT_CELLS[cell_id]
        return {
            "latitude": coords["lat"],
            "longitude": coords["lon"],
            "hourly": "precipitation",
            "models": "ecmwf_ifs025",  # or ecmwf_ifs
            "start_date": run_date,
            "end_date": (pd.to_datetime(run_date) + timedelta(days=forecast_days)).strftime("%Y-%m-%d"),
            "timezone": "UTC",
        }

    @staticmethod
    def is_known_missing(run_date_str: str) -> bool:
        """Checks if a run date is one of the 4 known unavailable ECMWF archive dates."""
        return run_date_str in KNOWN_MISSING_DATES

    @staticmethod
    def filter_available_runs(dates: List[str]) -> List[str]:
        """Drops missing dates. Never zero-fills missing runs."""
        return [d for d in dates if not OpenMeteoAcquirer.is_known_missing(d)]
