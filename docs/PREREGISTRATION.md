# RESILIENCE SL: Pre-Registration Plan & Gates (V3 Frozen Protocol)

**Project Title:** Evidence-Based Rainfall-Forecast Reliability and Historical Flood Exposure for the Kelani Catchment, Sri Lanka  
**Competition:** ModelX 2.0 Hackathon (`https://modelx2.pages.dev/`)  
**Target Basin:** Kelani Ganga Catchment (HydroBASINS Level 8 HYBAS_ID = 4080049050 / Level 10 reverse traversal)  
**Protocol Version:** V3.2 Frozen Protocol  
**Repository Branch:** `feature/phase2-workbench`  

---

## 1. Scientific Objectives & Boundary Conditions

RESILIENCE SL is an offline-capable, evidence-based research workbench designed to provide objective, falsifiable evaluation of Numerical Weather Prediction (ECMWF IFS HRES) rainfall forecasts and historical flood exposure for the Kelani River Basin.

### Core Non-Negotiables
1. **No Invented Risk Scores:** The system strictly separates rainfall forecast evaluation (Panel A) from historical land-cover flood exposure (Panel B). It never multiplies rainfall uncertainty with satellite exposure to produce synthetic "flood risk indexes".
2. **Refusal Over Overconfidence:** The system implements explicit refusal gates. If statistical power is insufficient (e.g. fewer than 20 independent heavy events), the system refuses to output inferential claims or percentage confidence scores, displaying descriptive event tables with explicit warning banners.
3. **Two-Reference Claim Rule:** No bias or error direction is claimed as established unless supported by both independent satellite rainfall references (CHIRPS v2.0 and CHIRPS v3.0 `sat`). If the two references disagree or their 95% bootstrap intervals cross zero, the finding is labeled **"reference-dependent"** or **"inconclusive"**.

---

## 2. Study Sites & Pilot Grid Coordinates

All forecast evaluations are anchored on three predeclared ECMWF IFS HRES (9 km native grid centres):
- **C1 (Coastal / Colombo River Mouth):** Lat `6.924429°N`, Lon `79.90725°E` (Elevation: Coastal lowlands)
- **C2 (Mid-Basin / Hanwella Hydrological Gauge):** Lat `6.924429°N`, Lon `80.05902°E` (Elevation: Mid-basin)
- **C3 (Upland / Kitulgala Headwaters):** Lat `6.9947276°N`, Lon `80.35442°E` (Elevation: Upland headwaters, east of 2010 flood map boundary `80.156°E`)

---

## 3. Forecast Time Windows & Stratification

### A. Window Definition
- **Evaluation Window:** 2024-03-14 to 2026-08-30 00:00 UTC initialization runs.
- **Request Accounting:** Exactly 2,700 scheduled cell-run requests (900 dates × 3 pilot cells). 2,688 succeeded; 12 requests returned "run not available" (2025-08-05, 2025-08-06, 2025-08-08, 2025-08-09 across the 3 cells). These missing runs are **dropped entirely** and never imputed with zeros.
- **Hourly Integration Convention:** Daily precipitation for valid UTC day $D$ is the sum of the preceding 24 hours stamped $D\text{ 01:00}$ through $(D+1)\text{ 00:00}$ UTC. Index 0 ($D\text{ 00:00}$) is null in Open-Meteo single runs. If any of the 24 hourly timestamps is missing, the entire day is dropped.
- **Forecast Leads:**
  - Lead 1: 24–48 hours from 00:00 UTC initialization
  - Lead 2: 48–72 hours from 00:00 UTC initialization
  - Lead 3: 72–96 hours from 00:00 UTC initialization

### B. Cycle Strata Definition
Operational ECMWF model cycle transitions take effect at 06:00 UTC on release dates:
- **Stratum S0 (Retrospective Hindcast):** 2024-03-14T00:00Z through 2024-11-12T00:00Z (Cycle 49r1 hindcasts).
- **Stratum S1 (Operational Cycle 49r1):** 2024-11-12T06:00Z (first 00 UTC run: 2024-11-13T00:00Z) through 2026-05-12T00:00Z (Cycle 49r1 operational era).
- **Stratum S2 (Operational Cycle 50r1):** 2026-05-12T06:00Z (first 00 UTC run: 2026-05-13T00:00Z) through 2026-08-30T00:00Z (Cycle 50r1 operational era).

---

## 4. Evidence Status Gates & Formal Amendments

| Gate ID | Target / Rule | Gate Criterion | Phase 1 V3 Status |
|---|---|---|---|
| **Gate G1** | Reference Data Ingestion | Complete CHIRPS v2.0 & v3.0 read with -9999 masked; 36 cell-days cross-checked | **PASSED** |
| **Gate G2** | Forecast Archive Completeness | Operational stratum S1 valid days >= 95% (achieved 541 / 546 = 99.1%) | **PASSED** |
| **Ordinary Rain Gate** | General Bias Inference | Requires >= 30 wet days (>= 1.0 mm at any pilot cell) | **PASSED** (S1 has 312-376 wet days) |
| **Heavy Rain Gate** | Extreme Rain Validation | Requires >= 20 independent event groups (separated by > 3 dry days) with rainfall >= 50 mm or >= 100 mm | **FAILED (Refusal Triggered)**: Only 8 independent groups found in S1. System switches to descriptive event tables. |
| **Calibration Gate** | Statistical Post-Processing | Post-processed forecast must reduce MAE on held-out blocks with 95% CI strictly below zero | **FAILED (Raw Retained)**: Climatology, seasonal bias, and ridge all failed to outperform raw ECMWF forecast. |

### Formal Protocol Amendments
- **Amendment A1 (Reference Separation):** Explicit separation of CHIRPS v3.0 `sat` (using IMERG Late V07) from CHIRPS v3.0 `rnl` (which uses ERA5 reanalysis). `rnl` is disqualified to avoid ECMWF self-evaluation bias.
- **Amendment A2 (HydroBASINS Reverse Traversal):** Hydrological catchment delineated strictly via reverse traversal of HydroBASINS `NEXT_DOWN` to prevent downstream leakage.
- **Amendment A3 (Corridor Isolation):** Cyclone Ditwah satellite imagery (EMSR851) restricted to the 236.6 km² Kelani Ganga corridor AOI 02.
- **Amendment A4 (Earth Engine Export Audit):** Manual Earth Engine batch export logged and verified after direct API rate limiting; 36 cell-days verified against raw GeoTIFFs.
- **Amendment A5 (Small-Cluster Guard):** When the number of independent event clusters is fewer than 5, cluster-bootstrap intervals are suppressed and marked **"not estimable (<5 clusters)"** to prevent spuriously narrow or degenerate confidence bounds.

---

## 5. Statistical Estimation & Uncertainty Rules

- **Event Grouping:** Independent weather events are defined by grouping consecutive wet days ($\ge 1.0\text{ mm}$ at any pilot cell) separated by $\le 3$ dry days. Robustness is checked at 2-day and 5-day dry gaps.
- **Uncertainty Bounds:** 95% Confidence Intervals are calculated via 2,000 cluster-bootstrap replications grouped by meteorological event cluster.
- **Deterministic Seed:** All bootstrap procedures employ a frozen random seed (`seed=42`) to guarantee bit-for-bit reproducibility.
