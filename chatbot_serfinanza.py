# chatbot_serfinanza.py — versión completa con registro automático en GitHub
import streamlit as st
import pandas as pd
import requests, io, datetime, base64, json
from openai import OpenAI

# ============================
# ⚙️ CONFIGURACIÓN INICIAL
# ============================
st.set_page_config(page_title="💬 Chatbot IA - Banco Serfinanza", layout="centered")

# Tokens y rutas
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "")
GITHUB_TOKEN = st.secrets.get("GH_TOKEN", "")
GITHUB_REPO = "andrescruz7777-arch/CHATBOT-SERFINANZA"
LOG_FILE = "logs_negociacion.xlsx"

# ============================
# 🔧 FUNCIONES AUXILIARES
# ============================

def get_public_ip_and_geo():
    """Obtiene IP pública y geolocalización"""
    try:
        ip = requests.get("https://api.ipify.org?format=json", timeout=10).json().get("ip", "Desconocida")
        geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=10).json()
        return ip, geo.get("city", "No disponible"), geo.get("regionName", "No disponible"), geo.get("country", "No disponible")
    except Exception:
        return "Desconocida", "No disponible", "No disponible", "No disponible"

def github_get_file(repo, path, token):
    """Obtiene archivo desde GitHub (base64 decode)"""
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        content = base64.b64decode(data["content"])
        sha = data["sha"]
        return content, sha
    elif r.status_code == 404:
        return None, None
    else:
        raise Exception(f"Error al obtener archivo: {r.status_code}")

def github_update_file(repo, path, token, new_content, sha=None):
    """Crea o actualiza archivo en GitHub"""
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    data = {
        "message": f"Registro actualizado {datetime.datetime.now()}",
        "content": base64.b64encode(new_content).decode("utf-8")
    }
    if sha:
        data["sha"] = sha
    r = requests.put(url, headers=headers, data=json.dumps(data))
    if r.status_code not in (200, 201):
        raise Exception(f"Error al subir archivo: {r.status_code} {r.text}")

def save_log_to_github(entry):
    """Guarda un registro en logs_negociacion.xlsx"""
    if not GITHUB_TOKEN:
        return
    try:
        content, sha = github_get_file(GITHUB_REPO, LOG_FILE, GITHUB_TOKEN)
        if content:
            df = pd.read_excel(io.BytesIO(content))
        else:
            df = pd.DataFrame()
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
        buf = io.BytesIO()
        df.to_excel(buf, index=False, engine="openpyxl")
        buf.seek(0)
        github_update_file(GITHUB_REPO, LOG_FILE, GITHUB_TOKEN, buf.read(), sha)
        st.success("✅ Registro guardado")
    except Exception as e:
        st.warning(f"No se pudo registrar el log: {e}")

# ============================
# 🎨 ESTILOS CORPORATIVOS
# ============================
st.markdown("""
<style>
html, body, .stApp, [data-testid="stAppViewContainer"] {
    background-color: #FFFFFF !important;
    color: #1B168C !important;
}
.header-container { display:flex; justify-content:space-between; align-items:center; padding:0 2rem; }
h1, h2, h3 { color:#1B168C !important; text-align:center; }
.highlight { color:#F43B63; font-weight:600; }
.intro-text { text-align:center; font-size:1.15em; font-weight:500; color:#1B168C; margin-top:15px; }
div.stButton > button {
    background-color:#1B168C !important; color:#FFF !important; border:none;
    border-radius:12px !important; padding:16px 60px !important;
    font-size:1.1em !important; font-weight:600 !important;
    box-shadow:0 4px 15px rgba(27,22,140,.3);
}
div.stButton > button:hover { background-color:#F43B63 !important; transform:scale(1.05); }
</style>
""", unsafe_allow_html=True)

# ============================
# 🖼️ CABECERA
# ============================
st.markdown("""
<div class="header-container">
    <img src="https://raw.githubusercontent.com/andrescruz7777-arch/CHATBOT-SERFINANZA/main/logo_contacto.png" width="160">
    <img src="https://raw.githubusercontent.com/andrescruz7777-arch/CHATBOT-SERFINANZA/main/logo_serfinanza.png" width="180">
</div>
""", unsafe_allow_html=True)

# ============================
# 💬 BIENVENIDA
# ============================
st.markdown("<h1>💬 Hola, soy Chris</h1>", unsafe_allow_html=True)
st.markdown("""
<div class="intro-text">
Soy tu <span class="highlight">Asistente Virtual IA</span> de <b>Contacto Solutions</b>, aliado estratégico de <b>Banco Serfinanza</b>.<br>
Estoy aquí para brindarte información de tus productos y registrar tus solicitudes.
</div>
""", unsafe_allow_html=True)

# ============================
# ESTADO Y VARIABLES
# ============================
if "start_chat" not in st.session_state: st.session_state["start_chat"] = False
if "cedula_validada" not in st.session_state: st.session_state["cedula_validada"] = False
if "chat_history" not in st.session_state: st.session_state["chat_history"] = []

# ============================
# 🚀 INICIAR
# ============================
col1, col2, col3 = st.columns([1, 2.4, 1])
with col2:
    if st.button("🚀 INICIAR CHATBOT"):
        st.session_state["start_chat"] = True

# ============================
# 🔍 VALIDACIÓN CÉDULA
# ============================
if st.session_state["start_chat"]:
    st.subheader("🔍 Verificación de identidad")
    with st.form("form_cedula"):
        cedula = st.text_input("🪪 Digita tu número de cédula:")
        submitted = st.form_submit_button("➡️ Continuar")

    if submitted and cedula:
        try:
            data = pd.read_excel("base_bot_serfinanza.xls")
        except Exception as e:
            st.error(f"Error al cargar la base: {e}")
            st.stop()

        cliente = data[data["NUMERO_IDENTIFICACION"].astype(str) == cedula.strip()]
        if cliente.empty:
            st.warning("⚠️ No encontramos información para ese documento.")
            st.stop()
        else:
            st.session_state["cedula_validada"] = True
            st.session_state["cliente_data"] = cliente

# ============================
# 🧭 DETALLE DE OBLIGACIONES
# ============================
if st.session_state.get("cedula_validada", False):
    cliente = st.session_state["cliente_data"]
    nombre = str(cliente["NOMBRE_FINAL"].iloc[0]).title()
    producto = cliente["TIPO_PRODUCTO"].iloc[0]
    estrategia = cliente["ESTRATEGIA_ACTUAL"].iloc[0]

    st.markdown(f"### 👋 Hola {nombre}, estas son tus obligaciones actuales:")
    st.dataframe(cliente[["TIPO_PRODUCTO", "ULTIMOS_CUENTA", "PAGO_MINIMO_MES", "MORA_ACTUAL", "ESTRATEGIA_ACTUAL"]])

    cuotas = ["Selecciona...", "12 cuotas", "24 cuotas", "36 cuotas", "48 cuotas", "60 cuotas", "No estoy interesado"]
    seleccion_cuota = st.selectbox("📆 Selecciona una opción:", cuotas)

    # ==== REGISTRO NEGOCIACIÓN ====
    if seleccion_cuota not in ["Selecciona...", "No estoy interesado"]:
        ip, ciudad, region, pais = get_public_ip_and_geo()
        log_entry = {
            "FechaHora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Cedula": cedula, "Nombre": nombre, "Producto": producto,
            "Estrategia": estrategia, "Cuotas": seleccion_cuota,
            "IP": ip, "Ciudad": ciudad, "Region": region, "Pais": pais,
            "MensajeUsuario": "", "RespuestaIA": ""
        }
        save_log_to_github(log_entry)

    # ==== CHAT IA ====
    if seleccion_cuota == "No estoy interesado":
        client = OpenAI(api_key=OPENAI_API_KEY)
        st.markdown("💬 Asesor Virtual IA – Banco Serfinanza")

        user_msg = st.chat_input("✍️ Escribe tus dudas o inquietudes...")
        if user_msg:
            st.session_state["chat_history"].append({"role": "user", "content": user_msg})
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres un asesor virtual empático del Banco Serfinanza."},
                    *st.session_state["chat_history"]
                ]
            )
            ai_reply = response.choices[0].message.content
            st.session_state["chat_history"].append({"role": "assistant", "content": ai_reply})
            st.markdown(f"**Chris (IA):** {ai_reply}")

            # Registro de trazabilidad del chat
            ip, ciudad, region, pais = get_public_ip_and_geo()
            log_entry = {
                "FechaHora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Cedula": cedula, "Nombre": nombre, "Producto": producto,
                "Estrategia": estrategia, "Cuotas": "No aplica (IA)",
                "IP": ip, "Ciudad": ciudad, "Region": region, "Pais": pais,
                "MensajeUsuario": user_msg, "RespuestaIA": ai_reply
            }
            save_log_to_github(log_entry)
