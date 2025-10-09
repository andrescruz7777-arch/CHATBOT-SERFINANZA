import streamlit as st
import pandas as pd

# ============================
# ⚙️ CONFIGURACIÓN INICIAL
# ============================
st.set_page_config(page_title="💬 Chatbot IA - Banco Serfinanza", layout="centered")

# Estado inicial seguro
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

.header-container {
    display: flex; justify-content: space-between; align-items: center; padding: 0 2rem;
}

h1, h2, h3 { color: #1B168C; text-align: center; }

[data-theme="light"] .intro-text { color: #1B168C; }
[data-theme="dark"]  .intro-text { color: #FFFFFF; }

.intro-text {
    text-align: center; font-size: 1.15em; font-weight: 500;
    line-height: 1.6em; margin-top: 15px; transition: color 0.3s ease;
}
.highlight { color: #F43B63; font-weight: 600; }

div.stButton > button, form button[kind="primary"] {
    background-color:#1B168C !important; color:#fff !important; border:none;
    border-radius:12px !important; padding:16px 60px !important; font-size:1.1em !important;
    font-weight:600 !important; cursor:pointer; transition:all .3s ease !important;
    box-shadow:0 4px 15px rgba(27,22,140,.3) !important;
}
div.stButton > button:hover, form button[kind="primary"]:hover {
    background-color:#F43B63 !important; box-shadow:0 0 20px rgba(244,59,99,.7) !important;
    transform:scale(1.05);
}

table { width:100%; border-collapse:collapse; border-radius:10px; overflow:hidden; }
th { background:#1B168C; color:#fff; text-align:center; padding:8px; }
td { text-align:center; padding:6px; border-bottom:1px solid #E5E7EB; }
tr:nth-child(even){ background:#F3F4F6; }
tr:hover{ background:#F43B63; color:#fff; transition:.2s; }
</style>
""", unsafe_allow_html=True)

# ============================
# 🖼️ CABECERA CON LOGOS
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
# 🚀 BOTÓN PRINCIPAL (CENTRADO)
# ============================
c1, c2, c3 = st.columns([1, 2.4, 1])
with c2:
    start = st.button("🚀 INICIAR CHATBOT", key="btn_iniciar_chatbot")

if start:
    st.session_state["start_chat"] = True
    st.session_state["intentos"] = 0

# ============================
# 🔁 MAPEO DE ESTRATEGIAS
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
# 🧭 VALIDACIÓN DE CÉDULA Y OBLIGACIONES
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

            # ---- Tabla de obligaciones ----
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
            ).fillna(0).map("{:,.0f}".format)

            st.markdown(obligaciones_vista.to_html(index=False, escape=False), unsafe_allow_html=True)

            # ---- Selector de obligación ----
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

                # ---- Mensajes según estrategia ----
                if estrategia == "REDIFERIDO CON PAGO":
                    mensaje = f"""{nombre}, Banco Serfinanza te invita a ampliar el plazo del saldo total del capital,
                    no incluye intereses ni otros conceptos de tu {producto} terminada en {cuenta} por valor de {saldo}
                    con una tasa del {tasa}. Realiza un abono de {abono} para aplicar la alternativa."""
                    cuotas = ["12 cuotas", "24 cuotas", "36 cuotas", "48 cuotas", "60 cuotas", "No estoy interesado"]
                elif estrategia == "REDIFERIDO SIN PAGO":
                    mensaje = f"""{nombre}, Banco Serfinanza te invita a ampliar el plazo del saldo total del capital,
                    no incluye intereses ni otros conceptos de tu {producto} terminada en {cuenta} por valor de {saldo}
                    con una tasa del {tasa}."""
                    cuotas = ["12 cuotas", "24 cuotas", "36 cuotas", "48 cuotas", "60 cuotas", "No estoy interesado"]
                elif estrategia == "REESTRUCTURACION CON PAGO":
                    mensaje = f"""{nombre}, Banco Serfinanza te invita a reestructurar el plazo del saldo total del capital,
                    no incluye intereses ni otros conceptos de tu {producto} terminada en {cuenta} por valor de {saldo}
                    con una tasa del {tasa}. Realiza un abono de {abono} para aplicar la alternativa."""
                    cuotas = ["12 cuotas", "24 cuotas", "36 cuotas", "48 cuotas", "60 cuotas", "No estoy interesado"]
                elif estrategia == "REESTRUCTURACION SIN PAGO":
                    mensaje = f"""{nombre}, Banco Serfinanza te invita a reestructurar el plazo del saldo total del capital,
                    no incluye intereses ni otros conceptos de tu {producto} terminada en {cuenta} por valor de {saldo}
                    con una tasa del {tasa}."""
                    cuotas = ["12 cuotas", "24 cuotas", "36 cuotas", "48 cuotas", "60 cuotas", "No estoy interesado"]
                elif estrategia == "PRORROGA SIN PAGO":
                    mensaje = f"""{nombre}, Banco Serfinanza te invita a diferir el capital de tu pago mínimo por valor de {pago_minimo}
                    de tu {producto} terminada en {cuenta} con una tasa del {tasa}.
                    Los intereses y otros conceptos serán diferidos a 12 meses al 0%."""
                    cuotas = ["12 cuotas", "24 cuotas", "36 cuotas", "No estoy interesado"]
                elif estrategia == "PRORROGA CON PAGO":
                    mensaje = f"""{nombre}, Banco Serfinanza te invita a diferir el capital de tu pago mínimo por valor de {pago_minimo}
                    de tu {producto} terminada en {cuenta} con una tasa del {tasa}.
                    Realiza un abono de {abono} para aplicar la alternativa. Los intereses y otros conceptos serán diferidos a 12 meses al 0%."""
                    cuotas = ["12 cuotas", "24 cuotas", "36 cuotas", "No estoy interesado"]
                else:
                    mensaje = f"{nombre}, tu obligación no cuenta con una alternativa activa de negociación en este momento."
                    cuotas = ["No estoy interesado"]

                # ---- Mostrar mensaje ----
                st.markdown(f"""
                <div style='padding:15px; background-color:#F9FAFB; border-radius:10px; border:1px solid #E5E7EB;'>
                    <b>💡 Alternativa disponible:</b><br><br>{mensaje}<br><br>
                    Responde con la letra correspondiente a la cantidad de cuotas que deseas:
                </div>
                """, unsafe_allow_html=True)

                seleccion_cuota = st.selectbox("📆 Selecciona una opción de plazo:", cuotas, key="cuota_elegida")

                if seleccion_cuota and seleccion_cuota != "No estoy interesado":
                    st.success(f"✅ Has seleccionado {seleccion_cuota}. ¡Excelente elección!")
                elif seleccion_cuota == "No estoy interesado":
                    st.warning("ℹ️ Entendido, no estás interesado en esta alternativa por ahora.")

        else:
            # —— CÉDULA NO ENCONTRADA ——
            if st.session_state["intentos"] == 1:
                st.warning("⚠️ No encontramos el número ingresado en nuestra base de datos. "
                           "Por favor verifica y vuelve a digitarlo sin espacios ni caracteres especiales.")
            elif st.session_state["intentos"] >= 2:
                st.error("❌ El número ingresado no se encuentra registrado. Digita nuevamente tu número de cédula sin puntos o caracteres especiales.")
                st.markdown("""
                Te invitamos a comunicarte con nuestros asesores para validar tu información:<br>
                📞 <b>601 7491928</b><br>
                💼 <b>Contacto Solutions S.A.S.</b><br>
                💬 <a href="https://wa.me/573112878102?text=Hola%2C+quisiera+validar+mi+información+en+el+Chatbot+IA+de+Serfinanza" target="_blank">Escríbenos por WhatsApp</a>
                """, unsafe_allow_html=True)
                st.stop()

