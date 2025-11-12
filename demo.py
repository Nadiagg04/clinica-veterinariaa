# demo.py
from src.modelos.persona import Persona
from src.modelos.mascota import Mascota
from src.modelos.veterinario import Veterinario
from src.modelos.cliente import Cliente
from src.servicios.servicio_veterinario import ServicioVeterinario

# Crear servicio
servicio = ServicioVeterinario()

# Crear personas y clientes
persona1 = Persona("Ana", "600111222")
cliente1 = Cliente(persona1)
servicio.agregar_cliente(cliente1)

# Crear veterinarios
vet1 = Veterinario("Juan Pérez", "Pediatría", "600333444")
servicio.agregar_veterinario(vet1)

# Crear mascotas
mascota1 = Mascota("Firulais", "Perro", 5, cliente1)
servicio.agregar_mascota(mascota1)

# Mostrar datos
print("=== Clientes registrados ===")
for c in servicio.listar_clientes():
    print("-", c)

print("\n=== Veterinarios registrados ===")
for v in servicio.listar_veterinarios():
    print("-", v)

print("\n=== Mascotas registradas ===")
for m in servicio.listar_mascotas():
    print("-", m)

print("\n=== Simulación de atención ===")
print(servicio.atender_mascota(vet1, mascota1))

