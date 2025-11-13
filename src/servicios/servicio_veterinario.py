from src.modelos.mascota import Mascota
from src.modelos.veterinario import Veterinario
from src.modelos.cliente import Cliente
from src.utils.excepciones import ErrorMascota, ErrorVeterinario, ErrorValidacion
from src.utils.logger import logger
from src.db.conector_db import ConectorDB


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
            conexion = self.db.conectar()
            cur = conexion.cursor()
            cur.execute(
                "INSERT INTO clientes (nombre, telefono) VALUES (?, ?)",
                (cliente.nombre, cliente.telefono)
            )
            conexion.commit()
            conexion.close()
            print(f"Cliente {cliente.nombre} guardado en la base de datos.")
        except Exception as e:
            print(f"Error SQLite real: {e}") 
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




    def atender_mascota(self, veterinario: Veterinario, mascota: Mascota):
        logger.info(f"Veterinario {veterinario.nombre} atendiendo a la mascota {mascota.nombre}.")
        if veterinario not in self.veterinarios:
            logger.error("Veterinario no encontrado en el sistema.")
            raise ErrorVeterinario("Veterinario no encontrado en el sistema.")
        if mascota not in self.mascotas:
            logger.error("Mascota no registrada en el sistema.")
            raise ErrorMascota("Mascota no registrada en el sistema.")
        return veterinario.atender_mascota(mascota)
