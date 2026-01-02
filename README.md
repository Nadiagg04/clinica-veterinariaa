# TRABAJO FINAL CLINICA VETERINARIA


Integrantes:

* Nadia González
* David Jesús Martín

Cómo ejecutar:

1. Crea un entorno virtual: python -m venv .venv
2. Instalar dependencias: pip install -r requirements.txt
3. Inicializar base de datos: python -m src.db.inicializador
4. Ejecutar Streamlit: streamlit run app/app.py



Características Principales

Sistema de Seguridad

\- Autenticación de usuarios con base de datos SQLite

\- Roles diferenciados: Administrador, Veterinario, Asistente

\- Registro de nuevos usuarios con activación por administrador

\- Contraseñas encriptadas con hash SHA-256



Módulos del Sistema

\- Dashboard con métricas y actividad reciente

\- Gestión de Clientes (CRUD completo)

\- Gestión de Veterinarios (CRUD completo)

\- Gestión de Mascotas (CRUD completo)

\- Registro de Atenciones Médicas

\- Panel de Administración para gestión de usuarios



Interfaz de Usuario

\- Interfaz moderna con Streamlit

\- Diseño responsive para todos los dispositivos

\- Navegación intuitiva con sidebar

\- Mensajes de feedback visuales



