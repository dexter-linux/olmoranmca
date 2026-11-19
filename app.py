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


def get_hero_bg_css():
    local_bg = "hero_bg.jpg"
    if os.path.exists(local_bg):
        with open(local_bg, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"url('data:image/jpeg;base64,{b64}')"
    return "url('https://images.unsplash.com/photo-1529156069898-49953e39b3ac?auto=format&fit=crop&w=1920&q=80')"


# --- Custom CSS ---
hero_bg_url = get_hero_bg_css()

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@700;800;900&display=swap');

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

# 1. HOME PAGE
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

# 2. ABOUT GACHARA
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
        st.markdown("""
            <div class="dark-card">
                <h4>Core Pillars: Unity, Knowledge & Wealth</h4>
                <p>
                    • <strong>Unity:</strong> Fostering inclusive dialogue across every village and community in Ol Moran Ward.<br><br>
                    • <strong>Knowledge:</strong> Investing in education, digital skills, and youth mentorship.<br><br>
                    • <strong>Wealth:</strong> Strengthening agricultural value chains, infrastructure, and local enterprise.
                </p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 3. OUR VISION
elif active == "Our Vision":
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">PEOPLE • PROGRESS • POSSIBILITY</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Our Vision for Ol Moran Ward</div>', unsafe_allow_html=True)

    v1, v2, v3 = st.columns(3)
    with v1:
        st.markdown("""
            <div class="dark-card">
                <h4>01. Youth & Digital Economy</h4>
                <p>Equipping young people with practical ICT skills, entrepreneurship support, and access to modern digital work opportunities.</p>
            </div>
        """, unsafe_allow_html=True)
    with v2:
        st.markdown("""
            <div class="dark-card">
                <h4>02. Agricultural & Economic Growth</h4>
                <p>Applying financial expertise to support cooperative societies, resilient farming practices, and fair market access for local farmers.</p>
            </div>
        """, unsafe_allow_html=True)
    with v3:
        st.markdown("""
            <div class="dark-card">
                <h4>03. Security, Water & Infrastructure</h4>
                <p>Advocating for reliable water access, rural road connectivity, human-wildlife conflict mitigation, and community safety.</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 4. ACHIEVEMENTS
elif active == "Achievements":
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">TRACK RECORD & IMPACT</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Key Milestones & Initiatives</div>', unsafe_allow_html=True)

    a1, a2 = st.columns(2)
    with a1:
        st.markdown("""
            <div class="dark-card">
                <h4>Technology & Digital Innovation</h4>
                <p>Designed and deployed modern software platforms, financial analytics workflows, and digital branding initiatives empowering businesses and community organizations.</p>
            </div>
        """, unsafe_allow_html=True)
    with a2:
        st.markdown("""
            <div class="dark-card">
                <h4>Education & Youth Mentorship</h4>
                <p>Championed academic mentorship and career guidance programs for students across Naiborom and Ol Moran Ward, bridging secondary and tertiary pathways.</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 5. EVENTS
elif active == "Events":
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">COMMUNITY ENGAGEMENT</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Upcoming Ward Forums & Events</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="dark-card">
            <h4>Ol Moran Ward Listening & Youth Empowerment Tour</h4>
            <p>Join Gachara Ndirangu across Naiborom, Kio, and Wangwachi for open community forums focused on youth employment, agriculture, and ward development priorities. Check the Gallery tab for highlights from recent engagements.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 6. GALLERY
elif active == "Gallery":
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    col_g1, col_g2 = st.columns([4, 1], vertical_alignment="center")
    with col_g1:
        st.markdown('<div class="section-kicker">MOMENTS & COMMUNITY ACTION</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">Photo Gallery</div>', unsafe_allow_html=True)
    with col_g2:
        if st.session_state.authenticated:
            if st.button("+ Upload Photos", use_container_width=True):
                st.session_state.active_page = "Admin"
                st.rerun()

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
                        <div style="background:#1f2226; padding:0.75rem 1rem; border-radius:0 0 6px 6px; border:1px solid #2e3238; border-top:none; margin-bottom:1.5rem;">
                            <div style="color:#ecc953; font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:1px;">{item.get('category', 'Gallery')}</div>
                            <div style="color:#ffffff; font-weight:600; font-size:0.95rem; margin-top:2px;">{item['caption']}</div>
                            <div style="color:#94a3b8; font-size:0.78rem; margin-top:4px;">{item['uploaded_at']}</div>
                        </div>
                    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 7. CONTACT / REGISTER
elif active == "Contact":
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">GET INVOLVED</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Join the Movement</div>', unsafe_allow_html=True)

    with st.form("volunteer_form"):
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number / WhatsApp")
        area = st.text_input("Village / Polling Station in Ol Moran Ward")
        message = st.text_area("How would you like to partner or share your ideas?")
        if st.form_submit_button("Submit"):
            if name and phone:
                st.success(f"Thank you, {name}! Your details have been recorded.")
            else:
                st.warning("Please enter your name and phone number.")
    st.markdown('</div>', unsafe_allow_html=True)

# 8. ADMIN PORTAL
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
