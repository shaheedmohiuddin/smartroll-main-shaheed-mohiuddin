
import streamlit as st
from src.database.config import supabase
from src.database.db import enroll_student_to_subject
import time


@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):

    student_id = st.session_state.student_data.get('student_id')

    res = (
        supabase.table('subjects')
        .select('subject_id, name')
        .eq('subject_code', subject_code)
        .execute()
    )

    if not res.data:
        st.error('Subject Code not found!')

        if st.button('Close'):
            st.query_params.clear()
            st.rerun()

        return

    subject = res.data[0]

    # Check existing enrollment
    check = (
        supabase.table('subject_students')
        .select('*')
        .eq('subject_id', subject['subject_id'])
        .eq('student_id', student_id)
        .execute()
    )

    # Already enrolled
    if check.data:

        st.markdown(
            """
            <div style="margin-bottom:12px;">
                <div style="color:#7866D8;font-size:1.2rem;font-weight:800;letter-spacing:.12em;">
                    ENROLLMENT STATUS
                </div>
                <div style="color:#25243A;font-size:1.1rem;font-weight:700;margin-top:4px;">
                    Already enrolled
                </div>
                <div style="color:#4B5563;font-size:.88rem;margin-top:4px;">
                    You are already enrolled in this subject.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button('Got it!', type='primary', width='stretch'):
            st.query_params.clear()
            st.rerun()

        return

    # Enrollment invitation
    st.markdown(
        f"""
        <div style="margin-bottom:12px;">
            <div style="color:#7866D8;font-size:.72rem;font-weight:800;letter-spacing:.12em;">
                STUDENT ENROLLMENT
            </div>

            <div style="color:#25243A;font-size:1.1rem;font-weight:700;margin-top:4px;">
                Join a class
            </div>

            <div style="color:#4B5563;font-size:.88rem;margin-top:4px;">
                Would you like to enroll in
                <strong style="color:#25243A;">{subject['name']}</strong>?
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            'No thanks!',
            width='stretch',
            type='secondary'
        ):
            st.query_params.clear()
            st.rerun()

    with col2:
        if st.button(
            'Yes, enroll now',
            type='primary',
            width='stretch'
        ):
            try:
                enroll_student_to_subject(
                    student_id,
                    subject['subject_id']
                )

                st.success('Joined successfully!')
                st.query_params.clear()

                time.sleep(2)
                st.rerun()

            except Exception as e:
                st.error(f"Enrollment failed: {e}")
