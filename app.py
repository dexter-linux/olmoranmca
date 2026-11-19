import streamlit as st
import os
import json
import uuid
from datetime import datetime
from PIL import Image

# --- Page Configuration ---
st.set_page_config(
    page_title="David Gachara Ndirangu | Finance, CS & Technology",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Constants & Storage Setup ---
UPLOAD_DIR = "gallery_uploads"
METADATA_FILE = os.path.join(UPLOAD_DIR, "metadata.json")
ADMIN_USER = "admin"
ADMIN_PASS = "Ga12ca34ra56$"

os.makedirs(UPLOAD_DIR, exist_ok=True)
if not os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, "w") as f:
        json.dump([], f)

# --- Helper Functions ---
def load_gallery():
    with open(METADATA_FILE, "r") as f:
        return json.load(f)

def save_gallery(data):
    with open(METADATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def save_uploaded_image(uploaded_file, caption):
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Open and save via PIL to ensure clean image formatting
    img = Image.open(uploaded_file)
    img.save(filepath)
    
    gallery_data = load_gallery()
    gallery_data.insert(0, {
        "id": unique_filename,
        "filename": unique_filename,
        "caption": caption.strip() if caption.strip() else uploaded_file.name,
        "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    save_gallery(gallery_data)

def delete_image(image_id):
    gallery_data = load_gallery()
    updated_data = [item for item in gallery_data if item["id"] != image_id]
    filepath = os.path.join(UPLOAD_DIR, image_id)
    if os.path.exists(filepath):
        os.remove(filepath)
    save_gallery(updated_data)

# --- Custom Styling ---
st.markdown("""
    <style>
    .hero-box {
        background: linear-gradient(135deg, #004d4d 0%, #002b36 100%);
        padding: 2.5rem;
        border-radius: 12px;
        color: #ffffff;
        margin-bottom: 1.5rem;
        border-left: 6px solid #2aa198;
    }
    .hero-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: #93a1a1;
        margin-bottom: 1.2rem;
    }
    .card {
        background-color: #161b22;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #30363d;
        height: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# --- Session State for Auth ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- Navigation Tabs ---
tab_profile, tab_gallery, tab_admin = st.tabs(["🏛️ Profile & Expertise", "🖼️ Gallery", "🔐 Admin Portal"])

# ==========================================
# TAB 1: PROFILE & EXPERTISE
# ==========================================
with tab_profile:
    st.markdown("""
        <div class="hero-box">
            <div class="hero-title">David Gachara Ndirangu</div>
            <div class="hero-subtitle">Finance • Computer Science • Strategic Technology Leadership</div>
            <p style="font-size: 1.05rem; line-height: 1.6;">
                David Gachara Ndirangu is a multidisciplinary professional with expertise spanning finance, computer science, and technology. 
                An alumnus of <strong>Naiborom Primary School</strong> and <strong>Alliance High School</strong>, he holds a 
                <strong>Bachelor of Commerce (Finance)</strong> from <strong>Kenyatta University</strong> and advanced training in 
                <strong>Computer Science & IT</strong>. His unique combination of financial acumen and technical expertise enables him 
                to drive strategic decision-making, technological adoption, and impactful leadership.
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="card">
                <h4>📊 Financial Acumen</h4>
                <p>Grounded in a Bachelor of Commerce (Finance) from Kenyatta University, applying quantitative modeling, fiscal discipline, and strategic resource allocation to drive sustainable growth.</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="card">
                <h4>💻 Computer Science & IT</h4>
                <p>Advanced training in software engineering, data systems, and modern web architecture—bridging the gap between complex technical infrastructure and business objectives.</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="card">
                <h4>🧭 Strategic Leadership</h4>
                <p>Shaped by foundational excellence at Naiborom Primary and Alliance High School, championing innovation, digital transformation, and community-focused impact.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Academic & Professional Foundation")
    st.markdown("""
    - **Tertiary Education:** Bachelor of Commerce (Finance) — *Kenyatta University*
    - **Technical Specialization:** Advanced Training in Computer Science & Information Technology
    - **Secondary Education:** *Alliance High School*
    - **Primary Education:** *Naiborom Primary School*
    """)

# ==========================================
# TAB 2: GALLERY
# ==========================================
with tab_gallery:
    st.header("Photo Gallery")
    gallery_items = load_gallery()

    if not gallery_items:
        st.info("No photos have been uploaded to the gallery yet. Log in via the Admin Portal tab to add photos.")
    else:
        cols = st.columns(3)
        for idx, item in enumerate(gallery_items):
            img_path = os.path.join(UPLOAD_DIR, item["filename"])
            if os.path.exists(img_path):
                with cols[idx % 3]:
                    st.image(img_path, use_container_width=True)
                    st.caption(f"**{item['caption']}** • *{item['uploaded_at']}*")

# ==========================================
# TAB 3: ADMIN PORTAL
# ==========================================
with tab_admin:
    st.header("Admin Portal")

    if not st.session_state.authenticated:
        with st.form("login_form"):
            st.subheader("Administrator Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

            if submitted:
                if username == ADMIN_USER and password == ADMIN_PASS:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
    else:
        col_head, col_logout = st.columns([5, 1])
        with col_head:
            st.success("Logged in as Administrator")
        with col_logout:
            if st.button("Logout"):
                st.session_state.authenticated = False
                st.rerun()

        st.subheader("Upload New Photos")
        with st.form("upload_form", clear_on_submit=True):
            uploaded_files = st.file_uploader(
                "Select photo(s) to publish to the Gallery",
                type=["png", "jpg", "jpeg", "webp"],
                accept_multiple_files=True
            )
            caption = st.text_input("Caption (applied to uploaded photo(s))", placeholder="e.g., Keynote Presentation / Community Project")
            upload_btn = st.form_submit_button("Upload to Gallery")

            if upload_btn:
                if uploaded_files:
                    for file in uploaded_files:
                        save_uploaded_image(file, caption)
                    st.success(f"Successfully uploaded {len(uploaded_files)} photo(s)!")
                    st.rerun()
                else:
                    st.warning("Please select at least one image file before uploading.")

        st.markdown("---")
        st.subheader("Manage Existing Gallery Photos")
        current_items = load_gallery()
        if not current_items:
            st.write("Gallery is currently empty.")
        else:
            for item in current_items:
                c1, c2, c3 = st.columns([1, 4, 1])
                img_path = os.path.join(UPLOAD_DIR, item["filename"])
                with c1:
                    if os.path.exists(img_path):
                        st.image(img_path, width=80)
                with c2:
                    st.write(f"**{item['caption']}**")
                    st.caption(f"Uploaded: {item['uploaded_at']}")
                with c3:
                    if st.button("Delete", key=f"del_{item['id']}"):
                        delete_image(item["id"])
                        st.rerun()
