from src.db.conector_db import ConectorDB

db = ConectorDB("clinica.db")

sql_clientes = """
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL
);
"""

sql_mascotas = """
CREATE TABLE IF NOT EXISTS mascotas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    especie TEXT NOT NULL,
    edad INTEGER NOT NULL,
    dueño_id INTEGER,
    FOREIGN KEY (dueño_id) REFERENCES clientes(id)
);
"""

sql_veterinarios = """
CREATE TABLE IF NOT EXISTS veterinarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    especialidad TEXT NOT NULL,
    telefono TEXT NOT NULL
);
"""

db.ejecutar(sql_clientes)
db.ejecutar(sql_mascotas)
db.ejecutar(sql_veterinarios)

print("Base de datos creada correctamente ✔")
print("Iniciando creación de la base de datos...")

from src.db.conector_db import ConectorDB

db = ConectorDB("clinica.db")

sql_clientes = """
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL
);
"""

sql_mascotas = """
CREATE TABLE IF NOT EXISTS mascotas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    especie TEXT NOT NULL,
    edad INTEGER NOT NULL,
    dueño_id INTEGER,
    FOREIGN KEY (dueño_id) REFERENCES clientes(id)
);
"""

sql_veterinarios = """
CREATE TABLE IF NOT EXISTS veterinarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    especialidad TEXT NOT NULL,
    telefono TEXT NOT NULL
);
"""

db.ejecutar(sql_clientes)
db.ejecutar(sql_mascotas)
db.ejecutar(sql_veterinarios)

print("Base de datos creada correctamente")
print("Iniciando creación de la base de datos...")

from src.db.conector_db import ConectorDB

db = ConectorDB("clinica.db")

sql_clientes = """
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL
);
"""

sql_mascotas = """
CREATE TABLE IF NOT EXISTS mascotas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    especie TEXT NOT NULL,
    edad INTEGER NOT NULL,
    dueño_id INTEGER,
    FOREIGN KEY (dueño_id) REFERENCES clientes(id)
);
"""

sql_veterinarios = """
CREATE TABLE IF NOT EXISTS veterinarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    especialidad TEXT NOT NULL,
    telefono TEXT NOT NULL
);
"""


db.ejecutar(sql_clientes)
db.ejecutar(sql_mascotas)
db.ejecutar(sql_veterinarios)

print("Base de datos creada correctamente ")

sql_facturas = """
CREATE TABLE IF NOT EXISTS facturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    base REAL NOT NULL,
    iva REAL NOT NULL,
    total REAL NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);
"""
db.ejecutar(sql_facturas)

print("Tabla FACTURAS creada ✔")

sql_atenciones = """
CREATE TABLE IF NOT EXISTS atenciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    veterinario_id INTEGER NOT NULL,
    mascota_id INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    nota TEXT,
    FOREIGN KEY (veterinario_id) REFERENCES veterinarios(id),
    FOREIGN KEY (mascota_id) REFERENCES mascotas(id)
);
"""
