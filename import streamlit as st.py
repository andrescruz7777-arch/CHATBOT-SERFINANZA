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
if "intentos" not in st.session_state:
    st.session_state["intentos"] = 0
if "cliente" not in st.session_state:
    st.session_state["cliente"] = None
if "obligacion_sel" not in st.session_state:
    st.session_state["obligacion_sel"] = None

# ============================
# 🎨 ESTILOS INSTITUCIONALES
# ============================
st.markdown("""
<style>
body {
    background-color: #FFFFFF;
    color: #333333;
    font-family: "Helvetica", sans-serif;
}

/* Encabezado */
.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 2rem;
}
h1, h2, h3 {
    color: #1B168C;
    text-align: center;
}
.intro-text {
    text-align: center;
    font-size: 1.15em;
    line-height: 1.6em;
    margin-top: 15px;
    color: #1B168C;
}
.highlight {
    color: #F43B63;
    font-weight: 600;
}

/* Botones */
div.stButton > button {
    background-color:#1B168C !important;
    color:#fff !important;
    border:none;
    border-radius:12px !important;
    padding:16px 60px !important;
    font-size:1.1em !important;
    font-weight:600 !important;
    box-shadow:0 4px 15px rgba(27,22,140,0.3) !important;
}
div.stButton > button:hover {
    background-color:#F43B63 !important;
    box-shadow:0 0 20px rgba(244,59,99,0.6) !important;
    transform:scale(1.05);
}

/* Tabla */
table {
    width:100%;
    border-collapse:collapse;
    border-radius:10px;
    overflow:hidden;
    margin-top:10px;
}
th {
    background:#1B168C;
    color:#FFFFFF;
    text-align:center;
    padding:8px;
    font-weight:600;
}
td {
    text-align:center;
    padding:6px;
    border-bottom:1px solid #E5E7EB;
    color:#333333;
}
tr:nth-child(even){ background:#F3F4F6; }
tr:hover{ background:#F43B63; color:#FFFFFF; transition:.2s; }

/* Bloques */
.alternativa {
    padding:20px;
    background:#FFFFFF;
    border-radius:15px;
    border:2px solid var(--color);
    box-shadow:0 4px 12px rgba(27,22,140,0.15);
    margin-top:15px;
}
.confirmacion {
    margin-top:20px;
    padding:18px;
    border-radius:12px;
    background:#FFFFFF;
    border:2px solid var(--color);
    color:#1B168C;
    font-size:1em;
    line-height:1.6em;
    box-shadow:0 4px 10px rgba(27,22,140,0.1);
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
# 🚀 BOTÓN PRINCIPAL
# ============================
c1, c2, c3 = st.columns([1, 2.4, 1])
with c2:
    if st.button("🚀 INICIAR CHATBOT"):
        st.session_state["start_chat"] = True

# ============================
# 🔁 MAPEO DE ESTRATEGIAS
# ============================
def estrategia_base_label(valor):
    if not isinstance(valor, str): return ""
    v = valor.strip().upper()
    if "REDIFERIDO" in v: return "REDIFERIDO"
    if "REESTRUCTURACION" in v or "REESTRUCTURACIÓN" in v: return "REESTRUCTURACIÓN"
    if "PRORROGA" in v or "PRÓRROGA" in v: return "PRÓRROGA"
    return valor

# ============================
# 🧭 FLUJO DE CHAT
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
# 📋 MOSTRAR OBLIGACIONES
# ============================
if st.session_state["cliente"] is not None:
    cliente = st.session_state["cliente"]
    nombre = str(cliente["NOMBRE_FINAL"].iloc[0]).title()
    obligaciones = cliente.copy()
    total = len(obligaciones)

    st.success(f"✅ Hola {nombre}, encontramos {total} obligación{'es' if total>1 else ''} asociada{'s' if total>1 else ''}.")
    cols_vis = ["ULTIMOS_CUENTA","TIPO_PRODUCTO","PAGO_MINIMO_MES","MORA_ACTUAL","ESTRATEGIA_ACTUAL"]
    vista = obligaciones[cols_vis].rename(columns={
        "ULTIMOS_CUENTA":"Últimos dígitos",
        "TIPO_PRODUCTO":"Producto",
        "PAGO_MINIMO_MES":"Pago mínimo ($)",
        "MORA_ACTUAL":"Mora (días)",
        "ESTRATEGIA_ACTUAL":"Estrategia"
    })
    st.markdown(vista.to_html(index=False), unsafe_allow_html=True)

    opciones = [f"{r['Producto']} (****{r['Últimos dígitos']})" for _,r in vista.iterrows()]
    seleccion = opciones[0] if len(opciones)==1 else st.selectbox("🤝 ¿Qué obligación deseas negociar?", opciones)

    obligacion = obligaciones.iloc[opciones.index(seleccion)]
    estrategia = obligacion["ESTRATEGIA_ACTUAL"].strip().upper()
    producto = obligacion["TIPO_PRODUCTO"]
    cuenta = obligacion["ULTIMOS_CUENTA"]
    tasa = obligacion.get("TASA","según condiciones vigentes")
    abono = f"${obligacion.get('VALOR_ABONO',0):,.0f}"
    saldo = f"${obligacion.get('ULTIMO_SALDO_CAPITAL',0):,.0f}"
    pago_min = f"${obligacion.get('PAGO_MINIMO_MES',0):,.0f}"
    color = "#F43B63" if "CON PAGO" in estrategia else "#1B168C"

    # ============================
    # 💡 MENSAJE DE ALTERNATIVA
    # ============================
    mensajes = {
        "REDIFERIDO CON PAGO": f"{nombre}, Banco Serfinanza te invita a ampliar el plazo del saldo total del capital, no incluye intereses y otros conceptos de tu {producto} terminada en {cuenta} por valor de {saldo} con una tasa del {tasa}. Realiza un abono de {abono} para aplicar la alternativa, respondiendo con la letra respectiva acorde con el número de cuotas que deseas: A: 12 cuotas, B: 24 cuotas, C: 36 cuotas, D: 48 cuotas, E: 60 cuotas, F: No estoy interesado.",
        "REDIFERIDO SIN PAGO": f"{nombre}, Banco Serfinanza te invita a ampliar el plazo del saldo total del capital, no incluye intereses y otros conceptos de tu {producto} terminada en {cuenta} por valor de {saldo} con una tasa del {tasa}. Responde con la letra respectiva acorde con el número de cuotas que deseas: A: 12 cuotas, B: 24 cuotas, C: 36 cuotas, D: 48 cuotas, E: 60 cuotas, F: No estoy interesado.",
        "REESTRUCTURACION CON PAGO": f"{nombre}, Banco Serfinanza te invita a reestructurar el plazo del saldo total del capital, no incluye intereses y otros conceptos de tu {producto} terminada en {cuenta} por valor de {saldo} con una tasa del {tasa}. Realiza un abono de {abono} para aplicar la alternativa, respondiendo con la letra respectiva acorde con el número de cuotas que deseas: A: 12 cuotas, B: 24 cuotas, C: 36 cuotas, D: 48 cuotas, E: 60 cuotas, F: No estoy interesado.",
        "REESTRUCTURACION SIN PAGO": f"{nombre}, Banco Serfinanza te invita a reestructurar el plazo del saldo total del capital, no incluye intereses y otros conceptos de tu {producto} terminada en {cuenta} por valor de {saldo} con una tasa del {tasa}. Responde con la letra respectiva acorde con el número de cuotas que deseas: A: 12 cuotas, B: 24 cuotas, C: 36 cuotas, D: 48 cuotas, E: 60 cuotas, F: No estoy interesado.",
        "PRORROGA SIN PAGO": f"{nombre}, Banco Serfinanza te invita a diferir el capital de tu pago mínimo por valor de {pago_min} de tu {producto} terminada en {cuenta} con una tasa del {tasa}, los intereses y otros conceptos serán diferidos a 12 meses al 0%. Responde con la letra respectiva acorde con el número de cuotas que deseas: A: 12 cuotas, B: 24 cuotas, C: 36 cuotas.",
        "PRORROGA CON PAGO": f"{nombre}, Banco Serfinanza te invita a diferir el capital de tu pago mínimo por valor de {pago_min} de tu {producto} terminada en {cuenta} con una tasa del {tasa}, los intereses y otros conceptos serán diferidos a 12 meses al 0%. Realiza un abono de {abono} y responde con la letra respectiva acorde con el número de cuotas que deseas: A: 12 cuotas, B: 24 cuotas, C: 36 cuotas."
    }

    st.markdown(f"<div class='alternativa' style='--color:{color}'>"
                f"<div style='font-weight:700;color:{color};font-size:1.1em'>💡 Alternativa disponible</div>"
                f"<div style='margin-top:10px;font-size:1em;color:#333'>{mensajes.get(estrategia,'No hay alternativa disponible.')}</div></div>",
                unsafe_allow_html=True)

    # ============================
    # 📆 SELECCIÓN DE CUOTAS
    # ============================
    if "PRORROGA" in estrategia:
        cuotas = ["Selecciona una opción...", "A: 12 cuotas", "B: 24 cuotas", "C: 36 cuotas"]
    else:
        cuotas = ["Selecciona una opción...", "A: 12 cuotas", "B: 24 cuotas", "C: 36 cuotas", "D: 48 cuotas", "E: 60 cuotas", "F: No estoy interesado"]

    seleccion_cuota = st.selectbox("📆 Selecciona una opción:", cuotas, index=0, key="cuota_seleccionada")

    # ============================
    # ✅ CONFIRMACIÓN FINAL
    # ============================
    if seleccion_cuota != "Selecciona una opción..." and seleccion_cuota != "F: No estoy interesado":
        letra, cuota_txt = seleccion_cuota.split(":")
        cuota_txt = cuota_txt.strip()
        confirmaciones = {
            "REDIFERIDO CON PAGO": f"Tu solicitud de ampliación de plazo al saldo capital a {cuota_txt} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente, la tasa será del {tasa} y cuando se realice el abono acordado.",
            "REDIFERIDO SIN PAGO": f"Tu solicitud de ampliación de plazo al saldo capital a {cuota_txt} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente, la tasa será del {tasa}.",
            "REESTRUCTURACION CON PAGO": f"Tu solicitud de reestructuración de plazo a {cuota_txt} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente, la tasa será la vigente del producto al momento del beneficio y cuando se realice el abono acordado.",
            "REESTRUCTURACION SIN PAGO": f"Tu solicitud de reestructuración de plazo a {cuota_txt} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente, la tasa será la vigente del producto al momento del beneficio.",
            "PRORROGA SIN PAGO": f"Tu solicitud de diferido del capital de tu pago mínimo a {cuota_txt} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente, la tasa será del {tasa}.",
            "PRORROGA CON PAGO": f"Tu solicitud de diferido del capital de tu pago mínimo a {cuota_txt} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente, siempre y cuando se realice el abono acordado. La tasa será del {tasa}."
        }
        confirmacion = confirmaciones.get(estrategia, "Tu solicitud ha sido registrada.")
        st.markdown(f"<div class='confirmacion' style='--color:{color}'><b>✅ Confirmación registrada:</b><br>{confirmacion}<br><br>Consulta términos y condiciones en la página web del Banco Serfinanza.</div>", unsafe_allow_html=True)
