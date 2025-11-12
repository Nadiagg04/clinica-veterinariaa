from src.modelos.persona import Persona

class Mascota:
    def __init__(self, nombre: str, especie: str, edad: int, dueño: Persona):
        self.nombre = nombre
        self.especie = especie
        self.edad = edad
        self.dueño = dueño

    def __str__(self):
        return f"{self.nombre} ({self.especie}, {self.edad} años) - Dueño: {self.dueño.nombre}"
