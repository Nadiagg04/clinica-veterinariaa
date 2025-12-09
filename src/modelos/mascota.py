from typing import Optional


class Mascota:
    def __init__(self, nombre, especie, edad, duenio_id: Optional[int] = None):
        self.nombre = nombre
        self.especie = especie
        self.edad = int(edad)
        self.duenio_id = duenio_id

    def __str__(self):
        return f"Mascota(nombre={self.nombre}, especie={self.especie}, edad={self.edad}, duenio_id={self.duenio_id})"
