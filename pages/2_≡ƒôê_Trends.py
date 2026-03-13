"""Page 2 — Monthly Trends"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import (load_data, get_monthly, ACCENT, BLUE, AMBER, RED, PURPLE,
                   BG, SURF, BORDER, TEXT, MUTED, apply_layout)

st.set_page_config(page_title="Trends · Fleet Fuel", page_icon="📈", layout="wide")
st.markdown("<style>.stApp{background-color:#0B0F1A;}section[data-testid='stSidebar']{background-color:#111827;border-right:1px solid #1E2E47;}</style>", unsafe_allow_html=True)

st.title("📈 Monthly Trends")
st.caption("May 2025 – Dec 2026 · Red-shaded = Nov 2025–Jan 2026 operational volume spike (×10–20 trips)")

df1, df2, df1_full, df1_eff = load_data()
monthly = get_monthly(df1_full)
xl = monthly["Year_Month"].tolist()
spike_idx = monthly[monthly["Is_Spike"]].index.tolist()

def spike_shapes():
    shapes = []
    for i in spike_idx:
        shapes.append(dict(type="rect", xref="x", yref="paper",
            x0=xl[i-1] if i > 0 else xl[i], x1=xl[i],
            y0=0, y1=1, fillcolor="rgba(255,77,109,0.07)", line_width=0))
    return shapes

# ── Total cost ───────────────────────────────────────────────────────────────
fig1 = go.Figure()
bar_colors = [RED if s else BLUE for s in monthly["Is_Spike"]]
fig1.add_trace(go.Bar(x=xl, y=monthly["Total_Cost"]/1e6, name="Monthly Spend",
    marker_color=bar_colors, hovertemplate="%{x}: KES %{y:.2f}M<extra></extra>"))
fig1.add_trace(go.Scatter(x=xl, y=monthly["MA3"]/1e6, mode="lines",
    line=dict(color=ACCENT, width=2.5), name="3-Month MA"))
fig1.add_trace(go.Scatter(x=xl, y=monthly["Trend"]/1e6, mode="lines",
    line=dict(color=AMBER, width=1.5, dash="dash"), name="Linear Trend"))
apply_layout(fig1, "Total Monthly Fuel Expenditure (KES) with 3-Month MA & Trend", 340)
fig1.update_layout(showlegend=True, shapes=spike_shapes(),
    yaxis_tickprefix="KES ", yaxis_ticksuffix="M", xaxis_tickangle=-45)
st.plotly_chart(fig1, width='stretch')

# ── MoM change + Litres per Trip ─────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    mom = monthly["MoM"].fillna(0)
    fig2 = go.Figure(go.Bar(
        x=xl, y=mom,
        marker_color=[ACCENT if v >= 0 else RED for v in mom],
        hovertemplate="%{x}: %{y:.1f}%<extra></extra>",
    ))
    fig2.add_hline(y=0, line_color="white", line_width=1, line_dash="dash")
    apply_layout(fig2, "Month-on-Month % Change in Total Litres", 300)
    fig2.update_layout(yaxis_ticksuffix="%", xaxis_tickangle=-45)
    st.plotly_chart(fig2, width='stretch')

with c2:
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=xl, y=monthly["LPT"], mode="lines+markers",
        line=dict(color=BLUE, width=2),
        marker=dict(color=BLUE, size=5),
        fill="tozeroy", fillcolor="rgba(56,182,255,0.07)",
        hovertemplate="%{x}: %{y:.1f} L/trip<extra></extra>"))
    apply_layout(fig3, "Litres per Trip (Efficiency Signal)", 300)
    fig3.update_layout(yaxis_ticksuffix=" L", xaxis_tickangle=-45, shapes=spike_shapes())
    st.plotly_chart(fig3, width='stretch')

# ── Trip volume + Efficiency trend ───────────────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    bar_c2 = [AMBER if s else PURPLE for s in monthly["Is_Spike"]]
    fig4 = go.Figure(go.Bar(x=xl, y=monthly["Trips"], marker_color=bar_c2,
        hovertemplate="%{x}: %{y:,} trips<extra></extra>"))
    apply_layout(fig4, "Monthly Trip Volume (Amber = Spike months)", 300)
    fig4.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig4, width='stretch')

with c4:
    ed = monthly["Avg_Eff_f"].values
    mn = monthly["Month_num"].values
    coef = np.polyfit(mn, ed, 1)
    et   = np.polyval(coef, mn)
    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(x=xl, y=ed, mode="lines+markers",
        line=dict(color=PURPLE, width=2),
        marker=dict(color=PURPLE, size=5),
        fill="tozeroy", fillcolor="rgba(192,132,252,0.07)",
        hovertemplate="%{x}: %{y:.3f} km/L<extra></extra>", name="Avg Eff."))
    fig5.add_trace(go.Scatter(x=xl, y=et, mode="lines",
        line=dict(color=AMBER, width=1.5, dash="dot"),
        name=f"Trend: {coef[0]:+.3f} km/L/mo"))
    apply_layout(fig5, "Average Monthly Efficiency (km/L) & Trend", 300)
    fig5.update_layout(showlegend=True, yaxis_ticksuffix=" km/L",
                       xaxis_tickangle=-45, shapes=spike_shapes())
    st.plotly_chart(fig5, width='stretch')

st.info(f"📌 **Nov 2025–Jan 2026 spike:** Trip volume increased ×10–20. "
        f"Efficiency signal remains stable at ~{ed.mean():.2f} km/L, "
        f"confirming the scale event is operational (genuine trips), not data noise.")
