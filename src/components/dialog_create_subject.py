
import streamlit as st
from src.database.db import create_subject


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):

    st.html("""
        <div style="margin-bottom:12px;">
            <div style="
                color:#7866D8;
                font-size:1.2rem;
                font-weight:800;
                letter-spacing:.12em;">
                TEACHER WORKSPACE
            </div>

            <div style="
                color:#25243A;
                font-size:1.1rem;
                font-weight:700;
                margin-top:4px;">
                Create a class
            </div>

            <div style="
                color:#4B5563;
                font-size:.88rem;
                margin-top:4px;
                line-height:1.5;">
                Add subject details to create a class for your students.
            </div>
        </div>
    """)

    sub_id = st.text_input(
        "Subject code",
        placeholder="CS101"
    )

    sub_name = st.text_input(
        "Subject name",
        placeholder="Introduction to Computer Science"
    )

    sub_section = st.text_input(
        "Section",
        placeholder="A"
    )

    if st.button("Create subject", type="primary", width="stretch"):
        if not all([sub_id.strip(), sub_name.strip(), sub_section.strip()]):
            st.warning("Please fill in all fields.")
            return

        try:
            create_subject(
                sub_id.strip(),
                sub_name.strip(),
                sub_section.strip(),
                teacher_id
            )
            st.toast("Subject created successfully!")
            st.rerun()

        except Exception as e:
            st.error(f"Error creating subject: {e}")
