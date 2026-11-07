# RESILIENCE SL: Executive & Practitioner Summary (Two-Page Brief)

**Target Audience:** Disaster Management Centre (DMC), Department of Meteorology, Irrigation Department, and District/Divisional Secretariats (Colombo & Gampaha)  
**Project:** RESILIENCE SL — ModelX 2.0 Open Research Workbench  

---

## 1. The Dilemma: Forecast Uncertainty Meets Spatial Misinterpretation

The Kelani River Catchment ($2,325.3\text{ km}^2$) is Sri Lanka's highest-risk flood basin. While emergency planners increasingly inspect global numerical forecasts (such as ECMWF IFS) and satellite flood maps, existing workflows suffer from three critical blind spots:
1. **Uncalibrated Global Forecasts:** ECMWF rainfall predictions are often treated as exact quantities without understanding lead-dependent error bars or seasonal monsoon bias.
2. **Boundary Inflation in Flood Maps:** Historical flood footprints (such as the May 2010 World Bank/ESA map) are frequently cited without catchment clipping, mistakenly attributing inundation from adjacent basins to the Kelani River.
3. **Synthetic "Risk Scores":** Commercial disaster dashboards routinely merge weather forecasts with land-cover datasets using arbitrary mathematical formulas, manufacturing false certainty that misleads field commanders.

---

## 2. Key Findings: What the Empirical Data Actually Proves

### Panel A: Rainfall Forecast Reliability (ECMWF IFS vs CHIRPS Satellite Data)
- **All-Days Performance (Cycle 49r1, Lead 1 to 3 Days):** Average bias across the 541 operational days is negligible ($-0.24$ to $-1.49\text{ mm/day}$), with Mean Absolute Error remaining steady at approximately $8.7\text{ to }9.3\text{ mm/day}$.
- **Southwest Monsoon Over-Forecasting:** In monsoon surge regimes (e.g. S0 and S2), ECMWF forecasts consistently overestimate rainfall by $+6.5\text{ to }+10.5\text{ mm/day}$ against both satellite references.
- **Inter-Monsoon Convective Deficit:** During inter-monsoon periods (IM1/IM2), localized convective cloudbursts are frequently missed or under-forecast by $5\text{ to }7\text{ mm/day}$.
- **Satellite Truth Does Not Exist:** In the upland headwaters (Kitulgala), CHIRPS v2.0 and CHIRPS v3.0 `sat` disagree on heavy rain ($\ge 50\text{ mm}$) by a factor of $2.4\times$ ($15\text{ vs }36\text{ days}$).
- **Post-Processing Calibration Null:** Statistical corrections (climatology, seasonal bias, ridge regression) failed to beat the raw ECMWF forecast on held-out test blocks. **The raw forecast is retained.**

### Panel B: Historical Flood Exposure & Resolution Effects
- **Catchment Clipping Reduces Mapped Area by 77%:** Of the $432.24\text{ km}^2$ flooded in the unclipped May 2010 map frame, **only $100.40\text{ km}^2$ ($23.2\%$) occurred inside the Kelani catchment**. The remaining area belongs to adjacent coastal ($47.60\text{ km}^2$) and neighbouring river basins ($284.24\text{ km}^2$).
- **The "Built-Up" Discrepancy (5.9 vs 21.7 km²):** Moderate-resolution ESA CCI (300 m) reports $21.7\text{ km}^2$ of urban inundation, whereas high-resolution ESA WorldCover (10 m) reports only $5.9\text{ km}^2$. High-resolution cross-tabulation proves that 300 m "urban" pixels in Sri Lanka contain on average only $45\%$ actual buildings, the rest being gardens and vegetation.
- **Canopy Obscuration (61% Tree Cover):** Over $61\text{ km}^2$ of the 2010 floodwater is classified as tree cover due to Sri Lanka's pervasive home-garden (*gewathu*) agroforestry landscape.

---

## 3. Real-World Case Study: Cyclone Ditwah (November 2025)

During Cyclone Ditwah, the system captured a critical forecast shift at the Colombo mouth (Cell C1):
- **Forecast Dynamic:** A 3-day lead forecast of $202.6\text{ mm}$ on Nov 27 dropped to $117.2\text{ mm}$ at Lead 2 and finalized at $65.9\text{ mm}$ at Lead 1.
- **Reference Discordance:** Realized rainfall on Nov 27 was $65.4\text{ mm}$ in CHIRPS v2.0 but $100.6\text{ mm}$ in CHIRPS v3.0 `sat` (a $35.2\text{ mm}$ spread).
- **Corridor Inundation (EMSR851):** Satellite sensors observed $33.77\text{ km}^2$ of floodwater on Nov 30 (PlanetScope) and $6.88\text{ km}^2$ on Dec 3 (Legion), while digital terrain models extrapolated $67.6\text{ km}^2$. RESILIENCE SL strictly segregates satellite observations from computer extrapolations.

---

## 4. What the System Refuses to Do (Epistemic Safeguards)

To protect lives and maintain scientific integrity, RESILIENCE SL enforces four hard computational refusal gates:
1. **Refuses Single Risk Scores:** The dashboard never computes a composite "flood risk index". Atmospheric uncertainty and historical exposure are presented as separate panels.
2. **Refuses Heavy-Rain Statistical Claims:** Because the operational record contains only 8 independent heavy rainfall events ($\ge 50\text{ mm}$), the system explicitly refuses to calculate parametric skill metrics, presenting descriptive event logs instead.
3. **Refuses Extrapolation As Ground Truth:** Satellite-observed inundation is strictly kept separate from hydro-model extrapolations.
4. **Refuses Single-Reference Confidence:** Forecast bias is marked "Supported" only when CHIRPS v2.0 and CHIRPS v3.0 agree in sign and their bootstrap intervals exclude zero.

---

## 5. Practical Guidance for District & Divisional Officers

1. **At 72-Hour Lead Time:** Monitor ECMWF trends, but expect potential $100+\text{ mm}$ shifts as the model approaches Lead 1. In the Southwest Monsoon, account for systematic over-forecasting.
2. **In Inter-Monsoon Seasons:** Do not rely on numerical models for localized convective peaks; supplement with local radar and gauge networks.
3. **When Reviewing Hazard Maps:** Verify that map extents are clipped to the hydrological watershed boundary ($2,325.2\text{ km}^2$), not arbitrary rectangular bounding boxes.
4. **When Assessing Land Loss:** Use high-resolution (10 m) land cover to evaluate residential building exposure rather than coarse (300 m) global layers.
