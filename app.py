import streamlit as st
import tempfile
import os
import base64
import asyncio
import numpy as np
from PIL import Image
from moviepy.editor import ImageClip, AudioFileClip, ColorClip, CompositeVideoClip
import edge_tts

st.set_page_config(page_title="AI Talking Photo – GlobalInternet.py", layout="centered")

# Language dictionary
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
        "caption": "Uses edge-tts male voice and static photo. No lip sync – simple and reliable."
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
        "caption": "Utilise la voix masculine edge-tts et une photo fixe. Pas de synchronisation labiale – simple et fiable."
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
        "caption": "Usa voz masculina edge-tts y foto fija. Sin sincronización de labios – simple y confiable."
    }}
}

# Default to English
if "lang" not in st.session_state:
    st.session_state.lang = "English"

def set_language():
    lang = st.session_state.lang
    return LANGUAGES[lang]["ui"], LANGUAGES[lang]["voice"]

# Sidebar language selector
with st.sidebar:
    st.image("https://flagcdn.com/w320/ht.png", width=80)
    st.markdown("### GlobalInternet.py")
    st.markdown("**Founder:** Gesner Deslandes")
    st.markdown("📞 WhatsApp: (509) 4738-5663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("---")
    st.selectbox("🌐 Language", options=list(LANGUAGES.keys()), key="lang", on_change=set_language)
    st.markdown("---")

# Get UI texts and voice for the selected language
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

# Initialize variables
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
            
            # 2. Generate audio with selected voice
            audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
            await generate_audio(text_to_say, audio_path, tts_voice)
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
            
            # 6. Composite video
            video = CompositeVideoClip([bg_clip, photo_clip], size=(target_w, img_array.shape[0]))
            video = video.set_audio(audio)
            
            # 7. Write video file
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
            video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", verbose=False, logger=None)
            
            st.session_state.video_path = output_path
            
            # Cleanup
            for p in [img_path, audio_path]:
                if os.path.exists(p):
                    os.unlink(p)
            if bg_image_path and os.path.exists(bg_image_path):
                os.unlink(bg_image_path)
            
            st.success(ui_text["success"])

# Show the video if it exists
if st.session_state.video_path and os.path.exists(st.session_state.video_path):
    st.markdown(f"### {ui_text['preview']}")
    st.video(st.session_state.video_path)
    with open(st.session_state.video_path, "rb") as f:
        video_bytes = f.read()
        b64 = base64.b64encode(video_bytes).decode()
        st.markdown(f'<a href="data:video/mp4;base64,{b64}" download="talking_photo.mp4"><button style="background-color:#28a745; color:white; padding:10px 20px; border:none; border-radius:30px; cursor:pointer;">{ui_text["download_btn"]}</button></a>', unsafe_allow_html=True)

st.markdown("---")
st.caption(ui_text["caption"])
