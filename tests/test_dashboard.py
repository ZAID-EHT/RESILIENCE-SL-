"""
Integration tests for the Streamlit research workbench, pre-computed tables,
provenance hashes, and safety disclaimer compliance.
"""

import json
from pathlib import Path
import pytest
import pandas as pd

from rsl.checksums import sha256_file


PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
APP_FILE = Path(__file__).resolve().parent.parent / "app" / "streamlit_app.py"


EXPECTED_TABLES = [
    "panel_a_stratum_metrics.csv",
    "panel_a_seasonal_metrics.csv",
    "panel_a_reference_agreement.csv",
    "panel_a_calibration.csv",
    "panel_a_event_counts.csv",
    "panel_a_top15_heavy_days.csv",
    "panel_b_basin_floodwater_units.csv",
    "panel_b_landcover_sensitivity.csv",
    "panel_b_cci_worldcover_crosswalk.csv",
    "panel_b_ds_divisions.csv",
    "ditwah_rainfall_leads.csv",
    "ditwah_emsr851_corridor.csv",
    "evidence_status_gates.csv",
    "dataset_register.csv",
]


def test_processed_tables_exist():
    """Verifies that all 14 required pre-computed tables exist in data/processed/."""
    for table_name in EXPECTED_TABLES:
        table_path = PROCESSED_DIR / table_name
        assert table_path.is_file(), f"Missing required pre-computed table: {table_name}"


def test_provenance_json_integrity():
    """Verifies provenance.json exists and its recorded hashes match current files on disk."""
    prov_path = PROCESSED_DIR / "provenance.json"
    assert prov_path.is_file(), "Missing provenance.json"

    with open(prov_path, "r", encoding="utf-8") as f:
        prov_data = json.load(f)

    assert "generated_tables" in prov_data
    table_hashes = prov_data["generated_tables"]

    for table_name in EXPECTED_TABLES:
        assert table_name in table_hashes, f"Table {table_name} missing from provenance.json"
        actual_hash = sha256_file(PROCESSED_DIR / table_name)
        expected_hash = table_hashes[table_name]
        assert actual_hash == expected_hash, f"SHA-256 mismatch for {table_name}!"


def test_safety_disclaimer_banner_present():
    """Verifies that the mandatory safety disclaimer banner is strictly present in streamlit_app.py."""
    assert APP_FILE.is_file(), "streamlit_app.py not found!"
    app_text = APP_FILE.read_text(encoding="utf-8")

    expected_banner_subtext = (
        "Research prototype. Not an official warning or a live flood-risk map. "
        "Areas outside historical mapped footprints are not necessarily safe."
    )
    assert expected_banner_subtext in app_text, "Mandatory safety banner text missing from streamlit_app.py!"


def test_product_sensitivity_wording_enforced():
    """Asserts that land-cover exposure uses 'product sensitivity' wording."""
    app_text = APP_FILE.read_text(encoding="utf-8")
    assert "product sensitivity" in app_text.lower(), "Wording 'product sensitivity' must be present in app."


def test_verified_panel_a_exact_values():
    """Validates exact numerical values in panel_a_stratum_metrics.csv against Phase 1 V3."""
    df = pd.read_csv(PROCESSED_DIR / "panel_a_stratum_metrics.csv")
    s1_v2_l1 = df[(df["stratum"] == "S1") & (df["reference"] == "v2.0") & (df["lead_day"] == 1)].iloc[0]

    assert s1_v2_l1["valid_days"] == 541
    assert s1_v2_l1["clusters"] == 55
    assert s1_v2_l1["bias_mm"] == -0.24
    assert s1_v2_l1["bias_ci_low"] == -2.27
    assert s1_v2_l1["bias_ci_high"] == 2.76
    assert s1_v2_l1["mae_mm"] == 8.65
    assert s1_v2_l1["mae_ci_low"] == 6.89
    assert s1_v2_l1["mae_ci_high"] == 10.05
    assert s1_v2_l1["rmse_mm"] == 13.45


def test_verified_panel_b_exact_values():
    """Validates exact numerical values in panel_b_basin_floodwater_units.csv."""
    df = pd.read_csv(PROCESSED_DIR / "panel_b_basin_floodwater_units.csv")
    inside_row = df[df["spatial_unit"].str.contains("Inside Verified Kelani")].iloc[0]
    total_row = df[df["spatial_unit"].str.contains("Full 2010 Map Frame")].iloc[0]

    assert inside_row["area_km2"] == 100.40
    assert inside_row["share_percent"] == 23.23
    assert total_row["area_km2"] == 432.24
    assert total_row["share_percent"] == 100.00


def test_verified_ditwah_exact_values():
    """Validates exact Cyclone Ditwah forecast shift and satellite discordance values."""
    df = pd.read_csv(PROCESSED_DIR / "ditwah_rainfall_leads.csv")
    nov27 = df[df["valid_date_utc"] == "2025-11-27"].iloc[0]

    # Forecast shifts: Lead 3 (202.6) -> Lead 2 (117.2) -> Lead 1 (65.9)
    assert nov27["forecast_lead3_mm"] == 202.6
    assert nov27["forecast_lead2_mm"] == 117.2
    assert nov27["forecast_lead1_mm"] == 65.9

    # Reference discordance: 65.4 vs 100.6
    assert nov27["chirps_v2_mm"] == 65.4
    assert nov27["chirps_v3_sat_mm"] == 100.6


def test_dataset_register_count():
    """Validates that dataset_register.csv contains exactly 14 monitored datasets."""
    df = pd.read_csv(PROCESSED_DIR / "dataset_register.csv")
    assert len(df) == 14
    assert "DS01_ECMWF_IFS_OPERATIONAL" in df["dataset_id"].values
    assert "DS14_COPERNICUS_HYDRO_NETWORK" in df["dataset_id"].values
