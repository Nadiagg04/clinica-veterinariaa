from src.repositorio.repositorio_mascotas import RepositorioMascotas
from src.modelos.persona import Persona
from src.modelos.mascota import Mascota

def test_repositorio_agregar_y_buscar():
    repo = RepositorioMascotas()
    dueño = Persona("Ana", "600111222")
    mascota = Mascota("Luna", "Perro", 3, dueño)

    repo.agregar(mascota)

    resultado = repo.buscar_por_nombre("Luna")
    assert len(resultado) == 1
    assert resultado[0].nombre == "Luna"
