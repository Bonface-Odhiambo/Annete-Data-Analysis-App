"""
theme.py — single source of truth for all visual styling.
Every page imports inject_css() and page_header() from here.
"""

import streamlit as st

# ── Colour tokens (match dashboard.html) ────────────────────────────────────
CYAN   = "#00E5FF"
GOLD   = "#FFD166"
CORAL  = "#FF6B6B"
LIME   = "#C3F73A"
VIOLET = "#B69CFF"
SKY    = "#74B9FF"
SNOW   = "#F0EDFF"
MUTED  = "rgba(240,237,255,.45)"

BG     = "#08060F"
DEEP   = "#0F0B1E"
MID    = "#1A1530"
RIM    = "rgba(255,255,255,.08)"
RIM2   = "rgba(255,255,255,.14)"

PALETTE = [CYAN, VIOLET, GOLD, CORAL, LIME, SKY]

TYPE_COLORS = {"Bus": CORAL, "Shuttle": SKY, "Eph": GOLD, "Admin": VIOLET, "Unknown": MUTED}

# Plotly layout defaults
PLOTLY_LAYOUT = dict(
    paper_bgcolor=MID,
    plot_bgcolor="#13102A",
    font=dict(color=SNOW, family="Space Mono, monospace", size=11),
    margin=dict(l=48, r=24, t=48, b=40),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        bordercolor=RIM,
        font=dict(color=MUTED),
    ),
)
AXIS_STYLE = dict(gridcolor="rgba(255,255,255,.06)", color=MUTED, linecolor=RIM)


def apply_plotly(fig, title="", height=360):
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text=title, font=dict(color=SNOW, size=13, family="Outfit, sans-serif")),
        height=height,
    )
    fig.update_xaxes(**AXIS_STYLE)
    fig.update_yaxes(**AXIS_STYLE)
    return fig


# ── CSS ──────────────────────────────────────────────────────────────────────
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Space+Mono:wght@400;700&display=swap');

/* ── root / body ── */
:root {
  --cyan:   #00E5FF;
  --gold:   #FFD166;
  --coral:  #FF6B6B;
  --lime:   #C3F73A;
  --violet: #B69CFF;
  --sky:    #74B9FF;
  --snow:   #F0EDFF;
  --muted:  rgba(240,237,255,.45);
  --faint:  rgba(240,237,255,.22);
  --bg:     #08060F;
  --deep:   #0F0B1E;
  --mid:    #1A1530;
  --rim:    rgba(255,255,255,.08);
  --rim2:   rgba(255,255,255,.14);
}

html, body, .stApp {
  background-color: var(--bg) !important;
  color: var(--snow) !important;
}

/* ── sidebar ── */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #110D20 0%, #0D0A1C 100%) !important;
  border-right: 1px solid var(--rim) !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }

/* ── headings ── */
h1, h2, h3, h4, h5, h6 {
  font-family: 'Outfit', sans-serif !important;
  color: var(--snow) !important;
}

/* ── metrics ── */
[data-testid="stMetric"] {
  background: var(--mid);
  border: 1px solid var(--rim);
  border-radius: 14px;
  padding: 18px 20px 14px !important;
}
[data-testid="stMetric"] label {
  font-family: 'Space Mono', monospace !important;
  font-size: 9px !important;
  letter-spacing: .1em !important;
  text-transform: uppercase !important;
  color: var(--faint) !important;
}
[data-testid="stMetricValue"] {
  font-family: 'Outfit', sans-serif !important;
  font-weight: 900 !important;
  font-size: 1.9rem !important;
  color: var(--snow) !important;
}
[data-testid="stMetricDelta"] {
  font-family: 'Space Mono', monospace !important;
  font-size: 10px !important;
}

/* ── tabs ── */
[data-testid="stTabs"] button {
  font-family: 'Space Mono', monospace !important;
  font-size: 11px !important;
  letter-spacing: .06em !important;
  color: var(--faint) !important;
  border-radius: 8px 8px 0 0 !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
  color: var(--cyan) !important;
  border-bottom-color: var(--cyan) !important;
}

/* ── dataframe / table ── */
[data-testid="stDataFrame"] {
  border: 1px solid var(--rim) !important;
  border-radius: 12px !important;
  overflow: hidden;
}

/* ── buttons ── */
.stButton > button {
  background: rgba(0,229,255,.1) !important;
  color: var(--cyan) !important;
  border: 1px solid rgba(0,229,255,.3) !important;
  border-radius: 8px !important;
  font-family: 'Space Mono', monospace !important;
  font-size: 11px !important;
}
.stButton > button:hover {
  background: rgba(0,229,255,.2) !important;
  border-color: var(--cyan) !important;
}

/* ── selectbox / inputs ── */
[data-baseweb="select"] > div,
[data-baseweb="input"] > div {
  background: var(--mid) !important;
  border-color: var(--rim) !important;
  color: var(--snow) !important;
}

/* ── spinner text ── */
[data-testid="stSpinner"] p { color: var(--muted) !important; }

/* ── hide footer / menu ── */
footer, #MainMenu { display: none !important; }

/* ── divider ── */
hr { border-color: var(--rim) !important; }

/* ── card helper ── */
.ui-card {
  background: var(--mid);
  border: 1px solid var(--rim);
  border-radius: 14px;
  padding: 20px 22px;
  margin-bottom: 14px;
}
.ui-card:hover { border-color: var(--rim2); }

/* ── kpi pill ── */
.kpi-pill {
  background: var(--mid);
  border: 1px solid var(--rim);
  border-radius: 14px;
  padding: 18px 20px 14px;
  position: relative; overflow: hidden;
}
.kpi-pill::after {
  content:''; position:absolute; bottom:0; left:0; right:0; height:3px;
}
.kpi-cyan::after   { background: linear-gradient(90deg,#007A8C,var(--cyan)); }
.kpi-violet::after { background: linear-gradient(90deg,#5B3FA0,var(--violet)); }
.kpi-gold::after   { background: linear-gradient(90deg,#A8610A,var(--gold)); }
.kpi-coral::after  { background: linear-gradient(90deg,#9C1C1C,var(--coral)); }
.kpi-lime::after   { background: linear-gradient(90deg,#5A7200,var(--lime)); }

.kpi-label {
  font-family: 'Space Mono', monospace; font-size: 9px;
  letter-spacing: .1em; text-transform: uppercase; color: var(--faint); margin-bottom: 6px;
}
.kpi-value { font-family:'Outfit',sans-serif; font-size:26px; font-weight:900; letter-spacing:-.03em; }
.kpi-sub   { font-family:'Space Mono',monospace; font-size:9px; color:var(--faint); margin-top:3px; }

/* ── section header ── */
.sec-hdr {
  display: flex; align-items: center; gap: 12px;
  margin: 28px 0 16px;
}
.sec-title { font-family:'Outfit',sans-serif; font-size:17px; font-weight:800; color:var(--snow); }
.sec-line  { flex:1; height:1px; background:linear-gradient(90deg,var(--rim2),transparent); }
.sec-tag   {
  font-family:'Space Mono',monospace; font-size:9px;
  color:var(--faint); background:var(--rim); border:1px solid var(--rim2);
  padding:3px 8px; border-radius:20px;
}

/* ── insight box ── */
.insight-box {
  background: rgba(0,229,255,.05);
  border: 1px solid rgba(0,229,255,.18);
  border-radius: 12px; padding: 14px 18px;
  font-family: 'Space Mono', monospace; font-size: 11px;
  color: var(--muted); line-height: 1.7; margin: 12px 0;
}
.insight-box strong { color: var(--cyan); }

/* ── grade badge ── */
.grade-A { color:#C3F73A; font-weight:800; }
.grade-B { color:#00E5FF; font-weight:700; }
.grade-C { color:#FFD166; font-weight:700; }
.grade-D { color:#FF6B6B; font-weight:700; }
</style>
"""


def inject_css():
    """Call once at the top of every page."""
    st.markdown(_CSS, unsafe_allow_html=True)


def page_header(icon: str, title: str, subtitle: str, tag: str = ""):
    """Render a consistent page header banner."""
    tag_html = f'<span class="sec-tag" style="font-size:10px;padding:4px 12px">{tag}</span>' if tag else ""
    st.markdown(f"""
<div class="ui-card" style="margin-bottom:22px;
     background:linear-gradient(135deg,rgba(0,229,255,.06),rgba(182,156,255,.04));">
  <div style="display:flex;align-items:center;gap:14px;margin-bottom:8px">
    <span style="font-size:28px">{icon}</span>
    <div>
      <div style="font-family:'Outfit',sans-serif;font-size:22px;font-weight:900;
                  letter-spacing:-.03em;color:var(--snow)">{title}</div>
      <div style="font-family:'Space Mono',monospace;font-size:10px;
                  color:var(--faint);margin-top:3px">{subtitle}</div>
    </div>
    {tag_html}
  </div>
</div>
""", unsafe_allow_html=True)


def sec_header(title: str, tag: str = ""):
    tag_html = f'<div class="sec-tag">{tag}</div>' if tag else ""
    st.markdown(f"""
<div class="sec-hdr">
  <div class="sec-title">{title}</div>
  <div class="sec-line"></div>
  {tag_html}
</div>
""", unsafe_allow_html=True)


def kpi_row(cards: list):
    """
    cards = [{"label","value","sub","color"}]  color in cyan/violet/gold/coral/lime
    """
    cols_html = ""
    for c in cards:
        cols_html += f"""
<div class="kpi-pill kpi-{c['color']}" style="flex:1;min-width:130px">
  <div class="kpi-label">{c['label']}</div>
  <div class="kpi-value" style="color:var(--{c['color']})">{c['value']}</div>
  <div class="kpi-sub">{c.get('sub','')}</div>
</div>"""
    st.markdown(
        f'<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:20px">{cols_html}</div>',
        unsafe_allow_html=True,
    )


def insight(text: str):
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)


def sidebar_brand():
    st.sidebar.markdown("""
<div style="padding:24px 18px 18px;border-bottom:1px solid rgba(255,255,255,.08)">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px">
    <div style="width:42px;height:42px;border-radius:13px;
                background:linear-gradient(135deg,#00E5FF,#B69CFF);
                display:flex;align-items:center;justify-content:center;
                font-size:20px;box-shadow:0 0 20px rgba(0,229,255,.3)">⛽</div>
    <div>
      <div style="font-family:'Outfit',sans-serif;font-size:15px;font-weight:900;
                  color:#F0EDFF;letter-spacing:-.02em;line-height:1.2">
        Fleet Fuel<br>Intelligence</div>
      <div style="font-family:'Space Mono',monospace;font-size:9px;
                  color:#00E5FF;letter-spacing:.14em;text-transform:uppercase;margin-top:4px">
        MSc · Strathmore</div>
    </div>
  </div>
  <div style="background:rgba(0,229,255,.06);border:1px solid rgba(0,229,255,.15);
              border-radius:10px;padding:11px 13px">
    <div style="font-family:'Outfit',sans-serif;font-size:12px;font-weight:700;color:#F0EDFF">
      Anette Kerubo Joseph</div>
    <div style="font-family:'Space Mono',monospace;font-size:9px;
                color:rgba(240,237,255,.45);line-height:1.9;margin-top:4px">
      Reg No: 151384<br>MSc Data Science &amp; Analytics<br>Strathmore University</div>
  </div>
</div>
<div style="margin:10px 6px 0;padding:9px 12px;
            background:rgba(195,247,58,.05);border:1px solid rgba(195,247,58,.18);
            border-radius:10px;display:flex;gap:8px;align-items:flex-start">
  <span style="font-size:13px">🔒</span>
  <div style="font-family:'Space Mono',monospace;font-size:9px;
              color:#C3F73A;line-height:1.75">
    Plates → VEH-001…VEH-228<br>
    Drivers → DRV-001…DRV-1465<br>
    PII stored securely &amp; separately</div>
</div>
""", unsafe_allow_html=True)
