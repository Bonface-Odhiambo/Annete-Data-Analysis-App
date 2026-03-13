"""Page 3 — EDA Figures (all 7 from NB1)"""
import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="EDA Figures · Fleet Fuel", page_icon="🔬", layout="wide")
st.markdown("<style>.stApp{background-color:#0B0F1A;}section[data-testid='stSidebar']{background-color:#111827;border-right:1px solid #1E2E47;}</style>", unsafe_allow_html=True)

st.title("🔬 EDA & Descriptive Figures")
st.caption("Notebook 1 outputs — click the expanders to view each figure at full resolution")

ASSETS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

FIGS = [
    ("fig1_1_univariate",    "Figure 1.1 — Univariate Distributions of Core Fuel Variables",
     "Histograms of 6 key variables with mean, median and skewness annotations."),
    ("fig1_2_vehicle_types", "Figure 1.2 — Fuel Consumption Profiles by Vehicle Type",
     "Boxplot efficiency, mean cost per trip and mean trip distance across Bus, Shuttle, EPH, Admin."),
    ("fig1_3_temporal",      "Figure 1.3 — Monthly Temporal Trends (May 2025 – Dec 2026)",
     "Monthly spend with 3-month MA, linear trend and operational spike annotation; MoM % change; efficiency trend."),
    ("fig1_4_routes",        "Figure 1.4 — Route-Level Fuel Efficiency Analysis (Top 15 Routes)",
     "Trip count and average efficiency per route; green = above fleet avg, red = below."),
    ("fig1_5_correlations",  "Figure 1.5 — Pearson Correlation Matrix & Target Correlations (RO2)",
     "Heatmap of all key variable correlations plus ranked bar chart vs fuel efficiency target."),
    ("fig1_6_efc_benchmark", "Figure 1.6 — Actual vs Expected Fuel Consumption (EFC Benchmark)",
     "Status pie chart, actual vs EFC midpoint by model, and % over-consuming by model."),
    ("fig1_7_drivers",       "Figure 1.7 — Driver Performance Analysis (Anonymised DRV Codes)",
     "Top 15 and bottom 15 DRV-coded drivers by average fuel efficiency (≥5 trips). RO2 — behavioural factor."),
]

for key, title, description in FIGS:
    with st.expander(f"**{title}**", expanded=False):
        st.caption(description)
        path = os.path.join(ASSETS, f"{key}.png")
        if os.path.exists(path):
            img = Image.open(path)
            st.image(img, use_container_width=True)
        else:
            st.warning(f"Figure not found: {path}")

st.markdown("---")
st.info("💡 All driver and vehicle identifiers in Fig 1.7 are anonymised DRV-/VEH-xxx codes. "
        "The original lookup table is stored separately and not included in this deployment.")
