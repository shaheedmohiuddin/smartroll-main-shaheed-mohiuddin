
import hashlib
import streamlit as st
from PIL import Image


@st.dialog("Add classroom photos")
def add_photos_dialog():
    """Capture or upload classroom photos for attendance; keeps images in session state."""

    st.markdown(
        """
        <div style="margin-bottom:12px;">
          <div style="color:#7866D8;font-size:1.2rem;font-weight:800;letter-spacing:.12em;">
            FACE ATTENDANCE
          </div>
          <div style="color:#25243A;font-size:1.15rem;font-weight:700;margin-top:4px;">
            Add classroom photos
          </div>
          <div style="color:#4B5563;font-size:.88rem;margin-top:4px;">
            Capture a classroom snapshot or upload clear images. Try to include students' faces
            with good lighting and minimal blur.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    if "photo_tab" not in st.session_state:
        st.session_state.photo_tab = "camera"

    if "added_photo_hashes" not in st.session_state:
        st.session_state.added_photo_hashes = set()

    # Camera and Upload tabs
    tab_camera, tab_upload = st.columns(2)

    with tab_camera:
        if st.button(
            "📷  Camera",
            type="primary" if st.session_state.photo_tab == "camera" else "secondary",
            width="stretch",
        ):
            st.session_state.photo_tab = "camera"
            st.rerun()

    with tab_upload:
        if st.button(
            "⬆️  Upload photos",
            type="primary" if st.session_state.photo_tab == "upload" else "secondary",
            width="stretch",
        ):
            st.session_state.photo_tab = "upload"
            st.rerun()

    # Light theme instruction card
    st.markdown(
        """
        <div style="
            background:#F4F1FF;
            border:1px solid #E8E5F2;
            border-radius:12px;
            padding:12px 14px;
            margin:10px 0;
            color:#4B5563;
            font-size:.85rem;
            line-height:1.6;
        ">
          <strong style="color:#25243A;">Tip:</strong>
          Use a wide classroom image with faces visible.
          Avoid very dark or blurry photos.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Camera tab
    if st.session_state.photo_tab == "camera":

        cam_photo = st.camera_input(
            "Take a classroom snapshot",
            key="dialog_cam"
        )

        if cam_photo is not None:
            raw = cam_photo.getvalue()
            photo_hash = hashlib.sha256(raw).hexdigest()

            if photo_hash not in st.session_state.added_photo_hashes:

                image = Image.open(cam_photo).convert("RGB").copy()

                st.session_state.attendance_images.append(image)
                st.session_state.added_photo_hashes.add(photo_hash)

                st.toast("Photo captured and added!")
                st.rerun()

    # Upload tab
    elif st.session_state.photo_tab == "upload":

        uploaded_files = st.file_uploader(
            "Choose image files",
            type=("jpg", "png", "jpeg"),
            accept_multiple_files=True,
            key="dialog_upload",
            help="You can select multiple classroom images at once.",
        )

        if uploaded_files:

            added_count = 0

            for file in uploaded_files:

                raw = file.getvalue()
                photo_hash = hashlib.sha256(raw).hexdigest()

                if photo_hash not in st.session_state.added_photo_hashes:

                    image = Image.open(file).convert("RGB").copy()

                    st.session_state.attendance_images.append(image)
                    st.session_state.added_photo_hashes.add(photo_hash)

                    added_count += 1

            if added_count:
                st.toast(f"{added_count} photo(s) added.")
                st.rerun()

    st.divider()

    # Photo preview section
    photos = st.session_state.attendance_images

    st.markdown(
        f"**Photos ready for scanning: {len(photos)}**"
    )

    if photos:

        preview_cols = st.columns(min(4, len(photos)))

        for idx, photo in enumerate(photos[-4:]):

            with preview_cols[idx]:

                st.image(
                    photo,
                    caption=f"Photo {len(photos)-min(4,len(photos))+idx+1}",
                    width="stretch"
                )

    # Bottom actions
    col_clear, col_done = st.columns(2)

    with col_clear:

        if st.button(
            "Clear photos",
            type="secondary",
            width="stretch",
            disabled=not photos
        ):
            st.session_state.attendance_images.clear()
            st.session_state.added_photo_hashes.clear()
            st.rerun()

    with col_done:

        if st.button(
            "Done",
            type="primary",
            width="stretch"
        ):
            st.rerun()
