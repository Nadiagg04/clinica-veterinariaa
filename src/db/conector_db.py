import sqlite3
from src.utils.excepciones import ErrorConexionDB


class ConectorDB:
    """Clase que gestiona la conexión y operaciones básicas con la base de datos SQLite."""

    def __init__(self, ruta_db="clinica.db"):
        self.ruta_db = ruta_db
        self.conexion = None

    def conectar(self):
        """Abre una conexión a la base de datos."""
        try:
            self.conexion = sqlite3.connect(self.ruta_db)
            return self.conexion
        except sqlite3.Error as e:
            raise ErrorConexionDB(f"Error al conectar con la base de datos: {e}")

    def cerrar(self):
        """Cierra la conexión abierta."""
        if self.conexion:
            self.conexion.close()

    def ejecutar(self, consulta, parametros=()):
        """Ejecuta una consulta con parámetros opcionales."""
        try:
            cur = self.conectar().cursor()
            cur.execute(consulta, parametros)
            self.conexion.commit()
            return cur
        except sqlite3.Error as e:
            raise ErrorConexionDB(f"Error al ejecutar consulta: {e}")
        finally:
            self.cerrar()
