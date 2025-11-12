from src.servicios.servicio_veterinario import ServicioVeterinario
from src.repositorio.repositorio_mascotas import RepositorioMascotas

def test_registro_y_listado_mascotas():
    repo = RepositorioMascotas()
    servicio = ServicioVeterinario(repo)

    servicio.registrar_mascota(
        "Max", "Gato", 2,
        "Sofía", "611222333"
    )

    mascotas = servicio.listar_mascotas()

    assert len(mascotas) == 1
    assert mascotas[0].nombre == "Max"

def test_buscar_mascota():
    repo = RepositorioMascotas()
    servicio = ServicioVeterinario(repo)

    servicio.registrar_mascota("Toby", "Perro", 4, "Carlos", "677888999")

    resultado = servicio.buscar_mascota("Toby")

    assert len(resultado) == 1
    assert resultado[0].especie == "Perro"
