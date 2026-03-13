"""Page 1 — Overview & KPIs"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import (load_data, get_monthly, get_vehicle_scores, get_route_scores,
                   get_anomalies, get_savings, PALETTE, TYPE_COLORS,
                   ACCENT, BLUE, AMBER, RED, PURPLE, BG, SURF, BORDER, TEXT, MUTED,
                   PLOTLY_LAYOUT, apply_layout)

st.set_page_config(page_title="Overview · Fleet Fuel", page_icon="📊", layout="wide")
st.markdown("""<style>.stApp{background-color:#0B0F1A;}
section[data-testid="stSidebar"]{background-color:#111827;border-right:1px solid #1E2E47;}
.kpi-card{background:#111827;border:1px solid #1E2E47;padding:1.1rem 1.3rem;}
.kpi-label{font-family:'Space Mono',monospace;font-size:.58rem;color:#6B7E99;letter-spacing:.1em;text-transform:uppercase;margin-bottom:.3rem;}
.kpi-value{font-size:1.8rem;font-weight:800;line-height:1;letter-spacing:-.03em;}
.kpi-unit{font-family:'Space Mono',monospace;font-size:.6rem;color:#6B7E99;margin-top:.25rem;}
</style>""", unsafe_allow_html=True)

st.title("📊 Overview & KPIs")
st.caption("Full dataset summary — May 2025 to Dec 2026 · All VEH-/DRV- codes are anonymised")

df1, df2, df1_full, df1_eff = load_data()
monthly  = get_monthly(df1_full)
vp       = get_vehicle_scores(df1_eff)
ra       = get_route_scores(df1_eff)
anom_df  = get_anomalies(df1_eff)
vp2, monthly_sav, annual_sav, _ = get_savings(df1_eff, df1_full, vp)

n_anom      = int(anom_df["Is_Anomaly"].sum())
fleet_avg   = df1_eff["Fuel Efficiency (km/l)"].mean()
total_spend = df1_full["Fuel Amount"].sum()
net_kes     = df1_eff["KES Saved/Excess"].sum()
over_pct    = (df1_eff["Fuel Excess/Saved"] < 0).mean() * 100
cpk         = (df1_eff["Fuel Amount"] / df1_eff["Mileage"].replace(0, float("nan"))).median()

# ── KPI Row 1 ────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("⛽ Total Fuel Spend",    f"KES {total_spend/1e6:.2f}M", "Full Tank trips")
c2.metric("💧 Total Litres",        f"{df1_full['Liters'].sum()/1000:.1f}K L", "Dispensed")
c3.metric("📏 Fleet Avg Efficiency",f"{fleet_avg:.3f} km/L", "Full Tank + odometer")
c4.metric("⚠️ Over-Consumption",    f"{over_pct:.1f}%", "Trips exceeding EFC benchmark", delta_color="inverse")

st.markdown("")
c5, c6, c7, c8 = st.columns(4)
c5.metric("🚗 Fleet Size",      str(df1["PlateNo"].nunique()),      "Anonymised VEH codes")
c6.metric("🛣 Full Tank Trips", f"{len(df1_full):,}",               "Efficiency basis")
c7.metric("💰 Cost per km",     f"KES {cpk:.2f}",                   "Median all trips")
c8.metric("🔍 Anomalies",       str(n_anom),                         "Isolation Forest 5%", delta_color="inverse")

st.markdown("---")

# ── Charts Row ───────────────────────────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    type_stats = df1_eff.groupby("Type")["Fuel Efficiency (km/l)"].mean().reset_index()
    colors = [TYPE_COLORS.get(t, BLUE) for t in type_stats["Type"]]
    fig = go.Figure(go.Bar(
        x=type_stats["Type"], y=type_stats["Fuel Efficiency (km/l)"].round(3),
        marker_color=colors, marker_line_color=colors, marker_line_width=1.5,
        text=type_stats["Fuel Efficiency (km/l)"].round(2).astype(str) + " km/L",
        textposition="outside",
    ))
    apply_layout(fig, "Avg Fuel Efficiency by Vehicle Type (km/L)", 300)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    type_spend = df1_full.groupby("Type")["Fuel Amount"].sum() / 1e6
    fig2 = go.Figure(go.Pie(
        labels=type_spend.index.tolist(),
        values=type_spend.values.round(2),
        hole=0.45,
        marker=dict(colors=[TYPE_COLORS.get(t, BLUE) for t in type_spend.index],
                    line=dict(color=BG, width=2)),
        textinfo="label+percent",
        hovertemplate="%{label}: KES %{value}M<extra></extra>",
    ))
    apply_layout(fig2, "Total Spend Distribution (KES Millions)", 300)
    st.plotly_chart(fig2, use_container_width=True)

# ── EFC Compliance + Monthly sparkline ───────────────────────────────────────
col_c, col_d = st.columns([1, 2])

with col_c:
    st.markdown("#### EFC Compliance")
    under = 100 - over_pct
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(name="Over EFC",    x=["Fleet"], y=[over_pct],  marker_color=RED,   text=[f"{over_pct:.1f}%"],  textposition="inside"))
    fig3.add_trace(go.Bar(name="Within EFC",  x=["Fleet"], y=[under],     marker_color=ACCENT, text=[f"{under:.1f}%"], textposition="inside"))
    fig3.update_layout(barmode="stack", **PLOTLY_LAYOUT, height=240, showlegend=True,
                       yaxis=dict(range=[0,100], gridcolor=BORDER, ticksuffix="%"),
                       xaxis=dict(gridcolor="rgba(0,0,0,0)"),
                       legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown(f"""<div style='font-family:Space Mono,monospace;font-size:.62rem;color:{MUTED}'>
    Net position: <span style='color:{RED}'>KES {abs(net_kes/1e6):.2f}M over-spent</span></div>""",
    unsafe_allow_html=True)

with col_d:
    fig4 = go.Figure()
    spike_colors = [RED if s else BLUE for s in monthly["Is_Spike"]]
    fig4.add_trace(go.Bar(x=monthly["Year_Month"], y=monthly["Total_Cost"]/1e6,
                          marker_color=spike_colors, name="Monthly Spend",
                          hovertemplate="%{x}: KES %{y:.2f}M<extra></extra>"))
    ma = monthly["MA3"] / 1e6
    fig4.add_trace(go.Scatter(x=monthly["Year_Month"], y=ma, mode="lines",
                              line=dict(color=ACCENT, width=2), name="3-Month MA"))
    apply_layout(fig4, "Monthly Fuel Cost with 3-Month MA (Red = Spike months)", 300)
    fig4.update_layout(showlegend=True, yaxis_tickprefix="KES ", yaxis_ticksuffix="M",
                       xaxis_tickangle=-45)
    st.plotly_chart(fig4, use_container_width=True)

# ── Summary stats table ───────────────────────────────────────────────────────
st.markdown("---")
st.markdown("#### Quick Dataset Summary")
summ = df1_eff[["Liters","Fuel Amount","Mileage","Fuel Efficiency (km/l)",
                 "Fuel Excess/Saved","KES Saved/Excess"]].describe().T.round(2)
summ.columns = ["Count","Mean","Std Dev","Min","Q1","Median","Q3","Max"]
summ["Count"] = summ["Count"].astype(int)
st.dataframe(summ, use_container_width=True)
