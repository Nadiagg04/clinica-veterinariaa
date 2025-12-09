import streamlit as st
from src.servicios.servicio_veterinario import ServicioVeterinario
from src.modelos.cliente import Cliente
from src.modelos.veterinario import Veterinario
from src.modelos.mascota import Mascota
import pandas as pd

# ===================== Inicialización =====================
st.set_page_config(page_title="Clínica Veterinaria", layout="wide")
servicio = ServicioVeterinario()

st.title(" Clínica Veterinaria")

menu = ["Clientes", "Veterinarios", "Mascotas", "Atenciones"]
choice = st.sidebar.selectbox("Menú", menu)

# ===================== CLIENTES =====================
if choice == "Clientes":
    st.subheader(" Clientes Registrados")
    try:
        clientes = servicio.listar_clientes()
        # Convertir a DataFrame para mejorar la visualización
        df_clientes = pd.DataFrame(clientes, columns=["ID", "Nombre", "Teléfono"])
        st.dataframe(df_clientes)  # Mejor que st.table, permite scroll y orden
    except Exception as e:
        st.error(str(e))

    with st.expander("Agregar Cliente"):
        nombre = st.text_input("Nombre")
        telefono = st.text_input("Teléfono")
        if st.button("Guardar Cliente"):
            if nombre and telefono:
                try:
                    cliente = Cliente(nombre, telefono)
                    servicio.agregar_cliente(cliente)
                    st.success(f"Cliente {nombre} guardado correctamente ")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Debes completar todos los campos")

# ===================== VETERINARIOS =====================
elif choice == "Veterinarios":
    st.subheader("Veterinarios Registrados")
    try:
        vets = servicio.listar_veterinarios()
        st.table(vets)
    except Exception as e:
        st.error(str(e))

    with st.expander("Agregar Veterinario"):
        nombre = st.text_input("Nombre del veterinario")
        especialidad = st.text_input("Especialidad")
        telefono = st.text_input("Teléfono")
        if st.button("Guardar Veterinario"):
            if nombre and especialidad and telefono:
                try:
                    vet = Veterinario(nombre, especialidad, telefono)
                    servicio.agregar_veterinario(vet)
                    st.success(f"Veterinario {nombre} guardado correctamente ")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Debes completar todos los campos")

# ===================== MASCOTAS =====================
elif choice == "Mascotas":
    st.subheader(" Mascotas Registradas")
    try:
        mascotas = servicio.listar_mascotas()
        st.table(mascotas)
    except Exception as e:
        st.error(str(e))

    with st.expander(" Agregar Mascota"):
        nombre = st.text_input("Nombre de la mascota")
        especie = st.text_input("Especie")
        edad = st.number_input("Edad", min_value=0, max_value=50)

        # Lista desplegable con clientes
        try:
            clientes = servicio.listar_clientes()
            cliente_options = {f"{c[1]} (ID:{c[0]})": c[0] for c in clientes}
            duenio_seleccionado = st.selectbox("Selecciona el dueño", list(cliente_options.keys()))
            duenio_id = cliente_options[duenio_seleccionado]
        except Exception as e:
            st.error("No hay clientes registrados.")
            duenio_id = None

        if st.button("Guardar Mascota"):
            if nombre and especie and duenio_id:
                try:
                    mascota = Mascota(nombre, especie, edad, duenio_id)
                    servicio.agregar_mascota(mascota)
                    st.success(f"Mascota {nombre} guardada correctamente ")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Debes completar todos los campos")

# ===================== ATENCIONES =====================
elif choice == "Atenciones":
    st.subheader("Registrar Atención")
    try:
        # Selección de veterinarios
        vets = servicio.listar_veterinarios()
        vet_options = {f"{v[1]} (ID:{v[0]})": v[0] for v in vets}
        vet_seleccionado = st.selectbox("Selecciona el veterinario", list(vet_options.keys()))
        veterinario_id = vet_options[vet_seleccionado]

        # Selección de mascotas
        mascotas = servicio.listar_mascotas()
        masc_options = {f"{m[1]} (ID:{m[0]})": m[0] for m in mascotas}
        masc_seleccionada = st.selectbox("Selecciona la mascota", list(masc_options.keys()))
        mascota_id = masc_options[masc_seleccionada]

        nota = st.text_area("Nota de la atención")
        if st.button("Registrar Atención"):
            servicio.registrar_atencion(veterinario_id, mascota_id, nota)
            st.success("Atención registrada correctamente ")
    except Exception as e:
        st.error(f"Error: {e}")

    st.subheader("Listado de Atenciones")
    try:
        atenciones = servicio.listar_atenciones()
        for a in atenciones:
            st.markdown(f"**ID:** {a[0]} | **Fecha:** {a[1]} | **Mascota:** {a[2]} | **Dueño:** {a[3]} | **Nota:** {a[4]}")
    except Exception as e:
        st.error(str(e))
