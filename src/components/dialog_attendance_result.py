import streamlit as st
import pandas as pd
from src.database.db import create_attendance


def show_attendance_result(df, logs):
    """Review detected attendance before saving to Supabase."""
    st.markdown(
        """
        <div style="padding:12px 0 8px 0;">
          <div style="color:#22D3EE;font-size:.72rem;font-weight:800;letter-spacing:.12em;">
            ATTENDANCE REVIEW
          </div>
          <div style="color:#F1F5F9;font-size:1.2rem;font-weight:700;margin-top:4px;">
            Check the results before saving
          </div>
          <div style="color:#94A3B8;font-size:.88rem;margin-top:4px;">
            Review student names and attendance status. You can discard this session or confirm it.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    present_count = 0
    absent_count = 0
    if "Status" in df.columns:
        present_count = int(df["Status"].astype(str).str.contains("Present", case=False, na=False).sum())
        absent_count = int(df["Status"].astype(str).str.contains("Absent", case=False, na=False).sum())

    c1, c2, c3 = st.columns(3)
    c1.metric("Total students", len(df))
    c2.metric("Present", present_count)
    c3.metric("Absent", absent_count)

    st.dataframe(df, hide_index=True, width="stretch")

    st.caption("Attendance is saved only after you confirm.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Discard results", width="stretch", type="secondary"):
            st.session_state.attendance_images = []
            st.session_state.voice_attendance_results = None
            st.rerun()

    with col2:
        if st.button("Confirm & save attendance", width="stretch", type="primary"):
            try:
                create_attendance(logs)
                st.toast("Attendance saved successfully!")
                st.session_state.attendance_images = []
                st.session_state.voice_attendance_results = None
                st.rerun()
            except Exception as e:
                st.error(f"Sync failed: {e}")


@st.dialog("Attendance Review")
def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs)
