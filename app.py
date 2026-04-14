import streamlit as st

# Custom Scaling & Layout Fix
st.set_page_config(page_title="GLOBALINTERNET.PY | Gesner Deslandes", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #0e1117; color: white; }
    .block-container { padding-top: 1rem !important; }
    .main-title { 
        font-size: 2.5rem; font-weight: bold; color: #48dbfb; 
        text-align: center; margin-bottom: 0px; text-transform: uppercase;
    }
    .sub-title {
        font-size: 1.2rem; text-align: center; margin-bottom: 1rem; color: #cccccc;
    }
    .section-box {
        background: #1e2130; padding: 15px; border-radius: 10px;
        border-left: 5px solid #48dbfb; margin-bottom: 10px;
    }
    .price-tag { color: #48dbfb; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Main Header
st.markdown('<p class="main-title">🌐 GLOBALINTERNET.PY</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Your Python Software Partner: Haiti to the World</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    st.markdown("### 📽️ Professional Presentation")
    # Replace the URL below with your newly generated video link
    VIDEO_URL = "https://raw.githubusercontent.com/Deslandes1/DeslandesGesner2026/main/Gesner%20Deslandes%202026.mp4"
    st.video(VIDEO_URL)
    
    st.markdown("---")
    st.info("🔐 **Try Before You Buy:** Use password **20082010** to explore our Live Demos.")

with col2:
    st.markdown("### 🛠️ Tech Stack & Services")
    with st.expander("View Full Services", expanded=True):
        st.write("🔹 **Custom Python Development** – Tailor-made business logic.")
        st.write("🔹 **AI & Machine Learning** – Intelligent bots & predictive models.")
        st.write("🔹 **Enterprise Systems** – School, POS, & Accounting software.")
        st.write("🔹 **Specialized Engineering** – Archives & Election systems.")

    st.markdown("### 🏆 Ready-to-Deploy Solutions")
    st.markdown("""
    | Project | Investment |
    | :--- | :--- |
    | **Haitian Drone Commander** | <span class="price-tag">$2,000</span> |
    | **Haiti Online Voting Software** | <span class="price-tag">$2,000</span> |
    | **School Management System** | <span class="price-tag">$1,500</span> |
    | **DSM-2026 Advanced Security** | <span class="price-tag">$299</span> |
    """, unsafe_allow_html=True)

    # Contact Card
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown("**👤 Owner:** Gesner Deslandes")
    st.markdown("**📞 WA:** (509) 4738-5663")
    st.markdown("**📧 Email:** deslandes78@gmail.com")
    st.markdown('</div>', unsafe_allow_html=True)

    wa_link = "https://wa.me/50947385663?text=I'm%20interested%20in%20your%20software%20solutions"
    st.link_button("🚀 Get Started via WhatsApp", wa_link, use_container_width=True)
