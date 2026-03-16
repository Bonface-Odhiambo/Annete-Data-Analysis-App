"""Page 1 — Overview & KPIs"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import (load_data, get_monthly, get_vehicle_scores, get_route_scores, display_df,
                   get_anomalies, get_savings, PALETTE, TYPE_COLORS,
                   ACCENT, BLUE, AMBER, RED, PURPLE, BG, SURF, BORDER, TEXT, MUTED,
                   PLOTLY_LAYOUT, apply_layout, hex_alpha)

st.set_page_config(page_title="Overview · Fleet Fuel", page_icon="📊", layout="wide")
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



st.title("📊 Overview & KPIs")
st.caption("Combined dataset — Jan 2025 to Dec 2026 · 32,772 records · Vehicle & driver identifiers anonymised (VEH-xxx / DRV-xxx)")

df, df_full, df_eff = load_data()
monthly  = get_monthly(df_full)
vp       = get_vehicle_scores(df_eff)
ra       = get_route_scores(df_eff)
anom_df  = get_anomalies(df)
vp2, monthly_sav, annual_sav, _ = get_savings(df_eff, df_full, vp)

n_anom      = int(anom_df["IF_Anomaly"].sum())
fleet_avg   = df_eff["Fuel_Eff_kmL"].mean()
total_spend = df["Fuel"].sum()
total_lit   = df["Liters"].sum()
with_efc    = df[df["EFC_mid_L"].notna()]
over_pct    = with_efc["Over_EFC"].mean() * 100 if len(with_efc) else 0
net_kes     = df["KES_variance"].sum()

# ── KPI Row 1 ────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("⛽ Total Fuel Spend",    f"KES {total_spend/1e6:.2f}M", f"{len(df):,} records")
c2.metric("💧 Total Litres",        f"{total_lit/1000:.1f}K L",    "All fueling events")
c3.metric("📏 Fleet Avg Efficiency",f"{fleet_avg:.3f} km/L",       f"From {len(df_eff):,} Full Tank trips")
c4.metric("⚠️ Over-Consumption",    f"{over_pct:.1f}%",
          f"Of {len(with_efc):,} trips with EFC data", delta_color="inverse")

st.markdown("")
c5, c6, c7, c8 = st.columns(4)
c5.metric("🚗 Fleet Size",      str(df["PlateNo"].nunique()),      "Unique vehicles")
c6.metric("🛣 Full Tank Trips", f"{len(df_full):,}",               "Efficiency basis")
c7.metric("💰 Net KES Variance",f"KES {net_kes/1e6:.2f}M",        "vs EFC benchmarks", delta_color="inverse")
c8.metric("🔍 Anomalies",       str(n_anom),                        "Isolation Forest 5%", delta_color="inverse")

st.markdown("---")

# ── Charts Row ───────────────────────────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    type_stats = df_eff.groupby("Type")["Fuel_Eff_kmL"].mean().reset_index()
    colors = [TYPE_COLORS.get(t, BLUE) for t in type_stats["Type"]]
    fig = go.Figure(go.Bar(
        x=type_stats["Type"], y=type_stats["Fuel_Eff_kmL"].round(3),
        marker_color=colors, marker_line_color=colors, marker_line_width=1.5,
        text=type_stats["Fuel_Eff_kmL"].round(2).astype(str) + " km/L",
        textposition="outside",
    ))
    apply_layout(fig, "Avg Fuel Efficiency by Vehicle Type (km/L)", 300)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, width="stretch")

with col_b:
    type_spend = df_full.groupby("Type")["Fuel"].sum() / 1e6
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
    st.plotly_chart(fig2, width="stretch")

# ── EFC Compliance + Monthly sparkline ───────────────────────────────────────
col_c, col_d = st.columns([1, 2])

with col_c:
    st.markdown("#### EFC Compliance")
    under = 100 - over_pct
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(name="Over EFC",   x=["Fleet"], y=[over_pct],
                          marker_color=RED,   text=[f"{over_pct:.1f}%"], textposition="inside"))
    fig3.add_trace(go.Bar(name="Within EFC", x=["Fleet"], y=[under],
                          marker_color=ACCENT, text=[f"{under:.1f}%"],  textposition="inside"))
    apply_layout(fig3, "", 240)
    fig3.update_layout(barmode="stack", showlegend=True,
                       legend=dict(orientation="h", y=-0.2))
    fig3.update_yaxes(range=[0,100], ticksuffix="%")
    fig3.update_xaxes(gridcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig3, width="stretch")
    st.markdown(f"""<div style='font-family:Space Mono,monospace;font-size:.62rem;color:{MUTED}'>
    Net KES variance: <span style='color:{RED}'>KES {abs(net_kes/1e6):.2f}M</span></div>""",
    unsafe_allow_html=True)

with col_d:
    fig4 = go.Figure()
    spike_colors = [RED if s else BLUE for s in monthly["Is_Spike"]]
    fig4.add_trace(go.Bar(x=monthly["Year_Month"], y=monthly["Total_Cost"]/1e6,
                          marker_color=spike_colors, name="Monthly Spend",
                          hovertemplate="%{x}: KES %{y:.2f}M<extra></extra>"))
    fig4.add_trace(go.Scatter(x=monthly["Year_Month"], y=monthly["MA3"]/1e6,
                              mode="lines", line=dict(color=ACCENT, width=2), name="3-Month MA"))
    apply_layout(fig4, "Monthly Fuel Cost with 3-Month MA (Red = Spike months)", 300)
    fig4.update_layout(showlegend=True, yaxis_tickprefix="KES ", yaxis_ticksuffix="M",
                       xaxis_tickangle=-45)
    st.plotly_chart(fig4, width="stretch")

st.markdown("---")
st.markdown("#### Quick Dataset Summary")
summ = df_eff[["Liters","Fuel","Fuel_Eff_kmL","Cost_per_Litre","EFC_deviation_L","KES_variance"]].describe().T.round(2)
st.dataframe(display_df(summ), use_container_width=True)
