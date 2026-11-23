import streamlit as st

SMARTROLL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root {
  --sr-bg: #0b1120;
  --sr-surface: #111c30;
  --sr-surface-2: #172338;
  --sr-border: #26364e;
  --sr-text: #f1f5f9;
  --sr-muted: #94a3b8;
  --sr-blue: #3b82f6;
  --sr-cyan: #22d3ee;
  --sr-purple: #818cf8;
}
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: radial-gradient(ellipse at 15% 0%, #14294a 0%, transparent 38%), var(--sr-bg); color: var(--sr-text); }

/* Hide Streamlit's top bar, toolbar/menu, deploy button, decoration and footer */
header[data-testid="stHeader"] { display: none !important; height: 0 !important; }
[data-testid="stToolbar"] { display: none !important; visibility: hidden !important; }
[data-testid="stMainMenu"] { display: none !important; }
.stDeployButton { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; height: 0 !important; }

.block-container { padding-top: 1rem; padding-bottom: 2.5rem; max-width: 1400px; }
section[data-testid="stSidebar"] { background: #0a1020; border-right: 1px solid var(--sr-border); }
section[data-testid="stSidebar"] * { color: var(--sr-text); }
h1, h2, h3, h4 { font-family: 'Inter', sans-serif !important; letter-spacing: -0.035em; color: var(--sr-text) !important; }
h1 { font-size: 2.35rem !important; font-weight: 800 !important; }
h2 { font-size: 1.8rem !important; font-weight: 750 !important; }
h3 { font-size: 1.35rem !important; font-weight: 700 !important; }
h4 { font-size: 1.1rem !important; font-weight: 650 !important; }
p, label, .stMarkdown { color: var(--sr-text); }
small, [data-testid="stCaptionContainer"] { color: var(--sr-muted) !important; }
hr { border-color: var(--sr-border) !important; }
[data-testid="stVerticalBlockBorderWrapper"] { border-color: var(--sr-border) !important; }
[data-testid="stMetric"] { background: linear-gradient(145deg, var(--sr-surface), var(--sr-surface-2)); border: 1px solid var(--sr-border); padding: 1rem 1.1rem; border-radius: 16px; }
[data-testid="stMetricLabel"] { color: var(--sr-muted) !important; }
[data-testid="stMetricValue"] { color: var(--sr-text) !important; }
[data-testid="stDataFrame"] { border: 1px solid var(--sr-border); border-radius: 12px; overflow: hidden; }
[data-testid="stSelectbox"], [data-testid="stMultiSelect"], [data-testid="stTextInput"], [data-testid="stTextArea"], [data-testid="stDateInput"], [data-testid="stNumberInput"] { background: transparent; }
input, textarea { background: var(--sr-surface) !important; color: var(--sr-text) !important; }
[data-baseweb="select"] > div, [data-baseweb="input"] > div { background: var(--sr-surface) !important; border-color: var(--sr-border) !important; border-radius: 10px !important; }
.stButton > button, [data-testid="stFormSubmitButton"] button { border-radius: 10px !important; border: 1px solid transparent !important; font-weight: 600 !important; transition: all .18s ease !important; min-height: 2.55rem; }
.stButton > button[kind="primary"], [data-testid="stFormSubmitButton"] button { background: linear-gradient(100deg, var(--sr-blue), #2563eb) !important; color: white !important; }
.stButton > button[kind="secondary"] { background: var(--sr-surface-2) !important; border-color: var(--sr-border) !important; color: var(--sr-text) !important; }
.stButton > button[kind="tertiary"] { background: transparent !important; color: var(--sr-muted) !important; }
.stButton > button:hover { border-color: #60a5fa !important; transform: translateY(-1px); box-shadow: 0 5px 18px #2563eb25; }
.stButton > button:disabled { opacity: .45; }
[data-testid="stAlert"] { border-radius: 12px; }
[data-testid="stTabs"] button { color: var(--sr-muted) !important; }
[data-testid="stTabs"] button[aria-selected="true"] { color: #60a5fa !important; }
[data-testid="stDialog"] > div { background: var(--sr-surface) !important; border: 1px solid var(--sr-border); border-radius: 18px; }
[data-testid="stImage"] img { border-radius: 14px; }
/* Subtle containers; do not style every Streamlit column as a card. */
[data-testid="stVerticalBlock"] > [data-testid="stElementContainer"] { color: var(--sr-text); }
@media (max-width: 768px) {
  .block-container { padding: 1rem .8rem 2rem; }
  h1 { font-size: 1.8rem !important; }
}
</style>
"""


def style_background_home():
    st.markdown(SMARTROLL_CSS, unsafe_allow_html=True)


def style_background_dashboard():
    st.markdown(SMARTROLL_CSS, unsafe_allow_html=True)


def style_base_layout():
    # Kept as a separate function so existing screens/imports remain unchanged.
    st.markdown(SMARTROLL_CSS, unsafe_allow_html=True)
