import streamlit as st
from datetime import date, time
from api import API


st.title("📅 Citas")


owners = API.list_owners()
owner_by_id = {o["id"]: o for o in owners}


pets = API.list_pets()
pet_label_to_id = {
f"{p['nombre']} ({owner_by_id.get(p['owner_id'], {}).get('nombre', '—')})": p["id"]
for p in pets
}


if not pets:
    st.warning("No hay mascotas registradas todavía.")
else:
    with st.expander("➕ Crear cita"):
        with st.form("form_appt"):
            pet_label = st.selectbox("Mascota", list(pet_label_to_id.keys()))
            vet = st.text_input("Veterinario/a", "Dra. López")
            fecha = st.date_input("Fecha", date.today())
            hora_inicio = st.time_input("Hora inicio", time(10, 0))
            hora_fin = st.time_input("Hora fin", time(10, 30))
            motivo = st.text_area("Motivo", "Consulta general")
            submitted = st.form_submit_button("Guardar cita")


        if submitted:
            try:
                API.create_appointment({
                "pet_id": pet_label_to_id[pet_label],
                "vet": vet,
                "fecha": fecha.isoformat(),
                "hora_inicio": hora_inicio.strftime("%H:%M:%S"),
                "hora_fin": hora_fin.strftime("%H:%M:%S"),
                "motivo": motivo,
                "estado": "pendiente",
                })
                st.success("Cita creada")
            except ValueError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Error: {e}")


st.subheader("Citas del día")


today_iso = date.today().isoformat()
appts = API.list_appointments(day=today_iso)
if not appts:
    st.info("No hay citas para hoy.")
else:
    for a in appts:
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            with col1:
                st.write("**Mascota**:", a["pet_id"]) # opcional: resolver nombre
                st.write("Prop:", owner_by_id.get(next((p['owner_id'] for p in pets if p['id']==a['pet_id']), None), {}).get('nombre', '—'))
            with col2:
                st.write("Vet:", a["vet"])
                st.write("Motivo:", a.get("motivo", ""))
            with col3:
                st.write("Hora:", f"{a['hora_inicio']} - {a['hora_fin']}")
                st.write("Estado:", a.get("estado", ""))
            with col4:
                if st.button("Marcar atendida", key=f"att_{a['id']}"):
                    a["estado"] = "atendida"
                    API.update_appointment(a["id"], a)
                    st.rerun()