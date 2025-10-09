import streamlit as st
import pandas as pd

# ============================
# ⚙️ CONFIGURACIÓN INICIAL
# ============================
st.set_page_config(page_title="💬 Chatbot IA - Banco Serfinanza", layout="centered")

if "start_chat" not in st.session_state:
    st.session_state["start_chat"] = False
if "intentos" not in st.session_state:
    st.session_state["intentos"] = 0

# ============================
# 🎨 ESTILOS PERSONALIZADOS
# ============================
st.markdown("""
<style>
body { background-color: #FFFFFF; }

/* CABECERA */
.header-container {
    display: flex; justify-content: space-between; align-items: center; padding: 0 2rem;
}

/* TÍTULOS */
h1, h2, h3 { color: #1B168C; text-align: center; }

/* TEXTO DE BIENVENIDA */
.intro-text {
    text-align: center;
    font-size: 1.15em;
    font-weight: 500;
    line-height: 1.6em;
    margin-top: 15px;
    color: #1B168C;
}
.highlight { color: #F43B63; font-weight: 600; }

/* BOTONES CON TEXTO BLANCO */
div.stButton > button, form button[kind="primary"] {
    background-color:#1B168C !important;
    color:#FFFFFF !important;
    border:none;
    border-radius:12px !important;
    padding:16px 60px !important;
    font-size:1.1em !important;
    font-weight:600 !important;
    cursor:pointer;
    transition:all .3s ease !important;
    box-shadow:0 4px 15px rgba(27,22,140,.3) !important;
}
div.stButton > button:hover, form button[kind="primary"]:hover {
    background-color:#F43B63 !important;
    color:#FFFFFF !important;
    box-shadow:0 0 20px rgba(244,59,99,.7) !important;
    transform:scale(1.05);
}

/* TABLA */
table { width:100%; border-collapse:collapse; border-radius:10px; overflow:hidden; }
th { background:#1B168C; color:#FFFFFF; text-align:center; padding:8px; }
td { text-align:center; padding:6px; border-bottom:1px solid #E5E7EB; color:#000000; }
tr:nth-child(even){ background:#F3F4F6; }
tr:hover{ background:#F43B63; color:#FFFFFF; transition:.2s; }
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
col1, col2, col3 = st.columns([1, 2.4, 1])
with col2:
    start = st.button("🚀 INICIAR CHATBOT", key="btn_iniciar_chatbot")

if start:
    st.session_state["start_chat"] = True
    st.session_state["intentos"] = 0

# ============================
# MAPEO DE ESTRATEGIAS
# ============================
def estrategia_base_label(valor: str) -> str:
    if not isinstance(valor, str):
        return ""
    v = valor.strip().upper()
    if v.startswith("REDIFERIDO"):
        return "REDIFERIDO"
    if v.startswith("REESTRUCTURACION") or v.startswith("REESTRUCTURACIÓN"):
        return "REESTRUCTURACIÓN"
    if v.startswith("PRORROGA") or v.startswith("PRÓRROGA"):
        return "PRÓRROGA"
    if v.startswith("ABONAR"):
        return "CANCELACIÓN DEL PAGO MÍNIMO"
    return valor

# ============================
# VALIDACIÓN DE CÉDULA
# ============================
if st.session_state.get("start_chat"):
    st.markdown("<hr><br>", unsafe_allow_html=True)
    st.subheader("🔍 Verificación de identidad")

    c1, c2, c3 = st.columns([1, 1.6, 1])
    with c2:
        with st.form("form_cedula", clear_on_submit=False):
            cedula = st.text_input("🪪 Digita tu número de cédula (sin puntos ni caracteres especiales):", key="cedula_input")
            submitted = st.form_submit_button("➡️ Continuar")

    if submitted and cedula:
        st.session_state["intentos"] += 1

        try:
            data = pd.read_excel("base_bot_serfinanza.xls")
        except Exception as e:
            st.error(f"Error al cargar la base: {e}")
            st.stop()

        cliente = data[data["NUMERO_IDENTIFICACION"].astype(str) == cedula.strip()]

        if not cliente.empty:
            st.success(f"✅ Perfecto, encontramos información asociada al documento {cedula}.")
            st.markdown("En los próximos pasos podrás visualizar tus obligaciones y opciones de negociación.")

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

            if seleccion:
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

                # ---- MENSAJES DE OFRECIMIENTO ----
                # (textos exactos como solicitaste)
                if estrategia == "REDIFERIDO CON PAGO":
                    mensaje = f"""{nombre} Banco Serfinanza te invita a ampliar el plazo del saldo total del capital, no incluye intereses y otros conceptos de tu {producto} terminada en {cuenta} por valor de {saldo} con una tasa del {tasa}. Realiza un abono de {abono} para aplicar la alternativa, respondiendo con la letra respectiva acorde con el número de cuotas que deseas:
                    A: 12 cuotas, B: 24 cuotas, C: 36 cuotas, D: 48 cuotas, E: 60 cuotas, F: No estoy interesado."""
                elif estrategia == "REDIFERIDO SIN PAGO":
                    mensaje = f"""{nombre} Banco Serfinanza te invita a ampliar el plazo del saldo total del capital, no incluye intereses y otros conceptos de tu {producto} terminada en {cuenta} por valor de {saldo} con una tasa del {tasa}. Respondiendo con la letra respectiva acorde con el número de cuotas que deseas:
                    A: 12 cuotas, B: 24 cuotas, C: 36 cuotas, D: 48 cuotas, E: 60 cuotas, F: No estoy interesado."""
                elif estrategia == "REESTRUCTURACION CON PAGO":
                    mensaje = f"""{nombre} Banco Serfinanza te invita a reestructurar el plazo del saldo total del capital, no incluye intereses y otros conceptos de tu {producto} terminada en {cuenta} por valor de {saldo} con una tasa del {tasa}. Realiza un abono de {abono} para aplicar la alternativa, respondiendo con la letra respectiva acorde con el número de cuotas que deseas:
                    A: 12 cuotas, B: 24 cuotas, C: 36 cuotas, D: 48 cuotas, E: 60 cuotas, F: No estoy interesado."""
                elif estrategia == "REESTRUCTURACION SIN PAGO":
                    mensaje = f"""{nombre} Banco Serfinanza te invita a reestructurar el plazo del saldo total del capital, no incluye intereses y otros conceptos de tu {producto} terminada en {cuenta} por valor de {saldo} con una tasa del {tasa}. Respondiendo con la letra respectiva acorde con el número de cuotas que deseas:
                    A: 12 cuotas, B: 24 cuotas, C: 36 cuotas, D: 48 cuotas, E: 60 cuotas, F: No estoy interesado."""
                elif estrategia == "PRORROGA SIN PAGO":
                    mensaje = f"""{nombre} Banco Serfinanza te invita a diferir el capital de tu pago mínimo por valor de {pago_minimo} de tu {producto} terminada en {cuenta} con una tasa del {tasa}, los intereses y otros conceptos serán diferidos a 12 meses al 0%. Respondiendo con la letra respectiva acorde con el número de cuotas que deseas A: 12 cuotas, B: 24 cuotas, C: 36 cuotas."""
                elif estrategia == "PRORROGA CON PAGO":
                    mensaje = f"""{nombre} Banco Serfinanza te invita a diferir el capital de tu pago mínimo por valor de {pago_minimo} de tu {producto} terminada en {cuenta} con una tasa del {tasa}, los intereses y otros conceptos serán diferidos a 12 meses al 0%. Realiza un abono de {abono} respondiendo con la letra respectiva acorde con el número de cuotas que deseas A: 12 cuotas, B: 24 cuotas, C: 36 cuotas."""
                else:
                    mensaje = f"{nombre}, tu obligación no cuenta con una alternativa activa de negociación en este momento."

                # ---- MOSTRAR MENSAJE ----
                st.markdown(f"""
                <div style='padding:20px; background:linear-gradient(135deg, #ffffff, #f8f9ff);
                    border-radius:15px; border:2px solid {color};
                    box-shadow:0 4px 12px rgba(27,22,140,0.15); margin-top:10px;'>
                    <div style='font-size:1.1em; color:{color}; font-weight:700;'>💡 Alternativa disponible</div>
                    <div style='margin-top:10px; font-size:1em; line-height:1.6em; color:#333;'>{mensaje}</div>
                </div>
                """, unsafe_allow_html=True)

                cuotas = ["Selecciona una opción...", "12 cuotas", "24 cuotas", "36 cuotas", "48 cuotas", "60 cuotas", "No estoy interesado"]
                seleccion_cuota = st.selectbox("📆 Selecciona una opción de plazo:", cuotas, key="cuota_elegida", index=0)

                if seleccion_cuota != "Selecciona una opción..." and seleccion_cuota != "No estoy interesado":
                    if estrategia == "REDIFERIDO CON PAGO":
                        confirm = f"Tu solicitud de la ampliación de plazo al saldo capital a {seleccion_cuota} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente, la tasa será del {tasa} y cuando se realice el abono acordado. Consulta términos y condiciones en la página web del Banco Serfinanza."
                    elif estrategia == "REDIFERIDO SIN PAGO":
                        confirm = f"Tu solicitud de la ampliación de plazo al saldo capital a {seleccion_cuota} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente, la tasa será del {tasa}. Consulta términos y condiciones en la página web del Banco Serfinanza."
                    elif estrategia == "REESTRUCTURACION CON PAGO":
                        confirm = f"Tu solicitud de reestructuración de plazo al saldo capital a {seleccion_cuota} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente, la tasa será la vigente del producto al momento de aplicar el beneficio y cuando se realice el abono acordado. La obligación quedará marcada como reestructurada ante las centrales de riesgo, consulta términos y condiciones en la página web del Banco Serfinanza."
                    elif estrategia == "REESTRUCTURACION SIN PAGO":
                        confirm = f"Tu solicitud de reestructuración de plazo al saldo capital a {seleccion_cuota} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente, la tasa será la vigente del producto al momento de aplicar el beneficio. La obligación quedará marcada como reestructurada ante las centrales de riesgo, consulta términos y condiciones en la página web del Banco Serfinanza."
                    elif estrategia == "PRORROGA SIN PAGO":
                        confirm = f"Tu solicitud de diferido del capital de tu pago mínimo a {seleccion_cuota} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente, la tasa será del {tasa}, consulta términos y condiciones en la página web del Banco Serfinanza."
                    elif estrategia == "PRORROGA CON PAGO":
                        confirm = f"Tu solicitud de diferido del capital de tu pago mínimo a {seleccion_cuota} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente siempre y cuando se realice el abono acordado, la tasa será del {tasa}, consulta términos y condiciones en la página web del Banco Serfinanza."
                    else:
                        confirm = ""

                    st.markdown(f"""
                    <div style='padding:20px; background:linear-gradient(135deg, #ffffff, #f8f9ff);
                        border-radius:15px; border:2px solid {color};
                        box-shadow:0 4px 12px rgba(27,22,140,0.15); margin-top:10px;'>
                        <div style='font-size:1.1em; color:{color}; font-weight:700;'>✅ Confirmación registrada</div>
                        <div style='margin-top:10px; font-size:1em; line-height:1.6em; color:#333;'>{confirm}</div>
                    </div>
                    """, unsafe_allow_html=True)
                elif seleccion_cuota == "No estoy interesado":
                    st.warning("ℹ️ Entendido, no estás interesado en esta alternativa por ahora.")
