"""Page 5 — Vehicle Benchmarking"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from PIL import Image
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import (load_data, get_vehicle_scores, get_anomalies, get_savings,
                   ACCENT, BLUE, AMBER, RED, PURPLE, TYPE_COLORS,
                   BG, SURF, BORDER, TEXT, MUTED, apply_layout)

st.set_page_config(page_title="Vehicles · Fleet Fuel", page_icon="🚗", layout="wide")
st.markdown("<style>.stApp{background-color:#0B0F1A;}section[data-testid='stSidebar']{background-color:#111827;border-right:1px solid #1E2E47;}</style>", unsafe_allow_html=True)

ASSETS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
GRADE_COLORS = {"A": ACCENT, "B": BLUE, "C": AMBER, "D": RED}

st.title("🚗 Vehicle Efficiency Benchmarking")
st.caption("All vehicle registrations anonymised as VEH-xxx codes | Within-type efficiency scoring (0–100)")

df1, df2, df1_full, df1_eff = load_data()
vp = get_vehicle_scores(df1_eff)
vp2, monthly_sav, annual_sav, type_q3 = get_savings(df1_eff, df1_full, vp)

total_g = lambda g: int((vp["Grade"] == g).sum())

# ── KPI cards ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("🚗 Vehicles Scored",   str(len(vp)),         "≥5 full-tank trips")
c2.metric("🏆 Grade A",           str(total_g("A")),    "Score 80–100 (excellent)")
c3.metric("⚠️ Grade D",           str(total_g("D")),    "Score 0–40 (intervention)", delta_color="inverse")
c4.metric("📉 Below Q3 Target",   str(total_g("C") + total_g("D")), "Grades C + D combined", delta_color="inverse")

st.markdown("---")

# ── Grade distribution chart ──────────────────────────────────────────────────
col_a, col_b = st.columns(2)
with col_a:
    grade_type = vp.groupby(["Type","Grade"]).size().reset_index(name="n")
    types_u = vp["Type"].unique().tolist()
    fig = go.Figure()
    for grade in ["D","C","B","A"]:
        vals = [int(grade_type[(grade_type["Type"]==t) & (grade_type["Grade"]==grade)]["n"].sum())
                for t in types_u]
        fig.add_trace(go.Bar(name=f"Grade {grade}", x=types_u, y=vals,
            marker_color=GRADE_COLORS[grade], marker_opacity=0.85,
            text=vals, textposition="inside", insidetextanchor="middle",
            textfont=dict(color="white", size=10)))
    apply_layout(fig, "Vehicle Grade Distribution by Type", 320)
    fig.update_layout(barmode="stack", showlegend=True,
                      xaxis=dict(gridcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    fig2 = go.Figure()
    for vtype in types_u:
        sub = vp[vp["Type"] == vtype]["Score"].dropna()
        fig2.add_trace(go.Box(y=sub, name=vtype,
            marker_color=TYPE_COLORS.get(vtype, BLUE),
            line_color=TYPE_COLORS.get(vtype, BLUE),
            fillcolor=TYPE_COLORS.get(vtype, BLUE) + "44",
            boxmean=True))
    apply_layout(fig2, "Efficiency Score Distribution by Type (0–100)", 320)
    fig2.update_layout(showlegend=False, yaxis_title="Score")
    st.plotly_chart(fig2, use_container_width=True)

# ── Top / Bottom tables ───────────────────────────────────────────────────────
st.markdown("---")
col_c, col_d = st.columns(2)

def grade_badge(g):
    colors = {"A": "#2DF5A820", "B": "#38B6FF20", "C": "#FFB54720", "D": "#FF4D6D20"}
    text   = {"A": "#2DF5A8",   "B": "#38B6FF",   "C": "#FFB547",   "D": "#FF4D6D"}
    return g  # streamlit dataframe handles colour separately

with col_c:
    st.markdown(f"#### 🏆 Top 10 Vehicles")
    top10 = vp.nlargest(10, "Score")[["PlateNo","Type","Avg_Eff","Score","Grade"]].copy()
    top10.columns = ["VEH ID","Type","Avg Eff (km/L)","Score","Grade"]
    top10 = top10.reset_index(drop=True)
    top10.index += 1
    st.dataframe(top10.style.format({"Avg Eff (km/L)": "{:.3f}", "Score": "{:.1f}"}),
                 use_container_width=True)

with col_d:
    st.markdown(f"#### 🚨 Bottom 10 — Priority Intervention")
    bot10 = vp.nsmallest(10, "Score")[["PlateNo","Type","Avg_Eff","Score","Grade"]].copy()
    bot10.columns = ["VEH ID","Type","Avg Eff (km/L)","Score","Grade"]
    bot10 = bot10.reset_index(drop=True)
    bot10.index += 1
    st.dataframe(bot10.style.format({"Avg Eff (km/L)": "{:.3f}", "Score": "{:.1f}"}),
                 use_container_width=True)

# ── Searchable full table ─────────────────────────────────────────────────────
st.markdown("---")
with st.expander("🔍 Search Full Vehicle Scoring Table"):
    filter_type  = st.multiselect("Filter by Type", vp["Type"].unique().tolist(), default=vp["Type"].unique().tolist())
    filter_grade = st.multiselect("Filter by Grade", ["A","B","C","D"], default=["A","B","C","D"])
    filtered = vp[(vp["Type"].isin(filter_type)) & (vp["Grade"].isin(filter_grade))]
    display = filtered[["PlateNo","Type","Trips","Avg_Eff","Score","Grade"]].sort_values("Score", ascending=False)
    display.columns = ["VEH ID","Type","Trips","Avg Eff (km/L)","Score","Grade"]
    st.dataframe(display.style.format({"Avg Eff (km/L)": "{:.3f}", "Score": "{:.1f}"}),
                 use_container_width=True)
    st.caption(f"{len(display)} vehicles shown")

# ── Benchmarking figure ───────────────────────────────────────────────────────
st.markdown("---")
with st.expander("**Fig 3.3 — Vehicle Benchmarking Full Figure**", expanded=False):
    path = os.path.join(ASSETS, "fig3_3_benchmarking.png")
    if os.path.exists(path):
        st.image(Image.open(path), use_container_width=True)
