"""
RESILIENCE SL: Five-View Research Workbench
Evidence-Based Rainfall-Forecast Reliability and Historical Flood Exposure for the Kelani Catchment, Sri Lanka.

ModelX 2.0 Open Research Workbench (Offline Capable).
"""

import sys
from pathlib import Path
from typing import Dict, Optional
import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk

# Add src to path for offline module imports
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from rsl.checksums import sha256_file

# Directory configuration
PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

# Page configuration
st.set_page_config(
    page_title="RESILIENCE SL | Research Workbench",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Permanent Mandatory Safety Banner
SAFETY_BANNER_PLAIN = "Research prototype. Not an official warning or a live flood-risk map. Areas outside historical mapped footprints are not necessarily safe."
SAFETY_BANNER_TEXT = f"⚠️ **{SAFETY_BANNER_PLAIN}**"


def render_permanent_banner():
    st.markdown(
        f"""
        <div style="background-color: #fff3cd; color: #856404; padding: 12px 18px; 
                    border-radius: 6px; border: 1px solid #ffeeba; margin-bottom: 18px; font-size: 15px;">
            {SAFETY_BANNER_TEXT}
        </div>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def load_processed_table(filename: str) -> Optional[pd.DataFrame]:
    """
    Safely loads pre-computed verified tables from data/processed/.
    Fails gracefully with a clear plain-language warning if the file is missing, never raising a stack trace.
    """
    filepath = PROCESSED_DIR / filename
    if not filepath.is_file():
        st.error(
            f"⚠️ **Missing Data Table:** The required file `{filename}` was not found in `{PROCESSED_DIR}`. "
            f"Please run `python scripts/generate_tables.py` to regenerate all verified tables."
        )
        return None
    try:
        return pd.read_csv(filepath)
    except Exception as e:
        st.error(f"⚠️ **Error Reading Table:** Could not read `{filename}`: {str(e)}")
        return None


# Sidebar Navigation
st.sidebar.image("https://raw.githubusercontent.com/ZAID-EHT/RESILIENCE-SL-/main/docs/assets/logo.png" if False else "🌊", width=50)
st.sidebar.title("RESILIENCE SL")
st.sidebar.caption("Kelani Catchment Research Workbench (Phase 2)")

nav_selection = st.sidebar.radio(
    "Select Research View:",
    [
        "1. Overview & Protocol",
        "2. Panel A: Rainfall Reliability",
        "3. Panel B: Flood Exposure",
        "4. Cyclone Ditwah Case Study",
        "5. Provenance & Gates",
    ],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Basin:** Kelani River ($2,325.2\\text{ km}^2$)\n
    **Target Pilots:** C1 (Coastal), C2 (Mid), C3 (Upland)\n
    **Forecast Model:** ECMWF IFS HRES (9 km)\n
    **References:** CHIRPS v2.0 & v3.0 sat\n
    **Status:** Fully Offline Research Prototype
    """
)

# ==============================================================================
# VIEW 1: Overview, Scientific Boundary & Readiness Protocol
# ==============================================================================
if nav_selection == "1. Overview & Protocol":
    render_permanent_banner()

    st.title("Kelani Catchment Evidence Triage Workbench")
    st.subheader("Objective Meteorological Verification & Hydrologic Exposure Analysis")

    st.markdown(
        """
        The **RESILIENCE SL** research workbench provides an evidence-based decision framework for disaster managers,
        hydrologists, and Divisional Secretariat officers in the Kelani River Basin (Western and Sabaragamuwa Provinces).
        
        Rather than attempting to forecast river flood heights or manufacturing an uncalibrated composite risk score,
        this system strictly separates **atmospheric forecast reliability** from **historical land-cover flood exposure**.
        """
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 🏛️ The Two-Panel Evidence Architecture")
        st.info(
            """
            - **Panel A (Atmospheric Reliability):** Rigorous evaluation of ECMWF Integrated Forecasting System (IFS HRES)
              rainfall forecasts at 24h, 48h, and 72h lead times against two independent satellite precipitation references
              (CHIRPS v2.0 and CHIRPS v3.0 `sat`).
            - **Panel B (Historical Exposure):** Geodesically-clipped flood exposure accounting for the May 2010 disaster
              ($100.40\\text{ km}^2$ inside Kelani) over 10 m ESA WorldCover and 300 m ESA CCI land cover.
            """
        )

        st.markdown("### 🚫 What the System Refuses to Do (Epistemic Boundaries)")
        st.error(
            """
            1. **Never Combines into a Single Risk Score:** Rainfall forecast error and land-cover exposure operate on different
               physical scales; multiplying them produces unverified mathematical illusions.
            2. **Never Overclaims Heavy-Rain Predictive Skill:** With only 8 independent events $\\ge 50\\text{ mm}$ in the operational
               record (below the pre-registered 20-event gate), parametric skill metrics are suppressed.
            3. **Never Confuses Model Extrapolation with Satellite Truth:** During Cyclone Ditwah, digital elevation model (DTM)
               extrapolations ($67.6\\text{ km}^2$) are strictly kept separate from earth observation ($33.77\\text{ km}^2$).
            4. **Never Relies on a Single Reference:** Bias statements are marked *Supported* only if both CHIRPS v2.0 and
               CHIRPS v3.0 `sat` agree in sign and their bootstrap intervals exclude zero.
            """
        )

    with col2:
        st.markdown("### 📋 5-Task Practitioner Verification Checklist")
        st.caption("Step through this protocol to verify research integrity (see `docs/USABILITY_PROTOCOL.md`).")

        t1 = st.checkbox("Task 1: Verify epistemic safeguards and safety disclaimer banner", value=True)
        t2 = st.checkbox("Task 2: Query 48–72h forecast error for Coastal Cell C1 (Lead 2, Stratum S1)")
        t3 = st.checkbox("Task 3: Trigger the heavy-rain refusal state (select subset >= 50 mm)")
        t4 = st.checkbox("Task 4: Contrast catchment-clipped (100.4 km²) vs unclipped (432.24 km²) floodwater")
        t5 = st.checkbox("Task 5: Inspect Cyclone Ditwah forecast lead shift and reference disagreement")

        completed_tasks = sum([t1, t2, t3, t4, t5])
        st.progress(completed_tasks / 5.0)
        st.write(f"**Verification Progress:** {completed_tasks} / 5 Tasks Completed ({completed_tasks * 20}%)")

        if completed_tasks == 5:
            st.success("🎉 All 5 practitioner verification tasks completed! Epistemic safeguards verified.")
        else:
            st.info("Complete the remaining tasks across Views 2, 3, and 4 to validate workbench compliance.")

# ==============================================================================
# VIEW 2: Panel A: Rainfall-Forecast Reliability
# ==============================================================================
elif nav_selection == "2. Panel A: Rainfall Reliability":
    render_permanent_banner()

    st.title("Panel A: Rainfall-Forecast Reliability Evaluation")
    st.caption("ECMWF IFS HRES (9 km) vs CHIRPS v2.0 and CHIRPS v3.0 sat (Co-Primary References)")

    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1, 1, 1])

    with col_ctrl1:
        stratum_sel = st.selectbox(
            "Select Forecast Stratum:",
            ["S1 (Operational Cycle 49r1)", "S0 (Retrospective Hindcast)", "S2 (Operational Cycle 50r1)"],
            index=0,
        )
        stratum_code = "S1" if "S1" in stratum_sel else ("S0" if "S0" in stratum_sel else "S2")

    with col_ctrl2:
        subset_sel = st.selectbox(
            "Select Evaluation Subset:",
            ["All Days", "Seasonal Breakdown", "Heavy Rain >= 50 mm", "Heavy Rain >= 100 mm"],
            index=0,
        )

    with col_ctrl3:
        ref_sel = st.selectbox(
            "Select Satellite Reference:",
            ["Side-by-Side Comparison", "CHIRPS v2.0", "CHIRPS v3.0 sat"],
            index=0,
        )

    st.markdown("---")

    # Handling Heavy Rain Refusal State
    if "Heavy Rain" in subset_sel:
        st.markdown(
            """
            <div style="background-color: #f8d7da; color: #721c24; padding: 16px; border-radius: 8px; border: 2px solid #f5c6cb; margin-bottom: 20px;">
                <h4 style="margin:0 0 8px 0;">🛑 INSUFFICIENT EVIDENCE: PRE-REGISTERED REFUSAL GATE TRIGGERED</h4>
                <p style="margin:0; font-size: 14.5px;">
                    In Stratum S1, only <b>8 independent meteorological event groups</b> contain a day with rainfall &ge; 50 mm against either reference 
                    (below the pre-registered <b>20-event gate threshold</b>). At &ge; 100 mm, at most 1 event group exists.<br><br>
                    <b>Epistemic Refusal Enforced:</b> The system strictly refuses to output parametric skill metrics (POD, FAR, CSI, Brier Scores) 
                    or probability scores to prevent dangerous false certainty. Displaying empirical descriptive case logs only.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        df_heavy = load_processed_table("panel_a_top15_heavy_days.csv")
        if df_heavy is not None:
            st.markdown("#### Descriptive Registry of Top Heavy-Rain Event Days (Stratum S1)")
            st.dataframe(df_heavy, use_container_width=True)

    elif subset_sel == "Seasonal Breakdown":
        st.markdown(f"#### Seasonal Breakdown for Lead 2 (48–72h) in Stratum {stratum_code}")
        df_seasonal = load_processed_table("panel_a_seasonal_metrics.csv")
        if df_seasonal is not None:
            sub = df_seasonal[df_seasonal["stratum"] == stratum_code]
            st.dataframe(sub, use_container_width=True)

            st.info(
                """
                **Monsoon Regime Findings:**
                - **Southwest Monsoon (SW):** Demonstrates systematic over-forecasting by ECMWF in S0 (+8.9 mm) and S2 (+10.5 mm),
                  both statistically significant against both references (**Supported**).
                - **Inter-Monsoon (IM1 / IM2):** ECMWF consistently underestimates localized convective cloudbursts (-5.5 to -7.4 mm),
                  but satellite uncertainty keeps status **Reference-Dependent**.
                - **Amendment A5:** Subsets with < 5 clusters display `not estimable (<5 clusters)`.
                """
            )

    else:
        # All Days View
        df_stratum = load_processed_table("panel_a_stratum_metrics.csv")
        if df_stratum is not None:
            sub = df_stratum[df_stratum["stratum"] == stratum_code]
            if ref_sel == "CHIRPS v2.0":
                sub = sub[sub["reference"] == "v2.0"]
            elif ref_sel == "CHIRPS v3.0 sat":
                sub = sub[sub["reference"] == "v3.0 sat"]

            st.markdown(f"#### Forecast Verification Metrics: Stratum {stratum_code} (All Days)")
            st.dataframe(sub, use_container_width=True)

            # Metric Cards
            if stratum_code == "S1" and ref_sel == "Side-by-Side Comparison":
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Lead 1 Bias (v2 vs v3)", "-0.24 mm / -1.09 mm", delta="Inconclusive")
                m2.metric("Lead 1 MAE (v2 vs v3)", "8.65 mm / 8.75 mm")
                m3.metric("Lead 2 Bias (v2 vs v3)", "-0.47 mm / -1.32 mm", delta="Inconclusive")
                m4.metric("Valid Cell-Days", "541 Days", delta="99.1% Complete")

        st.markdown("---")

        # Sub-panel 1: Calibration Results
        st.markdown("### ⚙️ Statistical Calibration Comparison (Rolling-Origin Cross-Validation)")
        st.caption("Evaluated on 30-day held-out test blocks with a 3-day purge buffer. Gate requirement: >= 20 event groups in both train and test.")
        df_cal = load_processed_table("panel_a_calibration.csv")
        if df_cal is not None:
            st.dataframe(df_cal, use_container_width=True)
            st.warning(
                "**Result:** All three post-processing schemes failed to outperform the raw ECMWF forecast on held-out blocks. "
                "Day-of-year climatology degraded MAE (+1.2 to +2.0 mm), while seasonal bias and ridge had intervals crossing zero. "
                "**The raw ECMWF forecast is retained.**"
            )

        st.markdown("---")

        # Sub-panel 2: Reference Agreement Across Pilot Cells
        st.markdown("### 🛰️ Reference Agreement Diagnostic: CHIRPS v2.0 vs CHIRPS v3.0 sat")
        st.caption("Direct cross-comparison over 900 calendar dates across the three pilot grid cells.")
        df_ref = load_processed_table("panel_a_reference_agreement.csv")
        if df_ref is not None:
            st.dataframe(df_ref, use_container_width=True)
            st.markdown(
                """
                > **Elevation Gradient Finding:** Daily correlation drops from **0.73** at the coast (C1) to **0.62** in the upland headwaters (C3).
                > Days with rainfall $\ge 50\\text{ mm}$ diverge by a factor of $2.4\\times$ at Kitulgala (15 days in v2.0 vs 36 days in v3.0 sat).
                > Neither satellite product can be treated as absolute ground truth.
                """
            )

# ==============================================================================
# VIEW 3: Panel B: Kelani Catchment Historical Flood Exposure
# ==============================================================================
elif nav_selection == "3. Panel B: Flood Exposure":
    render_permanent_banner()

    st.title("Panel B: Kelani Catchment Historical Flood Exposure")
    st.caption("May 2010 World Bank/ESA Flood Inundation Envelope & Multi-Resolution Land-Cover Analysis")

    view_toggle = st.radio(
        "Select Spatial Delineation Frame:",
        ["Clipped to Verified Kelani Catchment (100.40 km²)", "Unclipped Full Map Frame (432.24 km²)"],
        index=0,
        horizontal=True,
    )

    st.markdown("---")

    col_map, col_stat = st.columns([3, 2])

    with col_map:
        st.markdown("#### Hydrologic Watershed & Flood Footprint Map")

        # PyDeck offline rendering
        # Pilot cells coordinates
        pilot_data = [
            {"name": "C1: Coastal / Colombo", "lat": 6.924429, "lon": 79.90725, "color": [255, 0, 0]},
            {"name": "C2: Mid-basin / Hanwella", "lat": 6.924429, "lon": 80.05902, "color": [0, 200, 0]},
            {"name": "C3: Upland / Kitulgala", "lat": 6.9947276, "lon": 80.35442, "color": [0, 0, 255]},
        ]
        df_pilots = pd.DataFrame(pilot_data)

        # Polygon boundaries for Kelani Catchment (approximated boundary envelope for offline visual)
        catchment_poly = [
            [79.86, 6.92], [79.92, 6.89], [80.05, 6.85], [80.25, 6.82], [80.45, 6.90],
            [80.52, 7.05], [80.40, 7.15], [80.20, 7.18], [80.02, 7.10], [79.90, 7.02],
            [79.86, 6.92]
        ]
        flood_poly_clipped = [
            [79.88, 6.93], [79.95, 6.91], [80.02, 6.89], [80.08, 6.93],
            [80.02, 6.97], [79.93, 6.98], [79.88, 6.93]
        ]
        polygon_layer = pdk.Layer(
            "PolygonLayer",
            data=[{"polygon": catchment_poly, "name": "Kelani Catchment Boundary (2325.2 km²)"}],
            get_polygon="polygon",
            get_fill_color=[240, 240, 240, 40],
            get_line_color=[30, 144, 255, 200],
            line_width_min_pixels=3,
            pickable=True,
        )
        flood_layer = pdk.Layer(
            "PolygonLayer",
            data=[{"polygon": flood_poly_clipped, "name": "May 2010 Flood Inundation Envelope"}],
            get_polygon="polygon",
            get_fill_color=[65, 105, 225, 140],
            get_line_color=[0, 0, 139, 255],
            line_width_min_pixels=2,
            pickable=True,
        )
        scatter_layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_pilots,
            get_position=["lon", "lat"],
            get_color="color",
            get_radius=2500,
            pickable=True,
        )

        deck = pdk.Deck(
            layers=[polygon_layer, flood_layer, scatter_layer],
            initial_view_state=pdk.ViewState(latitude=6.96, longitude=80.12, zoom=9.2, pitch=0),
            tooltip={"text": "{name}"},
        )
        st.pydeck_chart(deck)
        st.caption("🔵 Blue Polygon: May 2010 Flood Envelope | 🌐 Outline: HydroBASINS Level 8/10 Watershed | 🔴 C1, 🟢 C2, 🔵 C3: Pilot Forecast Cells")

    with col_stat:
        st.markdown("#### Catchment Boundary Allocation")
        df_units = load_processed_table("panel_b_basin_floodwater_units.csv")
        if df_units is not None:
            st.dataframe(df_units[["spatial_unit", "area_km2", "share_percent"]], use_container_width=True)

        if "Clipped" in view_toggle:
            st.success(
                "**Hydrological Clipping Result:** Only **100.40 km² (23.2%)** of the 432.24 km² mapped floodwater "
                "actually fell inside the Kelani catchment boundary. The remaining 76.8% occurred in adjacent coastal units (47.6 km²) "
                "and neighbouring basins (284.2 km²). Raw unclipped maps overstate Kelani exposure by over 400%!"
            )
        else:
            st.warning(
                "**Unclipped Full Map Frame:** The raw 2010 flood file encloses 432.24 km² across 12,734 polygons. "
                "Over 65.8% of this area belongs to the Kalu, Attanagalu, and Negombo basins."
            )

    st.markdown("---")

    # Land Cover Product Sensitivity
    st.markdown("### 🏘️ Land-Cover Product Sensitivity: WorldCover (10m) vs ESA CCI (300m)")
    st.caption("Analysis of the 100.40 km² Kelani Catchment flood footprint across sensor resolutions.")

    df_sens = load_processed_table("panel_b_landcover_sensitivity.csv")
    if df_sens is not None:
        st.dataframe(df_sens, use_container_width=True)

    col_sens1, col_sens2 = st.columns(2)

    with col_sens1:
        st.markdown("#### The Urban Aggregation Diagnostic")
        st.info(
            """
            - **ESA WorldCover 2021 (10 m):** Built-up flood exposure is **5.90 km²**.
            - **ESA CCI 2010 (300 m):** Urban flood exposure is reported as **21.70 km²** ($3.7\\times$ higher).
            - **Diagnostic Proof:** Overlaying 10 m pixels inside 300 m CCI cells proves that CCI urban cells contain on average 
              only **45% actual built-up structures**. The remaining 55% consists of gardens, access roads, and small canals.
            """
        )
        df_xwalk = load_processed_table("panel_b_cci_worldcover_crosswalk.csv")
        if df_xwalk is not None:
            st.dataframe(df_xwalk, use_container_width=True)

    with col_sens2:
        st.markdown("#### The 61% Tree-Cover / Canopy Phenomenon")
        st.info(
            """
            - **WorldCover 2021:** Tree cover accounts for **61.00 km² (60.8%)** of the inundated footprint.
            - **Copernicus EMS 2025 Baseline:** In the river corridor AOI 02, reference land use indicates **69% forest/semi-natural**.
            - **Physical Reality:** In the wet-zone floodplains of Sri Lanka, extensive rural home-gardens (*gewathu*), rubber plantations,
              and coconut groves maintain a dense overstory canopy above inundated ground surfaces.
            """
        )
        df_ds = load_processed_table("panel_b_ds_divisions.csv")
        if df_ds is not None:
            st.markdown("##### Divisional Secretariat Exposure Breakdown")
            st.dataframe(df_ds, use_container_width=True)

# ==============================================================================
# VIEW 4: Cyclone Ditwah Case Study (Nov 2025)
# ==============================================================================
elif nav_selection == "4. Cyclone Ditwah Case Study":
    render_permanent_banner()

    st.title("Disaster Stress Test: Cyclone Ditwah (November 2025)")
    st.caption("End-to-End Evaluation of Multi-Lead Forecast Shift and Copernicus EMSR851 Rapid Mapping")

    st.markdown(
        """
        During the late-November 2025 Cyclone Ditwah event, extreme cyclonic rainfall triggered major inundation along the Kelani Ganga.
        This case provides an empirical stress test of multi-lead forecast stability and satellite flood mapping.
        """
    )

    st.markdown("### 🌧️ Forecast Evolution Across Leads at Coastal Cell C1")
    df_ditwah_rain = load_processed_table("ditwah_rainfall_leads.csv")
    if df_ditwah_rain is not None:
        col_t, col_c = st.columns([3, 2])
        with col_t:
            st.dataframe(df_ditwah_rain, use_container_width=True)
        with col_c:
            st.markdown(
                """
                **Critical Lead-Shift Findings (2025-11-27):**
                - **Lead 3 (72–96h):** Predicted an extreme **202.6 mm** deluge.
                - **Lead 2 (48–72h):** Dropped to **117.2 mm**.
                - **Lead 1 (24–48h):** Settled at **65.9 mm** (a $136.7\\text{ mm}$ shift!).
                - **Realized Satellite Rain:** CHIRPS v2.0 recorded **65.4 mm** (closely matching Lead 1), 
                  whereas CHIRPS v3.0 `sat` recorded **100.6 mm** (a $35.2\\text{ mm}$ reference spread).
                """
            )

    st.markdown("---")

    st.markdown("### 🛰️ Copernicus EMS Rapid Mapping (EMSR851, AOI 02 Kelani Corridor)")
    st.caption("Corridor extent: 236.6 km² (97.8% inside the verified Kelani catchment).")

    df_ems = load_processed_table("ditwah_emsr851_corridor.csv")
    if df_ems is not None:
        st.dataframe(df_ems, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Nov 30, 2025 Peak Analysis (PlanetScope Optical)")
        st.info(
            """
            - **Earth Observation (EO) Observed Floodwater:** **33.77 km²**
            - **Land Cover Under Flood:** 66% Tree cover, 13% Cropland, 10% Built-up.
            - **Overlap with 2010 Footprint:** **52.0%** of the 2010 corridor flood footprint was re-inundated.
            - **Model-Based DTM Extrapolation:** **67.60 km²** (Reported strictly separately; **never added to EO**).
            - **Quality Gate:** Passed (Not-analysed area = 2.7% < 50% threshold).
            """
        )
    with c2:
        st.markdown("#### Dec 03, 2025 Recession Analysis (Maxar Legion VHR)")
        st.info(
            """
            - **EO Observed Floodwater:** **6.88 km²** + **1.23 km²** flood trace.
            - **Model-Based Extrapolation:** **28.00 km²**.
            - **Not-Analysed Area:** **30.1%** of AOI (due to cloud cover and sensor angles; passed < 50% gate).
            - **Hydrological Insight:** Captures rapid drainage in urban Colombo while mid-basin agricultural backwaters lingered.
            """
        )

# ==============================================================================
# VIEW 5: Data Provenance, Pre-Registration Gates & Exports
# ==============================================================================
elif nav_selection == "5. Provenance & Gates":
    render_permanent_banner()

    st.title("Data Provenance, Pre-Registration Gates & Audit Registry")
    st.caption("Cryptographic Verification, Open Licences, and Bit-for-Bit Reproducibility")

    st.markdown("### 🛡️ Pre-Registered Gates & Protocol Amendments")
    df_gates = load_processed_table("evidence_status_gates.csv")
    if df_gates is not None:
        st.dataframe(df_gates, use_container_width=True)

    st.markdown("---")

    st.markdown("### 🗄️ Dataset Verification Register (14 Monitored Datasets)")
    df_reg = load_processed_table("dataset_register.csv")
    if df_reg is not None:
        st.dataframe(
            df_reg[["dataset_id", "name", "version", "provider", "verification_level", "license_type", "sha256"]],
            use_container_width=True,
        )

    st.markdown("---")

    st.markdown("### 💾 One-Click Data Table Exports")
    st.caption("Download all pre-computed verified tables in CSV format.")

    all_csvs = [
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

    exp_cols = st.columns(3)
    for idx, fname in enumerate(all_csvs):
        col = exp_cols[idx % 3]
        fpath = PROCESSED_DIR / fname
        if fpath.is_file():
            with open(fpath, "rb") as f:
                col.download_button(
                    label=f"📥 {fname}",
                    data=f.read(),
                    file_name=fname,
                    mime="text/csv",
                    key=f"dl_{fname}",
                )

    st.markdown("---")
    st.markdown(
        """
        **Reproducibility Command:**  
        ```bash
        python scripts/generate_tables.py && pytest
        ```
        """
    )
