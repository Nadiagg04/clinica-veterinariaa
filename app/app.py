import sys
import os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.servicios.servicio_veterinario import ServicioVeterinario
from src.repositorio.repositorio_mascotas import RepositorioMascotas
from src.modelos.mascota import Mascota
from src.modelos.persona import Persona
from src.modelos.cliente import Cliente
from src.modelos.veterinario import Veterinario

repo = RepositorioMascotas()
servicio = ServicioVeterinario()

st.title("Clínica Veterinaria Patitas")

# Estilos personalizados para que la UI se ve más acorde al tema
st.markdown(
    """
    <style>
    :root { --brand:#2b9c6f; --accent:#7bd389; --bg:#f7fff7; --card:#ffffff; --muted:#6b6b6b; --text:#0b2f1a }
    .stApp { background: linear-gradient(180deg, #f0f8f2 0%, #f7fff7 100%); color: var(--text); }
    .stApp, .stApp * { color: var(--text) !important; }
    .header-sub { color:var(--muted); text-align:center; margin-top:-10px; margin-bottom:18px; font-size:0.95rem }
    .stSidebar { background: linear-gradient(180deg, #eaf7f0, #dff3e8); }
    .card { color: var(--text); background: var(--card); padding: 12px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.06); margin-bottom:10px; }
    .small-muted { color:var(--muted); font-size:0.9rem; }
    .stButton>button { background-color: var(--brand) !important; color: white !important; border-radius:6px !important; }
    .stAlert, .stInfo, .stSuccess { color: var(--text) !important; }
    /* Formularios: forzar fondo claro y texto oscuro para inputs/textarea/select */
    input[type="text"], input[type="number"], input[type="tel"], input[type="search"], textarea, select {
        background: #ffffff !important;
        color: var(--text) !important;
        border: 1px solid #d6e6dc !important;
        border-radius: 6px !important;
        padding: 8px !important;
    }
    textarea { min-height: 80px !important; }
    /* Placeholder color */
    ::placeholder { color: #7b8b7a !important; }
    /* Streamlit-specific wrappers */
    .stTextInput input, .stNumberInput input, .stTextArea textarea, .stSelectbox select {
        background: #ffffff !important;
        color: var(--text) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="header-sub">Gestión clínica — Patitas</div>', unsafe_allow_html=True)

menu = st.sidebar.radio("Menú", ["Inicio", "Registrar Mascota", "Listar Mascotas", "Listar Clientes", "Veterinarios", "Productos", "Cuentas"])


# Helper: rerun safely across Streamlit versions
def safe_rerun():
    if hasattr(st, 'experimental_rerun'):
        try:
            st.experimental_rerun()
        except Exception:
            # fallback: prompt manual refresh
            st.info('Recarga la página para aplicar cambios.')
    else:
        st.info('Recarga la página para aplicar cambios.')

if menu == "Inicio":
    st.header("Bienvenido a la Clínica Veterinaria")
    try:
        mascotas = servicio.listar_mascotas()
        total_mascotas = len(mascotas)
    except Exception:
        total_mascotas = 0

    try:
        clientes = servicio.listar_clientes()
        total_clientes = len(clientes)
    except Exception:
        total_clientes = 0

    st.subheader("Resumen")
    st.write(f"- Mascotas registradas: {total_mascotas}")
    st.write(f"- Clientes registrados: {total_clientes}")

elif menu == "Registrar Mascota":
    st.header("Registrar una mascota")

    nombre = st.text_input("Nombre de la mascota")
    especie = st.text_input("Especie")
    edad = st.number_input("Edad", min_value=0, max_value=50, step=1)
    nombre_dueño = st.text_input("Nombre del dueño")
    telefono_dueño = st.text_input("Teléfono del dueño")

    if st.button("Guardar"):
        if nombre and especie and nombre_dueño and telefono_dueño:
            # Registrar al cliente (dueño) usando los datos del formulario
            persona_dueño = Persona(nombre_dueño, telefono_dueño)
            cliente = Cliente(persona_dueño)
            try:
                servicio.agregar_cliente(cliente)
            except Exception as e:
                st.error(f"Error al registrar el cliente: {e}")
            else:
                # Obtener el ID del dueño recién insertado
                try:
                    cur = servicio.db.ejecutar(
                        "SELECT id FROM clientes WHERE nombre = ? AND telefono = ? ORDER BY id DESC LIMIT 1",
                        (nombre_dueño, telefono_dueño)
                    )
                    row = cur.fetchone()
                    if row:
                        duenio_id = row[0]
                    else:
                        st.error("No se pudo obtener el ID del dueño.")
                        duenio_id = None
                except Exception as e:
                    st.error(f"Error al consultar el dueño: {e}")
                    duenio_id = None

                if duenio_id is not None:
                    mascota = Mascota(nombre, especie, edad, duenio_id)
                    try:
                        servicio.agregar_mascota(mascota)
                        st.success(f"Mascota registrada correctamente: {nombre}")
                    except Exception as e:
                        st.error(f"Error al registrar la mascota: {e}")
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
            st.markdown(f"<div class='card'><strong>{nombre}</strong> <span class='small-muted'>({especie}, {edad} años)</span><br/><span class='small-muted'>Dueño: {duenio}</span></div>", unsafe_allow_html=True)
            if st.button("Eliminar", key=f"del_mascota_{id_}"):
                try:
                    servicio.eliminar_mascota(id_)
                    st.success(f"Mascota {nombre} eliminada")
                    safe_rerun()
                except Exception as e:
                    st.error(f"Error al eliminar mascota: {e}")

elif menu == "Listar Clientes":
    st.header("Listado de clientes registrados")
    try:
        clientes = servicio.listar_clientes()
        if not clientes:
            st.info("Aún no hay clientes registrados.")
        else:
            for c in clientes:
                id_, nombre, telefono = c
                st.markdown(f"<div class='card'><strong>{nombre}</strong><br/><span class='small-muted'>Tel: {telefono}</span></div>", unsafe_allow_html=True)
                if st.button("Eliminar", key=f"del_cliente_{id_}"):
                    try:
                        servicio.eliminar_cliente(id_)
                        st.success(f"Cliente {nombre} eliminado")
                        safe_rerun()
                    except Exception as e:
                        st.error(f"Error al eliminar cliente: {e}")
    except Exception as e:
        st.error(f"No se pudieron cargar los clientes: {e}")

elif menu == "Veterinarios":
    st.header("Veterinarios")

    accion = st.radio("Acción", ["Registrar Veterinario", "Listar Veterinarios", "Atender Mascota", "Historial de consultas"])

    if accion == "Registrar Veterinario":
        nombre = st.text_input("Nombre del veterinario")
        especialidad = st.text_input("Especialidad")
        telefono = st.text_input("Teléfono")
        precio_consulta = st.number_input("Precio de consulta (€)", min_value=0.0, value=0.0, step=0.5, format="%.2f")

        if st.button("Guardar veterinario"):
            if nombre and especialidad:
                vet = Veterinario(nombre, especialidad, telefono, precio_consulta)
                try:
                    servicio.agregar_veterinario(vet)
                    st.success(f"Veterinario registrado: {nombre}")
                except Exception as e:
                    st.error(f"Error al registrar el veterinario: {e}")
            else:
                st.error("Faltan datos obligatorios: nombre o especialidad.")

    elif accion == "Listar Veterinarios":
        try:
            veterinarios = servicio.listar_veterinarios()
            if not veterinarios:
                st.info("Aún no hay veterinarios registrados.")
            else:
                for v in veterinarios:
                    id_, nombre, especialidad, telefono, precio = v
                    st.markdown(f"<div class='card'><strong>{nombre}</strong><br/><span class='small-muted'>{especialidad} — Tel: {telefono}</span><div class='small-muted'>Precio consulta: {float(precio):.2f} €</div></div>", unsafe_allow_html=True)
                    if st.button("Eliminar", key=f"del_vet_{id_}"):
                        try:
                            servicio.eliminar_veterinario(id_)
                            st.success(f"Veterinario {nombre} eliminado")
                            safe_rerun()
                        except Exception as e:
                            st.error(f"Error al eliminar veterinario: {e}")
        except Exception as e:
            st.error(f"No se pudieron cargar los veterinarios: {e}")

    elif accion == "Atender Mascota":
        # Cargar veterinarios y mascotas desde la BD
        try:
            vets = servicio.listar_veterinarios()
        except Exception:
            vets = []

        try:
            mascotas = servicio.listar_mascotas()
        except Exception:
            mascotas = []

        if not vets:
            st.info("No hay veterinarios disponibles. Registra uno primero.")
        elif not mascotas:
            st.info("No hay mascotas registradas.")
        else:
            vet_options = {f"{v[0]} - {v[1]} ({v[2]})": v for v in vets}
            mas_options = {f"{m[0]} - {m[1]} ({m[2]})": m for m in mascotas}

            vet_sel = st.selectbox("Selecciona veterinario", list(vet_options.keys()))
            mas_sel = st.selectbox("Selecciona mascota", list(mas_options.keys()))

            # obtener precio por defecto del veterinario seleccionado
            selected_vrow = vet_options.get(vet_sel)

            nota = st.text_area("Notas / Observaciones (opcional)")
            default_precio = float(selected_vrow[4]) if selected_vrow and len(selected_vrow) > 4 else 0.0
            precio = st.number_input("Precio base (sin IVA)", min_value=0.0, value=default_precio, step=0.5, format="%.2f")
            iva_sel = st.selectbox("IVA (%)", [0, 5, 10, 21], index=3)

            if st.button("Atender"):
                vrow = vet_options[vet_sel]
                mrow = mas_options[mas_sel]

                # Crear instancias en memoria para la acción (no duplicar en BD)
                # vrow: (id, nombre, especialidad, telefono, precio_consulta)
                precio_vet = float(vrow[4]) if len(vrow) > 4 else 0.0
                vet_obj = Veterinario(vrow[1], vrow[2], vrow[3], precio_vet)
                # Attach an id attribute for tracking
                setattr(vet_obj, 'id', vrow[0])
                if all((getattr(v, 'id', None) != vrow[0] for v in servicio.veterinarios)):
                    servicio.veterinarios.append(vet_obj)

                # Crear mascota en memoria
                m_id, m_nombre, m_especie, m_edad, m_duenio = mrow
                mas_obj = Mascota(m_nombre, m_especie, m_edad, mrow[4])
                setattr(mas_obj, 'id', m_id)
                if all((getattr(m, 'id', None) != m_id for m in servicio.mascotas)):
                    servicio.mascotas.append(mas_obj)

                try:
                    resultado = servicio.atender_mascota(vet_obj, mas_obj)
                    # Registrar la atención en la BD (siempre que tengamos ids)
                    try:
                        servicio.registrar_atencion(vet_obj.id, mas_obj.id, nota or "", precio=float(precio), iva=float(iva_sel))
                    except Exception as e:
                        st.warning(f"Atención realizada pero no se pudo guardar el historial: {e}")

                    st.success(resultado)
                except Exception as e:
                    st.error(f"No fue posible atender la mascota: {e}")

    elif accion == "Historial de consultas":
        try:
            veterinarios = servicio.listar_veterinarios()
        except Exception:
            veterinarios = []

        if not veterinarios:
            st.info("No hay veterinarios registrados.")
        else:
            vet_map = {f"{v[0]} - {v[1]} ({v[2]})": v for v in veterinarios}
            sel = st.selectbox("Selecciona veterinario", list(vet_map.keys()))
            if st.button("Mostrar historial"):
                vrow = vet_map[sel]
                vid = vrow[0]
                try:
                    historial = servicio.listar_atenciones_por_veterinario(vid)
                    if not historial:
                        st.info("No hay atenciones registradas para este veterinario.")
                    else:
                        for a in historial:
                            at_id, fecha, mascota_nombre, duenio_nombre, nota, precio, iva = a
                            total = 0.0
                            try:
                                total = float(precio) * (1 + float(iva) / 100)
                            except Exception:
                                total = 0.0
                            st.markdown(f"<div class='card'><strong>{mascota_nombre}</strong> <span class='small-muted'>[{fecha}]</span><br/><span class='small-muted'>Dueño: {duenio_nombre}</span><div class='small-muted'>Nota: {nota}</div><div class='small-muted'>Precio: {float(precio):.2f} € — IVA: {float(iva):.0f}% — Total: {total:.2f} €</div></div>", unsafe_allow_html=True)
                            if st.button("Eliminar", key=f"del_at_{at_id}"):
                                try:
                                    servicio.eliminar_atencion(at_id)
                                    st.success("Atención eliminada")
                                    safe_rerun()
                                except Exception as e:
                                    st.error(f"Error al eliminar atención: {e}")
                except Exception as e:
                    st.error(f"Error al obtener historial: {e}")


elif menu == "Productos":
    st.header("Catálogo de Productos")

    with st.form(key="form_producto"):
        nombre = st.text_input("Nombre del producto")
        descripcion = st.text_area("Descripción (opcional)")
        precio = st.number_input("Precio (€)", min_value=0.0, value=0.0, step=0.5, format="%.2f")
        stock = st.number_input("Stock", min_value=0, value=0, step=1)
        submit = st.form_submit_button("Agregar producto")

    if submit:
        if nombre:
            try:
                servicio.agregar_producto(nombre, descripcion or "", float(precio), int(stock))
                st.success(f"Producto agregado: {nombre}")
            except Exception as e:
                st.error(f"Error al agregar producto: {e}")
        else:
            st.error("El nombre del producto es obligatorio.")

    st.subheader("Productos disponibles")
    try:
        productos = servicio.listar_productos()
        if not productos:
            st.info("Aún no hay productos en el catálogo.")
        else:
            for p in productos:
                pid, pnombre, pdesc, pprecio, pstock = p
                st.markdown(f"<div class='card'><strong>{pnombre}</strong><br/><span class='small-muted'>{pdesc}</span><div class='small-muted'>Precio: {float(pprecio):.2f} € — Stock: {int(pstock)}</div></div>", unsafe_allow_html=True)
                # low stock warning
                try:
                    if int(pstock) <= 5:
                        st.warning(f"Stock bajo: {int(pstock)} unidades")
                except Exception:
                    pass

                cols = st.columns([1,1,1,1])
                with cols[0]:
                    if st.button("Eliminar", key=f"del_prod_{pid}"):
                        try:
                            servicio.eliminar_producto(pid)
                            st.success("Producto eliminado")
                            safe_rerun()
                        except Exception as e:
                            st.error(f"Error al eliminar producto: {e}")
                with cols[1]:
                    qty_sell = st.number_input("Vender (cant)", min_value=1, value=1, step=1, key=f"qty_sell_{pid}")
                    if st.button("Vender", key=f"vender_{pid}"):
                        try:
                            nuevo = servicio.vender_producto(pid, int(qty_sell))
                            st.success(f"Venta registrada. Stock nuevo: {nuevo}")
                            safe_rerun()
                        except Exception as e:
                            st.error(f"Error al vender producto: {e}")
                with cols[2]:
                    qty_rep = st.number_input("Reponer (cant)", min_value=1, value=1, step=1, key=f"qty_rep_{pid}")
                    if st.button("Reponer", key=f"reponer_{pid}"):
                        try:
                            nuevo = servicio.reponer_producto(pid, int(qty_rep))
                            st.success(f"Stock actualizado: {nuevo}")
                            safe_rerun()
                        except Exception as e:
                            st.error(f"Error al reponer producto: {e}")
    except Exception as e:
        st.error(f"No se pudo cargar el catálogo de productos: {e}")


elif menu == "Cuentas":
    st.header("Cuentas Totales — Resumen Económico")

    try:
        valor_inventario = servicio.calcular_valor_inventario()
    except Exception as e:
        st.error(f"Error al calcular inventario: {e}")
        valor_inventario = 0.0

    try:
        ingresos_consultas = servicio.calcular_ingresos_consultas()
    except Exception as e:
        st.error(f"Error al calcular ingresos por consultas: {e}")
        ingresos_consultas = 0.0

    total_general = float(valor_inventario) + float(ingresos_consultas)

    st.subheader("Totales")
    st.markdown(f"<div class='card'><strong>Valor inventario:</strong> {valor_inventario:.2f} €<br/><strong>Ingresos por consultas:</strong> {ingresos_consultas:.2f} €<br/><strong>Total general:</strong> {total_general:.2f} €</div>", unsafe_allow_html=True)

    # Detalle por producto (valor por producto)
    st.subheader("Detalle inventario")
    try:
        productos = servicio.listar_productos()
        if not productos:
            st.info("No hay productos en el inventario.")
        else:
            for p in productos:
                pid, nombre, desc, precio, stock = p
                try:
                    valor = float(precio) * int(stock)
                except Exception:
                    valor = 0.0
                st.markdown(f"<div class='card'><strong>{nombre}</strong> — Stock: {int(stock)} — Precio: {float(precio):.2f} € — Valor: {valor:.2f} €</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error al listar productos para detalle: {e}")

    # Detalle por veterinario
    st.subheader("Ingresos por veterinario")
    try:
        vets_ing = servicio.listar_ingresos_por_veterinario()
        if not vets_ing:
            st.info("No hay veterinarios/ingresos registrados.")
        else:
            for v in vets_ing:
                vid, vnombre, consultas, subtotal, total_con_iva = v
                st.markdown(f"<div class='card'><strong>{vnombre}</strong> — Consultas: {consultas} — Subtotal: {float(subtotal):.2f} € — Total (IVA incluido): {float(total_con_iva):.2f} €</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error al listar ingresos por veterinario: {e}")

