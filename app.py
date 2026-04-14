import streamlit as st

# --- CONFIGURATION ---
st.set_page_config(page_title="GlobalInternet.py | AI Avatar", layout="wide")

# --- VIDEO ASSET ---
# We convert your GitHub link to the raw URL so Streamlit can stream it
GITHUB_VIDEO_URL = "https://raw.githubusercontent.com/Deslandes1/DeslandesGesner2026/main/Gesner%20Deslandes%202026.mp4"

st.title("🐍 GlobalInternet.py AI Avatar")
st.write("Professional Python & AI Solutions by Gesner Deslandes")

# --- UI LAYOUT ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎥 AI Talking Avatar Promo")
    # Streamlit video player pulling directly from your GitHub repo
    st.video(GITHUB_VIDEO_URL)

with col2:
    st.markdown("### 📋 Quick Info")
    st.info("**Owner:** Gesner Deslandes")
    st.success("**Location:** Haiti / Global Online")
    st.write("📞 WhatsApp: (509) 4738-5663")
    st.write("📧 Email: deslandes78@gmail.com")

st.markdown("---")
st.markdown("### 🚀 Get Started Today")
st.write("Ready for the best professional software on the market? Connect with the leading Python builders.")
