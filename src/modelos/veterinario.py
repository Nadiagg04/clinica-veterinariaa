class Veterinario:
   

    def __init__(self, nombre: str, especialidad: str, telefono: str):
        self.nombre = nombre
        self.especialidad = especialidad
        self.telefono = telefono

    def __str__(self):
        return f"Dr. {self.nombre} - {self.especialidad}"

    def atender_mascota(self, mascota):
        
        return f"{self.nombre} está atendiendo a {mascota.nombre}"


