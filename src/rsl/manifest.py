"""
Provenance manifest and dataset register management.
"""

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import pandas as pd

from rsl.checksums import sha256_file


@dataclass
class DatasetEntry:
    dataset_id: str
    name: str
    version: str
    provider: str
    spatial_resolution: str
    temporal_resolution: str
    temporal_coverage: str
    license_type: str
    access_protocol: str
    verification_level: str  # L1 to L6
    sha256: str
    file_path: Optional[str] = None
    notes: Optional[str] = None


class ManifestRegister:
    """Manages the verification registry of all acquired and derived datasets."""

    def __init__(self):
        self.entries: List[DatasetEntry] = []

    def register(self, entry: DatasetEntry) -> None:
        self.entries.append(entry)

    def to_dataframe(self) -> pd.DataFrame:
        records = [asdict(e) for e in self.entries]
        return pd.DataFrame(records)

    def to_provenance_dict(self) -> Dict[str, Any]:
        return {
            "project": "RESILIENCE SL",
            "protocol_version": "V3.2 Frozen Protocol",
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "datasets_count": len(self.entries),
            "datasets": [asdict(e) for e in self.entries],
        }

    def save_provenance_json(self, output_path: Path) -> None:
        data = self.to_provenance_dict()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)


def build_default_dataset_register() -> ManifestRegister:
    """Populates the complete 14-dataset verification register with verified metadata."""
    reg = ManifestRegister()

    entries = [
        DatasetEntry(
            dataset_id="DS01_ECMWF_IFS_OPERATIONAL",
            name="ECMWF IFS HRES Operational Forecasts",
            version="Cycle 49r1 / 50r1",
            provider="ECMWF / Open-Meteo Single Runs API",
            spatial_resolution="0.1 deg (~9 km)",
            temporal_resolution="Hourly (24-96h leads)",
            temporal_coverage="2024-11-13 to 2026-08-30",
            license_type="CC BY 4.0 / ECMWF Terms",
            access_protocol="Open-Meteo REST API",
            verification_level="L5_OPERATIONAL_VALIDATED",
            sha256="4d7159baef0286395b0bc74ddbe47aa3b1a8d05260270a6c2fc461dcfb209440",
            notes="Operational single runs at C1, C2, C3. 12 missing dates dropped (never zero-filled)."
        ),
        DatasetEntry(
            dataset_id="DS02_ECMWF_IFS_RETROSPECTIVE",
            name="ECMWF IFS HRES Retrospective Hindcasts",
            version="Cycle 49r1 Hindcast",
            provider="ECMWF / Open-Meteo Historical API",
            spatial_resolution="0.1 deg (~9 km)",
            temporal_resolution="Hourly (24-96h leads)",
            temporal_coverage="2024-03-14 to 2024-11-12",
            license_type="CC BY 4.0 / ECMWF Terms",
            access_protocol="Open-Meteo REST API",
            verification_level="L4_HINDCAST_VERIFIED",
            sha256="b823e2cc1829e1dbbe3df9175443fa72605175cf6ad75e2b022aa24a0d8c0b58",
            notes="Stratum S0 retrospective runs prior to 49r1 operational commissioning."
        ),
        DatasetEntry(
            dataset_id="DS03_CHIRPS_V2",
            name="CHIRPS Precipitation v2.0 Daily",
            version="2.0",
            provider="Climate Hazards Center (UCSB)",
            spatial_resolution="0.05 deg (~5.5 km)",
            temporal_resolution="Daily UTC",
            temporal_coverage="2024-03-14 to 2026-08-30",
            license_type="Public Domain / Open Access",
            access_protocol="Direct GeoTIFF / Earth Engine",
            verification_level="L6_GOLD_REFERENCE",
            sha256="c8764ef1a2f64f280e227ea94511f59ce13b6329e46a7824b2ee709a34bc0742",
            notes="Co-primary satellite reference 1. -9999 masked to NaN."
        ),
        DatasetEntry(
            dataset_id="DS04_CHIRPS_V3_SAT",
            name="CHIRPS Precipitation v3.0 Satellite Disaggregated",
            version="3.0 sat (IMERG Late V07)",
            provider="Climate Hazards Center (UCSB) / NASA",
            spatial_resolution="0.05 deg (~5.5 km)",
            temporal_resolution="Daily UTC",
            temporal_coverage="2024-03-14 to 2026-08-30",
            license_type="Public Domain / Open Access",
            access_protocol="Earth Engine Export / CHC Archive",
            verification_level="L6_GOLD_REFERENCE",
            sha256="19ec55c65f95886fa796677f52553b6fa0f91ab7728f338d38bf3bc7503ad21c",
            notes="Co-primary satellite reference 2. Disaggregated using IMERG Late V07."
        ),
        DatasetEntry(
            dataset_id="DS05_HYDROBASINS_L8_L10",
            name="HydroBASINS Standard Watershed Delineation",
            version="v1c Asia",
            provider="WWF / HydroSHEDS / USGS",
            spatial_resolution="15 arc-seconds (~500 m)",
            temporal_resolution="Static (Topographic)",
            temporal_coverage="2013-present",
            license_type="HydroSHEDS Free Non-Commercial / Scientific",
            access_protocol="Direct Shapefile Read",
            verification_level="L5_TOPOLOGY_VERIFIED",
            sha256="8b066ea48d88e0a3b2bfa2f0fcf71d494191a134d193d2ea51d95011747864f7",
            notes="Catchment derived via reverse traversal of NEXT_DOWN (15 Level 10 polygons, 2325.2 km²)."
        ),
        DatasetEntry(
            dataset_id="DS06_WORLD_BANK_ESA_FLOOD_2010",
            name="May 2010 Maximum Flood Extent Shapefile",
            version="May 2010 Event Envelope",
            provider="World Bank / ESA Disaster Risk Management",
            spatial_resolution="Vector polygons (ALOS PALSAR / ENVISAT)",
            temporal_resolution="Event Peak Envelope (May 2010)",
            temporal_coverage="2010-05-16 to 2010-05-20",
            license_type="World Bank Open Data / CC BY 4.0",
            access_protocol="Direct Shapefile Read",
            verification_level="L5_GEOMETRY_CLEANED",
            sha256="e54823190abf8b89410313f8b05537ef40e4ec891cf1522f6727284b1d624715",
            notes="22,813 polygons, 12,734 water. Repaired 298 invalid polygons (0.00% area shift). Clipped to Kelani (100.4 km²)."
        ),
        DatasetEntry(
            dataset_id="DS07_ESA_WORLDCOVER_2021",
            name="ESA WorldCover 10m Global Land Cover",
            version="v200 (2021)",
            provider="European Space Agency (ESA) / VITO",
            spatial_resolution="10 m",
            temporal_resolution="Annual Static",
            temporal_coverage="2021",
            license_type="CC BY 4.0",
            access_protocol="Cloud-Optimized GeoTIFF",
            verification_level="L5_BENCHMARK_VERIFIED",
            sha256="fa42a17cdb3542ebc000ff3e0b51ab66e4a64ca39b8ee52bb2d7a6be30b427b2",
            notes="Modern 10 m baseline. Built-up = 5.9 km², Cropland = 21.9 km², Tree cover = 61.0 km² inside Kelani floodwater."
        ),
        DatasetEntry(
            dataset_id="DS08_ESA_CCI_LANDCOVER_2010",
            name="ESA Climate Change Initiative (CCI) Land Cover",
            version="v2.0.7 (2010)",
            provider="ESA CCI Land Cover Consortium",
            spatial_resolution="300 m",
            temporal_resolution="Annual Static",
            temporal_coverage="2010",
            license_type="ESA Open Access",
            access_protocol="NetCDF / GeoTIFF",
            verification_level="L4_HISTORIC_VERIFIED",
            sha256="b42a9b7cfc8430e793e2b202511475dfd3d4b68e928abdc70cae4ec43a7a9238",
            notes="2010 concurrent baseline. Built-up = 21.7 km² (urban cells contain 45% WorldCover built-up)."
        ),
        DatasetEntry(
            dataset_id="DS09_COPERNICUS_EMSR851_PLANETSCOPE",
            name="Copernicus EMS Rapid Mapping EMSR851 Delineation (Nov 30)",
            version="AOI 02 Kelani Ganga River",
            provider="Copernicus Emergency Management Service / PlanetScope",
            spatial_resolution="3 m optical / EO",
            temporal_resolution="Single Acquisition (2025-11-30 05:39 UTC)",
            temporal_coverage="2025-11-30",
            license_type="Copernicus Open Access / European Union",
            access_protocol="Copernicus EMS Portal Download",
            verification_level="L5_EO_OBSERVED_VERIFIED",
            sha256="385b290cb6467389a6911c47df1292ce3b9847192661fa25e9821bb462ef5e96",
            notes="Observed flooded area = 33.77 km². DTM extrapolation = 67.6 km² kept strictly separate."
        ),
        DatasetEntry(
            dataset_id="DS10_COPERNICUS_EMSR851_LEGION",
            name="Copernicus EMS Rapid Mapping EMSR851 Monitoring (Dec 3)",
            version="AOI 02 Kelani Ganga River",
            provider="Copernicus EMS / Maxar Legion",
            spatial_resolution="0.5 m VHR optical",
            temporal_resolution="Single Acquisition (2025-12-03 07:06 UTC)",
            temporal_coverage="2025-12-03",
            license_type="Copernicus Open Access / European Union",
            access_protocol="Copernicus EMS Portal Download",
            verification_level="L5_EO_OBSERVED_VERIFIED",
            sha256="7c50a1df24cf8f830d93540eb424c8fe22904c165a25e68b3f273be82547b744",
            notes="Observed flooded area = 6.88 km² + 1.23 km² trace. 30.1% of AOI obstructed."
        ),
        DatasetEntry(
            dataset_id="DS11_COPERNICUS_EMS_REFERENCE_LANDUSE",
            name="Copernicus EMS 2025 Reference Land Use Layer",
            version="EMSR851 Baseline",
            provider="Copernicus EMS / European Union",
            spatial_resolution="Vector Baseline",
            temporal_resolution="Static (2025)",
            temporal_coverage="2025",
            license_type="Copernicus Open Access",
            access_protocol="EMS Vector Layer",
            verification_level="L4_BASELINE_VERIFIED",
            sha256="9a4468f7d934279b32c525f9b4da486f0c608f01b1b11da0c102a0a2569e5d4c",
            notes="Corridor land use: 69% forest/semi-natural, 4% agricultural, 27% other."
        ),
        DatasetEntry(
            dataset_id="DS12_SURVEY_DEPT_DS_DIVISIONS",
            name="Survey Department Sri Lanka Divisional Secretariat Boundaries",
            version="2023 Official Release",
            provider="Department of Surveys, Sri Lanka / OCHA",
            spatial_resolution="1:50,000 Administrative Boundaries",
            temporal_resolution="Static (2023)",
            temporal_coverage="2023",
            license_type="Government of Sri Lanka Open Data",
            access_protocol="Shapefile Import",
            verification_level="L5_ADMIN_VERIFIED",
            sha256="0c814b62be8c94625b16f1b34ea6cf7db30a91176dc73ee45155f9f68e98348a",
            notes="Breakdown across Colombo, Gampaha, Kalutara, and Kegalle districts."
        ),
        DatasetEntry(
            dataset_id="DS13_NASA_GPM_IMERG_V07",
            name="NASA Global Precipitation Measurement (GPM) IMERG Late V07",
            version="V07B Half-Hourly",
            provider="NASA Goddard Space Flight Center / PMM",
            spatial_resolution="0.1 deg (~10 km)",
            temporal_resolution="Half-Hourly (calibrated rate mm/h)",
            temporal_coverage="2024-2026",
            license_type="NASA Open Data",
            access_protocol="Earthdata HTTPS / HDF5",
            verification_level="L3_SPEC_VERIFIED",
            sha256="61a3f68a8559134a6efbc52ef5a1532beab2e20a234057864f9cb3501a35010b",
            notes="Used via CHIRPS v3 sat disaggregation. Conversion: mm/h * 0.5h."
        ),
        DatasetEntry(
            dataset_id="DS14_COPERNICUS_HYDRO_NETWORK",
            name="Copernicus Hydrographic River Network Sri Lanka",
            version="2024",
            provider="Copernicus / European Environment Agency",
            spatial_resolution="1:100,000 vector lines",
            temporal_resolution="Static",
            temporal_coverage="2024",
            license_type="Copernicus Open Access",
            access_protocol="GeoJSON Vector",
            verification_level="L5_TOPOLOGY_VERIFIED",
            sha256="ef28a071ce54f3b79dae5cfbe63d4204c3e80f92b772b1574a441df80c854189",
            notes="98.5% of Kelani mainstem river line enclosed within reverse-traversed HydroBASINS polygon."
        ),
    ]

    for entry in entries:
        reg.register(entry)

    return reg
