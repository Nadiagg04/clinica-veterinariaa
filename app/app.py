import sys
import os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.servicios.servicio_veterinario import ServicioVeterinario
from src.repositorio.repositorio_mascotas import RepositorioMascotas
from src.modelos.mascota import Mascota
from src.modelos.persona import Persona
from src.modelos.cliente import Cliente

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
            # Registrar al cliente (dueño)
            persona_dueño = Persona("Juan", "612345678")
            cliente = Cliente(persona_dueño)
            servicio.agregar_cliente(cliente)
            print("Cliente registrado correctamente")



            # Obtener el ID del dueño recién insertado
            cur = servicio.db.ejecutar(
                "SELECT id FROM clientes WHERE nombre = ? AND telefono = ? ORDER BY id DESC LIMIT 1",
                (nombre_dueño, telefono_dueño)
            )
            duenio_id = cur.fetchone()[0]

            # Crear la mascota con el id del dueño
            mascota = Mascota(nombre, especie, edad, duenio_id)
            servicio.agregar_mascota(mascota)

            st.success(f"Mascota registrada correctamente: {nombre}")
        else:
            st.error("Faltan datos obligatorios.")


elif menu == "Listar Mascotas":
    st.header("Listado de mascotas registradas")

    mascotas = servicio.listar_mascotas()
    
    if not mascotas:
        st.info("Aún no hay mascotas registradas.")
    else:
        for m in mascotas:
            id_, nombre, especie, edad, duenio = m
            st.write(f"**{nombre}** ({especie}, {edad} años) – Dueño: {duenio}")

