"""
Page 7 — Deployment & Savings
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import os, glob

st.set_page_config(page_title="Deployment | Fleet Fuel", page_icon="🎯", layout="wide")

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from theme import inject_css, sidebar_brand, sec_header, insight, apply_plotly
from utils import load_data, get_vehicle_scores, get_savings, display_df

inject_css()
sidebar_brand()

df, df_full, df_eff = load_data()
vp = get_vehicle_scores(df_eff)
sav_vp, monthly_sav, annual_sav, type_q3 = get_savings(df_eff, df_full, vp)

st.markdown("""
<div class="ui-card" style="background:linear-gradient(135deg,rgba(255,107,107,.06),rgba(195,247,58,.04));margin-bottom:22px">
  <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:900;color:#F0EDFF">🚀 Deployment & Savings</div>
  <div style="font-family:'Space Mono',monospace;font-size:10px;color:rgba(240,237,255,.3);margin-top:4px">
    Savings model · Intervention roadmap · Research objective summary
  </div>
</div>
""", unsafe_allow_html=True)

# ── Savings KPIs ──────────────────────────────────────────────────────────────
c1,c2,c3,c4 = st.columns(4)
kpis = [
    (c1, "Annual Savings Potential", f"KES {annual_sav/1e6:.2f}M",  "Q3 target · all vehicle types", "lime"),
    (c2, "Monthly Savings",          f"KES {monthly_sav/1e3:.0f}K", "If Q3 targets met now",          "cyan"),
    (c3, "Net Over-Spend vs EFC",    "KES 25.26M",                  "Across all Full Tank trips",     "coral"),
    (c4, "% Recoverable",            f"{annual_sav/25.26e6*100:.0f}%","Of total over-EFC spend",      "violet"),
]
for col, label, val, sub, color in kpis:
    col.markdown(f"""
<div class="kpi-pill kpi-{color}">
  <div class="kpi-label">{label}</div>
  <div class="kpi-value" style="color:var(--{color})">{val}</div>
  <div class="kpi-sub">{sub}</div>
</div>""", unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── Savings callout banner ─────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(90deg,rgba(195,247,58,.1),rgba(0,229,255,.07));
  border:1px solid rgba(195,247,58,.3);border-radius:16px;
  padding:26px 32px;display:flex;align-items:center;gap:24px;margin-bottom:24px">
  <span style="font-size:42px;flex-shrink:0">💰</span>
  <div style="flex:1">
    <div style="font-family:'Outfit',sans-serif;font-size:20px;font-weight:900;
      color:#F0EDFF;margin-bottom:6px">
      KES {annual_sav/1e6:.2f}M in Annual Recoverable Savings
    </div>
    <div style="font-size:13px;color:rgba(240,237,255,.45);line-height:1.65;max-width:700px">
      Achieved by bringing underperforming vehicles to the <strong style="color:#F0EDFF">within-type Q3 efficiency benchmark</strong>.
      This requires no capital investment — only operational discipline: driver behaviour,
      maintenance schedules, and route optimisation.
    </div>
  </div>
  <div style="text-align:right;flex-shrink:0">
    <div style="font-family:'Outfit',sans-serif;font-size:40px;font-weight:900;
      color:#C3F73A;letter-spacing:-.04em">KES {annual_sav/1e6:.2f}M</div>
    <div style="font-family:'Space Mono',monospace;font-size:9px;
      color:rgba(240,237,255,.3);margin-top:3px">per year</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Type Q3 targets ────────────────────────────────────────────────────────────
sec_header("Q3 Efficiency Targets by Vehicle Type", "Benchmark for savings model")

types    = list(type_q3.keys())
targets  = [type_q3[t] for t in types]
actuals  = [df_eff[df_eff["Type"]==t]["Fuel_Eff_kmL"].mean() for t in types]
colors   = ["#FF6B6B","#74B9FF","#FFD166","#B69CFF"]

fig = go.Figure()
fig.add_trace(go.Bar(
    name="Actual Avg (km/L)", x=types, y=actuals,
    marker_color=["rgba(255,107,107,0.8)","rgba(116,185,255,0.8)","rgba(255,209,102,0.8)","rgba(182,156,255,0.8)"],
    marker_line_color="#0F0B1E", marker_line_width=2,
))
fig.add_trace(go.Bar(
    name="Q3 Target (km/L)", x=types, y=targets,
    marker_color="rgba(195,247,58,.45)",
    marker_line_color="#0F0B1E", marker_line_width=2,
    marker_pattern_shape="/",
))
apply_plotly(fig, "Actual Efficiency vs Q3 Benchmark by Vehicle Type", height=320)
fig.update_layout(barmode="group", bargap=0.25)
st.plotly_chart(fig, use_container_width=True)

# ── Savings waterfall by type ─────────────────────────────────────────────────
sec_header("Savings Breakdown by Type", "Monthly KES recovery estimate")

type_savings = sav_vp.groupby("Type")["Monthly_KES"].sum().sort_values(ascending=False)

fig2 = go.Figure(go.Bar(
    x=type_savings.index,
    y=type_savings.values / 1e3,
    marker_color=["#C3F73A","#00E5FF","#FFD166","#B69CFF"],
    marker_line_color="#0F0B1E", marker_line_width=2,
    text=[f"KES {v/1e3:.0f}K" for v in type_savings.values],
    textposition="outside",
    textfont=dict(family="Space Mono, monospace", size=10, color="#F0EDFF"),
))
apply_plotly(fig2, "Monthly Savings Potential by Vehicle Type (KES '000)", height=300)
fig2.update_layout(showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

# ── Intervention roadmap ───────────────────────────────────────────────────────
sec_header("Intervention Roadmap", "Priority actions")

interventions = [
    ("🔴", "Immediate",  "1–2 weeks",  "#FF6B6B",
     "Flag Grade-D vehicles for urgent maintenance review. "
     "Target the bottom 10 by efficiency score — these account for ~40% of recoverable savings."),
    ("🟡", "Short-term", "1–3 months", "#FFD166",
     "Deploy driver coaching for vehicles with consistent over-EFC patterns. "
     "Review petrol station allocations for cost/litre outliers."),
    ("🟢", "Medium-term","3–6 months", "#C3F73A",
     "Implement route re-assignment: move fuel-efficient vehicles to high-mileage routes. "
     "Adopt anomaly flagging from the Isolation Forest model in fleet management system."),
    ("🔵", "Ongoing",    "Continuous", "#74B9FF",
     "Monthly model re-training as new trip data accumulates. "
     "Track KPI dashboards weekly to confirm savings trajectory."),
]

for icon, phase, timeline, color, desc in interventions:
    st.markdown(f"""
<div class="ui-card" style="display:flex;gap:16px;align-items:flex-start;
  border-left:3px solid {color};padding-left:18px">
  <span style="font-size:20px;flex-shrink:0;margin-top:2px">{icon}</span>
  <div style="flex:1">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px">
      <div style="font-family:'Outfit',sans-serif;font-size:13px;font-weight:800;
        color:#F0EDFF">{phase}</div>
      <div style="font-family:'Space Mono',monospace;font-size:9px;
        color:{color};background:{color}18;border:1px solid {color}44;
        padding:2px 8px;border-radius:20px">{timeline}</div>
    </div>
    <div style="font-size:12px;color:rgba(240,237,255,.5);line-height:1.6">{desc}</div>
  </div>
</div>""", unsafe_allow_html=True)

# ── Research objective summary table ──────────────────────────────────────────
sec_header("Research Objective Summary", "CRISP-DM outcomes")

ros = [
    ("RO1", "Predict fuel consumption",
     "Gradient Boosting Regressor", "R² = 0.9904", "NB2 §9", "Modelling"),
    ("RO2", "Identify inefficient vehicles",
     "Within-type scoring + Grade A–D", "89.6% over-EFC", "NB3 §4", "Evaluation"),
    ("RO3", "Quantify recoverable savings",
     "Q3-gap savings model", f"KES {annual_sav/1e6:.2f}M/year", "NB3 §6", "Deployment"),
]

rows_html = ""
for ro, obj, method, result, notebook, phase in ros:
    rows_html += f"""
<tr>
  <td style="font-family:'Space Mono',monospace;font-size:10px;color:#00E5FF;white-space:nowrap">{ro}</td>
  <td style="font-size:12px;color:#F0EDFF">{obj}</td>
  <td style="font-size:11px;color:rgba(240,237,255,.5)">{method}</td>
  <td style="font-family:'Space Mono',monospace;font-size:11px;color:#C3F73A;font-weight:700">{result}</td>
  <td style="font-family:'Space Mono',monospace;font-size:10px;color:rgba(240,237,255,.3)">{notebook}</td>
  <td style="font-size:11px;color:#B69CFF">{phase}</td>
</tr>"""

st.markdown(f"""
<div style="background:#1A1530;border:1px solid rgba(255,255,255,.08);border-radius:14px;
  overflow:hidden;margin-bottom:20px">
  <table style="width:100%;border-collapse:collapse">
    <thead>
      <tr style="border-bottom:1px solid rgba(255,255,255,.08)">
        <th style="font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.1em;
          text-transform:uppercase;color:rgba(240,237,255,.3);padding:12px 20px;text-align:left">RO</th>
        <th style="font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.1em;
          text-transform:uppercase;color:rgba(240,237,255,.3);padding:12px 20px;text-align:left">Objective</th>
        <th style="font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.1em;
          text-transform:uppercase;color:rgba(240,237,255,.3);padding:12px 20px;text-align:left">Method</th>
        <th style="font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.1em;
          text-transform:uppercase;color:rgba(240,237,255,.3);padding:12px 20px;text-align:left">Result</th>
        <th style="font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.1em;
          text-transform:uppercase;color:rgba(240,237,255,.3);padding:12px 20px;text-align:left">Notebook</th>
        <th style="font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.1em;
          text-transform:uppercase;color:rgba(240,237,255,.3);padding:12px 20px;text-align:left">CRISP-DM</th>
      </tr>
    </thead>
    <tbody>{rows_html}</tbody>
  </table>
</div>
""", unsafe_allow_html=True)

# ── NB3 figures ───────────────────────────────────────────────────────────────
asset_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
nb3_imgs  = sorted(glob.glob(os.path.join(asset_dir, "nb3_*.png")))

if nb3_imgs:
    sec_header("NB3 Deployment Figures", f"{len(nb3_imgs)} charts")
    cols = st.columns(2)
    for i, img in enumerate(nb3_imgs):
        with cols[i % 2]:
            st.markdown(f"""
<div class="ui-card" style="padding:12px">
  <div style="font-family:'Space Mono',monospace;font-size:9px;
    color:rgba(240,237,255,.3);margin-bottom:6px">{os.path.basename(img)}</div>""",
            unsafe_allow_html=True)
            st.image(img, use_column_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

insight(f"""
The savings model applies to vehicles with a positive efficiency gap vs their within-type Q3 target.
Annual potential: <strong>KES {annual_sav/1e6:.2f}M</strong>.
This is conservative — it assumes only underperformers reach Q3, not the median or above.
A more aggressive target (e.g., Q2 or mean) would yield higher but riskier estimates.
""")
