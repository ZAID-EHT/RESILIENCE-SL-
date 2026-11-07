# RESILIENCE SL: Technical Report & Scientific Verification

**Title:** Evidence-Based Rainfall-Forecast Reliability and Historical Flood Exposure for the Kelani Catchment, Sri Lanka  
**Authors:** RESILIENCE SL Core Research Group  
**Competition:** ModelX 2.0 Hackathon (`https://modelx2.pages.dev/`)  
**Target Basin:** Kelani River Catchment (Western & Sabaragamuwa Provinces, Sri Lanka)  

---

## 1. Executive Summary & Scientific Purpose

The Kelani River Basin houses over 25% of Sri Lanka's population and generates approximately one-third of national GDP through the Colombo commercial hub. Despite recurrent catastrophic inundations (e.g. May 2010, May 2016, and November 2025 Cyclone Ditwah), disaster managers routinely face an evidence gap: numerical weather predictions from global centres such as ECMWF are consumed without localized lead-specific validation, while historical flood maps are frequently misapplied without hydrologic boundary clipping or resolution sensitivity disclosures.

**RESILIENCE SL** delivers an open, offline-capable scientific workbench that rigorously separates:
1. **Panel A (Atmospheric Reliability):** Systematic validation of ECMWF Integrated Forecasting System (IFS HRES) 24–96 h precipitation forecasts against two co-primary satellite precipitation products (CHIRPS v2.0 and CHIRPS v3.0 `sat`).
2. **Panel B (Historical Exposure):** Geodesically-clipped floodwater exposure analysis using the May 2010 World Bank/ESA flood map over modern and historic land-cover surfaces (ESA WorldCover 10 m and ESA CCI 300 m).

Crucially, RESILIENCE SL introduces a **Two-Panel Evidence Triage Architecture** that deliberately refuses to construct synthetic, uncalibrated "flood risk indices". Where observational events are insufficient for statistical power (e.g. fewer than 20 independent heavy rainfall events), the system enters an auditable **Refusal State**, displaying empirical case registries with explicit epistemic boundary alerts.

---

## 2. Catchment Delineation & Geospatial Rectification

### 2.1 HydroBASINS Reverse Graph Traversal
Hydrological boundary delineation for the Kelani Catchment was executed using HydroBASINS v1c Asia Level 8 and Level 10 datasets.
- **Outlet Cell:** Level 8 `HYBAS_ID = 4080049050`, with an upstream drainage area (`UP_AREA`) of $2,325.3\text{ km}^2$ and a geodesic area of $2,315.4\text{ km}^2$.
- **Reverse Traversal Algorithm:** Starting from the outlet polygon, an upstream directed graph search traversed the `NEXT_DOWN` topological attribute across Level 10 sub-basins. Exactly 15 contiguous sub-catchment polygons were identified.
- **Topological Integrity & Validation:**
  - $\sum \text{SUB\_AREA} = 2,325.2\text{ km}^2$, demonstrating an absolute area deviation of $-0.004\%$ compared to the official `UP_AREA` ($2,325.3\text{ km}^2$), comfortably within the pre-registered $1\%$ tolerance.
  - Exactly 0 virtual endorheic sink connections (`ENDO == 2`) were detected.
  - The derived catchment polygon encloses $98.5\%$ of the official Copernicus hydrographic river network for Kelani Ganga.
  - Overlap with administrative Colombo District equals $454.0\text{ km}^2$.
- **Coastal Unit Note:** The physical river-mouth estuary terminates in a separate $310.0\text{ km}^2$ adjacent coastal drainage unit, which accounts for $47.60\text{ km}^2$ of the 2010 mapped flood footprint.

### 2.2 Pilot Forecast Evaluation Grid Cells
Evaluation was anchored on three native 9 km ECMWF IFS HRES grid cell centres:
- **C1 (Coastal / Colombo Mouth):** $6.924429^\circ\text{N}$, $79.90725^\circ\text{E}$ (Located within the 2010 flood mapping frame).
- **C2 (Mid-Basin / Hanwella Key Gauging Corridor):** $6.924429^\circ\text{N}$, $80.05902^\circ\text{E}$ (Located within the 2010 flood mapping frame).
- **C3 (Upland / Kitulgala Headwater Catchment):** $6.9947276^\circ\text{N}$, $80.35442^\circ\text{E}$ (Positioned east of the 2010 flood map eastern boundary at $80.156^\circ\text{E}$).

---

## 3. Atmospheric Evaluation Methodology (Panel A)

### 3.1 Time Window Integration & Cycle Strata
- **Evaluation Period:** 2024-03-14 to 2026-08-30 (900 calendar dates; 2,700 scheduled cell-run requests).
- **Archive Completeness:** 2,688 requests completed successfully ($99.1\%$ in Stratum S1). Exactly 12 runs failed retrieval (dated 2025-08-05, 2025-08-06, 2025-08-08, 2025-08-09 across the 3 cells) and were explicitly dropped rather than zero-filled.
- **Preceding-Hour Integration:** Daily UTC precipitation for calendar date $D$ was integrated using the standard hydrological convention:
  $$\text{Rain}_{D} = \sum_{h=1}^{24} \text{HourlyPcp}(D\text{ 01:00} + (h-1)\text{ h})$$
  Timestamp $D\text{ 00:00}$ (Index 0) represents the initialization instant and contains null precipitation in Open-Meteo single runs. Any UTC window missing even a single hourly record was rejected.
- **Operational Cycle Strata:**
  - **Stratum S0 (Retrospective Hindcast):** 2024-03-14 00:00Z to 2024-11-12 00:00Z (Cycle 49r1 hindcasts).
  - **Stratum S1 (Operational Cycle 49r1):** 2024-11-12 06:00Z to 2026-05-12 00:00Z (First 00 UTC run: 2024-11-13).
  - **Stratum S2 (Operational Cycle 50r1):** 2026-05-12 06:00Z onward (First 00 UTC run: 2026-05-13).

### 3.2 Dual Co-Primary References & The Claim Rule
To avoid observational confirmation bias, two independent satellite precipitation references were evaluated side-by-side:
1. **CHIRPS v2.0:** Daily $0.05^\circ$ infrared-station quasi-global gauge-calibrated product.
2. **CHIRPS v3.0 sat:** Next-generation daily product that uses GPM IMERG Late V07 to disaggregate pentadal precipitation. (Note: CHIRPS v3.0 `rnl` disaggregates using ERA5 reanalysis; because ERA5 is an ECMWF model product, it was disqualified by Amendment A1 to eliminate model incest).

**Pre-Registered Two-Reference Claim Rule:**
A forecast bias, error trend, or post-processing calibration is classified as **"Supported"** if and only if:
1. Both reference comparisons yield identical directional sign; AND
2. Both 95% cluster-bootstrap confidence intervals strictly exclude zero.
Otherwise, the finding is classified as **"Reference-Dependent"** or **"Inconclusive"**.

### 3.3 Event Grouping & Bootstrap Uncertainty
- **Clustered Events:** Daily observations are serially correlated during monsoon surges. Consecutive wet days ($\ge 1.0\text{ mm}$ at any pilot cell) separated by $\le 3$ dry days are aggregated into independent event clusters.
- **Cluster Bootstrap:** 95% confidence intervals are calculated using 2,000 cluster-resamples (fixed seed `42`).
- **Amendment A5 (Small Cluster Guard):** If a stratum or sub-group contains fewer than 5 independent event clusters, bootstrap resampling is suppressed, and intervals are reported as **"not estimable (<5 clusters)"**.

---

## 4. Key Verification Findings (Panel A)

### 4.1 Stratum-Wide Forecast Metrics
Across the 541 operational S1 days:
- **Lead 1 (24–48 h):**
  - vs CHIRPS v2.0: Bias = $-0.24\text{ mm}$ (95% CI: $-2.27$ to $+2.76$), MAE = $8.65\text{ mm}$ ($6.89$ to $10.05$), RMSE = $13.45\text{ mm}$.
  - vs CHIRPS v3.0 sat: Bias = $-1.09\text{ mm}$ (95% CI: $-3.33$ to $+1.77$), MAE = $8.75\text{ mm}$ ($5.70$ to $10.62$), RMSE = $15.32\text{ mm}$.
- **Lead 2 (48–72 h):**
  - vs CHIRPS v2.0: Bias = $-0.47\text{ mm}$ (95% CI: $-2.43$ to $+2.58$), MAE = $8.80\text{ mm}$ ($6.96$ to $10.18$), RMSE = $13.15\text{ mm}$.
  - vs CHIRPS v3.0 sat: Bias = $-1.32\text{ mm}$ (95% CI: $-3.87$ to $+1.65$), MAE = $8.94\text{ mm}$ ($5.78$ to $10.89$), RMSE = $15.19\text{ mm}$.
- **Lead 3 (72–96 h):**
  - vs CHIRPS v2.0: Bias = $-0.64\text{ mm}$ (95% CI: $-2.77$ to $+2.43$), MAE = $9.30\text{ mm}$ ($7.22$ to $10.77$), RMSE = $14.92\text{ mm}$.
  - vs CHIRPS v3.0 sat: Bias = $-1.49\text{ mm}$ (95% CI: $-3.84$ to $+1.27$), MAE = $9.31\text{ mm}$ ($5.74$ to $11.78$), RMSE = $16.42\text{ mm}$.

**Scientific Takeaway:** At the all-days level in S1, both 95% confidence intervals bridge zero. The overall daily bias is statistically indistinguishable from zero, and mean absolute error remains steady at $\sim 8.7–9.3\text{ mm/day}$ across 1- to 3-day lead times.

### 4.2 Seasonal Regimes & Monsoon Over-Forecasting
Stratification by seasonal monsoon cycles reveals distinct regime behavior:
- **Southwest Monsoon (SW):**
  - In retrospective S0: Bias is positive and significant against both references (+8.9 mm vs v2; +6.5 mm vs v3 sat; both CIs exclude 0) $\rightarrow$ **Supported Over-Forecast**.
  - In operational S2: Bias is also positive and significant (+10.5 mm vs v2; +9.7 mm vs v3 sat; both CIs exclude 0) $\rightarrow$ **Supported Over-Forecast**.
  - In operational S1: Bias remains positive (+5.1 mm vs v2; +3.5 mm vs v3 sat), but intervals span zero $\rightarrow$ **Reference-Dependent**.
- **Inter-Monsoon Regimes (IM1 & IM2):** ECMWF consistently under-forecasts localized convective precipitation during transition months (S1 IM1: $-5.5\text{ mm}$ vs v2; $-6.8\text{ mm}$ vs v3 sat), but differences in satellite reference sensitivity keep the formal status as **Reference-Dependent**.

### 4.3 Reference Disagreement & Spatial Elevation Gradient
Direct comparison between CHIRPS v2.0 and v3.0 `sat` reveals significant divergence as elevation increases:
- **C1 Coastal:** Daily correlation $r = 0.73$, 5-day pentad $r = 0.91$. Days $\ge 50\text{ mm}$: v2 = 13, v3 = 18. Mean difference = $-0.27\text{ mm/day}$.
- **C2 Mid-Basin:** Daily correlation $r = 0.70$, 5-day pentad $r = 0.91$. Days $\ge 50\text{ mm}$: v2 = 13, v3 = 26. Mean difference = $+0.31\text{ mm/day}$.
- **C3 Upland:** Daily correlation drops to $r = 0.62$ (5-day $r = 0.83$). Days $\ge 50\text{ mm}$: v2 = 15, v3 = 36 (a $2.4\times$ discrepancy!). Mean difference = $+3.17\text{ mm/day}$.

This proves that satellite rainfall uncertainty expands dramatically in complex upland topography, necessitating cautious interpretation of headwater rainfall totals.

### 4.4 Calibration Failure: Why Raw ECMWF Is Retained
Three statistical calibration schemes were tested using rolling-origin cross-validation (initial 6-month training block, 30-day evaluation blocks, 3-day buffer purges):
1. **Day-of-Year Climatology:** Severely degraded forecast accuracy (v2 $\Delta\text{MAE} = +1.20\text{ mm}$; v3 sat $\Delta\text{MAE} = +2.03\text{ mm}$).
2. **Seasonal Additive Bias Adjustment:** Produced ambiguous, statistically insignificant shifts (v2 $\Delta\text{MAE} = -0.35\text{ mm}$; v3 sat $\Delta\text{MAE} = +0.43\text{ mm}$).
3. **Non-Negative Ridge Regression:** Failed to achieve consistent reduction across references (v2 $\Delta\text{MAE} = -0.92\text{ mm}$; v3 sat $\Delta\text{MAE} = +0.05\text{ mm}$, intervals crossing zero).

Furthermore, the pre-registered event gate required $\ge 20$ independent event groups in both training and test folds. S1 contained only 8 training event groups and 18 test groups against v2. Consequently, all calibration models were rejected, and the **raw ECMWF forecast was retained**.

---

## 5. Historical Flood Exposure Verification (Panel B)

### 5.1 Catchment Clipping vs Unclipped Map Frame
The historical maximum flood layer from the May 2010 disaster (World Bank / ESA HFM) comprises 22,813 total polygons (12,734 floodwater polygons, with 298 invalid self-intersections repaired with 0.00% area alteration).
- **Unclipped Raw Map Frame:** Encompasses $432.24\text{ km}^2$ of inundated surface.
- **Inside Verified Kelani Catchment:** Exactly $100.40\text{ km}^2$ ($23.2\%$).
- **Adjacent Coastal Units (including river mouth):** $47.60\text{ km}^2$ ($11.0\%$).
- **Outside River Basin Units (Kalu, Attanagalu, etc.):** $284.24\text{ km}^2$ ($65.8\%$).

**Crucial Finding:** Uncritical use of the raw 2010 shapefile exaggerates Kelani flood inundation by more than $400\%$. The 2010 satellite acquisition window covered only the lower $30\%$ of the Kelani catchment.

### 5.2 Product Sensitivity & The Urban Aggregation Fallacy
Overlaying the $100.40\text{ km}^2$ catchment-clipped flood footprint onto high-resolution and moderate-resolution land-cover maps demonstrates that observed exposure ranges reflect **product sensitivity**, not real land-use transitions:
- **Built-Up / Urban Inundation:**
  - ESA WorldCover 2021 (10 m): $5.9\text{ km}^2$
  - ESA CCI 2010 (300 m): $21.7\text{ km}^2$
  - *Diagnostic:* Aggregating 10 m WorldCover pixels into 300 m CCI grid cells proves that CCI "urban" pixels contain on average only $45\%$ actual built-up structures. The remaining $55\%$ consists of gardens, roads, and open water, producing a $3.7\times$ overstatement in 300 m data.
- **Cropland Inundation:**
  - ESA WorldCover 2021: $21.9\text{ km}^2$
  - ESA CCI 2010 (strict agricultural classes 10, 11, 20): $6.3\text{ km}^2$
  - ESA CCI 2010 (including mosaic agricultural class 30): $53.5\text{ km}^2$
- **The Tree Cover Phenomenon:**
  - In both WorldCover ($61.0\text{ km}^2$, $61\%$) and Copernicus EMS 2025 baseline mapping ($69\%$), dense tree canopy dominates the mapped flood footprint. In the wet-zone floodplains of Sri Lanka, extensive rural home-gardens (*gewathu*), rubber groves, and coconut plantations maintain continuous overstory canopy above inundated understories.

---

## 6. Cyclone Ditwah Corridor Validation (November 2025)

The November 2025 Cyclone Ditwah event provided an end-to-end real-world stress test:
1. **ECMWF Lead Shifts at Cell C1:**
   - On 2025-11-27, Lead 3 projected an extreme deluging total of $202.6\text{ mm}$.
   - By Lead 2, the forecast adjusted to $117.2\text{ mm}$.
   - By Lead 1, the forecast settled at $65.9\text{ mm}$.
   - Actual observations on Nov 27 revealed severe satellite disagreement: CHIRPS v2 recorded $65.4\text{ mm}$ (matching Lead 1), whereas CHIRPS v3 sat recorded $100.6\text{ mm}$.
2. **Copernicus EMSR851 Satellite Extent (AOI 02 Corridor: 236.6 km²):**
   - **2025-11-30 (PlanetScope EO):** Observed floodwater $= 33.77\text{ km}^2$ ($66\%$ tree cover, $13\%$ cropland, $10\%$ built-up). DTM model-based extrapolation $= 67.6\text{ km}^2$ (reported separately, never added). $52\%$ of the historical 2010 footprint inside the corridor was re-inundated.
   - **2025-12-03 (Legion EO):** Recession observed at $6.88\text{ km}^2$ floodwater $+ 1.23\text{ km}^2$ trace ($30.1\%$ of AOI obstructed or unanalysed).

---

## 7. Conclusions & Deployment Governance

RESILIENCE SL demonstrates that responsible hydrometeorological tools must lead with epistemic humility. By decoupling atmospheric forecast verification from flood exposure, disclosing satellite reference discordance, and refusing to invent uncalibrated risk metrics, this research workbench establishes a transparent, auditable benchmark for early action in Sri Lanka.
