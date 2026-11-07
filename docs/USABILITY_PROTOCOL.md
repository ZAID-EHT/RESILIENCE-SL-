# RESILIENCE SL: Practitioner Usability & Verification Protocol

**Protocol Target:** Divisional Secretariats (Kolonnawa, Kaduwela, Hanwella, Biyagama, Ruwanwella), Disaster Management Centre (DMC) Officers, and Independent Technical Evaluators.  
**Session Length:** Approximately 15–20 minutes  
**Environment:** Completely Offline Local Research Workbench (`app/streamlit_app.py`)  

---

## 1. Practitioner Evaluation Workflow

The RESILIENCE SL workbench provides a disciplined, two-panel decision triage framework designed to prevent misinterpretation of weather models and satellite flood maps:
1. **Atmospheric Panel (Panel A):** Query forecast error characteristics at specific lead times before acting on numerical rainfall bulletins.
2. **Exposure Panel (Panel B):** Evaluate historical flood envelopes clipped strictly to hydrological boundaries before allocating relief and zoning resources.
3. **Disaster Case Panel (Ditwah):** Review historical multi-lead model performance during extreme cyclonic stress tests.

---

## 2. Interactive 5-Task Practitioner Verification Checklist

Below are the five core tasks that every practitioner and technical evaluator should step through to verify workbench integrity:

### Task 1: Verify Epistemic Safeguards & Safety Disclaimers
- **Action:** Open View 1 ("Overview, Scientific Boundary & Readiness Protocol").
- **Verification Criterion:**
  - Confirm the permanent warning banner is clearly visible:
    > *"Research prototype. Not an official warning or a live flood-risk map. Areas outside historical mapped footprints are not necessarily safe."*
  - Verify that the four explicit refusal states ("What the System Refuses to Do") are clearly documented.

### Task 2: Evaluate 48–72h Forecast Reliability for Coastal Lowlands (Cell C1)
- **Action:** Navigate to View 2 ("Panel A: Rainfall-Forecast Reliability"). Select Stratum `S1 (Operational Cycle 49r1)`, Lead `Lead 2 (48-72h)`, and view the comparison against both satellite references.
- **Verification Criterion:**
  - Verify Bias is reported within $[-0.47\text{ mm}]$ (v2.0) and $[-1.32\text{ mm}]$ (v3.0 sat).
  - Verify MAE is reported as $8.80\text{ mm}$ (v2.0) and $8.94\text{ mm}$ (v3.0 sat).
  - Confirm the Status is correctly identified as **Reference-Dependent / Inconclusive** because the 95% bootstrap intervals cross zero.

### Task 3: Trigger the Heavy-Rain Epistemic Refusal State
- **Action:** On View 2, switch the rainfall subset from "All Days" to "Heavy Rain >= 50 mm" or "Heavy Rain >= 100 mm".
- **Verification Criterion:**
  - Verify that the dashboard immediately displays the prominent red refusal alert:
    > *"INSUFFICIENT EVIDENCE: Only 8 independent event groups contain a day >= 50 mm (< 20 pre-registered gate). Parametric skill metrics suppressed. Descriptive cases only."*
  - Confirm that the descriptive table of top 15 heavy-rain days is presented with raw values and no uncalibrated probability scores.

### Task 4: Contrast Catchment-Clipped vs Unclipped Historical Flood Exposure
- **Action:** Navigate to View 3 ("Panel B: Kelani Catchment Historical Flood Exposure"). Toggle the view between "Unclipped Full Map Frame" and "Clipped to Verified Kelani Catchment".
- **Verification Criterion:**
  - Confirm unclipped floodwater is reported as $432.24\text{ km}^2$, while catchment-clipped floodwater is exactly $100.40\text{ km}^2$ ($23.2\%$).
  - Confirm that $284.24\text{ km}^2$ ($65.8\%$) is correctly attributed to neighbouring river basins.
  - Review the Product Sensitivity Range for built-up land ($5.9\text{ km}^2$ WorldCover vs $21.7\text{ km}^2$ CCI) and check the urban pixel aggregation diagnostic ($45\%$ built-up).

### Task 5: Review Cyclone Ditwah Multi-Lead Forecast Shift
- **Action:** Navigate to View 4 ("Cyclone Ditwah Case View"). Select 2025-11-27 at Cell C1.
- **Verification Criterion:**
  - Observe the forecast progression across leads: Lead 3 ($202.6\text{ mm}$) $\rightarrow$ Lead 2 ($117.2\text{ mm}$) $\rightarrow$ Lead 1 ($65.9\text{ mm}$).
  - Note the severe reference discordance on Nov 27: CHIRPS v2.0 ($65.4\text{ mm}$) vs CHIRPS v3.0 `sat` ($100.6\text{ mm}$).
  - Confirm that satellite-observed floodwater ($33.77\text{ km}^2$ on Nov 30) is strictly segregated from model-based DTM extrapolation ($67.6\text{ km}^2$).

---

## 3. Evaluation Feedback Logging

Evaluators and officers record task completion timestamps, subjective clarity ratings (1 to 5), and operational observations. All feedback is logged locally to preserve complete privacy and operational independence.
