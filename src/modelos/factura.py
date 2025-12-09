class Factura:
    IVA = 0.21  # 21% IVA

    def __init__(self, cliente):
        self.cliente = cliente
        self.items = []  # lista de tuples (descripcion, precio)
        self.total_sin_iva = 0
        self.total_con_iva = 0

    def agregar_item(self, descripcion: str, precio: float):
        self.items.append((descripcion, precio))
        self.calcular_totales()

    def calcular_totales(self):
        self.total_sin_iva = sum(precio for _, precio in self.items)
        self.total_con_iva = self.total_sin_iva * (1 + self.IVA)

    def __str__(self):
        lineas = [f"Factura para {self.cliente.nombre}"]
        lineas.append("-" * 30)
        for desc, precio in self.items:
            lineas.append(f"{desc} ...... {precio} €")
        lineas.append("-" * 30)
        lineas.append(f"Subtotal: {self.total_sin_iva} €")
        lineas.append(f"IVA (21%): {self.total_sin_iva * self.IVA:.2f} €")
        lineas.append(f"TOTAL: {self.total_con_iva:.2f} €")
        return "\n".join(lineas)
