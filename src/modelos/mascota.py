class Mascota:
    def __init__(self, nombre: str, especie: str, edad: int, duenio_id: int = None):
        self.nombre = nombre
        self.especie = especie
        self.edad = edad
        self.duenio_id = duenio_id

    def __str__(self):
        return f"Mascota(nombre={self.nombre}, especie={self.especie}, edad={self.edad}, duenio_id={self.duenio_id})"
