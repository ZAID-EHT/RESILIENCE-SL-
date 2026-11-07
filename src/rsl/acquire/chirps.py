"""
CHIRPS v2.0 and CHIRPS v3.0 sat acquisition parameters and validation logic.
"""

from typing import Dict, Any, List
import numpy as np
import pandas as pd


class CHIRPSAcquirer:
    """Manages acquisition parameters and access rules for CHIRPS precipitation datasets."""

    V2_URL_TEMPLATE = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/tifs/p05/{year}/chirps-v2.0.{year}.{month:02d}.{day:02d}.tif.gz"
    V3_SAT_EARTH_ENGINE_ASSET = "projects/climate-hazards-center/assets/chirps/v3/daily_sat"
    V3_RNL_EARTH_ENGINE_ASSET = "projects/climate-hazards-center/assets/chirps/v3/daily_rnl"

    @classmethod
    def get_reference_metadata(cls) -> Dict[str, Any]:
        return {
            "v2.0": {
                "name": "CHIRPS v2.0",
                "resolution": "0.05 deg",
                "disaggregation": "None (Infrared-station pentad)",
                "status": "co-primary",
                "nodata_val": -9999.0,
            },
            "v3.0 sat": {
                "name": "CHIRPS v3.0 sat",
                "resolution": "0.05 deg",
                "disaggregation": "IMERG Late V07",
                "status": "co-primary",
                "nodata_val": -9999.0,
            },
            "v3.0 rnl": {
                "name": "CHIRPS v3.0 rnl",
                "resolution": "0.05 deg",
                "disaggregation": "ERA5 Reanalysis",
                "status": "disqualified_by_amendment_a1",
                "disqualification_reason": "ERA5 is an ECMWF product; using it creates model self-evaluation bias.",
            },
        }

    @staticmethod
    def is_eligible_reference(ref_name: str) -> bool:
        """Enforces Amendment A1: v3.0 rnl is strictly disqualified."""
        if ref_name in ["v2.0", "v3.0 sat"]:
            return True
        if ref_name == "v3.0 rnl":
            return False
        return False
