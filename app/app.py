import streamlit as st
import pandas as pd
import hashlib
import sqlite3
import os
from datetime import datetime

# ===================== CONFIGURACIÓN INICIAL =====================
st.set_page_config(
    page_title="Clínica Veterinaria",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== BASE DE DATOS DE USUARIOS =====================
def init_usuario_db():
    """Inicializa la base de datos de usuarios"""
    # Crear directorio database si no existe
    os.makedirs("database", exist_ok=True)
    
    conn = sqlite3.connect("database/usuarios.db")
    cursor = conn.cursor()
    
    # Tabla de usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        nombre TEXT NOT NULL,
        rol TEXT DEFAULT 'veterinario',
        email TEXT,
        activo INTEGER DEFAULT 1,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Verificar si ya existen usuarios
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        # Crear usuarios iniciales
        usuarios_iniciales = [
            ('admin', hash_password('admin123'), 'Administrador Principal', 'admin', 'admin@veterinaria.com'),
            ('vet1', hash_password('vet123'), 'Dr. Carlos López', 'veterinario', 'vet1@clinicavet.com'),
            ('vet2', hash_password('vet456'), 'Dra. Ana Martínez', 'veterinario', 'vet2@clinicavet.com')
        ]
        
        cursor.executemany(
            'INSERT INTO usuarios (username, password, nombre, rol, email) VALUES (?, ?, ?, ?, ?)',
            usuarios_iniciales
        )
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Crea hash de la contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verifica la contraseña"""
    return hash_password(password) == hashed

# ===================== FUNCIÓN PARA REGISTRAR USUARIOS =====================
def registrar_usuario(username, password, nombre, email=None, rol='veterinario'):
    """Registra un nuevo usuario en la base de datos"""
    conn = sqlite3.connect("database/usuarios.db")
    cursor = conn.cursor()
    
    try:
        # Verificar si el usuario ya existe
        cursor.execute("SELECT id FROM usuarios WHERE username = ? OR email = ?", 
                      (username, email))
        if cursor.fetchone():
            conn.close()
            return False, "El nombre de usuario o email ya están registrados"
        
        # Insertar nuevo usuario (activo por defecto)
        cursor.execute(
            """INSERT INTO usuarios (username, password, nombre, email, rol, activo) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (username, hash_password(password), nombre, email, rol, 1)
        )
        
        conn.commit()
        conn.close()
        return True, "¡Usuario registrado exitosamente! Ya puedes iniciar sesión."
    except sqlite3.Error as e:
        conn.close()
        return False, f"Error en la base de datos: {str(e)}"

# ===================== FUNCIONES DE AUTENTICACIÓN =====================
def check_login(username, password):
    """Verifica las credenciales del usuario"""
    conn = sqlite3.connect("database/usuarios.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, username, password, nombre, rol FROM usuarios WHERE username = ? AND activo = 1",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    
    if user and verify_password(password, user['password']):
        return {
            'id': user['id'],
            'username': user['username'],
            'nombre': user['nombre'],
            'rol': user['rol']
        }
    return None

def mostrar_login():
    """Muestra el formulario de login"""
    with st.container():
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.subheader("Iniciar Sesión")
            
            username = st.text_input("Usuario", placeholder="Ingrese su nombre de usuario")
            password = st.text_input("Contraseña", type="password", placeholder="Ingrese su contraseña")
            
            col1, col2 = st.columns(2)
            with col1:
                remember = st.checkbox("Recordar mi sesión", value=True)
            
            submit = st.form_submit_button("Acceder al Sistema", type="primary", use_container_width=True)
            
            if submit:
                if not username or not password:
                    st.error("Por favor ingrese usuario y contraseña")
                else:
                    user = check_login(username, password)
                    if user:
                        st.session_state['logged_in'] = True
                        st.session_state['user'] = user
                        st.success(f"¡Bienvenido, {user['nombre']}!")
                        st.rerun()
                    else:
                        st.error("Usuario o contraseña incorrectos")
        
        # Credenciales de demostración
        with st.expander("Credenciales de prueba", expanded=False):
            st.markdown("""
            <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #4CAF50;">
            <p><strong>Administrador:</strong></p>
            <p>Usuario: <code>admin</code></p>
            <p>Contraseña: <code>admin123</code></p>
            <p><strong>Veterinarios:</strong></p>
            <p>Usuario: <code>vet1</code> / <code>vet2</code></p>
            <p>Contraseña: <code>vet123</code> / <code>vet456</code></p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def mostrar_registro():
    """Muestra el formulario de registro"""
    with st.container():
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        with st.form("register_form"):
            st.subheader("Crear Nueva Cuenta")
            
            nombre = st.text_input("Nombre completo", placeholder="Ej: Dr. Carlos López")
            email = st.text_input("Correo electrónico", placeholder="ejemplo@clinicavet.com")
            username = st.text_input("Nombre de usuario", placeholder="Elige un nombre de usuario único")
            password = st.text_input("Contraseña", type="password", placeholder="Mínimo 6 caracteres")
            confirm_password = st.text_input("Confirmar contraseña", type="password", placeholder="Repite tu contraseña")
            
            rol = st.selectbox("Tipo de cuenta", 
                             ["veterinario", "asistente", "recepcionista"],
                             help="Los usuarios 'admin' solo pueden ser creados por administradores")
            
            col1, col2 = st.columns(2)
            with col1:
                aceptar_terminos = st.checkbox("Acepto los términos", value=True)
            
            submit = st.form_submit_button("Crear Mi Cuenta", type="primary", use_container_width=True)
            
            if submit:
                # Validaciones
                if not all([nombre, email, username, password, confirm_password]):
                    st.error("Por favor complete todos los campos")
                elif password != confirm_password:
                    st.error("Las contraseñas no coinciden")
                elif len(password) < 6:
                    st.error("La contraseña debe tener al menos 6 caracteres")
                elif not aceptar_terminos:
                    st.error("Debe aceptar los términos y condiciones")
                else:
                    # Intentar registrar
                    success, message = registrar_usuario(username, password, nombre, email, rol)
                    if success:
                        st.success(message)
                        # Esperar 2 segundos y cambiar a login
                        st.session_state['current_tab'] = 'login'
                        st.rerun()
                    else:
                        st.error(f"Error: {message}")
        
        # Información importante
        with st.expander("ℹ️ Información sobre el registro", expanded=False):
            st.markdown("""
            **Proceso de registro:**
            1. Complete el formulario con sus datos
            2. Su cuenta será creada inmediatamente
            3. Puede iniciar sesión con sus credenciales
            
            **Nota importante:**
            - Las cuentas de tipo "admin" solo pueden ser creadas por administradores existentes.
            - Si tiene problemas, contacte al administrador del sistema.
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)

def login_page():
    """Página principal con Login y Sign Up"""
    
    # Inicializar estado de pestaña
    if 'current_tab' not in st.session_state:
        st.session_state['current_tab'] = 'login'
    
    # CSS mejorado
    st.markdown("""
    <style>
    .main-container {
        max-width: 800px;
        margin: 50px auto;
        padding: 20px;
    }
    .header-container {
        text-align: center;
        margin-bottom: 40px;
    }
    .tab-buttons {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-bottom: 30px;
    }
    .tab-button {
        padding: 12px 40px;
        border: none;
        background: #f0f0f0;
        cursor: pointer;
        font-size: 16px;
        font-weight: 500;
        color: #666;
        border-radius: 8px;
        transition: all 0.3s;
    }
    .tab-button:hover {
        background: #e0e0e0;
        transform: translateY(-2px);
    }
    .tab-button.active {
        background: #4CAF50;
        color: white;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
    }
    .form-container {
        background: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-top: 20px;
    }
    .logo {
        font-size: 48px;
        margin-bottom: 10px;
    }
    .footer {
        text-align: center;
        margin-top: 30px;
        color: #666;
        font-size: 0.9em;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Encabezado
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    st.markdown('<div class="logo">🐾</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align: center;">Clínica Veterinaria</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">Sistema de Gestión Integral</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botones de pestaña
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.columns(2)
        with tab1:
            if st.button("🔐 Iniciar Sesión", 
                        use_container_width=True,
                        type="primary" if st.session_state['current_tab'] == 'login' else "secondary"):
                st.session_state['current_tab'] = 'login'
                st.rerun()
        with tab2:
            if st.button("📝 Registrarse", 
                        use_container_width=True,
                        type="primary" if st.session_state['current_tab'] == 'register' else "secondary"):
                st.session_state['current_tab'] = 'register'
                st.rerun()
    
    # Mostrar formulario según pestaña seleccionada
    if st.session_state['current_tab'] == 'login':
        mostrar_login()
    else:
        mostrar_registro()
    
    # Pie de página
    st.markdown('<div class="footer">', unsafe_allow_html=True)
    st.markdown('---')
    st.markdown('<p>© 2024 Clínica Veterinaria. Todos los derechos reservados.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def logout():
    """Cierra la sesión"""
    st.session_state['logged_in'] = False
    st.session_state['user'] = None
    st.rerun()

# ===================== PÁGINA PRINCIPAL =====================
def main_app():
    """Aplicación principal después del login"""
    # Importar aquí para evitar errores si no hay login
    from src.servicios.servicio_veterinario import ServicioVeterinario
    from src.modelos.cliente import Cliente
    from src.modelos.veterinario import Veterinario
    from src.modelos.mascota import Mascota
    
    servicio = ServicioVeterinario()
    user = st.session_state['user']
    
    # Sidebar con información del usuario
    with st.sidebar:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; 
                    border-radius: 10px; 
                    color: white; 
                    margin-bottom: 20px;">
            <h3>¡Hola, {user['nombre']}!</h3>
            <p>Rol: {user['rol'].capitalize()}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Cerrar Sesión", use_container_width=True):
            logout()
        
        st.markdown("---")
        
        # Menú de navegación
        menu_options = ["Dashboard", "Clientes", "Veterinarios", "Mascotas", "Atenciones"]
        
        if user['rol'] == 'admin':
            menu_options.append("Administración")
        
        choice = st.radio(
            "Navegación",
            menu_options,
            label_visibility="collapsed"
        )
    
    # ===================== DASHBOARD =====================
    if choice == "Dashboard":
        st.title("Dashboard")
        
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        try:
            clientes = servicio.listar_clientes()
            with col1:
                st.metric("Clientes", len(clientes))
        except:
            with col1:
                st.metric("Clientes", 0)
        
        try:
            mascotas = servicio.listar_mascotas()
            with col2:
                st.metric("Mascotas", len(mascotas))
        except:
            with col2:
                st.metric("Mascotas", 0)
        
        try:
            veterinarios = servicio.listar_veterinarios()
            with col3:
                st.metric("Veterinarios", len(veterinarios))
        except:
            with col3:
                st.metric("Veterinarios", 0)
        
        with col4:
            st.metric("Tu Rol", user['rol'].capitalize())
        
        # Sección de actividad reciente
        st.markdown("---")
        st.subheader("Actividad Reciente")
        
        try:
            atenciones = servicio.listar_atenciones()
            if atenciones:
                for a in atenciones[:5]:
                    with st.expander(f"{a[1]} - {a[2]} (Dueño: {a[3]})"):
                        st.write(f"Nota: {a[4]}")
            else:
                st.info("No hay atenciones registradas")
        except Exception as e:
            st.warning(f"No se pudieron cargar las atenciones: {str(e)}")
    
    # ===================== CLIENTES =====================
    elif choice == "Clientes":
        st.title("Gestión de Clientes")
        
        # Pestañas para organización
        tab1, tab2 = st.tabs(["Lista de Clientes", "Nuevo Cliente"])
        
        with tab1:
            st.subheader("Clientes Registrados")
            try:
                clientes = servicio.listar_clientes()
                if clientes:
                    df_clientes = pd.DataFrame(clientes, columns=["ID", "Nombre", "Teléfono"])
                    
                    # Buscador
                    search = st.text_input("Buscar cliente por nombre:")
                    if search:
                        df_clientes = df_clientes[df_clientes['Nombre'].str.contains(search, case=False)]
                    
                    st.dataframe(
                        df_clientes,
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Estadísticas
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Clientes", len(df_clientes))
                else:
                    st.info("No hay clientes registrados")
            except Exception as e:
                st.error(f"Error al cargar clientes: {str(e)}")
        
        with tab2:
            st.subheader("Agregar Nuevo Cliente")
            with st.form("nuevo_cliente_form"):
                nombre = st.text_input("Nombre completo", placeholder="Ej: Juan Pérez")
                telefono = st.text_input("Teléfono", placeholder="Ej: +54 9 11 1234-5678")
                
                col1, col2 = st.columns(2)
                with col1:
                    submit = st.form_submit_button("Guardar Cliente", type="primary")
                with col2:
                    reset = st.form_submit_button("Limpiar")
                
                if submit:
                    if nombre and telefono:
                        try:
                            cliente = Cliente(nombre, telefono)
                            servicio.agregar_cliente(cliente)
                            st.success(f"Cliente '{nombre}' guardado correctamente")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    else:
                        st.warning("Por favor complete todos los campos")
    
    # ===================== VETERINARIOS =====================
    elif choice == "Veterinarios":
        st.title("Gestión de Veterinarios")
        
        # Solo administradores pueden agregar veterinarios
        if user['rol'] != 'admin':
            st.warning("Solo los administradores pueden gestionar veterinarios")
            st.stop()
        
        tab1, tab2 = st.tabs(["Lista de Veterinarios", "Nuevo Veterinario"])
        
        with tab1:
            st.subheader("Veterinarios Registrados")
            try:
                vets = servicio.listar_veterinarios()
                if vets:
                    df_vets = pd.DataFrame(vets, columns=["ID", "Nombre", "Especialidad", "Teléfono"])
                    st.dataframe(df_vets, use_container_width=True, hide_index=True)
                else:
                    st.info("No hay veterinarios registrados")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        with tab2:
            st.subheader("Agregar Nuevo Veterinario")
            with st.form("nuevo_veterinario_form"):
                nombre = st.text_input("Nombre del veterinario")
                especialidad = st.text_input("Especialidad")
                telefono = st.text_input("Teléfono")
                
                submit = st.form_submit_button("Guardar Veterinario", type="primary")
                
                if submit:
                    if nombre and especialidad and telefono:
                        try:
                            vet = Veterinario(nombre, especialidad, telefono)
                            servicio.agregar_veterinario(vet)
                            st.success(f"Veterinario '{nombre}' guardado correctamente")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    else:
                        st.warning("Debes completar todos los campos")
    
    # ===================== MASCOTAS =====================
    elif choice == "Mascotas":
        st.title("Gestión de Mascotas")
        
        tab1, tab2 = st.tabs(["Lista de Mascotas", "Nueva Mascota"])
        
        with tab1:
            st.subheader("Mascotas Registradas")
            try:
                mascotas = servicio.listar_mascotas()
                if mascotas:
                    df_mascotas = pd.DataFrame(mascotas, columns=["ID", "Nombre", "Especie", "Edad", "Dueño ID"])
                    st.dataframe(df_mascotas, use_container_width=True, hide_index=True)
                else:
                    st.info("No hay mascotas registradas")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        with tab2:
            st.subheader("Agregar Nueva Mascota")
            try:
                clientes = servicio.listar_clientes()
                if not clientes:
                    st.error("No hay clientes registrados. Primero registre un cliente.")
                    st.stop()
                
                with st.form("nueva_mascota_form"):
                    nombre = st.text_input("Nombre de la mascota")
                    especie = st.selectbox("Especie", ["Perro", "Gato", "Conejo", "Ave", "Reptil", "Otro"])
                    edad = st.number_input("Edad", min_value=0, max_value=50, value=1)
                    
                    cliente_options = {f"{c[1]} (Tel: {c[2]})": c[0] for c in clientes}
                    duenio_seleccionado = st.selectbox("Selecciona el dueño", list(cliente_options.keys()))
                    duenio_id = cliente_options[duenio_seleccionado]
                    
                    submit = st.form_submit_button("Guardar Mascota", type="primary")
                    
                    if submit:
                        if nombre:
                            try:
                                mascota = Mascota(nombre, especie, edad, duenio_id)
                                servicio.agregar_mascota(mascota)
                                st.success(f"Mascota '{nombre}' guardada correctamente")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
                        else:
                            st.warning("Debes completar todos los campos")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # ===================== ATENCIONES =====================
    elif choice == "Atenciones":
        st.title("Gestión de Atenciones")
        
        tab1, tab2 = st.tabs(["Historial de Atenciones", "Nueva Atención"])
        
        with tab1:
            st.subheader("Historial de Atenciones")
            try:
                atenciones = servicio.listar_atenciones()
                if atenciones:
                    for a in atenciones:
                        with st.expander(f"{a[1]} - {a[2]} (Dueño: {a[3]})"):
                            st.write(f"ID Atención: {a[0]}")
                            st.write(f"Fecha: {a[1]}")
                            st.write(f"Mascota: {a[2]}")
                            st.write(f"Dueño: {a[3]}")
                            st.write(f"Nota: {a[4]}")
                else:
                    st.info("No hay atenciones registradas")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        with tab2:
            st.subheader("Registrar Nueva Atención")
            try:
                # Selección de veterinarios
                vets = servicio.listar_veterinarios()
                if not vets:
                    st.error("No hay veterinarios registrados")
                    st.stop()
                
                vet_options = {f"{v[1]} (Especialidad: {v[2]})": v[0] for v in vets}
                vet_seleccionado = st.selectbox("Selecciona el veterinario", list(vet_options.keys()))
                veterinario_id = vet_options[vet_seleccionado]
                
                # Selección de mascotas
                mascotas = servicio.listar_mascotas()
                if not mascotas:
                    st.error("No hay mascotas registradas")
                    st.stop()
                
                masc_options = {f"{m[1]} (Especie: {m[2]})": m[0] for m in mascotas}
                masc_seleccionada = st.selectbox("Selecciona la mascota", list(masc_options.keys()))
                mascota_id = masc_options[masc_seleccionada]
                
                nota = st.text_area("Nota de la atención", height=100)
                
                if st.button("Registrar Atención", type="primary"):
                    if nota:
                        servicio.registrar_atencion(veterinario_id, mascota_id, nota)
                        st.success("Atención registrada correctamente")
                        st.rerun()
                    else:
                        st.warning("Por favor ingrese una nota de atención")
            except Exception as e:
                st.error(f"Error: {e}")
    
    # ===================== ADMINISTRACIÓN =====================
    elif choice == "Administración":
        st.title("Panel de Administración")
        
        if user['rol'] != 'admin':
            st.error("Acceso denegado. Solo administradores pueden acceder a esta sección.")
            st.stop()
        
        tab1, tab2 = st.tabs(["Usuarios", "Estadísticas"])
        
        with tab1:
            st.subheader("Gestión de Usuarios")
            
            # Botones de acción
            col1, col2, col3 = st.columns(3)
            with col1:
                ver_activos = st.checkbox("Mostrar solo activos", value=True)
            with col2:
                buscar_usuario = st.text_input("Buscar usuario", placeholder="Nombre o usuario")
            
            # Listar usuarios con opciones de gestión
            conn = sqlite3.connect("database/usuarios.db")
            
            # Construir consulta según filtros
            query = "SELECT id, username, nombre, rol, email, activo FROM usuarios"
            conditions = []
            
            if ver_activos:
                conditions.append("activo = 1")
            
            if buscar_usuario:
                conditions.append("(username LIKE ? OR nombre LIKE ? OR email LIKE ?)")
                params = [f"%{buscar_usuario}%", f"%{buscar_usuario}%", f"%{buscar_usuario}%"]
            else:
                params = []
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY nombre"
            
            if buscar_usuario:
                df_usuarios = pd.read_sql_query(query, conn, params=params)
            else:
                df_usuarios = pd.read_sql_query(query, conn)
            
            # Agregar columna de estado
            df_usuarios['Estado'] = df_usuarios['activo'].apply(lambda x: 'Activo' if x == 1 else 'Inactivo')
            
            # Mostrar tabla
            st.dataframe(
                df_usuarios[['username', 'nombre', 'rol', 'email', 'Estado']],
                use_container_width=True,
                hide_index=True
            )
            
            # Sección para gestionar usuarios
            st.subheader("Acciones de Usuario")
            
            # Seleccionar usuario para gestionar
            usuarios_lista = df_usuarios[['id', 'username', 'nombre']].values.tolist()
            usuario_opciones = {f"{u[2]} ({u[1]})": u[0] for u in usuarios_lista}
            
            if usuario_opciones:
                usuario_seleccionado = st.selectbox("Seleccionar usuario", list(usuario_opciones.keys()))
                usuario_id = usuario_opciones[usuario_seleccionado]
                
                # Obtener estado actual del usuario
                cursor = conn.cursor()
                cursor.execute("SELECT activo, rol FROM usuarios WHERE id = ?", (usuario_id,))
                usuario_info = cursor.fetchone()
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("Activar", use_container_width=True):
                        cursor.execute("UPDATE usuarios SET activo = 1 WHERE id = ?", (usuario_id,))
                        conn.commit()
                        st.success("Usuario activado")
                        st.rerun()
                
                with col2:
                    if st.button("Desactivar", use_container_width=True):
                        cursor.execute("UPDATE usuarios SET activo = 0 WHERE id = ?", (usuario_id,))
                        conn.commit()
                        st.success("Usuario desactivado")
                        st.rerun()
                
                with col3:
                    nuevo_rol = st.selectbox("Cambiar rol", ["veterinario", "asistente", "recepcionista", "admin"],
                                            key=f"rol_{usuario_id}")
                    if st.button("Cambiar Rol", use_container_width=True):
                        cursor.execute("UPDATE usuarios SET rol = ? WHERE id = ?", (nuevo_rol, usuario_id))
                        conn.commit()
                        st.success(f"Rol cambiado a {nuevo_rol}")
                        st.rerun()
                
                with col4:
                    if st.button("Eliminar", use_container_width=True, type="secondary"):
                        if st.checkbox(f"¿Está seguro de eliminar a {usuario_seleccionado}?"):
                            cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
                            conn.commit()
                            st.success("Usuario eliminado")
                            st.rerun()
            
            conn.close()
            
            # Sección para crear nuevo usuario (solo admin)
            with st.expander("Crear Nuevo Usuario (Admin)"):
                with st.form("admin_nuevo_usuario_form"):
                    st.markdown("**Crear usuario directamente**")
                    
                    nuevo_username = st.text_input("Usuario*")
                    nuevo_password = st.text_input("Contraseña*", type="password")
                    nuevo_nombre = st.text_input("Nombre completo*")
                    nuevo_email = st.text_input("Email")
                    nuevo_rol = st.selectbox("Rol*", ["veterinario", "asistente", "recepcionista", "admin"])
                    activo_inmediato = st.checkbox("Activar inmediatamente", value=True)
                    
                    if st.form_submit_button("Crear Usuario Directamente", type="primary"):
                        if nuevo_username and nuevo_password and nuevo_nombre:
                            # Verificar si el usuario ya existe
                            conn = sqlite3.connect("database/usuarios.db")
                            cursor = conn.cursor()
                            cursor.execute("SELECT id FROM usuarios WHERE username = ?", (nuevo_username,))
                            if cursor.fetchone():
                                st.error("El nombre de usuario ya existe")
                            else:
                                try:
                                    activo = 1 if activo_inmediato else 0
                                    cursor.execute(
                                        """INSERT INTO usuarios 
                                           (username, password, nombre, email, rol, activo) 
                                           VALUES (?, ?, ?, ?, ?, ?)""",
                                        (nuevo_username, hash_password(nuevo_password), 
                                         nuevo_nombre, nuevo_email, nuevo_rol, activo)
                                    )
                                    conn.commit()
                                    st.success(f"Usuario '{nuevo_username}' creado exitosamente")
                                    st.rerun()
                                except sqlite3.Error as e:
                                    st.error(f"Error: {str(e)}")
                                finally:
                                    conn.close()
                        else:
                            st.warning("Complete los campos obligatorios (*)")
        
        with tab2:
            st.subheader("Estadísticas del Sistema")
            
            col1, col2, col3 = st.columns(3)
            
            # Estadísticas de usuarios
            conn = sqlite3.connect("database/usuarios.db")
            usuarios_count = pd.read_sql_query("SELECT COUNT(*) as total FROM usuarios", conn).iloc[0,0]
            usuarios_por_rol = pd.read_sql_query("SELECT rol, COUNT(*) as cantidad FROM usuarios GROUP BY rol", conn)
            conn.close()
            
            with col1:
                st.metric("Total Usuarios", usuarios_count)
            
            with col2:
                vet_count = 0
                if not usuarios_por_rol.empty:
                    vet_rows = usuarios_por_rol[usuarios_por_rol['rol'] == 'veterinario']
                    if not vet_rows.empty:
                        vet_count = vet_rows.iloc[0]['cantidad']
                st.metric("Veterinarios", vet_count)
            
            with col3:
                admin_count = 0
                if not usuarios_por_rol.empty:
                    admin_rows = usuarios_por_rol[usuarios_por_rol['rol'] == 'admin']
                    if not admin_rows.empty:
                        admin_count = admin_rows.iloc[0]['cantidad']
                st.metric("Administradores", admin_count)

# ===================== APLICACIÓN PRINCIPAL =====================
def main():
    """Función principal de la aplicación"""
    
    # Inicializar base de datos de usuarios
    init_usuario_db()
    
    # Verificar si el usuario está logueado
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    # Mostrar página de login o aplicación principal
    if not st.session_state['logged_in']:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()