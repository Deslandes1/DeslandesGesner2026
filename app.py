import streamlit as st
import asyncio
import tempfile
import base64
import os

# ----- 1. Audio Engine & Safety -----
try:
    import edge_tts
    import nest_asyncio
    nest_asyncio.apply()
    EDGE_TTS_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    EDGE_TTS_AVAILABLE = False

st.set_page_config(page_title="Portuguese with Gesner", layout="wide")

# ----- 2. Scaled Styling (Reduced Font & Spacing for Video) -----
def apply_custom_style():
    st.markdown("""
        <style>
        /* Compact UI Adjustments */
        .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }
        
        .stApp, [data-testid="stSidebar"] { 
            background: linear-gradient(135deg, #1a0b2e, #2d1b4e, #1a0b2e) !important; 
        }
        
        /* Scaled Header */
        .main-header { 
            background: linear-gradient(135deg, #ff6b6b, #feca57, #48dbfb); 
            padding: 0.8rem; 
            border-radius: 12px; 
            text-align: center; 
            margin-bottom: 0.5rem; 
        }
        .main-header h1 { color: white !important; font-size: 1.8rem !important; margin: 0; }
        .main-header p { color: #fff5cc; font-size: 0.9rem !important; margin: 0; }
        
        /* Sidebar scaling */
        [data-testid="stSidebar"] * { color: white !important; font-size: 0.85rem !important; }
        
        /* General Text scaling */
        html, body, .stMarkdown, p, span, label, h2, h3 { color: white !important; font-size: 0.95rem !important; }
        
        /* Tab scaling */
        .stTabs [role="tab"] { color: white !important; padding: 5px 10px !important; font-size: 0.8rem !important; }
        
        /* Button scaling */
        .stButton button { height: 28px !important; padding: 0 !important; font-size: 0.8rem !important; }
        </style>
    """, unsafe_allow_html=True)

def show_logo(size=50):
    st.markdown(f"""
        <div style="display: flex; justify-content: center; margin-bottom: 0.5rem;">
            <svg width="{size}" height="{size}" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" fill="url(#gradLogo)" stroke="#ffcc00" stroke-width="2"/>
                <defs><linearGradient id="gradLogo" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ff007f"/><stop offset="100%" stop-color="#00ffcc"/>
                </linearGradient></defs>
                <text x="50" y="65" font-size="40" text-anchor="middle" fill="white" font-weight="bold">📘</text>
            </svg>
        </div>
    """, unsafe_allow_html=True)

# ----- 3. Content Logic -----
temas = ["Apresentar-se", "Rotina diária", "No supermercado", "Pedir comida", "Perguntar direções", "Falar da família", "No consultório médico", "Entrevista de emprego", "Planejar uma viagem", "Clima e estações", "Comprar roupas", "No banco", "Usar transporte público", "Alugar um apartamento", "Comemorar um aniversário", "Ir ao cinema", "Na academia", "Fazer uma ligação", "Escrever um e-mail", "Falar de hobbies"]

async def save_speech(text, file_path):
    communicate = edge_tts.Communicate(text, "es-ES-AlvaroNeural")
    await communicate.save(file_path)

def reproducir_audio(texto, key):
    if st.button(f"🔊", key=key):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            try:
                asyncio.run(save_speech(texto, tmp.name))
                with open(tmp.name, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                    st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay style="width: 100%; height: 30px;"></audio>', unsafe_allow_html=True)
            finally:
                if os.path.exists(tmp.name): os.unlink(tmp.name)

# ----- 4. Sidebar & UI -----
apply_custom_style()

with st.sidebar:
    show_logo(40)
    st.markdown("### 🎯 Lições")
    lesson_number = st.selectbox("Escolha", list(range(1, 21)), index=0, key="lesson_selector")
    st.progress(lesson_number / 20)
    st.markdown("---")
    st.markdown("👨‍🏫 **Dev:** Gesner Deslandes")
    st.markdown("📞 (509) 4738-5663")
    st.markdown("🌐 GlobalInternet.py")
    st.markdown("**Preço:** $299 USD")

# Main Content
st.markdown(f'<div class="main-header"><h1>Portuguese with Gesner</h1><p>Lição {lesson_number}: {temas[lesson_number-1]}</p></div>', unsafe_allow_html=True)

tabs = st.tabs(["💬 Conversas", "📚 Vocabulário", "📖 Gramática", "🎧 Pronúncia"])

with tabs[0]:
    st.markdown(f"**Tema:** {temas[lesson_number-1]}")
    txt = "Olá! Vamos praticar português hoje?"
    st.text(txt)
    reproducir_audio(txt, "aud_1")

with tabs[1]:
    words = ["Olá", "Obrigado", "Sim", "Não", "Amigo"]
    cols = st.columns(len(words))
    for i, w in enumerate(words):
        with cols[i]:
            st.write(w)
            reproducir_audio(w, f"word_{i}")

with tabs[3]:
    st.write("Pratique a frase:")
    p_txt = "Eu gosto de aprender tecnologia."
    st.info(p_txt)
    reproducir_audio(p_txt, "p_1")
