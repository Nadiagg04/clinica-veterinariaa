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
                telefono TEXT,
                precio_consulta REAL DEFAULT 0
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
        ,
        "atenciones": """
            CREATE TABLE IF NOT EXISTS atenciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                veterinario_id INTEGER NOT NULL,
                mascota_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                nota TEXT,
<<<<<<< HEAD
                precio REAL DEFAULT 0,
                iva REAL DEFAULT 0,
=======
>>>>>>> 2a3e5dd4f6a3a59e1f31c7bac72313eb4ca87178
                FOREIGN KEY (veterinario_id) REFERENCES veterinarios(id),
                FOREIGN KEY (mascota_id) REFERENCES mascotas(id)
            );
        """
<<<<<<< HEAD
        ,
        "productos": """
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                precio REAL DEFAULT 0,
                stock INTEGER DEFAULT 0
            );
        """
=======
>>>>>>> 2a3e5dd4f6a3a59e1f31c7bac72313eb4ca87178
    }

    try:
        for nombre, sql in tablas.items():
            db.ejecutar(sql)
            logger.info(f"Tabla '{nombre}' verificada o creada correctamente")

        print("Base de datos inicializada correctamente.")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
        print(f"Error al inicializar la base de datos: {e}")


if __name__ == "__main__":
    inicializar_db()
