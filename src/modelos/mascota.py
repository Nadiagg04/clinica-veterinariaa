class Mascota:
    def __init__(self, nombre: str, especie: str, edad: int, duenio_id: int = None):
        self.nombre = nombre
        self.especie = especie
        self.edad = edad
<<<<<<< HEAD

        # Si es una Persona, la guardamos; si es un número, asumimos que es un ID de cliente
        # Mantener compatibilidad: exponer atributos con y sin acento
        if isinstance(dueño, Persona):
            # atributos con acento (existentes)
            self.dueño = dueño
            self.dueño_id = None  # se establecerá al guardar en BD
            # atributos ASCII para evitar problemas de acceso en otros módulos
            self.duenio = dueño
            self.duenio_id = None
        else:
            self.dueño = None
            self.dueño_id = dueño
            self.duenio = None
            self.duenio_id = dueño

    def __str__(self):
        if self.duenio:
            return f"{self.nombre} ({self.especie}, {self.edad} años) - Dueño: {self.duenio.nombre}"
        else:
            return f"{self.nombre} ({self.especie}, {self.edad} años) - Dueño ID: {self.duenio_id}"
=======
        self.duenio_id = duenio_id

    def __str__(self):
        return f"Mascota(nombre={self.nombre}, especie={self.especie}, edad={self.edad}, duenio_id={self.duenio_id})"
>>>>>>> 2a3e5dd4f6a3a59e1f31c7bac72313eb4ca87178
