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
# 💬 MENSAJE DE BIENVENIDA
# ============================
st.markdown("<h1>💬 Hola, soy Andrés</h1>", unsafe_allow_html=True)
st.markdown("""
<div class="caption-text">
Soy tu Asistente Virtual IA de <b>Contacto Solutions</b>, aliado estratégico de <b>Banco Serfinanza</b>.  
Estoy aquí para brindarte información de tus productos y opciones de negociación.  
</div>
""", unsafe_allow_html=True)

# ============================
# 🚀 BOTÓN CENTRADO CON COLOR Y FUNCIÓN
# ============================
col1, col2, col3 = st.columns([1,2,1])
with col2:
    start = st.button("🚀 INICIAR CHATBOT")
    st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #1B168C;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 14px 36px;
            font-size: 1.1em;
            font-weight: 600;
            transition: 0.3s;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }
        div.stButton > button:first-child:hover {
            background-color: #F43B63;
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)

if start:
    st.session_state["start_chat"] = True
    st.session_state["intentos"] = 0

# ============================
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
