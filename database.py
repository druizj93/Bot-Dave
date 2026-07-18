import sqlite3
import json
from datetime import datetime

class Database:
    def __init__(self, db_name='bot.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        """Crea las tablas necesarias con comentarios."""
        cursor = self.conn.cursor()
        
        # Tabla de usuarios (acceso restringido)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            allowed BOOLEAN DEFAULT FALSE,
            created_at TEXT
        )
        ''')
        
        # Memoria persistente
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT,
            response TEXT,
            model_used TEXT,
            timestamp TEXT
        )
        ''')
        
        # Datos de trading
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS trading_positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            symbol TEXT,
            position_type TEXT,  # long/short
            entry_price REAL,
            current_price REAL,
            status TEXT,
            timestamp TEXT
        )
        ''')
        
        # Notificaciones
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT,
            sent BOOLEAN DEFAULT FALSE,
            timestamp TEXT
        )
        ''')
        
        self.conn.commit()

    def add_user(self, user_id, username):
        """Añade usuario y permite solo al owner."""
        cursor = self.conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (user_id, username, allowed, created_at) VALUES (?, ?, ?, ?)",
                      (user_id, username, True, datetime.now().isoformat()))  # Set True for owner
        self.conn.commit()

    def is_allowed(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT allowed FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        return result and result[0]

    # Add more methods for memory, trading, etc.
    def save_conversation(self, user_id, message, response, model):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO conversations (user_id, message, response, model_used, timestamp) VALUES (?, ?, ?, ?, ?)",
                      (user_id, message, response, model, datetime.now().isoformat()))
        self.conn.commit()

    def get_memory(self, user_id, limit=10):
        cursor = self.conn.cursor()
        cursor.execute("SELECT message, response FROM conversations WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?", 
                      (user_id, limit))
        return cursor.fetchall()