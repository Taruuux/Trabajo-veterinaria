import streamlit as st
from datetime import date
from api import API


st.title("🏥 Clínica Veterinaria — Panel")


# Datos agregados
owners = API.list_owners()
pets = API.list_pets()


today = date.today().isoformat()
appts_today = API.list_appointments(day=today)


col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Propietarios", len(owners))
with col2:
    st.metric("Mascotas", len(pets))
with col3:
    st.metric("Citas de hoy", len(appts_today))


st.markdown("### Citas de hoy")
if not appts_today:
    st.info("No hay citas para hoy")
else:
    for a in appts_today:
     with st.container(border=True):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.write("**Mascota**:", a["pet_id"]) # opcional: resolver nombre con un map
            st.write("Vet:", a["vet"])
        with col2:
            st.write("Motivo:", a.get("motivo", ""))
            st.write("Hora:", f"{a['hora_inicio']} - {a['hora_fin']}")
        with col3:
            st.write("Estado:", a.get("estado", ""))