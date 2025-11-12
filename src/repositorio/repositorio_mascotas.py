from src.modelos.mascota import Mascota

class RepositorioMascotas:
    """Repositorio en memoria simulando una BD."""

    def __init__(self):
        self._mascotas = []

    def agregar(self, mascota: Mascota):
        self._mascotas.append(mascota)

    def obtener_todas(self):
        return self._mascotas

    def buscar_por_nombre(self, nombre: str):
        return [m for m in self._mascotas if m.nombre.lower() == nombre.lower()]
