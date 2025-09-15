# ================================================================
# ARCHIVO DE CONEXIÓN A LA BASE DE DATOS - AGROMATCH PYTHON
# Ruta: conexion/conexion.py
# ================================================================

import mysql.connector
from mysql.connector import Error
import os
from contextlib import contextmanager

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'Agromach_V2',  # Usando tu base de datos V2
    'user': 'root'
}

# Array de contraseñas posibles para diferentes configuraciones
PASSWORDS_TO_TRY = ['', '123456', 'password', 'admin']

def get_connection():
    """
    Establece conexión con la base de datos MySQL.
    Prueba diferentes contraseñas hasta encontrar una válida.
    """
    connection = None
    
    for password in PASSWORDS_TO_TRY:
        try:
            config = DB_CONFIG.copy()
            config['password'] = password
            
            connection = mysql.connector.connect(**config)
            
            if connection.is_connected():
                print(f"Conexión exitosa a MySQL con contraseña: {'(vacía)' if password == '' else '***'}")
                return connection
                
        except Error as e:
            continue
    
    if connection is None:
        raise Exception("Error: No se pudo conectar a la base de datos con ninguna contraseña.")

@contextmanager
def get_db_connection():
    """
    Context manager para manejar conexiones de base de datos de forma segura.
    """
    connection = None
    try:
        connection = get_connection()
        yield connection
    finally:
        if connection and connection.is_connected():
            connection.close()

def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """
    Ejecuta una consulta SQL de forma segura.
    
    Args:
        query (str): La consulta SQL
        params (tuple): Parámetros para la consulta
        fetch_one (bool): Si debe retornar solo un resultado
        fetch_all (bool): Si debe retornar todos los resultados
    
    Returns:
        Resultado de la consulta o None
    """
    with get_db_connection() as connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            
            if fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            else:
                connection.commit()
                return cursor.lastrowid if cursor.lastrowid else True
                
        except Error as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()

def test_connection():
    """
    Prueba la conexión a la base de datos.
    """
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"Conexión exitosa. Versión de MySQL: {version[0]}")
            return True
    except Exception as e:
        print(f"Error al conectar: {e}")
        return False

if __name__ == "__main__":
    # Prueba la conexión cuando se ejecuta directamente
    test_connection()
    
def execute_query_dict(query, params=None, fetch_one=False):
    """
    Función que devuelve diccionarios para compatibilidad con rutas nuevas
    """
    connection = None
    cursor = None
    
    try:
        connection = get_connection()  # Usa tu función existente de conexión
        cursor = connection.cursor(dictionary=True)  # IMPORTANTE: dictionary=True
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if query.strip().upper().startswith('SELECT'):
            if fetch_one:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
        else:
            connection.commit()
            if query.strip().upper().startswith('INSERT'):
                result = cursor.lastrowid
            else:
                result = cursor.rowcount
        
        return result
        
    except Exception as e:
        print(f"Error en execute_query_dict: {e}")
        if connection:
            connection.rollback()
        return None
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()