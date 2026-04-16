import streamlit as st
import tempfile
import os
import base64
import asyncio
import numpy as np
import requests
from PIL import Image
from moviepy.editor import *
import edge_tts

st.set_page_config(page_title="AI Media Studio – GlobalInternet.py", layout="centered")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .stApp label, .stApp .stMarkdown, .stApp .stText, .stApp .stCaption, .stApp .stInfo,
    .stApp .stSuccess, .stApp .stWarning, .stApp .stError, .stApp .stRadio label,
    .stApp .stSlider label, .stApp .stFileUploader label,
    .stApp .stTextArea label, .stApp .stButton button, .stApp .stAlert, .stApp .stException,
    .stApp .stCodeBlock, .stApp .stDataFrame, .stApp .stTable, .stApp .stTabs [role="tab"],
    .stApp .stTabs [role="tablist"] button, .stApp .stExpander, .stApp .stProgress > div,
    .stApp .stMetric label, .stApp .stMetric value, div, p, span, pre, code,
    .element-container, .stText p, .stText div, .stText span, .stText code {
        color: white !important;
    }
    .stSelectbox label {
        color: black !important;
    }
    .stRadio [role="radiogroup"] label {
        background: rgba(255,255,255,0.15);
        border-radius: 10px;
        padding: 0.3rem;
        margin: 0.2rem 0;
        color: white !important;
    }
    .stSelectbox div[data-baseweb="select"] {
        background-color: #2d1b4e;
        border: 1px solid #ffcc00;
        border-radius: 10px;
    }
    .stSelectbox div[data-baseweb="select"] div {
        color: white !important;
    }
    .stSelectbox svg {
        fill: white;
    }
    div[data-baseweb="popover"] ul {
        background-color: #f0f2f6 !important;
        border: 1px solid #cccccc;
    }
    div[data-baseweb="popover"] li {
        color: black !important;
        background-color: #f0f2f6 !important;
    }
    div[data-baseweb="popover"] li:hover {
        background-color: #d0d4dc !important;
    }
    .stSlider label, .stSlider div[data-baseweb="slider"] span {
        color: white !important;
    }
    .stFileUploader {
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 0.5rem;
        border: 1px dashed #48dbfb;
    }
    .stButton button {
        background-color: #ff6b35;
        color: white !important;
        border-radius: 30px;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #feca57;
        color: black !important;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #1a0b2e, #2d1b4e);
    }
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stText,
    section[data-testid="stSidebar"] label {
        color: white !important;
    }
    .stExpander {
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
    }
    .footer-caption {
        text-align: center;
        color: #cccccc !important;
        font-size: 0.8rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

LANGUAGES = {
    "English": {
        "ui": {
            "title": "🎭 AI Media Studio",
            "subtitle": "Create videos from photos, audio, or video – add speech or music.",
            "mode_label": "Mode",
            "mode_photo_speech": "📷 Photo + Speech (type text)",
            "mode_photo_audio": "📷 Photo + Uploaded Audio",
            "mode_photo_music": "📷 Photo + Background Music Only",
            "mode_video_music": "🎥 Video + Background Music",
            "photo_upload": "Choose a photo (face visible)",
            "audio_upload": "Upload your own audio (MP3/WAV)",
            "video_upload": "Upload a video (MP4)",
            "text_label": "What should the photo say?",
            "generate_btn": "Generate Video",
            "spinner": "Creating video...",
            "success": "Video created! Preview below.",
            "preview": "🎬 Preview",
            "download_btn": "⬇️ Download Video",
            "bg_label": "Background (for photo modes)",
            "bg_solid": "Solid color",
            "bg_custom": "Custom image",
            "color_picker": "Pick a color",
            "upload_bg": "Upload background image",
            "music_label": "Background music (optional)",
            "no_music": "None",
            "music_volume": "Music volume",
            "upload_music": "Or upload your own music",
            "caption": "Supports: Photo + Speech, Photo + Uploaded Audio, Photo + Music Only, Video + Background Music."
        },
        "voice": "en-US-GuyNeural"
    }
}

MUSIC_TRACKS = {
    "None": "",
    "Corporate 1": "https://cdn.pixabay.com/download/audio/2022/02/02/audio_bb7f0c6d9b.mp3",
    "Corporate 2": "https://cdn.pixabay.com/download/audio/2022/01/18/audio_d0f5e8c1e2.mp3",
    "Upbeat 1": "https://cdn.pixabay.com/download/audio/2022/05/16/audio_2b3c5d6e2f.mp3",
    "Upbeat 2": "https://cdn.pixabay.com/download/audio/2022/05/16/audio_3c4d5e6f7a.mp3",
    "Inspirational 1": "https://cdn.pixabay.com/download/audio/2022/03/10/audio_8a7b6c5d4e.mp3",
    "Inspirational 2": "https://cdn.pixabay.com/download/audio/2022/03/15/audio_9a8b7c6d5e.mp3",
    "Ambient 1": "https://cdn.pixabay.com/download/audio/2022/04/01/audio_1a2b3c4d5e.mp3",
    "Ambient 2": "https://cdn.pixabay.com/download/audio/2022/04/05/audio_2b3c4d5e6f.mp3",
    "Technology 1": "https://cdn.pixabay.com/download/audio/2022/06/10/audio_3c4d5e6f7a.mp3",
    "Technology 2": "https://cdn.pixabay.com/download/audio/2022/06/15/audio_4d5e6f7a8b.mp3",
    "Happy 1": "https://cdn.pixabay.com/download/audio/2022/07/20/audio_5e6f7a8b9c.mp3",
    "Happy 2": "https://cdn.pixabay.com/download/audio/2022/07/25/audio_6f7a8b9c0d.mp3",
    "Calm 1": "https://cdn.pixabay.com/download/audio/2022/08/30/audio_7a8b9c0d1e.mp3",
    "Calm 2": "https://cdn.pixabay.com/download/audio/2022/09/05/audio_8b9c0d1e2f.mp3",
    "Energetic 1": "https://cdn.pixabay.com/download/audio/2022/10/12/audio_9c0d1e2f3a.mp3",
    "Energetic 2": "https://cdn.pixabay.com/download/audio/2022/11/18/audio_0d1e2f3a4b.mp3",
    "Cinematic 1": "https://cdn.pixabay.com/download/audio/2022/12/22/audio_1e2f3a4b5c.mp3",
    "Cinematic 2": "https://cdn.pixabay.com/download/audio/2023/01/10/audio_2f3a4b5c6d.mp3",
    "Funky 1": "https://cdn.pixabay.com/download/audio/2023/02/14/audio_3a4b5c6d7e.mp3",
    "Funky 2": "https://cdn.pixabay.com/download/audio/2023/03/18/audio_4b5c6d7e8f.mp3",
    "Jazz 1": "https://cdn.pixabay.com/download/audio/2023/04/22/audio_5c6d7e8f9a.mp3",
    "Jazz 2": "https://cdn.pixabay.com/download/audio/2023/05/26/audio_6d7e8f9a0b.mp3",
    "Rock 1": "https://cdn.pixabay.com/download/audio/2023/06/30/audio_7e8f9a0b1c.mp3",
    "Rock 2": "https://cdn.pixabay.com/download/audio/2023/07/04/audio_8f9a0b1c2d.mp3",
    "Electronic 1": "https://cdn.pixabay.com/download/audio/2023/08/08/audio_9a0b1c2d3e.mp3",
    "Electronic 2": "https://cdn.pixabay.com/download/audio/2023/09/12/audio_0b1c2d3e4f.mp3",
    "Orchestral 1": "https://cdn.pixabay.com/download/audio/2023/10/16/audio_1c2d3e4f5a.mp3",
    "Orchestral 2": "https://cdn.pixabay.com/download/audio/2023/11/20/audio_2d3e4f5a6b.mp3",
    "Piano 1": "https://cdn.pixabay.com/download/audio/2023/12/24/audio_3e4f5a6b7c.mp3",
    "Piano 2": "https://cdn.pixabay.com/download/audio/2024/01/28/audio_4f5a6b7c8d.mp3",
    "Guitar 1": "https://cdn.pixabay.com/download/audio/2024/02/02/audio_5a6b7c8d9e.mp3",
    "Guitar 2": "https://cdn.pixabay.com/download/audio/2024/03/06/audio_6b7c8d9e0f.mp3",
    "Chill 1": "https://cdn.pixabay.com/download/audio/2024/04/10/audio_7c8d9e0f1a.mp3",
    "Chill 2": "https://cdn.pixabay.com/download/audio/2024/05/14/audio_8d9e0f1a2b.mp3",
    "Dreamy 1": "https://cdn.pixabay.com/download/audio/2024/06/18/audio_9e0f1a2b3c.mp3",
    "Dreamy 2": "https://cdn.pixabay.com/download/audio/2024/07/22/audio_0f1a2b3c4d.mp3",
    "Summer 1": "https://cdn.pixabay.com/download/audio/2024/08/26/audio_1a2b3c4d5e.mp3",
    "Summer 2": "https://cdn.pixabay.com/download/audio/2024/09/30/audio_2b3c4d5e6f.mp3",
    "Winter 1": "https://cdn.pixabay.com/download/audio/2024/10/04/audio_3c4d5e6f7a.mp3",
    "Winter 2": "https://cdn.pixabay.com/download/audio/2024/11/08/audio_4d5e6f7a8b.mp3",
    "Nature 1": "https://cdn.pixabay.com/download/audio/2024/12/12/audio_5e6f7a8b9c.mp3",
    "Nature 2": "https://cdn.pixabay.com/download/audio/2025/01/16/audio_6f7a8b9c0d.mp3",
    "Space 1": "https://cdn.pixabay.com/download/audio/2025/02/20/audio_7a8b9c0d1e.mp3",
    "Space 2": "https://cdn.pixabay.com/download/audio/2025/03/24/audio_8b9c0d1e2f.mp3",
    "Retro 1": "https://cdn.pixabay.com/download/audio/2025/04/01/audio_9c0d1e2f3a.mp3",
    "Retro 2": "https://cdn.pixabay.com/download/audio/2025/04/05/audio_0d1e2f3a4b.mp3",
    "Vlog 1": "https://cdn.pixabay.com/download/audio/2025/04/09/audio_1e2f3a4b5c.mp3",
    "Vlog 2": "https://cdn.pixabay.com/download/audio/2025/04/13/audio_2f3a4b5c6d.mp3",
}

if "lang" not in st.session_state:
    st.session_state.lang = "English"

with st.sidebar:
    st.image("https://flagcdn.com/w320/ht.png", width=80)
    st.markdown("### GlobalInternet.py")
    st.markdown("**Founder:** Gesner Deslandes")
    st.markdown("📞 WhatsApp: (509) 4738-5663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("---")
    st.selectbox("🌐 Language", options=list(LANGUAGES.keys()), key="lang")
    st.markdown("---")

ui = LANGUAGES[st.session_state.lang]["ui"]
tts_voice = LANGUAGES[st.session_state.lang]["voice"]

st.title(ui["title"])
st.markdown(ui["subtitle"])

mode = st.radio(ui["mode_label"], [
    ui["mode_photo_speech"],
    ui["mode_photo_audio"],
    ui["mode_photo_music"],
    ui["mode_video_music"]
])

bg_image_path = None

if mode != ui["mode_video_music"]:
    with st.sidebar:
        bg_option = st.radio(ui["bg_label"], [ui["bg_solid"], ui["bg_custom"]])
        if bg_option == ui["bg_solid"]:
            bg_color = st.color_picker(ui["color_picker"], "#1a1a2e")
        else:
            bg_image_file = st.file_uploader(ui["upload_bg"], type=["jpg", "png", "jpeg"])
            if bg_image_file:
                bg_image_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
                with open(bg_image_path, "wb") as f:
                    f.write(bg_image_file.getbuffer())

selected_music = "None"
music_volume = 0.5
uploaded_music = None

# Always show music selector (optional background for all modes)
music_options = list(MUSIC_TRACKS.keys())
selected_music = st.selectbox(ui["music_label"], music_options, index=0)
if selected_music != "None":
    music_volume = st.slider(ui["music_volume"], 0.0, 1.0, 0.5, 0.05)
uploaded_music = st.file_uploader(ui["upload_music"], type=["mp3", "wav"])

photo_file = None
text_to_say = ""
audio_file = None
video_file = None

if mode == ui["mode_photo_speech"]:
    photo_file = st.file_uploader(ui["photo_upload"], type=["jpg", "png", "jpeg"])
    text_to_say = st.text_area(ui["text_label"], height=100, placeholder="Type your message here...")
elif mode == ui["mode_photo_audio"]:
    photo_file = st.file_uploader(ui["photo_upload"], type=["jpg", "png", "jpeg"])
    audio_file = st.file_uploader(ui["audio_upload"], type=["mp3", "wav"])
elif mode == ui["mode_photo_music"]:
    photo_file = st.file_uploader(ui["photo_upload"], type=["jpg", "png", "jpeg"])
else:
    video_file = st.file_uploader(ui["video_upload"], type=["mp4"])

if "video_path" not in st.session_state:
    st.session_state.video_path = None

async def generate_speech(text, output_path, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def load_audio_file(file_path):
    """Attempt to load an audio file and return an AudioFileClip, or None if invalid."""
    try:
        clip = AudioFileClip(file_path)
        # Check if duration is valid (not zero)
        if clip.duration <= 0:
            raise ValueError("Audio duration is zero or invalid")
        return clip
    except Exception as e:
        st.error(f"Audio file is invalid or corrupted: {e}")
        return None

if st.button(ui["generate_btn"], use_container_width=True):
    # Validation
    if mode == ui["mode_photo_speech"] and (not photo_file or not text_to_say.strip()):
        st.warning("Please upload a photo and enter text.")
        st.stop()
    elif mode == ui["mode_photo_audio"] and (not photo_file or not audio_file):
        st.warning("Please upload a photo and an audio file.")
        st.stop()
    elif mode == ui["mode_photo_music"] and not photo_file:
        st.warning("Please upload a photo.")
        st.stop()
    elif mode == ui["mode_video_music"] and not video_file:
        st.warning("Please upload a video file.")
        st.stop()

    with st.spinner(ui["spinner"]):
        try:
            if mode != ui["mode_video_music"]:
                # --- Photo modes ---
                img_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
                with open(img_path, "wb") as f:
                    f.write(photo_file.getbuffer())
                img = Image.open(img_path).convert("RGB")
                target_w = 720
                ratio = target_w / img.width
                new_size = (target_w, int(img.height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
                img_array = np.array(img)
                target_h = img_array.shape[0]

                # Background
                if bg_option == ui["bg_solid"]:
                    bg_rgb = tuple(int(bg_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
                    bg_clip = ColorClip(size=(target_w, target_h), color=bg_rgb, duration=1)
                else:
                    if bg_image_path and os.path.exists(bg_image_path):
                        bg_img = Image.open(bg_image_path).convert("RGB")
                        bg_img = bg_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
                        bg_clip = ImageClip(np.array(bg_img), duration=1)
                    else:
                        bg_clip = ColorClip(size=(target_w, target_h), color=(0,0,0), duration=1)

                # Determine main audio and duration
                if mode == ui["mode_photo_speech"]:
                    audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                    asyncio.run(generate_speech(text_to_say, audio_path, tts_voice))
                    main_audio = load_audio_file(audio_path)
                    if main_audio is None:
                        st.stop()
                    duration = main_audio.duration
                    main_audio_file = audio_path
                elif mode == ui["mode_photo_audio"]:
                    audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                    with open(audio_path, "wb") as f:
                        f.write(audio_file.getbuffer())
                    main_audio = load_audio_file(audio_path)
                    if main_audio is None:
                        st.stop()
                    duration = main_audio.duration
                    main_audio_file = audio_path
                else:  # mode_photo_music
                    if uploaded_music:
                        audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                        with open(audio_path, "wb") as f:
                            f.write(uploaded_music.getbuffer())
                    elif selected_music != "None":
                        music_url = MUSIC_TRACKS[selected_music]
                        audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                        resp = requests.get(music_url)
                        if resp.status_code != 200:
                            st.error("Failed to download the selected music track. Please try another one or upload your own.")
                            st.stop()
                        with open(audio_path, "wb") as f:
                            f.write(resp.content)
                    else:
                        st.error("Please select or upload a music track.")
                        st.stop()
                    # Validate the downloaded/uploaded music file
                    main_audio = load_audio_file(audio_path)
                    if main_audio is None:
                        st.stop()
                    duration = main_audio.duration
                    main_audio_file = audio_path

                bg_clip = bg_clip.set_duration(duration)
                photo_clip = ImageClip(img_array, duration=duration).set_position("center")
                video = CompositeVideoClip([bg_clip, photo_clip], size=(target_w, target_h))
                video = video.set_audio(main_audio)

                # Add optional background music only for non‑music modes (to avoid double music)
                if mode != ui["mode_photo_music"] and (selected_music != "None" or uploaded_music):
                    if uploaded_music:
                        music_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                        with open(music_path, "wb") as f:
                            f.write(uploaded_music.getbuffer())
                    else:
                        music_url = MUSIC_TRACKS[selected_music]
                        music_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                        resp = requests.get(music_url)
                        if resp.status_code != 200:
                            st.error("Failed to download background music.")
                            st.stop()
                        with open(music_path, "wb") as f:
                            f.write(resp.content)
                    bg_music = load_audio_file(music_path)
                    if bg_music is None:
                        st.warning("Background music is invalid, skipping.")
                    else:
                        if bg_music.duration < duration:
                            n_loops = int(duration / bg_music.duration) + 1
                            bg_music = concatenate_audioclips([bg_music] * n_loops)
                        bg_music = bg_music.subclip(0, duration).volumex(music_volume)
                        final_audio = CompositeAudioClip([main_audio, bg_music])
                        video = video.set_audio(final_audio)
                        os.unlink(music_path)

                output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
                video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", verbose=False, logger=None)

                os.unlink(img_path)
                os.unlink(main_audio_file)
                if bg_image_path and os.path.exists(bg_image_path):
                    os.unlink(bg_image_path)

            else:
                # --- Video mode ---
                video_path_input = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
                with open(video_path_input, "wb") as f:
                    f.write(video_file.getbuffer())
                video_clip = VideoFileClip(video_path_input)
                duration = video_clip.duration

                if selected_music != "None" or uploaded_music:
                    if uploaded_music:
                        music_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                        with open(music_path, "wb") as f:
                            f.write(uploaded_music.getbuffer())
                    else:
                        music_url = MUSIC_TRACKS[selected_music]
                        music_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                        resp = requests.get(music_url)
                        if resp.status_code != 200:
                            st.error("Failed to download background music.")
                            st.stop()
                        with open(music_path, "wb") as f:
                            f.write(resp.content)
                    music_clip = load_audio_file(music_path)
                    if music_clip is None:
                        st.warning("Background music is invalid, skipping.")
                    else:
                        if music_clip.duration < duration:
                            n_loops = int(duration / music_clip.duration) + 1
                            music_clip = concatenate_audioclips([music_clip] * n_loops)
                        music_clip = music_clip.subclip(0, duration).volumex(music_volume)
                        orig_audio = video_clip.audio
                        if orig_audio:
                            final_audio = CompositeAudioClip([orig_audio, music_clip])
                        else:
                            final_audio = music_clip
                        video_clip = video_clip.set_audio(final_audio)
                    os.unlink(music_path)

                output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
                video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)
                os.unlink(video_path_input)

            st.session_state.video_path = output_path
            st.success(ui["success"])

        except Exception as e:
            st.error(f"Error: {e}")

if st.session_state.video_path and os.path.exists(st.session_state.video_path):
    st.markdown(f"### {ui['preview']}")
    st.video(st.session_state.video_path)
    with open(st.session_state.video_path, "rb") as f:
        video_bytes = f.read()
        b64 = base64.b64encode(video_bytes).decode()
        st.markdown(f'<a href="data:video/mp4;base64,{b64}" download="output.mp4"><button style="background-color:#28a745; color:white; padding:10px 20px; border:none; border-radius:30px; cursor:pointer;">{ui["download_btn"]}</button></a>', unsafe_allow_html=True)

st.markdown(f'<div class="footer-caption">{ui["caption"]}</div>', unsafe_allow_html=True)
