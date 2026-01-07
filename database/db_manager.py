#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AZTLÁN DECODE - GESTOR DE BASE DE DATOS
Sistema de persistencia con SQLite + Encriptación
"""

import sqlite3
import hashlib
import json
from datetime import datetime, timedelta
from functools import wraps
import os
from contextlib import contextmanager

class DatabaseManager:
    """Gestor de base de datos con seguridad y encriptación"""
    
    def __init__(self, db_path='database/aztlan.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._initialize_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager para conexiones seguras"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _initialize_database(self):
        """Crear todas las tablas necesarias"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabla de usuarios con verificación de edad
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    birth_date TEXT NOT NULL,
                    age_verified BOOLEAN DEFAULT 0,
                    age_verification_method TEXT,
                    is_minor BOOLEAN DEFAULT 0,
                    parent_email TEXT,
                    parental_consent BOOLEAN DEFAULT 0,
                    consent_date TEXT,
                    privacy_settings TEXT DEFAULT '{"level": "high"}',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    last_login TEXT,
                    account_status TEXT DEFAULT 'active'
                )
            ''')
            
            # Tabla de sesiones
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_token TEXT UNIQUE NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    expires_at TEXT NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Tabla de búsquedas (historial permanente)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS search_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    search_type TEXT NOT NULL,
                    search_query TEXT NOT NULL,
                    search_data TEXT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Tabla de favoritos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS favorites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    item_type TEXT NOT NULL,
                    item_id TEXT NOT NULL,
                    item_data TEXT,
                    notes TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    UNIQUE(user_id, item_type, item_id)
                )
            ''')
            
            # Tabla de cache de APIs
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS api_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cache_key TEXT UNIQUE NOT NULL,
                    cache_data TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    expires_at TEXT NOT NULL
                )
            ''')
            
            # Tabla de reportes exportados
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS exports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    export_type TEXT NOT NULL,
                    export_format TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Tabla de auditoría (compliance)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT NOT NULL,
                    details TEXT,
                    ip_address TEXT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Tabla de notificaciones
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    notification_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    message TEXT NOT NULL,
                    read BOOLEAN DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Índices para optimización
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(session_token)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_cache_key ON api_cache(cache_key)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_search_user ON search_history(user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_favorites_user ON favorites(user_id)')
    
    def create_user(self, username, email, password, birth_date, parent_email=None):
        """Crear usuario con verificación de edad automática"""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Calcular edad
        birth = datetime.strptime(birth_date, '%Y-%m-%d')
        age = (datetime.now() - birth).days // 365
        is_minor = age < 18
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, birth_date, is_minor, parent_email)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, email, password_hash, birth_date, is_minor, parent_email))
            
            user_id = cursor.lastrowid
            
            # Log de auditoría
            self._log_audit(user_id, 'USER_CREATED', f'New user created - Minor: {is_minor}')
            
            return user_id
    
    def authenticate_user(self, email, password):
        """Autenticar usuario y crear sesión"""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM users WHERE email = ? AND password_hash = ?
            ''', (email, password_hash))
            
            user = cursor.fetchone()
            if not user:
                return None
            
            # Crear sesión
            import secrets
            session_token = secrets.token_urlsafe(32)
            expires_at = (datetime.now() + timedelta(days=7)).isoformat()
            
            cursor.execute('''
                INSERT INTO sessions (user_id, session_token, expires_at)
                VALUES (?, ?, ?)
            ''', (user['id'], session_token, expires_at))
            
            # Actualizar último login
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
            ''', (user['id'],))
            
            self._log_audit(user['id'], 'USER_LOGIN', 'User logged in')
            
            return {
                'user_id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'is_minor': user['is_minor'],
                'session_token': session_token
            }
    
    def verify_session(self, session_token):
        """Verificar si una sesión es válida"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.*, u.* FROM sessions s
                JOIN users u ON s.user_id = u.id
                WHERE s.session_token = ? AND s.expires_at > ?
            ''', (session_token, datetime.now().isoformat()))
            
            return cursor.fetchone()
    
    def add_search_history(self, user_id, search_type, search_query, search_data=None):
        """Agregar búsqueda al historial permanente"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO search_history (user_id, search_type, search_query, search_data)
                VALUES (?, ?, ?, ?)
            ''', (user_id, search_type, search_query, json.dumps(search_data) if search_data else None))
    
    def get_search_history(self, user_id, limit=50):
        """Obtener historial de búsquedas"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM search_history WHERE user_id = ?
                ORDER BY timestamp DESC LIMIT ?
            ''', (user_id, limit))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def add_favorite(self, user_id, item_type, item_id, item_data=None, notes=None):
        """Agregar a favoritos"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO favorites (user_id, item_type, item_id, item_data, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, item_type, item_id, json.dumps(item_data) if item_data else None, notes))
    
    def get_favorites(self, user_id, item_type=None):
        """Obtener favoritos"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if item_type:
                cursor.execute('''
                    SELECT * FROM favorites WHERE user_id = ? AND item_type = ?
                    ORDER BY created_at DESC
                ''', (user_id, item_type))
            else:
                cursor.execute('''
                    SELECT * FROM favorites WHERE user_id = ?
                    ORDER BY created_at DESC
                ''', (user_id,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def cache_api_data(self, cache_key, data, ttl_hours=24):
        """Guardar datos de API en cache"""
        expires_at = (datetime.now() + timedelta(hours=ttl_hours)).isoformat()
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO api_cache (cache_key, cache_data, expires_at)
                VALUES (?, ?, ?)
            ''', (cache_key, json.dumps(data), expires_at))
    
    def get_cached_api_data(self, cache_key):
        """Obtener datos cacheados de API"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT cache_data FROM api_cache 
                WHERE cache_key = ? AND expires_at > ?
            ''', (cache_key, datetime.now().isoformat()))
            
            row = cursor.fetchone()
            if row:
                return json.loads(row['cache_data'])
            return None
    
    def _log_audit(self, user_id, action, details, ip_address=None):
        """Registrar acción en auditoría (compliance)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO audit_log (user_id, action, details, ip_address)
                VALUES (?, ?, ?, ?)
            ''', (user_id, action, details, ip_address))
    
    def cleanup_expired(self):
        """Limpiar datos expirados (sessions, cache)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            
            cursor.execute('DELETE FROM sessions WHERE expires_at < ?', (now,))
            cursor.execute('DELETE FROM api_cache WHERE expires_at < ?', (now,))
            
            return cursor.rowcount

# Instancia global
db = DatabaseManager()
