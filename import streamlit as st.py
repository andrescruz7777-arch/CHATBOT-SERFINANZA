# ============================
# 🚀 BOTÓN SERFINANZA — CENTRADO + HOVER FUNCIONAL Y ACTIVO
# ============================

# CSS + estilo corporativo
st.markdown("""
<style>
.button-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 25px;
}

/* Estilos base */
div.stButton > button:first-child {
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
div.stButton > button:first-child:hover {
    background-color: #F43B63;              /* Rojo Serfinanza */
    box-shadow: 0 0 20px rgba(244,59,99,0.7); /* brillo rojo */
    transform: scale(1.07);
}
</style>
""", unsafe_allow_html=True)

# Botón funcional (Streamlit detecta clic)
st.markdown("<div class='button-wrapper'>", unsafe_allow_html=True)
start = st.button("🚀 INICIAR CHATBOT")
st.markdown("</div>", unsafe_allow_html=True)

# Activación real del flujo
if start:
    st.session_state["start_chat"] = True
    st.session_state["intentos"] = 0


# ============================
# 🧭 VALIDACIÓN DE CÉDULA + BOTÓN CONTINUAR
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
