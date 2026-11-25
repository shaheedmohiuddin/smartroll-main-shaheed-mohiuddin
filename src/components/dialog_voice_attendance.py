
import streamlit as st
import pandas as pd

from src.database.config import supabase
from datetime import datetime

from src.pipelines.voice_pipeline import process_bulk_audio
from src.components.dialog_attendance_result import show_attendance_result


@st.dialog("Voice Attendance")
def voice_attendance_dialog(selected_subject_id):

    st.html("""
        <div style="padding:4px 0 12px 0;">
            <div style="
                color:#7866D8;
                font-size:1.2rem;
                font-weight:800;
                letter-spacing:.12em;">
                VOICE-BASED ATTENDANCE
            </div>

            <div style="
                color:#25243A;
                font-size:1.15rem;
                font-weight:700;
                margin-top:4px;">
                Record and identify students
            </div>

            <div style="
                color:#4B5563;
                font-size:.88rem;
                margin-top:5px;
                line-height:1.5;">
                Ask students to say
                <strong style="color:#7866D8;">“I am present”</strong>.
                SmartRoll will match the audio with enrolled voice profiles.
            </div>
        </div>
    """)

    st.html("""
        <div style="
            background:#F4F1FF;
            border:1px solid #E8E5F2;
            border-radius:14px;
            padding:13px 15px;
            margin:0 0 12px 0;
            color:#4B5563;
            font-size:.85rem;
            line-height:1.5;">

            <span style="
                color:#7866D8;
                font-weight:700;">
                Recording tips
            </span>

            <br>

            Record in a quiet room, speak clearly, and ensure students
            take turns if possible.
        </div>
    """)

    audio_data = st.audio_input("🎙️ Record classroom audio")

    if audio_data is not None:
        st.caption(
            "Audio captured. Listen to the recording before analyzing if needed."
        )

    # Analyze button
    if st.button(
        "Analyze voice & mark attendance",
        width="stretch",
        type="primary"
    ):

        # Check if audio was recorded
        if audio_data is None:
            st.warning("Please record audio before analyzing.")
            st.stop()

        with st.spinner("Listening for enrolled voice profiles…"):

            # Fetch enrolled students
            enrolled_res = (
                supabase.table("subject_students")
                .select("*, students(*)")
                .eq("subject_id", selected_subject_id)
                .execute()
            )

            enrolled_students = enrolled_res.data

            if not enrolled_students:
                st.warning("No students enrolled in this course.")
                st.stop()

            # Create voice candidate dictionary
            candidates_dict = {
                s["students"]["student_id"]:
                s["students"]["voice_embedding"]

                for s in enrolled_students
                if s["students"].get("voice_embedding") is not None
            }

            if not candidates_dict:
                st.error(
                    "No enrolled students have voice profiles registered."
                )
                st.stop()

            # Read audio
            audio_bytes = audio_data.read()

            # Process audio
            detected_scores = process_bulk_audio(
                audio_bytes,
                candidates_dict
            )

            results = []
            attendance_to_log = []

            current_timestamp = datetime.now().strftime(
                "%Y-%m-%dT%H:%M:%S"
            )

            # Generate attendance results
            for node in enrolled_students:

                student = node["students"]

                student_id = student["student_id"]

                score = detected_scores.get(
                    student_id,
                    detected_scores.get(str(student_id), 0.0)
                )

                is_present = score > 0

                results.append({
                    "Name": student["name"],
                    "ID": student_id,
                    "Source": score if is_present else "-",
                    "Status": "✅ Present" if is_present else "Absent"
                })

                attendance_to_log.append({
                    "student_id": student_id,
                    "subject_id": selected_subject_id,
                    "timestamp": current_timestamp,
                    "is_present": bool(is_present)
                })

            # Save results in session state
            st.session_state.voice_attendance_results = (
                pd.DataFrame(results),
                attendance_to_log
            )

    # Display results if available
    if st.session_state.get("voice_attendance_results"):

        st.divider()

        df_results, logs = st.session_state.voice_attendance_results

        show_attendance_result(df_results, logs)
