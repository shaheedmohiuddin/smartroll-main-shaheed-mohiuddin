import streamlit as st
from html import escape


def subject_card(name, code, section, stats=None, footer_callback=None):
    """Render a SmartRoll themed subject card. Existing API is preserved."""
    safe_name = escape(str(name))
    safe_code = escape(str(code))
    safe_section = escape(str(section))

    html = f"""
    <div style="
        background: linear-gradient(145deg, #14213A, #101A2D);
        border: 1px solid #26364E;
        border-radius: 18px;
        padding: 20px 22px;
        margin: 0 0 16px 0;
        box-shadow: 0 8px 24px rgba(0,0,0,.16);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            width: 4px; height: 100%; position: absolute;
            left: 0; top: 0;
            background: linear-gradient(180deg, #3B82F6, #22D3EE);
        "></div>
        <div style="color:#F1F5F9;font-size:1.12rem;font-weight:700;margin-bottom:10px;">
            📚 {safe_name}
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;">
            <span style="background:#1D3557;color:#93C5FD;padding:5px 10px;border-radius:8px;font-size:.78rem;">
                {safe_code}
            </span>
            <span style="background:#1B2B40;color:#CBD5E1;padding:5px 10px;border-radius:8px;font-size:.78rem;">
                Section {safe_section}
            </span>
        </div>
    """

    if stats:
        html += '<div style="display:flex;gap:8px;flex-wrap:wrap;">'
        for icon, label, value in stats:
            safe_label = escape(str(label))
            safe_value = escape(str(value))
            html += f"""
            <div style="
                background:#0B1120;border:1px solid #26364E;
                padding:8px 11px;border-radius:10px;
                color:#94A3B8;font-size:.82rem;
            ">
                {icon} <span style="color:#F1F5F9;font-weight:700;">{safe_value}</span>
                <span>{safe_label}</span>
            </div>
            """
        html += "</div>"

    html += "</div>"
    st.html(html)

    if footer_callback:
        footer_callback()
