# Fleet Fuel Intelligence Dashboard

**MSc Dissertation: Predictive Modelling for Fuel Efficiency and Fleet Optimisation in Public Transport**
Anette Kerubo Joseph | 151384 | Strathmore University — MSc Data Science & Analytics
CRISP-DM Methodology · Dataset: May 2025 – December 2026 · All identifiers anonymised

---

## Project Overview

This project applies machine learning to a real-world public transport fleet dataset (14,526 records across 178 anonymised vehicles) to predict fuel efficiency, detect anomalies, benchmark vehicles and routes, and quantify recoverable fuel cost savings. The full analysis is delivered through three Jupyter notebooks and an interactive Streamlit dashboard.

**Key Outcome:** The Gradient Boosting model achieved R² = 0.9904 on unseen test data, and the deployment analysis estimates **KES 8.03M in annual recoverable savings** if underperforming vehicles reach their within-type Q3 efficiency target.

---

## Rubric Compliance

### 1 · Data Collection and Preprocessing — 10 marks

#### 1.1 Data Selection & Handling of Missing Values and Outliers (1 mark)
**Addressed in:** `NB1_EDA_Descriptive_Analysis.ipynb` — Section 1: Data Loading & Quality Assessment

- Dataset sourced from a live public transport fleet management system (May 2025 – Dec 2026), covering 14,526 trip records across Sheet1 (fuel transactions) and Sheet2 (odometer/EFC benchmarks).
- Missing value audit performed across all 24 columns. Columns with >40% missingness were excluded. For critical numeric fields (Liters, Mileage, Fuel Amount), rows with nulls were dropped to preserve analytical integrity.
- Outlier detection used IQR-based flagging at the data selection stage, with separate Isolation Forest anomaly detection at the modelling stage (NB3), giving a two-stage approach to outlier treatment.
- The dataset was confirmed to start from **May 2025**, with 688 erroneous earlier records removed during cleaning to produce the `Fleet_Fuel_Cleaned_Dataset_v4.xlsx` used throughout.

#### 1.2 Data Cleaning (3 marks)
**Addressed in:** `NB1_EDA_Descriptive_Analysis.ipynb` — Section 2: Cleaning Pipeline

- **PII anonymisation:** 228 unique vehicle registration plates mapped to `VEH-001…VEH-228`; 1,465 driver names mapped to `DRV-001…DRV-1465` (consistent across both sheets and the Car-Driver lookup). A separate lookup file is maintained outside the repository.
- **Duplicate removal:** Trip-level duplicates identified and removed using `Instance ID` as the unique key.
- **Date standardisation:** All date fields parsed with `pd.to_datetime(errors='coerce')`, with timezone and format inconsistencies resolved; records outside the operational window (May 2025 – Dec 2026) excluded.
- **Type filtering:** Analysis restricted to `Fueling Type == "Full_Tank"` trips (8,489 records) to ensure valid efficiency calculations; partial fills excluded from the efficiency target variable.
- **Consistency checks:** Vehicle type cross-referenced against Car-Driver sheet; mismatched records reconciled. Fuel efficiency values > 20 km/L or < 0.5 km/L flagged and removed.
- **`.ffill().bfill()` replacement:** Used instead of deprecated `fillna(method=...)` for forward/backward fill on sequential records.

#### 1.3 Feature Engineering and Feature Selection (6 marks)
**Addressed in:** `NB2_Feature_Engineering_ML_Models.ipynb` — Sections 1–3

**Engineered Features:**

| Feature | Method | Rationale |
|---------|--------|-----------|
| `Route_Category` | `pd.cut(Mileage, [0,400,800,9999], labels=['Short','Medium','Long'])` | Captures non-linear distance effect on efficiency |
| `Cost_per_Litre` | `Fuel Amount / Liters` | Proxy for fuel grade/supplier variation |
| `Month_sin` / `Month_cos` | Cyclical encoding of calendar month | Preserves seasonal continuity across year boundaries |
| `Type_enc` | `LabelEncoder` on vehicle Type | Encodes fleet segment without ordinal assumption |
| `Route_enc` | `LabelEncoder` on Route | Captures route-specific fixed effects |
| `Route_Cat_enc` | Ordinal map Short→0 / Medium→1 / Long→2 | Ordered numeric for tree-split efficiency |

**Feature Selection — Two-Stage Pipeline:**
1. **Filter stage:** Pearson correlation and mutual information computed against the target (`Fuel Efficiency (km/l)`). Features with |r| < 0.05 and MI < 0.01 discarded.
2. **Wrapper stage (RFE):** `sklearn.feature_selection.RFE` with `LinearRegression` base estimator, `n_features_to_select=6`, applied on the standardised matrix. Selected: `['Liters', 'Mileage', 'Fuel Amount', 'Type_enc', 'Route_Cat_enc', 'Route_enc']`.

This two-stage approach ensures selected features are both statistically relevant (filter) and contribute incrementally in a multivariate context (wrapper).

---

### 2 · Model Selection and Development — 15 marks

#### 2.1 Model Selection — Appropriate Choice (4 marks)
**Addressed in:** `NB2_Feature_Engineering_ML_Models.ipynb` — Section 4

Four models were selected to span the bias-variance spectrum and reflect methods covered in the programme:

| Model | Justification |
|-------|--------------|
| **Ridge Regression** | Linear baseline; tests whether a simple regularised linear model is sufficient |
| **Random Forest** | Ensemble of decision trees; handles non-linearity and feature interactions |
| **Gradient Boosting** | Sequential error-correction ensemble; well-suited to tabular data with mixed feature types |
| **Neural Network (MLP)** | Multi-layer perceptron with early stopping; tests whether deep representations improve on tree ensembles |

The target variable `Fuel Efficiency (km/l)` is continuous, making regression the correct task family. All four models are appropriate for regression on structured tabular data.

#### 2.2 Model Development (4 marks)
**Addressed in:** `NB2_Feature_Engineering_ML_Models.ipynb` — Sections 5–6

- **Train/test split:** 80/20 by date order (6,321 train / 1,581 test) to respect temporal structure.
- **StandardScaler:** Applied to all features; fit on train set only, applied to test set to prevent leakage.
- **Cross-validation:** 5-fold KFold (`shuffle=True, random_state=42`) on the training set for all four models.
- All models trained with `random_state=42` for full reproducibility.

**Model Configurations:**
```python
Ridge(alpha=1.0)
RandomForestRegressor(n_estimators=200, max_depth=12, min_samples_leaf=4, n_jobs=-1, random_state=42)
GradientBoostingRegressor(n_estimators=300, max_depth=5, learning_rate=0.05, subsample=0.8, random_state=42)
MLPRegressor(hidden_layer_sizes=(128,64,32), activation='relu', solver='adam', alpha=0.001,
             max_iter=500, early_stopping=True, random_state=42)
```

#### 2.3 Optimisation Through Techniques Learnt (4 marks)
**Addressed in:** `NB2_Feature_Engineering_ML_Models.ipynb` — Section 7

- **Regularisation:** Ridge uses L2 penalty (`alpha=1.0`); MLP uses L2 weight decay (`alpha=0.001`) and early stopping.
- **Subsampling:** GBM uses `subsample=0.8` (stochastic gradient boosting) to reduce variance.
- **Depth control:** Random Forest uses `max_depth=12` and `min_samples_leaf=4`; GBM uses `max_depth=5`.
- **Slow-learner principle:** GBM uses low learning rate (0.05) with high estimator count (300), following established gradient boosting optimisation practice.
- **Feature scaling:** StandardScaler ensures Ridge and MLP are not dominated by features with large numeric ranges.

#### 2.4 Innovation (3 marks)
**Addressed across all notebooks**

- **Cyclical temporal encoding** (`Month_sin`, `Month_cos`) preserves the circular nature of calendar months — a domain-appropriate engineering choice absent from standard pipelines.
- **Within-type vehicle scoring** normalises efficiency scores within each vehicle type (`Bus`, `Shuttle`, `EPH`, `Admin`) separately, preventing cross-type comparison bias.
- **Two-stage feature selection** (correlation filter → RFE wrapper) combines global statistical relevance with multivariate incremental contribution.
- **Lag-feature GBM forecaster** (NB3) uses previous-month volumes as features for time-series prediction, avoiding stationarity assumptions required by ARIMA.
- **Isolation Forest anomaly detection** with `contamination=0.05` integrated into the deployment pipeline to flag suspicious trips.

---

### 3 · Evaluation Metrics and Results — 10 marks

#### 3.1 Selection of Metrics (5 marks)
**Addressed in:** `NB2_Feature_Engineering_ML_Models.ipynb` — Section 8

| Metric | Why Selected |
|--------|-------------|
| **R²** | Measures proportion of variance explained; scale-independent; standard for regression |
| **MAE** | Average absolute error in km/L units; directly interpretable; robust to outliers |
| **RMSE** | Penalises large errors more heavily; reveals worst-case behaviour |
| **CV R² ± std** | Confirms generalisation beyond the single test split; std measures stability |

Using both MAE and RMSE is intentional: if RMSE >> MAE, it signals specific large errors that average metrics would hide.

#### 3.2 Result Interpretation (5 marks)
**Addressed in:** `NB2_Feature_Engineering_ML_Models.ipynb` — Section 9 and `NB3_Forecasting_Fleet_Optimisation.ipynb` — Section 5

**Model Results:**

| Model | R² | MAE (km/L) | RMSE (km/L) | CV R² | CV Std |
|-------|----|-----------|------------|-------|--------|
| Ridge Regression | 0.8910 | 0.6066 | 0.9630 | 0.8947 | 0.0105 |
| Random Forest | 0.9772 | 0.0979 | 0.4408 | 0.9898 | 0.0043 |
| **Gradient Boosting** | **0.9904** | **0.0885** | **0.2854** | **0.9909** | **0.0036** |
| Neural Network (MLP) | 0.9853 | 0.1194 | 0.3542 | 0.9911 | 0.0016 |

**Interpretation:**
- GBM is selected as the production model. R² = 0.9904 means the model explains 99.04% of the variance in fuel efficiency on unseen test data.
- MAE of 0.0885 km/L means predictions are on average within ~1.5% of the fleet mean (5.842 km/L) — precise enough for trip-level anomaly flagging.
- The narrow CV standard deviation (0.0036) confirms that performance is stable across data subsets, not a result of a favourable split.
- Ridge regression's much higher MAE (0.6066) confirms the relationship is substantially non-linear, justifying ensemble methods.
- The three key efficiency drivers (GBM feature importance): `Liters` > `Mileage` > `Fuel Amount`.
- **Fleet finding:** 89.6% of Full Tank trips exceed EFC benchmarks, representing a net KES 25.26M over-spend. The savings model estimates KES 8.03M/year is recoverable if underperforming vehicles reach the Q3 efficiency target within their vehicle type.

---

### 4 · Implementation and Code Quality — 10 marks

#### 4.1 Code Structure (3 marks)

The project follows a clean three-notebook CRISP-DM structure:

```
NB1_EDA_Descriptive_Analysis.ipynb       ← Data Understanding + Preparation
NB2_Feature_Engineering_ML_Models.ipynb  ← Modelling + Evaluation
NB3_Forecasting_Fleet_Optimisation.ipynb ← Deployment-focused analysis + savings
```

Shared logic (column names, file paths, colour palette) is defined in an initialisation cell at the top of each notebook. The Streamlit dashboard uses `utils.py` so all data loading, model training, and scoring functions are written once and imported by all 7 pages — avoiding repetition and making updates atomic.

#### 4.2 Documentation (3 marks)

- Every function has a docstring describing inputs, outputs, and logic.
- All major code blocks have inline comments explaining the reasoning, not just restating the code.
- Each notebook section begins with a markdown cell stating the CRISP-DM phase, research objective addressed, and expected outputs.
- Figure captions and annotations are embedded directly in notebook outputs.
- This README explicitly maps every rubric criterion to its implementation location.

#### 4.3 Reproducibility — Model Pipelines (4 marks)

Full end-to-end reproducibility achieved through:

- `random_state=42` on all stochastic operations (train/test split, KFold, RandomForest, GradientBoosting, MLP, IsolationForest).
- Pinned `requirements.txt` listing exact package versions.
- `NB3` contains a final cell that calls `build_dashboard.py` to regenerate `fleet_fuel_dashboard.html` from scratch.
- Streamlit app uses `@st.cache_data` and `@st.cache_resource` so models train once and all computations are deterministic on re-run.
- `Fleet_Fuel_Cleaned_Dataset_v4.xlsx` is the single source of truth for all notebooks and the dashboard.

**To reproduce the full pipeline:**
```bash
pip install jupyter pandas numpy matplotlib seaborn scipy scikit-learn openpyxl
# Place Fleet_Fuel_Cleaned_Dataset_v4.xlsx alongside the notebooks
# Run NB1 → NB2 → NB3 in order
# NB3 final cell regenerates fleet_fuel_dashboard.html
```

---

### 5 · Deployment — 10 marks

**Addressed in:** Streamlit Dashboard + `NB3_Forecasting_Fleet_Optimisation.ipynb` — Section 6

The project is deployed as a fully interactive **7-tab Streamlit web dashboard**.

| Tab | Deployment Deliverable |
|-----|----------------------|
| Overview | Live KPI cards, spend distribution, EFC compliance, monthly cost chart |
| Trends | Monthly trends with 3-month MA, MoM change, trip volume, efficiency trend |
| EDA Figures | All 7 NB1 figures with interactive zoom |
| ML Models | 4-model comparison cards, R²/MAE/RMSE charts, feature importance, actual vs predicted scatter |
| Vehicles | Vehicle grade A–D scoring, searchable table, top/bottom 10 |
| Routes | Route optimisation matrix, ranked tables, route search |
| Deployment | Savings KPIs, intervention roadmap cards, RO summary table, NB3 figures |

Additionally, a **self-contained HTML dashboard** (`fleet_fuel_dashboard.html`) produced by `build_dashboard.py` can be opened in any browser without a server — all 18 figures, KPIs, and Chart.js charts compiled into a single 4.3 MB file.

**Deployment stack:** Streamlit Community Cloud (free tier) · Python 3.12 · Plotly · scikit-learn · No external API dependencies.

---

### 6 · Presentation and Communication — 5 marks

- The Streamlit dashboard presents findings through visual KPI cards, interactive Plotly charts, searchable data tables, and plain-English insight boxes — accessible to both a non-technical fleet manager and a technical examiner.
- Every figure includes a caption and annotation (mean lines, threshold lines, spike annotations) so charts are self-explanatory without reading surrounding text.
- The three research objectives are summarised in a structured table on the Deployment page, mapping each RO to its method, result, and CRISP-DM phase.
- Notebook markdown cells follow a consistent structure: *Objective → Method → Result → Interpretation*.
- The HTML dashboard can be presented offline in a browser during the viva or submission demonstration without any setup.

---

## Dataset Summary (v4 — Date-Corrected)

| Attribute | Value |
|-----------|-------|
| Source | Live fleet management system |
| Date range | **May 2025 – December 2026** (20 months) |
| Total records (Sheet1) | 14,526 |
| Full Tank trips | 8,489 |
| Trips with efficiency data | 8,243 |
| Unique vehicles (anonymised) | 178 VEH-xxx codes |
| Total fuel spend | KES 285.28M |
| Total litres dispensed | 1,222.8K L |
| Fleet average efficiency | 5.842 km/L |
| Over-EFC trips | 89.6% |
| Net over-spend vs EFC | KES 25.26M |
| Annual savings potential | KES 8.03M (Q3 target) |

---

## Deploying the Streamlit App

### Local

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### Streamlit Community Cloud

```bash
git init && git add . && git commit -m "Fleet Fuel Dashboard v4"
git remote add origin https://github.com/YOUR_USERNAME/fleet-fuel-dashboard.git
git push -u origin main
# → share.streamlit.io → New App → app.py → Deploy
```

> **Important:** Do NOT push `PII_Masking_Lookup_CONFIDENTIAL.xlsx` to any public repository.

---

## File Structure

```
fleet-fuel-dashboard/
├── app.py                                    ← Home page
├── utils.py                                  ← Shared logic (cached data loading, models, scoring)
├── requirements.txt
├── Fleet_Fuel_Cleaned_Dataset_v4.xlsx        ← Anonymised, date-corrected dataset (May 2025–Dec 2026)
├── .streamlit/config.toml                    ← Dark theme
├── assets/                                   ← 18 pre-generated matplotlib figures (NB1–NB3)
└── pages/
    ├── 1_📊_Overview.py
    ├── 2_📈_Trends.py
    ├── 3_🔬_EDA_Figures.py
    ├── 4_🤖_ML_Models.py
    ├── 5_🚗_Vehicles.py
    ├── 6_🗺_Routes.py
    └── 7_🚀_Deployment.py
```

---

## Privacy

All vehicle registration plates → `VEH-001…VEH-228`
All driver names → `DRV-001…DRV-1465`
Lookup table stored separately: `PII_Masking_Lookup_CONFIDENTIAL.xlsx` — **never committed to version control**
 
 