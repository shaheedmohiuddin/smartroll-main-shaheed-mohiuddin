
import streamlit as st

SMARTROLL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
:root {
 --sr-bg:#F7F7FB; --sr-surface:#FFFFFF; --sr-surface-2:#F4F1FF;
 --sr-border:#E8E5F2; --sr-text:#25243A; --sr-muted:#77758D;
 --sr-purple:#7866D8; --sr-purple-dark:#6654C7; --sr-lilac:#EDE9FF; --sr-blue:#7B8CF5;
}
html,body,[class*="css"],button {font-family:'Plus Jakarta Sans',Inter,sans-serif !important;}
.stApp {background:var(--sr-bg) !important;color:var(--sr-text) !important;}
header[data-testid="stHeader"]{display:flex!important;visibility:visible!important;background:transparent!important;}

/* Keep Streamlit controls visible while developing and testing UI changes. */
[data-testid="stToolbar"],
[data-testid="stMainMenu"],
.stDeployButton,
[data-testid="stDecoration"],
#MainMenu,
footer {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    height: auto !important;
}

/* Horizontal padding reduced; vertical padding unchanged */
.block-container{
    padding-top:1.25rem!important;
    padding-bottom:2.5rem!important;
    padding-left:1.5rem!important;
    padding-right:1.5rem!important;
    max-width:1280px!important;
}

section[data-testid="stSidebar"]{background:#FFFFFF!important;border-right:1px solid var(--sr-border)!important;}
section[data-testid="stSidebar"] *{color:var(--sr-text)!important;}
h1,h2,h3,h4{font-family:'Plus Jakarta Sans',sans-serif!important;letter-spacing:-.035em;color:var(--sr-text)!important;}
h1{font-size:2.15rem!important;font-weight:800!important;} h2{font-size:1.65rem!important;font-weight:750!important;}
h3{font-size:1.28rem!important;font-weight:700!important;} h4{font-size:1.05rem!important;font-weight:650!important;}
p,label,.stMarkdown{color:var(--sr-text)!important;} small,[data-testid="stCaptionContainer"]{color:var(--sr-muted)!important;}
[data-testid="stMarkdownContainer"] p{color:var(--sr-text)!important;}
[data-testid="stMarkdownContainer"] h1,[data-testid="stMarkdownContainer"] h2,[data-testid="stMarkdownContainer"] h3{color:var(--sr-text)!important;}
[data-testid="stTextInput"] label,[data-testid="stSelectbox"] label,[data-testid="stCameraInput"] label{color:#45445D!important;}
hr{border-color:var(--sr-border)!important;}
[data-testid="stVerticalBlockBorderWrapper"]{background:#FFFFFF!important;border:1px solid var(--sr-border)!important;border-radius:20px!important;box-shadow:0 5px 20px rgba(54,45,100,.045)!important;}
[data-testid="stMetric"]{background:linear-gradient(145deg,#FFFFFF,#F8F6FF)!important;border:1px solid var(--sr-border)!important;padding:1rem 1.1rem!important;border-radius:16px!important;}
[data-testid="stMetricLabel"]{color:var(--sr-muted)!important;} [data-testid="stMetricValue"]{color:var(--sr-text)!important;}
[data-testid="stDataFrame"]{border:1px solid var(--sr-border)!important;border-radius:12px!important;overflow:hidden;}
input,textarea{background:#FFFFFF!important;color:var(--sr-text)!important;border-color:var(--sr-border)!important;}
[data-baseweb="select"]>div,[data-baseweb="input"]>div{background:#FFFFFF!important;border-color:var(--sr-border)!important;border-radius:11px!important;}
.stButton>button,[data-testid="stFormSubmitButton"] button{border-radius:11px!important;border:1px solid transparent!important;font-weight:650!important;transition:all .18s ease!important;min-height:2.55rem!important;}
.stButton>button[kind="primary"],[data-testid="stFormSubmitButton"] button{background:var(--sr-purple)!important;color:#FFFFFF!important;}
.stButton>button[kind="secondary"]{background:#FFFFFF!important;border-color:var(--sr-border)!important;color:var(--sr-text)!important;}
.stButton>button[kind="tertiary"]{background:transparent!important;color:var(--sr-muted)!important;}
.stButton>button:hover{border-color:#B9AEF2!important;transform:translateY(-1px);box-shadow:0 5px 16px rgba(120,102,216,.12)!important;}
.stButton>button:disabled{opacity:.45;}
[data-testid="stAlert"]{border-radius:12px!important;}
[data-testid="stTabs"] button{color:var(--sr-muted)!important;} [data-testid="stTabs"] button[aria-selected="true"]{color:var(--sr-purple)!important;}
[data-testid="stDialog"]>div{background:#FFFFFF!important;border:1px solid var(--sr-border)!important;border-radius:18px!important;}
[data-testid="stImage"] img{border-radius:14px!important;}

/* Convert legacy inline dark colors to the selected light theme */
[style*="color:#F1F5F9"],[style*="color: #F1F5F9"],[style*="color:#E2E8F0"],[style*="color: #E2E8F0"],[style*="color:#CBD5E1"],[style*="color: #CBD5E1"]{color:var(--sr-text)!important;}
[style*="color:#94A3B8"],[style*="color: #94A3B8"],[style*="color:#64748B"],[style*="color: #64748B"]{color:var(--sr-muted)!important;}
[style*="color:#22D3EE"],[style*="color: #22D3EE"],[style*="color:#60A5FA"],[style*="color: #60A5FA"],[style*="color:#93C5FD"],[style*="color: #93C5FD"]{color:var(--sr-purple)!important;}
[style*="background:#0B1120"],[style*="background: #0B1120"],[style*="background:#111C30"],[style*="background: #111C30"],[style*="background:#14213A"],[style*="background: #14213A"],[style*="background:#1D3557"],[style*="background: #1D3557"],[style*="background:#172338"],[style*="background: #172338"]{background:#F4F1FF!important;}

/* Mobile: horizontal padding reduced; vertical padding unchanged */
@media(max-width:768px){
    .block-container{
        padding-top:1rem!important;
        padding-bottom:2rem!important;
        padding-left:.55rem!important;
        padding-right:.55rem!important;
    }
    h1{font-size:1.8rem!important;}
}

/* Student dashboard section headings with purple accent dots */
.sr-section-heading {
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    font-size: 2.8rem !important;
    line-height: 1.2 !important;
    font-weight: 800 !important;
    letter-spacing: -0.035em !important;
    color: var(--sr-text) !important;
    margin: 0.45rem 0 0.9rem 0 !important;
    padding: 0 !important;
}
.sr-section-dot {
    display: inline-block !important;
    width: 9px !important;
    height: 88px !important;
    min-width: 9px !important;
    border-radius: 50% !important;
    background: var(--sr-purple) !important;
    box-shadow: 0 0 0 4px var(--sr-lilac) !important;
}
.sr-enrolled-heading {
    margin-top: 1.15rem !important;
    margin-bottom: 0.05rem !important;
}
@media (max-width: 768px) {
    .sr-section-heading {
        font-size: 2.5rem !important;
        gap: 10px !important;
    }
}
</style>
"""

def style_background_home():
 st.markdown(SMARTROLL_CSS,unsafe_allow_html=True)

def style_background_dashboard():
 st.markdown(SMARTROLL_CSS,unsafe_allow_html=True)

def style_base_layout():
 st.markdown(SMARTROLL_CSS,unsafe_allow_html=True)


def set_toolbar_visibility(visible: bool = True) -> None:
    """
    Show or hide Streamlit's toolbar and related controls.

    Keep visible=True during development so you can access the Streamlit
    menu and inspect/reload the app while making UI changes.
    """
    toolbar_display = "flex" if visible else "none"
    toolbar_visibility = "visible" if visible else "hidden"

    st.markdown(
        f"""
        <style>
        header[data-testid="stHeader"] {{
            display: flex !important;
            visibility: visible !important;
        }}
        [data-testid="stToolbar"],
        [data-testid="stMainMenu"],
        .stDeployButton,
        [data-testid="stDecoration"],
        #MainMenu {{
            display: {toolbar_display} !important;
            visibility: {toolbar_visibility} !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
