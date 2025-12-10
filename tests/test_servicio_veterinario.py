from src.servicios.servicio_veterinario import ServicioVeterinario
from src.modelos.cliente import Cliente
from src.modelos.mascota import Mascota
import uuid
from src.repositorio.repositorio_mascotas import RepositorioMascotas

def test_registro_y_listado_mascotas():
    # Usamos el servicio real que persiste en la BD integrada
    servicio = ServicioVeterinario()

    cliente = Cliente("Sofía", "611222333")
    servicio.agregar_cliente(cliente)

    # obtener id del dueño insertado
    clientes = servicio.listar_clientes()
    duenio_id = None
    for c in clientes:
        if c[1] == "Sofía":
            duenio_id = c[0]
            break

    unique_name = f"Max_{uuid.uuid4().hex[:8]}"
    mascota = Mascota(unique_name, "Gato", 2, duenio_id)
    servicio.agregar_mascota(mascota)

    mascotas = servicio.listar_mascotas()

    resultado = [m for m in mascotas if m[1] == unique_name]
    assert resultado[0][1] == unique_name

def test_buscar_mascota():
    servicio = ServicioVeterinario()

    cliente = Cliente("Carlos", "677888999")
    servicio.agregar_cliente(cliente)

    clientes = servicio.listar_clientes()
    duenio_id = None
    for c in clientes:
        if c[1] == "Carlos":
            duenio_id = c[0]
            break

    unique_name = f"Toby_{uuid.uuid4().hex[:8]}"
    mascota = Mascota(unique_name, "Perro", 4, duenio_id)
    servicio.agregar_mascota(mascota)

    mascotas = servicio.listar_mascotas()
    resultado = [m for m in mascotas if m[1] == unique_name]

    assert len(resultado) == 1
    assert resultado[0][2] == "Perro"
