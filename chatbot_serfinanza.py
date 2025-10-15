import streamlit as st
import pandas as pd
import requests
import io
import datetime
from openai import OpenAI
from github import Github

# ============================
# ⚙️ CONFIGURACIÓN INICIAL
# ============================
st.set_page_config(page_title="💬 Chatbot IA - Banco Serfinanza", layout="centered")

# --- Repositorio y token (ajusta tu token personal aquí) ---
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
REPO_NAME = "andrescruz7777-arch/CHATBOT-SERFINANZA"
EXCEL_FILE = "logs_negociacion.xlsx"

# Inicializa conexión GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# ============================
# 🎨 ESTILOS CORPORATIVOS
# ============================
st.markdown("""
<style>
html, body, .stApp, [data-testid="stAppViewContainer"] {
    background-color: #FFFFFF !important;
    color: #1B168C !important;
}
h1, h2, h3 { color: #1B168C !important; text-align: center; }
.intro-text { text-align:center; font-size:1.1em; font-weight:500; color:#1B168C; }
.highlight { color:#F43B63; font-weight:600; }
div.stButton > button {
    background-color:#1B168C !important; color:#FFF !important; border:none; border-radius:10px;
    padding:12px 40px !important; font-weight:600; font-size:1em; box-shadow:0 4px 15px rgba(27,22,140,.3);
}
div.stButton > button:hover { background-color:#F43B63 !important; transform:scale(1.05); }
table { width:100%; border-collapse:collapse; }
th { background:#1B168C; color:#FFF; padding:10px; }
td { text-align:center; padding:8px; border-bottom:1px solid #EEE; }
</style>
""", unsafe_allow_html=True)

# ============================
# 🖼️ CABECERA
# ============================
st.markdown("""
<div style="display:flex;justify-content:space-between;align-items:center;padding:0 2rem;">
    <img src="https://raw.githubusercontent.com/andrescruz7777-arch/CHATBOT-SERFINANZA/main/logo_contacto.png" width="160">
    <img src="https://raw.githubusercontent.com/andrescruz7777-arch/CHATBOT-SERFINANZA/main/logo_serfinanza.png" width="180">
</div>
""", unsafe_allow_html=True)

st.markdown("<h1>💬 Hola, soy Chris</h1>", unsafe_allow_html=True)
st.markdown("""
<div class="intro-text">
Soy tu <span class="highlight">Asistente Virtual IA</span> de <b>Contacto Solutions</b>, aliado estratégico de <b>Banco Serfinanza</b>.<br>
Estoy aquí para brindarte información de tus productos y registrar tus solicitudes.
</div>
""", unsafe_allow_html=True)

# ============================
# 🧠 FUNCIONES AUXILIARES
# ============================

def get_geolocation():
    """Obtiene IP pública y geolocalización."""
    try:
        ip = requests.get("https://api.ipify.org?format=json").json().get("ip", "Desconocida")
        geo = requests.get(f"http://ip-api.com/json/{ip}").json()
        return {
            "ip": ip,
            "ciudad": geo.get("city", "No disponible"),
            "region": geo.get("regionName", "No disponible"),
            "pais": geo.get("country", "No disponible")
        }
    except Exception:
        return {"ip":"Desconocida","ciudad":"No disponible","region":"No disponible","pais":"No disponible"}

def append_to_github_excel(nuevo_registro: dict):
    """Agrega una fila nueva al Excel del repositorio y lo actualiza."""
    try:
        file_content = repo.get_contents(EXCEL_FILE)
        df_existente = pd.read_excel(io.BytesIO(file_content.decoded_content))
    except Exception:
        df_existente = pd.DataFrame()

    nuevo_df = pd.DataFrame([nuevo_registro])
    df_final = pd.concat([df_existente, nuevo_df], ignore_index=True)

    # Convierte a bytes
    excel_bytes = io.BytesIO()
    df_final.to_excel(excel_bytes, index=False, engine="openpyxl")
    excel_bytes.seek(0)

    # Actualiza archivo en el repositorio
    repo.update_file(
        path=EXCEL_FILE,
        message=f"Actualización de registro {nuevo_registro.get('Cedula','')}",
        content=excel_bytes.getvalue(),
        sha=file_content.sha if 'file_content' in locals() else None
    )

# ============================
# 💬 CHATBOT / SIMULADOR
# ============================
st.subheader("🪪 Validación rápida")
cedula = st.text_input("Digita tu número de cédula:", key="cedula")
nombre = st.text_input("Tu nombre completo:", key="nombre")
producto = st.selectbox("Selecciona tu producto:", ["TARJETA DE CRÉDITO", "CRÉDITO DE LIBRE INVERSIÓN", "OTRO"])
estrategia = st.selectbox("Estrategia actual:", ["REDIFERIDO SIN PAGO", "REESTRUCTURACION CON PAGO", "PRORROGA"])
cuotas = st.selectbox("Selecciona la cantidad de cuotas:", ["12 cuotas", "24 cuotas", "36 cuotas", "48 cuotas", "60 cuotas"])

if st.button("💾 Registrar negociación"):
    geo = get_geolocation()
    registro = {
        "FechaHora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Cedula": cedula,
        "Nombre": nombre,
        "Producto": producto,
        "Estrategia": estrategia,
        "Cuotas": cuotas,
        "IP": geo["ip"],
        "Ciudad": geo["ciudad"],
        "Region": geo["region"],
        "Pais": geo["pais"]
    }
    append_to_github_excel(registro)
    st.success("✅ Registro guardado exitosamente en GitHub.")
    st.json(registro)
