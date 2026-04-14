import streamlit as st
import requests
import time

# --- GET YOUR KEY AT d-id.com ---
API_KEY = st.secrets["DID_API_KEY"] # Recommended: Use Streamlit Secrets
API_URL = "https://api.d-id.com"

def generate_avatar_video(image_url, script):
    # 1. Create the 'Talk'
    payload = {
        "script": {"type": "text", "input": script, "provider": {"type": "microsoft", "voice_id": "en-US-ChristopherNeural"}},
        "source_url": image_url
    }
    headers = {"Authorization": f"Basic {API_KEY}", "Content-Type": "application/json"}
    
    response = requests.post(f"{API_URL}/talks", json=payload, headers=headers)
    talk_id = response.json().get("id")

    # 2. Polling for completion
    while True:
        status_res = requests.get(f"{API_URL}/talks/{talk_id}", headers=headers)
        status = status_res.json().get("status")
        if status == "done":
            return status_res.json().get("result_url")
        elif status == "error":
            return None
        time.sleep(2)

# ... inside your button logic ...
if st.button("🚀 Generate"):
    # Note: image_url must be a public link for D-ID to access it
    video_url = generate_avatar_video(my_public_image_url, script_text)
    if video_url:
        st.video(video_url)
