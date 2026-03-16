"""Page 4 — ML Models"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import (load_data, train_models, ACCENT, BLUE, AMBER, RED, PURPLE,
                   BG, SURF, BORDER, TEXT, MUTED, PLOTLY_LAYOUT, apply_layout, hex_alpha)

st.set_page_config(page_title="ML Models · Fleet Fuel", page_icon="🤖", layout="wide")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=JetBrains+Mono:wght@400;500&family=Inter:wght@400;500&display=swap');
.stApp{background-color:#080D18;color:#E8F0FF;}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#0A1120 0%,#0D1828 60%,#091016 100%);border-right:1px solid #1C2D47;}
.sb-brand{padding:1.4rem 1.2rem 1rem;border-bottom:1px solid #1C2D47;background:linear-gradient(135deg,rgba(0,229,160,.06) 0%,rgba(0,184,255,.04) 100%);}
.sb-brand-icon{font-size:2rem;line-height:1;margin-bottom:.4rem;}
.sb-brand-title{font-family:'Syne',sans-serif;font-size:1.05rem;font-weight:800;color:#E8F0FF;letter-spacing:-.01em;line-height:1.2;margin:0;}
.sb-brand-sub{font-family:'JetBrains Mono',monospace;font-size:.6rem;color:#00E5A0;letter-spacing:.1em;text-transform:uppercase;margin-top:.3rem;}
.sb-section-label{font-family:'JetBrains Mono',monospace;font-size:.52rem;letter-spacing:.15em;text-transform:uppercase;color:#5A7299;padding:.9rem 1.2rem .3rem;}
.sb-nav-item{display:flex;align-items:center;gap:.75rem;padding:.55rem 1.2rem;margin:.1rem .5rem;border-radius:8px;border:1px solid transparent;}
.sb-nav-icon{width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1rem;flex-shrink:0;}
.sb-nav-text{font-family:'Inter',sans-serif;font-size:.82rem;font-weight:500;color:#E8F0FF;}
.sb-nav-badge{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:.55rem;color:#5A7299;background:#162035;border:1px solid #1C2D47;padding:.1rem .35rem;border-radius:4px;}
.ic-teal{background:rgba(0,229,160,.15);}.ic-blue{background:rgba(0,184,255,.15);}.ic-amber{background:rgba(255,184,48,.15);}.ic-red{background:rgba(255,61,107,.15);}.ic-purple{background:rgba(176,110,255,.15);}.ic-green{background:rgba(52,211,153,.15);}.ic-cyan{background:rgba(34,211,238,.15);}
.sb-author{margin:.8rem .5rem;padding:.75rem 1rem;background:#162035;border:1px solid #1C2D47;border-radius:10px;}
.sb-author-name{font-family:'Syne',sans-serif;font-size:.82rem;font-weight:700;color:#E8F0FF;}
.sb-author-detail{font-family:'JetBrains Mono',monospace;font-size:.58rem;color:#8A9BBB;line-height:1.7;margin-top:.3rem;}
.sb-privacy{margin:.5rem .5rem .8rem;padding:.5rem 1rem;background:rgba(0,229,160,.04);border:1px solid rgba(0,229,160,.2);border-radius:8px;display:flex;align-items:center;gap:.5rem;}
.sb-privacy-icon{font-size:.9rem;}
.sb-privacy-text{font-family:'JetBrains Mono',monospace;font-size:.58rem;color:#00E5A0;letter-spacing:.05em;line-height:1.5;}
h1,h2,h3{font-family:'Syne',sans-serif!important;}
footer{display:none!important;}#MainMenu{display:none!important;}
</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
      <div class="sb-brand-icon">⛽</div>
      <div class="sb-brand-title">Fleet Fuel<br>Intelligence</div>
      <div class="sb-brand-sub">MSc Dissertation · Strathmore</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="sb-section-label">Navigation</div>', unsafe_allow_html=True)
    nav_items = [
        ("📊", "ic-teal",   "Overview & KPIs",    "KPI summary"),
        ("📈", "ic-blue",   "Trends",             "Time series"),
        ("🔬", "ic-purple", "EDA Figures",        "NB1 outputs"),
        ("🤖", "ic-amber",  "ML Models",          "R²=0.9212"),
        ("🚗", "ic-red",    "Vehicles",           "VEH-xxx scores"),
        ("🗺", "ic-cyan",   "Routes",             "Route analysis"),
        ("🚀", "ic-green",  "Deployment",         "Savings"),
    ]
    for icon, ic_cls, label, badge in nav_items:
        st.markdown(f"""
        <div class="sb-nav-item">
          <div class="sb-nav-icon {ic_cls}">{icon}</div>
          <span class="sb-nav-text">{label}</span>
          <span class="sb-nav-badge">{badge}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("""
    <div class="sb-section-label" style="margin-top:.6rem">Researcher</div>
    <div class="sb-author">
      <div class="sb-author-name">Anette Kerubo Joseph</div>
      <div class="sb-author-detail">Reg No: 151384<br>MSc Data Science &amp; Analytics<br>Strathmore University</div>
    </div>
    <div class="sb-privacy">
      <span class="sb-privacy-icon">🔒</span>
      <div class="sb-privacy-text">Plates → VEH-xxx<br>Drivers → DRV-xxxx<br>PII stored separately</div>
    </div>
    """, unsafe_allow_html=True)



st.title("🤖 ML Models & Performance")
st.caption(f"Target: Litres consumed per fueling event · Training set: combined 31,250+ rows · 4 models compared")

df, df_full, df_eff = load_data()
results, y_te, features, models_def, fi = train_models(df)

model_names = list(results.keys())
MODEL_COLORS = [RED, BLUE, AMBER, PURPLE]

c1, c2 = st.columns(2)
with c1:
    r2_vals = [results[n]["r2"] for n in model_names]
    fig = go.Figure(go.Bar(
        x=model_names, y=r2_vals,
        marker_color=[hex_alpha(c, 0.73) for c in MODEL_COLORS],
        marker_line_color=MODEL_COLORS, marker_line_width=2,
        text=[f"{v:.4f}" for v in r2_vals], textposition="outside",
    ))
    apply_layout(fig, "R² Score by Model", 320)
    fig.update_layout(showlegend=False)
    fig.update_xaxes(tickangle=-20)
    fig.update_yaxes(range=[0.7, 1.0])
    st.plotly_chart(fig, width="stretch")

with c2:
    mae_vals  = [results[n]["mae"]  for n in model_names]
    rmse_vals = [results[n]["rmse"] for n in model_names]
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(name="MAE",  x=model_names, y=mae_vals,
                          marker_color=[hex_alpha(c,0.73) for c in MODEL_COLORS]))
    fig2.add_trace(go.Bar(name="RMSE", x=model_names, y=rmse_vals,
                          marker_color=[hex_alpha(c,0.45) for c in MODEL_COLORS],
                          marker_line_color=MODEL_COLORS, marker_line_width=1.5))
    apply_layout(fig2, "MAE & RMSE by Model (Litres)", 320)
    fig2.update_layout(barmode="group", xaxis_tickangle=-20)
    st.plotly_chart(fig2, width="stretch")

# ── Metrics table ──────────────────────────────────────────────────────────
st.markdown("#### Model Comparison Table")
import pandas as pd
tbl = pd.DataFrame([{
    "Model": n,
    "R²":      results[n]["r2"],
    "MAE (L)": results[n]["mae"],
    "RMSE (L)":results[n]["rmse"],
    "CV R²":   results[n]["cv_mean"],
} for n in model_names])
st.dataframe(tbl.set_index("Model"), use_container_width=True)

# ── Feature importance ─────────────────────────────────────────────────────
st.markdown("#### Feature Importance (Gradient Boosting)")
fi_sorted = sorted(fi.items(), key=lambda x: -x[1])
fi_names  = [x[0] for x in fi_sorted]
fi_vals   = [x[1] for x in fi_sorted]
fig3 = go.Figure(go.Bar(
    x=fi_vals, y=fi_names, orientation="h",
    marker_color=[hex_alpha(ACCENT, 0.7)]*len(fi_names),
    marker_line_color=ACCENT, marker_line_width=1,
    text=[f"{v:.3f}" for v in fi_vals], textposition="outside",
))
apply_layout(fig3, "Feature Importance — Gradient Boosting", 380)
fig3.update_layout(showlegend=False)
st.plotly_chart(fig3, width="stretch")

# ── Actual vs predicted ────────────────────────────────────────────────────
st.markdown("#### Actual vs Predicted — Gradient Boosting")
gb_pred = results["Gradient Boosting"]["y_pred"]
fig4 = go.Figure()
fig4.add_trace(go.Scatter(
    x=y_te[:800], y=gb_pred[:800], mode="markers",
    marker=dict(color=hex_alpha(ACCENT, 0.5), size=4),
    name="Predictions",
    hovertemplate="Actual: %{x:.1f} L<br>Pred: %{y:.1f} L<extra></extra>"
))
mn, mx = float(y_te.min()), float(y_te.max())
fig4.add_trace(go.Scatter(x=[mn,mx], y=[mn,mx], mode="lines",
                           line=dict(color=RED, dash="dash", width=1.5), name="Perfect fit"))
apply_layout(fig4, "Actual vs Predicted Litres (sample 800 test points)", 380)
fig4.update_layout(xaxis_title="Actual (L)", yaxis_title="Predicted (L)")
st.plotly_chart(fig4, width="stretch")

st.info(f"""**Dataset note:** Models trained on **{len(df.dropna(subset=['Route','Type','Model','Liters','Fuel'])):,} rows** 
(all ML-ready records from the combined Sheet1 + Sheet2 dataset). 
Champion: **Gradient Boosting** — R² {results['Gradient Boosting']['r2']:.4f}, 
MAE {results['Gradient Boosting']['mae']:.2f} L, RMSE {results['Gradient Boosting']['rmse']:.2f} L.""")
