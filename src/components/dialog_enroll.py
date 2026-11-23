import streamlit as st
from src.database.config import supabase
from src.database.db import enroll_student_to_subject


@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.markdown(
        """
        <div style="margin-bottom:12px;">
          <div style="color:#22D3EE;font-size:.72rem;font-weight:800;letter-spacing:.12em;">STUDENT ENROLLMENT</div>
          <div style="color:#F1F5F9;font-size:1.1rem;font-weight:700;margin-top:4px;">Join a class</div>
          <div style="color:#94A3B8;font-size:.88rem;margin-top:4px;">Enter the subject code shared by your teacher.</div>
        </div>
        """, unsafe_allow_html=True
    )
    join_code = st.text_input("Subject code", placeholder="e.g. CS101").strip()

    if st.button("Enroll now", type="primary", width="stretch"):
        if not join_code:
            st.warning("Please enter a subject code.")
            return
        try:
            res = supabase.table("subjects").select("subject_id, name, subject_code").eq("subject_code", join_code).execute()
            if not res.data:
                st.error("Subject code not found. Check the code and try again.")
                return
            subject = res.data[0]
            student_id = st.session_state.student_data["student_id"]

            check = supabase.table("subject_students").select("*").eq("subject_id", subject["subject_id"]).eq("student_id", student_id).execute()
            if check.data:
                st.info("You are already enrolled in this subject.")
                return

            enroll_student_to_subject(student_id, subject["subject_id"])
            st.success(f"Successfully enrolled in {subject['name']}!")
            st.rerun()
        except Exception as e:
            st.error(f"Enrollment failed: {e}")
