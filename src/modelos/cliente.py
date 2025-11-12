from src.modelos.persona import Persona

class Cliente:
    def __init__(self, persona: Persona):
        self.nombre = persona.nombre
        self.telefono = persona.telefono

    def __str__(self):
        return f"{self.nombre} - {self.telefono}"
