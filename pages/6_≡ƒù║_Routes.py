"""Page 6 — Routes"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import (load_data, get_route_scores, display_df, TYPE_COLORS,
                   ACCENT, BLUE, AMBER, RED,
                   BG, SURF, BORDER, TEXT, MUTED, PLOTLY_LAYOUT, apply_layout, hex_alpha)

st.set_page_config(page_title="Routes · Fleet Fuel", page_icon="🗺", layout="wide")
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



st.title("🗺 Route Analysis")
st.caption("Route efficiency scores — min 5 Full Tank trips per route/type combination")

df, df_full, df_eff = load_data()
ra = get_route_scores(df_eff)

types_u = sorted(ra["Type"].dropna().unique().tolist())
sel = st.multiselect("Vehicle Type", types_u, default=types_u)
rf = ra[ra["Type"].isin(sel)] if sel else ra

col1, col2 = st.columns(2)
with col1:
    top15 = rf.nlargest(15, "Score")
    fig = go.Figure(go.Bar(
        x=top15["Score"], y=top15["Route"],
        orientation="h",
        marker_color=[hex_alpha(TYPE_COLORS.get(t,BLUE),0.75) for t in top15["Type"]],
        marker_line_color=[TYPE_COLORS.get(t,BLUE) for t in top15["Type"]],
        marker_line_width=1.5,
        text=[f"{s:.1f}" for s in top15["Score"]], textposition="outside",
    ))
    apply_layout(fig, "Top 15 Routes by Efficiency Score", 460)
    fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, width="stretch")

with col2:
    fig2 = go.Figure(go.Scatter(
        x=rf["Trips"], y=rf["Avg_Eff"],
        mode="markers",
        marker=dict(
            color=[TYPE_COLORS.get(t,BLUE) for t in rf["Type"]],
            size=rf["Score"]/6+4, opacity=0.75,
            line=dict(color="rgba(255,255,255,0.3)", width=0.5)
        ),
        text=rf["Route"],
        hovertemplate="%{text}<br>Trips: %{x}<br>Avg Eff: %{y:.3f}<extra></extra>",
    ))
    apply_layout(fig2, "Route Trips vs Efficiency (bubble = Score)", 460)
    fig2.update_layout(xaxis_title="Number of Trips", yaxis_title="Avg Efficiency (km/L)")
    st.plotly_chart(fig2, width="stretch")

# Type breakdown
fig3 = go.Figure()
for vtype in types_u:
    sub = rf[rf["Type"]==vtype]
    if len(sub):
        fig3.add_trace(go.Box(
            y=sub["Avg_Eff"], name=vtype,
            marker_color=TYPE_COLORS.get(vtype,BLUE),
            line_color=TYPE_COLORS.get(vtype,BLUE),
            fillcolor=hex_alpha(TYPE_COLORS.get(vtype,BLUE),0.27),
            boxmean=True,
        ))
apply_layout(fig3, "Route Efficiency Distribution by Vehicle Type", 300)
st.plotly_chart(fig3, width="stretch")

st.dataframe(display_df(rf.sort_values("Score",ascending=False).reset_index(drop=True)),
             use_container_width=True)
