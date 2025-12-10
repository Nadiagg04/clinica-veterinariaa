import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

import sqlite3

class ConectorDB:
    def __init__(self):
        self.db_file = "clinica_veterinaria.db"
        self.conexion = None    

    def conectar(self):
        try:
            self.conexion = sqlite3.connect(self.db_file)
            print("Conexión exitosa a SQLite")
        except Exception as e:
            print(f"Error al conectar: {e}")
            self.conexion = None
        return self.conexion

    def cerrar(self):
        if self.conexion:
            self.conexion.close()
            print("Conexión cerrada")
