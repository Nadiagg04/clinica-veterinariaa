import sqlite3
from src.utils.excepciones import ErrorConexionDB

class ConectorDB:
    def __init__(self, ruta_db="clinica.db"):
        self.ruta_db = ruta_db
        self.conexion = None

    def conectar(self):
        try:
            # Always (re)create a connection and store it
            self.conexion = sqlite3.connect(self.ruta_db)
            return self.conexion
        except sqlite3.Error as e:
            raise ErrorConexionDB(f"Error al conectar con la base de datos: {e}")

    def cerrar(self):
        if self.conexion:
            try:
                self.conexion.close()
            finally:
                # Ensure internal reference is cleared so next call reconnects
                self.conexion = None

    def ejecutar(self, consulta, parametros=()):
        try:
            # Ensure we have a usable connection. If the existing connection
            # was closed elsewhere, operations will raise sqlite3.ProgrammingError
            # so we attempt to reconnect in that case.
            if not self.conexion:
                self.conectar()

            try:
                cur = self.conexion.cursor()
                cur.execute(consulta, parametros)
            except sqlite3.ProgrammingError:
                # Connection was closed; reconnect and retry once
                self.conectar()
                cur = self.conexion.cursor()
                cur.execute(consulta, parametros)

            self.conexion.commit()
            return cur
        except sqlite3.Error as e:
            raise ErrorConexionDB(f"Error al ejecutar consulta: {e}")
