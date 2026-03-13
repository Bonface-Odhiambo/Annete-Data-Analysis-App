"""Page 4 — ML Models"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from PIL import Image
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import (load_data, train_models, ACCENT, BLUE, AMBER, RED, PURPLE,
                   BG, SURF, BORDER, TEXT, MUTED, PLOTLY_LAYOUT, apply_layout)

st.set_page_config(page_title="ML Models · Fleet Fuel", page_icon="🤖", layout="wide")
st.markdown("<style>.stApp{background-color:#0B0F1A;}section[data-testid='stSidebar']{background-color:#111827;border-right:1px solid #1E2E47;}</style>", unsafe_allow_html=True)

ASSETS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

st.title("🤖 Machine Learning Models")
st.caption("CRISP-DM Phases: Modelling → Evaluation | RO1 & RO3")

df1, df2, df1_full, df1_eff = load_data()

with st.spinner("Training 4 models on 7,902 samples (this runs once, then is cached)…"):
    results, y_test, SELECTED, models = train_models(df1_eff)

MODEL_COLORS = [BLUE, ACCENT, AMBER, PURPLE]
model_names  = list(results.keys())

# ── Model summary cards ───────────────────────────────────────────────────────
st.markdown("### Model Performance Summary")
cols = st.columns(4)
best_r2 = max(v["r2"] for v in results.values())
for i, (name, res) in enumerate(results.items()):
    with cols[i]:
        is_best = res["r2"] == best_r2
        border  = MODEL_COLORS[i]
        badge   = " 🥇 BEST" if is_best else ""
        st.markdown(f"""<div style='background:{SURF};border:1px solid {border};
            border-top:3px solid {border};padding:1rem;margin-bottom:.5rem'>
            <div style='font-family:Space Mono,monospace;font-size:.58rem;color:{MUTED};
                letter-spacing:.1em;text-transform:uppercase'>{name}{badge}</div>
            <div style='font-size:1.7rem;font-weight:800;color:{border};margin:.3rem 0'>
                {res["r2"]}</div>
            <div style='font-family:Space Mono,monospace;font-size:.6rem;color:{MUTED}'>R² Score</div>
            <div style='margin-top:.6rem;font-family:Space Mono,monospace;font-size:.62rem'>
                <span style='color:{MUTED}'>MAE  </span><span style='color:{TEXT}'>{res["mae"]}</span><br>
                <span style='color:{MUTED}'>RMSE </span><span style='color:{TEXT}'>{res["rmse"]}</span><br>
                <span style='color:{MUTED}'>CV μ </span><span style='color:{TEXT}'>{res["cv_mean"]}</span><br>
                <span style='color:{MUTED}'>CV σ </span><span style='color:{TEXT}'>{res["cv_std"]}</span>
            </div></div>""", unsafe_allow_html=True)

st.markdown("---")

# ── R² and error charts ───────────────────────────────────────────────────────
c1, c2 = st.columns(2)
with c1:
    r2_vals = [results[n]["r2"] for n in model_names]
    fig = go.Figure(go.Bar(
        x=model_names, y=r2_vals,
        marker_color=[c + "BB" for c in MODEL_COLORS],
        marker_line_color=MODEL_COLORS, marker_line_width=2,
        text=[str(v) for v in r2_vals], textposition="outside",
    ))
    apply_layout(fig, "R² Score Comparison (Higher = Better)", 320)
    fig.update_layout(yaxis=dict(range=[0.85, 1.0], gridcolor=BORDER), xaxis=dict(gridcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(name="MAE", x=model_names,
        y=[results[n]["mae"] for n in model_names],
        marker_color=[c + "99" for c in MODEL_COLORS],
        marker_line_color=MODEL_COLORS, marker_line_width=1.5))
    fig2.add_trace(go.Bar(name="RMSE", x=model_names,
        y=[results[n]["rmse"] for n in model_names],
        marker_color=[c + "44" for c in MODEL_COLORS],
        marker_line_color=MODEL_COLORS, marker_line_width=1.5))
    apply_layout(fig2, "MAE & RMSE (km/L) — Lower = Better", 320)
    fig2.update_layout(barmode="group", showlegend=True,
                       xaxis=dict(gridcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig2, use_container_width=True)

# ── Actual vs predicted scatter ───────────────────────────────────────────────
c3, c4 = st.columns(2)
with c3:
    yp_gbm = results["Gradient Boosting"]["y_pred"]
    sample  = min(400, len(y_test))
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=y_test[:sample], y=yp_gbm[:sample], mode="markers",
        marker=dict(color=ACCENT, size=5, opacity=0.35, line=dict(width=0)),
        name="Trip predictions",
        hovertemplate="Actual: %{x:.2f}<br>Predicted: %{y:.2f}<extra></extra>"))
    lim = [min(y_test.min(), yp_gbm.min()), max(y_test.max(), yp_gbm.max())]
    fig3.add_trace(go.Scatter(x=lim, y=lim, mode="lines",
        line=dict(color="white", width=1.5, dash="dash"), name="Perfect prediction"))
    apply_layout(fig3, f"GBM: Actual vs Predicted (R²={results['Gradient Boosting']['r2']})", 340)
    fig3.update_layout(showlegend=True,
        xaxis_title="Actual (km/L)", yaxis_title="Predicted (km/L)")
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    # Feature importance (GBM)
    gbm_model = models["Gradient Boosting"]
    imp = gbm_model.feature_importances_
    order = np.argsort(imp)
    fig4 = go.Figure(go.Bar(
        x=imp[order], y=[SELECTED[i] for i in order],
        orientation="h",
        marker_color=[ACCENT, BLUE, AMBER, RED, PURPLE, "#F5F53D"][:len(SELECTED)],
        text=[f"{v:.3f}" for v in imp[order]], textposition="outside",
    ))
    apply_layout(fig4, "GBM Feature Importance (RO2: Key Factors)", 340)
    fig4.update_layout(xaxis=dict(gridcolor=BORDER), yaxis=dict(gridcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig4, use_container_width=True)

# ── NB2 figures gallery ───────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### Notebook 2 Figures")
for key, title in [
    ("fig2_1_feature_selection",  "Fig 2.1 — Feature Selection (Filter + RFE Wrapper)"),
    ("fig2_2_model_evaluation",   "Fig 2.2 — Full Model Evaluation Dashboard"),
    ("fig2_3_feature_importance", "Fig 2.3 — Feature Importance Across All 3 Models"),
    ("fig2_4_learning_curves",    "Fig 2.4 — Learning Curves: Bias-Variance Assessment"),
    ("fig2_5_results_table",      "Fig 2.5 — Model Performance Summary Table"),
]:
    with st.expander(f"**{title}**"):
        path = os.path.join(ASSETS, f"{key}.png")
        if os.path.exists(path):
            st.image(Image.open(path), use_container_width=True)
