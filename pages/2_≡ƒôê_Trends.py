"""
Page 2 — Trends
"""
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Trends | Fleet Fuel", page_icon="📈", layout="wide")

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from theme import inject_css, sidebar_brand, sec_header, insight, apply_plotly
from utils import load_data, get_monthly

inject_css()
sidebar_brand()

df, df_full, df_eff = load_data()
monthly = get_monthly(df_full)

st.markdown("""
<div class="ui-card" style="background:linear-gradient(135deg,rgba(116,185,255,.06),rgba(0,229,255,.04));margin-bottom:22px">
  <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:900;color:#F0EDFF">📈 Trends</div>
  <div style="font-family:'Space Mono',monospace;font-size:10px;color:rgba(240,237,255,.3);margin-top:4px">
    Monthly cost, volume &amp; efficiency trends · Full Tank trips only
  </div>
</div>
""", unsafe_allow_html=True)

# ── Controls ──────────────────────────────────────────────────────────────────
c1, c2 = st.columns([3, 1])
with c2:
    show_spikes = st.checkbox("Highlight spend spikes", value=True)

# ── Spend + MA chart ──────────────────────────────────────────────────────────
sec_header("Monthly Fuel Cost", "KES · 3-Month Moving Average")

fig = go.Figure()
if show_spikes:
    spikes = monthly[monthly["Is_Spike"] == True]
    fig.add_trace(go.Scatter(
        x=spikes["Year_Month"], y=spikes["Total_Cost"],
        mode="markers", name="Spike",
        marker=dict(size=12, color="#FF6B6B", symbol="diamond",
                    line=dict(color="#08060F", width=2)),
    ))
fig.add_trace(go.Scatter(
    x=monthly["Year_Month"], y=monthly["Total_Cost"],
    mode="lines+markers", name="Monthly Cost",
    line=dict(color="#00E5FF", width=2.5),
    marker=dict(size=5), fill="tozeroy", fillcolor="rgba(0,229,255,.06)",
))
fig.add_trace(go.Scatter(
    x=monthly["Year_Month"], y=monthly["MA3"],
    mode="lines", name="3-Month MA",
    line=dict(color="#B69CFF", width=1.5, dash="dot"),
))
fig.add_trace(go.Scatter(
    x=monthly["Year_Month"], y=monthly["Trend"],
    mode="lines", name="Trend",
    line=dict(color="#FFD166", width=1, dash="dash"),
))
apply_plotly(fig, height=320)
fig.update_layout(hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# ── MoM + LPT ─────────────────────────────────────────────────────────────────
sec_header("Month-on-Month Change & Litres per Trip", "Dual Metrics")

left, right = st.columns(2)

with left:
    fig2 = go.Figure(go.Bar(
        x=monthly["Year_Month"],
        y=monthly["MoM"].fillna(0),
        marker_color=monthly["MoM"].apply(
            lambda v: "rgba(255,107,107,.8)" if v > 0 else "rgba(195,247,58,.8)"
        ),
        name="MoM %",
    ))
    apply_plotly(fig2, "Month-on-Month Volume Change (%)", height=280)
    fig2.update_layout(showlegend=False)
    fig2.add_hline(y=0, line_color="rgba(255,255,255,.2)", line_width=1)
    st.plotly_chart(fig2, use_container_width=True)

with right:
    fig3 = go.Figure(go.Scatter(
        x=monthly["Year_Month"], y=monthly["LPT"],
        mode="lines+markers", name="Litres/Trip",
        line=dict(color="#FFD166", width=2),
        marker=dict(size=5, color="#FFD166"),
        fill="tozeroy", fillcolor="rgba(255,209,102,.06)",
    ))
    apply_plotly(fig3, "Average Litres per Trip", height=280)
    st.plotly_chart(fig3, use_container_width=True)

# ── Efficiency trend ──────────────────────────────────────────────────────────
sec_header("Efficiency Trend", "km/L · Monthly Average")

fig4 = go.Figure()
fig4.add_trace(go.Scatter(
    x=monthly["Year_Month"], y=monthly["Avg_Eff_f"],
    mode="lines+markers", name="Avg Efficiency",
    line=dict(color="#C3F73A", width=2.5),
    marker=dict(size=5, color="#C3F73A"),
    fill="tozeroy", fillcolor="rgba(195,247,58,.06)",
))
fleet_mean = monthly["Avg_Eff_f"].mean()
fig4.add_hline(y=fleet_mean, line_color="rgba(255,209,102,.5)",
               line_dash="dot", annotation_text=f"Fleet mean {fleet_mean:.2f} km/L",
               annotation_font_color="#FFD166")
apply_plotly(fig4, height=280)
st.plotly_chart(fig4, use_container_width=True)

insight(f"""
The fleet's average efficiency shows a trend of <strong>{monthly['Avg_Eff_f'].iloc[-1]:.2f} km/L</strong>
in the most recent month vs a fleet mean of <strong>{fleet_mean:.2f} km/L</strong>.
Month-on-month volume swings of more than 10% are flagged as spikes — these often correlate
with route changes or seasonal operations. The 3-month moving average smooths short-term noise
to reveal the underlying cost trajectory.
""")
