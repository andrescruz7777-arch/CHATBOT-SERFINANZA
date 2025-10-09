import streamlit as st
import pandas as pd

# ============================
# ⚙️ CONFIGURACIÓN INICIAL
# ============================
st.set_page_config(page_title="💬 Chatbot IA - Banco Serfinanza", layout="centered")

# ============================
# 🎨 ESTILOS PERSONALIZADOS
# ============================
st.markdown("""
<style>
/* Fondo general */
body {
    background-color: #FFFFFF;
}

/* Cabecera con dos logos */
.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 2rem;
}

/* Títulos */
h1, h2, h3 {
    color: #1B168C; /* Azul corporativo Serfinanza */
    text-align: center;
}

/* Texto de bienvenida adaptable a tema */
[data-theme="light"] .intro-text {
    color: #1B168C; /* Azul en tema claro */
}
[data-theme="dark"] .intro-text {
    color: #FFFFFF; /* Blanco en tema oscuro */
}
.intro-text {
    text-align: center;
    font-size: 1.15em;
    font-weight: 500;
    line-height: 1.6em;
    margin-top: 15px;
    transition: color 0.3s ease;
}
.highlight {
    color: #F43B63; /* Rojo Serfinanza */
    font-weight: 600;
}

/* Botones institucionales */
div.stButton > button:first-child {
    background-color: #1B168C;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 20px 60px;
    font-size: 1.1em;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(27,22,140,0.3);
}
div.stButton > button:first-child:hover {
    background-color: #F43B63;
    box-shadow: 0 0 20px rgba(244,59,99,0.7);
    transform: scale(1.07);
}
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
Soy tu <span class="highlight">Asistente Virtual IA</span> de <b>Contacto Solutions</b>, aliado estratégico de <b>Banco Serfinanza</b>.  
Estoy aquí para brindarte información de tus productos y opciones de negociación.
</div>
""", unsafe_allow_html=True)
# ============================
# 🚀 BOTÓN PRINCIPAL (ALARGADO Y VISUALMENTE CENTRADO)
# ============================

st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #1B168C;              /* Azul Serfinanza */
    color: white;
    border: none;
    border-radius: 12px;
    padding: 20px 60px;                     /* ⬅️ más ancho */
    font-size: 1.15em;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(27,22,140,0.3);
}
div.stButton > button:first-child:hover {
    background-color: #F43B63;              /* Rojo hover */
    box-shadow: 0 0 20px rgba(244,59,99,0.7);
    transform: scale(1.06);
}
</style>
""", unsafe_allow_html=True)

# Botón con clave única
col1, col2, col3 = st.columns([1, 2.4, 1])
with col2:
    start = st.button("🚀 INICIAR CHATBOT", key="btn_iniciar_chatbot")

# Activar flujo
if start:
    st.session_state["start_chat"] = True
    st.session_state["intentos"] = 0
# ============================
# 🧭 VALIDACIÓN DE CÉDULA Y MOSTRAR OBLIGACIONES
# ============================
if st.session_state.get("start_chat"):
    st.markdown("<hr><br>", unsafe_allow_html=True)
    st.subheader("🔍 Verificación de identidad")

    cedula = st.text_input("🪪 Digita tu número de cédula (sin puntos ni caracteres especiales):", key="cedula_input")

    # Botón adicional junto con Enter
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        siguiente = st.button("➡️ Continuar", key="continuar_btn")

    # Intentar cargar la base
    try:
        data = pd.read_excel("base_bot_serfinanza.xls")
    except Exception as e:
        st.error(f"Error al cargar la base: {e}")
        st.stop()

    # El flujo se activa si presiona Enter o clic en Continuar
    if cedula and (siguiente or st.session_state.get("cedula_input")):
        st.session_state["intentos"] += 1
        cliente = data[data["NUMERO_IDENTIFICACION"].astype(str) == cedula.strip()]

        if not cliente.empty:
            st.success(f"✅ Perfecto, encontramos información asociada al documento {cedula}.")
            st.markdown("En los próximos pasos podrás visualizar tus obligaciones y opciones de negociación.")

            # ============================
            # 💳 MOSTRAR OBLIGACIONES EN TABLA
            # ============================
            obligaciones_cliente = cliente.copy()
            total_obligaciones = len(obligaciones_cliente)
            nombre_cliente = obligaciones_cliente["NOMBRE_FINAL"].iloc[0].title()

            st.markdown(
                f"### 👋 Hola {nombre_cliente}, actualmente cuentas con **{total_obligaciones} obligación{'es' if total_obligaciones > 1 else ''}** registradas."
            )
            st.markdown("A continuación te presento el estado de cada una 👇")

            # Convertir columnas necesarias a formato visible
            columnas_visibles = [
                "ULTIMOS_CUENTA",
                "TIPO_PRODUCTO",
                "PAGO_MINIMO_MES",
                "MORA_ACTUAL",
                "ESTRATEGIA_ACTUAL"
            ]

            # Renombrar columnas para visual más amigable
            obligaciones_vista = obligaciones_cliente[columnas_visibles].rename(columns={
                "ULTIMOS_CUENTA": "Últimos dígitos",
                "TIPO_PRODUCTO": "Producto",
                "PAGO_MINIMO_MES": "Pago mínimo mes ($)",
                "MORA_ACTUAL": "Mora (días)",
                "ESTRATEGIA_ACTUAL": "Estrategia actual"
            })

            # Formatear valores numéricos
            obligaciones_vista["Pago mínimo mes ($)"] = pd.to_numeric(
                obligaciones_vista["Pago mínimo mes ($)"], errors="coerce"
            ).fillna(0).map("{:,.0f}".format)

            # Aplicar estilo de tabla
            st.markdown("""
            <style>
            table {
                width: 100%;
                border-collapse: collapse;
                border-radius: 10px;
                overflow: hidden;
            }
            th {
                background-color: #1B168C;
                color: white;
                text-align: center;
                padding: 8px;
            }
            td {
                text-align: center;
                padding: 6px;
                border-bottom: 1px solid #E5E7EB;
            }
            tr:nth-child(even) {
                background-color: #F3F4F6;
            }
            tr:hover {
                background-color: #F43B63;
                color: white;
                transition: 0.2s;
            }
            </style>
            """, unsafe_allow_html=True)

            # Mostrar tabla
            st.markdown(obligaciones_vista.to_html(index=False, escape=False), unsafe_allow_html=True)

            # ============================
            # 🤝 SELECCIÓN DE OBLIGACIÓN
            # ============================
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 🤝 ¿Qué obligación deseas negociar?")

            opciones = [
                f"{row['Producto']} ({row['Últimos dígitos']})"
                for _, row in obligaciones_vista.iterrows()
            ]
            seleccion = st.selectbox("Selecciona una opción:", opciones, key="obligacion_seleccionada")

            if seleccion:
                st.session_state["obligacion_seleccionada"] = seleccion
                st.info(f"✅ Has seleccionado {seleccion}. A continuación se mostrarán las opciones de negociación disponibles.")

        else:
            # ============================
            # ⚠️ MANEJO DE CÉDULA NO ENCONTRADA
            # ============================
            if st.session_state["intentos"] == 1:
                st.warning("⚠️ No encontramos el número ingresado en nuestra base de datos. "
                           "Por favor verifica y vuelve a digitarlo sin espacios ni caracteres especiales.")
            elif st.session_state["intentos"] >= 2:
                st.error("❌ El número ingresado no se encuentra registrado. Digita nuevamente tu número de cédula sin puntos o caracteres especiales.")
                st.markdown("""
                Te invitamos a comunicarte con nuestros asesores para validar tu información:  
                📞 <b>601 7491928</b>  
                💼 <b>Contacto Solutions S.A.S.</b>  
                💬 <a href="https://wa.me/573112878102?text=Hola%2C+quisiera+validar+mi+información+en+el+Chatbot+IA+de+Serfinanza" target="_blank">Escríbenos por WhatsApp</a>
                """, unsafe_allow_html=True)
                st.stop()

# Selector de obligación (ahora también con itertuples y atributos)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🤝 ¿Qué obligación deseas negociar?")

opciones = [
    f"Obligación {i} — {r.TIPO_PRODUCTO} ({r.ULTIMOS_CUENTA})"
    for i, r in enumerate(obligaciones_cliente.itertuples(index=False), start=1)
]
seleccion = st.selectbox("Selecciona una opción:", opciones, key="obligacion_seleccionada")

if seleccion:
    st.session_state["obligacion_seleccionada"] = seleccion
    st.info(f"✅ Has seleccionado {seleccion}. A continuación se mostrarán las opciones de negociación disponibles.")

        else:
            if st.session_state["intentos"] == 1:
                st.warning("⚠️ No encontramos el número ingresado en nuestra base de datos. "
                           "Por favor verifica y vuelve a digitarlo sin espacios ni caracteres especiales.")
            elif st.session_state["intentos"] >= 2:
                st.error("❌ El número ingresado no se encuentra registrado. Digita nuevamente tu número de cédula sin puntos o caracteres especiales.")
                st.markdown("""
                Te invitamos a comunicarte con nuestros asesores para validar tu información:  
                📞 <b>601 7491928</b>  
                💼 <b>Contacto Solutions S.A.S.</b>  
                💬 <a href="https://wa.me/573112878102?text=Hola%2C+quisiera+validar+mi+información+en+el+Chatbot+IA+de+Serfinanza" target="_blank">Escríbenos por WhatsApp</a>
                """, unsafe_allow_html=True)
                st.stop()
