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

st.set_page_config(page_title="Let's Learn Portuguese with Gesner", layout="wide")

# ----- 2. Styling (Purple Margins & Force White Sidebar Text) -----
def apply_custom_style():
    st.markdown("""
        <style>
        .stApp, [data-testid="stSidebar"] { 
            background: linear-gradient(135deg, #1a0b2e, #2d1b4e, #1a0b2e) !important; 
        }
        .main-header { 
            background: linear-gradient(135deg, #ff6b6b, #feca57, #48dbfb); 
            padding: 1.5rem; border-radius: 20px; text-align: center; margin-bottom: 1rem; 
        }
        .main-header h1 { color: white !important; text-shadow: 2px 2px 4px #000000; font-size: 2.5rem; margin: 0; }
        [data-testid="stSidebar"] * { color: white !important; }
        [data-testid="stSidebar"] label p { color: white !important; font-weight: bold !important; }
        html, body, [data-testid="stHeader"], .stMarkdown, p, span, label, h2, h3 { color: white !important; }
        .stButton button { background-color: #ff6b6b; color: white !important; border-radius: 30px; font-weight: bold; width: 100%; border: none; }
        .stTabs [role="tab"] { color: white !important; }
        </style>
    """, unsafe_allow_html=True)

def show_logo():
    st.markdown("""
        <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
            <svg width="80" height="80" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" fill="url(#gradLogo)" stroke="#ffcc00" stroke-width="2"/>
                <defs><linearGradient id="gradLogo" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ff007f"/><stop offset="100%" stop-color="#00ffcc"/>
                </linearGradient></defs>
                <text x="50" y="65" font-size="40" text-anchor="middle" fill="white" font-weight="bold">📘</text>
            </svg>
        </div>
    """, unsafe_allow_html=True)

async def save_speech(text, file_path):
    communicate = edge_tts.Communicate(text, "es-ES-AlvaroNeural")
    await communicate.save(file_path)

def reproducir_audio(texto, key):
    if not EDGE_TTS_AVAILABLE:
        st.info("🔇 Áudio desabilitado.")
        return
    if st.button(f"🔊 Ouvir", key=key):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            try:
                asyncio.run(save_speech(texto, tmp.name))
                with open(tmp.name, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                    st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay style="width: 100%;"></audio>', unsafe_allow_html=True)
            finally:
                if os.path.exists(tmp.name): os.unlink(tmp.name)

temas = ["Apresentar-se", "Rotina diária", "No supermercado", "Pedir comida", "Perguntar direções", "Falar da família", "No consultório médico", "Entrevista de emprego", "Planejar uma viagem", "Clima e estações", "Comprar roupas", "No banco", "Usar transporte público", "Alugar um apartamento", "Comemorar um aniversário", "Ir ao cinema", "Na academia", "Fazer uma ligação", "Escrever um e-mail", "Falar de hobbies"]

def get_lesson_content(n):
    tema = temas[n-1]
    return {
        "conversas": [f"A: Olá! Hoje vamos praticar {tema}.\nB: Sim! É um assunto muito importante."],
        "vocabulario": ["Olá", "Oi", "Bom dia", "Boa tarde", "Obrigado"],
        "gramatica": [f"1. Como usar verbos em {tema}."],
        "pronuncia": [f"Eu quero aprender mais sobre {tema}."]
    }

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    apply_custom_style()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_logo()
        st.markdown("<h1 style='text-align: center;'>🔐 Login Required</h1>", unsafe_allow_html=True)
        pwd = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if pwd == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Senha incorreta.")
    st.stop()

apply_custom_style()
with st.sidebar:
    show_logo()
    st.markdown("### 🎯 Menu de Lições")
    lesson_number = st.selectbox("Selecione a lição", list(range(1, 21)), index=0, key="lesson_selector")
    st.progress(lesson_number / 20)
    st.markdown("---")
    st.markdown("### 👨‍🏫 Informações do Desenvolvedor")
    st.markdown("**Nome:** Gesner Deslandes")
    st.markdown("📞 **WhatsApp:** (509) 4738-5663")
    st.markdown("📧 **Email:** deslandes78@gmail.com")
    st.markdown("🌐 **GlobalInternet.py**")
    st.markdown("---")
    st.markdown("### 💰 Preço: $299 USD")

st.markdown(f'<div class="main-header"><h1>📘 Let\'s Learn Portuguese with Gesner</h1><p>Lição {lesson_number}: {temas[lesson_number-1]}</p></div>', unsafe_allow_html=True)
content = get_lesson_content(lesson_number)
tabs = st.tabs(["💬 Conversas", "📚 Vocabulário", "📖 Gramática", "🎧 Pronúncia", "❓ Quiz"])

with tabs[3]:
    st.markdown("### Pratique sua pronúncia")
    for idx, p in enumerate(content["pronuncia"]):
        st.write(p)
        reproducir_audio(p, f"p_{lesson_number}_{idx}")
