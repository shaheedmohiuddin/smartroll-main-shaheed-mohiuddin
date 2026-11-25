import streamlit as st

from src.ui.base_layouts import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance,train_classifier,get_face_embeddings
from src.pipelines.voice_pipeline import get_voice_embedding

from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance,unenroll_student_to_subject
import time
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card

def student_dashboard():

    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    header_dashboard()

    st.markdown(
        f"""
        <div class="smartroll-welcome">
            <div class="smartroll-welcome-label">STUDENT WORKSPACE</div>
            <h2>Welcome back, {student_data['name']} 👋</h2>
            <p>Keep track of your classes and attendance in one place.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Logout",
        type="secondary",
        key="loginbackbtn",
        shortcut="control+backspace"
    ):
        st.session_state["is_logged_in"] = False
        del st.session_state.student_data
        st.rerun()

    st.markdown(
        '<div class="sr-section-heading">'
        '<span class="sr-section-dot"></span>'
        '<span>Your Learning Overview</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    with st.spinner("Loading your enrolled subjects..."):

        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    # Ensure logs is a list
    logs = logs or []

    # =========================
    # ATTENDANCE STATISTICS
    # =========================

    stats_map = {}

    for log in logs:

        sid = log['subject_id']

        if sid not in stats_map:
            stats_map[sid] = {
                "total": 0,
                "attended": 0
            }

        stats_map[sid]["total"] += 1

        # FIX: Check the individual log, not the entire logs list
        if log.get('is_present'):
            stats_map[sid]["attended"] += 1

    total_classes = sum(item["total"] for item in stats_map.values())
    total_attended = sum(item["attended"] for item in stats_map.values())
    overall_pct = round((total_attended / total_classes) * 100) if total_classes else 0

    metric_cols = st.columns(3)
    with metric_cols[0]:
        st.metric("Enrolled Subjects", len(subjects))
    with metric_cols[1]:
        st.metric("Classes Attended", total_attended)
    with metric_cols[2]:
        st.metric("Overall Attendance", f"{overall_pct}%")

    title_cols = st.columns([3, 1], vertical_alignment="center")

    with title_cols[0]:
        st.markdown(
            '<div class="sr-section-heading sr-enrolled-heading">'
            '<span class="sr-section-dot"></span>'
            '<span>Your Enrolled Subjects</span>'
            '</div>',
            unsafe_allow_html=True,
        )

    with title_cols[1]:
        if st.button(
            "＋ Enroll in Subject",
            type="primary",
            width="content",
        ):
            enroll_dialog()

    st.divider()

    # =========================
    # SUBJECT CARDS
    # =========================

    cols = st.columns(2)

    for i, sub_nod in enumerate(subjects):

        sub = sub_nod['subjects']
        sid = sub['subject_id']

        stats = stats_map.get(
            sid,
            {
                "total": 0,
                "attended": 0
            }
        )

        def unenroll_button():

            if st.button(
                "Unenroll from this course",
                type="tertiary",
                width="stretch",
                icon=":material/delete_forever:",
                key=f"unenroll_{sid}"
            ):

                unenroll_student_to_subject(student_id, sid)

                st.toast(
                    f"Unenrolled from {sub['name']} successfully"
                )

                st.rerun()

        with cols[i % 2]:

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=(
                    (" ", "Total Classes", stats['total']),
                    (" ", "Attended", stats['attended'])
                ),
                footer_callback=unenroll_button
            )

def student_screen():

    style_background_dashboard()
    style_base_layout()

    st.markdown("""
        <style>

        /* Compact, centered FaceID camera */
        div[data-testid="stCameraInput"] {
            width: 100% !important;
            max-width: 520px !important;
            margin: 0 auto !important;
        }
        div[data-testid="stCameraInput"] video,
        div[data-testid="stCameraInput"] img {
            width: 100% !important;
            max-width: 520px !important;
            height: auto !important;
            border-radius: 16px !important;
        }
        /* Camera controls: SmartRoll blue/cyan */
        div[data-testid="stCameraInput"] button {
            width: 100% !important;
            max-width: 520px !important;
            background: linear-gradient(135deg, #2563EB, #0891B2) !important;
            color: #FFFFFF !important;
            border: 1px solid rgba(34, 211, 238, 0.45) !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            letter-spacing: 0.2px !important;
            box-shadow: 0 6px 18px rgba(37, 99, 235, 0.22) !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stCameraInput"] button:hover {
            background: linear-gradient(135deg, #1D4ED8, #0E7490) !important;
            border-color: #22D3EE !important;
            box-shadow: 0 8px 22px rgba(34, 211, 238, 0.25) !important;
            transform: translateY(-1px) !important;
        }
        div[data-testid="stCameraInput"] button:active {
            transform: translateY(0) !important;
        }
        div[data-testid="stCameraInput"] button p {
            color: #FFFFFF !important;
            font-weight: 700 !important;
            margin: 0 !important;
        }
        /* SmartRoll welcome toast */
        div[data-testid="stToast"] {
            background: linear-gradient(135deg, #1D4ED8, #0891B2) !important;
            color: #FFFFFF !important;
            border: 1px solid rgba(34, 211, 238, 0.55) !important;
            border-radius: 14px !important;
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.30) !important;
        }
        div[data-testid="stToast"] p,
        div[data-testid="stToast"] span {
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }
        .smartroll-welcome {
            background: linear-gradient(120deg, rgba(59,130,246,.18), rgba(34,211,238,.08));
            border: 1px solid rgba(59,130,246,.28);
            border-radius: 20px;
            padding: 1.35rem 1.6rem;
            margin: 1rem 0 1.2rem 0;
        }
        .smartroll-welcome-label {
            color: #6D5BD0 !important;
            font-size: .72rem;
            font-weight: 800;
            letter-spacing: .13em;
            margin-bottom: .4rem;
        }
        .smartroll-welcome h2 {
            color: #25243A !important;
            margin: 0 !important;
            font-size: 1.65rem !important;
            text-align: left !important;
        }
        .smartroll-welcome p {
            color: #5F6078 !important;
            margin: .35rem 0 0 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize registration state
    if "show_registration" not in st.session_state:
        st.session_state.show_registration = False

    if "student_data" in st.session_state:
        student_dashboard()
        return

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go back to home",
            type="secondary",
            key="loginbackbtn",
            shortcut="control+backspace"
        ):
            st.session_state["login_type"] = None
            st.rerun()

    st.markdown("""
        <style>
        .register-title {
            color: #25243A !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 3rem !important;
            font-weight: 700 !important;
            margin-top: 30px !important;
            text-align: center !important;
        }
        </style>

        <p class="register-title">
            Login using FaceID
        </p>
    """, unsafe_allow_html=True)

    photo_source = st.camera_input(
        "Position your face in the center"
    )

    if photo_source:

        img = np.array(Image.open(photo_source))

        with st.spinner("AI is scanning..."):

            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:

                st.warning("Face not found")

            elif num_faces > 1:

                st.warning("Multiple faces found")

            else:

                if detected:

                    student_id = list(detected.keys())[0]

                    all_students = get_all_students()

                    student = next(
                        (
                            s for s in all_students
                            if s["student_id"] == student_id
                        ),
                        None
                    )

                    if student:

                        st.session_state.is_logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state.student_data = student

                        st.toast(
                            f'👋 Welcome Back {student["name"]}'
                        )

                        time.sleep(1)
                        st.rerun()

                else:

                    st.info(
                        "Face not recognized! "
                        "You might be a new student!"
                    )

                    st.session_state.show_registration = True


    # ==============================
    # REGISTRATION
    # ==============================

    if st.session_state.show_registration:

        with st.container(border=True):

            st.header("Register new profile")

            new_name = st.text_input(
                "Enter your name",
                placeholder="E.g. Shaheed Mohiuddin"
            )

            st.subheader("Optional: Voice Enrollment")

            st.info(
                "Enroll your voice only for attendance"
            )

            audio_data = None

            try:

                audio_data = st.audio_input(
                    "Record a short phrase like: "
                    "I am present, My name is Mohammed bin Wahlan."
                )

            except Exception:

                st.warning(
                    "Voice enrollment is unavailable."
                )

            if st.button(
                "Create Account",
                type="primary"
            ):

                if not new_name:

                    st.warning(
                        "Please enter your name!"
                    )

                elif photo_source is None:

                    st.warning(
                        "Please capture your face first."
                    )

                else:

                    with st.spinner(
                        "Creating profile..."
                    ):

                        img = np.array(
                            Image.open(photo_source)
                        )

                        encodings = get_face_embeddings(img)

                        if len(encodings) > 0:

                            face_emb = encodings[0].tolist()

                            voice_emb = None

                            if audio_data:

                                voice_emb = get_voice_embedding(
                                    audio_data.read()
                                )

                            response_data = create_student(
                                new_name,
                                face_embedding=face_emb,
                                voice_embedding=voice_emb
                            )

                            if response_data:

                                train_classifier()

                                st.session_state.is_logged_in = True
                                st.session_state.user_role = "student"
                                st.session_state.student_data = response_data[0]

                                st.toast(
                                    f"Profile Created! Hi {new_name}!"
                                )

                                time.sleep(1)

                                st.rerun()

                            else:

                                st.error(
                                    "Failed to create student profile."
                                )

                        else:

                            st.error(
                                "Couldn't capture your facial "
                                "features for registration."
                            )