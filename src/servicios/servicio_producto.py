from src.modelos.producto import Producto

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
        if nombre:
            producto.nombre = nombre
        if precio is not None:
            producto.precio = precio
        if stock is not None:
            producto.stock = stock
        producto.guardar()

    @staticmethod
    def eliminar(producto):
        producto.eliminar()
