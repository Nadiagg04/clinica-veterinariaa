import streamlit as st
import pandas as pd

from src.servicios.servicio_veterinario import ServicioVeterinario
from src.modelos.cliente import Cliente
from src.modelos.veterinario import Veterinario
from src.modelos.mascota import Mascota

# ===================== CONFIGURACIÓN =====================
st.set_page_config(page_title="Clínica Veterinaria", layout="wide")
st.title("Clínica Veterinaria")

# Servicio principal
servicio = ServicioVeterinario()

# Menú lateral
menu = ["Clientes", "Veterinarios", "Mascotas", "Productos", "Atenciones"]
choice = st.sidebar.selectbox("Selecciona una sección", menu)


# =================================================================
# CLIENTES
# =================================================================
if choice == "Clientes":
    st.subheader("Clientes Registrados")

    try:
        clientes = servicio.listar_clientes()
        df_clientes = pd.DataFrame(clientes, columns=["ID", "Nombre", "Teléfono"])
        st.dataframe(df_clientes, use_container_width=True)
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
                    st.success(f"Cliente {nombre} registrado correctamente.")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Completa todos los campos.")


# =================================================================
# VETERINARIOS
# =================================================================
elif choice == "Veterinarios":
    st.subheader("Veterinarios Registrados")

    try:
        vets = servicio.listar_veterinarios()

        # Construcción flexible: funciona aunque cambien las columnas
        df_vets = pd.DataFrame(vets)

        # Opción elegante si tus datos SIEMPRE tienen estas columnas:
        # df_vets = pd.DataFrame(vets, columns=["ID", "Nombre", "Especialidad", "Telefono"])

        st.dataframe(df_vets, use_container_width=True)

    except Exception as e:
        st.error(f"Error cargando veterinarios: {e}")

    with st.expander("Agregar Veterinario"):
        nombre = st.text_input("Nombre del veterinario")
        especialidad = st.text_input("Especialidad")
        telefono = st.text_input("Teléfono")

        if st.button("Guardar Veterinario"):
            if nombre and especialidad:
                try:
                    vet = Veterinario(nombre, especialidad, telefono)
                    servicio.agregar_veterinario(vet)
                    st.success(f"Veterinario {nombre} registrado.")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Completa los campos obligatorios.")
# =================================================================
# MASCOTAS
# =================================================================
elif choice == "Mascotas":
    st.subheader("Mascotas Registradas")

    try:
        mascotas = servicio.listar_mascotas()
        df_mascotas = pd.DataFrame(mascotas, columns=["ID", "Nombre", "Especie", "Edad", "Dueño ID"])
        st.dataframe(df_mascotas, use_container_width=True)
    except Exception as e:
        st.error(str(e))

    # ================= GRÁFICO: Mascotas por especie =================
    if not df_mascotas.empty:
        try:
            st.subheader("Distribución de Mascotas por Especie")

            conteo = df_mascotas["Especie"].value_counts()

            st.bar_chart(conteo)
        except Exception as e:
            st.error(f"Error al generar gráfico: {e}")

    # ================= Formulario para agregar mascotas =================
    with st.expander("Agregar Mascota"):
        nombre = st.text_input("Nombre de la mascota")
        especie = st.text_input("Especie")
        edad = st.number_input("Edad", min_value=0, max_value=50)

        # Select con dueños
        try:
            clientes = servicio.listar_clientes()
            cliente_options = {f"{c[1]} (ID {c[0]})": c[0] for c in clientes}
            duenio_label = st.selectbox("Selecciona dueño", list(cliente_options.keys()))
            duenio_id = cliente_options[duenio_label]
        except:
            st.error("No hay clientes registrados.")
            duenio_id = None

        if st.button("Guardar Mascota"):
            if nombre and especie and duenio_id:
                try:
                    mascota = Mascota(nombre, especie, edad, duenio_id)
                    servicio.agregar_mascota(mascota)
                    st.success(f"Mascota {nombre} registrada.")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Completa todos los campos.")
# =================================================================
# PRODUCTOS
# =================================================================
elif choice == "Productos":
    st.subheader("Productos")

    st.info("Esta sección se habilitará cuando tengas el modelo Producto implementado.")


# =================================================================
# ATENCIONES
# =================================================================
elif choice == "Atenciones":
    st.subheader("Registrar Atención")

    try:
        # Veterinarios
        vets = servicio.listar_veterinarios()
        vet_options = {f"{v[1]} (ID {v[0]})": v[0] for v in vets}
        vet_label = st.selectbox("Selecciona veterinario", list(vet_options.keys()))
        veterinario_id = vet_options[vet_label]

        # Mascotas
        mascotas = servicio.listar_mascotas()
        masc_options = {f"{m[1]} (ID {m[0]})": m[0] for m in mascotas}
        masc_label = st.selectbox("Selecciona mascota", list(masc_options.keys()))
        mascota_id = masc_options[masc_label]

        nota = st.text_area("Nota clínica")

        if st.button("Registrar Atención"):
            servicio.registrar_atencion(veterinario_id, mascota_id, nota)
            st.success("Atención registrada correctamente.")

    except Exception as e:
        st.error(str(e))

    st.subheader("Historial de Atenciones")

    try:
        atenciones = servicio.listar_atenciones()
        df_at = pd.DataFrame(atenciones, columns=["ID", "Fecha", "Mascota", "Dueño", "Nota"])
        st.dataframe(df_at, use_container_width=True)
    except Exception as e:
        st.error(str(e))
