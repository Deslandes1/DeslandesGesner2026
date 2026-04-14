import streamlit as st

# Set layout to wide
st.set_page_config(page_title="GLOBALINTERNET.PY", layout="wide")

st.markdown("""
    <style>
    /* Prevent scrolling and ensure full-screen fit */
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden;
        height: 100vh;
    }
    
    /* Main container scaling */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 98% !important;
        transform: scale(0.92);
        transform-origin: top center;
    }

    /* Header styling */
    .main-title { 
        font-size: 2.2rem !important; 
        font-weight: bold; 
        color: #48dbfb; 
        text-align: center; 
        margin-bottom: 0px; 
        text-transform: uppercase;
    }
    
    .sub-title {
        font-size: 1rem !important;
        text-align: center;
        margin-bottom: 1rem;
        color: #cccccc;
    }

    /* ZOOMED VIDEO */
    video {
        max-height: 70vh !important;
        width: 100% !important;
        border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(72, 219, 251, 0.3);
    }

    /* Text formatting */
    .small-text {
        font-size: 0.85rem !important;
        line-height: 1.3;
    }

    .section-box {
        background: #1e2130; 
        padding: 10px; 
        border-radius: 10px;
        border-left: 4px solid #48dbfb; 
    }

    /* Shining link effect */
    .shining-link {
        color: #48dbfb !important;
        font-weight: bold;
        text-decoration: none;
        text-shadow: 0 0 5px rgba(72, 219, 251, 0.5);
    }

    /* Clean UI: Hide menus */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Main Header
st.markdown('<p class="main-title">🌐 GLOBALINTERNET.PY</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Python Software Partner: Haiti to the World</p>', unsafe_allow_html=True)

# Column Layout
col1, col2 = st.columns([1.8, 1], gap="medium")

with col1:
    # VIDEO SECTION
    VIDEO_URL = "https://raw.githubusercontent.com/Deslandes1/DeslandesGesner2026/main/Gesner%20Deslandes%202026.mp4"
    st.video(VIDEO_URL)
    
    st.markdown('**🔐 Live Demos Password:** `20082010`')
    st.info("💡 Our Language Suites now feature high-fidelity native neural voices!")

with col2:
    st.markdown("### 🏆 Software Demos")
    
    # Updated links section
    st.markdown("""
    <div class="small-text">
    🚀 <b>Drone Commander:</b> $2,000<br>
    🗳️ <b>Online Voting:</b> $2,000<br>
    🏫 <b>School Management:</b> $1,500<br>
    🛡️ <b>Security Radar:</b> $299<br><br>
    🌐 <b>Language Suites ($299 ea):</b><br>
    🇺🇸 <a href="https://let-s-learn-english-with-gesner-fasbf2hvwsfpkzz9s9oc4f.streamlit.app/" style="color:#48dbfb">Learn English Demo</a><br>
    🇪🇸 <a href="https://let-s-learn-spanish-with-gesner-twe8na7wraihczvq2lhfkl.streamlit.app/" style="color:#48dbfb">Learn Spanish Demo</a><br>
    🇵🇹 <a href="https://let-s-learn-portuguese-with-gesner-hqz5b8w8ebgvcrhbtuuxe5.streamlit.app/" style="color:#48dbfb">Learn Portuguese Demo</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 💎 Why Us?")
    st.markdown("""
    <div class="small-text">
    ✅ Full Source Code Included<br>
    ✅ Zero Subscriptions<br>
    ✅ 1-Year Free Support
    </div>
    """, unsafe_allow_html=True)

    # Contact Card with Website Link
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.write("👤 **Gesner Deslandes**")
    st.write("📞 **WA:** (509) 4738-5663")
    st.write("📧 deslandes78@gmail.com")
    st.markdown('🌐 <a class="shining-link" href="https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/" target="_blank">GlobalInternet.py Official Site</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    wa_link = "https://wa.me/50947385663?text=Interested%20in%20your%20software%20solutions"
    st.link_button("🚀 Start WhatsApp", wa_link, use_container_width=True)
