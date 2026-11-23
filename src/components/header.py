import streamlit as st

LOGO_URL = (
    "https://play-lh.googleusercontent.com/"
    "PdnHPKi-hAWxZGE6D8HYQE-JRFOgFrFMiCz6n247vBkF1FuXW9UO2TqFktP4PTdFYIgNxieSaQgv4M_UbITsq34"
)


def _apply_header_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@700;800&display=swap');

        .sr-header-logo {
            object-fit: cover;
            border-radius: 22px;
            box-shadow: 0 10px 28px rgba(0, 0, 0, 0.34);
        }

        /* Home header */
        .sr-header-home {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 1.5rem 0 0.35rem 0;
        }
        .sr-header-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(2.8rem, 6vw, 4rem);
            font-weight: 800;
            letter-spacing: 0.05em;
            line-height: 1.05;
            margin: 0.7rem 0 0 0;
            text-align: center;
        }
        .sr-header-title span {
            background: linear-gradient(95deg, #F8FAFC 10%, #60A5FA 52%, #22D3EE 95%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Dashboard header */
        .sr-header-dash {
            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 16px;
            padding: 0.65rem 0 1rem 0;
        }
        .sr-header-dash-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 2.15rem;
            font-weight: 800;
            letter-spacing: 0.04em;
            line-height: 1.1;
            margin: 0;
        }
        .sr-header-dash-title span {
            background: linear-gradient(95deg, #F8FAFC 10%, #60A5FA 52%, #22D3EE 95%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .sr-header-role-badge {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: #22D3EE;
            margin-left: 0.65rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def header_home() -> None:
    _apply_header_styles()
    st.markdown(
        f"""
        <div class="sr-header-home">
            <img src="{LOGO_URL}" alt="SmartRoll Logo" class="sr-header-logo" style="height:132px; width:132px;" />
            <div class="sr-header-title"><span>SMARTROLL</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def header_dashboard(role_label: str | None = None) -> None:
    _apply_header_styles()
    badge_html = (
        f'<span class="sr-header-role-badge">· {role_label}</span>'
        if role_label
        else ""
    )
    st.markdown(
        f"""
        <div class="sr-header-dash">
            <img src="{LOGO_URL}" alt="SmartRoll Logo" class="sr-header-logo" style="height:72px; width:72px;" />
            <h2 class="sr-header-dash-title"><span>SMARTROLL</span>{badge_html}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )