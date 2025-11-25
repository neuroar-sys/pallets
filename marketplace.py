import sqlite3
import google.generativeai as genai
from datetime import datetime
import threading

class PalletsAI:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generar_descripcion(self, info_producto):
        """Genera descripción de producto usando IA"""
        try:
            # ✅ CORREGIDO: Usar comillas triples normales, NO escapadas
            prompt = f"""
            Eres un experto en marketing para muebles de pallets ecológicos.
            Crea una descripción atractiva y persuasiva para este producto:
            
            Información del producto: {info_producto}
            
            La descripción debe:
            - Ser breve (100-150 palabras)
            - Destacar los beneficios ecológicos
            - Incluir características únicas
            - Ser atractiva para compradores
            - Usar un tono cálido y profesional
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Descripción estándar para {info_producto}. (Error en IA: {str(e)})"

class DatabaseManager:
    def __init__(self):
        # ✅ CORREGIDO: Usar :memory: para base de datos en memoria
        # Streamlit Cloud no persiste archivos en disco
        self.conn = sqlite3.connect(':memory:', check_same_thread=False)
        self.lock = threading.Lock()  # Para seguridad en entornos concurrentes
        self.create_tables()
    
    def create_tables(self):
        """Crea las tablas necesarias en la base de datos"""
        with self.lock:
            # Tabla de fabricantes
            self.conn.execute('''
                CREATE TABLE fabricantes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    localidad TEXT NOT NULL,
                    telefono TEXT NOT NULL,
                    especialidad TEXT,
                    experiencia INTEGER,
                    descripcion TEXT,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de productos
            self.conn.execute('''
                CREATE TABLE productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fabricante_id INTEGER,
                    nombre TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    descripcion TEXT,
                    precio REAL NOT NULL,
                    materiales TEXT,
                    dimensiones TEXT,
                    fecha_publicacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (fabricante_id) REFERENCES fabricantes (id)
                )
            ''')
            
            self.conn.commit()
    
    def agregar_fabricante(self, fabricante_data):
        """Agrega un nuevo fabricante a la base de datos"""
        try:
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO fabricantes (nombre, localidad, telefono, especialidad, experiencia, descripcion)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    fabricante_data['nombre'],
                    fabricante_data['localidad'],
                    fabricante_data['telefono'],
                    fabricante_data.get('especialidad', ''),
                    int(fabricante_data.get('experiencia', 0)),
                    fabricante_data.get('descripcion', '')
                ))
                self.conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error agregando fabricante: {e}")
            return None
    
    def obtener_fabricantes(self):
        """Obtiene todos los fabricantes registrados"""
        try:
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute('SELECT * FROM fabricantes ORDER BY fecha_registro DESC')
                return cursor.fetchall()
        except Exception as e:
            print(f"Error obteniendo fabricantes: {e}")
            return []
    
    def agregar_producto(self, producto_data):
        """Agrega un nuevo producto a la base de datos"""
        try:
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO productos (fabricante_id, nombre, categoria, descripcion, precio, materiales, dimensiones)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    producto_data['fabricante_id'],
                    producto_data['nombre'],
                    producto_data['categoria'],
                    producto_data.get('descripcion', ''),
                    float(producto_data['precio']),
                    producto_data.get('materiales', ''),
                    producto_data.get('dimensiones', '')
                ))
                self.conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error agregando producto: {e}")
            return None
    
    def obtener_productos(self):
        """Obtiene todos los productos con información del fabricante"""
        try:
            with self.lock:
                cursor = self.conn.cursor()
                cursor.execute('''
                    SELECT p.*, f.nombre as fabricante_nombre, f.localidad, f.telefono
                    FROM productos p
                    LEFT JOIN fabricantes f ON p.fabricante_id = f.id
                    ORDER BY p.fecha_publicacion DESC
                ''')
                return cursor.fetchall()
        except Exception as e:
            print(f"Error obteniendo productos: {e}")
            return []

# Para pruebas locales (opcional)
if __name__ == "__main__":
    db = DatabaseManager()
    print("Base de datos inicializada correctamente")