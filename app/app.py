import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import streamlit as st
from src.servicios.servicio_veterinario import ServicioVeterinario
from src.repositorio.repositorio_mascotas import RepositorioMascotas

repo = RepositorioMascotas()
servicio = ServicioVeterinario()


st.title("Clínica Veterinaria Patitas")

menu = st.sidebar.radio("Menú", ["Registrar Mascota", "Listar Mascotas"])

if menu == "Registrar Mascota":
    st.header("Registrar una mascota")

    nombre = st.text_input("Nombre de la mascota")
    especie = st.text_input("Especie")
    edad = st.number_input("Edad", min_value=0, max_value=50, step=1)
    nombre_dueño = st.text_input("Nombre del dueño")
    telefono_dueño = st.text_input("Teléfono del dueño")

    if st.button("Guardar"):
        if nombre and especie and nombre_dueño and telefono_dueño:
            mascota = servicio.registrar_mascota(
                nombre, especie, edad,
                nombre_dueño, telefono_dueño
            )
            st.success(f"✅ Mascota registrada: {mascota}")
        else:
            st.error("❌ Faltan datos obligatorios.")

elif menu == "Listar Mascotas":
    st.header("Listado de mascotas registradas")

    mascotas = servicio.listar_mascotas()
    
    if not mascotas:
        st.info("Aún no hay mascotas registradas.")
    else:
        for m in mascotas:
            st.write(f"🐶 **{m.nombre}** ({m.especie}, {m.edad} años) – Dueño: {m.dueño.nombre}")
