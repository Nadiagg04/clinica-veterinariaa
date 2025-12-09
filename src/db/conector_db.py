import sqlite3

class ConectorDB:
    def __init__(self, db_name="clinica.db"):
        self.db_name = db_name
        self.conn = None

    def conectar(self):
        if not self.conn:
            self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def ejecutar(self, query, params=None):
        try:
<<<<<<< HEAD
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
=======
            conn = self.conectar()
            cursor = conn.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            conn.commit()
            return cursor
        except Exception as e:
            raise e

    def cerrar(self):
        if self.conn:
            self.conn.close()
            self.conn = None


>>>>>>> 2a3e5dd4f6a3a59e1f31c7bac72313eb4ca87178
