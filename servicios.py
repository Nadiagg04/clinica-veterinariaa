from modelos import Mascota, Veterinario, Producto

class ServicioMascota:
    @staticmethod
    def crear_mascota(nombre, especie, edad, dueno):
        m = Mascota(nombre, especie, edad, dueno)
        m.guardar()
        return m

    @staticmethod
    def obtener_todas():
        return Mascota.obtener_todas()

    @staticmethod
    def actualizar(mascota, nombre=None, especie=None, edad=None, dueno=None):
        if nombre: mascota.nombre = nombre
        if especie: mascota.especie = especie
        if edad is not None: mascota.edad = edad
        if dueno: mascota.dueno = dueno
        mascota.guardar()

    @staticmethod
    def eliminar(mascota):
        mascota.eliminar()


class ServicioVeterinario:
    @staticmethod
    def crear_veterinario(nombre, especialidad):
        v = Veterinario(nombre, especialidad)
        v.guardar()
        return v

    @staticmethod
    def obtener_todos():
        return Veterinario.obtener_todos()

    @staticmethod
    def actualizar(veterinario, nombre=None, especialidad=None):
        if nombre: veterinario.nombre = nombre
        if especialidad: veterinario.especialidad = especialidad
        veterinario.guardar()

    @staticmethod
    def eliminar(veterinario):
        veterinario.eliminar()



class ServicioProducto:
    @staticmethod
    def crear_producto(nombre, precio, stock):
        p = Producto(nombre, precio, stock)
        p.guardar()
        return p

    @staticmethod
    def obtener_todos():
        return Producto.obtener_todos()

    @staticmethod
    def actualizar(producto, nombre=None, precio=None, stock=None):
        if nombre: producto.nombre = nombre
        if precio is not None: producto.precio = precio
        if stock is not None: producto.stock = stock
        producto.guardar()

    @staticmethod
    def eliminar(producto):
        producto.eliminar()
