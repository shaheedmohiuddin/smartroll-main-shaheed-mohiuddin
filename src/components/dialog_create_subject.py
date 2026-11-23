import streamlit as st
from src.database.db import create_subject


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.markdown(
        """
        <div style="margin-bottom:12px;">
          <div style="color:#22D3EE;font-size:.72rem;font-weight:800;letter-spacing:.12em;">TEACHER WORKSPACE</div>
          <div style="color:#F1F5F9;font-size:1.1rem;font-weight:700;margin-top:4px;">Create a class</div>
          <div style="color:#94A3B8;font-size:.88rem;margin-top:4px;">Add subject details to create a class for your students.</div>
        </div>
        """, unsafe_allow_html=True
    )
    sub_id = st.text_input("Subject code", placeholder="CS101")
    sub_name = st.text_input("Subject name", placeholder="Introduction to Computer Science")
    sub_section = st.text_input("Section", placeholder="A")

    if st.button("Create subject", type="primary", width="stretch"):
        if not all([sub_id.strip(), sub_name.strip(), sub_section.strip()]):
            st.warning("Please fill in all fields.")
            return
        try:
            create_subject(sub_id.strip(), sub_name.strip(), sub_section.strip(), teacher_id)
            st.toast("Subject created successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error creating subject: {e}")
