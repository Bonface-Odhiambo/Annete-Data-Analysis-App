"""
Page 3 — EDA Figures
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import os, glob

st.set_page_config(page_title="EDA | Fleet Fuel", page_icon="�", layout="wide")

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from theme import inject_css, sidebar_brand, sec_header, insight, apply_plotly
from utils import load_data

inject_css()
sidebar_brand()

df, df_full, df_eff = load_data()

st.markdown("""
<div class="ui-card" style="background:linear-gradient(135deg,rgba(182,156,255,.06),rgba(0,229,255,.04));margin-bottom:22px">
  <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:900;color:#F0EDFF">🔬 EDA Figures</div>
  <div style="font-family:'Space Mono',monospace;font-size:10px;color:rgba(240,237,255,.3);margin-top:4px">
    Notebook 1 outputs — distributions, correlations, vehicle benchmarks
  </div>
</div>
""", unsafe_allow_html=True)

# ── Pre-generated asset images (NB1) ─────────────────────────────────────────
asset_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
imgs = sorted(glob.glob(os.path.join(asset_dir, "*.png")))

if imgs:
    sec_header("Pre-generated NB1 Figures", f"{len(imgs)} charts")
    cols = st.columns(2)
    for i, img in enumerate(imgs):
        with cols[i % 2]:
            st.markdown(f"""
<div class="ui-card" style="padding:14px">
  <div style="font-family:'Space Mono',monospace;font-size:9px;
    color:rgba(240,237,255,.3);margin-bottom:8px">
    Figure {i+1} · {os.path.basename(img)}
  </div>""", unsafe_allow_html=True)
            st.image(img, use_column_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("No pre-generated assets found in /assets/ — showing interactive equivalents below.")

# ── Interactive EDA ───────────────────────────────────────────────────────────
sec_header("Interactive Distributions", "From live dataset")

tab1, tab2, tab3, tab4 = st.tabs(["Efficiency Dist.", "Liters Dist.", "Cost/Litre", "Correlation"])

with tab1:
    fig = go.Figure(go.Histogram(
        x=df_eff["Fuel_Eff_kmL"].dropna(),
        nbinsx=60,
        marker_color="#00E5FF",
        marker_line_color="#0F0B1E",
        marker_line_width=1,
        name="km/L",
    ))
    mean_val = df_eff["Fuel_Eff_kmL"].mean()
    fig.add_vline(x=mean_val, line_color="#FFD166", line_dash="dot",
                  annotation_text=f"Mean {mean_val:.2f}", annotation_font_color="#FFD166")
    apply_plotly(fig, "Fuel Efficiency Distribution (km/L)", height=320)
    st.plotly_chart(fig, use_container_width=True)
    insight(f"Fleet mean efficiency: <strong>{mean_val:.3f} km/L</strong>. "
            f"Distribution is right-skewed, indicating most trips cluster below the mean "
            f"with a tail of high-efficiency outliers.")

with tab2:
    fig2 = go.Figure(go.Histogram(
        x=df_full["Liters"].dropna(),
        nbinsx=60,
        marker_color="#B69CFF",
        marker_line_color="#0F0B1E",
        marker_line_width=1,
    ))
    apply_plotly(fig2, "Litres Consumed Distribution", height=320)
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    if "Cost_per_Litre" in df_full.columns:
        cpl = df_full["Cost_per_Litre"].dropna()
        cpl = cpl[(cpl > 0) & (cpl < cpl.quantile(0.99))]
        fig3 = go.Figure(go.Histogram(
            x=cpl, nbinsx=50,
            marker_color="#FFD166",
            marker_line_color="#0F0B1E",
            marker_line_width=1,
        ))
        apply_plotly(fig3, "Cost per Litre (KES) Distribution", height=320)
        st.plotly_chart(fig3, use_container_width=True)
        insight(f"Median cost/litre: <strong>KES {cpl.median():.2f}</strong>. "
                f"Spread indicates variation across petrol stations and fuel grades.")

with tab4:
    num_cols = ["Liters","Fuel_Eff_kmL","Cost_per_Litre","Mileage"]
    num_cols = [c for c in num_cols if c in df_eff.columns]
    if len(num_cols) >= 2:
        corr = df_eff[num_cols].corr()
        import plotly.figure_factory as ff
        fig4 = go.Figure(go.Heatmap(
            z=corr.values,
            x=corr.columns, y=corr.index,
            colorscale=[[0,"#FF6B6B"],[0.5,"#1A1530"],[1,"#00E5FF"]],
            zmin=-1, zmax=1,
            text=corr.round(2).values,
            texttemplate="%{text}",
            textfont=dict(family="Space Mono, monospace", size=11),
        ))
        apply_plotly(fig4, "Feature Correlation Matrix", height=380)
        st.plotly_chart(fig4, use_container_width=True)

# ── Box plots by vehicle type ──────────────────────────────────────────────────
sec_header("Efficiency by Vehicle Type", "Box plot · Full Tank trips")

if "Type" in df_eff.columns:
    import plotly.express as px
    fig5 = px.box(
        df_eff.dropna(subset=["Fuel_Eff_kmL","Type"]),
        x="Type", y="Fuel_Eff_kmL",
        color="Type",
        color_discrete_map={"Bus":"#FF6B6B","Shuttle":"#74B9FF","Eph":"#FFD166","Admin":"#B69CFF"},
        points="outliers",
    )
    apply_plotly(fig5, "Fuel Efficiency (km/L) by Vehicle Type", height=320)
    fig5.update_layout(showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)
