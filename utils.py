"""
Shared data loading, model training, and utility functions
Called by all pages — cached so models only train once.
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

from sklearn.linear_model import Ridge, LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, IsolationForest
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.feature_selection import RFE

# ── Colour palette ─────────────────────────────────────────────────────────
ACCENT  = "#2DF5A8"
BLUE    = "#38B6FF"
AMBER   = "#FFB547"
RED     = "#FF4D6D"
PURPLE  = "#C084FC"
PALETTE = [RED, BLUE, AMBER, PURPLE, ACCENT, "#F5F53D"]
TYPE_COLORS = {"Bus": RED, "Shuttle": BLUE, "EPH": AMBER, "Admin": PURPLE}

BG     = "#0B0F1A"
SURF   = "#111827"
SURF2  = "#1A2235"
BORDER = "#1E2E47"
TEXT   = "#E2EAF4"
MUTED  = "#6B7E99"

PLOTLY_LAYOUT = dict(
    paper_bgcolor=BG, plot_bgcolor=SURF,
    font=dict(color=TEXT, family="Space Mono, monospace", size=11),
    xaxis=dict(gridcolor=BORDER, color=MUTED, linecolor=BORDER),
    yaxis=dict(gridcolor=BORDER, color=MUTED, linecolor=BORDER),
    margin=dict(l=40, r=20, t=40, b=40),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=BORDER, font=dict(color=MUTED)),
)

def apply_layout(fig, title="", height=350):
    fig.update_layout(**PLOTLY_LAYOUT, title=dict(text=title, font=dict(color=TEXT, size=13)),
                      height=height)
    return fig

# ── Data loading ───────────────────────────────────────────────────────────
DATA_FILE = "Fleet_Fuel_Cleaned_Dataset_v4.xlsx"

@st.cache_data(show_spinner="Loading dataset…")
def load_data():
    df1 = pd.read_excel(DATA_FILE, sheet_name="Sheet1_Cleaned", engine="openpyxl")
    df2 = pd.read_excel(DATA_FILE, sheet_name="Sheet2_Cleaned", engine="openpyxl")
    df1["Date"] = pd.to_datetime(df1["Date"], errors="coerce")
    df2["Date"] = pd.to_datetime(df2["Date"], errors="coerce")
    df1_full = df1[df1["Fueling Type"] == "Full_Tank"].copy()
    df1_eff  = df1_full[
        df1_full["Fuel Efficiency (km/l)"].notna() & df1_full["Mileage"].notna()
    ].copy().reset_index(drop=True)
    return df1, df2, df1_full, df1_eff

@st.cache_data(show_spinner="Computing monthly aggregates…")
def get_monthly(_df1_full):
    _df1_full = _df1_full.copy()
    _df1_full["YM"] = _df1_full["Date"].dt.to_period("M")
    m = _df1_full.groupby("YM").agg(
        Trips=("Instance ID", "count"),
        Total_Liters=("Liters", "sum"),
        Total_Cost=("Fuel Amount", "sum"),
        Avg_Eff=("Fuel Efficiency (km/l)", "mean"),
        Net_KES=("KES Saved/Excess", "sum"),
    ).reset_index()
    m["Year_Month"] = m["YM"].astype(str)
    m["Month_num"]  = range(len(m))
    m["MA3"]        = m["Total_Cost"].rolling(3, min_periods=1).mean()
    m["Trend"]      = np.polyval(np.polyfit(range(len(m)), m["Total_Cost"], 1), range(len(m)))
    m["MoM"]        = m["Total_Liters"].pct_change() * 100
    m["Avg_Eff_f"]  = m["Avg_Eff"].ffill().bfill()
    m["Is_Spike"]   = m["Total_Liters"] > 100_000
    m["LPT"]        = m["Total_Liters"] / m["Trips"]
    return m

@st.cache_resource(show_spinner="Training ML models (one-time, ~60s)…")
def train_models(_df1_eff):
    fe = _df1_eff.copy()
    fe["Route_Category"] = pd.cut(fe["Mileage"], bins=[0,400,800,9999], labels=["Short","Medium","Long"])
    fe["Cost_per_Litre"] = fe["Fuel Amount"] / fe["Liters"].replace(0, np.nan)
    fe["Month_sin"]      = np.sin(2 * np.pi * fe["Date"].dt.month / 12)
    fe["Month_cos"]      = np.cos(2 * np.pi * fe["Date"].dt.month / 12)
    le_t = LabelEncoder(); le_r = LabelEncoder()
    fe["Type_enc"]      = le_t.fit_transform(fe["Type"].fillna("Unknown"))
    fe["Route_enc"]     = le_r.fit_transform(fe["Route"].fillna("Unknown"))
    fe["Route_Cat_enc"] = fe["Route_Category"].map({"Short":0,"Medium":1,"Long":2}).fillna(1)

    FEATURES = ["Liters","Mileage","Fuel Amount","Cost_per_Litre","Type_enc",
                "Route_Cat_enc","Month_sin","Month_cos","Odometer","Route_enc"]
    TARGET   = "Fuel Efficiency (km/l)"
    mdf      = fe[FEATURES + [TARGET]].dropna()
    X_all = mdf[FEATURES].values; y_all = mdf[TARGET].values

    rfe = RFE(LinearRegression(), n_features_to_select=6, step=1)
    rfe.fit(StandardScaler().fit_transform(X_all), y_all)
    SELECTED = [FEATURES[i] for i, s in enumerate(rfe.support_) if s]

    X = mdf[SELECTED].values; y = y_all
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
    sc  = StandardScaler()
    Xtr = sc.fit_transform(X_tr); Xte = sc.transform(X_te)
    kf  = KFold(n_splits=5, shuffle=True, random_state=42)

    models = {
        "Linear Regression": Ridge(alpha=1.0),
        "Random Forest":     RandomForestRegressor(n_estimators=200, max_depth=12,
                                                   min_samples_leaf=4, n_jobs=-1, random_state=42),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=300, max_depth=5,
                                                       learning_rate=0.05, subsample=0.8, random_state=42),
        "Neural Network":    MLPRegressor(hidden_layer_sizes=(128,64,32), activation="relu",
                                          solver="adam", alpha=0.001, max_iter=500,
                                          early_stopping=True, random_state=42),
    }
    results = {}
    for name, model in models.items():
        model.fit(Xtr, y_tr)
        yp = model.predict(Xte)
        cv = cross_val_score(model, Xtr, y_tr, cv=kf, scoring="r2")
        results[name] = {
            "model": model, "y_pred": yp,
            "r2":      round(r2_score(y_te, yp), 4),
            "mae":     round(mean_absolute_error(y_te, yp), 4),
            "rmse":    round(float(np.sqrt(mean_squared_error(y_te, yp))), 4),
            "cv_mean": round(cv.mean(), 4),
            "cv_std":  round(cv.std(), 4),
        }
    return results, y_te, SELECTED, models

@st.cache_data(show_spinner="Scoring vehicles…")
def get_vehicle_scores(_df1_eff):
    vp = _df1_eff.groupby(["PlateNo","Type"]).agg(
        Trips=("Instance ID","count"),
        Avg_Eff=("Fuel Efficiency (km/l)","mean"),
        Avg_Liters=("Liters","mean"),
        Total_Cost=("Fuel Amount","sum"),
        Net_KES=("KES Saved/Excess","sum"),
    ).reset_index()
    vp = vp[vp["Trips"] >= 5].copy()
    vp["Score"] = vp.groupby("Type")["Avg_Eff"].transform(
        lambda x: ((x - x.min()) / (x.max() - x.min() + 1e-9) * 100).round(1))
    vp["Grade"] = pd.cut(vp["Score"], bins=[0,40,60,80,101], labels=["D","C","B","A"])
    return vp

@st.cache_data(show_spinner="Scoring routes…")
def get_route_scores(_df1_eff):
    ra = _df1_eff.groupby(["Route","Type"]).agg(
        Trips=("Instance ID","count"),
        Avg_Eff=("Fuel Efficiency (km/l)","mean"),
        Std_Eff=("Fuel Efficiency (km/l)","std"),
    ).reset_index()
    ra = ra[ra["Trips"] >= 10].copy()
    er = ra["Avg_Eff"].max() - ra["Avg_Eff"].min() + 1e-9
    sr = ra["Std_Eff"].fillna(0).max() - ra["Std_Eff"].fillna(0).min() + 1e-9
    ra["Score"] = (((ra["Avg_Eff"] - ra["Avg_Eff"].min()) / er) * 0.6 +
                   (1 - (ra["Std_Eff"].fillna(0) - ra["Std_Eff"].fillna(0).min()) / sr) * 0.4) * 100
    return ra

@st.cache_data(show_spinner="Detecting anomalies…")
def get_anomalies(_df1_eff):
    cols = ["Liters","Fuel Amount","Mileage","Fuel Efficiency (km/l)","Fuel Excess/Saved"]
    mask = _df1_eff[cols].notna().all(axis=1)
    iso  = IsolationForest(contamination=0.05, n_estimators=200, random_state=42)
    iso.fit(_df1_eff.loc[mask, cols])
    labels = iso.predict(_df1_eff.loc[mask, cols])
    scores = iso.score_samples(_df1_eff.loc[mask, cols])
    out = _df1_eff.copy()
    out["Is_Anomaly"]    = False
    out["Anomaly_Score"] = np.nan
    out.loc[mask, "Is_Anomaly"]    = (labels == -1)
    out.loc[mask, "Anomaly_Score"] = scores
    return out

@st.cache_data(show_spinner="Computing savings…")
def get_savings(_df1_eff, _df1_full, _vehicle_scores):
    vp = _vehicle_scores.copy()
    type_q3    = _df1_eff.groupby("Type")["Fuel Efficiency (km/l)"].quantile(0.75).to_dict()
    avg_cpl    = (_df1_full["Fuel Amount"] / _df1_full["Liters"].replace(0, np.nan)).median()
    vp["Target_Eff"]  = vp["Type"].map(type_q3)
    vp["Gap"]         = (vp["Target_Eff"] - vp["Avg_Eff"]).clip(lower=0)
    vp["Monthly_L"]   = vp["Trips"] / 24 * vp["Avg_Liters"]
    vp["Monthly_KES"] = vp["Monthly_L"] * (vp["Gap"] / vp["Avg_Eff"].replace(0, np.nan)) * avg_cpl
    monthly_sav = vp["Monthly_KES"].sum()
    annual_sav  = monthly_sav * 12
    return vp, monthly_sav, annual_sav, type_q3
