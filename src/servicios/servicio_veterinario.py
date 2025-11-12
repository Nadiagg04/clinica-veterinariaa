from src.modelos.mascota import Mascota
from src.modelos.veterinario import Veterinario
from src.modelos.cliente import Cliente
from src.utils.excepciones import ErrorMascota, ErrorVeterinario, ErrorValidacion


class ServicioVeterinario:
    """Clase que simula la gestión básica de la clínica veterinaria."""

    def __init__(self):
        self.mascotas = []
        self.veterinarios = []
        self.clientes = []

    def agregar_mascota(self, mascota: Mascota):
        if not isinstance(mascota, Mascota):
            raise ErrorMascota("El objeto no es una mascota válida.")
        self.mascotas.append(mascota)

    def agregar_veterinario(self, veterinario: Veterinario):
        if not isinstance(veterinario, Veterinario):
            raise ErrorVeterinario("El objeto no es un veterinario válido.")
        self.veterinarios.append(veterinario)

    def agregar_cliente(self, cliente: Cliente):
        if not isinstance(cliente, Cliente):
            raise ErrorValidacion("El objeto no es un cliente válido.")
        self.clientes.append(cliente)

    def listar_mascotas(self):
        return self.mascotas

    def listar_veterinarios(self):
        return self.veterinarios

    def listar_clientes(self):
        return self.clientes

    def atender_mascota(self, veterinario: Veterinario, mascota: Mascota):
        if veterinario not in self.veterinarios:
            raise ErrorVeterinario("Veterinario no encontrado en el sistema.")
        if mascota not in self.mascotas:
            raise ErrorMascota("Mascota no registrada en el sistema.")
        return veterinario.atender_mascota(mascota)
