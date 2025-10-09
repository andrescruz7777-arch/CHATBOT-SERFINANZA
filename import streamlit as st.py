import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ============================
# ⚙️ CONFIGURACIÓN INICIAL
# ============================
st.set_page_config(page_title="💬 Chatbot IA - Banco Serfinanza", layout="centered")

if "start_chat" not in st.session_state:
    st.session_state["start_chat"] = False
if "cliente" not in st.session_state:
    st.session_state["cliente"] = None

# ============================
# 🎨 ESTILOS CORPORATIVOS Y ANIMACIÓN
# ============================
st.markdown("""
<style>
/* Fondo blanco global */
html, body, [class*="stAppViewContainer"], [class*="stMainBlockContainer"], .stApp {
    background-color: #FFFFFF !important;
    color: #1B168C !important;
}

/* Tipografía general */
*, p, span, div, label {
    color: #1B168C !important;
    font-family: 'Segoe UI', sans-serif !important;
}

/* Encabezados */
h1, h2, h3 {
    color: #1B168C !important;
    text-align: center !important;
    font-weight: 700 !important;
}

/* Contenedor logos */
.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 2rem;
}

/* Texto bienvenida */
.intro-text {
    text-align: center;
    font-size: 1.15em;
    line-height: 1.6em;
    margin-top: 15px;
    color: #1B168C !important;
}
.highlight { color: #F43B63 !important; font-weight: 600; }

/* === BOTÓN PRINCIPAL === */
div.stButton > button {
    background-color: #1B168C !important;
    color: white !important;
    border: none !important;
    border-radius: 18px !important;
    padding: 16px 70px !important;
    font-size: 1.1em !important;
    font-weight: 600 !important;
    box-shadow: 0 6px 18px rgba(27,22,140,0.3) !important;
    transition: all 0.3s ease !important;
    animation: bounce 3s infinite ease-in-out;
}
div.stButton > button:hover {
    background-color: #F43B63 !important;
    box-shadow: 0 0 25px rgba(244,59,99,0.6) !important;
    transform: scale(1.05);
}

/* Animación rebote */
@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-3px); }
}

/* Botón de formularios */
form button {
    background-color: #1B168C !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    border: none !important;
    box-shadow: 0 4px 10px rgba(27,22,140,.3) !important;
}
form button:hover {
    background-color: #F43B63 !important;
}

/* === CAMPOS === */
input[type="text"], [data-baseweb="select"] div {
    background-color: white !important;
    color: #1B168C !important;
    border: 2px solid #1B168C !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* === TABLA === */
.tabla-ob table {
    width: 100%;
    border-collapse: collapse;
    border-radius: 10px;
    overflow: hidden;
    background: #FFFFFF !important;
}
.tabla-ob th {
    background: #1B168C !important;
    color: #FFFFFF !important;
    text-align: center;
    padding: 10px;
}
.tabla-ob td {
    text-align: center;
    padding: 8px;
    color: #333333 !important;
    border-bottom: 1px solid #E5E7EB !important;
}
.tabla-ob tr:nth-child(even) td { background: #F3F4F6 !important; }
.tabla-ob tr:hover td {
    background: #F43B63 !important;
    color: #FFFFFF !important;
    transition: .2s;
}

/* === TARJETAS === */
.alternativa {
    padding: 20px;
    background: #FFFFFF;
    border-radius: 15px;
    border: 2px solid var(--color);
    box-shadow: 0 4px 12px rgba(27,22,140,0.15);
    margin-top: 15px;
}
.confirmacion {
    margin-top: 20px;
    padding: 18px;
    border-radius: 12px;
    background: #FFFFFF;
    border: 2px solid var(--color);
    color: #1B168C;
    font-size: 1em;
    line-height: 1.6em;
    box-shadow: 0 4px 10px rgba(27,22,140,0.1);
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
# 💬 BIENVENIDA
# ============================
st.markdown("<h1>💬 Hola, soy Andrés</h1>", unsafe_allow_html=True)
st.markdown("""
<div class="intro-text">
Soy tu <span class="highlight">Asistente Virtual IA</span> de <b>Contacto Solutions</b>, aliado estratégico de <b>Banco Serfinanza</b>.<br>
Estoy aquí para brindarte información de tus productos y opciones de negociación.
</div>
""", unsafe_allow_html=True)

# ============================
# 🚀 INICIO
# ============================
c1, c2, c3 = st.columns([1, 2.4, 1])
with c2:
    if st.button("🚀 INICIAR CHATBOT"):
        st.session_state["start_chat"] = True

# ============================
# MAPEO DE ALTERNATIVAS
# ============================
def map_alternativa(v: str) -> str:
    if not isinstance(v, str):
        return ""
    v = v.strip().upper()
    if "REDIFERIDO" in v:
        return "REDIFERIDO"
    if "REESTRUCTURACION" in v or "REESTRUCTURACIÓN" in v:
        return "REESTRUCTURACIÓN"
    if "PRORROGA" in v or "PRÓRROGA" in v:
        return "PRÓRROGA"
    if "ABONAR" in v:
        return "CANCELACIÓN DEL PAGO MÍNIMO"
    return v

# ============================
# 🔍 VALIDACIÓN DE CÉDULA
# ============================
if st.session_state["start_chat"]:
    st.markdown("<hr><br>", unsafe_allow_html=True)
    st.subheader("🔍 Verificación de identidad")

    c1, c2, c3 = st.columns([1, 1.6, 1])
    with c2:
        with st.form("form_cedula", clear_on_submit=False):
            cedula = st.text_input("🪪 Ingresa tu número de cédula:", key="cedula_input")
            submit = st.form_submit_button("➡️ Continuar")

    if submit and cedula:
        try:
            data = pd.read_excel("base_bot_serfinanza.xls")
        except Exception as e:
            st.error(f"Error cargando base: {e}")
            st.stop()

        cliente = data[data["NUMERO_IDENTIFICACION"].astype(str) == cedula.strip()]
        if cliente.empty:
            st.warning("⚠️ No se encontró el número ingresado. Verifica e inténtalo nuevamente.")
        else:
            st.session_state["cliente"] = cliente

# ============================
# 📋 OBLIGACIONES
# ============================
if st.session_state["cliente"] is not None:
    cliente = st.session_state["cliente"]
    nombre = str(cliente["NOMBRE_FINAL"].iloc[0]).title()
    obligaciones = cliente.copy()
    total = len(obligaciones)

    st.success(f"✅ Hola {nombre}, encontramos {total} obligación{'es' if total>1 else ''} asociada{'s' if total>1 else ''}.")

    # Tabla
    cols_vis = ["ULTIMOS_CUENTA","TIPO_PRODUCTO","PAGO_MINIMO_MES","MORA_ACTUAL","ESTRATEGIA_ACTUAL"]
    vista = obligaciones[cols_vis].rename(columns={
        "ULTIMOS_CUENTA":"Últimos dígitos",
        "TIPO_PRODUCTO":"Producto",
        "PAGO_MINIMO_MES":"Pago mínimo ($)",
        "MORA_ACTUAL":"Mora (días)",
        "ESTRATEGIA_ACTUAL":"Alternativa"
    })
    vista["Alternativa"] = vista["Alternativa"].apply(map_alternativa)
    vista["Pago mínimo ($)"] = pd.to_numeric(vista["Pago mínimo ($)"], errors="coerce").fillna(0).map(lambda x: f"$ {x:,.0f}")
    st.markdown(f"<div class='tabla-ob'>{vista.to_html(index=False)}</div>", unsafe_allow_html=True)

    # Selección
    opciones = [f"{r['Producto']} (****{r['Últimos dígitos']})" for _, r in vista.iterrows()]
    seleccion = opciones[0] if len(opciones) == 1 else st.selectbox("🤝 ¿Qué obligación deseas negociar?", opciones)

    obligacion = obligaciones.iloc[opciones.index(seleccion)]
    estrategia = obligacion["ESTRATEGIA_ACTUAL"].strip().upper()
    producto = obligacion["TIPO_PRODUCTO"]
    cuenta = obligacion["ULTIMOS_CUENTA"]
    tasa = obligacion.get("TASA","según condiciones vigentes")
    abono = f"${obligacion.get('VALOR_ABONO',0):,.0f}"
    saldo = f"${obligacion.get('ULTIMO_SALDO_CAPITAL',0):,.0f}"
    pago_min = f"${obligacion.get('PAGO_MINIMO_MES',0):,.0f}"
    color = "#F43B63" if "CON PAGO" in estrategia else "#1B168C"

    st.markdown(
        f"<div class='alternativa' style='--color:{color}'>"
        f"<div style='font-weight:700;color:{color};font-size:1.05em'>💡 Alternativa disponible</div>"
        f"<div style='margin-top:10px;font-size:1em;color:#333'>{nombre}, Banco Serfinanza te invita a la alternativa {map_alternativa(estrategia)} de tu {producto} terminada en {cuenta}. Selecciona tu opción de plazo.</div>"
        f"</div>",
        unsafe_allow_html=True
    )

    cuotas = ["Selecciona una opción...", "A: 12 cuotas", "B: 24 cuotas", "C: 36 cuotas"]
    if "PRORROGA" not in estrategia:
        cuotas += ["D: 48 cuotas", "E: 60 cuotas", "F: No estoy interesado"]
    seleccion_cuota = st.selectbox("📆 Selecciona una opción:", cuotas, index=0)

    if seleccion_cuota != "Selecciona una opción..." and seleccion_cuota != "F: No estoy interesado":
        _, cuota_txt = seleccion_cuota.split(":")
        cuota_txt = cuota_txt.strip()
        confirmacion = f"Tu solicitud de {map_alternativa(estrategia).lower()} a {cuota_txt} ha sido registrada exitosamente. La tasa será del {tasa}."
        st.markdown(f"<div class='confirmacion' style='--color:{color}'><b>✅ Confirmación registrada:</b><br>{confirmacion}</div>", unsafe_allow_html=True)

        registro = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Cédula": cliente["NUMERO_IDENTIFICACION"].iloc[0],
            "Nombre": nombre,
            "Producto": producto,
            "Cuenta": cuenta,
            "Alternativa": map_alternativa(estrategia),
            "Cuota seleccionada": cuota_txt,
            "Confirmación": confirmacion
        }])
        path = "confirmaciones_chatbot.xlsx"
        if os.path.exists(path):
            prev = pd.read_excel(path)
            registro = pd.concat([prev, registro], ignore_index=True)
        registro.to_excel(path, index=False)
        st.success("💾 Registro guardado exitosamente en confirmaciones_chatbot.xlsx")

    elif seleccion_cuota == "F: No estoy interesado":
        st.warning("ℹ️ Entendido, no estás interesado en esta alternativa por ahora.")
