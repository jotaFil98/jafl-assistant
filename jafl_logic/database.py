# database.py

import sqlite3
from datetime import datetime
import threading

DB_NAME = 'jafl_data.db'
lock = threading.Lock()

# ------------------- Conexión -------------------

def get_db_connection():
    """Establece y devuelve la conexión a la base de datos."""
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    return conn

# ------------------- Creación de tablas -------------------

def create_interactions_table():
    """Crea la tabla de interacciones si no existe."""
    with lock:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT,
                response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Tabla para respuestas específicas (pregunta-respuesta)
        c.execute('''
            CREATE TABLE IF NOT EXISTS respuestas (
                pregunta TEXT PRIMARY KEY,
                respuesta TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

# ------------------- Operaciones Interacciones -------------------

def insert_interaction(user_input, response):
    """Inserta una nueva interacción en la base de datos."""
    with lock:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO interactions (user_input, response) VALUES (?, ?)",
            (user_input, response)
        )
        conn.commit()
        conn.close()

def get_all_interactions():
    """Obtiene todas las interacciones registradas."""
    with lock:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM interactions")
        rows = c.fetchall()
        conn.close()
    return rows

def get_last_interaction():
    """Obtiene la última interacción registrada."""
    with lock:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM interactions ORDER BY timestamp DESC LIMIT 1")
        row = c.fetchone()
        conn.close()
    return row

def delete_all_interactions():
    """Elimina todas las interacciones."""
    with lock:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("DELETE FROM interactions")
        conn.commit()
        conn.close()

def get_interactions_by_date(date_str):
    """
    Devuelve todas las interacciones de una fecha específica (YYYY-MM-DD).
    """
    with lock:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("""
            SELECT * FROM interactions
            WHERE DATE(timestamp) = ?
        """, (date_str,))
        rows = c.fetchall()
        conn.close()
    return rows

def get_interaction_count():
    """Devuelve el número total de interacciones registradas."""
    with lock:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM interactions")
        count = c.fetchone()[0]
        conn.close()
    return count

def get_most_common_phrases(limit=5):
    """
    Devuelve las frases más usadas por el usuario (user_input), ordenadas por frecuencia.
    """
    with lock:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("""
            SELECT user_input, COUNT(*) as freq
            FROM interactions
            GROUP BY user_input
            ORDER BY freq DESC
            LIMIT ?
        """, (limit,))
        rows = c.fetchall()
        conn.close()
    return rows

# ------------------- Operaciones para respuestas guardadas -------------------

def get_respuesta_de_base(pregunta):
    """Busca una respuesta guardada para una pregunta específica."""
    pregunta_norm = pregunta.lower().strip()
    with lock:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT respuesta FROM respuestas WHERE pregunta = ?", (pregunta_norm,))
        fila = c.fetchone()
        conn.close()
    if fila:
        return fila[0]
    return None

def agregar_respuesta_a_base(pregunta, respuesta):
    """Agrega o actualiza una respuesta para una pregunta específica."""
    pregunta_norm = pregunta.lower().strip()
    with lock:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            "INSERT OR REPLACE INTO respuestas (pregunta, respuesta) VALUES (?, ?)",
            (pregunta_norm, respuesta)
        )
        conn.commit()
        conn.close()

def obtener_todas_respuestas():
    """Obtiene todas las preguntas y respuestas guardadas."""
    with lock:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT pregunta, respuesta FROM respuestas")
        filas = c.fetchall()
        conn.close()
    return {pregunta: respuesta for pregunta, respuesta in filas}

# ------------------- Inicialización -------------------

# Crear tablas al importar el módulo para asegurar que existan
create_interactions_table()
