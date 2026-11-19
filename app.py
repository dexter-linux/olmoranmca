import streamlit as st
import os
import json
import uuid
import base64
from datetime import datetime
from PIL import Image

# --- Page Configuration ---
st.set_page_config(
    page_title="Gachara Ndirangu | Ol Moran Ward",
    page_icon="🟡",
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

# --- Session State Initialization ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "active_page" not in st.session_state:
    st.session_state.active_page = "Home"

# --- Helper Functions ---
def load_gallery():
    with open(METADATA_FILE, "r") as f:
        return json.load(f)

def save_gallery(data):
    with open(METADATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def save_uploaded_image(uploaded_file, caption, category="Campaign & Community"):
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, unique_filename)
    
    img = Image.open(uploaded_file)
    img.save(filepath)
    
    gallery_data = load_gallery()
    gallery_data.insert(0, {
        "id": unique_filename,
        "filename": unique_filename,
        "caption": caption.strip() if caption.strip() else uploaded_file.name,
        "category": category,
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

def get_hero_bg_css():
    """Uses local hero_bg.jpg if placed in root folder, otherwise uses a high-res community fallback."""
    local_bg = "hero_bg.jpg"
    if os.path.exists(local_bg):
        with open(local_bg, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"url('data:image/jpeg;base64,{b64}')"
    return "url('https://images.unsplash.com/photo-1529156069898-49953e39b3ac?auto=format&fit=crop&w=1920&q=80')"

# --- Custom CSS matching the Screenshot Aesthetic ---
hero_bg_url = get_hero_bg_css()

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@700;800;900&display=swap');

/* Hide default Streamlit chrome */
#MainMenu {{visibility: hidden;}}
header {{visibility: hidden;}}
footer {{visibility: hidden;}}

.stApp {{
    background-color: #16181a;
    color: #f4f4f4;
    font-family: 'Inter', sans-serif;
}}

.block-container {{
    padding-top: 0rem !important;
    padding-bottom: 2rem !important;
    padding-left: 0rem !important;
    padding-right: 0rem !important;
    max-width: 100% !important;
}}

/* Top Navbar Container */
.navbar-wrapper {{
    background-color: #1a1c1e;
    border-bottom: 1px solid #2c2f33;
    padding: 0.75rem 3.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}}

.brand-box {{
    display: flex;
    align-items: center;
    gap: 14px;
}}

.gn-monogram {{
    border: 1.5px solid #ecc953;
    color: #ecc953;
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    font-size: 1.15rem;
    padding: 6px 10px;
    letter-spacing: 1px;
    line-height: 1;
}}

.brand-text-top {{
    color: #ffffff;
    font-weight: 700;
    font-size: 0.92rem;
    letter-spacing: 0.5px;
    line-height: 1.2;
}}

.brand-text-sub {{
    color: #ecc953;
    font-weight: 600;
    font-size: 0.68rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}}

/* Streamlit Nav Buttons Styling */
div[data-testid="stHorizontalBlock"] .stButton > button {{
    background-color: transparent;
    color: #e2e8f0;
    border: none;
    font-size: 0.88rem;
    font-weight: 500;
    padding: 0.4rem 0.6rem;
    transition: color 0.2s ease;
}}

div[data-testid="stHorizontalBlock"] .stButton > button:hover {{
    color: #ecc953;
    background-color: transparent;
}}

/* Gold Action Buttons (Login / Admin) */
.gold-btn > div > button {{
    background-color: #ecc953 !important;
    color: #16181a !important;
    font-weight: 600 !important;
    border-radius: 4px !important;
    padding: 0.45rem 1.2rem !important;
    border: none !important;
}}

.gold-btn > div > button:hover {{
    background-color: #f6d870 !important;
    color: #16181a !important;
}}

/* Hero Section */
.hero-section {{
    position: relative;
    width: 100%;
    min-height: 82vh;
    background-image: linear-gradient(
        90deg,
        rgba(20, 22, 24, 0.92) 0%,
        rgba(24, 27, 30, 0.78) 52%,
        rgba(24, 27, 30, 0.55) 100%
    ), {hero_bg_url};
    background-size: cover;
    background-position: center right;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 4rem 5rem;
}}

.hero-kicker {{
    color: #ecc953;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 8px;
}}

.hero-dot {{
    height: 7px;
    width: 7px;
    background-color: #ecc953;
    border-radius: 50%;
    display: inline-block;
}}

.hero-headline {{
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(2.8rem, 5.2vw, 4.7rem);
    font-weight: 800;
    line-height: 1.04;
    color: #ffffff;
    text-transform: uppercase;
    margin-bottom: 1.8rem;
    max-width: 760px;
}}

.hero-headline .gold-accent {{
    color: #ecc953;
    display: block;
}}

.hero-candidate-name {{
    font-size: 1.35rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.25rem;
}}

.hero-candidate-role {{
    color: #ecc953;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-bottom: 1rem;
}}

.hero-tagline {{
    color: #d1d5db;
    font-size: 1.02rem;
    line-height: 1.6;
    max-width: 540px;
}}

/* Inner Content Container */
.page-container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 3rem 2.5rem;
}}

.section-kicker {{
    color: #ecc953;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}}

.section-heading {{
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 1.5rem;
}}

.dark-card {{
    background-color: #1f2226;
    border: 1px solid #2e3238;
    border-top: 3px solid #ecc953;
    border-radius: 6px;
    padding: 1.75rem;
    height: 100%;
}}

.dark-card h4 {{
    color: #ecc953;
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem;
    margin-bottom: 0.75rem;
}}

.dark-card p {{
    color: #cbd5e1;
    font-size: 0.95rem;
    line-height: 1.6;
}}
</style>
""", unsafe_allow_html=True)

# ==========================================
# TOP NAVIGATION BAR
# ==========================================
nav_col_brand, nav_col_links, nav_col_auth = st.columns([2.4, 5.2, 1.8], vertical_alignment="center")

with nav_col_brand:
    st.markdown("""
        <div style="padding: 0.8rem 0 0.8rem 2.5rem;" class="brand-box">
            <div class="gn-monogram">GN</div>
            <div>
                <div class="brand-text-top">GACHARA NDIRANGU</div>
                <div class="brand-text-sub">OL MORAN WARD</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with nav_col_links:
    pages = ["Home", "About Gachara", "Our Vision", "Achievements", "Events", "Gallery", "Contact"]
    link_cols = st.columns(len(pages))
    for idx, page_name in enumerate(pages):
        with link_cols[idx]:
            label = f"🟡 {page_name}" if st.session_state.active_page == page_name else page_name
            if st.button(page_name, key=f"nav_{page_name}", use_container_width=True):
                st.session_state.active_page = page_name
                st.rerun()

with nav_col_auth:
    st.markdown('<div class="gold-btn" style="padding-right: 2rem;">', unsafe_allow_html=True)
    if st.session_state.authenticated:
        c_adm, c_out = st.columns(2)
        with c_adm:
            if st.button("Admin", key="nav_admin_panel", use_container_width=True):
                st.session_state.active_page = "Admin"
                st.rerun()
        with c_out:
            if st.button("Logout", key="nav_logout_btn", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.active_page = "Home"
                st.rerun()
    else:
        c_log, c_reg = st.columns(2)
        with c_log:
            if st.button("Login", key="nav_login_btn", use_container_width=True):
                st.session_state.active_page = "Admin"
                st.rerun()
        with c_reg:
            if st.button("Register", key="nav_register_btn", use_container_width=True):
                st.session_state.active_page = "Contact"
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr style='margin: 0; border-color: #2c2f33;'>", unsafe_allow_html=True)

# ==========================================
# PAGE ROUTING
# ==========================================
active = st.session_state.active_page

# ------------------------------------------
# 1. HOME PAGE (Hero Banner + Quick Summary)
# ------------------------------------------
if active == "Home":
    st.markdown("""
        <div class="hero-section">
            <div class="hero-kicker">
                <span class="hero-dot"></span> PEOPLE &nbsp;•&nbsp; PROGRESS &nbsp;•&nbsp; POSSIBILITY
            </div>
            <div class="hero-headline">
                A STRONGER
                <span class="gold-accent">OL MORAN</span>
                STARTS WITH US.
            </div>
            <div class="hero-candidate-name">Gachara Ndirangu</div>
            <div class="hero-candidate-role">MCA ASPIRANT • OL MORAN WARD</div>
            <div class="hero-tagline">
                Unity, Knowledge and Wealth. A shared commitment to listening, working together and building opportunities across our ward.
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">LEADERSHIP & EXPERTISE</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Multidisciplinary Vision for Ol Moran</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
            <div class="dark-card">
                <h4>Finance & Resource Stewardship</h4>
                <p>Holding a Bachelor of Commerce (Finance) from Kenyatta University, David Gachara Ndirangu brings disciplined budgeting, transparent allocation, and economic empowerment to community development.</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="dark-card">
                <h4>Computer Science & Technology</h4>
                <p>With advanced training in Computer Science & IT, he champions digital literacy, youth innovation hubs, and modern technology adoption to unlock new opportunities across Ol Moran Ward.</p>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
            <div class="dark-card">
                <h4>Rooted in Excellence</h4>
                <p>An alumnus of Naiborom Primary School and Alliance High School, his leadership combines local grassroots understanding with strategic national-level problem solving.</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# 2. ABOUT GACHARA
# ------------------------------------------
elif active == "About Gachara":
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">BIOGRAPHY & BACKGROUND</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">About David Gachara Ndirangu</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="dark-card" style="margin-bottom: 2rem;">
            <p style="font-size: 1.08rem; color: #f1f5f9;">
                <strong>David Gachara Ndirangu</strong> is a multidisciplinary professional with expertise spanning finance, computer science, and technology. 
                An alumnus of <strong>Naiborom Primary School</strong> and <strong>Alliance High School</strong>, he holds a 
                <strong>Bachelor of Commerce (Finance)</strong> from <strong>Kenyatta University</strong> and advanced training in 
                <strong>Computer Science & IT</strong>. His unique combination of financial acumen and technical expertise enables him 
                to drive strategic decision-making, technological adoption, and impactful leadership.
            </p>
        </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
            <div class="dark-card">
                <h4>Academic Foundation</h4>
                <p>
                    • <strong>Kenyatta University:</strong> Bachelor of Commerce (Finance)<br><br>
                    • <strong>Computer Science & IT:</strong> Advanced Technical & Systems Training<br><br>
                    • <strong>Alliance High School:</strong> Secondary Education<br><br>
                    • <strong>Naiborom Primary School:</strong> Primary Education (Ol Moran Ward)
                </p>
            </div>
        """, unsafe_allow_html=True)
    with col_b:
