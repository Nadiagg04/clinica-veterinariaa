from src.modelos.mascota import Mascota
from src.modelos.veterinario import Veterinario
from src.modelos.cliente import Cliente
from src.utils.excepciones import ErrorMascota, ErrorVeterinario, ErrorValidacion
from src.utils.logger import Logger
from src.db.conector_db import ConectorDB
from datetime import datetime


class ServicioVeterinario:

    def __init__(self):
        self.db = ConectorDB()
        self.mascotas = []
        self.veterinarios = []
        self.clientes = []

    # -------- CLIENTES --------

    def agregar_cliente(self, cliente: Cliente):
        if not isinstance(cliente, Cliente):
            raise ErrorValidacion("El objeto no es un cliente válido.")

        try:
            self.db.ejecutar(
                "INSERT INTO clientes (nombre, telefono) VALUES (?, ?)",
                (cliente.nombre, cliente.telefono)
            )
            logger.info(f"Cliente {cliente.nombre} guardado en la base de datos.")
        except Exception as e:
            logger.error(f"Error al guardar el cliente: {e}")
            raise ErrorValidacion("Error al guardar el cliente en la base de datos.")

    def listar_clientes(self):
        logger.info("Listando clientes")
        try:
            cur = self.db.ejecutar("SELECT id, nombre, telefono FROM clientes")
            return cur.fetchall()
        except Exception as e:
            logger.error(f"Error al listar clientes: {e}")
            raise ErrorValidacion("Error al obtener los clientes.")

    # -------- VETERINARIOS --------

    def agregar_veterinario(self, veterinario: Veterinario):
        logger.info(f"Agregando veterinario: {veterinario.nombre}")

        if not isinstance(veterinario, Veterinario):
            raise ErrorVeterinario("El objeto no es un veterinario válido.")

        try:
            # Compatibilidad con esquemas antiguos: comprobar si existe la columna precio_consulta
            cur = self.db.ejecutar("PRAGMA table_info(veterinarios)")
            cols = [r[1] for r in cur.fetchall()]
            if 'precio_consulta' in cols:
                self.db.ejecutar(
                    "INSERT INTO veterinarios (nombre, especialidad, telefono, precio_consulta) VALUES (?, ?, ?, ?)",
                    (veterinario.nombre, veterinario.especialidad, veterinario.telefono, getattr(veterinario, 'precio_consulta', 0.0))
                )
            else:
                # tabla antigua sin columna precio_consulta -> intentar añadir la columna y guardar el precio
                try:
                    self.db.ejecutar("ALTER TABLE veterinarios ADD COLUMN precio_consulta REAL DEFAULT 0")
                    logger.info("Columna 'precio_consulta' añadida a la tabla 'veterinarios' (migración automática).")
                    # ahora insertar incluyendo la columna
                    self.db.ejecutar(
                        "INSERT INTO veterinarios (nombre, especialidad, telefono, precio_consulta) VALUES (?, ?, ?, ?)",
                        (veterinario.nombre, veterinario.especialidad, veterinario.telefono, getattr(veterinario, 'precio_consulta', 0.0))
                    )
                except Exception:
                    # Si por alguna razón no se pudo alterar la tabla, caer a insertar sin la columna
                    logger.info("No se pudo añadir la columna 'precio_consulta'; insertando sin ella.")
                    self.db.ejecutar(
                        "INSERT INTO veterinarios (nombre, especialidad, telefono) VALUES (?, ?, ?)",
                        (veterinario.nombre, veterinario.especialidad, veterinario.telefono)
                    )
            logger.info(f"Veterinario {veterinario.nombre} guardado en la base de datos.")
        except Exception as e:
            logger.error(f"Error al guardar el veterinario: {e}")
            raise ErrorVeterinario("Error al guardar el veterinario.")

    def listar_veterinarios(self):
        logger.info("Listando veterinarios")
        try:
            cur = self.db.ejecutar("SELECT id, nombre, especialidad, telefono FROM veterinarios")
            return cur.fetchall()
        except Exception as e:
            logger.error(f"Error al listar veterinarios: {e}")
            raise ErrorVeterinario("Error al obtener los veterinarios.")

    # -------- MASCOTAS --------

    def agregar_mascota(self, mascota: Mascota):
        logger.info(f"Agregando mascota: {mascota.nombre}")

        if not isinstance(mascota, Mascota):
            raise ErrorMascota("El objeto no es una mascota válida.")

        try:
        
            self.db.ejecutar(
                "INSERT INTO clientes (nombre, telefono) VALUES (?, ?)",
                (cliente.nombre, cliente.telefono)
            )
            print(f"Cliente {cliente.nombre} guardado en la base de datos.")
        except Exception as e:
            logger.error(f"Error al guardar el cliente en la base de datos: {e}")
            raise ErrorValidacion("Error al guardar el cliente en la base de datos.")



    def listar_mascotas(self):
        logger.info("Listando mascotas")
        try:
            cur = self.db.ejecutar("""
                SELECT m.id, m.nombre, m.especie, m.edad, c.nombre AS duenio
                FROM mascotas m
                LEFT JOIN clientes c ON m.duenio_id = c.id
            """)
            return cur.fetchall()
        except Exception as e:
            logger.error(f"Error al listar mascotas: {e}")
            raise ErrorMascota("Error al obtener las mascotas.")

    # -------- ATENCIONES --------

    def registrar_atencion(self, veterinario_id: int, mascota_id: int, nota: str = ""):
        logger.info("Registrando atención")
        try:
            # Compatibilidad: si la columna precio_consulta no existe, obtener solo los campos disponibles
            cur = self.db.ejecutar("PRAGMA table_info(veterinarios)")
            cols = [r[1] for r in cur.fetchall()]
            if 'precio_consulta' in cols:
                cur = self.db.ejecutar("SELECT id, nombre, especialidad, telefono, precio_consulta FROM veterinarios")
                veterinarios = cur.fetchall()
            else:
                cur = self.db.ejecutar("SELECT id, nombre, especialidad, telefono FROM veterinarios")
                raw = cur.fetchall()
                # Añadir un valor por defecto 0.0 para precio_consulta al mapear
                veterinarios = [(r[0], r[1], r[2], r[3], 0.0) for r in raw]

            if not veterinarios:
                logger.warning("No hay veterinarios registrados en la base de datos.")
                raise ErrorVeterinario("No hay veterinarios registrados.")

            return veterinarios
        except Exception as e:
            logger.error(f"Error al registrar la atención: {e}")
            raise ErrorValidacion("Error al registrar la atención.")

    def listar_atenciones(self):
        logger.info("Listando atenciones")
        try:
            cur = self.db.ejecutar(
                """
                SELECT a.id, a.fecha, m.nombre AS mascota, c.nombre AS duenio, a.nota
                FROM atenciones a
                LEFT JOIN mascotas m ON a.mascota_id = m.id
                LEFT JOIN clientes c ON m.duenio_id = c.id
                ORDER BY a.fecha DESC
                """
            )
            return cur.fetchall()
        except Exception as e:
            logger.error(f"Error al listar clientes: {e}")
            raise ErrorValidacion("Error al obtener los clientes desde la base de datos.")


    # --- Métodos para catálogo de productos ---
    def agregar_producto(self, nombre: str, descripcion: str = "", precio: float = 0.0, stock: int = 0):
        logger.info(f"Agregando producto: {nombre}")
        try:
            self.db.ejecutar(
                "INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (?, ?, ?, ?)",
                (nombre, descripcion, float(precio), int(stock))
            )
            logger.info(f"Producto {nombre} guardado en la base de datos.")
        except Exception as e:
            logger.error(f"Error al guardar el producto en la base de datos: {e}")
            raise ErrorValidacion("Error al guardar el producto en la base de datos.")

    def listar_productos(self):
        logger.info("Listando productos desde la base de datos.")
        try:
            cur = self.db.ejecutar("SELECT id, nombre, descripcion, precio, stock FROM productos")
            productos = cur.fetchall()
            return productos
        except Exception as e:
            logger.error(f"Error al listar productos: {e}")
            raise ErrorValidacion("Error al obtener los productos desde la base de datos.")

    def eliminar_producto(self, producto_id: int):
        logger.info(f"Eliminando producto id={producto_id}")
        try:
            self.db.ejecutar("DELETE FROM productos WHERE id = ?", (producto_id,))
        except Exception as e:
            logger.error(f"Error al eliminar producto: {e}")
            raise ErrorValidacion("Error al eliminar el producto.")


    def vender_producto(self, producto_id: int, cantidad: int = 1):
        """Decrementa el stock de un producto si hay suficiente inventario."""
        logger.info(f"Vender producto id={producto_id} cantidad={cantidad}")
        try:
            cur = self.db.ejecutar("SELECT stock, nombre FROM productos WHERE id = ?", (producto_id,))
            row = cur.fetchone()
            if not row:
                raise ErrorValidacion("Producto no encontrado.")
            stock_actual, nombre = row[0], row[1] if len(row) > 1 else None
            stock_actual = int(stock_actual or 0)
            cantidad = int(cantidad)
            if cantidad <= 0:
                raise ErrorValidacion("La cantidad a vender debe ser mayor que cero.")
            if cantidad > stock_actual:
                raise ErrorValidacion(f"No hay suficiente stock. Stock disponible: {stock_actual}.")

            nuevo = stock_actual - cantidad
            self.db.ejecutar("UPDATE productos SET stock = ? WHERE id = ?", (nuevo, producto_id))
            logger.info(f"Producto {producto_id} vendido. Stock anterior={stock_actual}, nuevo={nuevo}")
            return nuevo
        except ErrorValidacion:
            raise
        except Exception as e:
            logger.error(f"Error al vender producto: {e}")
            raise ErrorValidacion("Error al procesar la venta del producto.")


    def reponer_producto(self, producto_id: int, cantidad: int = 1):
        """Incrementa el stock de un producto."""
        logger.info(f"Reponer producto id={producto_id} cantidad={cantidad}")
        try:
            cur = self.db.ejecutar("SELECT stock FROM productos WHERE id = ?", (producto_id,))
            row = cur.fetchone()
            if not row:
                raise ErrorValidacion("Producto no encontrado.")
            stock_actual = int(row[0] or 0)
            cantidad = int(cantidad)
            if cantidad <= 0:
                raise ErrorValidacion("La cantidad a reponer debe ser mayor que cero.")

            nuevo = stock_actual + cantidad
            self.db.ejecutar("UPDATE productos SET stock = ? WHERE id = ?", (nuevo, producto_id))
            logger.info(f"Producto {producto_id} repuesto. Stock anterior={stock_actual}, nuevo={nuevo}")
            return nuevo
        except ErrorValidacion:
            raise
        except Exception as e:
            logger.error(f"Error al reponer producto: {e}")
            raise ErrorValidacion("Error al reponer el producto.")


    # --- Cálculos financieros / contables ---
    def calcular_valor_inventario(self) -> float:
        """Calcula el valor total del inventario (sum(precio * stock))."""
        logger.info("Calculando valor del inventario.")
        try:
            cur = self.db.ejecutar("SELECT SUM(precio * stock) FROM productos")
            row = cur.fetchone()
            total = float(row[0]) if row and row[0] is not None else 0.0
            return total
        except Exception as e:
            logger.error(f"Error al calcular inventario: {e}")
            raise ErrorValidacion("Error al calcular el valor del inventario.")

    def calcular_ingresos_consultas(self) -> float:
        """Calcula los ingresos totales por consultas considerando el IVA."""
        logger.info("Calculando ingresos por consultas.")
        try:
            # Comprobar estructura de la tabla atenciones para compatibilidad con BD antiguas
            cur = self.db.ejecutar("PRAGMA table_info(atenciones)")
            cols = [r[1] for r in cur.fetchall()]
            if 'precio' in cols:
                # tenemos columna precio; comprobar si existe iva
                if 'iva' in cols:
                    cur = self.db.ejecutar("SELECT SUM(precio * (1 + iva/100.0)) FROM atenciones")
                else:
                    cur = self.db.ejecutar("SELECT SUM(precio) FROM atenciones")
                row = cur.fetchone()
                total = float(row[0]) if row and row[0] is not None else 0.0
                return total
            else:
                # Sin columna precio: no hay datos de importe en la tabla
                logger.info("La tabla 'atenciones' no contiene la columna 'precio'; ingresos por consultas = 0.0")
                return 0.0
        except Exception as e:
            logger.error(f"Error al calcular ingresos por consultas: {e}")
            raise ErrorValidacion("Error al calcular ingresos por consultas.")

    def listar_ingresos_por_veterinario(self):
        """Devuelve lista con (vet_id, nombre, consultas, subtotal, total_con_iva)."""
        logger.info("Listando ingresos por veterinario.")
        try:
            # Verificar si la tabla atenciones contiene precio/iva
            cur = self.db.ejecutar("PRAGMA table_info(atenciones)")
            cols = [r[1] for r in cur.fetchall()]
            if 'precio' in cols:
                if 'iva' in cols:
                    sql = """
                    SELECT v.id, v.nombre, COUNT(a.id) as consultas,
                           COALESCE(SUM(a.precio), 0) as subtotal,
                           COALESCE(SUM(a.precio * (1 + a.iva/100.0)), 0) as total_con_iva
                    FROM veterinarios v
                    LEFT JOIN atenciones a ON v.id = a.veterinario_id
                    GROUP BY v.id
                    ORDER BY total_con_iva DESC
                    """
                else:
                    sql = """
                    SELECT v.id, v.nombre, COUNT(a.id) as consultas,
                           COALESCE(SUM(a.precio), 0) as subtotal,
                           COALESCE(SUM(a.precio), 0) as total_con_iva
                    FROM veterinarios v
                    LEFT JOIN atenciones a ON v.id = a.veterinario_id
                    GROUP BY v.id
                    ORDER BY total_con_iva DESC
                    """
            else:
                # No hay información de importes; devolver filas con 0s
                sql = """
                    SELECT v.id, v.nombre, COUNT(a.id) as consultas,
                           0 as subtotal,
                           0 as total_con_iva
                    FROM veterinarios v
                    LEFT JOIN atenciones a ON v.id = a.veterinario_id
                    GROUP BY v.id
                    ORDER BY total_con_iva DESC
                    """

            cur = self.db.ejecutar(sql)
            rows = cur.fetchall()
            return rows
        except Exception as e:
            logger.error(f"Error al listar ingresos por veterinario: {e}")
            raise ErrorValidacion("Error al obtener los ingresos por veterinario.")


    def registrar_atencion(self, veterinario_id: int, mascota_id: int, nota: str = "", precio: float = 0.0, iva: float = 0.0):
        """Registra una atención (consulta) realizada por un veterinario a una mascota.

        Args:
            veterinario_id: id del veterinario en la BD
            mascota_id: id de la mascota en la BD
            nota: texto opcional con observaciones
        """
        logger.info(f"Registrando atención: vet={veterinario_id} masc={mascota_id}")
        try:
            fecha = datetime.now().isoformat(sep=' ', timespec='seconds')

            # Comprobar columnas existentes en atenciones
            cur = self.db.ejecutar("PRAGMA table_info(atenciones)")
            cols = [r[1] for r in cur.fetchall()]

            # Si faltan columnas precio/iva, intentar añadirlas (migración automática)
            missing = []
            for c, ddl in (('precio', 'REAL DEFAULT 0'), ('iva', 'REAL DEFAULT 0')):
                if c not in cols:
                    missing.append((c, ddl))

            if missing:
                try:
                    for c, ddl in missing:
                        self.db.ejecutar(f"ALTER TABLE atenciones ADD COLUMN {c} {ddl}")
                    # re-leer columnas
                    cur = self.db.ejecutar("PRAGMA table_info(atenciones)")
                    cols = [r[1] for r in cur.fetchall()]
                    logger.info("Columnas faltantes añadidas a 'atenciones'.")
                except Exception:
                    # Si no se puede alterar la tabla, seguiremos intentando insertar con las columnas disponibles
                    logger.info("No se pudieron añadir columnas faltantes a 'atenciones'; se insertará con columnas disponibles.")

            # Construir INSERT dinámico según columnas disponibles
            insert_cols = ['veterinario_id', 'mascota_id', 'fecha', 'nota']
            params = [veterinario_id, mascota_id, fecha, nota]
            if 'precio' in cols:
                insert_cols.append('precio')
                params.append(precio)
            if 'iva' in cols:
                insert_cols.append('iva')
                params.append(iva)

            placeholders = ','.join(['?'] * len(params))
            sql = f"INSERT INTO atenciones ({', '.join(insert_cols)}) VALUES ({placeholders})"
            self.db.ejecutar(sql, tuple(params))
            logger.info("Atención registrada en la base de datos.")
        except Exception as e:
            logger.error(f"Error al registrar la atención: {e}")
            raise ErrorValidacion("Error al registrar la atención en la base de datos.")


    def listar_atenciones_por_veterinario(self, veterinario_id: int):
        """Devuelve el historial de atenciones de un veterinario.

        Retorna lista de tuplas: (id_atencion, fecha, nombre_mascota, nombre_duenio, nota)
        """
        logger.info(f"Listando atenciones para veterinario {veterinario_id}")
        try:
            cur = self.db.ejecutar(
                """
                SELECT a.id, a.fecha, m.nombre AS mascota, c.nombre AS duenio, a.nota, a.precio, a.iva
                FROM atenciones a
                LEFT JOIN mascotas m ON a.mascota_id = m.id
                LEFT JOIN clientes c ON m.duenio_id = c.id
                WHERE a.veterinario_id = ?
                ORDER BY a.fecha DESC
                """,
                (veterinario_id,)
            )
            atenciones = cur.fetchall()
            return atenciones
        except Exception as e:
            logger.error(f"Error al listar atenciones: {e}")
            raise ErrorValidacion("Error al obtener el historial de atenciones.")


    def eliminar_mascota(self, mascota_id: int):
        logger.info(f"Eliminando mascota id={mascota_id}")
        try:
            self.db.ejecutar("DELETE FROM mascotas WHERE id = ?", (mascota_id,))
            # limpiar memoria
            self.mascotas = [m for m in self.mascotas if getattr(m, 'id', None) != mascota_id]
        except Exception as e:
            logger.error(f"Error al eliminar mascota: {e}")
            raise ErrorMascota("Error al eliminar la mascota.")


    def eliminar_cliente(self, cliente_id: int):
        logger.info(f"Eliminando cliente id={cliente_id}")
        try:
            # eliminar mascotas del cliente primero para mantener integridad
            self.db.ejecutar("DELETE FROM mascotas WHERE duenio_id = ?", (cliente_id,))
            self.db.ejecutar("DELETE FROM clientes WHERE id = ?", (cliente_id,))
            # limpiar memoria
            self.clientes = [c for c in self.clientes if getattr(c, 'id', None) != cliente_id]
            self.mascotas = [m for m in self.mascotas if getattr(m, 'duenio_id', None) != cliente_id and getattr(m, 'duenio', None) and getattr(m.duenio, 'id', None) != cliente_id]
        except Exception as e:
            logger.error(f"Error al eliminar cliente: {e}")
            raise ErrorValidacion("Error al eliminar el cliente.")


    def eliminar_veterinario(self, veterinario_id: int):
        logger.info(f"Eliminando veterinario id={veterinario_id}")
        try:
            # eliminar atenciones asociadas
            self.db.ejecutar("DELETE FROM atenciones WHERE veterinario_id = ?", (veterinario_id,))
            self.db.ejecutar("DELETE FROM veterinarios WHERE id = ?", (veterinario_id,))
            # limpiar memoria
            self.veterinarios = [v for v in self.veterinarios if getattr(v, 'id', None) != veterinario_id]
        except Exception as e:
            logger.error(f"Error al eliminar veterinario: {e}")
            raise ErrorVeterinario("Error al eliminar el veterinario.")


    def eliminar_atencion(self, atencion_id: int):
        logger.info(f"Eliminando atencion id={atencion_id}")
        try:
            self.db.ejecutar("DELETE FROM atenciones WHERE id = ?", (atencion_id,))
        except Exception as e:
            logger.error(f"Error al eliminar atencion: {e}")
            raise ErrorValidacion("Error al eliminar la atención.")




    def atender_mascota(self, veterinario: Veterinario, mascota: Mascota):
        logger.info(f"Veterinario {veterinario.nombre} atendiendo a la mascota {mascota.nombre}.")
        if veterinario not in self.veterinarios:
            logger.error("Veterinario no encontrado en el sistema.")
            raise ErrorVeterinario("Veterinario no encontrado en el sistema.")
        if mascota not in self.mascotas:
            logger.error("Mascota no registrada en el sistema.")
            raise ErrorMascota("Mascota no registrada en el sistema.")
        return veterinario.atender_mascota(mascota)
