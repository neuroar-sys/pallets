import sqlite3
import json
from datetime import datetime
import google.generativeai as genai
import os

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('pallets_marketplace.db', check_same_thread=False)
        self.init_database()
    
    def init_database(self):
        cursor = self.conn.cursor()
        
        # Tabla fabricantes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fabricantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                localidad TEXT NOT NULL,
                telefono TEXT,
                especialidad TEXT,
                experiencia TEXT,
                descripcion TEXT,
                fecha_registro DATE
            )
        ''')
        
        # Tabla productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fabricante_id INTEGER,
                nombre TEXT NOT NULL,
                categoria TEXT,
                descripcion TEXT,
                precio INTEGER,
                materiales TEXT,
                dimensiones TEXT,
                estado TEXT DEFAULT 'disponible',
                fecha_publicacion DATE,
                FOREIGN KEY (fabricante_id) REFERENCES fabricantes (id)
            )
        ''')
        
        self.conn.commit()
    
    def agregar_fabricante(self, datos):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO fabricantes (nombre, localidad, telefono, especialidad, experiencia, descripcion, fecha_registro)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            datos['nombre'],
            datos['localidad'],
            datos.get('telefono', ''),
            datos.get('especialidad', ''),
            datos.get('experiencia', ''),
            datos.get('descripcion', ''),
            datetime.now().date()
        ))
        fabricante_id = cursor.lastrowid
        self.conn.commit()
        return fabricante_id
    
    def obtener_fabricantes(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM fabricantes')
        return cursor.fetchall()
    
    def agregar_producto(self, datos):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO productos (fabricante_id, nombre, categoria, descripcion, precio, materiales, dimensiones, fecha_publicacion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datos['fabricante_id'],
            datos['nombre'],
            datos['categoria'],
            datos.get('descripcion', ''),
            datos['precio'],
            datos.get('materiales', ''),
            datos.get('dimensiones', ''),
            datetime.now().date()
        ))
        producto_id = cursor.lastrowid
        self.conn.commit()
        return producto_id
    
    def obtener_productos(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT p.*, f.nombre as fabricante_nombre, f.localidad, f.telefono
            FROM productos p
            JOIN fabricantes f ON p.fabricante_id = f.id
        ''')
        return cursor.fetchall()

class PalletsAI:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.db = DatabaseManager()
    
    def generar_descripcion(self, producto_info):
        prompt = f\"\"\"Eres un experto en marketing para muebles de pallets reciclados.
        
        Información del producto: {producto_info}
        
        Genera una descripción comercial atractiva que:
        - Destaque que es ecológico y sustentable
        - Mencione que es artesanal y único
        - Sea cálida y persuasiva
        - Máximo 100 palabras
        
        Responde SOLO con la descripción, sin títulos adicionales.\"\"\"
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f\"Descripción del producto: {producto_info}. Hecho artesanalmente con pallets reciclados. \"

# Prueba rápida de la base de datos
if __name__ == \"__main__\":
    db = DatabaseManager()
    print(\" Base de datos inicializada correctamente\")
    print(\" Fabricantes:\", len(db.obtener_fabricantes()))
    print(\" Productos:\", len(db.obtener_productos()))
