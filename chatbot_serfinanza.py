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
# 🔧 FUNCIONES AUXILIARES
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
    """Guarda un registro en logs_negociacion.xlsx (Bogotá, últimos 4, orden exacto)"""
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
# 🎨 ESTILOS CORPORATIVOS
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
# 🔍 VALIDACIÓN DE CÉDULA
# ============================
if st.session_state["start_chat"]:
    st.markdown("<hr><br>", unsafe_allow_html=True)
    st.subheader("🔍 Verificación de identidad")

    c1, c2, c3 = st.columns([1, 1.6, 1])
    with c2:
        with st.form("form_cedula", clear_on_submit=False):
            cedula = st.text_input("🪪 Digita tu número de cédula (sin puntos ni caracteres especiales):", key="cedula_input")
            submitted = st.form_submit_button("➡️ Continuar")
            if submitted and not cedula.strip():
                st.warning("⚠️ Por favor ingresa tu número de cédula antes de continuar.")
                st.stop()

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
    obligaciones_cliente = cliente.copy()
    total_obligaciones = len(obligaciones_cliente)
    nombre_cliente = str(obligaciones_cliente["NOMBRE_FINAL"].iloc[0]).title()

    st.markdown(f"### 👋 Hola {nombre_cliente}, actualmente cuentas con **{total_obligaciones} obligación{'es' if total_obligaciones>1 else ''}** registradas.")
    st.markdown("A continuación te presento el estado de cada una 👇")

    cols_vis = ["ULTIMOS_CUENTA","TIPO_PRODUCTO","PAGO_MINIMO_MES","MORA_ACTUAL","ESTRATEGIA_ACTUAL"]
    obligaciones_vista = obligaciones_cliente[cols_vis].rename(columns={
        "ULTIMOS_CUENTA":"Últimos dígitos",
        "TIPO_PRODUCTO":"Producto",
        "PAGO_MINIMO_MES":"Pago mínimo mes ($)",
        "MORA_ACTUAL":"Mora (días)",
        "ESTRATEGIA_ACTUAL":"Alternativa"
    })
    obligaciones_vista["Alternativa"] = obligaciones_vista["Alternativa"].apply(estrategia_base_label)
    obligaciones_vista["Pago mínimo mes ($)"] = pd.to_numeric(obligaciones_vista["Pago mínimo mes ($)"], errors="coerce").fillna(0).map("${:,.0f}".format)
    st.markdown(obligaciones_vista.to_html(index=False, escape=False), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🤝 ¿Qué obligación deseas negociar?")

    opciones = [f"{row['Producto']} ({row['Últimos dígitos']})" for _, row in obligaciones_vista.iterrows()]
    seleccion = st.selectbox("Selecciona una opción:", opciones, key="obligacion_seleccionada")

    obligacion_sel = obligaciones_cliente.iloc[opciones.index(seleccion)]
    estrategia = obligacion_sel["ESTRATEGIA_ACTUAL"].strip().upper()
    nombre = str(obligacion_sel["NOMBRE_FINAL"]).title()
    producto = obligacion_sel["TIPO_PRODUCTO"]
    cuenta = obligacion_sel["ULTIMOS_CUENTA"]
    color = "#1B168C" if "SIN PAGO" in estrategia else "#F43B63"

    cuotas = ["Selecciona una opción...", "12 cuotas", "24 cuotas", "36 cuotas", "48 cuotas", "60 cuotas", "No estoy interesado"]
    seleccion_cuota = st.selectbox("📆 Selecciona una opción:", cuotas, index=0, key="cuota_tmp")

    if seleccion_cuota not in ["Selecciona una opción...", "No estoy interesado"]:
        confirm = f"Tu solicitud de negociación a {seleccion_cuota} fue registrada exitosamente."
        st.success(confirm)
        ip, ciudad, region, pais = get_ip_geo()
        save_log({
            "Cedula": cedula, "Nombre": nombre, "Producto": producto,
            "Estrategia": estrategia, "Cuotas": seleccion_cuota,
            "Cuenta": cuenta, "IP": ip, "Ciudad": ciudad,
            "Region": region, "Pais": pais, "IP_Usuario": ip,
            "MensajeUsuario": "", "RespuestaIA": ""
        })

    elif seleccion_cuota == "No estoy interesado":
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []
        for msg in st.session_state["chat_history"]:
            if msg["role"] == "user":
                st.markdown(f"<div style='text-align:right;'><div style='display:inline-block; background:#F43B63; color:white; padding:10px 14px; border-radius:15px;'>{msg['content']}</div></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align:left;'><div style='display:inline-block; background:#FFF; color:#1B168C; border:1.8px solid #1B168C; padding:10px 14px; border-radius:15px;'>{msg['content']}</div></div>", unsafe_allow_html=True)

        user_msg = st.chat_input("✍️ Escribe tus dudas o inquietudes aquí...")
        if user_msg:
            st.session_state["chat_history"].append({"role": "user", "content": user_msg})
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "Eres un asesor virtual empático del Banco Serfinanza."}, *st.session_state["chat_history"]]
            )
            ai_reply = response.choices[0].message.content
            st.session_state["chat_history"].append({"role": "assistant", "content": ai_reply})
            ip, ciudad, region, pais = get_ip_geo()
            save_log({
                "Cedula": cedula, "Nombre": nombre, "Producto": producto,
                "Estrategia": estrategia, "Cuotas": "Chat IA",
                "Cuenta": cuenta, "IP": ip, "Ciudad": ciudad,
                "Region": region, "Pais": pais, "IP_Usuario": ip,
                "MensajeUsuario": user_msg, "RespuestaIA": ai_reply
            })
            st.rerun()
