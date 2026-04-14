import streamlit as st

# Custom Styling for the GlobalInternet.py Brand
st.set_page_config(page_title="GlobalInternet.py | Gesner Deslandes", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #0e1117; color: white; }
    .main-title { font-size: 3rem; font-weight: bold; color: #48dbfb; text-align: center; }
    .contact-bar { background: #1e2130; padding: 20px; border-radius: 15px; border-left: 5px solid #48dbfb; }
    </style>
""", unsafe_allow_html=True)

# Main Header
st.markdown('<p class="main-title">🌐 GlobalInternet.py</p>', unsafe_allow_html=True)
st.write("<h3 style='text-align: center;'>Your Python Software Partner: Haiti to the World</h3>", unsafe_allow_html=True)

# Layout: Video on Left, Info on Right
col1, col2 = st.columns([3, 2])

with col1:
    # Converting your GitHub link to the 'raw' format for streaming
    RAW_VIDEO_URL = "https://raw.githubusercontent.com/Deslandes1/DeslandesGesner2026/main/Gesner%20Deslandes%202026.mp4"
    st.video(RAW_VIDEO_URL)

with col2:
    st.markdown("### 🛠️ Our Ready-to-Deploy Solutions")
    st.write("✅ **No Subscriptions** - One-time license.")
    st.write("✅ **Full Source Code** - Total transparency.")
    st.write("✅ **1-Year Support** - Expert setup included.")
    
    st.markdown("---")
    
    st.markdown('<div class="contact-bar">', unsafe_allow_html=True)
    st.write("👤 **Owner:** Gesner Deslandes")
    st.write("📞 **WhatsApp:** (509) 4738-5663")
    st.write("📧 **Email:** deslandes78@gmail.com")
    st.markdown('</div>', unsafe_allow_html=True)

    # WhatsApp Direct Link Button
    wa_link = "https://wa.me/50947385663?text=I'm%20interested%20in%20your%20software%20solutions"
    st.link_button("🚀 Get Started via WhatsApp", wa_link, use_container_width=True)
