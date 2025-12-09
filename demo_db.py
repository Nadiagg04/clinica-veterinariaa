from src.servicios.servicio_veterinario import ServicioVeterinario
from src.modelos.mascota import Mascota
from src.modelos.cliente import Cliente
from src.modelos.veterinario import Veterinario

servicio = ServicioVeterinario()

print("\n=== INSERTANDO DATOS ===")

cliente1 = Cliente("Laura", "612345678")
servicio.agregar_cliente(cliente1)

vet1 = Veterinario("Dr. Gómez", "Cirugía", "987654321")
servicio.agregar_veterinario(vet1)

mascota1 = Mascota("Toby", "Perro", 5, duenio_id=1)
servicio.agregar_mascota(mascota1)

print("\n=== LISTANDO CLIENTES ===")
print(servicio.listar_clientes())

print("\n=== LISTANDO VETERINARIOS ===")
print(servicio.listar_veterinarios())

print("\n=== LISTANDO MASCOTAS ===")
print(servicio.listar_mascotas())

print("\n=== LISTANDO ATENCIONES ===")
atenciones = servicio.listar_atenciones()
for at in atenciones:
    print(f"ID: {at[0]}, Fecha: {at[1]}, Mascota: {at[2]}, Dueño: {at[3]}, Nota: {at[4]}")

from datetime import datetime

print("\n=== REGISTRANDO ATENCIONES ===")
# Supongamos que el id del veterinario es 1 y el de la mascota es 1
# Ajusta estos IDs según los que tengas en tu base de datos
servicio.registrar_atencion(veterinario_id=1, mascota_id=1, nota="Vacunación completa")
servicio.registrar_atencion(veterinario_id=1, mascota_id=1, nota="Revisión general")
print("Atenciones registradas correctamente ")

print("\n=== LISTANDO ATENCIONES ===")
atenciones = servicio.listar_atenciones()
for at in atenciones:
    print(f"ID: {at[0]}, Fecha: {at[1]}, Mascota: {at[2]}, Dueño: {at[3]}, Nota: {at[4]}")

