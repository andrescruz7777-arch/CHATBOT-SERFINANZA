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
    padding: 14px 42px;
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
    padding: 16px 80px;                     /* ⬅️ más ancho */
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
# 🧭 VALIDACIÓN DE CÉDULA
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
        else:
            if st.session_state["intentos"] == 1:
                st.warning("⚠️ No encontramos el número ingresado en nuestra base de datos. "
                           "Por favor verifica y vuelve a digitarlo sin espacios ni caracteres especiales.")
            elif st.session_state["intentos"] >= 2:
                st.error("❌ El número ingresado no se encuentra registrado.")
                st.markdown("""
                Te invitamos a comunicarte con nuestros asesores para validar tu información:  
                📞 <b>601 7491928</b>  
                💼 <b>Contacto Solutions S.A.S.</b>  
                💬 <a href="https://wa.me/573112878102?text=Hola%2C+quisiera+validar+mi+información+en+el+Chatbot+IA+de+Serfinanza" target="_blank">Escríbenos por WhatsApp</a>
                """, unsafe_allow_html=True)
                st.stop()
