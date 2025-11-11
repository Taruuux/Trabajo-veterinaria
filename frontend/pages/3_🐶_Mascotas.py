import streamlit as st
from api import API


st.title("🐶 Mascotas")


owners = API.list_owners()
name_to_id = {o["nombre"]: o["id"] for o in owners}


with st.expander("➕ Añadir mascota"):
    with st.form("form_pet"):
        owner_name = st.selectbox("Propietario", list(name_to_id.keys()))
        nombre = st.text_input("Nombre mascota", "")
        especie = st.selectbox("Especie", ["perro", "gato", "otro"])
        submitted = st.form_submit_button("Guardar")


    if submitted:
        if not nombre:
            st.error("La mascota debe tener nombre.")
        else:
            try:
                API.create_pet({
                "owner_id": name_to_id[owner_name],
                "nombre": nombre,
                "especie": especie,
                })
                st.success("Mascota guardada")
            except Exception as e:
                st.error(f"Error: {e}")


st.subheader("Listado")
owner_filter = st.selectbox("Filtrar por propietario", ["(todas)"] + list(name_to_id.keys()))
owner_id = name_to_id.get(owner_filter) if owner_filter != "(todas)" else None
pets = API.list_pets(owner_id=owner_id)


# Opcional: mostrar con nombre de propietario
id_to_name = {o["id"]: o["nombre"] for o in owners}
rows = []
for p in pets:
    rows.append({
    "ID": p["id"],
    "Mascota": p["nombre"],
    "Especie": p["especie"],
    "Propietario": id_to_name.get(p["owner_id"], "—"),
    })


st.table(rows)