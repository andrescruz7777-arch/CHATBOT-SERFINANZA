import streamlit as st
import pandas as pd

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
# 🎨 ESTILOS CORPORATIVOS
# ============================
st.markdown("""
<style>
/* ===========================
   🎨 ESTILOS GLOBALES
=========================== */
html, body, .stApp, [data-testid="stAppViewContainer"] {
    background-color: #FFFFFF !important;
    color: #1B168C !important;
}

/* CABECERA */
.header-container {
    display: flex; 
    justify-content: space-between; 
    align-items: center; 
    padding: 0 2rem;
}

/* TITULOS */
h1, h2, h3 { 
    color: #1B168C !important; 
    text-align: center; 
}

/* TEXTO INICIAL */
.intro-text {
    text-align: center;
    font-size: 1.15em;
    font-weight: 500;
    line-height: 1.6em;
    margin-top: 15px;
    color: #1B168C !important;
}
.highlight { 
    color: #F43B63; 
    font-weight: 600; 
}

/* ===========================
   🟦 BOTONES
=========================== */
div.stButton > button, 
form button[kind="primary"] {
    background-color:#1B168C !important;
    color:#FFFFFF !important;           /* 🔹 Texto blanco */
    border:none;
    border-radius:12px !important;
    padding:16px 60px !important;
    font-size:1.1em !important;
    font-weight:600 !important;
    cursor:pointer;
    transition:all .3s ease !important;
    box-shadow:0 4px 15px rgba(27,22,140,.3) !important;
}
div.stButton > button:hover, 
form button[kind="primary"]:hover {
    background-color:#F43B63 !important;
    color:#FFFFFF !important;
    box-shadow:0 0 20px rgba(244,59,99,.7) !important;
    transform:scale(1.05);
}

/* ===========================
   🪪 CAMPO DE CÉDULA
=========================== */
label, 
.stTextInput label {
    color: #1B168C !important;
    font-weight: 700 !important;
}

.stTextInput > div > div {
    background-color: #1B168C !important;
    border: 2px solid #F43B63 !important;
    border-radius: 10px !important;
}

.stTextInput > div > div > input {
    background-color: transparent !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    border: none !important;
    box-shadow: none !important;
}

.stTextInput input::placeholder {
    color: #E5E7EB !important;
    opacity: 1 !important;
}

/* ===========================
   📊 TABLA
=========================== */
table { 
    width:100%; 
    border-collapse:collapse; 
    border-radius:10px; 
    overflow:hidden; 
}
th { 
    background:#1B168C; 
    color:#FFFFFF; 
    text-align:center; 
    padding:10px; 
}
td { 
    text-align:center; 
    padding:8px; 
    border-bottom:1px solid #E5E7EB; 
    color:#000000; 
}
tr:nth-child(even){ 
    background:#F9FAFB; 
}
tr:hover{ 
    background:#F43B63; 
    color:#FFFFFF; 
    transition:.2s; 
}

/* ===========================
   ⚠️ MENSAJES (WARNING / ERROR / SUCCESS)
=========================== */
.stAlert, .st-emotion-cache-ue6h4q, .st-emotion-cache-1wivap2 {
    color: #000000 !important;        /* Texto negro */
    font-weight: 600 !important;
}
.stAlert p, .stAlert span, .stAlert div {
    color: #000000 !important;        /* Texto negro también dentro */
}

/* Ajuste para íconos de alerta */
.st-emotion-cache-1wbqy5l, .st-emotion-cache-1avcm0n {
    color: #000000 !important;
}
</style>
""", unsafe_allow_html=True)


/* ===========================
   🟦 BOTONES
=========================== */
div.stButton > button, 
form button[kind="primary"] {
    background-color:#1B168C !important;
    color:#FFFFFF !important;           /* 🔹 Texto blanco */
    border:none;
    border-radius:12px !important;
    padding:16px 60px !important;
    font-size:1.1em !important;
    font-weight:600 !important;
    cursor:pointer;
    transition:all .3s ease !important;
    box-shadow:0 4px 15px rgba(27,22,140,.3) !important;
}
div.stButton > button:hover, 
form button[kind="primary"]:hover {
    background-color:#F43B63 !important;
    color:#FFFFFF !important;           /* 🔹 Texto blanco al pasar el mouse */
    box-shadow:0 0 20px rgba(244,59,99,.7) !important;
    transform:scale(1.05);
}

/* ===========================
   🪪 CAMPOS DE TEXTO (CÉDULA)
=========================== */
label, 
.stTextInput label {
    color: #1B168C !important;  /* 🔹 Azul institucional */
    font-weight: 700 !important;
}

.stTextInput > div > div {
    background-color: #1B168C !important; /* 🔹 Fondo azul */
    border: 2px solid #F43B63 !important; /* 🔹 Borde rosado */
    border-radius: 10px !important;
}

.stTextInput > div > div > input {
    background-color: transparent !important;
    color: #FFFFFF !important;            /* 🔹 Texto blanco */
    font-weight: 600 !important;
    border: none !important;
    box-shadow: none !important;
}

.stTextInput input::placeholder {
    color: #E5E7EB !important;
    opacity: 1 !important;
}

/* ===========================
   📊 TABLA
=========================== */
table { 
    width:100%; 
    border-collapse:collapse; 
    border-radius:10px; 
    overflow:hidden; 
}
th { 
    background:#1B168C; 
    color:#FFFFFF; 
    text-align:center; 
    padding:10px; 
}
td { 
    text-align:center; 
    padding:8px; 
    border-bottom:1px solid #E5E7EB; 
    color:#000000; 
}
tr:nth-child(even){ 
    background:#F9FAFB; 
}
tr:hover{ 
    background:#F43B63; 
    color:#FFFFFF; 
    transition:.2s; 
}

/* ===========================
   ⚠️ MENSAJES (INFO / WARNING / ERROR)
=========================== */
[data-baseweb="toast"] div, 
div[data-testid="stNotification"] p, 
div[data-testid="stNotification"] span {
    color: #000000 !important;     /* 🔹 Texto negro */
    font-weight: 600 !important;
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
            cedula = st.text_input(
                "🪪 Digita tu número de cédula (sin puntos ni caracteres especiales):",
                key="cedula_input"
            )
            submitted = st.form_submit_button("➡️ Continuar")

            # Validación obligatoria antes de procesar
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
    obligaciones_vista["Pago mínimo mes ($)"] = pd.to_numeric(
        obligaciones_vista["Pago mínimo mes ($)"], errors="coerce"
    ).fillna(0).map("${:,.0f}".format)

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
    saldo = f"${obligacion_sel.get('ULTIMO_SALDO_CAPITAL', 0):,.0f}"
    tasa = obligacion_sel.get("TASA", "según condiciones vigentes")
    abono = f"${obligacion_sel.get('VALOR_ABONO', 0):,.0f}"
    pago_minimo = f"${obligacion_sel.get('PAGO_MINIMO_MES', 0):,.0f}"
    color = "#1B168C" if "SIN PAGO" in estrategia else "#F43B63"

    # ============= MENSAJE OFRECIMIENTO ============
    mensajes = {
        "REDIFERIDO CON PAGO": f"""{nombre} Banco Serfinanza te invita a ampliar el plazo del saldo total del capital, no incluye intereses y otros conceptos de tu {producto} terminada en {cuenta} por valor de {saldo} con una tasa del {tasa}. Realiza un abono de {abono} para aplicar la alternativa, respondiendo con la letra respectiva acorde con el número de cuotas que deseas:
        A: 12 cuotas, B: 24 cuotas, C: 36 cuotas, D: 48 cuotas, E: 60 cuotas, F: No estoy interesado.""",
        "REDIFERIDO SIN PAGO": f"""{nombre} Banco Serfinanza te invita a ampliar el plazo del saldo total del capital, no incluye intereses y otros conceptos de tu {producto} terminada en {cuenta} por valor de {saldo} con una tasa del {tasa}. Respondiendo con la letra respectiva acorde con el número de cuotas que deseas:
        A: 12 cuotas, B: 24 cuotas, C: 36 cuotas, D: 48 cuotas, E: 60 cuotas, F: No estoy interesado.""",
        "REESTRUCTURACION CON PAGO": f"""{nombre} Banco Serfinanza te invita a reestructurar el plazo del saldo total del capital, no incluye intereses y otros conceptos de tu {producto} terminada en {cuenta} por valor de {saldo} con una tasa del {tasa}. Realiza un abono de {abono} para aplicar la alternativa, respondiendo con la letra respectiva acorde con el número de cuotas que deseas:
        A: 12 cuotas, B: 24 cuotas, C: 36 cuotas, D: 48 cuotas, E: 60 cuotas, F: No estoy interesado.""",
        "REESTRUCTURACION SIN PAGO": f"""{nombre} Banco Serfinanza te invita a reestructurar el plazo del saldo total del capital, no incluye intereses y otros conceptos de tu {producto} terminada en {cuenta} por valor de {saldo} con una tasa del {tasa}. Respondiendo con la letra respectiva acorde con el número de cuotas que deseas:
        A: 12 cuotas, B: 24 cuotas, C: 36 cuotas, D: 48 cuotas, E: 60 cuotas, F: No estoy interesado.""",
        "PRORROGA SIN PAGO": f"""{nombre} Banco Serfinanza te invita a diferir el capital de tu pago mínimo por valor de {pago_minimo} de tu {producto} terminada en {cuenta} con una tasa del {tasa}, los intereses y otros conceptos serán diferidos a 12 meses al 0%. Respondiendo con la letra respectiva acorde con el número de cuotas que deseas A: 12 cuotas, B: 24 cuotas, C: 36 cuotas.""",
        "PRORROGA CON PAGO": f"""{nombre} Banco Serfinanza te invita a diferir el capital de tu pago mínimo por valor de {pago_minimo} de tu {producto} terminada en {cuenta} con una tasa del {tasa}, los intereses y otros conceptos serán diferidos a 12 meses al 0%. Realiza un abono de {abono} respondiendo con la letra respectiva acorde con el número de cuotas que deseas A: 12 cuotas, B: 24 cuotas, C: 36 cuotas."""
    }

    mensaje = mensajes.get(estrategia, f"{nombre}, tu obligación no cuenta con una alternativa activa de negociación en este momento.")

    st.markdown(f"""
    <div style='padding:20px; background:#FFFFFF; border-radius:15px; border:2px solid {color};
    box-shadow:0 4px 12px rgba(27,22,140,0.15); margin-top:10px;'>
        <div style='font-size:1.1em; color:{color}; font-weight:700;'>💡 Alternativa disponible</div>
        <div style='margin-top:10px; font-size:1em; line-height:1.6em; color:#333;'>{mensaje}</div>
    </div>
    """, unsafe_allow_html=True)

    # ============= DESPLEGABLE Y CONFIRMACIÓN ============
    cuotas = ["Selecciona una opción...", "12 cuotas", "24 cuotas", "36 cuotas", "48 cuotas", "60 cuotas", "No estoy interesado"]
    seleccion_cuota = st.selectbox("📆 Selecciona una opción:", cuotas, index=0, key="cuota_tmp")

    if seleccion_cuota not in ["Selecciona una opción...", "No estoy interesado"]:
        confirmaciones = {
            "REDIFERIDO CON PAGO": f"Tu solicitud de la ampliación de plazo al saldo capital a {seleccion_cuota} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente, la tasa será del {tasa} y cuando se realice el abono acordado. Consulta términos y condiciones en la página web del Banco Serfinanza.",
            "REDIFERIDO SIN PAGO": f"Tu solicitud de la ampliación de plazo al saldo capital a {seleccion_cuota} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente, la tasa será del {tasa}. Consulta términos y condiciones en la página web del Banco Serfinanza.",
            "REESTRUCTURACION CON PAGO": f"Tu solicitud de reestructuración de plazo al saldo capital a {seleccion_cuota} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente, la tasa será la vigente del producto al momento de aplicar el beneficio y cuando se realice el abono acordado. La obligación quedará marcada como reestructurada ante las centrales de riesgo.",
            "REESTRUCTURACION SIN PAGO": f"Tu solicitud de reestructuración de plazo al saldo capital a {seleccion_cuota} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente, la tasa será la vigente del producto al momento de aplicar el beneficio.",
            "PRORROGA SIN PAGO": f"Tu solicitud de diferido del capital de tu pago mínimo a {seleccion_cuota} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente, la tasa será del {tasa}.",
            "PRORROGA CON PAGO": f"Tu solicitud de diferido del capital de tu pago mínimo a {seleccion_cuota} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente siempre y cuando se realice el abono acordado, la tasa será del {tasa}."
        }

        confirm = confirmaciones.get(estrategia, "")
        st.markdown(f"""
        <div style='padding:20px; background:#FFFFFF; border-radius:15px; border:2px solid {color};
        box-shadow:0 4px 12px rgba(27,22,140,0.15); margin-top:10px;'>
            <div style='font-size:1.1em; color:{color}; font-weight:700;'>✅ Confirmación registrada</div>
            <div style='margin-top:10px; font-size:1em; line-height:1.6em; color:#333;'>{confirm}</div>
        </div>
        """, unsafe_allow_html=True)
    elif seleccion_cuota == "No estoy interesado":
        st.warning("ℹ️ Entendido, no estás interesado en esta alternativa por ahora.")

