"""
Page 6 — Routes
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Routes | Fleet Fuel", page_icon="🗺", layout="wide")

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from theme import inject_css, sidebar_brand, sec_header, insight, apply_plotly
from utils import load_data, get_route_scores, display_df

inject_css()
sidebar_brand()

df, df_full, df_eff = load_data()
ra = get_route_scores(df_eff)

st.markdown("""
<div class="ui-card" style="background:linear-gradient(135deg,rgba(195,247,58,.06),rgba(0,229,255,.04));margin-bottom:22px">
  <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:900;color:#F0EDFF">🗺 Routes</div>
  <div style="font-family:'Space Mono',monospace;font-size:10px;color:rgba(240,237,255,.3);margin-top:4px">
    Route-level efficiency scoring · Optimisation matrix · Min 5 trips per route
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
kpis = [
    (c1, "Routes Analysed",   str(ra["Route"].nunique()),           "Min 5 trips",           "cyan"),
    (c2, "Best Avg Eff.",     f"{ra['Avg_Eff'].max():.2f} km/L",   "Top route",              "lime"),
    (c3, "Worst Avg Eff.",    f"{ra['Avg_Eff'].min():.2f} km/L",   "Lowest route",           "coral"),
    (c4, "Avg Route Score",   f"{ra['Score'].mean():.1f}",          "0–100 composite",        "violet"),
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
c1, c2 = st.columns([2,1])
with c1:
    search = st.text_input("Search route", placeholder="Route name or code")
with c2:
    type_opts = ["All"] + sorted(ra["Type"].dropna().unique().tolist())
    sel_type  = st.selectbox("Vehicle Type", type_opts)

filtered = ra.copy()
if sel_type != "All": filtered = filtered[filtered["Type"] == sel_type]
if search:            filtered = filtered[filtered["Route"].str.contains(search, case=False, na=False)]

# ── Scatter: Avg Eff vs Consistency ──────────────────────────────────────────
sec_header("Efficiency vs Consistency Matrix", "Bubble = trip count")

fig = go.Figure()
types = filtered["Type"].dropna().unique()
type_colors = {"Bus":"#FF6B6B","Shuttle":"#74B9FF","Eph":"#FFD166","Admin":"#B69CFF"}

for t in types:
    sub = filtered[filtered["Type"] == t]
    fig.add_trace(go.Scatter(
        x=sub["Avg_Eff"],
        y=sub["Std_Eff"].fillna(0),
        mode="markers",
        name=t,
        marker=dict(
            size=sub["Trips"].clip(5, 50).apply(lambda x: x**0.5 * 4),
            color=type_colors.get(t, "#B69CFF"),
            opacity=0.75,
            line=dict(color="#0F0B1E", width=1),
        ),
        text=sub["Route"],
        hovertemplate="<b>%{text}</b><br>Avg: %{x:.2f} km/L<br>Std: %{y:.2f}<extra></extra>",
    ))

apply_plotly(fig, "Route Optimisation Matrix (Avg Efficiency vs Variability)", height=380)
fig.update_xaxes(title="Avg Efficiency (km/L)")
fig.update_yaxes(title="Std Dev (km/L) — lower is more consistent")
# Target quadrant annotation
if not filtered.empty:
    med_eff = filtered["Avg_Eff"].median()
    med_std = filtered["Std_Eff"].fillna(0).median()
    fig.add_shape(type="rect",
        x0=med_eff, x1=filtered["Avg_Eff"].max()*1.05,
        y0=0, y1=med_std,
        line=dict(color="rgba(195,247,58,.3)", width=1, dash="dot"),
        fillcolor="rgba(195,247,58,.04)",
    )
    fig.add_annotation(
        x=filtered["Avg_Eff"].max()*0.98, y=med_std*0.2,
        text="✦ Target zone", font=dict(color="#C3F73A", size=10, family="Space Mono"),
        showarrow=False,
    )
st.plotly_chart(fig, use_container_width=True)

# ── Top / Bottom routes ───────────────────────────────────────────────────────
sec_header("Route Rankings", "By composite efficiency score")

left, right = st.columns(2)
with left:
    st.markdown("""<div style="font-family:'Space Mono',monospace;font-size:9px;
      letter-spacing:.1em;text-transform:uppercase;color:#C3F73A;margin-bottom:8px">
      ▲ Top 10 Routes</div>""", unsafe_allow_html=True)
    top = filtered.nlargest(10, "Score")[["Route","Type","Trips","Avg_Eff","Std_Eff","Score"]]
    st.dataframe(display_df(top), use_container_width=True, height=340)

with right:
    st.markdown("""<div style="font-family:'Space Mono',monospace;font-size:9px;
      letter-spacing:.1em;text-transform:uppercase;color:#FF6B6B;margin-bottom:8px">
      ▼ Bottom 10 Routes</div>""", unsafe_allow_html=True)
    bot = filtered.nsmallest(10, "Score")[["Route","Type","Trips","Avg_Eff","Std_Eff","Score"]]
    st.dataframe(display_df(bot), use_container_width=True, height=340)

# ── Full table ─────────────────────────────────────────────────────────────────
sec_header("All Routes", f"{len(filtered)} routes shown")
st.dataframe(
    display_df(filtered.sort_values("Score", ascending=False)),
    use_container_width=True, height=400,
)

insight("""
Routes in the <strong style="color:#C3F73A">target zone</strong> (high efficiency + low variability)
represent best-practice operating conditions. Vehicles on low-scoring routes should be audited
for driver behaviour, route terrain, and fuel station proximity. Consistency (low Std Dev) is
weighted at 40% in the composite score.
""")
