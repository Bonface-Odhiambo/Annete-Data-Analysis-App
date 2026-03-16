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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@300;400;500;600&display=swap');

:root {
  --bg:      #0B0914;
  --surf:    #130D20;
  --surf2:   #1A1230;
  --border:  #2A1D45;
  --border2: #3A2860;
  --v1:      #A78BFA;
  --v2:      #7C3AED;
  --teal:    #2DD4BF;
  --pink:    #F472B6;
  --amber:   #FCD34D;
  --red:     #F87171;
  --sky:     #38BDF8;
  --green:   #34D399;
  --text:    #EDE9FE;
  --muted:   #6D5FA0;
  --muted2:  #A99BC8;
}

.stApp { background-color: var(--bg); color: var(--text); }
* { box-sizing: border-box; }

section[data-testid="stSidebar"] {
  background: linear-gradient(180deg,#0D0A1C 0%,#110E24 50%,#0A0816 100%) !important;
  border-right: 1px solid var(--border) !important;
  min-width: 268px !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }

.sb-brand {
  padding: 1.5rem 1.2rem 1.1rem;
  border-bottom: 1px solid var(--border);
  background: linear-gradient(135deg,rgba(167,139,250,.07) 0%,rgba(45,212,191,.04) 100%);
}
.sb-logo {
  width: 42px; height: 42px; border-radius: 12px;
  background: linear-gradient(135deg,#7C3AED,#2DD4BF);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.3rem; margin-bottom: .7rem;
}
.sb-brand-title {
  font-family:'Syne',sans-serif; font-size:1.05rem; font-weight:800;
  color:var(--text); letter-spacing:-.01em; line-height:1.2; margin:0;
}
.sb-brand-sub {
  font-family:'JetBrains Mono',monospace; font-size:.58rem;
  color:var(--teal); letter-spacing:.12em; text-transform:uppercase; margin-top:.35rem;
}

.sb-section-label {
  font-family:'JetBrains Mono',monospace; font-size:.5rem;
  letter-spacing:.18em; text-transform:uppercase;
  color:var(--muted); padding:.9rem 1.2rem .35rem;
}

.sb-nav-item {
  display:flex; align-items:center; gap:.7rem;
  padding:.52rem 1rem; margin:.06rem .5rem;
  border-radius:10px; border:1px solid transparent;
  transition:background .15s,border-color .15s;
}
.sb-nav-item:hover { background:rgba(167,139,250,.08); border-color:rgba(167,139,250,.22); }
.sb-nav-icon {
  width:34px; height:34px; border-radius:9px;
  display:flex; align-items:center; justify-content:center; flex-shrink:0;
}
.sb-nav-text { font-family:'Inter',sans-serif; font-size:.82rem; font-weight:500; color:var(--text); }
.sb-nav-badge {
  margin-left:auto;
  font-family:'JetBrains Mono',monospace; font-size:.53rem;
  color:var(--muted); background:var(--surf2);
  border:1px solid var(--border); padding:.1rem .38rem; border-radius:5px;
}

.sb-author {
  margin:.7rem .5rem .4rem;
  padding:.75rem 1rem;
  background:var(--surf2); border:1px solid var(--border); border-radius:11px;
}
.sb-author-name { font-family:'Syne',sans-serif; font-size:.82rem; font-weight:700; color:var(--text); }
.sb-author-detail {
  font-family:'JetBrains Mono',monospace; font-size:.56rem;
  color:var(--muted2); line-height:1.75; margin-top:.3rem;
}
.sb-privacy {
  margin:.4rem .5rem .9rem;
  padding:.5rem 1rem;
  background:rgba(45,212,191,.05); border:1px solid rgba(45,212,191,.22); border-radius:9px;
  display:flex; align-items:flex-start; gap:.55rem;
}
.sb-privacy-icon { font-size:.95rem; margin-top:.05rem; }
.sb-privacy-text {
  font-family:'JetBrains Mono',monospace; font-size:.57rem;
  color:var(--teal); letter-spacing:.04em; line-height:1.65;
}

/* ── Home hero ── */
.hero-wrap {
  background: linear-gradient(135deg,rgba(124,58,237,.08) 0%,rgba(45,212,191,.05) 50%,rgba(244,114,182,.04) 100%);
  border:1px solid var(--border); border-radius:18px;
  padding:2.6rem 3rem; position:relative; overflow:hidden; margin-bottom:1.4rem;
}
.hero-wrap::before {
  content:''; position:absolute; top:-80px; right:-80px;
  width:300px; height:300px; border-radius:50%;
  background:radial-gradient(circle,rgba(124,58,237,.12) 0%,transparent 70%);
  pointer-events:none;
}
.hero-wrap::after {
  content:''; position:absolute; bottom:-60px; left:20%;
  width:200px; height:200px; border-radius:50%;
  background:radial-gradient(circle,rgba(45,212,191,.07) 0%,transparent 70%);
  pointer-events:none;
}
.hero-eyebrow {
  font-family:'JetBrains Mono',monospace; font-size:.62rem;
  letter-spacing:.2em; text-transform:uppercase; color:var(--v1); margin-bottom:.65rem;
}
.hero-title {
  font-family:'Syne',sans-serif; font-size:2.1rem; font-weight:800;
  color:var(--text); line-height:1.16; letter-spacing:-.03em; margin:0 0 .55rem;
}
.hero-title .hl { color:var(--teal); }
.hero-sub {
  font-family:'Inter',sans-serif; font-size:.9rem;
  color:var(--muted2); line-height:1.65; max-width:620px; margin-bottom:1.3rem;
}
.hero-meta { display:flex; gap:1.6rem; flex-wrap:wrap; }
.hero-meta-item {
  font-family:'JetBrains Mono',monospace; font-size:.6rem;
  color:var(--muted); letter-spacing:.04em;
}
.hero-meta-item span { color:var(--muted2); }

/* ── Stat pills ── */
.stat-row { display:flex; gap:.8rem; flex-wrap:wrap; margin-bottom:1.4rem; }
.stat-pill {
  flex:1; min-width:125px; background:var(--surf);
  border:1px solid var(--border); border-radius:14px;
  padding:1.1rem 1.2rem; position:relative; overflow:hidden;
}
.stat-pill::after {
  content:''; position:absolute; bottom:0; left:0; width:100%; height:2.5px;
}
.sp-v::after  { background:linear-gradient(90deg,var(--v2),var(--v1)); }
.sp-t::after  { background:linear-gradient(90deg,#0F766E,var(--teal)); }
.sp-a::after  { background:linear-gradient(90deg,#B45309,var(--amber)); }
.sp-r::after  { background:linear-gradient(90deg,#B91C1C,var(--red)); }
.sp-p::after  { background:linear-gradient(90deg,var(--v2),var(--pink)); }

.stat-pill-val {
  font-family:'Syne',sans-serif; font-size:1.55rem; font-weight:800;
  line-height:1; letter-spacing:-.03em; margin-bottom:.28rem;
}
.sp-v .stat-pill-val { color:var(--v1); }
.sp-t .stat-pill-val { color:var(--teal); }
.sp-a .stat-pill-val { color:var(--amber); }
.sp-r .stat-pill-val { color:var(--red); }
.sp-p .stat-pill-val { color:var(--pink); }
.stat-pill-label { font-family:'Inter',sans-serif; font-size:.72rem; color:var(--muted2); font-weight:500; }
.stat-pill-sub { font-family:'JetBrains Mono',monospace; font-size:.54rem; color:var(--muted); margin-top:.2rem; }

/* ── CRISP-DM strip ── */
.method-strip {
  background:var(--surf); border:1px solid var(--border); border-radius:12px;
  padding:1rem 1.4rem; display:flex; align-items:center;
  gap:1rem; flex-wrap:wrap; margin-bottom:1.4rem;
}
.method-step { display:flex; align-items:center; gap:.5rem;
  font-family:'Inter',sans-serif; font-size:.7rem; color:var(--muted2); }
.method-step-num {
  width:20px; height:20px; border-radius:50%;
  background:linear-gradient(135deg,var(--v2),var(--v1));
  color:#fff; font-family:'JetBrains Mono',monospace;
  font-size:.58rem; font-weight:700;
  display:flex; align-items:center; justify-content:center; flex-shrink:0;
}
.method-arrow { color:var(--border2); font-size:.75rem; }

/* ── Feature cards ── */
.feat-grid {
  display:grid; grid-template-columns:repeat(auto-fit,minmax(195px,1fr));
  gap:.8rem; margin-bottom:1.4rem;
}
.feat-card {
  background:var(--surf); border:1px solid var(--border); border-radius:13px;
  padding:1.1rem 1.2rem; transition:border-color .2s,transform .18s;
}
.feat-card:hover { border-color:var(--border2); transform:translateY(-2px); }
.feat-card-icon {
  width:36px; height:36px; border-radius:9px; margin-bottom:.55rem;
  display:flex; align-items:center; justify-content:center;
}
.feat-card-title { font-family:'Syne',sans-serif; font-size:.85rem; font-weight:700; color:var(--text); margin-bottom:.25rem; }
.feat-card-desc { font-family:'Inter',sans-serif; font-size:.71rem; color:var(--muted2); line-height:1.55; }

/* ── CTA ── */
.cta-bar {
  background:linear-gradient(90deg,rgba(124,58,237,.1) 0%,rgba(45,212,191,.07) 100%);
  border:1px solid rgba(167,139,250,.25); border-radius:11px;
  padding:.95rem 1.4rem; display:flex; align-items:center; gap:.8rem;
}
.cta-text { font-family:'Inter',sans-serif; font-size:.83rem; color:var(--text); }
.cta-text strong { color:var(--v1); }

/* ── Streamlit overrides ── */
h1,h2,h3 { font-family:'Syne',sans-serif !important; }
.stMetric label { font-family:'JetBrains Mono',monospace !important; font-size:.6rem !important; letter-spacing:.05em !important; }
div[data-testid="stMetricValue"] { font-family:'Syne',sans-serif !important; font-weight:800 !important; color:var(--text) !important; }
footer { display:none !important; }
#MainMenu { display:none !important; }
</style>
""", unsafe_allow_html=True)

# ── SVG icon helpers ──────────────────────────────────────────────────────────
def svg_icon(path_d, color, size=18):
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none"
      xmlns="http://www.w3.org/2000/svg" style="flex-shrink:0">
      <path d="{path_d}" stroke="{color}" stroke-width="1.8"
        stroke-linecap="round" stroke-linejoin="round"/>
    </svg>'''

ICONS = {
    # Grid/dashboard — Overview
    "overview": "M3 3h7v7H3V3zm0 11h7v7H3v-7zm11-11h7v7h-7V3zm0 11h7v7h-7v-7z",
    # Line chart — Trends
    "trends":   "M3 17l4-8 4 4 4-6 4 4 3-6",
    # Microscope/flask — EDA
    "eda":      "M9 3h6m-3 0v7m-5 4l-2 7h14l-2-7M9 10h6",
    # CPU/brain — ML Models
    "ml":       "M12 2a4 4 0 014 4v1h1a2 2 0 010 4h-1v1a4 4 0 01-4 4H8a4 4 0 01-4-4v-1H3a2 2 0 010-4h1V6a4 4 0 014-4h4zM9 9h.01M15 9h.01M9 13h6",
    # Car — Vehicles
    "vehicles": "M5 17H3v-5l2-5h14l2 5v5h-2m-1 0H7m0 0a2 2 0 100 4 2 2 0 000-4zm10 0a2 2 0 100 4 2 2 0 000-4z",
    # Map pin — Routes
    "routes":   "M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 010-5 2.5 2.5 0 010 5z",
    # Rocket — Deployment
    "deploy":   "M12 2l2.4 7.4H22l-6.2 4.5 2.4 7.4L12 17l-6.2 4.3 2.4-7.4L2 9.4h7.6L12 2z",
}

# icon bg colours
IC_BG = {
    "overview": ("rgba(45,212,191,.15)",  "#2DD4BF"),
    "trends":   ("rgba(56,189,248,.15)",  "#38BDF8"),
    "eda":      ("rgba(167,139,250,.15)", "#A78BFA"),
    "ml":       ("rgba(252,211,77,.15)",  "#FCD34D"),
    "vehicles": ("rgba(244,114,182,.15)", "#F472B6"),
    "routes":   ("rgba(52,211,153,.15)",  "#34D399"),
    "deploy":   ("rgba(248,113,113,.15)", "#F87171"),
}

def nav_item(key, label, badge):
    bg, clr = IC_BG[key]
    icon_svg = svg_icon(ICONS[key], clr, 16)
    return f"""
    <div class="sb-nav-item">
      <div class="sb-nav-icon" style="background:{bg}">{icon_svg}</div>
      <span class="sb-nav-text">{label}</span>
      <span class="sb-nav-badge">{badge}</span>
    </div>"""

def feat_icon(key):
    bg, clr = IC_BG[key]
    return f'<div class="feat-card-icon" style="background:{bg}">{svg_icon(ICONS[key],clr,18)}</div>'

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
      <div class="sb-logo">⛽</div>
      <div class="sb-brand-title">Fleet Fuel<br>Intelligence</div>
      <div class="sb-brand-sub">MSc · Strathmore University</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sb-section-label">Pages</div>', unsafe_allow_html=True)

    pages = [
        ("overview", "Overview & KPIs",  "KPIs"),
        ("trends",   "Trends",           "Time"),
        ("eda",      "EDA Figures",      "NB1"),
        ("ml",       "ML Models",        "R²=0.9212"),
        ("vehicles", "Vehicles",         "VEH-xxx"),
        ("routes",   "Routes",           "Analysis"),
        ("deploy",   "Deployment",       "Savings"),
    ]
    for key, label, badge in pages:
        st.markdown(nav_item(key, label, badge), unsafe_allow_html=True)

    st.markdown("""
    <div class="sb-section-label" style="margin-top:.5rem">Researcher</div>
    <div class="sb-author">
      <div class="sb-author-name">Anette Kerubo Joseph</div>
      <div class="sb-author-detail">
        Reg No: 151384<br>
        MSc Data Science &amp; Analytics<br>
        Strathmore University
      </div>
    </div>
    <div class="sb-privacy">
      <span class="sb-privacy-icon">🔒</span>
      <div class="sb-privacy-text">
        Plates → VEH-xxx codes<br>
        Drivers → DRV-xxxx codes<br>
        PII stored separately &amp; securely
      </div>
    </div>""", unsafe_allow_html=True)

# ── Home page ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div class="hero-eyebrow">⛽ MSc Dissertation &nbsp;·&nbsp; CRISP-DM &nbsp;·&nbsp; Strathmore University</div>
  <h1 class="hero-title">Fleet Fuel <span class="hl">Intelligence</span><br>Dashboard</h1>
  <p class="hero-sub">
    Predictive Modelling for Fuel Efficiency and Fleet Optimisation in Public Transport —
    combining 32,772 anonymised trip records with machine learning to surface KES 645M+ in
    fleet spend patterns and actionable savings opportunities.
  </p>
  <div class="hero-meta">
    <span class="hero-meta-item">📅 <span>Jan 2025 – Dec 2026</span></span>
    <span class="hero-meta-item">🚌 <span>32,772 records &nbsp;·&nbsp; 2 sheets merged</span></span>
    <span class="hero-meta-item">🤖 <span>4 ML models &nbsp;·&nbsp; GB R²=0.9212</span></span>
    <span class="hero-meta-item">🔒 <span>Fully anonymised (VEH-xxx / DRV-xxxx)</span></span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="stat-row">
  <div class="stat-pill sp-t">
    <div class="stat-pill-val">32,772</div>
    <div class="stat-pill-label">Total Records</div>
    <div class="stat-pill-sub">Sheet1 + Sheet2 merged</div>
  </div>
  <div class="stat-pill sp-v">
    <div class="stat-pill-val">KES 645M</div>
    <div class="stat-pill-label">Total Fuel Spend</div>
    <div class="stat-pill-sub">Jan 2025 – Dec 2026</div>
  </div>
  <div class="stat-pill sp-a">
    <div class="stat-pill-val">5.845</div>
    <div class="stat-pill-label">Avg Efficiency (km/L)</div>
    <div class="stat-pill-sub">Full Tank trips</div>
  </div>
  <div class="stat-pill sp-r">
    <div class="stat-pill-val">91.0%</div>
    <div class="stat-pill-label">Over-EFC Trips</div>
    <div class="stat-pill-sub">Of trips with benchmark</div>
  </div>
  <div class="stat-pill sp-p">
    <div class="stat-pill-val">R²=0.9212</div>
    <div class="stat-pill-label">Gradient Boosting</div>
    <div class="stat-pill-sub">Champion model</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="method-strip">
  <div class="method-step"><div class="method-step-num">1</div>Business Understanding</div>
  <div class="method-arrow">→</div>
  <div class="method-step"><div class="method-step-num">2</div>Data Understanding</div>
  <div class="method-arrow">→</div>
  <div class="method-step"><div class="method-step-num">3</div>Data Preparation</div>
  <div class="method-arrow">→</div>
  <div class="method-step"><div class="method-step-num">4</div>Modelling</div>
  <div class="method-arrow">→</div>
  <div class="method-step"><div class="method-step-num">5</div>Evaluation</div>
  <div class="method-arrow">→</div>
  <div class="method-step"><div class="method-step-num">6</div>Deployment</div>
</div>
""", unsafe_allow_html=True)

# ── Feature cards ─────────────────────────────────────────────────────────────
feat_cards = [
    ("overview", "Overview & KPIs",  "32,772 records · KES 645M spend · EFC compliance across full fleet."),
    ("trends",   "Trends",           "Monthly cost trends, 3-month MA, MoM % change and litres-per-trip."),
    ("eda",      "EDA Figures",      "All Notebook 1 outputs — univariate, vehicle types, correlations, benchmarks."),
    ("ml",       "ML Models",        "4 models (Ridge, RF, GBM, MLP) on 31,250 rows. Champion: GBM R²=0.9212."),
    ("vehicles", "Vehicles",         "Per-vehicle efficiency grades A–D and cost breakdown. VEH-xxx anonymised."),
    ("routes",   "Routes",           "Route-level efficiency scoring and consistency across all vehicle types."),
    ("deploy",   "Deployment",       "Savings potential, below-benchmark vehicles, monthly KES recovery estimates."),
]

cards_html = '<div class="feat-grid">'
for key, title, desc in feat_cards:
    bg, clr = IC_BG[key]
    icon_svg = svg_icon(ICONS[key], clr, 18)
    cards_html += (
        f'<div class="feat-card">'
        f'<div class="feat-card-icon" style="background:{bg}">{icon_svg}</div>'
        f'<div class="feat-card-title">{title}</div>'
        f'<div class="feat-card-desc">{desc}</div>'
        f'</div>'
    )
cards_html += '</div>'
st.markdown(cards_html, unsafe_allow_html=True)

# ── CTA ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cta-bar">
  <span style="font-size:1.1rem">👈</span>
  <span class="cta-text"><strong>Select a page from the sidebar</strong> to begin exploring the dashboard.</span>
</div>
""", unsafe_allow_html=True)
