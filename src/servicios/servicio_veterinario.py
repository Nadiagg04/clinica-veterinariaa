from src.modelos.mascota import Mascota
from src.modelos.veterinario import Veterinario
from src.modelos.cliente import Cliente
from src.utils.excepciones import ErrorMascota, ErrorVeterinario, ErrorValidacion
from src.utils.logger import logger


class ServicioVeterinario:
    """Clase que simula la gestión básica de la clínica veterinaria."""

    def __init__(self):
        self.mascotas = []
        self.veterinarios = []
        self.clientes = []

    def agregar_mascota(self, mascota: Mascota):
        logger.info(f"Agregando mascota: {mascota.nombre}")
        if not isinstance(mascota, Mascota):
            logger.error("El objeto no es una mascota válida.")
            raise ErrorMascota("El objeto no es una mascota válida.")
        self.mascotas.append(mascota)

    def agregar_veterinario(self, veterinario: Veterinario):
        logger.info(f"Agregando veterinario: {veterinario.nombre}")
        if not isinstance(veterinario, Veterinario):
            logger.error("El objeto no es un veterinario válido.")
            raise ErrorVeterinario("El objeto no es un veterinario válido.")
        self.veterinarios.append(veterinario)

    def agregar_cliente(self, cliente: Cliente):
        logger.info(f"Agregando cliente: {cliente.nombre}")
        if not isinstance(cliente, Cliente):
            logger.error("El objeto no es un cliente válido.")
            raise ErrorValidacion("El objeto no es un cliente válido.")
        self.clientes.append(cliente)

    def listar_mascotas(self):
        logger.info("Listando mascotas registradas.")
        if not self.mascotas:
            logger.error("No hay mascotas registradas.")
            raise ErrorMascota("No hay mascotas registradas.")
        return self.mascotas

    def listar_veterinarios(self):
        logger.info("Listando veterinarios registrados.")
        if not self.veterinarios:
            logger.error("No hay veterinarios registrados.")
            raise ErrorVeterinario("No hay veterinarios registrados.")
        return self.veterinarios

    def listar_clientes(self):
        logger.info("Listando clientes registrados.")
        if not self.clientes:
            logger.error("No hay clientes registrados.")
            raise ErrorValidacion("No hay clientes registrados.")
        return self.clientes

    def atender_mascota(self, veterinario: Veterinario, mascota: Mascota):
        logger.info(f"Veterinario {veterinario.nombre} atendiendo a la mascota {mascota.nombre}.")
        if veterinario not in self.veterinarios:
            logger.error("Veterinario no encontrado en el sistema.")
            raise ErrorVeterinario("Veterinario no encontrado en el sistema.")
        if mascota not in self.mascotas:
            logger.error("Mascota no registrada en el sistema.")
            raise ErrorMascota("Mascota no registrada en el sistema.")
        return veterinario.atender_mascota(mascota)
