class Producto:
    """Modelo simple para productos vendidos en la clínica."""

    def __init__(self, nombre: str, descripcion: str = "", precio: float = 0.0, stock: int = 0):
        self.id = None
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = float(precio) if precio is not None else 0.0
        self.stock = int(stock) if stock is not None else 0

    def __repr__(self):
        return f"Producto(id={self.id}, nombre={self.nombre!r}, precio={self.precio}, stock={self.stock})"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "stock": self.stock,
        }
