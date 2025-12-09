class Cliente:
    def __init__(self, nombre: str, telefono: str):
        self.nombre = nombre
        self.telefono = telefono

    def __str__(self):
        return f"Cliente(nombre={self.nombre}, telefono={self.telefono})"
