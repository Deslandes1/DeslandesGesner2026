import streamlit as st

# Custom Scaling & Layout Fix
st.set_page_config(page_title="GlobalInternet.py | Gesner Deslandes", layout="wide")

st.markdown("""
    <style>
    /* Force the app to fit on one screen without scrolling */
    .stApp { 
        background: #0e1117; 
        color: white; 
        max-height: 100vh; 
        overflow: hidden; 
    }
    
    /* Reduce vertical padding in the main container */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }

    /* Scale down titles for video capture */
    .main-title { 
        font-size: 2.2rem; 
        font-weight: bold; 
        color: #48dbfb; 
        text-align: center; 
        margin-bottom: 0px;
    }
    
    .sub-title {
        font-size: 1.1rem !important;
        text-align: center;
        margin-bottom: 1rem;
        color: #cccccc;
    }

    /* Compact contact bar */
    .contact-bar { 
        background: #1e2130; 
        padding: 12px; 
        border-radius: 10px; 
        border-left: 4px solid #48dbfb; 
        font-size: 0.9rem;
    }

    /* Adjust video height to prevent overflow */
    video {
        max-height: 60vh;
        border-radius: 12px;
    }

    /* Slim down the sidebar if used */
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Main Header
st.markdown('<p class="main-title">🌐 GlobalInternet.py</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Your Python Software Partner: Haiti to the World</p>', unsafe_allow_html=True)

# Layout: Video on Left, Info on Right
col1, col2 = st.columns([3, 2], gap="medium")

with col1:
    # Converting GitHub link to 'raw' format
    RAW_VIDEO_URL = "https://raw.githubusercontent.com/Deslandes1/DeslandesGesner2026/main/Gesner%20Deslandes%202026.mp4"
    st.video(RAW_VIDEO_URL)

with col2:
    st.markdown("### 🛠️ Solutions")
    st.write("✅ **No Subscriptions**")
    st.write("✅ **Full Source Code**")
    st.write("✅ **1-Year Support**")
    
    st.markdown("---")
    
    st.markdown('<div class="contact-bar">', unsafe_allow_html=True)
    st.write("👤 **Owner:** Gesner Deslandes")
    st.write("📞 **WA:** (509) 4738-5663")
    st.write("📧 **Email:** deslandes78@gmail.com")
    st.markdown('</div>', unsafe_allow_html=True)

    # Compact Button
    wa_link = "https://wa.me/50947385663?text=I'm%20interested%20in%20your%20software%20solutions"
    st.link_button("🚀 Start via WhatsApp", wa_link, use_container_width=True)
