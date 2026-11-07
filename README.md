# RESILIENCE SL: Evidence-Based Rainfall-Forecast Reliability and Historical Flood Exposure for the Kelani Catchment, Sri Lanka

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests: 49 Passed](https://img.shields.io/badge/tests-49%20passed-brightgreen.svg)]()
[![Reproducibility: Bit--for--Bit](https://img.shields.io/badge/reproducibility-deterministic%20SHA--256-success.svg)]()
[![ModelX 2.0](https://img.shields.io/badge/Hackathon-ModelX%202.0-orange.svg)](https://modelx2.pages.dev/)


> **Research prototype. Not an official warning or a live flood-risk map. Areas outside historical mapped footprints are not necessarily safe.**

---

## 1. Executive Summary & Purpose

The Kelani River Basin ($2,325.2\text{ km}^2$) is Sri Lanka's economic and population heartland, housing over a quarter of the island's citizens and driving one-third of national GDP through the Colombo commercial zone. Despite severe recurrent inundations (e.g., May 2010, May 2016, and November 2025 Cyclone Ditwah), disaster managers routinely face an evidence gap: numerical weather predictions from global centres (ECMWF IFS) are acted upon without localized lead-resolved error boundaries, while historical satellite flood maps are frequently cited without hydrologic boundary clipping or resolution sensitivity disclosures.

**RESILIENCE SL** delivers an open-source, offline-capable scientific research workbench that establishes:
1. **Panel A (Atmospheric Reliability):** Systematic verification of ECMWF Integrated Forecasting System (IFS HRES, native 9 km) 24–96 h precipitation forecasts against two co-primary satellite precipitation products (CHIRPS v2.0 and CHIRPS v3.0 `sat`).
2. **Panel B (Historical Exposure):** Geodesically-clipped flood exposure accounting for the May 2010 disaster ($100.40\text{ km}^2$ inside Kelani) evaluated across multi-resolution land cover (10 m ESA WorldCover and 300 m ESA CCI).

---

## 2. Core Epistemic Safeguards: What the System Refuses to Do

To protect lives and preserve scientific integrity, RESILIENCE SL enforces four computational refusal gates:

| # | Epistemic Safeguard | Operational Action |
|---|---|---|
| **1** | **No Invented "Flood Risk Scores"** | Strictly separates rainfall reliability (Panel A) from land-cover exposure (Panel B). Never multiplies atmospheric uncertainty with satellite exposure to manufacture artificial risk numbers. |
| **2** | **Refusal on Sparse Heavy Events** | Pre-registered gate requires $\ge 20$ independent meteorological event groups. In Stratum S1, only **8 groups** contain a day $\ge 50\text{ mm}$. The system suppresses parametric skill scores and presents descriptive empirical logs. |
| **3** | **No Model Extrapolation Conflation** | During Cyclone Ditwah, digital terrain model (DTM) flood extrapolations ($67.6\text{ km}^2$) are strictly segregated from satellite Earth Observation ($33.77\text{ km}^2$). |
| **4** | **Two-Reference Claim Rule** | Bias is marked **"Supported"** only if both CHIRPS v2.0 and CHIRPS v3.0 `sat` have the same sign and both 95% bootstrap intervals exclude zero; otherwise labeled **"Reference-Dependent"** or **"Inconclusive"**. |

---

## 3. Verified Phase 1 V3 Key Scientific Results

Every number in the workbench and test suite strictly matches the verified V3 results:

### A. Study Area & Pilot Cells (`config/sites.yaml`)
- **Kelani Catchment:** Derived via HydroBASINS v1c Asia Level 8 (`HYBAS_ID = 4080049050`, `UP_AREA = 2325.3 km²`) and Level 10 reverse traversal of `NEXT_DOWN` (15 polygons, $\sum \text{SUB\_AREA} = 2325.2\text{ km}^2$, $-0.004\%$ diff, 0 virtual connections `ENDO=2`, $98.5\%$ Copernicus river line enclosed, Colombo district overlap = $454.0\text{ km}^2$).
- **Three Pilot Forecast Cells (ECMWF IFS 9 km native centres):**
  - **C1 (Coastal / Colombo mouth):** Lat `6.924429°N`, Lon `79.90725°E`
  - **C2 (Mid-basin / Hanwella gauge):** Lat `6.924429°N`, Lon `80.05902°E`
  - **C3 (Upland / Kitulgala headwaters):** Lat `6.9947276°N`, Lon `80.35442°E` (East of 2010 flood frame $80.156^\circ\text{E}$)

### B. Atmospheric Forecast Performance (`data/processed/panel_a_stratum_metrics.csv`)
- **Operational Cycle 49r1 (Stratum S1, 541 Valid Days):**
  - **Lead 1 (24–48h):** Bias vs v2.0 = $-0.24\text{ mm}$ (CI: $-2.27$ to $+2.76$); vs v3.0 sat = $-1.09\text{ mm}$ (CI: $-3.33$ to $+1.77$); MAE = $8.65\text{ mm}$ / $8.75\text{ mm}$.
  - **Lead 2 (48–72h):** Bias vs v2.0 = $-0.47\text{ mm}$ (CI: $-2.43$ to $+2.58$); vs v3.0 sat = $-1.32\text{ mm}$ (CI: $-3.87$ to $+1.65$); MAE = $8.80\text{ mm}$ / $8.94\text{ mm}$.
  - **Lead 3 (72–96h):** Bias vs v2.0 = $-0.64\text{ mm}$ (CI: $-2.77$ to $+2.43$); vs v3.0 sat = $-1.49\text{ mm}$ (CI: $-3.84$ to $+1.27$); MAE = $9.30\text{ mm}$ / $9.31\text{ mm}$.
- **Monsoon Regime Breakdown:** Southwest Monsoon exhibits statistically significant over-forecasting in S0 ($+8.9\text{ mm}$ vs v2; $+6.5\text{ mm}$ vs v3 sat) and S2 ($+10.5\text{ mm}$ vs v2; $+9.7\text{ mm}$ vs v3 sat). Inter-monsoon convective rains are underestimated ($-5.5$ to $-7.4\text{ mm}$).
- **Elevation Gradient Discordance:** CHIRPS v2.0 and v3.0 sat daily correlation drops from $0.73$ at the coast (C1) to $0.62$ in upland Kitulgala (C3), where days $\ge 50\text{ mm}$ diverge by $2.4\times$ ($15\text{ vs }36\text{ days}$).
- **Calibration Failure:** Day-of-year climatology worsened error ($+1.2\text{ to }+2.0\text{ mm}$); seasonal bias and ridge regression had intervals crossing zero. **Raw ECMWF forecast is retained.**

### C. Historical Flood Exposure & Resolution Effects (`data/processed/panel_b_basin_floodwater_units.csv`)
- **Hydrological Clipping Impact:**
  - Raw unclipped May 2010 map frame: **$432.24\text{ km}^2$**
  - Inside verified Kelani catchment: **$100.40\text{ km}^2$ ($23.2\%$)**
  - Adjacent coastal units (incl. river mouth): **$47.60\text{ km}^2$ ($11.0\%$)**
  - Other basins falsely attributed if unclipped: **$284.24\text{ km}^2$ ($65.8\%$)**
- **Land-Cover Product Sensitivity (Inside 100.4 km² Kelani Floodwater):**
  - **Built-Up:** ESA WorldCover 10 m reports **$5.9\text{ km}^2$**; ESA CCI 300 m reports **$21.7\text{ km}^2$** ($3.7\times$ overstatement). Crosswalk diagnostic proves 300 m urban cells contain on average only $45\%$ actual buildings.
  - **Cropland:** WorldCover reports **$21.9\text{ km}^2$**; CCI strict reports **$6.3\text{ km}^2$** (expands to **$53.5\text{ km}^2$** with mosaic class 30).
  - **Tree Cover:** Accounts for **$61.0\text{ km}^2$ ($60.8\%$)** due to pervasive wet-zone home gardens (*gewathu*) concealing floodwaters beneath the canopy.

### D. Cyclone Ditwah Stress Test (`data/processed/ditwah_rainfall_leads.csv`)
- **ECMWF Lead Shift (Nov 27, 2025 at C1):** Lead 3 ($202.6\text{ mm}$) $\rightarrow$ Lead 2 ($117.2\text{ mm}$) $\rightarrow$ Lead 1 ($65.9\text{ mm}$).
- **Satellite Disagreement (Nov 27):** CHIRPS v2 recorded $65.4\text{ mm}$ while CHIRPS v3 sat recorded $100.6\text{ mm}$ ($35.2\text{ mm}$ spread).
- **Copernicus EMSR851 (AOI 02 Corridor: 236.6 km²):**
  - Nov 30 (PlanetScope): EO observed floodwater $= 33.77\text{ km}^2$; DTM extrapolation $= 67.60\text{ km}^2$; $52.0\%$ overlap with 2010 footprint.
  - Dec 03 (Legion): EO observed floodwater $= 6.88\text{ km}^2$ + $1.23\text{ km}^2$ trace; DTM extrapolation $= 28.00\text{ km}^2$.

---

## 4. Repository Structure

```text
resilience-sl/
├── .gitignore
├── README.md                           <- Project overview, reproducibility, and verified evidence
├── pyproject.toml                      <- Package configuration and pinned dependencies
├── requirements.txt                    <- Direct pip dependencies
├── docs/
│   ├── PREREGISTRATION.md              <- Pre-registered gates (G1, G2, Heavy, Calib, Amendments A1-A5)
│   ├── TECHNICAL_REPORT.md             <- Full scientific methodology, derivations, and audit logs
│   ├── TWO_PAGE_SUMMARY.md             <- Executive policy brief for Disaster Management Centre (DMC)
│   └── USABILITY_PROTOCOL.md           <- 5-Task practitioner verification protocol
├── config/
│   ├── sites.yaml                      <- Catchment geometry, pilot cell coordinates (C1-C3)
│   └── periods.yaml                    <- Cycle strata (S0, S1, S2), seasons, and gate thresholds
├── src/
│   └── rsl/
│       ├── __init__.py
│       ├── checksums.py                <- Deterministic SHA-256 computation
│       ├── manifest.py                 <- 14-dataset provenance register (L1-L6)
│       ├── acquire/                    <- Parameter builders and data acquisition specs
│       │   ├── openmeteo.py
│       │   ├── chirps.py
│       │   ├── imerg.py
│       │   ├── floodmap.py
│       │   └── landcover.py
│       ├── clean/                      <- Integration, unit conversion, masks, and graph traversal
│       │   ├── time_windows.py
│       │   ├── units.py
│       │   ├── masks.py
│       │   └── geometry.py
│       └── analysis/                   <- Statistical verification and exposure cross-tabulation
│           ├── join.py
│           ├── events.py
│           ├── baselines.py
│           ├── calibrate.py
│           ├── metrics.py
│           ├── bootstrap.py
│           └── exposure.py
├── data/
│   └── processed/                      <- 14 pre-computed verified research CSV tables + provenance.json
├── app/
│   └── streamlit_app.py                <- 5-view offline interactive research workbench
├── tests/                              <- Comprehensive automated pytest suite (49 tests)
│   ├── test_time_windows.py
│   ├── test_units.py
│   ├── test_masks.py
│   ├── test_join.py
│   ├── test_events.py
│   ├── test_geometry.py
│   ├── test_exposure.py
│   ├── test_metrics.py
│   └── test_dashboard.py
└── scripts/
    ├── generate_tables.py              <- Generates all verified CSVs and provenance.json
    ├── run_all.ps1                     <- One-click execution and verification script (PowerShell)
    └── run_all.sh                      <- One-click execution and verification script (Bash)
```

---

## 5. Quickstart & Offline Execution

### 5.1 Installation
Clone the repository and set up a Python virtual environment:
```bash
git clone https://github.com/ZAID-EHT/RESILIENCE-SL-.git
cd RESILIENCE-SL-
git checkout feature/phase2-workbench

python -m venv .venv
# On Windows PowerShell:
.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 5.2 One-Click Pipeline Execution
Run the full verification and regeneration pipeline:
```bash
# On Windows PowerShell:
.\scripts\run_all.ps1

# On Linux/macOS:
chmod +x scripts/run_all.sh
./scripts/run_all.sh
```

### 5.3 Launch the Interactive Research Workbench
Launch the five-view offline dashboard:
```bash
streamlit run app/streamlit_app.py
```

### 5.4 Execute Automated Test Suite
Run the 49 unit and integration tests:
```bash
pytest -v
```

---

## 6. Pre-Registration Gates & Protocol Amendments

The complete audit status of pre-registered gates is summarized below (`data/processed/evidence_status_gates.csv`):

| Gate ID | Target / Rule | Result | Operational Status |
|---|---|---|---|
| **Gate G1** | Reference Ingestion & Sanitization | 100% matched across 5,400 cell-days, 0 nodata leakage | **PASSED** |
| **Gate G2** | Forecast Archive Completeness | 99.1% (541 / 546 valid days in S1, 12 dropped missing dates) | **PASSED** |
| **Ordinary Rain Gate** | General Bias Assessment | $\ge 30$ wet days per stratum (312 v2, 376 v3 sat in S1) | **PASSED** |
| **Heavy Rain Gate** | Heavy Rain Predictive Skill | 8 independent event groups $\ge 50\text{ mm}$ ($< 20$ gate threshold) | **FAILED (Refusal Triggered: Descriptive Only)** |
| **Calibration Gate** | Statistical Post-Processing | Climatology worse ($+1.2$ to $+2.0\text{ mm}$); Ridge/Bias inconclusive | **FAILED (Raw Forecast Retained)** |
| **Amendment A1** | Disqualification of CHIRPS v3 `rnl` | Excluded because ERA5 is an ECMWF product (self-evaluation bias) | **ENFORCED** |
| **Amendment A2** | HydroBASINS Reverse Traversal | Upstream traversal of `NEXT_DOWN`; $-0.004\%$ area deviation | **ENFORCED** |
| **Amendment A3** | Ditwah Corridor AOI Isolation | Restricted to 236.6 km² AOI 02; DTM extrapolation segregated | **ENFORCED** |
| **Amendment A4** | Earth Engine Export Audit | 36 cell-days cross-checked against raw GeoTIFFs following API rate limit | **ENFORCED** |
| **Amendment A5** | Small-Cluster Suppression Guard | Suppresses bootstrap CI estimation when independent clusters $< 5$ | **ENFORCED** |

---

## 7. Open Licences & Data Provenance

All datasets used in RESILIENCE SL comply with scientific open-access licensing terms:
- **ECMWF IFS Forecasts:** European Centre for Medium-Range Weather Forecasts (ECMWF) / Open-Meteo API (CC BY 4.0).
- **CHIRPS v2.0 & v3.0 sat:** Climate Hazards Center, UC Santa Barbara (Public Domain / Open Access).
- **HydroBASINS v1c Asia:** WWF / HydroSHEDS / USGS (Free Non-Commercial Scientific License).
- **May 2010 Flood Envelope:** World Bank / European Space Agency (World Bank Open Data / CC BY 4.0).
- **ESA WorldCover 2021:** European Space Agency (CC BY 4.0).
- **ESA CCI Land Cover:** ESA Climate Change Initiative Open Access.
- **Copernicus EMSR851:** Copernicus Emergency Management Service / European Union (Open Access).

---

## 8. AI Assistance & Methodology Disclosure

In accordance with ModelX 2.0 hackathon competition guidelines:
- Large Language Models (LLMs) were utilized for code scaffolding, typing annotations, and markdown documentation generation.
- All numerical values, physical algorithms (HydroBASINS reverse traversal, time-window integration, cluster bootstrap), pre-registered gates, and statistical results are derived directly from the verified Phase 1 V3 research protocol and audited through 49 automated unit and integration tests.

---

## 9. Git Branching Model & Contribution Policy

> **IMPORTANT GIT RULE:**  
> Direct pushes to `main` are strictly prohibited. All Phase 2 workbench development is tracked on the feature branch:  
> `feature/phase2-workbench`  
> Teammates review code and verify test execution before opening a Pull Request into `main`.
