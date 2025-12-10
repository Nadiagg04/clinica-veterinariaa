from conector import ConectorDB

class Mascota:
    def __init__(self, nombre, especie, edad, dueno, id=None):
        self.id = id
        self.nombre = nombre
        self.especie = especie
        self.edad = edad
        self.dueno = dueno

    # Crear o actualizar
    def guardar(self):
        db = ConectorDB()
        conexion = db.conectar()
        if conexion:
            cursor = conexion.cursor()
            if self.id is None:
                cursor.execute(
                    "INSERT INTO Mascota (nombre, especie, edad, dueno) VALUES (?, ?, ?, ?)",
                    (self.nombre, self.especie, self.edad, self.dueno)
                )
                self.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE Mascota SET nombre=?, especie=?, edad=?, dueno=? WHERE id=?",
                    (self.nombre, self.especie, self.edad, self.dueno, self.id)
                )
            conexion.commit()
            db.cerrar()

    # Leer todos los registros
    @staticmethod
    def obtener_todas():
        db = ConectorDB()
        conexion = db.conectar()
        mascotas = []
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, especie, edad, dueno FROM Mascota")
            for fila in cursor.fetchall():
                mascotas.append(Mascota(*fila[1:], id=fila[0]))
            db.cerrar()
        return mascotas

    # Eliminar registro
    def eliminar(self):
        if self.id is None:
            return
        db = ConectorDB()
        conexion = db.conectar()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Mascota WHERE id=?", (self.id,))
            conexion.commit()
            db.cerrar()


class Veterinario:
    def __init__(self, nombre, especialidad, id=None):
        self.id = id
        self.nombre = nombre
        self.especialidad = especialidad

    # Crear o actualizar
    def guardar(self):
        db = ConectorDB()
        conexion = db.conectar()
        if conexion:
            cursor = conexion.cursor()
            if self.id is None:
                cursor.execute(
                    "INSERT INTO Veterinario (nombre, especialidad) VALUES (?, ?)",
                    (self.nombre, self.especialidad)
                )
                self.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE Veterinario SET nombre=?, especialidad=? WHERE id=?",
                    (self.nombre, self.especialidad, self.id)
                )
            conexion.commit()
            db.cerrar()

    # Leer todos los registros
    @staticmethod
    def obtener_todos():
        db = ConectorDB()
        conexion = db.conectar()
        vets = []
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, especialidad FROM Veterinario")
            for fila in cursor.fetchall():
                vets.append(Veterinario(fila[1], fila[2], id=fila[0]))
            db.cerrar()
        return vets

    # Eliminar registro
    def eliminar(self):
        if self.id is None:
            return
        db = ConectorDB()
        conexion = db.conectar()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Veterinario WHERE id=?", (self.id,))
            conexion.commit()
            db.cerrar()

class Producto:
    def __init__(self, nombre, precio, stock, id=None):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def guardar(self):
        db = ConectorDB()
        conexion = db.conectar()
        if conexion:
            cursor = conexion.cursor()
            if self.id is None:
                cursor.execute(
                    "INSERT INTO Producto (nombre, precio, stock) VALUES (?, ?, ?)",
                    (self.nombre, self.precio, self.stock)
                )
                self.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE Producto SET nombre=?, precio=?, stock=? WHERE id=?",
                    (self.nombre, self.precio, self.stock, self.id)
                )
            conexion.commit()
            db.cerrar()

    @staticmethod
    def obtener_todos():
        db = ConectorDB()
        conexion = db.conectar()
        productos = []
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, precio, stock FROM Producto")
            for fila in cursor.fetchall():
                productos.append(Producto(fila[1], fila[2], fila[3], id=fila[0]))
            db.cerrar()
        return productos

    def eliminar(self):
        if self.id is None:
            return
        db = ConectorDB()
        conexion = db.conectar()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Producto WHERE id=?", (self.id,))
            conexion.commit()
            db.cerrar()
