import streamlit as st
import pandas as pd
from openai import OpenAI
import requests, io, base64, json, datetime, pytz

# ============================
# ⚙️ CONFIGURACIÓN INICIAL
# ============================
st.set_page_config(page_title="💬 Chatbot IA - Banco Serfinanza", layout="centered")

# Estado persistente
if "start_chat" not in st.session_state:
    st.session_state["start_chat"] = False
if "cedula_validada" not in st.session_state:
    st.session_state["cedula_validada"] = False
if "intentos" not in st.session_state:
    st.session_state["intentos"] = 0
if "cuota_elegida" not in st.session_state:
    st.session_state["cuota_elegida"] = None

# ============================
# 🔧 CONFIGURACIÓN GITHUB
# ============================
GH_TOKEN = st.secrets.get("GH_TOKEN", "")
REPO = "andrescruz7777-arch/CHATBOT-SERFINANZA"
FILE_PATH = "logs_negociacion.xlsx"
tz_bogota = pytz.timezone("America/Bogota")

# ============================
# 🔧 FUNCIONES AUXILIARES (IP/Geo y GitHub)
# ============================
def get_ip_geo():
    try:
        ip = requests.get("https://api.ipify.org?format=json", timeout=8).json().get("ip", "Desconocida")
        geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=8).json()
        return ip, geo.get("city", "No disponible"), geo.get("regionName", "No disponible"), geo.get("country", "No disponible")
    except:
        return "Desconocida", "No disponible", "No disponible", "No disponible"

def get_file_from_github(repo, path, token):
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        return base64.b64decode(data["content"]), data["sha"]
    elif r.status_code == 404:
        return None, None
    else:
        raise Exception(r.text)

def push_file_to_github(repo, path, token, content_bytes, sha=None):
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    payload = {
        "message": f"Registro actualización {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "content": base64.b64encode(content_bytes).decode("utf-8")
    }
    if sha:
        payload["sha"] = sha
    r = requests.put(url, headers=headers, data=json.dumps(payload))
    if r.status_code not in (200, 201):
        raise Exception(f"Error GitHub: {r.status_code} -> {r.text}")

def mask_last4(value):
    s = str(value).strip()
    digits = "".join([c for c in s if c.isdigit()])
    return f"****{digits[-4:]}" if len(digits) >= 4 else s

def save_log(entry_base: dict):
    """Guarda un registro en logs_negociacion.xlsx (Bogotá, últimos 4, orden exacto) y muestra ✅ Registro guardado."""
    if not GH_TOKEN:
        return
    try:
        now_bogota = datetime.datetime.now(tz_bogota)
        entry_base["FechaHora"] = now_bogota.strftime("%Y-%m-%d %H:%M:%S")
        entry_base["Fecha"] = now_bogota.strftime("%Y-%m-%d %H:%M:%S")
        if "Cuenta" in entry_base and entry_base["Cuenta"]:
            entry_base["UltimosDigitos"] = mask_last4(entry_base["Cuenta"])
        elif "UltimosDigitos" not in entry_base:
            entry_base["UltimosDigitos"] = ""

        cols = [
            "FechaHora","Cedula","Nombre","Producto","UltimosDigitos","Estrategia",
            "Cuotas","IP","Ciudad","Region","Pais","Fecha","Cuenta","IP_Usuario",
            "MensajeUsuario","RespuestaIA"
        ]

        content, sha = get_file_from_github(REPO, FILE_PATH, GH_TOKEN)
        if content:
            df = pd.read_excel(io.BytesIO(content))
        else:
            df = pd.DataFrame(columns=cols)

        for c in cols:
            if c not in df.columns:
                df[c] = ""

        row = {c: entry_base.get(c, "") for c in cols}
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)[cols]

        buffer = io.BytesIO()
        df.to_excel(buffer, index=False, engine="openpyxl")
        buffer.seek(0)
        push_file_to_github(REPO, FILE_PATH, GH_TOKEN, buffer.read(), sha)
        st.success("✅ Registro guardado")
    except Exception as e:
        st.warning(f"No se pudo registrar: {e}")

# ============================
# 🎨 ESTILOS CORPORATIVOS (tus colores intactos)
# ============================
st.markdown("""
<style>
html, body, .stApp, [data-testid="stAppViewContainer"] {
    background-color: #FFFFFF !important;
    color: #1B168C !important;
}
.header-container {
    display: flex; justify-content: space-between; align-items: center; padding: 0 2rem;
}
h1, h2, h3 { color: #1B168C !important; text-align: center; }
.intro-text {
    text-align: center; font-size: 1.15em; font-weight: 500; line-height: 1.6em;
    margin-top: 15px; color: #1B168C !important;
}
.highlight { color: #F43B63; font-weight: 600; }

div.stButton > button, form button[kind="primary"] {
    background-color:#1B168C !important; color:#FFFFFF !important; border:none;
    border-radius:12px !important; padding:16px 60px !important;
    font-size:1.1em !important; font-weight:600 !important;
    box-shadow:0 4px 15px rgba(27,22,140,.3) !important;
}
div.stButton > button:hover, form button[kind="primary"]:hover {
    background-color:#F43B63 !important; transform:scale(1.05);
}
label, .stTextInput label { color: #1B168C !important; font-weight: 700 !important; }
.stTextInput > div > div {
    background-color: #1B168C !important; border: 2px solid #F43B63 !important;
    border-radius: 10px !important;
}
.stTextInput > div > div > input {
    background-color: transparent !important; color: #FFFFFF !important;
    font-weight: 600 !important; border: none !important;
}
.stTextInput input::placeholder { color: #E5E7EB !important; opacity: 1 !important; }
table { width:100%; border-collapse:collapse; border-radius:10px; overflow:hidden; }
th { background:#1B168C; color:#FFFFFF; text-align:center; padding:10px; }
td { text-align:center; padding:8px; border-bottom:1px solid #E5E7EB; color:#000000; }
tr:nth-child(even){ background:#F9FAFB; } tr:hover{ background:#F43B63; color:#FFFFFF; }
.stAlert p, .stAlert span, .stAlert div { color: #000000 !important; font-weight: 600 !important; }
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
# 💬 MENSAJE DE BIENVENIDA
# ============================
st.markdown("<h1>💬 Hola, soy Chris</h1>", unsafe_allow_html=True)
st.markdown("""
<div class="intro-text">
Soy tu <span class="highlight">Asistente Virtual IA</span> de <b>Contacto Solutions</b>, aliado estratégico de <b>Banco Serfinanza</b>.<br>
Estoy aquí para brindarte información de tus productos y opciones de negociación.
</div>
""", unsafe_allow_html=True)

# ============================
# 🚀 BOTÓN INICIAR
# ============================
col1, col2, col3 = st.columns([1, 2.4, 1])
with col2:
    if st.button("🚀 INICIAR CHATBOT"):
        st.session_state["start_chat"] = True

# ============================
# FUNCIÓN NORMALIZAR ESTRATEGIAS
# ============================
def estrategia_base_label(valor: str) -> str:
    if not isinstance(valor, str): return ""
    v = valor.strip().upper()
    if v.startswith("REDIFERIDO"): return "REDIFERIDO"
    if v.startswith("REESTRUCTURACION") or v.startswith("REESTRUCTURACIÓN"): return "REESTRUCTURACIÓN"
    if v.startswith("PRORROGA") or v.startswith("PRÓRROGA"): return "PRÓRROGA"
    if v.startswith("ABONAR"): return "CANCELACIÓN DEL PAGO MÍNIMO"
    return valor

# ============================
# 💡 OFRECIMIENTO (COMPATIBLE con textos parciales)
# ============================
def mensaje_ofrecimiento_por_estrategia(estrategia_texto, nombre, producto, cuenta, saldo, tasa, abono, pago_min, color):
    et = (estrategia_texto or "").upper().strip()
    mensajes = {
        "REDIFERIDO CON PAGO": f"{nombre}, Banco Serfinanza te invita a ampliar el plazo del saldo total del capital, "
                               f"no incluye intereses y otros conceptos de tu <b>{producto}</b> terminada en <b>{cuenta}</b> "
                               f"por valor de <b>{saldo}</b> con una tasa del <b>{tasa}</b>. "
                               f"Realiza un abono de <b>{abono}</b> para aplicar la alternativa, respondiendo con la letra respectiva "
                               "acorde con el número de cuotas que deseas: A: 12 cuotas, B: 24 cuotas, C: 36 cuotas, D: 48 cuotas, E: 60 cuotas, F: No estoy interesado.",
        "REDIFERIDO SIN PAGO": f"{nombre}, Banco Serfinanza te invita a ampliar el plazo del saldo total del capital, "
                               f"no incluye intereses y otros conceptos de tu <b>{producto}</b> terminada en <b>{cuenta}</b> "
                               f"por valor de <b>{saldo}</b> con una tasa del <b>{tasa}</b>. "
                               "Responde con la letra respectiva acorde con el número de cuotas que deseas: A: 12 cuotas, B: 24 cuotas, C: 36 cuotas, D: 48 cuotas, E: 60 cuotas, F: No estoy interesado.",
        "REESTRUCTURACION CON PAGO": f"{nombre}, Banco Serfinanza te invita a reestructurar el plazo del saldo total del capital, "
                                     f"no incluye intereses y otros conceptos de tu <b>{producto}</b> terminada en <b>{cuenta}</b> "
                                     f"por valor de <b>{saldo}</b> con una tasa del <b>{tasa}</b>. "
                                     f"Realiza un abono de <b>{abono}</b> para aplicar la alternativa, respondiendo con la letra respectiva "
                                     "acorde con el número de cuotas que deseas: A: 12 cuotas, B: 24 cuotas, C: 36 cuotas, D: 48 cuotas, E: 60 cuotas, F: No estoy interesado.",
        "REESTRUCTURACION SIN PAGO": f"{nombre}, Banco Serfinanza te invita a reestructurar el plazo del saldo total del capital, "
                                     f"no incluye intereses y otros conceptos de tu <b>{producto}</b> terminada en <b>{cuenta}</b> "
                                     f"por valor de <b>{saldo}</b> con una tasa del <b>{tasa}</b>. "
                                     "Responde con la letra respectiva acorde con el número de cuotas que deseas: A: 12 cuotas, B: 24 cuotas, C: 36 cuotas, D: 48 cuotas, E: 60 cuotas, F: No estoy interesado.",
        "PRORROGA SIN PAGO": f"{nombre}, Banco Serfinanza te invita a diferir el capital de tu pago mínimo por valor de <b>{pago_min}</b> "
                              f"de tu <b>{producto}</b> terminada en <b>{cuenta}</b> con una tasa del <b>{tasa}</b>, "
                              "los intereses y otros conceptos serán diferidos a 12 meses al 0%. "
                              "Responde con la letra respectiva acorde con el número de cuotas que deseas: A: 12 cuotas, B: 24 cuotas, C: 36 cuotas.",
        "PRORROGA CON PAGO": f"{nombre}, Banco Serfinanza te invita a diferir el capital de tu pago mínimo por valor de <b>{pago_min}</b> "
                              f"de tu <b>{producto}</b> terminada en <b>{cuenta}</b> con una tasa del <b>{tasa}</b>, "
                              "los intereses y otros conceptos serán diferidos a 12 meses al 0%. "
                              f"Realiza un abono de <b>{abono}</b> y responde con la letra respectiva acorde con el número de cuotas que deseas: A: 12 cuotas, B: 24 cuotas, C: 36 cuotas."
    }

    # Coincidencia flexible
    clave = None
    for k in mensajes.keys():
        if k in et or k.split()[0] in et:
            clave = k
            break

    cuerpo = mensajes.get(clave, f"{nombre}, Banco Serfinanza te ofrece una alternativa sobre tu <b>{producto}</b> terminada en <b>{cuenta}</b>.")

    return f"""
    <div style='padding:20px; background:#FFFFFF; border-radius:15px; border:2px solid {color};
    box-shadow:0 4px 12px rgba(27,22,140,0.15); margin-top:10px;'>
        <div style='font-size:1.1em; color:{color}; font-weight:700;'>💡 Alternativa disponible</div>
        <div style='margin-top:10px; font-size:1em; line-height:1.6em; color:#333;'>{cuerpo}</div>
    </div>
    """

# ============================
# ✅ CONFIRMACIONES (COMPATIBLE también con textos parciales)
# ============================
def mensaje_confirmacion_por_estrategia(estrategia_texto, cuotas_txt, producto, cuenta, tasa, color):
    et = (estrategia_texto or "").upper().strip()
    cuotas_num = (cuotas_txt or "").replace(" cuotas", "").strip()

    if "REDIFERIDO" in et and "CON" in et:
        cuerpo = (f"Tu solicitud de la ampliación de plazo al saldo capital a <b>{cuotas_num} cuotas</b> en tu <b>{producto}</b> "
                  f"terminada en <b>{cuenta}</b> ha sido registrada exitosamente, la tasa será del <b>{tasa}</b> "
                  "y cuando se realice el abono acordado. Consulta términos y condiciones en la página web del Banco Serfinanza.")
    elif "REDIFERIDO" in et:
        cuerpo = (f"Tu solicitud de la ampliación de plazo al saldo capital a <b>{cuotas_num} cuotas</b> en tu <b>{producto}</b> "
                  f"terminada en <b>{cuenta}</b> ha sido registrada exitosamente, la tasa será del <b>{tasa}</b>. "
                  "Consulta términos y condiciones en la página web del Banco Serfinanza.")
    elif "REESTRUCTURACION" in et and "CON" in et:
        cuerpo = (f"Tu solicitud de reestructuración de plazo al saldo capital a <b>{cuotas_num} cuotas</b> en tu <b>{producto}</b> "
                  f"terminada en <b>{cuenta}</b> ha sido registrada exitosamente, la tasa será la vigente del producto al momento de aplicar el beneficio "
                  "y cuando se realice el abono acordado. La obligación quedará marcada como reestructurada ante las centrales de riesgo, "
                  "consulta términos y condiciones en la página web del Banco Serfinanza.")
    elif "REESTRUCTURACION" in et:
        cuerpo = (f"Tu solicitud de reestructuración de plazo al saldo capital a <b>{cuotas_num} cuotas</b> en tu <b>{producto}</b> "
                  f"terminada en <b>{cuenta}</b> ha sido registrada exitosamente, la tasa será la vigente del producto al momento de aplicar el beneficio. "
                  "La obligación quedará marcada como reestructurada ante las centrales de riesgo, consulta términos y condiciones en la página web del Banco Serfinanza.")
    elif "PRORROGA" in et and "CON" in et:
        cuerpo = (f"Tu solicitud de diferido del capital de tu pago mínimo a <b>{cuotas_num} cuotas</b> en tu <b>{producto}</b> "
                  f"terminada en <b>{cuenta}</b> ha sido registrada exitosamente siempre y cuando se realice el abono acordado, "
                  f"la tasa será del <b>{tasa}</b>, consulta términos y condiciones en la página web del Banco Serfinanza.")
    elif "PRORROGA" in et:
        cuerpo = (f"Tu solicitud de diferido del capital de tu pago mínimo a <b>{cuotas_num} cuotas</b> en tu <b>{producto}</b> "
                  f"terminada en <b>{cuenta}</b> ha sido registrada exitosamente, la tasa será del <b>{tasa}</b>, "
                  "consulta términos y condiciones en la página web del Banco Serfinanza.")
    else:
        cuerpo = "Tu solicitud fue registrada exitosamente. Consulta términos y condiciones en la página web del Banco Serfinanza."

    return f"""
    <div style='padding:20px; background:#FFFFFF; border-radius:15px; border:2px solid {color};
    box-shadow:0 4px 12px rgba(27,22,140,0.15); margin-top:10px;'>
        <div style='font-size:1.1em; color:{color}; font-weight:700;'>✅ Confirmación registrada</div>
        <div style='margin-top:10px; font-size:1em; line-height:1.6em; color:#333;'>{cuerpo}</div>
    </div>
    """
