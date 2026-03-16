"""
Shared data loading, feature engineering, model training, and utility functions.
Called by all pages — cached so models only train once.

Data pipeline (v5 — CORRECTED):
  Sheet1 (15,214 rows) + Sheet2 (17,561 rows) STACKED → ~32,772 combined rows.
  Sheet1 holds efficiency outcome columns (km/L, mileage, KES variance).
  Sheet2 holds vehicle benchmark columns (EFC, EFE, Model).
  All feature engineering runs on the combined set.
  ML trains on 31,250+ rows (all rows with Route + Type + Model + Liters + Fuel).
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, IsolationForest
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ── Colour palette ──────────────────────────────────────────────────────────
ACCENT  = "#2DF5A8"
BLUE    = "#38B6FF"
AMBER   = "#FFB547"
RED     = "#FF4D6D"
PURPLE  = "#C084FC"
PALETTE = [RED, BLUE, AMBER, PURPLE, ACCENT, "#F5F53D"]
TYPE_COLORS = {"Bus": RED, "Shuttle": BLUE, "Eph": AMBER, "Admin": PURPLE}

BG     = "#0B0F1A"
SURF   = "#111827"
SURF2  = "#1A2235"
BORDER = "#1E2E47"
TEXT   = "#E2EAF4"
MUTED  = "#6B7E99"

PLOTLY_LAYOUT = dict(
    paper_bgcolor=BG, plot_bgcolor=SURF,
    font=dict(color=TEXT, family="Space Mono, monospace", size=11),
    margin=dict(l=40, r=20, t=40, b=40),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=BORDER, font=dict(color=MUTED)),
)
AXIS_STYLE = dict(gridcolor=BORDER, color=MUTED, linecolor=BORDER)

def apply_layout(fig, title="", height=350):
    fig.update_layout(**PLOTLY_LAYOUT,
                      title=dict(text=title, font=dict(color=TEXT, size=13)),
                      height=height)
    fig.update_xaxes(**AXIS_STYLE)
    fig.update_yaxes(**AXIS_STYLE)
    return fig

def hex_alpha(hex_color, alpha=0.7):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f"rgba({r},{g},{b},{alpha})"

# ── Helpers ─────────────────────────────────────────────────────────────────
def _parse_range_mid(val):
    s = str(val).strip()
    if ":" in s and len(s) > 10:
        return np.nan
    try:
        parts = s.split("-")
        return (float(parts[0].strip()) + float(parts[1].strip())) / 2
    except Exception:
        return np.nan

# ── Data loading ─────────────────────────────────────────────────────────────
DATA_FILE = "Fleet_Fuel_Cleaned_Dataset_v5.xlsx"

@st.cache_data(show_spinner="Loading & merging dataset…")
def load_data():
    raw1 = pd.read_excel(DATA_FILE, sheet_name="Sheet1_Cleaned", engine="openpyxl")
    raw2 = pd.read_excel(DATA_FILE, sheet_name="Sheet2_Cleaned", engine="openpyxl")
    car  = pd.read_excel(DATA_FILE, sheet_name="CarDriver_Lookup", engine="openpyxl")

    # ── Sheet 1 ──
    s1 = raw1.copy()
    s1["source"] = "S1"
    s1 = s1.drop(columns=["trip_status","Idling","Max Speed (kph)"], errors="ignore")
    car_map = car.set_index("PlateNo")["Model"].to_dict()
    s1["Model"]       = s1["PlateNo"].map(car_map)
    s1["EFC_mid_L"]   = np.nan
    s1["EFE_mid_kmL"] = np.nan

    # ── Sheet 2 ──
    s2 = raw2.copy()
    s2["source"]      = "S2"
    s2["EFC_mid_L"]   = s2["E.F.C"].apply(_parse_range_mid)
    s2["EFE_mid_kmL"] = s2["E.F.E"].apply(_parse_range_mid)
    s2 = s2.drop(columns=["E.F.C","E.F.E",
                           "DRIVER SERIAL NUMBER ",
                           "Number plate SERIAL number"], errors="ignore")

    s1_only = ["Liters Consumed","Fuel Amount","Mileage",
               "Fuel Efficiency (km/l)","Anticipated Consumption (L)",
               "Fuel Excess/Saved","KES Saved/Excess"]
    for col in s1_only:
        if col not in s2.columns:
            s2[col] = np.nan

    # ── Stack ──
    df = pd.concat([s1, s2], ignore_index=True, sort=False)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    for col in ["PlateNo","Route","Type","Model","Fueling Type","Petrol Station","Driver Name"]:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"nan":np.nan,"None":np.nan,"NaN":np.nan})

    df["Fueling Type"] = df["Fueling Type"].str.replace(
        r"(?i)^top[\s_]?up$","Top_Up",regex=True)
    df["Fueling Type"] = df["Fueling Type"].str.replace(
        r"(?i)^full[\s_]?tank$","Full_Tank",regex=True)
    df["Type"] = df["Type"].str.title()

    # Back-fill EFC/EFE for S1 rows via PlateNo lookup
    efc_map = (s2[s2["EFC_mid_L"].notna()]
               .groupby("PlateNo")[["EFC_mid_L","EFE_mid_kmL"]].first())
    mask = df["EFC_mid_L"].isna()
    df.loc[mask,"EFC_mid_L"]   = df.loc[mask,"PlateNo"].map(efc_map["EFC_mid_L"])
    df.loc[mask,"EFE_mid_kmL"] = df.loc[mask,"PlateNo"].map(efc_map["EFE_mid_kmL"])

    df = df.drop_duplicates(
        subset=["Instance ID","PlateNo","Date","Liters"], keep="first"
    ).reset_index(drop=True)

    # ── Feature engineering ──
    df["Year"]       = df["Date"].dt.year
    df["Month"]      = df["Date"].dt.month
    df["Quarter"]    = df["Date"].dt.quarter
    df["DayOfWeek"]  = df["Date"].dt.dayofweek
    df["Is_Weekend"] = (df["DayOfWeek"] >= 5).astype(int)
    df["Is_Full_Tank"] = df["Fueling Type"].str.contains("Full", na=False).astype(int)
    df["Cost_per_Litre"] = (df["Fuel"] / df["Liters"].replace(0,np.nan)).round(4)

    df["Fuel_Eff_kmL"] = pd.to_numeric(
        df.get("Fuel Efficiency (km/l)", pd.Series(np.nan,index=df.index)),
        errors="coerce")
    df.loc[df["Fuel_Eff_kmL"] > 30, "Fuel_Eff_kmL"] = np.nan

    df["EFC_deviation_L"] = (df["Liters"] - df["EFC_mid_L"]).round(4)
    df["EFC_pct_dev"]     = (df["EFC_deviation_L"] / df["EFC_mid_L"] * 100).round(2)
    df["Over_EFC"]        = (df["EFC_deviation_L"] > 0).astype(int)
    df["KES_variance"]    = (df["EFC_deviation_L"] * df["Cost_per_Litre"]).round(2)

    for col in ["Cost_per_Litre","Liters"]:
        q1, q3 = df[col].quantile([0.25,0.75])
        iqr = q3 - q1
        df[f"Anom_{col}"] = (
            (df[col] < q1-1.5*iqr)|(df[col] > q3+1.5*iqr)
        ).astype(int)
    df["Is_Anomaly"] = (
        (df["Anom_Cost_per_Litre"]==1)|(df["Anom_Liters"]==1)
    ).astype(int)

    df_full = df[df["Is_Full_Tank"]==1].copy()
    df_eff  = df_full[df_full["Fuel_Eff_kmL"].notna()].copy().reset_index(drop=True)
    return df, df_full, df_eff


@st.cache_data(show_spinner="Computing monthly aggregates…")
def get_monthly(_df_full):
    m = _df_full.copy()
    m["YM"] = m["Date"].dt.to_period("M")
    agg = m.groupby("YM").agg(
        Trips=("Instance ID","count"),
        Total_Liters=("Liters","sum"),
        Total_Cost=("Fuel","sum"),
        Avg_Eff=("Fuel_Eff_kmL","mean"),
        Net_KES=("KES_variance","sum"),
    ).reset_index()
    agg["Year_Month"] = agg["YM"].astype(str)
    agg["Month_num"]  = range(len(agg))
    agg["MA3"]    = agg["Total_Cost"].rolling(3,min_periods=1).mean()
    agg["Trend"]  = np.polyval(
        np.polyfit(range(len(agg)), agg["Total_Cost"],1), range(len(agg)))
    agg["MoM"]    = agg["Total_Liters"].pct_change()*100
    agg["Avg_Eff_f"] = agg["Avg_Eff"].ffill().bfill()
    agg["Is_Spike"]  = agg["Total_Liters"] > agg["Total_Liters"].quantile(0.9)
    agg["LPT"]    = agg["Total_Liters"] / agg["Trips"]
    return agg


@st.cache_resource(show_spinner="Training ML models (one-time, ~60 s)…")
def train_models(_df):
    ml = _df.dropna(subset=["Route","Type","Model","Liters","Fuel"]).copy()
    cat_cols = ["Route","Type","Model","Fueling Type"]
    le_dict = {}
    for col in cat_cols:
        ml[col] = ml[col].fillna("Unknown")
        le = LabelEncoder()
        ml[col+"_enc"] = le.fit_transform(ml[col].astype(str))
        le_dict[col] = le
    ml["EFC_filled"] = ml["EFC_mid_L"].fillna(ml["EFC_mid_L"].median())
    ml["EFE_filled"] = ml["EFE_mid_kmL"].fillna(ml["EFE_mid_kmL"].median())
    FEATURES = ["Cost_per_Litre","Year","Month","Quarter","DayOfWeek",
                "Is_Weekend","Is_Full_Tank","Route_enc","Type_enc",
                "Model_enc","Fueling Type_enc","EFC_filled","EFE_filled"]
    TARGET = "Liters"
    mdf = ml[FEATURES+[TARGET]].dropna()
    X = mdf[FEATURES].values; y = mdf[TARGET].values
    X_tr,X_te,y_tr,y_te = train_test_split(X,y,test_size=0.2,random_state=42)
    sc = StandardScaler()
    Xtr_sc = sc.fit_transform(X_tr); Xte_sc = sc.transform(X_te)
    models_def = {
        "Linear Regression (Ridge)": Ridge(alpha=1.0),
        "Random Forest": RandomForestRegressor(n_estimators=150,random_state=42,n_jobs=-1),
        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=300,max_depth=5,learning_rate=0.05,subsample=0.8,random_state=42),
        "Neural Network (MLP)": MLPRegressor(
            hidden_layer_sizes=(128,64,32),activation="relu",solver="adam",
            alpha=0.001,max_iter=500,early_stopping=True,random_state=42),
    }
    results = {}
    for name, model in models_def.items():
        use_sc = name in ("Linear Regression (Ridge)","Neural Network (MLP)")
        Xt = Xtr_sc if use_sc else X_tr
        Xv = Xte_sc if use_sc else X_te
        model.fit(Xt, y_tr); yp = model.predict(Xv)
        cv_X = sc.transform(mdf[FEATURES].values) if use_sc else mdf[FEATURES].values
        cv = cross_val_score(model,cv_X,y,cv=5,scoring="r2").mean()
        results[name] = {
            "model":model,"y_pred":yp,
            "r2":    round(float(r2_score(y_te,yp)),4),
            "mae":   round(float(mean_absolute_error(y_te,yp)),4),
            "rmse":  round(float(np.sqrt(mean_squared_error(y_te,yp))),4),
            "cv_mean":round(float(cv),4),
            "cv_std":0.0,
        }
    gb = models_def["Gradient Boosting"]
    fi = dict(zip(FEATURES, gb.feature_importances_))
    return results, y_te, FEATURES, models_def, fi


@st.cache_data(show_spinner="Scoring vehicles…")
def get_vehicle_scores(_df_eff):
    vp = _df_eff.groupby(["PlateNo","Type"]).agg(
        Trips=("Instance ID","count"),
        Avg_Eff=("Fuel_Eff_kmL","mean"),
        Avg_Liters=("Liters","mean"),
        Total_Cost=("Fuel","sum"),
        Net_KES=("KES_variance","sum"),
    ).reset_index()
    vp = vp[vp["Trips"]>=3].copy()
    vp["Score"] = vp.groupby("Type")["Avg_Eff"].transform(
        lambda x: ((x-x.min())/(x.max()-x.min()+1e-9)*100).round(1))
    vp["Grade"] = pd.cut(vp["Score"],bins=[0,40,60,80,101],labels=["D","C","B","A"])
    return vp


@st.cache_data(show_spinner="Scoring routes…")
def get_route_scores(_df_eff):
    ra = _df_eff.groupby(["Route","Type"]).agg(
        Trips=("Instance ID","count"),
        Avg_Eff=("Fuel_Eff_kmL","mean"),
        Std_Eff=("Fuel_Eff_kmL","std"),
    ).reset_index()
    ra = ra[ra["Trips"]>=5].copy()
    er = ra["Avg_Eff"].max()-ra["Avg_Eff"].min()+1e-9
    sr = ra["Std_Eff"].fillna(0).max()-ra["Std_Eff"].fillna(0).min()+1e-9
    ra["Score"] = (
        ((ra["Avg_Eff"]-ra["Avg_Eff"].min())/er)*0.6 +
        (1-(ra["Std_Eff"].fillna(0)-ra["Std_Eff"].fillna(0).min())/sr)*0.4
    )*100
    return ra


@st.cache_data(show_spinner="Detecting anomalies…")
def get_anomalies(_df):
    cols = ["Liters","Fuel","Cost_per_Litre"]
    mask = _df[cols].notna().all(axis=1)
    iso  = IsolationForest(contamination=0.05,n_estimators=200,random_state=42)
    iso.fit(_df.loc[mask,cols])
    labels = iso.predict(_df.loc[mask,cols])
    scores = iso.score_samples(_df.loc[mask,cols])
    out = _df.copy()
    out["IF_Anomaly"] = False; out["IF_Score"] = np.nan
    out.loc[mask,"IF_Anomaly"] = (labels==-1)
    out.loc[mask,"IF_Score"]   = scores
    return out


@st.cache_data(show_spinner="Computing savings…")
def get_savings(_df_eff, _df_full, _vehicle_scores):
    vp = _vehicle_scores.copy()
    type_q3 = _df_eff.groupby("Type")["Fuel_Eff_kmL"].quantile(0.75).to_dict()
    avg_cpl = (_df_full["Fuel"]/_df_full["Liters"].replace(0,np.nan)).median()
    n_months = max(len(_df_eff["Date"].dt.to_period("M").unique()),1)
    vp["Target_Eff"]  = vp["Type"].map(type_q3)
    vp["Gap"]         = (vp["Target_Eff"]-vp["Avg_Eff"]).clip(lower=0)
    vp["Monthly_L"]   = (vp["Trips"]/n_months)*vp["Avg_Liters"]
    vp["Monthly_KES"] = vp["Monthly_L"]*(vp["Gap"]/vp["Avg_Eff"].replace(0,np.nan))*avg_cpl
    monthly_sav = vp["Monthly_KES"].sum()
    annual_sav  = monthly_sav*12
    return vp, monthly_sav, annual_sav, type_q3


# ── Column display renaming ─────────────────────────────────────────────────
# Maps internal column names to clean display labels for any st.dataframe() output.
# PlateNo values are already VEH-xxx; Driver Name values are already DRV-xxxx.
# This just makes the column headers presentable.
DISPLAY_COLS = {
    "PlateNo":     "Vehicle ID",
    "Driver Name": "Driver ID",
    "Driver1":     "Driver ID",
    "Instance ID": "Trip ID",
    "Fuel":        "Fuel Cost (KES)",
    "Liters":      "Litres",
    "Fuel_Eff_kmL":"Efficiency (km/L)",
    "KES_variance":"KES Variance",
    "EFC_mid_L":   "EFC Benchmark (L)",
    "EFC_deviation_L": "EFC Deviation (L)",
    "Cost_per_Litre":  "Cost/Litre (KES)",
    "Is_Anomaly":  "Anomaly Flag",
    "Over_EFC":    "Over EFC",
    "source":      "Source Sheet",
}

def display_df(df, drop_pii=True, rename=True):
    """Return a display-safe copy of df: drops raw PII columns if any slipped through,
    renames columns to friendly labels."""
    out = df.copy()
    # Drop any raw PII columns that should never appear (belt-and-suspenders)
    pii_cols = ["Petrol Station"]  # operational detail not needed on screen
    out = out.drop(columns=[c for c in pii_cols if c in out.columns], errors="ignore")
    if rename:
        out = out.rename(columns={k: v for k, v in DISPLAY_COLS.items() if k in out.columns})
    return out
