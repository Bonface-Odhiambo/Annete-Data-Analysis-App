"""
Fleet Fuel Intelligence Dashboard — Streamlit App
MSc Dissertation: Predictive Modelling for Fuel Efficiency and Fleet Optimisation
Anette Kerubo Joseph | 151384 | Strathmore University
"""

import streamlit as st

st.set_page_config(
    page_title="Fleet Fuel Intelligence",
    page_icon="⛽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=Space+Mono:wght@400;700&display=swap');

/* Dark background */
.stApp { background-color: #0B0F1A; }
section[data-testid="stSidebar"] { background-color: #111827; border-right: 1px solid #1E2E47; }

/* Typography */
h1,h2,h3 { font-family: 'Syne', sans-serif !important; }
.mono { font-family: 'Space Mono', monospace; font-size: 0.72rem; }

/* KPI cards */
.kpi-card {
    background: #111827;
    border: 1px solid #1E2E47;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0;
}
.kpi-label { font-family: 'Space Mono', monospace; font-size: 0.58rem; color: #6B7E99;
             letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.3rem; }
.kpi-value { font-family: 'Syne', sans-serif; font-size: 1.8rem; font-weight: 800;
             line-height: 1; letter-spacing: -0.03em; }
.kpi-unit  { font-family: 'Space Mono', monospace; font-size: 0.6rem; color: #6B7E99; margin-top: 0.25rem; }

/* Accent colours */
.g { color: #2DF5A8; }
.b { color: #38B6FF; }
.a { color: #FFB547; }
.r { color: #FF4D6D; }
.p { color: #C084FC; }

/* Privacy badge */
.priv-badge {
    background: rgba(45,245,168,.08); border: 1px solid rgba(45,245,168,.25);
    color: #2DF5A8; font-family: 'Space Mono', monospace; font-size: 0.62rem;
    letter-spacing: 0.12em; padding: 0.3rem 0.8rem; text-transform: uppercase;
    display: inline-block;
}
/* Section rule */
.sec-rule { border-top: 1px solid #1E2E47; margin: 1rem 0 0.8rem; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⛽ Fleet Fuel Intelligence")
    st.markdown('<span class="priv-badge">🔒 Anonymised Dataset</span>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    **Author:** Anette Kerubo Joseph  
    **Reg No:** 151384  
    **Programme:** MSc Data Science & Analytics  
    **Institution:** Strathmore University  
    """)
    st.markdown("---")
    st.markdown("""
    **Navigate using the pages below:**
    - 📊 Overview
    - 📈 Trends
    - 🔬 EDA Figures
    - 🤖 ML Models
    - 🚗 Vehicles
    - 🗺 Routes
    - 🚀 Deployment
    """)
    st.markdown("---")
    st.caption("All vehicle registrations → VEH-xxx  \nAll driver names → DRV-xxx  \nLookup stored separately.")

# ── Home page ─────────────────────────────────────────────────────────────────
st.markdown("""
# Fleet Fuel Intelligence Dashboard
### Predictive Modelling for Fuel Efficiency and Fleet Optimisation in Public Transport
""")

st.markdown("""
> **MSc Dissertation** — Anette Kerubo Joseph | 151384 | Strathmore University  
> CRISP-DM Methodology · All VEH-/DRV- identifiers are anonymised codes
""")

st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.info("📊 **Overview & KPIs** → Key fleet metrics, spend and efficiency summaries")
with col2:
    st.info("🤖 **ML Models** → GBM R²=0.9904 — 4 model comparison with full evaluation")
with col3:
    st.info("🚀 **Deployment** → KES 8.03M annual savings potential + intervention roadmap")

st.markdown("---")
st.markdown("**👈 Select a page from the sidebar to begin exploring the dashboard.**")
