import streamlit as st
from api import API


st.title("👤 Propietarios")


with st.expander("➕ Añadir propietario"):
    

    with st.form("form_owner"):
        nombre = st.text_input("Nombre completo", "")
        telefono = st.text_input("Teléfono", "")
        email = st.text_input("Email", "")
        submitted = st.form_submit_button("Guardar")

    if submitted:
        nombre_clean = nombre.strip()
        tel_clean = telefono.strip() or None
        email_clean = email.strip() or None
        # si hay algo en email, exige formato básico
        if email_clean and "@" not in email_clean:
            st.error("Email inválido. Déjalo vacío o pon uno real.")
            st.stop()
        if not nombre_clean:
            st.error("El nombre es obligatorio.")
            st.stop()

        try:
            API.create_owner({"nombre": nombre_clean, "telefono": tel_clean, "email": email_clean})
            st.success("Propietario guardado")
            st.rerun()
        except Exception as e:
            st.error(str(e))
            st.stop()

    st.subheader("Listado")
    try:
        owners = API.list_owners()
    except Exception as e:
        st.error(str(e)); st.stop()
    st.table(owners)
