from src.db.conector_db import ConectorDB
from src.utils.logger import logger

def inicializar_db():
    """Crea las tablas necesarias para la clínica veterinaria si no existen."""
    db = ConectorDB("clinica.db")

    tablas = {
        "clientes": """
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT
            );
        """,
        "veterinarios": """
            CREATE TABLE IF NOT EXISTS veterinarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                especialidad TEXT,
                telefono TEXT
            );
        """,
        "mascotas": """
            CREATE TABLE IF NOT EXISTS mascotas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                especie TEXT,
                edad INTEGER,
                duenio_id INTEGER,
                FOREIGN KEY (duenio_id) REFERENCES clientes(id)
            );
        """
    }

    try:
        for nombre, sql in tablas.items():
            db.ejecutar(sql)
            logger.info(f"Tabla '{nombre}' verificada o creada correctamente ✅")

        print("Base de datos inicializada correctamente.")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
        print(f"Error al inicializar la base de datos: {e}")
