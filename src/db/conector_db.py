import sqlite3
from src.utils.excepciones import ErrorConexionDB

class ConectorDB:
    def __init__(self, ruta_db="clinica.db"):
        self.ruta_db = ruta_db
        self.conexion = None

    def conectar(self):
        try:
            self.conexion = sqlite3.connect(self.ruta_db)
            return self.conexion
        except sqlite3.Error as e:
            raise ErrorConexionDB(f"Error al conectar con la base de datos: {e}")

    def cerrar(self):
        if self.conexion:
            self.conexion.close()

    def ejecutar(self, consulta, parametros=()):
        try:
            if not self.conexion:
                self.conectar()
            cur = self.conexion.cursor()
            cur.execute(consulta, parametros)
            self.conexion.commit()
            return cur
        except sqlite3.Error as e:
            raise ErrorConexionDB(f"Error al ejecutar consulta: {e}")
