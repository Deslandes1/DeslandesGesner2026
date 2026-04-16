import streamlit as st
import tempfile
import os
import base64
import numpy as np
from gtts import gTTS
from PIL import Image, ImageDraw
from moviepy.editor import VideoClip, AudioFileClip, CompositeVideoClip, ImageClip, ColorClip, concatenate_videoclips

st.set_page_config(page_title="AI Talking Photo – GlobalInternet.py", layout="centered")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    h1, h2, h3 { color: #48dbfb; }
    .stButton button { background-color: #ff6b35; color: white; border-radius: 30px; }
    .stAlert { background-color: #1e2130; color: white; }
</style>
""", unsafe_allow_html=True)

st.title("🎭 AI Talking Photo")
st.markdown("Upload a photo, type your message, and watch it speak – no API keys required.")

# Sidebar for background options
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

# Main interface
uploaded_file = st.file_uploader("Choose a photo (face visible)", type=["jpg", "png", "jpeg"])
text_to_say = st.text_area("What should the photo say?", height=100, placeholder="Type your message here...")
mouth_animation = st.checkbox("Enable mouth animation (simple open/close)", value=True)

if st.button("Generate Talking Video", use_container_width=True):
    if not uploaded_file or not text_to_say.strip():
        st.warning("Please upload a photo and enter text.")
    else:
        with st.spinner("Creating talking video... (this may take a minute)"):
            # 1. Save uploaded image
            img_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
            with open(img_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # 2. Generate speech audio (gTTS – free)
            audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
            tts = gTTS(text=text_to_say, lang="en", slow=False)
            tts.save(audio_path)
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            
            # 3. Load and resize image
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
            
            # 5. Create base image clip
            base_clip = ImageClip(img_array, duration=duration).set_position("center")
            
            # 6. Mouth animation (if enabled)
            if mouth_animation:
                def make_mouth_frame(t):
                    # Create transparent overlay
                    frame = np.zeros((img_array.shape[0], img_array.shape[1], 4), dtype=np.uint8)
                    # Mouth region (fixed position – lower center)
                    face_bottom = int(img_array.shape[0] * 0.65)
                    mouth_y = face_bottom + 30
                    mouth_width = int(img_array.shape[1] * 0.3)
                    mouth_height = int(mouth_width * 0.4)
                    # Simulate open/close with sine wave (5 Hz)
                    amplitude = int(mouth_height * (0.5 + 0.5 * np.sin(2 * np.pi * 5 * t)))
                    mouth_h = max(5, mouth_height + amplitude)
                    # Draw ellipse
                    overlay = Image.new("RGBA", (img_array.shape[1], img_array.shape[0]), (0,0,0,0))
                    draw = ImageDraw.Draw(overlay)
                    left = (img_array.shape[1] - mouth_width) // 2
                    top = mouth_y - mouth_h // 2
                    right = left + mouth_width
                    bottom = top + mouth_h
                    draw.ellipse([left, top, right, bottom], fill=(255, 100, 100, 180))
                    return np.array(overlay)
                
                mouth_clip = VideoClip(make_mouth_frame, duration=duration).set_position("center")
                video = CompositeVideoClip([bg_clip, base_clip, mouth_clip], size=(target_w, img_array.shape[0]))
            else:
                video = CompositeVideoClip([bg_clip, base_clip], size=(target_w, img_array.shape[0]))
            
            # 7. Add audio
            video = video.set_audio(audio)
            
            # 8. Write video file
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
            video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", verbose=False, logger=None)
            
            # 9. Provide download link
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
st.caption("Note: This tool uses a simple mouth animation overlay (not AI lip-sync). For realistic talking head videos, consider using D-ID, HeyGen, or Wav2Lip with a GPU.")
