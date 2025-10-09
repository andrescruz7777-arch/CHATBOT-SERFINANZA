import streamlit as st
import pandas as pd

# ============================
# Configuración inicial
# ============================
st.set_page_config(page_title="🤖 Chatbot IA - Serfinanza", layout="centered")

st.image("imagenes/logo_contacto.png", width=220)  # Puedes cambiar por el logo que envíes
st.title("💬 Hola, soy Andrés")
st.caption("Asistente Virtual IA de Contacto Solutions — aliado estratégico de Banco Serfinanza")

st.markdown("""
Bienvenido 👋  
Soy tu asistente virtual diseñado para brindarte información actualizada sobre tus productos y opciones de negociación.  
Por favor, digita tu número de cédula **sin puntos ni caracteres especiales** para iniciar tu consulta.
""")

# ============================
# Cargar base de datos
# ============================
try:
    data = pd.read_excel("data/base_bot_serfinanza.xls")
except Exception as e:
    st.error(f"Error al cargar la base: {e}")
    st.stop()

# ============================
# Flujo principal
# ============================
if st.button("🚀 INICIAR CHATBOT"):
    st.session_state["start_chat"] = True
    st.session_state["intentos"] = 0  # Contador de intentos

if st.session_state.get("start_chat"):
    cedula = st.text_input("🪪 Ingresa tu número de cédula:")

    if cedula:
        st.session_state["intentos"] += 1
        cliente = data[data["NUMERO_IDENTIFICACION"].astype(str) == cedula]

        if not cliente.empty:
            st.success(f"✅ Perfecto, encontramos información asociada al documento {cedula}.")
            # Aquí se pasa al siguiente paso: mostrar obligaciones, estrategias, etc.
        else:
            if st.session_state["intentos"] == 1:
                st.warning("⚠️ No encontramos el número ingresado en nuestra base de datos. "
                           "Por favor verifica y vuelve a digitarlo sin espacios ni caracteres especiales.")
            elif st.session_state["intentos"] >= 2:
                st.error("❌ El número ingresado no se encuentra registrado. "
                         "Te invitamos a comunicarte con nuestros asesores para validar tu información:")
                st.markdown("""
                📞 **601 390 6300** opción 2  
                💼 **Contacto Solutions S.A.S.**
                """)
                st.stop()
