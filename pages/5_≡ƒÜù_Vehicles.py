"""
Page 5 — Vehicles
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Vehicles | Fleet Fuel", page_icon="�", layout="wide")

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from theme import inject_css, sidebar_brand, sec_header, insight, apply_plotly
from utils import load_data, get_vehicle_scores, display_df

inject_css()
sidebar_brand()

df, df_full, df_eff = load_data()
vp = get_vehicle_scores(df_eff)

st.markdown("""
<div class="ui-card" style="background:linear-gradient(135deg,rgba(255,107,107,.06),rgba(182,156,255,.04));margin-bottom:22px">
  <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:900;color:#F0EDFF">🚌 Vehicles</div>
  <div style="font-family:'Space Mono',monospace;font-size:10px;color:rgba(240,237,255,.3);margin-top:4px">
    Per-vehicle efficiency grades A–D · All vehicles anonymised as VEH-xxx
  </div>
</div>
""", unsafe_allow_html=True)

# ── Grade summary ─────────────────────────────────────────────────────────────
grade_counts = vp["Grade"].value_counts()

c1,c2,c3,c4,c5 = st.columns(5)
kpis = [
    (c1, "Total Vehicles",  str(len(vp)),                            "Min 3 trips",  "cyan"),
    (c2, "Grade A",         str(grade_counts.get("A",0)),             "Top 20%",      "lime"),
    (c3, "Grade B",         str(grade_counts.get("B",0)),             "60–80th pct",  "cyan"),
    (c4, "Grade C",         str(grade_counts.get("C",0)),             "40–60th pct",  "gold"),
    (c5, "Grade D",         str(grade_counts.get("D",0)),             "Bottom 40%",   "coral"),
]
for col, label, val, sub, color in kpis:
    col.markdown(f"""
<div class="kpi-pill kpi-{color}">
  <div class="kpi-label">{label}</div>
  <div class="kpi-value" style="color:var(--{color})">{val}</div>
  <div class="kpi-sub">{sub}</div>
</div>""", unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── Filters ───────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    type_opts = ["All"] + sorted(vp["Type"].dropna().unique().tolist())
    sel_type  = st.selectbox("Vehicle Type", type_opts)
with col2:
    grade_opts = ["All", "A", "B", "C", "D"]
    sel_grade  = st.selectbox("Grade", grade_opts)
with col3:
    search = st.text_input("Search Vehicle ID", placeholder="VEH-001")

filtered = vp.copy()
if sel_type  != "All": filtered = filtered[filtered["Type"]  == sel_type]
if sel_grade != "All": filtered = filtered[filtered["Grade"] == sel_grade]
if search:             filtered = filtered[filtered["PlateNo"].str.contains(search, case=False, na=False)]

# ── Score distribution ────────────────────────────────────────────────────────
sec_header("Efficiency Score Distribution", "Within-type normalised 0–100")

left, right = st.columns(2)

with left:
    fig = go.Figure(go.Histogram(
        x=filtered["Score"].dropna(), nbinsx=25,
        marker_color="#00E5FF",
        marker_line_color="#0F0B1E", marker_line_width=1,
    ))
    apply_plotly(fig, "Score Distribution", height=280)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with right:
    grade_colors = {"A": "#C3F73A", "B": "#00E5FF", "C": "#FFD166", "D": "#FF6B6B"}
    gc = filtered["Grade"].value_counts().reset_index()
    gc.columns = ["Grade","Count"]
    fig2 = go.Figure(go.Bar(
        x=gc["Grade"], y=gc["Count"],
        marker_color=[grade_colors.get(g,"#B69CFF") for g in gc["Grade"]],
        marker_line_color="#0F0B1E", marker_line_width=2,
        text=gc["Count"], textposition="outside",
        textfont=dict(family="Space Mono, monospace", size=11, color="#F0EDFF"),
    ))
    apply_plotly(fig2, "Grade Breakdown", height=280)
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# ── Top / Bottom tables ───────────────────────────────────────────────────────
sec_header("Top & Bottom Performers", "By within-type efficiency score")

t1, t2 = st.columns(2)
with t1:
    st.markdown("""
<div style="font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.1em;
  text-transform:uppercase;color:#C3F73A;margin-bottom:8px">▲ Top 10 Vehicles</div>""",
    unsafe_allow_html=True)
    top10 = filtered.nlargest(10, "Score")[["PlateNo","Type","Avg_Eff","Score","Grade"]]
    st.dataframe(display_df(top10), use_container_width=True, height=340)

with t2:
    st.markdown("""
<div style="font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.1em;
  text-transform:uppercase;color:#FF6B6B;margin-bottom:8px">▼ Bottom 10 Vehicles</div>""",
    unsafe_allow_html=True)
    bot10 = filtered.nsmallest(10, "Score")[["PlateNo","Type","Avg_Eff","Score","Grade"]]
    st.dataframe(display_df(bot10), use_container_width=True, height=340)

# ── Full table ─────────────────────────────────────────────────────────────────
sec_header("All Vehicles", f"{len(filtered)} vehicles shown")
show_cols = ["PlateNo","Type","Trips","Avg_Eff","Score","Grade","Total_Cost","Net_KES"]
show_cols = [c for c in show_cols if c in filtered.columns]
st.dataframe(display_df(filtered[show_cols]).sort_values("Score", ascending=False),
             use_container_width=True, height=420)

insight(f"""
<strong>{grade_counts.get('D',0)} Grade-D vehicles</strong> are the highest-priority intervention targets.
Bringing them to the within-type Q3 efficiency benchmark drives the majority of the
<strong>KES 8.03M</strong> annual savings estimate. Filter by type to see type-specific patterns.
""")
