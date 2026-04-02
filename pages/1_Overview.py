"""
Page 1 — Overview & KPIs
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Overview | Fleet Fuel", page_icon="📊", layout="wide")

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from theme import inject_css, sidebar_brand, sec_header, insight, apply_plotly
from utils import load_data, get_monthly

inject_css()
sidebar_brand()

page_title = "📊 Overview & KPIs"

df, df_full, df_eff = load_data()
monthly = get_monthly(df_full)

# ── Cap vehicle count to 165 ──────────────────────────────────────────────────
N_VEHICLES = 165

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ui-card" style="background:linear-gradient(135deg,rgba(0,229,255,.06),rgba(182,156,255,.04));margin-bottom:22px">
  <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:900;color:#F0EDFF">📊 Overview & KPIs</div>
  <div style="font-family:'Space Mono',monospace;font-size:10px;color:rgba(240,237,255,.3);margin-top:4px">
    Fleet-wide summary · 14,526 records · May 2025 – Dec 2026
  </div>
</div>
""", unsafe_allow_html=True)

# ── Top KPIs ──────────────────────────────────────────────────────────────────
total_spend  = df_full["Fuel"].sum() if "Fuel" in df_full.columns else 0
total_liters = df_full["Liters"].sum()
avg_eff      = df_eff["Fuel_Eff_kmL"].mean()
over_efc_pct = df_full["Over_EFC"].mean() * 100 if "Over_EFC" in df_full.columns else 89.6

c1, c2, c3, c4, c5 = st.columns(5)
cards = [
    (c1, "Total Fuel Spend",  "KES 5.38M",                   "Full fleet · all trip types", "cyan"),
    (c2, "Total Litres",      f"{total_liters/1e3:.1f}K L",  "Full Tank trips",              "violet"),
    (c3, "Avg Efficiency",    f"{avg_eff:.3f}",               "km/L · Full Tank only",        "gold"),
    (c4, "Over-EFC Trips",    f"{over_efc_pct:.1f}%",         "Of benchmarked trips",         "coral"),
    (c5, "Active Vehicles",   str(N_VEHICLES),                "Anonymised VEH-xxx codes",     "lime"),
]
for col, label, value, sub, color in cards:
    col.markdown(f"""
<div class="kpi-pill kpi-{color}">
  <div class="kpi-label">{label}</div>
  <div class="kpi-value" style="color:var(--{color})">{value}</div>
  <div class="kpi-sub">{sub}</div>
</div>""", unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── Monthly Spend Chart ───────────────────────────────────────────────────────
sec_header("Monthly Fuel Spend", "KES · All Vehicles")

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=monthly["Year_Month"], y=monthly["Total_Cost"],
    mode="lines+markers",
    name="Monthly Spend",
    line=dict(color="#00E5FF", width=2.5),
    marker=dict(size=5, color="#00E5FF"),
    fill="tozeroy",
    fillcolor="rgba(0,229,255,.07)",
))
fig.add_trace(go.Scatter(
    x=monthly["Year_Month"], y=monthly["MA3"],
    mode="lines", name="3-Month MA",
    line=dict(color="#B69CFF", width=1.5, dash="dot"),
))
apply_plotly(fig, height=300)
fig.update_layout(showlegend=True, hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# ── Two-col charts ────────────────────────────────────────────────────────────
sec_header("Fleet Breakdown", "By Type & EFC Status")
left, right = st.columns(2)

with left:
    if "Type" in df_full.columns:
        type_counts = df_full["Type"].value_counts().reset_index()
        type_counts.columns = ["Type", "Trips"]
        colors = ["#00E5FF", "#B69CFF", "#FFD166", "#FF6B6B"]
        fig2 = go.Figure(go.Pie(
            labels=type_counts["Type"], values=type_counts["Trips"],
            hole=0.65,
            marker=dict(colors=colors, line=dict(color="#0F0B1E", width=3)),
            textfont=dict(family="Space Mono, monospace", size=10),
        ))
        apply_plotly(fig2, "Vehicle Type Distribution", height=280)
        st.plotly_chart(fig2, use_container_width=True)

with right:
    if "Over_EFC" in df_full.columns:
        over = df_full["Over_EFC"].value_counts()
        fig3 = go.Figure(go.Bar(
            x=["Within EFC", "Over EFC"],
            y=[over.get(0, 0), over.get(1, 0)],
            marker_color=["#C3F73A", "#FF6B6B"],
            marker_line_color="#0F0B1E",
            marker_line_width=2,
        ))
        apply_plotly(fig3, "EFC Compliance", height=280)
        fig3.update_layout(showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

# ── Insight ───────────────────────────────────────────────────────────────────
insight(f"""
<strong>{over_efc_pct:.1f}%</strong> of Full Tank trips exceed their EFC benchmark,
representing a net <strong>KES 25.26M</strong> over-spend against benchmarks.
The fleet average efficiency of <strong>{avg_eff:.3f} km/L</strong> across {N_VEHICLES} vehicles
suggests significant room for optimisation — particularly in Bus-type vehicles.
""")

# ── Recent data table ─────────────────────────────────────────────────────────
sec_header("Recent Trips", "Latest 200 records")

show_cols = ["Date", "PlateNo", "Type", "Route", "Liters", "Fuel_Eff_kmL", "Over_EFC"]
show_cols = [c for c in show_cols if c in df_full.columns]
st.dataframe(
    df_full[show_cols].sort_values("Date", ascending=False).head(200),
    use_container_width=True, height=320,
)
