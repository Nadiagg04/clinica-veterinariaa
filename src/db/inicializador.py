from src.db.conector_db import ConectorDB
from src.utils.logger import logger

def precargar_datos(db: ConectorDB) -> None:
    """Inserta datos iniciales si las tablas están vacías."""
    try:
        # Clientes
        cur = db.ejecutar("SELECT COUNT(*) FROM clientes")
        clientes_count = cur.fetchone()[0]

        if clientes_count == 0:
            clientes = [
                ("María Pérez", "555-0101"),
                ("Juan López", "555-0202"),
                ("Ana Gómez", "555-0303"),
            ]
            cliente_ids = []
            for nombre, telefono in clientes:
                c = db.ejecutar(
                    "INSERT INTO clientes (nombre, telefono) VALUES (?, ?)",
                    (nombre, telefono),
                )
                cliente_ids.append(c.lastrowid)
            logger.info("Clientes de ejemplo insertados")
        else:
            # obtener algunos ids existentes para relacionar mascotas si se necesita
            cliente_ids = []
            cur = db.ejecutar("SELECT id FROM clientes LIMIT 3")
            for row in cur.fetchall():
                cliente_ids.append(row[0])

        # Veterinarios
        cur = db.ejecutar("SELECT COUNT(*) FROM veterinarios")
        vets_count = cur.fetchone()[0]
        if vets_count == 0:
            vets = [
                ("Dr. Carlos Ruiz", "Dermatología", "555-1001", 25.0),
                ("Dra. Laura Martínez", "Cardiología", "555-1002", 30.0),
            ]
            vet_ids = []
            for nombre, especialidad, telefono, precio in vets:
                c = db.ejecutar(
                    "INSERT INTO veterinarios (nombre, especialidad, telefono, precio_consulta) VALUES (?, ?, ?, ?)",
                    (nombre, especialidad, telefono, precio),
                )
                vet_ids.append(c.lastrowid)
            logger.info("Veterinarios de ejemplo insertados")
        else:
            vet_ids = []
            cur = db.ejecutar("SELECT id FROM veterinarios LIMIT 2")
            for row in cur.fetchall():
                vet_ids.append(row[0])

        # Mascotas
        cur = db.ejecutar("SELECT COUNT(*) FROM mascotas")
        pets_count = cur.fetchone()[0]
        if pets_count == 0 and cliente_ids:
            mascotas = [
                ("Toby", "Perro", 4, cliente_ids[0] if len(cliente_ids) > 0 else None),
                ("Mimi", "Gato", 2, cliente_ids[1] if len(cliente_ids) > 1 else None),
                ("Rex", "Perro", 7, cliente_ids[2] if len(cliente_ids) > 2 else None),
            ]
            pet_ids = []
            for nombre, especie, edad, duenio_id in mascotas:
                c = db.ejecutar(
                    "INSERT INTO mascotas (nombre, especie, edad, duenio_id) VALUES (?, ?, ?, ?)",
                    (nombre, especie, edad, duenio_id),
                )
                pet_ids.append(c.lastrowid)
            logger.info("Mascotas de ejemplo insertadas")
        else:
            pet_ids = []
            cur = db.ejecutar("SELECT id FROM mascotas LIMIT 3")
            for row in cur.fetchall():
                pet_ids.append(row[0])

        # Productos
        try:
            cur = db.ejecutar("SELECT COUNT(*) FROM productos")
            prod_count = cur.fetchone()[0]
        except Exception:
            prod_count = 0

        if prod_count == 0:
            productos = [
                ("Pipetas anti-pulgas", "Tratamiento tópico", 12.5, 50),
                ("Alimento Premium 1kg", "Comida balanceada para perros", 8.0, 30),
            ]
            for nombre, descripcion, precio, stock in productos:
                db.ejecutar(
                    "INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (?, ?, ?, ?)",
                    (nombre, descripcion, precio, stock),
                )
            logger.info("Productos de ejemplo insertados")

        # Atenciones (ejemplo: si hay vets y pets)
        if vet_ids and pet_ids:
            cur = db.ejecutar("SELECT COUNT(*) FROM atenciones")
            aten_count = cur.fetchone()[0]
            if aten_count == 0:
                import datetime

                fecha = datetime.datetime.now().isoformat()
                db.ejecutar(
                    "INSERT INTO atenciones (veterinario_id, mascota_id, fecha, nota, precio, iva) VALUES (?, ?, ?, ?, ?, ?)",
                    (vet_ids[0], pet_ids[0], fecha, "Chequeo general", 25.0, 4.0),
                )
                if len(vet_ids) > 1 and len(pet_ids) > 1:
                    db.ejecutar(
                        "INSERT INTO atenciones (veterinario_id, mascota_id, fecha, nota, precio, iva) VALUES (?, ?, ?, ?, ?, ?)",
                        (vet_ids[1], pet_ids[1], fecha, "Vacunación", 30.0, 4.8),
                    )
                logger.info("Atenciones de ejemplo insertadas")

    except Exception as e:
        logger.error(f"Error al precargar datos iniciales: {e}")


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
                precio REAL DEFAULT 0,
                iva REAL DEFAULT 0,
                FOREIGN KEY (veterinario_id) REFERENCES veterinarios(id),
                FOREIGN KEY (mascota_id) REFERENCES mascotas(id)
            );
        """
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
    }

    try:
        for nombre, sql in tablas.items():
            db.ejecutar(sql)
            logger.info(f"Tabla '{nombre}' verificada o creada correctamente")

        # Precarga de datos iniciales si las tablas están vacías
        precargar_datos(db)

        print("Base de datos inicializada correctamente.")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
        print(f"Error al inicializar la base de datos: {e}")


if __name__ == "__main__":
    inicializar_db()


def precargar_datos(db: ConectorDB) -> None:
    """Inserta datos iniciales si las tablas están vacías."""
    try:
        # Clientes
        cur = db.ejecutar("SELECT COUNT(*) FROM clientes")
        clientes_count = cur.fetchone()[0]

        if clientes_count == 0:
            clientes = [
                ("María Pérez", "555-0101"),
                ("Juan López", "555-0202"),
                ("Ana Gómez", "555-0303"),
            ]
            cliente_ids = []
            for nombre, telefono in clientes:
                c = db.ejecutar(
                    "INSERT INTO clientes (nombre, telefono) VALUES (?, ?)",
                    (nombre, telefono),
                )
                cliente_ids.append(c.lastrowid)
            logger.info("Clientes de ejemplo insertados")
        else:
            # obtener algunos ids existentes para relacionar mascotas si se necesita
            cliente_ids = []
            cur = db.ejecutar("SELECT id FROM clientes LIMIT 3")
            for row in cur.fetchall():
                cliente_ids.append(row[0])

        # Veterinarios
        cur = db.ejecutar("SELECT COUNT(*) FROM veterinarios")
        vets_count = cur.fetchone()[0]
        if vets_count == 0:
            vets = [
                ("Dr. Carlos Ruiz", "Dermatología", "555-1001", 25.0),
                ("Dra. Laura Martínez", "Cardiología", "555-1002", 30.0),
            ]
            vet_ids = []
            for nombre, especialidad, telefono, precio in vets:
                c = db.ejecutar(
                    "INSERT INTO veterinarios (nombre, especialidad, telefono, precio_consulta) VALUES (?, ?, ?, ?)",
                    (nombre, especialidad, telefono, precio),
                )
                vet_ids.append(c.lastrowid)
            logger.info("Veterinarios de ejemplo insertados")
        else:
            vet_ids = []
            cur = db.ejecutar("SELECT id FROM veterinarios LIMIT 2")
            for row in cur.fetchall():
                vet_ids.append(row[0])

        # Mascotas
        cur = db.ejecutar("SELECT COUNT(*) FROM mascotas")
        pets_count = cur.fetchone()[0]
        if pets_count == 0 and cliente_ids:
            mascotas = [
                ("Toby", "Perro", 4, cliente_ids[0] if len(cliente_ids) > 0 else None),
                ("Mimi", "Gato", 2, cliente_ids[1] if len(cliente_ids) > 1 else None),
                ("Rex", "Perro", 7, cliente_ids[2] if len(cliente_ids) > 2 else None),
            ]
            pet_ids = []
            for nombre, especie, edad, duenio_id in mascotas:
                c = db.ejecutar(
                    "INSERT INTO mascotas (nombre, especie, edad, duenio_id) VALUES (?, ?, ?, ?)",
                    (nombre, especie, edad, duenio_id),
                )
                pet_ids.append(c.lastrowid)
            logger.info("Mascotas de ejemplo insertadas")
        else:
            pet_ids = []
            cur = db.ejecutar("SELECT id FROM mascotas LIMIT 3")
            for row in cur.fetchall():
                pet_ids.append(row[0])

        # Productos
        try:
            cur = db.ejecutar("SELECT COUNT(*) FROM productos")
            prod_count = cur.fetchone()[0]
        except Exception:
            prod_count = 0

        if prod_count == 0:
            productos = [
                ("Pipetas anti-pulgas", "Tratamiento tópico", 12.5, 50),
                ("Alimento Premium 1kg", "Comida balanceada para perros", 8.0, 30),
            ]
            for nombre, descripcion, precio, stock in productos:
                db.ejecutar(
                    "INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (?, ?, ?, ?)",
                    (nombre, descripcion, precio, stock),
                )
            logger.info("Productos de ejemplo insertados")

        # Atenciones (ejemplo: si hay vets y pets)
        if vet_ids and pet_ids:
            cur = db.ejecutar("SELECT COUNT(*) FROM atenciones")
            aten_count = cur.fetchone()[0]
            if aten_count == 0:
                import datetime

                fecha = datetime.datetime.now().isoformat()
                db.ejecutar(
                    "INSERT INTO atenciones (veterinario_id, mascota_id, fecha, nota, precio, iva) VALUES (?, ?, ?, ?, ?, ?)",
                    (vet_ids[0], pet_ids[0], fecha, "Chequeo general", 25.0, 4.0),
                )
                if len(vet_ids) > 1 and len(pet_ids) > 1:
                    db.ejecutar(
                        "INSERT INTO atenciones (veterinario_id, mascota_id, fecha, nota, precio, iva) VALUES (?, ?, ?, ?, ?, ?)",
                        (vet_ids[1], pet_ids[1], fecha, "Vacunación", 30.0, 4.8),
                    )
                logger.info("Atenciones de ejemplo insertadas")

    except Exception as e:
        logger.error(f"Error al precargar datos iniciales: {e}")
