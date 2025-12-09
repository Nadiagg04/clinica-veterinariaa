import sqlite3
from src.utils.excepciones import ErrorConexionDB


class ConectorDB:
    def __init__(self, db_name: str = "clinica.db"):
        self.db_name = db_name
        self.conn: sqlite3.Connection | None = None

    def conectar(self) -> sqlite3.Connection:
        if self.conn is None:
            try:
                self.conn = sqlite3.connect(self.db_name)
            except sqlite3.Error as e:
                raise ErrorConexionDB(f"Error al conectar con la base de datos: {e}")
        return self.conn

    def ejecutar(self, consulta: str, parametros: tuple = ()):  # retorna cursor
        try:
            conn = self.conectar()
            cur = conn.cursor()
            cur.execute(consulta, parametros)
            conn.commit()
            return cur
        except sqlite3.Error as e:
            raise ErrorConexionDB(f"Error al ejecutar consulta: {e}")

    def cerrar(self) -> None:
        if self.conn:
            try:
                self.conn.close()
            finally:
                self.conn = None
