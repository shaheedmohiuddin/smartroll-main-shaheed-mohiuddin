
import streamlit as st
import segno
import io
import html


@st.dialog("Share Subject")
def share_subject_dialog(subject_name, subject_code):

    app_domain = "https://smartroll-main.streamlit.app"
    join_url = f"{app_domain}/?join-code={subject_code}"

    safe_subject = html.escape(str(subject_name))
    safe_code = html.escape(str(subject_code))
    safe_url = html.escape(join_url)

    # Generate QR code
    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind="png", scale=6, border=4)

    # Dialog CSS
    st.html("""
    <style>
        .share-label {
            color: #7866D8;
            font-size: 1.2rem;
            font-weight: 800;
            letter-spacing: .12em;
        }

        .share-title {
            color: #25243A;
            font-size: 1.15rem;
            font-weight: 700;
            margin-top: 4px;
        }

        .share-description {
            color: #4B5563;
            font-size: .88rem;
            margin-top: 4px;
            line-height: 1.5;
        }

        .share-code-card {
            background: #F4F1FF;
            border: 1px solid #E8E5F2;
            border-radius: 10px;
            padding: 12px;
            color: #7866D8;
            font-size: 1.1rem;
            font-weight: 800;
            letter-spacing: 1.5px;
            overflow-wrap: anywhere;
        }

        .share-link-card {
            background: #F8F7FC;
            border: 1px solid #E8E5F2;
            border-radius: 10px;
            padding: 10px;
            color: #4B5563;
            font-size: .75rem;
            line-height: 1.5;
            overflow-wrap: anywhere;
            word-break: break-word;
        }
    </style>
    """)

    # Header
    st.html(f"""
        <div style="margin-bottom:12px;">
            <div class="share-label">CLASS INVITATION</div>
            <div class="share-title">
                Invite students to {safe_subject}
            </div>
            <div class="share-description">
                Share the subject code or QR code so students can enroll.
            </div>
        </div>
    """)

    # Original column proportions preserved
    left, right = st.columns(
        [1.2, 1],
        vertical_alignment="center"
    )

    # LEFT COLUMN
    with left:

        st.markdown("#### Subject code")

        st.html(f"""
            <div class="share-code-card">
                {safe_code}
            </div>
        """)

        st.markdown("#### Enrollment link")

        st.html(f"""
            <div class="share-link-card">
                {safe_url}
            </div>
        """)

        st.caption(
            "Students can open the link or enter the code "
            "in SmartRoll to join this subject."
        )

    # RIGHT COLUMN
    with right:

        st.markdown("#### QR code")

        st.image(
            out.getvalue(),
            width=220,
            caption="Scan to enroll"
        )

        st.caption(
            "Students can scan this QR code with their phone."
        )
