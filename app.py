import streamlit as st
import tempfile
import os
import base64
import numpy as np
from gtts import gTTS
from PIL import Image
from moviepy.editor import ImageClip, AudioFileClip, ColorClip, CompositeVideoClip

st.set_page_config(page_title="AI Talking Photo – GlobalInternet.py", layout="centered")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    h1, h2, h3 { color: #48dbfb; }
    .stButton button { background-color: #ff6b35; color: white; border-radius: 30px; }
</style>
""", unsafe_allow_html=True)

st.title("🎭 AI Talking Photo")
st.markdown("Upload a photo, type a message, and the photo will 'speak' (audio + static image). No API keys required.")

with st.sidebar:
    st.image("https://flagcdn.com/w320/ht.png", width=80)
    st.markdown("### GlobalInternet.py")
    st.markdown("**Founder:** Gesner Deslandes")
    st.markdown("📞 WhatsApp: (509) 4738-5663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("---")
    bg_option = st.radio("Background", ["Solid color", "Custom image"])
    if bg_option == "Solid color":
        bg_color = st.color_picker("Pick a color", "#1a1a2e")
    else:
        bg_image_file = st.file_uploader("Upload background image", type=["jpg", "png", "jpeg"])
        bg_image_path = None
        if bg_image_file:
            bg_image_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
            with open(bg_image_path, "wb") as f:
                f.write(bg_image_file.getbuffer())

uploaded_file = st.file_uploader("Choose a photo (face visible)", type=["jpg", "png", "jpeg"])
text_to_say = st.text_area("What should the photo say?", height=100, placeholder="Type your message here...")

if st.button("Generate Talking Video", use_container_width=True):
    if not uploaded_file or not text_to_say.strip():
        st.warning("Please upload a photo and enter text.")
    else:
        with st.spinner("Creating video... (this may take up to a minute)"):
            # 1. Save uploaded image
            img_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
            with open(img_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # 2. Generate speech audio
            audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
            tts = gTTS(text=text_to_say, lang="en", slow=False)
            tts.save(audio_path)
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            
            # 3. Load and resize photo
            img = Image.open(img_path).convert("RGB")
            target_w = 720
            ratio = target_w / img.width
            new_size = (target_w, int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            img_array = np.array(img)
            
            # 4. Create background
            if bg_option == "Solid color":
                bg_rgb = tuple(int(bg_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
                bg_clip = ColorClip(size=(target_w, img_array.shape[0]), color=bg_rgb, duration=duration)
            else:
                if bg_image_path and os.path.exists(bg_image_path):
                    bg_img = Image.open(bg_image_path).convert("RGB")
                    bg_img = bg_img.resize((target_w, img_array.shape[0]), Image.Resampling.LANCZOS)
                    bg_clip = ImageClip(np.array(bg_img), duration=duration)
                else:
                    bg_clip = ColorClip(size=(target_w, img_array.shape[0]), color=(0,0,0), duration=duration)
            
            # 5. Create photo clip (centered)
            photo_clip = ImageClip(img_array, duration=duration).set_position("center")
            
            # 6. Composite video
            video = CompositeVideoClip([bg_clip, photo_clip], size=(target_w, img_array.shape[0]))
            video = video.set_audio(audio)
            
            # 7. Write video file
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
            video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", verbose=False, logger=None)
            
            # 8. Provide download link
            with open(output_path, "rb") as f:
                video_bytes = f.read()
                b64 = base64.b64encode(video_bytes).decode()
                st.success("Video generated successfully!")
                st.markdown(f'<a href="data:video/mp4;base64,{b64}" download="talking_photo.mp4"><button style="background-color:#28a745; color:white; padding:10px 20px; border:none; border-radius:30px; cursor:pointer;">⬇️ Download Video</button></a>', unsafe_allow_html=True)
            
            # Cleanup
            for p in [img_path, audio_path, output_path]:
                if os.path.exists(p):
                    os.unlink(p)
            if bg_image_path and os.path.exists(bg_image_path):
                os.unlink(bg_image_path)

st.markdown("---")
st.caption("Note: This version uses a static photo with audio. For realistic lip-sync, you would need an AI service like D-ID or HeyGen (requires API key).")
