from src.modelos.persona import Persona

class Mascota:
    def __init__(self, nombre: str, especie: str, edad: int, dueño: Persona | int):
        self.nombre = nombre
        self.especie = especie
        self.edad = edad

        # Si es una Persona, la guardamos; si es un número, asumimos que es un ID de cliente
        if isinstance(dueño, Persona):
            self.dueño = dueño
            self.dueño_id = None  # se establecerá al guardar en BD
        else:
            self.dueño = None
            self.dueño_id = dueño

    def __str__(self):
        if self.dueño:
            return f"{self.nombre} ({self.especie}, {self.edad} años) - Dueño: {self.dueño.nombre}"
        else:
            return f"{self.nombre} ({self.especie}, {self.edad} años) - Dueño ID: {self.dueño_id}"
