import streamlit as st
import pandas as pd

# ============================
# ⚙️ CONFIGURACIÓN INICIAL
# ============================
st.set_page_config(page_title="💬 Chatbot IA - Banco Serfinanza", layout="wide")

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

/* Botón principal */
div.stButton > button:first-child {
    background-color: #1B168C;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.6em 1.2em;
    font-weight: 600;
    transition: 0.3s;
}
div.stButton > button:first-child:hover {
    background-color: #F43B63; /* Rojo Ser */
    color: white;
}

/* Mensajes */
.caption-text {
    text-align: center;
    color: #333333;
    font-size: 1.1em;
    margin-top: 1em;
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
# 💬 MENSAJE DE BIENVENIDA (MEJOR VISIBILIDAD Y CONTRASTE)
# ============================
st.markdown("""
<style>
/* Detectar tema oscuro o claro automáticamente */
[data-theme="light"] .intro-text {
    color: #1B168C; /* Azul Serfinanza en tema claro */
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
</style>

<div class="intro-text">
Soy tu <span class="highlight">Asistente Virtual IA</span> de <b>Contacto Solutions</b>, aliado estratégico de <b>Banco Serfinanza</b>.  
Estoy aquí para brindarte información de tus productos y opciones de negociación.
</div>
""", unsafe_allow_html=True)
# ============================
# 🚀 BOTÓN SERFINANZA — CENTRADO + HOVER FUNCIONAL
# ============================

st.markdown("""
<style>
.button-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 25px;
}

/* Estilos base */
.button-wrapper button {
    background-color: #1B168C;              /* Azul Serfinanza */
    color: white;
    border: none;
    border-radius: 12px;
    padding: 14px 42px;
    font-size: 1.1em;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(27,22,140,0.3); /* sombra azul */
}

/* Hover con brillo rojo */
.button-wrapper button:hover {
    background-color: #F43B63;              /* Rojo Serfinanza */
    box-shadow: 0 0 20px rgba(244,59,99,0.7); /* brillo rojo */
    transform: scale(1.07);
}
</style>

<div class="button-wrapper">
    <button onclick="window.location.href='#'">🚀 INICIAR CHATBOT</button>
</div>
""", unsafe_allow_html=True)

# 🧭 VALIDACIÓN DE CÉDULA
# ============================
if st.session_state.get("start_chat"):
    st.markdown("<br>", unsafe_allow_html=True)
    cedula = st.text_input("🪪 Digita tu número de cédula (sin puntos ni caracteres especiales):")

    # Intentar cargar la base
    try:
        data = pd.read_excel("base_bot_serfinanza.xls")
    except Exception as e:
        st.error(f"Error al cargar la base: {e}")
        st.stop()

    if cedula:
        st.session_state["intentos"] += 1
        cliente = data[data["NUMERO_IDENTIFICACION"].astype(str) == cedula]

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
