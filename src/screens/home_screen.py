from pathlib import Path
import streamlit as st
from src.components.header import header_home
from src.ui.base_layouts import style_base_layout, style_background_home

ASSETS_DIR = Path("assets")


def _apply_home_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');
        html, body, [class*="st-"], button { font-family: 'Plus Jakarta Sans', sans-serif !important; }

        .sr-hero { text-align:center; padding:.5rem 0 1.5rem; max-width:900px; margin:0 auto; }
        .sr-hero-eyebrow { color:#22D3EE; font-size:.72rem; font-weight:800; letter-spacing:.18em; text-transform:uppercase; margin-bottom:.65rem; }
        .sr-hero-title { font-family:'Space Grotesk',sans-serif !important; font-size:clamp(2rem,4.5vw,3.25rem); line-height:1.12; letter-spacing:-.045em; font-weight:700; color:#F8FAFC; margin:0; text-align:center; }
        .sr-hero-title span { background:linear-gradient(90deg,#60A5FA,#22D3EE); -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; }
        .sr-hero-copy { color:#94A3B8; font-size:.96rem; line-height:1.65; margin:.75rem auto 0; max-width:640px; text-align:center; }

        /* Portal cards */
        div[data-testid="stVerticalBlockBorderWrapper"] { border:1px solid rgba(96,165,250,.20) !important; border-radius:24px !important; background:linear-gradient(145deg,rgba(19,34,57,.96),rgba(11,17,32,.90)) !important; box-shadow:0 12px 32px rgba(0,0,0,.20); transition:transform .22s ease,border-color .22s ease,box-shadow .22s ease; }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover { border-color:rgba(34,211,238,.45) !important; box-shadow:0 16px 38px rgba(34,211,238,.07); transform:translateY(-2px); }
        .sr-role-tag { font-family:'Space Grotesk',sans-serif !important; text-align:center; color:#22D3EE; font-size:1.82rem; font-weight:700; letter-spacing:.13em; text-transform:uppercase; margin:.3rem 0 .55rem; }
        .sr-role-title { text-align:center !important; color:#F1F5F9 !important; font-family:'Space Grotesk',sans-serif !important; font-size:1.30rem; font-weight:700; letter-spacing:-.025em; line-height:1.3; margin:.15rem 0 .45rem; }
        .sr-role-desc { text-align:center !important; color:#94A3B8 !important; font-size:.86rem; line-height:1.55; min-height:2.8rem; margin:0 auto .45rem; max-width:94%; }
        div[data-testid="stImage"] { display:flex; justify-content:center; align-items:center; margin:.2rem auto .45rem; }
        div[data-testid="stImage"] img { object-fit:contain; padding:0; background:transparent !important; border-radius:0; }
        div[data-testid="stButton"] button[kind="primary"] { border-radius:13px !important; min-height:2.9rem !important; font-family:'Plus Jakarta Sans',sans-serif !important; font-size:.92rem !important; font-weight:700 !important; letter-spacing:.01em; transition:transform .16s ease,box-shadow .16s ease; }
        div[data-testid="stButton"] button[kind="primary"]:hover { transform:translateY(-1px); box-shadow:0 7px 20px rgba(34,211,238,.20); }

        .sr-feature-card { border:1px solid rgba(148,163,184,.13); border-radius:16px; background:linear-gradient(145deg,rgba(17,28,48,.72),rgba(11,17,32,.55)); padding:1rem 1.05rem; min-height:108px; }
        .sr-feature-title { color:#E2E8F0; font-size:.9rem; font-weight:700; margin-bottom:.3rem; }
        .sr-feature-copy { color:#94A3B8; font-size:.78rem; line-height:1.5; margin:0; }
        .sr-bottom-summary { text-align:center; max-width:680px; margin:1.4rem auto .6rem; }
        .sr-bottom-summary p { color:#94A3B8 !important; font-size:.94rem; margin:0 !important; }
        .sr-tagline-below { display:inline-block; color:#22D3EE; font-size:.76rem; font-weight:700; letter-spacing:.16em; text-transform:uppercase; margin-top:.45rem; }
        @media(max-width:700px) { .sr-hero{padding-bottom:1rem;} .sr-hero-copy{font-size:.86rem;} .sr-role-title{font-size:1.12rem;} .sr-role-desc{font-size:.82rem;min-height:0;} }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_portal_card(*, role_key: str, tag: str, title: str, description: str, image_path: Path, button_label: str) -> None:
    with st.container(border=True):
        st.markdown(f'<div class="sr-role-tag">{tag}</div>', unsafe_allow_html=True)

        # A dedicated center column keeps the illustration centered.
        image_left, image_center, image_right = st.columns([1, 2, 1])
        with image_center:
            if image_path.exists():
                st.image(str(image_path), width=210)
            else:
                st.caption(f"Image not found: {image_path}")

        st.markdown(f'<div class="sr-role-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sr-role-desc">{description}</div>', unsafe_allow_html=True)

    # Buttons are outside the card, so they line up across both columns.
    if st.button(button_label, type="primary", width="stretch", key=f"portal_btn_{role_key}"):
        st.session_state["login_type"] = role_key
        st.rerun()


def _render_highlights() -> None:
    st.markdown("<div style='height: 1.1rem;'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="medium")
    highlights = [
        (c1, "Instant Roll Calls", "Mark and review attendance in seconds without manual spreadsheets."),
        (c2, "Live Eligibility View", "Students can check subject-wise attendance and session updates anytime."),
        (c3, "Organized Subjects", "Keep courses, rosters, and session logs cleanly separated by class."),
    ]
    for col, heading, body in highlights:
        with col:
            st.markdown(f"""
                <div class="sr-feature-card">
                    <div class="sr-feature-title">{heading}</div>
                    <p class="sr-feature-copy">{body}</p>
                </div>
            """, unsafe_allow_html=True)


def _render_bottom_summary() -> None:
    st.markdown("""
        <div style="text-align:center;color:#64748B;font-size:.75rem;margin-top:1.5rem;">
            Powered by AI · Designed for smarter classrooms
        </div>
        <section class="sr-bottom-summary">
            <p>Fast attendance tracking, clear records, and simpler class management. Select your workspace to continue.</p>
            <div class="sr-tagline-below">AI Attendance System</div>
        </section>
    """, unsafe_allow_html=True)


def home_screen() -> None:
    header_home()
    style_background_home()
    style_base_layout()
    _apply_home_styles()

    
    student_col, teacher_col = st.columns([1, 1], gap="large")
    with student_col:
        _render_portal_card(
            role_key="student", tag="Student Portal", title="Your learning, your record",
            description="Check attendance percentages, join active classes, and track sessions.",
            image_path=ASSETS_DIR / "student1.png", button_label="Continue as Student",
        )
    with teacher_col:
        _render_portal_card(
            role_key="teacher", tag="Teacher Portal", title="Manage your classroom",
            description="Take attendance, manage subjects, and monitor class participation.",
            image_path=ASSETS_DIR / "teacher.png", button_label="Continue as Teacher",
        )

    _render_highlights()
    _render_bottom_summary()