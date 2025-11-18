from src.modelos.mascota import Mascota
from src.modelos.veterinario import Veterinario
from src.modelos.cliente import Cliente
from src.utils.excepciones import ErrorMascota, ErrorVeterinario, ErrorValidacion
from src.utils.logger import logger
from src.db.conector_db import ConectorDB
from datetime import datetime


class ServicioVeterinario:
    """Clase que simula la gestión básica de la clínica veterinaria."""

    def __init__(self):
        self.mascotas = []
        self.veterinarios = []
        self.clientes = []
        self.db = ConectorDB()  

    def agregar_mascota(self, mascota: Mascota):
        logger.info(f"Agregando mascota: {mascota.nombre}")
        if not isinstance(mascota, Mascota):
            logger.error("El objeto no es una mascota válida.")
            raise ErrorMascota("El objeto no es una mascota válida.")
        self.mascotas.append(mascota)
        # Guardar en la base de datos
        try:
            self.db.ejecutar(
                "INSERT INTO mascotas (nombre, especie, edad, duenio_id) VALUES (?, ?, ?, ?)",
                (mascota.nombre, mascota.especie, mascota.edad, mascota.duenio_id)
            )
            logger.info(f"Mascota {mascota.nombre} guardada en la base de datos.")
        except Exception as e:
            logger.error(f"Error al guardar la mascota en la base de datos: {e}")
            raise ErrorMascota("Error al guardar la mascota en la base de datos.")

    def agregar_veterinario(self, veterinario: Veterinario):
        logger.info(f"Agregando veterinario: {veterinario.nombre}")
        if not isinstance(veterinario, Veterinario):
            logger.error("El objeto no es un veterinario válido.")
            raise ErrorVeterinario("El objeto no es un veterinario válido.")
        self.veterinarios.append(veterinario)
        try:
            self.db.ejecutar(
                "INSERT INTO veterinarios (nombre, especialidad, telefono) VALUES (?, ?, ?)",
                (veterinario.nombre, veterinario.especialidad, veterinario.telefono)
            )
            logger.info(f"Veterinario {veterinario.nombre} guardado en la base de datos.")
        except Exception as e:
            logger.error(f"Error al guardar el veterinario en la base de datos: {e}")
            raise ErrorVeterinario("Error al guardar el veterinario en la base de datos.")
        
    def agregar_cliente(self, cliente: Cliente):
        if not isinstance(cliente, Cliente):
            raise ErrorValidacion("El objeto no es un cliente válido.")

        self.clientes.append(cliente)

        try:
            # Use ConectorDB.ejecutar to handle connection lifecycle consistently
            self.db.ejecutar(
                "INSERT INTO clientes (nombre, telefono) VALUES (?, ?)",
                (cliente.nombre, cliente.telefono)
            )
            print(f"Cliente {cliente.nombre} guardado en la base de datos.")
        except Exception as e:
            logger.error(f"Error al guardar el cliente en la base de datos: {e}")
            raise ErrorValidacion("Error al guardar el cliente en la base de datos.")



    def listar_mascotas(self):
        logger.info("Listando mascotas desde la base de datos.")
        try:
            cur = self.db.ejecutar("""
                SELECT m.id, m.nombre, m.especie, m.edad, c.nombre AS duenio
                FROM mascotas m
                LEFT JOIN clientes c ON m.duenio_id = c.id
            """)
            mascotas = cur.fetchall()

            if not mascotas:
                logger.warning("No hay mascotas registradas en la base de datos.")
                raise ErrorMascota("No hay mascotas registradas.")

            return mascotas
        except Exception as e:
            logger.error(f"Error al listar mascotas: {e}")
            raise ErrorMascota("Error al obtener las mascotas desde la base de datos.")


    def listar_veterinarios(self):
        logger.info("Listando veterinarios desde la base de datos.")
        try:
            cur = self.db.ejecutar("SELECT id, nombre, especialidad, telefono FROM veterinarios")
            veterinarios = cur.fetchall()

            if not veterinarios:
                logger.warning("No hay veterinarios registrados en la base de datos.")
                raise ErrorVeterinario("No hay veterinarios registrados.")

            return veterinarios
        except Exception as e:
            logger.error(f"Error al listar veterinarios: {e}")
            raise ErrorVeterinario("Error al obtener los veterinarios desde la base de datos.")
        
    def listar_clientes(self):
        logger.info("Listando clientes desde la base de datos.")
        try:
            # Eliminamos 'email' de la consulta
            cur = self.db.ejecutar("SELECT id, nombre, telefono FROM clientes")
            clientes = cur.fetchall()

            if not clientes:
                logger.warning("No hay clientes registrados en la base de datos.")
                raise ErrorValidacion("No hay clientes registrados.")

            return clientes
        except Exception as e:
            logger.error(f"Error al listar clientes: {e}")
            raise ErrorValidacion("Error al obtener los clientes desde la base de datos.")


    def registrar_atencion(self, veterinario_id: int, mascota_id: int, nota: str = ""):
        """Registra una atención (consulta) realizada por un veterinario a una mascota.

        Args:
            veterinario_id: id del veterinario en la BD
            mascota_id: id de la mascota en la BD
            nota: texto opcional con observaciones
        """
        logger.info(f"Registrando atención: vet={veterinario_id} masc={mascota_id}")
        try:
            fecha = datetime.now().isoformat(sep=' ', timespec='seconds')
            self.db.ejecutar(
                "INSERT INTO atenciones (veterinario_id, mascota_id, fecha, nota) VALUES (?, ?, ?, ?)",
                (veterinario_id, mascota_id, fecha, nota)
            )
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
                SELECT a.id, a.fecha, m.nombre AS mascota, c.nombre AS duenio, a.nota
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
