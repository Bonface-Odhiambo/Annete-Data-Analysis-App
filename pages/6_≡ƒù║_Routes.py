"""Page 6 — Route Optimisation"""
import streamlit as st
import plotly.graph_objects as go
from PIL import Image
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import (load_data, get_route_scores, ACCENT, BLUE, AMBER, RED, PURPLE,
                   TYPE_COLORS, BG, SURF, BORDER, TEXT, MUTED, apply_layout)

st.set_page_config(page_title="Routes · Fleet Fuel", page_icon="🗺", layout="wide")
st.markdown("<style>.stApp{background-color:#0B0F1A;}section[data-testid='stSidebar']{background-color:#111827;border-right:1px solid #1E2E47;}</style>", unsafe_allow_html=True)

ASSETS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

st.title("🗺 Route Optimisation")
st.caption("Route score = 60% efficiency + 40% consistency | ≥10 trips required | RO3")

df1, df2, df1_full, df1_eff = load_data()
ra = get_route_scores(df1_eff)

c1, c2, c3 = st.columns(3)
c1.metric("🗺 Routes Scored",          str(len(ra)),                              "≥10 trips")
c2.metric("🏆 Best Route Efficiency",  f"{ra['Avg_Eff'].max():.2f} km/L",        ra.loc[ra['Avg_Eff'].idxmax(),'Route'][:30])
c3.metric("⚠️ Worst Route Efficiency", f"{ra['Avg_Eff'].min():.2f} km/L",        ra.loc[ra['Avg_Eff'].idxmin(),'Route'][:30], delta_color="inverse")

st.markdown("---")

# ── Scatter matrix ────────────────────────────────────────────────────────────
col_a, col_b = st.columns([3, 2])
with col_a:
    fig = go.Figure()
    for vtype in ra["Type"].unique():
        sub = ra[ra["Type"] == vtype]
        fig.add_trace(go.Scatter(
            x=sub["Avg_Eff"], y=sub["Std_Eff"].fillna(0),
            mode="markers", name=vtype,
            marker=dict(size=sub["Trips"]*0.3+5, color=TYPE_COLORS.get(vtype, BLUE),
                        opacity=0.7, line=dict(width=0)),
            text=sub["Route"], hovertemplate="<b>%{text}</b><br>Avg: %{x:.2f} km/L<br>Std: %{y:.2f}<extra></extra>"))
    eff_med = ra["Avg_Eff"].median(); std_med = ra["Std_Eff"].fillna(0).median()
    fig.add_vline(x=eff_med, line_color="white", line_dash="dot", line_width=1, opacity=0.4)
    fig.add_hline(y=std_med, line_color="white", line_dash="dot", line_width=1, opacity=0.4)
    fig.add_annotation(x=ra["Avg_Eff"].max()*0.97, y=ra["Std_Eff"].fillna(0).min()*1.1,
        text="OPTIMAL", font=dict(color=ACCENT, size=11, family="Space Mono"), showarrow=False)
    apply_layout(fig, "Route Optimisation Matrix (bubble size = trip count)", 380)
    fig.update_layout(showlegend=True, xaxis_title="Avg Efficiency (km/L)", yaxis_title="Std Dev")
    st.plotly_chart(fig, width='stretch')

with col_b:
    top10   = ra.nlargest(10, "Score")
    bot10   = ra.nsmallest(10, "Score")
    fig2    = go.Figure()
    fig2.add_trace(go.Bar(
        y=[r[:30]+"…" if len(r)>30 else r for r in top10["Route"]],
        x=top10["Score"], orientation="h",
        marker_color=ACCENT, name="Top 10",
        text=top10["Score"].round(0).astype(int), textposition="inside"))
    fig2.add_trace(go.Bar(
        y=[r[:30]+"…" if len(r)>30 else r for r in bot10["Route"]],
        x=bot10["Score"], orientation="h",
        marker_color=RED, name="Bottom 10",
        text=bot10["Score"].round(0).astype(int), textposition="inside"))
    apply_layout(fig2, "Top & Bottom 10 Route Scores", 380)
    fig2.update_layout(showlegend=True, barmode="overlay",
                       xaxis=dict(range=[0,100], gridcolor=BORDER),
                       yaxis=dict(gridcolor="rgba(0,0,0,0)"),
                       yaxis_autorange="reversed")
    st.plotly_chart(fig2, width='stretch')

# ── Tables ────────────────────────────────────────────────────────────────────
st.markdown("---")
col_c, col_d = st.columns(2)
with col_c:
    st.markdown("#### 🏆 Top 10 Routes")
    d = top10[["Route","Type","Trips","Avg_Eff","Std_Eff","Score"]].reset_index(drop=True)
    d.columns = ["Route","Type","Trips","Avg Eff (km/L)","Std Eff","Score"]
    d.index += 1
    st.dataframe(d.style.format({"Avg Eff (km/L)":"{:.3f}","Std Eff":"{:.3f}","Score":"{:.1f}"}),
                 width='stretch')
with col_d:
    st.markdown("#### ⚠️ Bottom 10 Routes — Intervention Priority")
    d2 = bot10[["Route","Type","Trips","Avg_Eff","Std_Eff","Score"]].reset_index(drop=True)
    d2.columns = ["Route","Type","Trips","Avg Eff (km/L)","Std Eff","Score"]
    d2.index += 1
    st.dataframe(d2.style.format({"Avg Eff (km/L)":"{:.3f}","Std Eff":"{:.3f}","Score":"{:.1f}"}),
                 width='stretch')

# ── Searchable table ──────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("🔍 Search All Routes"):
    search = st.text_input("Filter by route name")
    show = ra.copy()
    if search:
        show = show[show["Route"].str.contains(search, case=False, na=False)]
    show = show[["Route","Type","Trips","Avg_Eff","Std_Eff","Score"]].sort_values("Score",ascending=False)
    show.columns = ["Route","Type","Trips","Avg Eff (km/L)","Std Eff","Score"]
    st.dataframe(show.style.format({"Avg Eff (km/L)":"{:.3f}","Std Eff":"{:.3f}","Score":"{:.1f}"}),
                 width='stretch')

with st.expander("**Fig 3.5 — Route Optimisation Full Figure**"):
    path = os.path.join(ASSETS, "fig3_5_route_optimisation.png")
    if os.path.exists(path):
        st.image(Image.open(path), width='stretch')
