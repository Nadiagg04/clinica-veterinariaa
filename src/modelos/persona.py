class Persona:
    def __init__(self, nombre: str, telefono: str):
        self.nombre = nombre
        self.telefono = telefono

    def __str__(self):
        return f"{self.nombre} ({self.telefono})"
