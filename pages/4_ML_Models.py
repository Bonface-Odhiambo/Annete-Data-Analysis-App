"""
Page 4 — ML Models
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="ML Models | Fleet Fuel", page_icon="⚙️", layout="wide")

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from theme import inject_css, sidebar_brand, sec_header, insight, apply_plotly
from utils import load_data, train_models

inject_css()
sidebar_brand()

df, df_full, df_eff = load_data()
results, y_te, features, models_def, feat_imp = train_models(df)

st.markdown("""
<div class="ui-card" style="background:linear-gradient(135deg,rgba(255,209,102,.06),rgba(182,156,255,.04));margin-bottom:22px">
  <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:900;color:#F0EDFF">🤖 ML Models</div>
  <div style="font-family:'Space Mono',monospace;font-size:10px;color:rgba(240,237,255,.3);margin-top:4px">
    4-model comparison · Ridge · Random Forest · Gradient Boosting · MLP
  </div>
</div>
""", unsafe_allow_html=True)

# ── Model cards ───────────────────────────────────────────────────────────────
sec_header("Model Performance", "Test Set Results")

COLOR_MAP = {
    "Linear Regression (Ridge)": ("#74B9FF", "sky"),
    "Random Forest":              ("#B69CFF", "violet"),
    "Gradient Boosting":          ("#C3F73A", "lime"),
    "Neural Network (MLP)":       ("#FFD166", "gold"),
}

best_name = max(results, key=lambda k: results[k]["r2"])

cols = st.columns(4)
for i, (name, res) in enumerate(results.items()):
    color_hex, color_var = COLOR_MAP.get(name, ("#00E5FF","cyan"))
    is_champion = name == best_name
    border = "rgba(195,247,58,.4)" if is_champion else "rgba(255,255,255,.08)"
    badge = '<span style="font-family:\'Space Mono\',monospace;font-size:8px;color:#C3F73A;background:rgba(195,247,58,.12);border:1px solid rgba(195,247,58,.3);border-radius:20px;padding:2px 8px;margin-left:8px">✦ Champion</span>' if is_champion else ""

    with cols[i]:
        st.markdown(f"""
<div style="background:#1A1530;border:1px solid {border};border-radius:14px;
  padding:18px 16px;position:relative;overflow:hidden;height:100%">
  <div style="position:absolute;bottom:0;left:0;right:0;height:3px;
    background:linear-gradient(90deg,{color_hex}44,{color_hex})"></div>
  <div style="font-family:'Outfit',sans-serif;font-size:12px;font-weight:700;
    color:#F0EDFF;margin-bottom:4px">{name}{badge}</div>
  <div style="font-family:'Outfit',sans-serif;font-size:28px;font-weight:900;
    color:{color_hex};letter-spacing:-.03em;margin:10px 0 4px">{res['r2']}</div>
  <div style="font-family:'Space Mono',monospace;font-size:8px;
    color:rgba(240,237,255,.3);margin-bottom:10px">R² Score</div>
  <div style="display:flex;justify-content:space-between;
    font-family:'Space Mono',monospace;font-size:9px;color:rgba(240,237,255,.45)">
    <span>MAE<br><strong style="color:#F0EDFF">{res['mae']}</strong></span>
    <span>RMSE<br><strong style="color:#F0EDFF">{res['rmse']}</strong></span>
    <span>CV R²<br><strong style="color:#F0EDFF">{res['cv_mean']}</strong></span>
  </div>
</div>""", unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── Bar comparison ────────────────────────────────────────────────────────────
sec_header("Metric Comparison", "All 4 Models")

tab1, tab2, tab3 = st.tabs(["R² Score", "MAE (km/L)", "RMSE (km/L)"])

names  = list(results.keys())
colors = [COLOR_MAP[n][0] for n in names]

for tab, metric, label in [
    (tab1, "r2",   "R² Score"),
    (tab2, "mae",  "MAE (km/L)"),
    (tab3, "rmse", "RMSE (km/L)"),
]:
    with tab:
        vals = [results[n][metric] for n in names]
        fig = go.Figure(go.Bar(
            x=names, y=vals,
            marker_color=colors,
            marker_line_color="#0F0B1E",
            marker_line_width=2,
            text=[f"{v:.4f}" for v in vals],
            textposition="outside",
            textfont=dict(family="Space Mono, monospace", size=10, color="#F0EDFF"),
        ))
        apply_plotly(fig, label, height=300)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# ── Feature importance ────────────────────────────────────────────────────────
sec_header("GBM Feature Importance", "Gradient Boosting Champion Model")

left, right = st.columns([1, 1])

with left:
    fi_sorted = sorted(feat_imp.items(), key=lambda x: x[1], reverse=True)
    fi_names  = [f[0] for f in fi_sorted]
    fi_vals   = [f[1] for f in fi_sorted]

    fig_fi = go.Figure(go.Bar(
        y=fi_names, x=fi_vals,
        orientation="h",
        marker_color=["#00E5FF" if v == max(fi_vals) else "#B69CFF" for v in fi_vals],
        marker_line_color="#0F0B1E", marker_line_width=1,
        text=[f"{v:.3f}" for v in fi_vals], textposition="outside",
        textfont=dict(family="Space Mono, monospace", size=9, color="#F0EDFF"),
    ))
    apply_plotly(fig_fi, "Feature Importance (GBM)", height=len(fi_names)*36 + 60)
    fig_fi.update_layout(showlegend=False)
    st.plotly_chart(fig_fi, use_container_width=True)

with right:
    # Actual vs predicted scatter for champion
    gb_res = results[best_name]
    y_pred = gb_res["y_pred"]
    n = min(len(y_te), len(y_pred), 800)
    idx = np.random.choice(len(y_te), n, replace=False)

    fig_av = go.Figure()
    fig_av.add_trace(go.Scatter(
        x=y_te[idx], y=y_pred[idx],
        mode="markers",
        marker=dict(color="#00E5FF", size=4, opacity=0.6,
                    line=dict(color="#0F0B1E", width=0.5)),
        name="Predicted vs Actual",
    ))
    mn = min(y_te[idx].min(), y_pred[idx].min())
    mx = max(y_te[idx].max(), y_pred[idx].max())
    fig_av.add_trace(go.Scatter(
        x=[mn, mx], y=[mn, mx],
        mode="lines", name="Perfect Fit",
        line=dict(color="#C3F73A", width=1.5, dash="dot"),
    ))
    apply_plotly(fig_av, f"{best_name} — Actual vs Predicted", height=380)
    st.plotly_chart(fig_av, use_container_width=True)

insight(f"""
<strong>Champion: {best_name}</strong> — R² = {results[best_name]['r2']}, 
MAE = {results[best_name]['mae']} L, RMSE = {results[best_name]['rmse']} L. 
Top feature: <strong>{fi_sorted[0][0]}</strong> ({fi_sorted[0][1]:.1%} importance).
The wide gap between Ridge MAE ({results['Linear Regression (Ridge)']['mae']}) and GBM MAE 
({results['Gradient Boosting']['mae']}) confirms the relationship is substantially non-linear.
""")
