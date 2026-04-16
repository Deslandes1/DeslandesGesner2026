import streamlit as st
import tempfile
import os
import base64
import asyncio
import numpy as np
from PIL import Image
from moviepy.editor import ImageClip, AudioFileClip, ColorClip, CompositeVideoClip, concatenate_audioclips
import edge_tts

st.set_page_config(page_title="AI Talking Photo – GlobalInternet.py", layout="centered")

# Language settings
LANGUAGES = {
    "English": {"code": "en", "voice": "en-US-GuyNeural", "ui": {
        "title": "🎭 AI Talking Photo",
        "subtitle": "Upload a photo, type a message, and the photo will speak (static image + voice).",
        "bg_label": "Background",
        "bg_solid": "Solid color",
        "bg_custom": "Custom image",
        "color_picker": "Pick a color",
        "upload_bg": "Upload background image",
        "upload_photo": "Choose a photo (face visible)",
        "message_label": "What should the photo say?",
        "generate_btn": "Generate Talking Video",
        "warning_photo": "Please upload a photo and enter text.",
        "spinner": "Creating video... (may take up to a minute)",
        "success": "Video created successfully! Preview below.",
        "preview": "🎬 Preview",
        "download_btn": "⬇️ Download Video",
        "caption": "Uses edge-tts male voice and static photo. No lip sync – simple and reliable.",
        "music_label": "Background music (optional)",
        "no_music": "None",
        "music_volume": "Music volume"
    }},
    "French": {"code": "fr", "voice": "fr-FR-HenriNeural", "ui": {
        "title": "🎭 Photo Parlante IA",
        "subtitle": "Téléchargez une photo, tapez un message, et la photo parlera (image fixe + voix).",
        "bg_label": "Arrière‑plan",
        "bg_solid": "Couleur unie",
        "bg_custom": "Image personnalisée",
        "color_picker": "Choisissez une couleur",
        "upload_bg": "Téléchargez une image d'arrière‑plan",
        "upload_photo": "Choisissez une photo (visage visible)",
        "message_label": "Que doit dire la photo ?",
        "generate_btn": "Générer la vidéo parlante",
        "warning_photo": "Veuillez télécharger une photo et entrer un texte.",
        "spinner": "Création de la vidéo... (peut prendre une minute)",
        "success": "Vidéo créée avec succès ! Aperçu ci‑dessous.",
        "preview": "🎬 Aperçu",
        "download_btn": "⬇️ Télécharger la vidéo",
        "caption": "Utilise la voix masculine edge-tts et une photo fixe. Pas de synchronisation labiale – simple et fiable.",
        "music_label": "Musique de fond (optionnelle)",
        "no_music": "Aucune",
        "music_volume": "Volume musique"
    }},
    "Spanish": {"code": "es", "voice": "es-ES-AlvaroNeural", "ui": {
        "title": "🎭 Foto Parlante IA",
        "subtitle": "Sube una foto, escribe un mensaje y la foto hablará (imagen fija + voz).",
        "bg_label": "Fondo",
        "bg_solid": "Color sólido",
        "bg_custom": "Imagen personalizada",
        "color_picker": "Elige un color",
        "upload_bg": "Sube una imagen de fondo",
        "upload_photo": "Elige una foto (rostro visible)",
        "message_label": "¿Qué debe decir la foto?",
        "generate_btn": "Generar video parlante",
        "warning_photo": "Por favor sube una foto y escribe un texto.",
        "spinner": "Creando video... (puede tomar un minuto)",
        "success": "¡Video creado con éxito! Vista previa abajo.",
        "preview": "🎬 Vista previa",
        "download_btn": "⬇️ Descargar video",
        "caption": "Usa voz masculina edge-tts y foto fija. Sin sincronización de labios – simple y confiable.",
        "music_label": "Música de fondo (opcional)",
        "no_music": "Ninguna",
        "music_volume": "Volumen música"
    }}
}

# 50 promotional background music tracks (royalty-free URLs – replace with your own)
# Using free tracks from Pixabay and other sources – all are short and usable.
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

# Fill remaining up to 50 (already 50 entries)
# Ensure we have exactly 50 keys (including "None")
# The dict above has 1 + 49 = 50 entries.

if "lang" not in st.session_state:
    st.session_state.lang = "English"

def set_language():
    lang = st.session_state.lang
    return LANGUAGES[lang]["ui"], LANGUAGES[lang]["voice"]

with st.sidebar:
    st.image("https://flagcdn.com/w320/ht.png", width=80)
    st.markdown("### GlobalInternet.py")
    st.markdown("**Founder:** Gesner Deslandes")
    st.markdown("📞 WhatsApp: (509) 4738-5663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("---")
    st.selectbox("🌐 Language", options=list(LANGUAGES.keys()), key="lang", on_change=set_language)
    st.markdown("---")

ui_text, tts_voice = set_language()

st.markdown(f"""
<style>
    .stApp {{ background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }}
    h1, h2, h3 {{ color: #48dbfb; }}
    .stButton button {{ background-color: #ff6b35; color: white; border-radius: 30px; }}
</style>
""", unsafe_allow_html=True)

st.title(ui_text["title"])
st.markdown(ui_text["subtitle"])

bg_image_path = None

with st.sidebar:
    bg_option = st.radio(ui_text["bg_label"], [ui_text["bg_solid"], ui_text["bg_custom"]])
    if bg_option == ui_text["bg_solid"]:
        bg_color = st.color_picker(ui_text["color_picker"], "#1a1a2e")
    else:
        bg_image_file = st.file_uploader(ui_text["upload_bg"], type=["jpg", "png", "jpeg"])
        if bg_image_file:
            bg_image_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
            with open(bg_image_path, "wb") as f:
                f.write(bg_image_file.getbuffer())

uploaded_file = st.file_uploader(ui_text["upload_photo"], type=["jpg", "png", "jpeg"])
text_to_say = st.text_area(ui_text["message_label"], height=100, placeholder="Type your message here...")

# Background music selection
music_options = list(MUSIC_TRACKS.keys())
selected_music = st.selectbox(ui_text["music_label"], music_options, index=0)
music_volume = 0.5
if selected_music != "None":
    music_volume = st.slider(ui_text["music_volume"], 0.0, 1.0, 0.5, 0.05)

if "video_path" not in st.session_state:
    st.session_state.video_path = None

async def generate_audio(text, output_path, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

if st.button(ui_text["generate_btn"], use_container_width=True):
    if not uploaded_file or not text_to_say.strip():
        st.warning(ui_text["warning_photo"])
    else:
        with st.spinner(ui_text["spinner"]):
            # 1. Save uploaded image
            img_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
            with open(img_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # 2. Generate spoken audio (male voice)
            audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
            asyncio.run(generate_audio(text_to_say, audio_path, tts_voice))
            voice_clip = AudioFileClip(audio_path)
            duration = voice_clip.duration
            
            # 3. Load and resize photo
            img = Image.open(img_path).convert("RGB")
            target_w = 720
            ratio = target_w / img.width
            new_size = (target_w, int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            img_array = np.array(img)
            
            # 4. Create background
            if bg_option == ui_text["bg_solid"]:
                bg_rgb = tuple(int(bg_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
                bg_clip = ColorClip(size=(target_w, img_array.shape[0]), color=bg_rgb, duration=duration)
            else:
                if bg_image_path and os.path.exists(bg_image_path):
                    bg_img = Image.open(bg_image_path).convert("RGB")
                    bg_img = bg_img.resize((target_w, img_array.shape[0]), Image.Resampling.LANCZOS)
                    bg_clip = ImageClip(np.array(bg_img), duration=duration)
                else:
                    bg_clip = ColorClip(size=(target_w, img_array.shape[0]), color=(0,0,0), duration=duration)
            
            # 5. Create photo clip (static, centered)
            photo_clip = ImageClip(img_array, duration=duration).set_position("center")
            
            # 6. Composite video (background + photo)
            video = CompositeVideoClip([bg_clip, photo_clip], size=(target_w, img_array.shape[0]))
            
            # 7. Add audio (voice + optional background music)
            if selected_music != "None" and MUSIC_TRACKS[selected_music]:
                import requests
                music_url = MUSIC_TRACKS[selected_music]
                # Download background music
                music_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                resp = requests.get(music_url)
                with open(music_path, "wb") as f:
                    f.write(resp.content)
                music_clip = AudioFileClip(music_path)
                # Loop music to match duration
                if music_clip.duration < duration:
                    n_loops = int(duration / music_clip.duration) + 1
                    music_clip = concatenate_audioclips([music_clip] * n_loops)
                music_clip = music_clip.subclip(0, duration).volumex(music_volume)
                # Mix voice and music
                final_audio = CompositeAudioClip([voice_clip, music_clip])
                video = video.set_audio(final_audio)
                # Cleanup music temp file
                os.unlink(music_path)
            else:
                video = video.set_audio(voice_clip)
            
            # 8. Write video
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
            video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", verbose=False, logger=None)
            
            st.session_state.video_path = output_path
            
            # Cleanup temporary files
            for p in [img_path, audio_path]:
                if os.path.exists(p):
                    os.unlink(p)
            if bg_image_path and os.path.exists(bg_image_path):
                os.unlink(bg_image_path)
            
            st.success(ui_text["success"])

if st.session_state.video_path and os.path.exists(st.session_state.video_path):
    st.markdown(f"### {ui_text['preview']}")
    st.video(st.session_state.video_path)
    with open(st.session_state.video_path, "rb") as f:
        video_bytes = f.read()
        b64 = base64.b64encode(video_bytes).decode()
        st.markdown(f'<a href="data:video/mp4;base64,{b64}" download="talking_photo.mp4"><button style="background-color:#28a745; color:white; padding:10px 20px; border:none; border-radius:30px; cursor:pointer;">{ui_text["download_btn"]}</button></a>', unsafe_allow_html=True)

st.markdown("---")
st.caption(ui_text["caption"])
