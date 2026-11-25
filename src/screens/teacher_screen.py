import streamlit as st

from src.ui.base_layouts import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard

from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects, get_attendance_for_teacher
from src.components.subject_card import subject_card
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_add_photos import add_photos_dialog
from src.pipelines.face_pipeline import predict_attendance
import numpy as np
from src.database.config import supabase
from datetime import datetime
import pandas as pd
from src.components.dialog_attendance_result import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog

def teacher_screen():

    style_background_dashboard()
    style_base_layout()


    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=='login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type=='register':
        teacher_screen_register()

 
def teacher_dashboard():
    teacher_data = st.session_state.teacher_data

    # SmartRoll Teacher Dashboard Header
    st.html("""
        <div style="padding:8px 0 20px 0;">
            <div style="
                font-size:13px;
                letter-spacing:2px;
                text-transform:uppercase;
                color:#7866D8;
                font-weight:700;
                margin-bottom:8px;">
                SMARTROLL • TEACHER WORKSPACE
            </div>

            <div style="
                font-size:30px;
                font-weight:750;
                color:#25243A;
                line-height:1.2;">
                Your classroom,
                <span style="color:#7866D8;">In control.</span>
            </div>

            <div style="
                color:#4B5563;
                font-size:15px;
                margin-top:8px;">
                Manage classes and take AI-powered attendance in one place.
            </div>
        </div>
    """)

    # Welcome message and logout
    c1, c2 = st.columns([3, 1], vertical_alignment="center")

    with c1:
        st.markdown(
            f"""
            <div style="
                color:#25243A;
                font-size:17px;
                font-weight:600;">
                Welcome back, {teacher_data['name']} 👋
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        if st.button(
            "Logout",
            type="secondary",
            key="loginbackbtn",
            width="stretch",
            shortcut="control+backspace"
        ):
            st.session_state["is_logged_in"] = False
            del st.session_state.teacher_data
            st.rerun()

    st.space()

    # Initialize active dashboard tab
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    # Dashboard navigation
    tab1, tab2, tab3 = st.columns(3, gap="small")

    with tab1:
        type1 = (
            "primary"
            if st.session_state.current_teacher_tab == "take_attendance"
            else "secondary"
        )

        if st.button(
            "Take Attendance",
            type=type1,
            width="stretch",
            icon=":material/ar_on_you:"
        ):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with tab2:
        type2 = (
            "primary"
            if st.session_state.current_teacher_tab == "manage_subjects"
            else "secondary"
        )

        if st.button(
            "Manage Subjects",
            type=type2,
            width="stretch",
            icon=":material/book_ribbon:"
        ):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with tab3:
        type3 = (
            "primary"
            if st.session_state.current_teacher_tab == "attendance_records"
            else "secondary"
        )

        if st.button(
            "Attendance Records",
            type=type3,
            width="stretch",
            icon=":material/cards_stack:"
        ):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    st.divider()

    # Render selected dashboard content
    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()

    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()

    elif st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()



def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.subheader('Take AI Attendance')

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images=[]

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('You haven’t created any subjects yet! Please create one to begin!')
        return


    subject_options = {f"{s['name']} - {s['subject_code']}" : s['subject_id'] for s in subjects}

    col1, col2=st.columns([2,1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox(
            "Select subject",
            options=list(subject_options.keys())
            )

    with col2:
        if st.button('Add Photos', type="primary", width="stretch", icon=':material/photo_prints:',):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    # =========================
    # PHOTO GALLERY
    # =========================

    if st.session_state.attendance_images:
        st.subheader("Added Photos")

        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(
                    img,
                    width="stretch",
                    caption=f"Photo {idx + 1}"
                )

    # =========================
    # ACTION BUTTONS (ALWAYS VISIBLE)
    # =========================

    has_photos = bool(st.session_state.attendance_images)

    c1, c2, c3 = st.columns(3)

    # Clear photos
    with c1:
        if st.button(
            "Clear all photos",
            width="stretch",
            type="tertiary",
            icon=":material/delete:",
            disabled=not has_photos
        ):
            st.session_state.attendance_images = []
            st.rerun()

    # Face analysis
    with c2:
        if st.button(
            "Run Face Analysis",
            width="stretch",
            type="secondary",
            icon=":material/analytics:",
            disabled=not has_photos
        ):
            with st.spinner("Deep scanning classroom photos..."):

                all_detected_ids = {}

                for idx, img in enumerate(st.session_state.attendance_images):

                    img_np = np.array(img.convert("RGB"))

                    detected, _, _ = predict_attendance(img_np)

                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)

                            all_detected_ids.setdefault(
                                student_id, []
                            ).append(f"Photo {idx + 1}")

                # Fetch enrolled students
                enrolled_res = (
                    supabase.table("subject_students")
                    .select("*, students(*)")
                    .eq("subject_id", selected_subject_id)
                    .execute()
                )

                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning("No students enrolled in this course")

                else:
                    results = []
                    attendance_to_log = []

                    current_timestamp = datetime.now().strftime(
                        "%Y-%m-%dT%H:%M:%S"
                    )

                    for node in enrolled_students:

                        student = node["students"]

                        sources = all_detected_ids.get(
                            int(student["student_id"]), []
                        )

                        is_present = len(sources) > 0

                        results.append({
                            "Name": student["name"],
                            "ID": student["student_id"],
                            "Source": ", ".join(sources) if is_present else "-",
                            "Status": "✅ Present" if is_present else "Absent"
                        })

                        attendance_to_log.append({
                            "student_id": student["student_id"],
                            "subject_id": selected_subject_id,
                            "timestamp": current_timestamp,
                            "is_present": bool(is_present)
                        })

                    attendance_result_dialog(
                        pd.DataFrame(results),
                        attendance_to_log
                    )

    # Voice attendance
    with c3:
        if st.button(
            "Use Voice Attendance",
            type="primary",
            width="stretch",
            icon=":material/mic:"
        ):
            voice_attendance_dialog(selected_subject_id)
                                                                                            


                                

def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <h3 style="
                color: #25243A !important;
                font-size: 35px;
                font-weight: 800;
            ">
                Manage Subjects
            </h3>
        """, unsafe_allow_html=True)
        
    with col2:
        if st.button('Create New Subject', width='stretch'):
            create_subject_dialog(teacher_id)
    
    #List all subjects
    
    # List all subjects
    subjects = get_teacher_subjects(teacher_id)

    if subjects:

        for sub in subjects:

            stats = [
                ("", "Students", sub['total_students']),
                ("", "Classes", sub['total_clases'])
            ]

            def share_btn(sub=sub):
                if st.button(
                    f"Share Code: {sub['name']}",
                    key=f"Share_{sub['subject_code']}",
                    icon=":material/share:"
                ):
                    share_subject_dialog(
                        sub['name'],
                        sub['subject_code']
                    )

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )

    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")

def teacher_tab_attendance_records():
    st.subheader('Attendance Records')

    teacher_id = st.session_state.teacher_data['teacher_id']

    records = get_attendance_for_teacher(teacher_id)

    if not records:
        st.info("No attendance records found.")
        return

    data = []

    for r in records:
        ts = r.get('timestamp')

        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts.replace("Z", "+00:00")).strftime("%y-%m-%d %I:%M %p") if ts else "N/A",
            "Subject": r['subjects']['name'],
            "Subject_Code": r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })

    df = pd.DataFrame(data)

    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject_Code'])
        .agg(
            Present_Count=('is_present', 'sum'),
            Total_Count=('is_present', 'count')
        )
        .reset_index()
    )

    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + "/"
        + summary['Total_Count'].astype(str)
        + " students"
    )

    display_df = (
        summary.sort_values(by='ts_group', ascending=False)
        [['Time', 'Subject', 'Subject_Code', 'Attendance Stats']]
    )

    st.dataframe(display_df, width='stretch', hide_index=True)

    
def login_teacher(username, password):
    if not username or not password:
        return False
    
    teacher= teacher_login(username,password)

    if teacher:
        st.session_state.user_role='teacher'
        st.session_state.teacher_data=teacher
        st.session_state['is_logged_in'] = True
        return True

    return False





def _teacher_auth_styles():
    st.markdown("""
        <style>
        /* Compact, premium SmartRoll authentication inputs */
        div[data-testid="stTextInput"] {
            max-width: 100% !important;
            margin-bottom: 0.55rem !important;
        }
        div[data-testid="stTextInput"] label {
            color: #45445D !important;
            font-size: 0.88rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.25rem !important;
        }
        div[data-testid="stTextInput"] input {
            height: 56px !important;
            min-height: 56px !important;
            border-radius: 14px !important;
            padding: 0.75rem 1rem !important;
            font-size: 1.05rem !important;
            line-height: 1.2 !important;
            letter-spacing: normal !important;
            box-sizing: border-box !important;
        }
        div[data-testid="stTextInput"] input::placeholder {
            opacity: 0.65 !important;
        }
        div[data-testid="stButton"] button {
            min-height: 56px !important;
            height: 56px !important;
            border-radius: 14px !important;
            padding: 0.75rem 1rem !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 0.45rem !important;
            white-space: nowrap !important;
            line-height: 1.2 !important;
            letter-spacing: normal !important;
        }
        div[data-testid="stButton"] button p {
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1.2 !important;
            letter-spacing: normal !important;
            white-space: nowrap !important;
        }
        </style>
    """, unsafe_allow_html=True)


def teacher_screen_login():
    header_left, header_center, header_right = st.columns([1, 2, 1], vertical_alignment="center")

    with header_center:
        header_dashboard()    

    with header_right:
        if st.button("Go back to home", type="secondary", key="loginbackbtn", shortcut='control+backspace'):
            st.session_state["login_type"] = None
            st.rerun()

    _teacher_auth_styles()

    st.markdown("""
    <div style="text-align: center; margin: 18px 0 14px; width: 100%;">
        <div style="font-size: 15px; font-weight: 700; letter-spacing: 2px; color: #22D3EE; text-align: center;">
            TEACHER PORTAL
        </div>
        <div style="color: #25243A !important; font-size: 32px; font-weight: 700; line-height: 1.2; margin: 6px 0 4px; text-align: center;">
            Welcome back
        </div>
        <div style="color: #5F6078 !important; font-size: 14px; text-align: center;">
            Login to manage your classroom
        </div>
    </div>
""", unsafe_allow_html=True)

    # Narrow centered form on larger screens
    left, form_col, right = st.columns([1, 1.8, 1])
    with form_col:
        teacher_username = st.text_input("Username", placeholder="@yourusername", key="teacher_login_username")
        teacher_pass = st.text_input("Password", type="password", placeholder="Enter your password", key="teacher_login_password")

        st.write("")
        if st.button('Login', icon=':material/passkey:', shortcut='control+enter', width='stretch', key='teacher_login_submit'):
            if login_teacher(teacher_username, teacher_pass):
                st.toast('Welcome back!', icon="👋")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username and password")

        if st.button('Create teacher account', type='primary', icon=':material/person_add:', width='stretch', key='teacher_login_register'):
            st.session_state.teacher_login_type = 'register'
            st.rerun()


def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass or not teacher_pass_confirm:
        return False, "All Fields are required"
    if check_teacher_exists(teacher_username):
        return False, "Username already taken"
    if teacher_pass != teacher_pass_confirm:
        return False, "Password doesn't match"

    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Successfully created! Login Now"
    except Exception as e:
        return False, f"Unexpected Error: {e}"

    
def teacher_screen_register():
    header_left, header_center, header_right = st.columns([1, 2, 1], vertical_alignment="center")

    with header_center:
        header_dashboard()

    with header_right:
        if st.button("Go back to home", type="secondary", key="loginbackbtn", shortcut='control+backspace'):
            st.session_state["login_type"] = None
            st.rerun()

    _teacher_auth_styles()

    st.markdown("""
        <div style="text-align:center; margin: 22px 0 10px;">
            <div style="font-size:12px; font-weight:700; letter-spacing:2px; color:#22D3EE;">TEACHER PORTAL</div>
            <h2 style="color:#25243A !important; font-size:32px; margin:6px 0 0;">Create your account</h2>
            <p style="color:#5F6078 !important; margin:4px 0 0; font-size:14px;">Set up your teacher profile to get started</p>
        </div>
    """, unsafe_allow_html=True)

    left, form_col, right = st.columns([1, 1.8, 1])
    with form_col:
        teacher_username = st.text_input("Username", placeholder="@yourusername", key="teacher_register_username")
        teacher_name = st.text_input("Full name", placeholder="Your full name", key="teacher_register_name")
        teacher_pass = st.text_input("Password", type="password", placeholder="Create a password", key="teacher_register_password")
        teacher_pass_confirm = st.text_input("Confirm password", type="password", placeholder="Re-enter password", key="teacher_register_confirm")

        st.write("")
        if st.button('Register now', icon=':material/passkey:', shortcut='control+enter', width='stretch', key='teacher_register_submit'):
            success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = 'login'
                st.rerun()
            else:
                st.error(message)

        if st.button('Already have an account? Login', type='primary', icon=':material/login:', width='stretch', key='teacher_register_login'):
            st.session_state.teacher_login_type = 'login'
            st.rerun()
