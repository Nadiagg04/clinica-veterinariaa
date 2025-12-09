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


