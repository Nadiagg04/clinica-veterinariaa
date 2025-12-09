class Veterinario:

    def __init__(self, nombre: str, especialidad: str, telefono: str, precio_consulta: float = 0.0):
        self.nombre = nombre
        self.especialidad = especialidad
        self.telefono = telefono
        self.precio_consulta = float(precio_consulta)

    def __str__(self):
        return f"Dr. {self.nombre} - {self.especialidad}"

    def atender_mascota(self, mascota):
        return f"{self.nombre} está atendiendo a {mascota.nombre}"
