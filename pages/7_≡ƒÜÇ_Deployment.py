"""Page 7 — Deployment, Forecasting & Savings"""
import streamlit as st
import plotly.graph_objects as go
from PIL import Image
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import (load_data, get_vehicle_scores, get_route_scores, get_anomalies,
                   get_savings, train_models, ACCENT, BLUE, AMBER, RED, PURPLE,
                   PALETTE, TYPE_COLORS, BG, SURF, BORDER, TEXT, MUTED, apply_layout)

st.set_page_config(page_title="Deployment · Fleet Fuel", page_icon="🚀", layout="wide")
st.markdown("<style>.stApp{background-color:#0B0F1A;}section[data-testid='stSidebar']{background-color:#111827;border-right:1px solid #1E2E47;}</style>", unsafe_allow_html=True)

ASSETS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

st.title("🚀 Deployment & Decision Support")
st.caption("CRISP-DM Phase 6 | RO3 — Practical applicability and intervention roadmap")

df1, df2, df1_full, df1_eff = load_data()
vp = get_vehicle_scores(df1_eff)
ra = get_route_scores(df1_eff)
anom_df = get_anomalies(df1_eff)
vp2, monthly_sav, annual_sav, type_q3 = get_savings(df1_eff, df1_full, vp)
results, y_test, SELECTED, models = train_models(df1_eff)
n_anom = int(anom_df["Is_Anomaly"].sum())

# ── Savings hero section ──────────────────────────────────────────────────────
st.markdown(f"""
<div style='background:linear-gradient(135deg,rgba(45,245,168,.06),rgba(45,245,168,.02));
     border:1px solid rgba(45,245,168,.25);padding:1.5rem 2rem;margin-bottom:1.2rem'>
  <div style='font-family:Space Mono,monospace;font-size:.62rem;color:{MUTED};
       letter-spacing:.1em;text-transform:uppercase;margin-bottom:.4rem'>
    Estimated Annual Savings Potential</div>
  <div style='font-size:3rem;font-weight:800;color:{ACCENT};letter-spacing:-.04em;line-height:1'>
    KES {annual_sav/1e6:.2f}M</div>
  <div style='font-family:Space Mono,monospace;font-size:.65rem;color:{MUTED};margin-top:.4rem'>
    If all vehicles reach 75th-percentile (Q3) efficiency target within their vehicle type</div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("📅 Monthly Savings",     f"KES {monthly_sav/1000:.0f}K",             "Per month at Q3 target")
c2.metric("🔍 Anomalies Flagged",   str(n_anom),                                 "5% Isolation Forest", delta_color="inverse")
c3.metric("🤖 Best Model R²",       str(results["Gradient Boosting"]["r2"]),     "GBM (Gradient Boosting)")
c4.metric("🗺 Routes Scored",       str(len(ra)),                                "61 routes ranked")

st.markdown("---")

# ── Savings by type ───────────────────────────────────────────────────────────
sbt = vp2.groupby("Type").agg(Monthly_KES=("Monthly_KES","sum"), Avg_Gap=("Gap","mean")).reset_index()

col_a, col_b = st.columns(2)
with col_a:
    fig = go.Figure(go.Bar(
        x=sbt["Type"], y=sbt["Monthly_KES"]/1000,
        marker_color=[TYPE_COLORS.get(t, BLUE) for t in sbt["Type"]],
        marker_line_color=[TYPE_COLORS.get(t, BLUE) for t in sbt["Type"]],
        marker_line_width=1.5,
        text=(sbt["Monthly_KES"]/1000).round(0).astype(int).astype(str).apply(lambda v: f"KES {v}K"),
        textposition="outside",
    ))
    apply_layout(fig, "Monthly Savings Potential by Vehicle Type (KES)", 310)
    fig.update_layout(yaxis_title="KES (000s)", xaxis=dict(gridcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig, width='stretch')

with col_b:
    fig2 = go.Figure(go.Bar(
        x=sbt["Type"], y=sbt["Avg_Gap"].round(3),
        marker_color=[TYPE_COLORS.get(t, BLUE) for t in sbt["Type"]],
        text=sbt["Avg_Gap"].round(2).astype(str) + " km/L",
        textposition="outside",
    ))
    apply_layout(fig2, "Avg Efficiency Gap vs Q3 Target (km/L)", 310)
    fig2.update_layout(yaxis_title="Gap (km/L)", xaxis=dict(gridcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig2, width='stretch')

# ── Recommended interventions ─────────────────────────────────────────────────
st.markdown("---")
st.markdown("### Recommended Interventions")
col1, col2, col3, col4 = st.columns(4)
interventions = [
    (col1, "🚗", "Driver Eco-Training",    ACCENT,
     f"Bottom 20% DRV-coded drivers consume 2× more fuel. "
     f"{int((vp2['Gap']>0).sum())} vehicles with efficiency gap identified for targeted coaching."),
    (col2, "🗺", "Route Re-allocation",    BLUE,
     f"Bottom 10 routes show high efficiency variability. "
     f"Reassign Bus fleet to routes with score >60 where feasible."),
    (col3, "🔧", "Preventive Maintenance", AMBER,
     f"{n_anom} anomalous trips flagged. Cross-reference with maintenance logs "
     f"to identify systemic faults in Grade D vehicles."),
    (col4, "⚡", "Real-time Anomaly API",  RED,
     f"Deploy GBM model (R²={results['Gradient Boosting']['r2']}) as REST API endpoint "
     f"to flag deviating trips in-journey for dispatcher alerts."),
]
for col, icon, title, color, desc in interventions:
    with col:
        st.markdown(f"""<div style='background:{SURF};border:1px solid {BORDER};
            border-top:2px solid {color};padding:1rem'>
            <div style='font-size:1.4rem;margin-bottom:.4rem'>{icon}</div>
            <div style='font-size:.84rem;font-weight:700;color:{color};margin-bottom:.4rem'>{title}</div>
            <div style='font-family:Space Mono,monospace;font-size:.6rem;color:{MUTED};line-height:1.6'>{desc}</div>
        </div>""", unsafe_allow_html=True)

# ── RO summary ────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### Research Objectives — Summary")
q3_eff = df1_eff["Fuel Efficiency (km/l)"].quantile(0.75)

ro_data = {
    "Research Objective": ["RO1 — Predictive Model", "RO1 — Forecasting", "RO2 — Key Factors",
                            "RO3 — Vehicle Scoring", "RO3 — Anomaly Detection",
                            "RO3 — Route Scoring", "RO3 — Savings Estimate"],
    "Result / Output": [
        f"GBM R²={results['Gradient Boosting']['r2']}, MAE={results['Gradient Boosting']['mae']} km/L",
        "Monthly volume R²=0.931 (lag-feature GBM)",
        "Litres, Mileage, Vehicle Type, Route Category",
        f"{len(vp2)} vehicles graded A–D (within-type)",
        f"{n_anom} trips flagged (Isolation Forest, 5%)",
        f"{len(ra)} routes ranked (60% eff + 40% consistency)",
        f"KES {annual_sav/1e6:.2f}M/year at Q3 target ({q3_eff:.2f} km/L)",
    ],
    "CRISP-DM Phase": ["Modelling","Modelling","Data Understanding",
                        "Evaluation","Evaluation","Evaluation","Deployment"],
}
import pandas as pd
st.dataframe(pd.DataFrame(ro_data), width='stretch', hide_index=True)

# ── NB3 figures ───────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### Notebook 3 Figures")
for key, title in [
    ("fig3_1_timeseries",        "Fig 3.1 — Time-Series Decomposition"),
    ("fig3_2_forecasting",       "Fig 3.2 — ML Forecasting (GBM Lag-Feature Model)"),
    ("fig3_4_anomaly",           "Fig 3.4 — Anomaly Detection (Isolation Forest)"),
    ("fig3_6_savings",           "Fig 3.6 — Savings Potential & CRISP-DM Deployment Summary"),
]:
    with st.expander(f"**{title}**"):
        path = os.path.join(ASSETS, f"{key}.png")
        if os.path.exists(path):
            st.image(Image.open(path), width='stretch')
