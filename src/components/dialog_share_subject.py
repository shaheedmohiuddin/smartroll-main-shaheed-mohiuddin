import streamlit as st
import segno
import io


@st.dialog("Share Subject")
def share_subject_dialog(subject_name, subject_code):
    app_domain = "smartroll-main.streamlit.app"
    join_url = f"{app_domain}/?join-code={subject_code}"

    st.markdown(
        f"""
        <div style="margin-bottom:12px;">
            <div style="color:#22D3EE;font-size:.72rem;font-weight:800;letter-spacing:.12em;">
                CLASS INVITATION
            </div>
            <div style="color:#F1F5F9;font-size:1.15rem;font-weight:700;margin-top:4px;">
                Invite students to {subject_name}
            </div>
            <div style="color:#94A3B8;font-size:.88rem;margin-top:4px;">
                Share the subject code or QR code so students can enroll.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind="png", scale=6, border=4)

    left, right = st.columns([1.2, 1], vertical_alignment="center")

    with left:
        st.markdown("#### Subject code")
        st.code(str(subject_code), language="text")
        st.markdown("#### Enrollment link")
        st.code(join_url, language="text")
        st.caption("Students can open the link or enter the code in SmartRoll to join this subject.")

    with right:
        st.markdown("#### QR code")
        st.image(out.getvalue(), width=220, caption="Scan to enroll")
        st.caption("Students can scan this QR code with their phone.")

   