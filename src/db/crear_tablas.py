import sqlite3
import os

DB_PATH = "clinica.db"

def crear_tablas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS veterinarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            especialidad TEXT,
            telefono TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mascotas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            especie TEXT,
            edad INTEGER,
            duenio_id INTEGER,
            FOREIGN KEY(duenio_id) REFERENCES clientes(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atenciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            veterinario_id INTEGER NOT NULL,
            mascota_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            nota TEXT,
            FOREIGN KEY(veterinario_id) REFERENCES veterinarios(id),
            FOREIGN KEY(mascota_id) REFERENCES mascotas(id)
        )
    """)

    conn.commit()
    conn.close()
    print("[OK] Tablas creadas correctamente")

if __name__ == "__main__":
    crear_tablas()
