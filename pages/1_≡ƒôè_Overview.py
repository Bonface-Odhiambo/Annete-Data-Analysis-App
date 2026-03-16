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
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=JetBrains+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap');
:root{--bg:#0B0914;--surf:#130D20;--surf2:#1A1230;--border:#2A1D45;--border2:#3A2860;--v1:#A78BFA;--v2:#7C3AED;--teal:#2DD4BF;--pink:#F472B6;--amber:#FCD34D;--red:#F87171;--sky:#38BDF8;--green:#34D399;--text:#EDE9FE;--muted:#6D5FA0;--muted2:#A99BC8;}
.stApp{background-color:var(--bg);color:var(--text);}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#0D0A1C 0%,#110E24 50%,#0A0816 100%)!important;border-right:1px solid var(--border)!important;min-width:268px!important;}
section[data-testid="stSidebar"]>div{padding:0!important;}
.sb-brand{padding:1.5rem 1.2rem 1.1rem;border-bottom:1px solid var(--border);background:linear-gradient(135deg,rgba(167,139,250,.07) 0%,rgba(45,212,191,.04) 100%);}
.sb-logo{width:42px;height:42px;border-radius:12px;background:linear-gradient(135deg,#7C3AED,#2DD4BF);display:flex;align-items:center;justify-content:center;font-size:1.3rem;margin-bottom:.7rem;}
.sb-brand-title{font-family:'Syne',sans-serif;font-size:1.05rem;font-weight:800;color:var(--text);letter-spacing:-.01em;line-height:1.2;margin:0;}
.sb-brand-sub{font-family:'JetBrains Mono',monospace;font-size:.58rem;color:var(--teal);letter-spacing:.12em;text-transform:uppercase;margin-top:.35rem;}
.sb-section-label{font-family:'JetBrains Mono',monospace;font-size:.5rem;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);padding:.9rem 1.2rem .35rem;}
.sb-nav-item{display:flex;align-items:center;gap:.7rem;padding:.52rem 1rem;margin:.06rem .5rem;border-radius:10px;border:1px solid transparent;transition:background .15s,border-color .15s;}
.sb-nav-item:hover{background:rgba(167,139,250,.08);border-color:rgba(167,139,250,.22);}
.sb-nav-icon{width:34px;height:34px;border-radius:9px;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.sb-nav-text{font-family:'Inter',sans-serif;font-size:.82rem;font-weight:500;color:var(--text);}
.sb-nav-badge{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:.53rem;color:var(--muted);background:var(--surf2);border:1px solid var(--border);padding:.1rem .38rem;border-radius:5px;}
.sb-author{margin:.7rem .5rem .4rem;padding:.75rem 1rem;background:var(--surf2);border:1px solid var(--border);border-radius:11px;}
.sb-author-name{font-family:'Syne',sans-serif;font-size:.82rem;font-weight:700;color:var(--text);}
.sb-author-detail{font-family:'JetBrains Mono',monospace;font-size:.56rem;color:var(--muted2);line-height:1.75;margin-top:.3rem;}
.sb-privacy{margin:.4rem .5rem .9rem;padding:.5rem 1rem;background:rgba(45,212,191,.05);border:1px solid rgba(45,212,191,.22);border-radius:9px;display:flex;align-items:flex-start;gap:.55rem;}
.sb-privacy-icon{font-size:.95rem;margin-top:.05rem;}
.sb-privacy-text{font-family:'JetBrains Mono',monospace;font-size:.57rem;color:var(--teal);letter-spacing:.04em;line-height:1.65;}
h1,h2,h3{font-family:'Syne',sans-serif!important;}
footer{display:none!important;}#MainMenu{display:none!important;}
</style>""", unsafe_allow_html=True)

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(__file__)))
from utils import ACCENT  # noqa — triggers path setup only

def _svg(d, c, s=16):
    return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="{d}" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'

_ICONS = {
    "overview": "M3 3h7v7H3V3zm0 11h7v7H3v-7zm11-11h7v7h-7V3zm0 11h7v7h-7v-7z",
    "trends":   "M3 17l4-8 4 4 4-6 4 4 3-6",
    "eda":      "M9 3h6m-3 0v7m-5 4l-2 7h14l-2-7M9 10h6",
    "ml":       "M12 2a4 4 0 014 4v1h1a2 2 0 010 4h-1v1a4 4 0 01-4 4H8a4 4 0 01-4-4v-1H3a2 2 0 010-4h1V6a4 4 0 014-4h4zM9 9h.01M15 9h.01M9 13h6",
    "vehicles": "M5 17H3v-5l2-5h14l2 5v5h-2m-1 0H7m0 0a2 2 0 100 4 2 2 0 000-4zm10 0a2 2 0 100 4 2 2 0 000-4z",
    "routes":   "M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 010-5 2.5 2.5 0 010 5z",
    "deploy":   "M12 2l2.4 7.4H22l-6.2 4.5 2.4 7.4L12 17l-6.2 4.3 2.4-7.4L2 9.4h7.6L12 2z",
}
_IC_BG = {
    "overview": ("rgba(45,212,191,.15)",  "#2DD4BF"),
    "trends":   ("rgba(56,189,248,.15)",  "#38BDF8"),
    "eda":      ("rgba(167,139,250,.15)", "#A78BFA"),
    "ml":       ("rgba(252,211,77,.15)",  "#FCD34D"),
    "vehicles": ("rgba(244,114,182,.15)", "#F472B6"),
    "routes":   ("rgba(52,211,153,.15)",  "#34D399"),
    "deploy":   ("rgba(248,113,113,.15)", "#F87171"),
}
def _nav(key, label, badge):
    bg, clr = _IC_BG[key]
    return (f'<div class="sb-nav-item">'
            f'<div class="sb-nav-icon" style="background:{bg}">{_svg(_ICONS[key],clr)}</div>'
            f'<span class="sb-nav-text">{label}</span>'
            f'<span class="sb-nav-badge">{badge}</span>'
            f'</div>')

with st.sidebar:
    st.markdown('''<div class="sb-brand"><div class="sb-logo">⛽</div>
    <div class="sb-brand-title">Fleet Fuel<br>Intelligence</div>
    <div class="sb-brand-sub">MSc · Strathmore University</div></div>''', unsafe_allow_html=True)
    st.markdown('<div class="sb-section-label">Pages</div>', unsafe_allow_html=True)
    _pages = [("overview","Overview & KPIs","KPIs"),("trends","Trends","Time"),
               ("eda","EDA Figures","NB1"),("ml","ML Models","R²=0.9212"),
               ("vehicles","Vehicles","VEH-xxx"),("routes","Routes","Analysis"),
               ("deploy","Deployment","Savings")]
    for _k, _l, _b in _pages:
        st.markdown(_nav(_k, _l, _b), unsafe_allow_html=True)
    st.markdown('''<div class="sb-section-label" style="margin-top:.5rem">Researcher</div>
    <div class="sb-author"><div class="sb-author-name">Anette Kerubo Joseph</div>
    <div class="sb-author-detail">Reg No: 151384<br>MSc Data Science &amp; Analytics<br>Strathmore University</div></div>
    <div class="sb-privacy"><span class="sb-privacy-icon">🔒</span>
    <div class="sb-privacy-text">Plates → VEH-xxx codes<br>Drivers → DRV-xxxx codes<br>PII stored separately</div></div>''',
    unsafe_allow_html=True)





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
