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
