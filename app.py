import streamlit as st

# Set layout to wide
st.set_page_config(page_title="GLOBALINTERNET.PY", layout="wide")

st.markdown("""
    <style>
    /* Prevent any scrolling on the main page */
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden;
        height: 100vh;
    }
    
    /* Global scaling: reduce everything to 90% */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        max-width: 95% !important;
        transform: scale(0.9);
        transform-origin: top center;
    }

    /* Shrink the header */
    .main-title { 
        font-size: 1.8rem !important; 
        font-weight: bold; 
        color: #48dbfb; 
        text-align: center; 
        margin-bottom: 0px; 
        text-transform: uppercase;
    }
    
    .sub-title {
        font-size: 0.9rem !important;
        text-align: center;
        margin-bottom: 0.5rem;
        color: #cccccc;
    }

    /* Limit video size so it doesn't push content down */
    video {
        max-height: 50vh !important;
        width: auto !important;
        margin: 0 auto;
        display: block;
    }

    /* Smaller text for the lists */
    .small-text {
        font-size: 0.85rem !important;
        line-height: 1.2;
    }

    .section-box {
        background: #1e2130; 
        padding: 8px; 
        border-radius: 8px;
        border-left: 3px solid #48dbfb; 
        font-size: 0.8rem;
    }

    /* Hide Streamlit elements that take up space */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Main Header
st.markdown('<p class="main-title">🌐 GLOBALINTERNET.PY</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Python Software Partner: Haiti to the World</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1.3, 1], gap="small")

with col1:
    # Video Section
    VIDEO_URL = "https://raw.githubusercontent.com/Deslandes1/DeslandesGesner2026/main/Gesner%20Deslandes%202026.mp4"
    st.video(VIDEO_URL)
    
    st.markdown('<p class="small-text">🔐 <b>Live Demos:</b> Use password <b>20082010</b></p>', unsafe_allow_html=True)

with col2:
    st.markdown("<h5 style='margin-bottom:0px;'>🏆 Software & Pricing</h5>", unsafe_allow_html=True)
    st.markdown("""
    <div class="small-text">
    🚀 <b>Drone Commander:</b> $2,000<br>
    🗳️ <b>Online Voting:</b> $2,000<br>
    🏫 <b>School Management:</b> $1,500<br>
    🛡️ <b>Security Radar:</b> $299<br>
    🇵🇹 <b>Portuguese Course:</b> $299
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h5 style='margin-bottom:0px;'>💎 Why Us?</h5>", unsafe_allow_html=True)
    st.markdown("""
    <div class="small-text">
    ✅ Full Source Code Included<br>
    ✅ Zero Subscriptions<br>
    ✅ 1-Year Free Support
    </div>
    """, unsafe_allow_html=True)

    # Contact Card
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.write("👤 **Gesner Deslandes**")
    st.write("📞 **WA:** (509) 4738-5663")
    st.write("📧 deslandes78@gmail.com")
    st.markdown('</div>', unsafe_allow_html=True)

    wa_link = "https://wa.me/50947385663?text=Interested%20in%20software"
    st.link_button("🚀 Start WhatsApp", wa_link, use_container_width=True)
