class Utilidades:

    @staticmethod
    def aplicar_iva(precio: float, iva: float = 21) -> float:
        """Devuelve el precio final aplicando IVA."""
        return precio + (precio * iva / 100)

    @staticmethod
    def validar_cadena(texto: str) -> bool:
        """Devuelve True si el texto no está vacío."""
        return isinstance(texto, str) and texto.strip() != ""

    @staticmethod
    def validar_telefono(telefono: str) -> bool:
        """Valida que el teléfono sea numérico y de 9 dígitos."""
        return telefono.isdigit() and len(telefono) == 9
