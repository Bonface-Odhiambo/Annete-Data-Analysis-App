"""
Fleet Fuel Intelligence Dashboard
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

# ── Master CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@300;400;500;600&display=swap');

/* ── Root variables ── */
:root {
  --bg:       #080D18;
  --surf:     #0F1829;
  --surf2:    #162035;
  --border:   #1C2D47;
  --border2:  #243552;
  --accent:   #00E5A0;
  --accent2:  #00B8FF;
  --amber:    #FFB830;
  --red:      #FF3D6B;
  --purple:   #B06EFF;
  --text:     #E8F0FF;
  --muted:    #5A7299;
  --muted2:   #8A9BBB;
}

/* ── Global ── */
.stApp { background-color: var(--bg); color: var(--text); }
* { box-sizing: border-box; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #1a2332 0%, #1f2937 60%, #1a1f2e 100%);
  border-right: 1px solid var(--border);
  min-width: 260px !important;
  z-index: 9999 !important;
  position: relative !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }

/* ── Sidebar brand block ── */
.sb-brand {
  padding: 1.4rem 1.2rem 1rem;
  border-bottom: 1px solid var(--border);
  background: linear-gradient(135deg, rgba(0,229,160,.06) 0%, rgba(0,184,255,.04) 100%);
}
.sb-brand-icon {
  font-size: 2rem;
  line-height: 1;
  margin-bottom: .4rem;
}
.sb-brand-title {
  font-family: 'Syne', sans-serif;
  font-size: 1.05rem;
  font-weight: 800;
  color: var(--text);
  letter-spacing: -.01em;
  line-height: 1.2;
  margin: 0;
}
.sb-brand-sub {
  font-family: 'JetBrains Mono', monospace;
  font-size: .6rem;
  color: var(--accent);
  letter-spacing: .1em;
  text-transform: uppercase;
  margin-top: .3rem;
}

/* ── Sidebar nav section label ── */
.sb-section-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: .52rem;
  letter-spacing: .15em;
  text-transform: uppercase;
  color: var(--muted);
  padding: .9rem 1.2rem .3rem;
}

/* ── Sidebar nav items ── */
.sb-nav-item {
  display: flex;
  align-items: center;
  gap: .75rem;
  padding: .55rem 1.2rem;
  margin: .1rem .5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background .15s, border-color .15s;
  border: 1px solid transparent;
  text-decoration: none;
}
.sb-nav-item:hover {
  background: rgba(0,229,160,.06);
  border-color: rgba(0,229,160,.18);
}
.sb-nav-icon {
  width: 36px; height: 36px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
  border: 1px solid rgba(255,255,255,0.1);
}
.sb-nav-text { font-family: 'Inter', sans-serif; font-size: .82rem; font-weight: 500; color: var(--text); }
.sb-nav-badge {
  margin-left: auto;
  font-family: 'JetBrains Mono', monospace;
  font-size: .55rem;
  color: var(--muted);
  background: var(--surf2);
  border: 1px solid var(--border);
  padding: .1rem .35rem;
  border-radius: 4px;
}

/* Icon background colours */
.ic-teal    { background: rgba(0,229,160,.25); }
.ic-blue    { background: rgba(0,184,255,.25); }
.ic-amber   { background: rgba(255,184,48,.25); }
.ic-red     { background: rgba(255,61,107,.25); }
.ic-purple  { background: rgba(176,110,255,.25); }
.ic-green   { background: rgba(52,211,153,.25); }
.ic-cyan    { background: rgba(34,211,238,.25); }

/* ── Sidebar author card ── */
.sb-author {
  margin: .8rem .5rem;
  padding: .75rem 1rem;
  background: var(--surf2);
  border: 1px solid var(--border);
  border-radius: 10px;
}
.sb-author-name {
  font-family: 'Syne', sans-serif;
  font-size: .82rem;
  font-weight: 700;
  color: var(--text);
}
.sb-author-detail {
  font-family: 'JetBrains Mono', monospace;
  font-size: .58rem;
  color: var(--muted2);
  line-height: 1.7;
  margin-top: .3rem;
}

/* ── Sidebar privacy badge ── */
.sb-privacy {
  margin: .5rem .5rem .8rem;
  padding: .5rem 1rem;
  background: rgba(0,229,160,.04);
  border: 1px solid rgba(0,229,160,.2);
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: .5rem;
}
.sb-privacy-icon { font-size: .9rem; }
.sb-privacy-text {
  font-family: 'JetBrains Mono', monospace;
  font-size: .58rem;
  color: var(--accent);
  letter-spacing: .05em;
  line-height: 1.5;
}

/* ── Home page hero ── */
.hero-wrap {
  background: linear-gradient(135deg, rgba(0,229,160,.05) 0%, rgba(0,184,255,.04) 50%, rgba(176,110,255,.03) 100%);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 2.5rem 2.8rem;
  position: relative;
  overflow: hidden;
  margin-bottom: 1.5rem;
}
.hero-wrap::before {
  content: '';
  position: absolute;
  top: -60px; right: -60px;
  width: 260px; height: 260px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(0,229,160,.08) 0%, transparent 70%);
  pointer-events: none;
}
.hero-eyebrow {
  font-family: 'JetBrains Mono', monospace;
  font-size: .62rem;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: .6rem;
}
.hero-title {
  font-family: 'Syne', sans-serif;
  font-size: 2rem;
  font-weight: 800;
  color: var(--text);
  line-height: 1.18;
  letter-spacing: -.03em;
  margin: 0 0 .5rem;
}
.hero-title span { color: var(--accent); }
.hero-sub {
  font-family: 'Inter', sans-serif;
  font-size: .9rem;
  color: var(--muted2);
  line-height: 1.6;
  max-width: 640px;
  margin-bottom: 1.2rem;
}
.hero-meta {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}
.hero-meta-item {
  font-family: 'JetBrains Mono', monospace;
  font-size: .62rem;
  color: var(--muted);
  letter-spacing: .05em;
}
.hero-meta-item span { color: var(--muted2); }

/* ── Stat pills ── */
.stat-row {
  display: flex;
  gap: .8rem;
  flex-wrap: wrap;
  margin-bottom: 1.5rem;
}
.stat-pill {
  flex: 1;
  min-width: 130px;
  background: var(--surf);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1rem 1.2rem;
  position: relative;
  overflow: hidden;
}
.stat-pill::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0;
  width: 100%; height: 2px;
}
.sp-teal::after   { background: var(--accent); }
.sp-blue::after   { background: var(--accent2); }
.sp-amber::after  { background: var(--amber); }
.sp-red::after    { background: var(--red); }
.sp-purple::after { background: var(--purple); }

.stat-pill-val {
  font-family: 'Syne', sans-serif;
  font-size: 1.6rem;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -.03em;
  margin-bottom: .25rem;
}
.sp-teal .stat-pill-val   { color: var(--accent); }
.sp-blue .stat-pill-val   { color: var(--accent2); }
.sp-amber .stat-pill-val  { color: var(--amber); }
.sp-red .stat-pill-val    { color: var(--red); }
.sp-purple .stat-pill-val { color: var(--purple); }

.stat-pill-label {
  font-family: 'Inter', sans-serif;
  font-size: .72rem;
  color: var(--muted2);
  font-weight: 500;
}
.stat-pill-sub {
  font-family: 'JetBrains Mono', monospace;
  font-size: .55rem;
  color: var(--muted);
  margin-top: .2rem;
}

/* ── Feature cards ── */
.feat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: .8rem;
  margin-bottom: 1.5rem;
}
.feat-card {
  background: var(--surf);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.1rem 1.2rem;
  transition: border-color .2s, transform .2s;
}
.feat-card:hover {
  border-color: var(--border2);
  transform: translateY(-1px);
}
.feat-card-icon {
  font-size: 1.4rem;
  margin-bottom: .5rem;
  display: block;
}
.feat-card-title {
  font-family: 'Syne', sans-serif;
  font-size: .85rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: .25rem;
}
.feat-card-desc {
  font-family: 'Inter', sans-serif;
  font-size: .72rem;
  color: var(--muted2);
  line-height: 1.55;
}

/* ── Methodology strip ── */
.method-strip {
  background: var(--surf);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1rem 1.4rem;
  display: flex;
  align-items: center;
  gap: 1.2rem;
  flex-wrap: wrap;
  margin-bottom: 1.2rem;
}
.method-step {
  display: flex;
  align-items: center;
  gap: .5rem;
  font-family: 'Inter', sans-serif;
  font-size: .72rem;
  color: var(--muted2);
}
.method-step-num {
  width: 20px; height: 20px;
  border-radius: 50%;
  background: var(--accent);
  color: var(--bg);
  font-family: 'JetBrains Mono', monospace;
  font-size: .6rem;
  font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.method-arrow { color: var(--border2); font-size: .8rem; }

/* ── Call to action bar ── */
.cta-bar {
  background: linear-gradient(90deg, rgba(0,229,160,.08) 0%, rgba(0,184,255,.06) 100%);
  border: 1px solid rgba(0,229,160,.2);
  border-radius: 10px;
  padding: .9rem 1.4rem;
  display: flex;
  align-items: center;
  gap: .8rem;
}
.cta-arrow { font-size: 1.2rem; }
.cta-text {
  font-family: 'Inter', sans-serif;
  font-size: .82rem;
  color: var(--text);
}
.cta-text strong { color: var(--accent); }

/* ── Streamlit overrides ── */
h1, h2, h3 { font-family: 'Syne', sans-serif !important; }
.stMetric label { font-family: 'JetBrains Mono', monospace !important; font-size: .6rem !important; }
div[data-testid="stMetricValue"] { font-family: 'Syne', sans-serif !important; font-weight: 800 !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:

    # Brand
    st.markdown("""
    <div class="sb-brand">
      <div class="sb-brand-icon">⛽</div>
      <div class="sb-brand-title">Fleet Fuel<br>Intelligence</div>
      <div class="sb-brand-sub">MSc Dissertation · Strathmore</div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation label
    st.markdown('<div class="sb-section-label">Navigation</div>', unsafe_allow_html=True)

    # Nav items — Streamlit auto-generates page links; we style the sidebar context
    nav_items = [
        ("�", "ic-teal",   "Overview & KPIs",    "KPI summary",    "1"),
        ("📈", "ic-blue",   "Trends",             "Time series",    "2"),
        ("🔎", "ic-purple", "EDA Figures",        "NB1 outputs",    "3"),
        ("🧠", "ic-amber",  "ML Models",          "R²=0.9212",      "4"),
        ("🚐", "ic-red",    "Vehicles",           "VEH-xxx scores", "5"),
        ("🗺️", "ic-cyan",   "Routes",             "Route analysis", "6"),
        ("🎯", "ic-green",  "Deployment",         "Savings",        "7"),
    ]

    for icon, ic_cls, label, badge, _ in nav_items:
        st.markdown(f"""
        <div class="sb-nav-item">
          <div class="sb-nav-icon {ic_cls}">{icon}</div>
          <span class="sb-nav-text">{label}</span>
          <span class="sb-nav-badge">{badge}</span>
        </div>
        """, unsafe_allow_html=True)

    # Author card
    st.markdown("""
    <div class="sb-section-label" style="margin-top:.6rem">Researcher</div>
    <div class="sb-author">
      <div class="sb-author-name">Anette Kerubo Joseph</div>
      <div class="sb-author-detail">
        Reg No: 151384<br>
        MSc Data Science &amp; Analytics<br>
        Strathmore University
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Privacy badge
    st.markdown("""
    <div class="sb-privacy">
      <span class="sb-privacy-icon">🔒</span>
      <div class="sb-privacy-text">
        Plates → VEH-xxx<br>
        Drivers → DRV-xxxx<br>
        PII stored separately
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── Home page ──────────────────────────────────────────────────────────────────

# Hero section
st.markdown("""
<div class="hero-wrap">
  <div class="hero-eyebrow">⛽ MSc Dissertation · CRISP-DM · Strathmore University</div>
  <h1 class="hero-title">Fleet Fuel <span>Intelligence</span><br>Dashboard</h1>
  <p class="hero-sub">
    Predictive Modelling for Fuel Efficiency and Fleet Optimisation in Public Transport —
    combining 32,772 anonymised trip records with machine learning to identify
    KES 645M+ in fleet spend patterns and surface actionable savings opportunities.
  </p>
  <div class="hero-meta">
    <span class="hero-meta-item">📅 <span>Jan 2025 – Dec 2026</span></span>
    <span class="hero-meta-item">🚌 <span>32,772 records · 2 data sheets merged</span></span>
    <span class="hero-meta-item">🤖 <span>4 ML models · Champion GB R²=0.9212</span></span>
    <span class="hero-meta-item">🔒 <span>Fully anonymised (VEH-xxx / DRV-xxxx)</span></span>
  </div>
</div>
""", unsafe_allow_html=True)

# KPI stat pills
st.markdown("""
<div class="stat-row">
  <div class="stat-pill sp-teal">
    <div class="stat-pill-val">32,772</div>
    <div class="stat-pill-label">Total Records</div>
    <div class="stat-pill-sub">Sheet1 + Sheet2 merged</div>
  </div>
  <div class="stat-pill sp-blue">
    <div class="stat-pill-val">KES 645M</div>
    <div class="stat-pill-label">Total Fuel Spend</div>
    <div class="stat-pill-sub">Jan 2025 – Dec 2026</div>
  </div>
  <div class="stat-pill sp-amber">
    <div class="stat-pill-val">5.845</div>
    <div class="stat-pill-label">Avg Efficiency (km/L)</div>
    <div class="stat-pill-sub">Full Tank trips</div>
  </div>
  <div class="stat-pill sp-red">
    <div class="stat-pill-val">91.0%</div>
    <div class="stat-pill-label">Over-EFC Trips</div>
    <div class="stat-pill-sub">Of trips with benchmark data</div>
  </div>
  <div class="stat-pill sp-purple">
    <div class="stat-pill-val">R²=0.9212</div>
    <div class="stat-pill-label">Gradient Boosting</div>
    <div class="stat-pill-sub">Champion model</div>
  </div>
</div>
""", unsafe_allow_html=True)

# CRISP-DM methodology strip
st.markdown("""
<div class="method-strip">
  <div class="method-step"><div class="method-step-num">1</div> Business Understanding</div>
  <div class="method-arrow">→</div>
  <div class="method-step"><div class="method-step-num">2</div> Data Understanding</div>
  <div class="method-arrow">→</div>
  <div class="method-step"><div class="method-step-num">3</div> Data Preparation</div>
  <div class="method-arrow">→</div>
  <div class="method-step"><div class="method-step-num">4</div> Modelling</div>
  <div class="method-arrow">→</div>
  <div class="method-step"><div class="method-step-num">5</div> Evaluation</div>
  <div class="method-arrow">→</div>
  <div class="method-step"><div class="method-step-num">6</div> Deployment</div>
</div>
""", unsafe_allow_html=True)

# Feature cards
st.markdown("""
<div class="feat-grid">
  <div class="feat-card">
    <span class="feat-card-icon">�</span>
    <div class="feat-card-title">Overview & KPIs</div>
    <div class="feat-card-desc">Fleet-wide spend, efficiency and EFC compliance across 32,772 records.</div>
  </div>
  <div class="feat-card">
    <span class="feat-card-icon">📈</span>
    <div class="feat-card-title">Trends</div>
    <div class="feat-card-desc">Monthly cost trends, 3-month MA, MoM change and litres-per-trip over time.</div>
  </div>
  <div class="feat-card">
    <span class="feat-card-icon">🔎</span>
    <div class="feat-card-title">EDA Figures</div>
    <div class="feat-card-desc">All Notebook 1 outputs — univariate, vehicle types, correlations, EFC benchmarks.</div>
  </div>
  <div class="feat-card">
    <span class="feat-card-icon">🧠</span>
    <div class="feat-card-title">ML Models</div>
    <div class="feat-card-desc">4 models (Ridge, RF, GBM, MLP) trained on 31,250 rows. Champion: GBM R²=0.9212.</div>
  </div>
  <div class="feat-card">
    <span class="feat-card-icon">🚐</span>
    <div class="feat-card-title">Vehicles</div>
    <div class="feat-card-desc">Per-vehicle efficiency scores, grades A–D, and cost breakdown. VEH-xxx anonymised.</div>
  </div>
  <div class="feat-card">
    <span class="feat-card-icon">🗺️</span>
    <div class="feat-card-title">Routes</div>
    <div class="feat-card-desc">Route-level efficiency scoring and consistency analysis across all vehicle types.</div>
  </div>
  <div class="feat-card">
    <span class="feat-card-icon">🎯</span>
    <div class="feat-card-title">Deployment</div>
    <div class="feat-card-desc">Savings potential, vehicles below benchmark, monthly and annual KES recovery estimates.</div>
  </div>
</div>
""", unsafe_allow_html=True)

# CTA
st.markdown("""
<div class="cta-bar">
  <span class="cta-arrow">👈</span>
  <span class="cta-text"><strong>Select a page from the sidebar</strong> to begin exploring the dashboard.</span>
</div>
""", unsafe_allow_html=True)
