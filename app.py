import streamlit as st
import tempfile
import os
import base64
import numpy as np
import asyncio
from PIL import Image, ImageDraw
from moviepy.editor import ImageClip, AudioFileClip, ColorClip, CompositeVideoClip, VideoClip
import edge_tts

st.set_page_config(page_title="AI Talking Photo – GlobalInternet.py", layout="centered")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    h1, h2, h3 { color: #48dbfb; }
    .stButton button { background-color: #ff6b35; color: white; border-radius: 30px; }
</style>
""", unsafe_allow_html=True)

st.title("🎭 AI Talking Photo")
st.markdown("Upload a photo, type a message, and the photo will speak with moving lips and a male voice.")

# Initialize variables
bg_image_path = None

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
        if bg_image_file:
            bg_image_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
            with open(bg_image_path, "wb") as f:
                f.write(bg_image_file.getbuffer())

uploaded_file = st.file_uploader("Choose a photo (face visible)", type=["jpg", "png", "jpeg"])
text_to_say = st.text_area("What should the photo say?", height=100, placeholder="Type your message here...")
lip_intensity = st.slider("Lip movement intensity", 0.0, 1.0, 0.7, 0.05, help="Higher = more mouth opening")

if "video_path" not in st.session_state:
    st.session_state.video_path = None

async def generate_audio(text, output_path):
    communicate = edge_tts.Communicate(text, "en-US-GuyNeural")
    await communicate.save(output_path)

if st.button("Generate Talking Video", use_container_width=True):
    if not uploaded_file or not text_to_say.strip():
        st.warning("Please upload a photo and enter text.")
    else:
        with st.spinner("Creating talking video... (may take up to a minute)"):
            # 1. Save uploaded image
            img_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
            with open(img_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # 2. Generate male voice audio
            audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
            asyncio.run(generate_audio(text_to_say, audio_path))
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            fps = 30
            
            # 3. Load and resize photo
            img = Image.open(img_path).convert("RGBA")
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
            
            # 5. Time‑based mouth movement (sine wave, no audio analysis – stable and error‑free)
            mouth_y = int(img_array.shape[0] * 0.65)
            mouth_width = int(img_array.shape[1] * 0.3)
            max_mouth_height = int(mouth_width * 0.4)
            min_mouth_height = 3
            
            def make_frame(t):
                # Sine wave with frequency 5 Hz (natural talking rhythm)
                amplitude_factor = 0.5 + 0.5 * np.sin(2 * np.pi * 5 * t)
                mouth_h = int(min_mouth_height + (max_mouth_height - min_mouth_height) * amplitude_factor * lip_intensity)
                overlay = Image.new("RGBA", (img_array.shape[1], img_array.shape[0]), (0,0,0,0))
                draw = ImageDraw.Draw(overlay)
                left = (img_array.shape[1] - mouth_width) // 2
                top = mouth_y - mouth_h // 2
                right = left + mouth_width
                bottom = top + mouth_h
                draw.ellipse([left, top, right, bottom], fill=(255, 100, 100, 180))
                return np.array(overlay)
            
            mouth_clip = VideoClip(make_frame, duration=duration).set_position("center")
            
            # 6. Composite photo + mouth
            photo_clip = ImageClip(img_array, duration=duration).set_position("center")
            video = CompositeVideoClip([bg_clip, photo_clip, mouth_clip], size=(target_w, img_array.shape[0]))
            video = video.set_audio(audio)
            
            # 7. Write video
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
            video.write_videofile(output_path, fps=fps, codec="libx264", audio_codec="aac", verbose=False, logger=None)
            
            st.session_state.video_path = output_path
            
            # Cleanup
            for p in [img_path, audio_path]:
                if os.path.exists(p):
                    os.unlink(p)
            if bg_image_path and os.path.exists(bg_image_path):
                os.unlink(bg_image_path)
            
            st.success("Video ready! Preview below.")

if st.session_state.video_path and os.path.exists(st.session_state.video_path):
    st.markdown("### 🎬 Preview")
    st.video(st.session_state.video_path)
    with open(st.session_state.video_path, "rb") as f:
        video_bytes = f.read()
        b64 = base64.b64encode(video_bytes).decode()
        st.markdown(f'<a href="data:video/mp4;base64,{b64}" download="talking_photo_lipsync.mp4"><button style="background-color:#28a745; color:white; padding:10px 20px; border:none; border-radius:30px; cursor:pointer;">⬇️ Download Video</button></a>', unsafe_allow_html=True)

st.markdown("---")
st.caption("Uses edge-tts male voice (en-US-GuyNeural) and time‑based lip movement (sine wave). This avoids audio analysis errors and works reliably on Streamlit Cloud.")
