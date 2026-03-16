"""Page 7 — Deployment Insights"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import (load_data, get_vehicle_scores, get_savings, display_df,
                   ACCENT, BLUE, AMBER, RED, PURPLE,
                   BG, SURF, BORDER, TEXT, MUTED, PLOTLY_LAYOUT, apply_layout, hex_alpha)

st.set_page_config(page_title="Deployment · Fleet Fuel", page_icon="🚀", layout="wide")
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





st.title("🚀 Deployment & Savings Insights")
st.caption("Estimated savings from optimising under-performing vehicles to fleet benchmark · Vehicle IDs anonymised (VEH-xxx)")

df, df_full, df_eff = load_data()
vp = get_vehicle_scores(df_eff)
vp2, monthly_sav, annual_sav, type_q3 = get_savings(df_eff, df_full, vp)

c1, c2, c3 = st.columns(3)
c1.metric("💰 Monthly Savings Potential", f"KES {monthly_sav/1e6:.2f}M")
c2.metric("📅 Annual Savings Potential",  f"KES {annual_sav/1e6:.2f}M")
c3.metric("🚗 Vehicles Below Target",
          str(int((vp2["Gap"] > 0).sum())), f"of {len(vp2)} scored vehicles")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    top_sav = vp2[vp2["Monthly_KES"] > 0].nlargest(15, "Monthly_KES")
    fig = go.Figure(go.Bar(
        x=top_sav["Monthly_KES"] / 1000,
        y=top_sav["PlateNo"],        # VEH-xxx values
        orientation="h",
        marker_color=[hex_alpha(AMBER, 0.75)] * len(top_sav),
        marker_line_color=AMBER, marker_line_width=1.5,
        text=[f"KES {v/1000:.1f}K" for v in top_sav["Monthly_KES"]],
        textposition="outside",
    ))
    apply_layout(fig, "Top 15 Vehicles — Monthly Savings Potential (KES '000)", 460)
    fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed"),
                      yaxis_title="Vehicle ID")
    st.plotly_chart(fig, width="stretch")

with col2:
    type_sav = vp2.groupby("Type")["Monthly_KES"].sum().reset_index()
    fig2 = go.Figure(go.Pie(
        labels=type_sav["Type"].tolist(),
        values=(type_sav["Monthly_KES"] / 1000).round(1).tolist(),
        hole=0.45,
        marker=dict(line=dict(color=BG, width=2)),
        textinfo="label+percent",
        hovertemplate="%{label}: KES %{value}K/month<extra></extra>",
    ))
    apply_layout(fig2, "Monthly Savings by Vehicle Type", 380)
    st.plotly_chart(fig2, width="stretch")

# Gap analysis — Vehicle ID in hover
fig3 = go.Figure()
for vtype, color in [("Bus", RED), ("Shuttle", BLUE), ("Eph", AMBER)]:
    sub = vp2[vp2["Type"] == vtype]
    if len(sub):
        fig3.add_trace(go.Scatter(
            x=sub["Avg_Eff"], y=sub["Gap"],
            mode="markers", name=vtype,
            marker=dict(color=color, size=8, opacity=0.75),
            text=sub["PlateNo"],   # VEH-xxx
            hovertemplate="<b>%{text}</b><br>Avg: %{x:.3f} km/L<br>Gap: %{y:.3f}<extra></extra>",
        ))
apply_layout(fig3, "Efficiency Gap vs Current Performance", 350)
fig3.update_layout(xaxis_title="Avg Fuel Efficiency (km/L)", yaxis_title="Gap to Fleet Benchmark")
st.plotly_chart(fig3, width="stretch")

# Fleet benchmark targets
st.markdown("#### Fleet Benchmark Targets (75th Percentile by Type)")
import pandas as pd
bm = pd.DataFrame([{"Vehicle Type": t, "Target Efficiency (km/L)": round(v, 3)}
                   for t, v in type_q3.items()])
st.dataframe(bm, use_container_width=True)

st.markdown(f"""
---
**Methodology:** Savings estimated by comparing each vehicle's average efficiency to the 75th percentile
for its vehicle type. Cost per litre = fleet median (KES/L). Monthly savings = litres saved × cost/L.  
**Annual savings potential: KES {annual_sav/1e6:.2f}M** assuming current trip frequency continues.  
*All vehicle identifiers shown as VEH-xxx anonymised codes.*
""")
