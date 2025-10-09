import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ============================
# ⚙️ CONFIGURACIÓN INICIAL
# ============================
st.set_page_config(page_title="💬 Chatbot IA - Banco Serfinanza", layout="centered")

# Estado inicial seguro
for key, val in {
    "start_chat": False,
    "intentos": 0,
    "cedula_valida": False,
    "cliente_data": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

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
# 🚀 INICIAR CHATBOT
# ============================
c1, c2, c3 = st.columns([1, 2.4, 1])
with c2:
    if st.button("🚀 INICIAR CHATBOT", key="btn_iniciar_chatbot"):
        st.session_state["start_chat"] = True

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
# 🧭 VALIDACIÓN DE CÉDULA
# ============================
if st.session_state["start_chat"]:
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
            st.session_state["cedula_valida"] = True
            st.session_state["cliente_data"] = cliente
        else:
            if st.session_state["intentos"] == 1:
                st.warning("⚠️ No encontramos el número ingresado en nuestra base de datos. Verifica e inténtalo nuevamente.")
            elif st.session_state["intentos"] >= 2:
                st.error("❌ No se encontró el número ingresado. Comunícate con nuestros asesores:")
                st.markdown("""
                📞 <b>601 7491928</b><br>
                💼 <b>Contacto Solutions S.A.S.</b><br>
                💬 <a href="https://wa.me/573112878102" target="_blank">Escríbenos por WhatsApp</a>
                """, unsafe_allow_html=True)
                st.stop()

# ============================
# 📋 MOSTRAR OBLIGACIONES
# ============================
if st.session_state["cedula_valida"]:
    cliente = st.session_state["cliente_data"]
    obligaciones_cliente = cliente.copy()
    total_obligaciones = len(obligaciones_cliente)
    nombre_cliente = str(obligaciones_cliente["NOMBRE_FINAL"].iloc[0]).title()

    st.success(f"✅ Perfecto, encontramos información asociada al documento {cedula}.")
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
    ).fillna(0).map("{:,.0f}".format)

    st.markdown(obligaciones_vista.to_html(index=False, escape=False), unsafe_allow_html=True)

    # Selector
    st.markdown("<br>", unsafe_allow_html=True)
    opciones = [f"{row['Producto']} ({row['Últimos dígitos']})" for _, row in obligaciones_vista.iterrows()]
    seleccion = st.selectbox("🤝 ¿Qué obligación deseas negociar?", opciones, key="obligacion_seleccionada")

    obligacion_sel = obligaciones_cliente.iloc[opciones.index(seleccion)]
    estrategia = obligacion_sel["ESTRATEGIA_ACTUAL"].strip().upper()
    producto = obligacion_sel["TIPO_PRODUCTO"]
    cuenta = obligacion_sel["ULTIMOS_CUENTA"]
    tasa = obligacion_sel.get("TASA", "según condiciones vigentes")

    # Colores
    color = "#F43B63" if "CON PAGO" in estrategia else "#1B168C"

    st.markdown(f"""
    <div style='
        padding:20px;
        background:linear-gradient(135deg, #ffffff, #f8f9ff);
        border-radius:15px;
        border:2px solid {color};
        box-shadow:0 4px 12px rgba(27,22,140,0.15);
        margin-top:10px;
    '>
        <div style='font-size:1.1em; color:{color}; font-weight:700;'>
            💡 Alternativa disponible
        </div>
        <div style='margin-top:10px; font-size:1em; line-height:1.6em; color:#333;'>
            {estrategia.title()} disponible para tu {producto} terminada en {cuenta}. Selecciona el plazo que más se ajuste a ti.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Lista de cuotas
    cuotas = ["Selecciona una opción...", "12 cuotas", "24 cuotas", "36 cuotas", "48 cuotas", "60 cuotas", "No estoy interesado"]
    seleccion_cuota = st.selectbox("📆 Selecciona una opción de plazo:", cuotas, index=0)

    # ============================
    # ✅ CONFIRMACIÓN Y REGISTRO
    # ============================
    if seleccion_cuota != "Selecciona una opción..." and seleccion_cuota != "No estoy interesado":
        if estrategia == "REDIFERIDO CON PAGO":
            confirmacion = f"Tu solicitud de ampliación de plazo al saldo capital a {seleccion_cuota} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente, la tasa será del {tasa} y cuando se realice el abono acordado."
        elif estrategia == "REDIFERIDO SIN PAGO":
            confirmacion = f"Tu solicitud de ampliación de plazo al saldo capital a {seleccion_cuota} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente, la tasa será del {tasa}."
        elif estrategia == "REESTRUCTURACION CON PAGO":
            confirmacion = f"Tu solicitud de reestructuración de plazo a {seleccion_cuota} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente, la tasa será la vigente del producto al momento de aplicar el beneficio y cuando se realice el abono acordado."
        elif estrategia == "REESTRUCTURACION SIN PAGO":
            confirmacion = f"Tu solicitud de reestructuración de plazo a {seleccion_cuota} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente, la tasa será la vigente del producto al momento de aplicar el beneficio."
        elif estrategia == "PRORROGA CON PAGO":
            confirmacion = f"Tu solicitud de diferido del pago mínimo a {seleccion_cuota} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente, siempre y cuando se realice el abono acordado. La tasa será del {tasa}."
        elif estrategia == "PRORROGA SIN PAGO":
            confirmacion = f"Tu solicitud de diferido del pago mínimo a {seleccion_cuota} en tu {producto} terminada en {cuenta} ha sido registrada exitosamente, la tasa será del {tasa}."
        else:
            confirmacion = "Tu solicitud ha sido registrada."

        st.markdown(f"""
        <div style='
            margin-top:20px;
            padding:18px;
            border-radius:12px;
            background-color:#E9F7EF;
            border-left:5px solid {color};
            color:#1B168C;
            font-size:1em;
            line-height:1.6em;
        '>
            <b>✅ Confirmación registrada:</b><br>{confirmacion}<br><br>
            Consulta términos y condiciones en la página web del Banco Serfinanza.
        </div>
        """, unsafe_allow_html=True)

        # Guardar registro
        registro = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Cédula": cedula,
            "Nombre": nombre_cliente,
            "Producto": producto,
            "Cuenta": cuenta,
            "Estrategia": estrategia,
            "Cuotas": seleccion_cuota,
            "Confirmación": confirmacion
        }])

        file_path = "confirmaciones_chatbot.xlsx"
        if os.path.exists(file_path):
            prev = pd.read_excel(file_path)
            registro = pd.concat([prev, registro], ignore_index=True)
        registro.to_excel(file_path, index=False)

        st.success("📄 Registro guardado exitosamente en confirmaciones_chatbot.xlsx")
