import streamlit as st
import os
import json
import uuid
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
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

# --- Session State Initialization ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "active_page" not in st.session_state:
    st.session_state.active_page = "Home"


# --- Helper Functions ---
def load_gallery():
    if not os.path.exists(METADATA_FILE):
        return []
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_gallery(data):
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
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


# --- Custom CSS (White Body + Black & Gold Theme) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

.stApp {
    background-color: #ffffff;
    color: #111827;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.block-container {
    padding-top: 0rem !important;
    padding-bottom: 3rem !important;
    padding-left: 0rem !important;
    padding-right: 0rem !important;
    max-width: 100% !important;
}

/* Top Announcement Bar (Black & Gold) */
.top-announcement {
    background-color: #111315;
    color: #f4f4f5;
    text-align: center;
    font-size: 0.82rem;
    font-weight: 500;
    padding: 0.55rem 1rem;
    letter-spacing: 0.2px;
}

.top-announcement span {
    color: #ecc953;
    font-weight: 600;
}

/* Brand Monogram */
.brand-box {
    display: flex;
    align-items: center;
    gap: 10px;
}

.gn-monogram {
    background-color: #111315;
    color: #ecc953;
    border: 1.5px solid #ecc953;
    font-weight: 800;
    font-size: 0.95rem;
    padding: 6px 9px;
    border-radius: 6px;
    letter-spacing: 0.5px;
    line-height: 1;
}

.brand-label {
    color: #111827;
    font-weight: 800;
    font-size: 0.94rem;
    letter-spacing: -0.2px;
}

/* Nav Links */
div[data-testid="stHorizontalBlock"] .stButton > button {
    background-color: transparent;
    color: #374151;
    border: none;
    font-size: 0.86rem;
    font-weight: 600;
    padding: 0.4rem 0.45rem;
    transition: color 0.15s ease;
}

div[data-testid="stHorizontalBlock"] .stButton > button:hover {
    color: #b8860b;
    background-color: transparent;
}

/* Primary Gold CTA Button */
.cta-gold > div > button {
    background-color: #ecc953 !important;
    color: #111315 !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.35rem !important;
    border: 1px solid #d4af37 !important;
    transition: all 0.2s ease !important;
}

.cta-gold > div > button:hover {
    background-color: #f5d76e !important;
    color: #111315 !important;
}

/* Secondary Black/Outline CTA Button */
.cta-outline > div > button {
    background-color: #ffffff !important;
    color: #111827 !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.35rem !important;
    border: 1px solid #d1d5db !important;
    transition: all 0.2s ease !important;
}

.cta-outline > div > button:hover {
    border-color: #111827 !important;
    background-color: #f9fafb !important;
}

/* Centered Hero Section */
.centered-hero {
    max-width: 860px;
    margin: 0 auto;
    text-align: center;
    padding: 4.2rem 1.5rem 1.8rem 1.5rem;
}

.hero-eyebrow {
    color: #b8860b;
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    margin-bottom: 1.1rem;
}

.hero-main-title {
    font-size: clamp(2.5rem, 5vw, 4.1rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -1.2px;
    color: #111827;
    margin-bottom: 1.3rem;
}

.hero-main-title .gold-line {
    color: #c59316;
    display: block;
}

.hero-subcopy {
    color: #4b5563;
    font-size: 1.08rem;
    line-height: 1.65;
    max-width: 660px;
    margin: 0 auto 2rem auto;
}

/* Credential Pill Strip */
.credential-strip {
    display: inline-flex;
    align-items: center;
    gap: 12px;
    background-color: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 999px;
    padding: 0.45rem 1.1rem;
    margin-top: 1.4rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #1f2937;
}

.pill-badge {
    background-color: #111315;
    color: #ecc953;
    padding: 3px 11px;
    border-radius: 999px;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.74rem;
}

/* Framed Preview Window */
.showcase-frame {
    max-width: 1020px;
    margin: 2.5rem auto 0 auto;
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 14px 40px rgba(17, 24, 39, 0.08);
}

.showcase-header {
    background-color: #111315;
    color: #d1d5db;
    padding: 0.85rem 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.82rem;
}

.showcase-body {
    padding: 2.2rem 2.5rem;
    background-color: #fafafa;
}

/* Standard Inner Page Container */
.page-container {
    max-width: 1120px;
    margin: 0 auto;
    padding: 3rem 2rem;
}

.section-kicker {
    color: #b8860b;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.45rem;
}

.section-heading {
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.6px;
    color: #111827;
    margin-bottom: 1.5rem;
}

.light-card {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-top: 3px solid #ecc953;
    border-radius: 12px;
    padding: 1.65rem;
    height: 100%;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
    transition: border-color 0.2s ease, transform 0.2s ease;
}

.light-card:hover {
    border-color: #111315;
}

.light-card h4 {
    color: #111827;
    font-size: 1.12rem;
    font-weight: 700;
    margin-bottom: 0.65rem;
}

.light-card p {
    color: #4b5563;
    font-size: 0.94rem;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. TOP ANNOUNCEMENT BANNER
# ==========================================
st.markdown("""
    <div class="top-announcement">
        🟡 Ol Moran Ward Development Initiative &nbsp;•&nbsp; Unity, Knowledge &amp; Wealth &nbsp;<span>Explore Our Vision →</span>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 2. TOP NAVIGATION BAR
# ==========================================
nav_brand, nav_links, nav_auth = st.columns([2.0, 5.8, 1.8], vertical_alignment="center")

with nav_brand:
    st.markdown("""
        <div style="padding: 0.75rem 0 0.75rem 2rem;" class="brand-box">
            <div class="gn-monogram">GN</div>
            <div class="brand-label">Gachara Ndirangu</div>
        </div>
    """, unsafe_allow_html=True)

with nav_links:
    pages = ["Home", "Why Gachara", "About", "Our Vision", "Achievements", "Events", "Gallery", "Contact"]
    link_cols = st.columns(len(pages))
    for idx, page_name in enumerate(pages):
        with link_cols[idx]:
            if st.button(page_name, key=f"nav_{page_name}", use_container_width=True):
                st.session_state.active_page = page_name
                st.rerun()

with nav_auth:
    st.markdown('<div style="padding-right: 1.5rem;">', unsafe_allow_html=True)
    if st.session_state.authenticated:
        c_adm, c_out = st.columns(2)
        with c_adm:
            st.markdown('<div class="cta-gold">', unsafe_allow_html=True)
            if st.button("Admin", key="nav_admin_panel", use_container_width=True):
                st.session_state.active_page = "Admin"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with c_out:
            st.markdown('<div class="cta-outline">', unsafe_allow_html=True)
            if st.button("Logout", key="nav_logout_btn", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.active_page = "Home"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        c_log, c_reg = st.columns(2)
        with c_log:
            st.markdown('<div class="cta-outline">', unsafe_allow_html=True)
            if st.button("Login", key="nav_login_btn", use_container_width=True):
                st.session_state.active_page = "Admin"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with c_reg:
            st.markdown('<div class="cta-gold">', unsafe_allow_html=True)
            if st.button("Join Us", key="nav_register_btn", use_container_width=True):
                st.session_state.active_page = "Contact"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr style='margin: 0; border-color: #e5e7eb;'>", unsafe_allow_html=True)

# ==========================================
# PAGE ROUTING
# ==========================================
active = st.session_state.active_page

# ------------------------------------------
# HOME PAGE
# ------------------------------------------
if active == "Home":
    st.markdown("""
        <div class="centered-hero">
            <div class="hero-eyebrow">FINANCE • COMPUTER SCIENCE • STRATEGIC LEADERSHIP</div>
            <div class="hero-main-title">
                A Stronger Ol Moran.
                <span class="gold-line">Built on Finance &amp; Technology.</span>
            </div>
            <div class="hero-subcopy">
                David Gachara Ndirangu combines financial discipline from Kenyatta University with advanced expertise in Computer Science &amp; IT to drive transparent governance, digital innovation, and sustainable opportunity across Ol Moran Ward.
            </div>
        </div>
    """, unsafe_allow_html=True)

    sp1, btn_col1, btn_col2, btn_col3, sp2 = st.columns([2.3, 1.5, 1.6, 1.3, 2.3], vertical_alignment="center")
    with btn_col1:
        st.markdown('<div class="cta-gold">', unsafe_allow_html=True)
        if st.button("Why Gachara →", key="hero_cta_why", use_container_width=True):
            st.session_state.active_page = "Why Gachara"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with btn_col2:
        st.markdown('<div class="cta-outline">', unsafe_allow_html=True)
        if st.button("Explore Our Vision", key="hero_cta_vision", use_container_width=True):
            st.session_state.active_page = "Our Vision"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with btn_col3:
        if st.button("View Gallery →", key="hero_cta_gallery", use_container_width=True):
            st.session_state.active_page = "Gallery"
            st.rerun()

    st.markdown("""
        <div style="text-align: center;">
            <div class="credential-strip">
                <span>B.Com (Finance) • Kenyatta University</span>
                <span class="pill-badge">CS &amp; IT Specialist</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="showcase-frame">
            <div class="showcase-header">
                <div>📄 <strong style="color:#ecc953;">gachara_ndirangu.profile</strong> &nbsp;•&nbsp; Ol Moran Ward, Laikipia</div>
                <div>Naiborom Primary &nbsp;→&nbsp; Alliance High School &nbsp;→&nbsp; Kenyatta University</div>
            </div>
            <div class="showcase-body">
    """, unsafe_allow_html=True)

    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        st.markdown("""
            <div class="light-card">
                <h4>📊 Financial Acumen</h4>
                <p>Bachelor of Commerce (Finance) training applied to transparent ward budgeting, resource accountability, and local cooperative growth.</p>
            </div>
        """, unsafe_allow_html=True)
    with sc2:
        st.markdown("""
            <div class="light-card">
                <h4>💻 Computer Science &amp; IT</h4>
                <p>Modern software engineering, data-driven decision-making, and digital skills empowerment for youth and local enterprises.</p>
            </div>
        """, unsafe_allow_html=True)
    with sc3:
        st.markdown("""
            <div class="light-card">
                <h4>🤝 Impactful Leadership</h4>
                <p>Rooted in Naiborom Primary and Alliance High School values—listening closely and delivering practical infrastructure and security solutions.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

# ------------------------------------------
# WHY GACHARA PAGE
# ------------------------------------------
elif active == "Why Gachara":
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">THE CASE FOR MULTIDISCIPLINARY LEADERSHIP</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Why Gachara Ndirangu?</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="light-card" style="margin-bottom: 2rem;">
            <p style="font-size: 1.06rem; color: #1f2937;">
                Modern ward representation demands more than promises—it requires <strong>financial literacy</strong> to manage public funds responsibly and <strong>technological fluency</strong> to connect residents to modern economic opportunities. David Gachara Ndirangu brings both.
            </p>
        </div>
    """, unsafe_allow_html=True)

    w1, w2, w3 = st.columns(3)
    with w1:
        st.markdown("""
            <div class="light-card">
                <h4>1. Proven Financial Discipline</h4>
                <p>With a Bachelor of Commerce (Finance) from Kenyatta University, every project is evaluated for cost-effectiveness, transparency, and measurable community return.</p>
            </div>
        """, unsafe_allow_html=True)
    with w2:
        st.markdown("""
            <div class="light-card">
                <h4>2. Future-Ready Tech Adoption</h4>
                <p>Advanced Computer Science &amp; IT expertise enables smarter service delivery, digital literacy programs for youth, and data-backed planning for water and agriculture.</p>
            </div>
        """, unsafe_allow_html=True)
    with w3:
        st.markdown("""
            <div class="light-card">
                <h4>3. Deep Local Roots</h4>
                <p>Educated at Naiborom Primary School and Alliance High School, he understands the everyday realities of Ol Moran families and brings national-caliber leadership home.</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# ABOUT PAGE
# ------------------------------------------
elif active == "About":
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">BIOGRAPHY &amp; CREDENTIALS</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">About David Gachara Ndirangu</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="light-card" style="margin-bottom: 2rem;">
            <p style="font-size: 1.08rem; color: #1f2937;">
                <strong>David Gachara Ndirangu</strong> is a multidisciplinary professional with expertise spanning finance, computer science, and technology. 
                An alumnus of <strong>Naiborom Primary School</strong> and <strong>Alliance High School</strong>, he holds a 
                <strong>Bachelor of Commerce (Finance)</strong> from <strong>Kenyatta University</strong> and advanced training in 
                <strong>Computer Science &amp; IT</strong>. His unique combination of financial acumen and technical expertise enables him 
                to drive strategic decision-making, technological adoption, and impactful leadership.
            </p>
        </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
            <div class="light-card">
                <h4>Education &amp; Training</h4>
                <p>
                    • <strong>Kenyatta University:</strong> Bachelor of Commerce (Finance)<br><br>
                    • <strong>Computer Science &amp; IT:</strong> Advanced Software, Data &amp; Systems Training<br><br>
                    • <strong>Alliance High School:</strong> Kenya Certificate of Secondary Education<br><br>
                    • <strong>Naiborom Primary School:</strong> Primary Education (Ol Moran Ward)
                </p>
            </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
            <div class="light-card">
                <h4>Core Leadership Values</h4>
                <p>
                    • <strong>Unity:</strong> Bringing every community across Ol Moran Ward together around shared goals.<br><br>
                    • <strong>Knowledge:</strong> Expanding access to quality education, ICT training, and youth mentorship.<br><br>
                    • <strong>Wealth:</strong> Unlocking agricultural value chains, market access, and local enterprise.
                </p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# OUR VISION PAGE
# ------------------------------------------
elif active == "Our Vision":
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">PEOPLE • PROGRESS • POSSIBILITY</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Strategic Vision for Ol Moran Ward</div>', unsafe_allow_html=True)

    v1, v2, v3 = st.columns(3)
    with v1:
        st.markdown("""
            <div class="light-card">
                <h4>01. Youth &amp; Digital Economy</h4>
                <p>Establishing ICT empowerment hubs, coding and digital skills bootcamps, and youth enterprise support across the ward.</p>
            </div>
        """, unsafe_allow_html=True)
    with v2:
        st.markdown("""
            <div class="light-card">
                <h4>02. Agricultural Resilience</h4>
                <p>Strengthening farmer cooperatives, water harvesting, and fair market linkages using sound financial planning.</p>
            </div>
        """, unsafe_allow_html=True)
    with v3:
        st.markdown("""
            <div class="light-card">
                <h4>03. Security &amp; Infrastructure</h4>
                <p>Championing passable rural roads, reliable water points, solar lighting, and human-wildlife conflict mitigation.</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# ACHIEVEMENTS PAGE
# ------------------------------------------
elif active == "Achievements":
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">TRACK RECORD</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Key Milestones &amp; Initiatives</div>', unsafe_allow_html=True)

    a1, a2 = st.columns(2)
    with a1:
        st.markdown("""
            <div class="light-card">
                <h4>Technology &amp; Digital Systems</h4>
                <p>Built and deployed custom software tools, financial analytics solutions, and digital platforms supporting organizations and entrepreneurs.</p>
            </div>
        """, unsafe_allow_html=True)
    with a2:
        st.markdown("""
            <div class="light-card">
                <h4>Student Mentorship &amp; Community Support</h4>
                <p>Led academic guidance and motivational programs for primary and secondary students across Naiborom and Ol Moran Ward.</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# EVENTS PAGE
# ------------------------------------------
elif active == "Events":
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">COMMUNITY ENGAGEMENT</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Ward Forums &amp; Outreach</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="light-card">
            <h4>Ol Moran Ward Listening &amp; Youth Empowerment Forums</h4>
            <p>Interactive community sessions across Naiborom, Kio, and Wangwachi focused on agriculture, youth skills, and local infrastructure priorities. Visit the Gallery tab to view highlights.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# GALLERY PAGE
# ------------------------------------------
elif active == "Gallery":
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    col_g1, col_g2 = st.columns([4, 1], vertical_alignment="center")
    with col_g1:
        st.markdown('<div class="section-kicker">MOMENTS &amp; COMMUNITY ACTION</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">Photo Gallery</div>', unsafe_allow_html=True)
    with col_g2:
        if st.session_state.authenticated:
            st.markdown('<div class="cta-gold">', unsafe_allow_html=True)
            if st.button("+ Upload Photos", use_container_width=True):
                st.session_state.active_page = "Admin"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    gallery_items = load_gallery()

    if not gallery_items:
        st.info("No photos in the gallery yet. Click 'Login' in the top-right corner to sign in as Admin and upload photos.")
    else:
        cols = st.columns(3)
        for idx, item in enumerate(gallery_items):
            img_path = os.path.join(UPLOAD_DIR, item["filename"])
            if os.path.exists(img_path):
                with cols[idx % 3]:
                    st.image(img_path, use_container_width=True)
                    st.markdown(f"""
                        <div style="background:#ffffff; padding:0.85rem 1rem; border-radius:0 0 10px 10px; border:1px solid #e5e7eb; border-top:none; margin-bottom:1.5rem; box-shadow:0 4px 12px rgba(0,0,0,0.04);">
                            <div style="color:#b8860b; font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:1px;">{item.get('category', 'Gallery')}</div>
                            <div style="color:#111827; font-weight:700; font-size:0.95rem; margin-top:2px;">{item['caption']}</div>
                            <div style="color:#6b7280; font-size:0.78rem; margin-top:4px;">{item['uploaded_at']}</div>
                        </div>
                    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# CONTACT PAGE
# ------------------------------------------
elif active == "Contact":
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">GET INVOLVED</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Join the Movement</div>', unsafe_allow_html=True)

    with st.form("volunteer_form"):
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number / WhatsApp")
        area = st.text_input("Village / Polling Station in Ol Moran Ward")
        message = st.text_area("How would you like to collaborate or share your feedback?")
        if st.form_submit_button("Submit"):
            if name and phone:
                st.success(f"Thank you, {name}! Your message has been received.")
            else:
                st.warning("Please provide your name and phone number.")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# ADMIN PORTAL
# ------------------------------------------
elif active == "Admin":
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">ADMINISTRATOR ACCESS</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Gallery Management Portal</div>', unsafe_allow_html=True)

    if not st.session_state.authenticated:
        col_spacer1, col_login, col_spacer2 = st.columns([1, 1.5, 1])
        with col_login:
            with st.form("admin_login_form"):
                st.subheader("Sign In")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login", use_container_width=True)

                if submitted:
                    if username == ADMIN_USER and password == ADMIN_PASS:
                        st.session_state.authenticated = True
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
    else:
        st.success("Authenticated as Administrator (`admin`).")

        with st.form("upload_gallery_form", clear_on_submit=True):
            st.subheader("Upload New Photos to Gallery")
            uploaded_files = st.file_uploader(
                "Choose photo(s) (JPG, PNG, WEBP)",
                type=["png", "jpg", "jpeg", "webp"],
                accept_multiple_files=True
            )
            c_cap, c_cat = st.columns([2, 1])
            with c_cap:
                caption = st.text_input("Photo Caption", placeholder="e.g., Youth Engagement Forum in Ol Moran")
            with c_cat:
                category = st.selectbox(
                    "Category",
                    ["Campaign & Community", "Youth & Innovation", "Leadership & Events", "Projects"]
                )

            upload_submitted = st.form_submit_button("Publish to Gallery")
            if upload_submitted:
                if uploaded_files:
                    for file in uploaded_files:
                        save_uploaded_image(file, caption, category)
                    st.success(f"Uploaded {len(uploaded_files)} photo(s) to the Gallery!")
                    st.rerun()
                else:
                    st.warning("Please select at least one photo.")

        st.markdown("---")
        st.subheader("Manage Published Gallery Photos")
        current_items = load_gallery()
        if not current_items:
            st.info("No photos uploaded yet.")
        else:
            for item in current_items:
                c1, c2, c3 = st.columns([1, 4, 1], vertical_alignment="center")
                img_path = os.path.join(UPLOAD_DIR, item["filename"])
                with c1:
                    if os.path.exists(img_path):
                        st.image(img_path, width=90)
                with c2:
                    st.write(f"**{item['caption']}**")
                    st.caption(f"{item.get('category', 'Gallery')} • Uploaded {item['uploaded_at']}")
                with c3:
                    if st.button("Delete", key=f"del_{item['id']}", use_container_width=True):
                        delete_image(item["id"])
                        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
