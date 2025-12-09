from src.modelos.mascota import Mascota
from src.modelos.veterinario import Veterinario
from src.modelos.cliente import Cliente
from src.utils.excepciones import ErrorMascota, ErrorVeterinario, ErrorValidacion
from src.utils.logger import Logger
from src.db.conector_db import ConectorDB
from datetime import datetime

logger = Logger


class ServicioVeterinario:
    """Clase de gestión veterinaria con base de datos."""

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
                "INSERT INTO mascotas (nombre, especie, edad, duenio_id) VALUES (?, ?, ?, ?)",
                (mascota.nombre, mascota.especie, mascota.edad, mascota.duenio_id)
            )
            logger.info(f"Mascota {mascota.nombre} guardada en la base de datos.")
        except Exception as e:
            logger.error(f"Error al guardar mascota: {e}")
            raise ErrorMascota("Error al guardar mascota.")

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
            fecha = datetime.now().isoformat(sep=" ", timespec="seconds")
            self.db.ejecutar(
                "INSERT INTO atenciones (veterinario_id, mascota_id, fecha, nota) VALUES (?, ?, ?, ?)",
                (veterinario_id, mascota_id, fecha, nota)
            )
            logger.info("Atención registrada correctamente.")
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
            logger.error(f"Error al listar atenciones: {e}")
            raise ErrorValidacion("Error al obtener las atenciones.")
