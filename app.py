"""
Fleet Fuel Intelligence Dashboard — Home Page
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

from theme import inject_css, sidebar_brand, sec_header, insight

inject_css()
sidebar_brand()

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
  position:relative;overflow:hidden;
  background:linear-gradient(135deg,rgba(0,229,255,.07),rgba(182,156,255,.06) 50%,rgba(255,107,107,.04));
  border:1px solid rgba(255,255,255,.14);border-radius:20px;
  padding:44px 52px;margin-bottom:28px">

  <div style="position:absolute;top:-100px;right:-80px;width:380px;height:380px;border-radius:50%;
    background:radial-gradient(circle,rgba(0,229,255,.12),transparent 65%);pointer-events:none"></div>
  <div style="position:absolute;bottom:-80px;left:10%;width:260px;height:260px;border-radius:50%;
    background:radial-gradient(circle,rgba(182,156,255,.09),transparent 65%);pointer-events:none"></div>

  <div style="font-family:'Space Mono',monospace;font-size:10px;letter-spacing:.2em;
    text-transform:uppercase;color:#00E5FF;margin-bottom:14px">
    ⛽ MSc Dissertation &nbsp;·&nbsp; CRISP-DM &nbsp;·&nbsp; Strathmore University
  </div>

  <h1 style="font-size:46px;font-weight:900;letter-spacing:-.04em;line-height:1.08;
    margin-bottom:16px;color:#F0EDFF">
    Fleet Fuel
    <span style="background:linear-gradient(90deg,#00E5FF,#B69CFF);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">
      Intelligence</span><br>Dashboard
  </h1>

  <p style="font-size:15px;color:rgba(240,237,255,.45);line-height:1.7;max-width:640px;margin-bottom:26px">
    Predictive modelling for fuel efficiency and fleet optimisation in public transport —
    combining <strong style="color:#F0EDFF">14,526 anonymised trip records</strong> across 178 vehicles
    with machine learning to surface KES 285M+ in fleet spend patterns and
    <strong style="color:#C3F73A">KES 8.03M</strong> in annual recoverable savings.
  </p>

  <div style="display:flex;flex-wrap:wrap;gap:8px">
    <span style="font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.06em;
      color:rgba(240,237,255,.45);background:rgba(255,255,255,.04);
      border:1px solid rgba(255,255,255,.08);border-radius:6px;padding:5px 10px;
      display:flex;align-items:center;gap:5px">
      <span style="width:4px;height:4px;border-radius:50%;background:#00E5FF;display:inline-block"></span>
      May 2025 – Dec 2026
    </span>
    <span style="font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.06em;
      color:rgba(240,237,255,.45);background:rgba(255,255,255,.04);
      border:1px solid rgba(255,255,255,.08);border-radius:6px;padding:5px 10px;
      display:flex;align-items:center;gap:5px">
      <span style="width:4px;height:4px;border-radius:50%;background:#B69CFF;display:inline-block"></span>
      14,526 Records · 2 Sheets
    </span>
    <span style="font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.06em;
      color:rgba(240,237,255,.45);background:rgba(255,255,255,.04);
      border:1px solid rgba(255,255,255,.08);border-radius:6px;padding:5px 10px;
      display:flex;align-items:center;gap:5px">
      <span style="width:4px;height:4px;border-radius:50%;background:#FFD166;display:inline-block"></span>
      4 ML Models · GBM Champion
    </span>
    <span style="font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.06em;
      color:rgba(240,237,255,.45);background:rgba(255,255,255,.04);
      border:1px solid rgba(255,255,255,.08);border-radius:6px;padding:5px 10px;
      display:flex;align-items:center;gap:5px">
      <span style="width:4px;height:4px;border-radius:50%;background:#FF6B6B;display:inline-block"></span>
      89.6% Over-EFC Trips
    </span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Row ───────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)

def kpi(col, label, value, sub, color):
    col.markdown(f"""
<div class="kpi-pill kpi-{color}">
  <div class="kpi-label">{label}</div>
  <div class="kpi-value" style="color:var(--{color})">{value}</div>
  <div class="kpi-sub">{sub}</div>
</div>""", unsafe_allow_html=True)

kpi(c1, "Total Records",     "14,526",    "Sheet1 + Sheet2 merged",  "cyan")
kpi(c2, "Total Fuel Spend",  "KES 285M",  "May 2025 – Dec 2026",     "violet")
kpi(c3, "Avg Efficiency",    "5.842",     "km/L · Full Tank trips",  "gold")
kpi(c4, "Over-EFC Trips",    "89.6%",     "Of trips with benchmark", "coral")
kpi(c5, "GBM R² Score",      "0.9904",    "Champion model · test set","lime")

# ── CRISP-DM ──────────────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:28px'></div>", unsafe_allow_html=True)
sec_header("CRISP-DM Methodology", "6 Phases")

steps = [
    ("1", "Business Understanding"),
    ("2", "Data Understanding"),
    ("3", "Data Preparation"),
    ("4", "Modelling"),
    ("5", "Evaluation"),
    ("6", "Deployment"),
]
cols = st.columns(len(steps) * 2 - 1)
for i, (num, label) in enumerate(steps):
    with cols[i * 2]:
        st.markdown(f"""
<div style="display:flex;flex-direction:column;align-items:center;gap:6px;padding:14px 0">
  <div style="width:30px;height:30px;border-radius:50%;
    background:linear-gradient(135deg,#00E5FF,#B69CFF);
    font-family:'Space Mono',monospace;font-size:12px;font-weight:700;
    color:#08060F;display:flex;align-items:center;justify-content:center">{num}</div>
  <div style="font-size:11px;font-weight:600;color:rgba(240,237,255,.45);
    text-align:center;white-space:nowrap">{label}</div>
</div>""", unsafe_allow_html=True)
    if i < len(steps) - 1:
        with cols[i * 2 + 1]:
            st.markdown(
                '<div style="display:flex;align-items:center;justify-content:center;'
                'height:58px;color:rgba(255,255,255,.2);font-size:18px;margin-top:14px">→</div>',
                unsafe_allow_html=True)

# ── Feature cards ──────────────────────────────────────────────────────────
sec_header("Dashboard Pages", "7 Tabs")

pages = [
    ("📊", "Overview & KPIs",   "rgba(0,229,255,.12)",    "KPI cards, EFC compliance, monthly cost chart."),
    ("📈", "Trends",             "rgba(116,185,255,.12)",  "Monthly trends, 3-month MA, MoM % change."),
    ("🔬", "EDA Figures",        "rgba(182,156,255,.12)",  "All NB1 figures — distributions, correlations, benchmarks."),
    ("🤖", "ML Models",          "rgba(255,209,102,.12)",  "4 model comparison: Ridge, RF, GBM, MLP."),
    ("🚌", "Vehicles",           "rgba(255,107,107,.12)",  "Per-vehicle efficiency grades A–D (VEH-xxx)."),
    ("🗺", "Routes",             "rgba(195,247,58,.12)",   "Route-level efficiency scoring and optimisation."),
    ("🚀", "Deployment",         "rgba(255,107,107,.12)",  "Savings potential, intervention roadmap, KES recovery."),
]

cols = st.columns(4)
for i, (icon, title, bg, desc) in enumerate(pages):
    with cols[i % 4]:
        st.markdown(f"""
<div class="ui-card" style="cursor:pointer">
  <div style="width:38px;height:38px;border-radius:10px;background:{bg};
    display:flex;align-items:center;justify-content:center;
    font-size:18px;margin-bottom:10px">{icon}</div>
  <div style="font-family:'Outfit',sans-serif;font-size:13px;
    font-weight:700;color:#F0EDFF;margin-bottom:5px">{title}</div>
  <div style="font-size:11px;color:rgba(240,237,255,.45);line-height:1.6">{desc}</div>
</div>""", unsafe_allow_html=True)

# ── Savings callout ───────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(90deg,rgba(195,247,58,.08),rgba(0,229,255,.06));
  border:1px solid rgba(195,247,58,.25);border-radius:14px;
  padding:22px 28px;display:flex;align-items:center;gap:20px;margin:8px 0 24px">
  <span style="font-size:36px;flex-shrink:0">💰</span>
  <div style="flex:1">
    <div style="font-family:'Outfit',sans-serif;font-size:16px;font-weight:800;
      color:#F0EDFF;margin-bottom:4px">KES 8.03M Annual Recoverable Savings</div>
    <div style="font-size:13px;color:rgba(240,237,255,.45);line-height:1.55">
      If underperforming vehicles reach the within-type Q3 efficiency target, the fleet can recover
      KES 8.03M/year. Current over-EFC spend totals <strong style="color:#F0EDFF">KES 25.26M</strong>
      — with 89.6% of Full Tank trips exceeding benchmarks.
    </div>
  </div>
  <div style="text-align:right;flex-shrink:0">
    <div style="font-family:'Outfit',sans-serif;font-size:34px;font-weight:900;
      color:#C3F73A;letter-spacing:-.04em">KES 8.03M</div>
    <div style="font-family:'Space Mono',monospace;font-size:9px;
      color:rgba(240,237,255,.22);margin-top:2px">/ year recoverable</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── CTA ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(90deg,rgba(0,229,255,.07),rgba(182,156,255,.07));
  border:1px solid rgba(182,156,255,.2);border-radius:12px;
  padding:16px 22px;display:flex;align-items:center;gap:12px">
  <span style="font-size:20px">👈</span>
  <span style="font-size:14px;color:#F0EDFF">
    <strong style="color:#B69CFF">Select a page from the sidebar</strong>
    to explore trends, vehicles, routes, ML models and deployment savings.
  </span>
</div>
""", unsafe_allow_html=True)

