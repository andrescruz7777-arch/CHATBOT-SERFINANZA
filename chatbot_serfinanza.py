import streamlit as st
import pandas as pd
import requests
from openai import OpenAI
from datetime import datetime
import base64
import json

# ============================
# ⚙️ CONFIGURACIÓN INICIAL
# ============================
st.set_page_config(page_title="💬 Chatbot IA - Banco Serfinanza", layout="centered")

if "start_chat" not in st.session_state:
    st.session_state["start_chat"] = False
if "cedula_validada" not in st.session_state:
    st.session_state["cedula_validada"] = False
if "intentos" not in st.session_state:
    st.session_state["intentos"] = 0
if "cuota_elegida" not in st.session_state:
    st.session_state["cuota_elegida"] = None

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
.intro-text { text-align: center; font-size: 1.15em; font-weight: 500; line-height: 1.6em;
    margin-top: 15px; color: #1B168C !important; }
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
    tasa = obligacion_sel.get("TASA", "según condiciones vigentes")
    color = "#1B168C" if "SIN PAGO" in estrategia else "#F43B63"

    # ============================
    # 💡 ALTERNATIVA DISPONIBLE
    # ============================
    st.markdown(f"""
    <div style='padding:20px; background:#FFFFFF; border-radius:15px; border:2px solid {color};
    box-shadow:0 4px 12px rgba(27,22,140,0.15); margin-top:10px;'>
        <div style='font-size:1.1em; color:{color}; font-weight:700;'>💡 Alternativa disponible</div>
        <div style='margin-top:10px; font-size:1em; line-height:1.6em; color:#333;'>
            {nombre}, Banco Serfinanza te ofrece una alternativa sobre tu {producto} terminada en {cuenta}.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ============================
    # 📆 SELECCIÓN DE CUOTAS
    # ============================
    cuotas = ["Selecciona una opción...", "12 cuotas", "24 cuotas", "36 cuotas", "48 cuotas", "60 cuotas", "No estoy interesado"]
    seleccion_cuota = st.selectbox("📆 Selecciona una opción:", cuotas, index=0, key="cuota_tmp")

    # ============================
    # ✅ NEGOCIACIÓN
    # ============================
    if seleccion_cuota not in ["Selecciona una opción...", "No estoy interesado"]:
        confirm = f"Tu solicitud de negociación a {seleccion_cuota} fue registrada exitosamente. Consulta términos en la web de Banco Serfinanza."
        st.success(confirm)

        # 🔍 Obtener IP del cliente
        try:
            ip = requests.get("https://api.ipify.org?format=json").json()["ip"]
        except:
            ip = "No disponible"

        # 🧾 Crear registro local
        registro = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Cedula": cedula,
            "Nombre": nombre,
            "Producto": producto,
            "Cuenta": cuenta,
            "Estrategia": estrategia,
            "Cuotas": seleccion_cuota,
            "IP_Usuario": ip
        }])

        try:
            df_existente = pd.read_excel("logs_negociacion.xlsx")
            df_final = pd.concat([df_existente, registro], ignore_index=True)
        except:
            df_final = registro

        df_final.to_excel("logs_negociacion.xlsx", index=False)

        # 🚀 Subir a GitHub automáticamente
        import base64
        import requests

        with open("logs_negociacion.xlsx", "rb") as f:
            contenido = base64.b64encode(f.read()).decode()

        url = "https://api.github.com/repos/andrescruz7777-arch/CHATBOT-SERFINANZA/contents/logs_negociacion.xlsx"
        headers = {
            "Authorization": f"Bearer {st.secrets['GH_TOKEN']}",
            "Content-Type": "application/json"
        }

        data = {
            "message": f"📝 Actualización de logs de negociación - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "content": contenido,
            "branch": "main"
        }

        r = requests.put(url, headers=headers, data=json.dumps(data))
        if r.status_code in [200, 201]:
            st.success("✅ Registro actualizado en GitHub correctamente.")
        else:
            st.warning(f"⚠️ No se pudo subir a GitHub ({r.status_code}).")

