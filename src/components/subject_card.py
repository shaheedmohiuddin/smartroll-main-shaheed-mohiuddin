import streamlit as st
from html import escape


def subject_card(name, code, section, stats=None, footer_callback=None):
    """Render a clean SmartRoll subject card. API and behavior are preserved."""
    safe_name = escape(str(name))
    safe_code = escape(str(code))
    safe_section = escape(str(section))

    html = f'''<div style="background:#FFFFFF;border:1px solid #E8E5F2;border-radius:18px;padding:20px 22px;margin:0 0 16px 0;box-shadow:0 5px 18px rgba(54,45,100,.045);position:relative;overflow:hidden;">
      <div style="width:4px;height:100%;position:absolute;left:0;top:0;background:linear-gradient(180deg,#7866D8,#B5A8F6);"></div>
      <div style="color:#25243A;font-size:1.12rem;font-weight:700;margin-bottom:10px;">📚 {safe_name}</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;">
        <span style="background:#EDE9FF;color:#6654C7;padding:5px 10px;border-radius:8px;font-size:.78rem;">{safe_code}</span>
        <span style="background:#F4F1FF;color:#77758D;padding:5px 10px;border-radius:8px;font-size:.78rem;">Section {safe_section}</span>
      </div>'''

    if stats:
        html += '<div style="display:flex;gap:8px;flex-wrap:wrap;">'
        for icon, label, value in stats:
            html += f'''<div style="background:#F8F7FC;border:1px solid #E8E5F2;padding:8px 11px;border-radius:10px;color:#77758D;font-size:.82rem;">{icon} <span style="color:#25243A;font-weight:700;">{escape(str(value))}</span> <span>{escape(str(label))}</span></div>'''
        html += '</div>'

    html += '</div>'
    st.html(html)
    if footer_callback:
        footer_callback()
