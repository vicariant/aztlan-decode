#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AZTLÁN DECODE - DASHBOARD AVANZADO
Estadísticas globales y análisis histórico
"""

from collections import defaultdict
from datetime import datetime, timedelta
import numpy as np

class AdvancedDashboard:
    """Dashboard con métricas globales y análisis avanzado"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def get_global_statistics(self):
        """Obtener estadísticas globales de la plataforma"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total de usuarios
            cursor.execute('SELECT COUNT(*) FROM users WHERE account_status = "active"')
            total_users = cursor.fetchone()[0]
            
            # Usuarios menores
            cursor.execute('SELECT COUNT(*) FROM users WHERE is_minor = 1 AND account_status = "active"')
            minor_users = cursor.fetchone()[0]
            
            # Total de búsquedas
            cursor.execute('SELECT COUNT(*) FROM search_history')
            total_searches = cursor.fetchone()[0]
            
            # Equipos más buscados (top 10)
            cursor.execute('''
                SELECT search_query, COUNT(*) as count
                FROM search_history
                WHERE search_type = 'team'
                GROUP BY search_query
                ORDER BY count DESC
                LIMIT 10
            ''')
            top_teams = [{'team': row['search_query'], 'searches': row['count']} 
                        for row in cursor.fetchall()]
            
            # Actividad reciente (últimas 24h)
            yesterday = (datetime.now() - timedelta(days=1)).isoformat()
            cursor.execute('''
                SELECT COUNT(*) FROM search_history WHERE timestamp > ?
            ''', (yesterday,))
            recent_activity = cursor.fetchone()[0]
            
            # Usuarios activos (última semana)
            week_ago = (datetime.now() - timedelta(days=7)).isoformat()
            cursor.execute('''
                SELECT COUNT(DISTINCT user_id) FROM search_history WHERE timestamp > ?
            ''', (week_ago,))
            active_users = cursor.fetchone()[0]
            
            return {
                'total_users': total_users,
                'minor_users': minor_users,
                'total_searches': total_searches,
                'top_teams': top_teams,
                'recent_activity_24h': recent_activity,
                'active_users_week': active_users,
                'minor_percentage': (minor_users / total_users * 100) if total_users > 0 else 0
            }
    
    def get_user_dashboard(self, user_id):
        """Dashboard personalizado para usuario"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Información del usuario
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            user = dict(cursor.fetchone())
            
            # Estadísticas de búsqueda
            cursor.execute('''
                SELECT COUNT(*) as total, search_type
                FROM search_history
                WHERE user_id = ?
                GROUP BY search_type
            ''', (user_id,))
            search_stats = {row['search_type']: row['total'] for row in cursor.fetchall()}
            
            # Favoritos
            cursor.execute('SELECT COUNT(*) FROM favorites WHERE user_id = ?', (user_id,))
            total_favorites = cursor.fetchone()[0]
            
            # Exportaciones
            cursor.execute('SELECT COUNT(*) FROM exports WHERE user_id = ?', (user_id,))
            total_exports = cursor.fetchone()[0]
            
            # Actividad reciente
            cursor.execute('''
                SELECT * FROM search_history
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT 10
            ''', (user_id,))
            recent_searches = [dict(row) for row in cursor.fetchall()]
            
            # Equipos favoritos
            cursor.execute('''
                SELECT * FROM favorites
                WHERE user_id = ? AND item_type = 'team'
                ORDER BY created_at DESC
            ''', (user_id,))
            favorite_teams = [dict(row) for row in cursor.fetchall()]
            
            return {
                'user': user,
                'search_stats': search_stats,
                'total_favorites': total_favorites,
                'total_exports': total_exports,
                'recent_searches': recent_searches,
                'favorite_teams': favorite_teams
            }
    
    def get_trending_teams(self, timeframe_days=7):
        """Equipos trending en los últimos N días"""
        cutoff = (datetime.now() - timedelta(days=timeframe_days)).isoformat()
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT search_query, COUNT(*) as count
                FROM search_history
                WHERE search_type = 'team' AND timestamp > ?
                GROUP BY search_query
                ORDER BY count DESC
                LIMIT 20
            ''', (cutoff,))
            
            return [{'team': row['search_query'], 'searches': row['count']} 
                   for row in cursor.fetchall()]
    
    def get_platform_health(self):
        """Métricas de salud de la plataforma"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Tasa de error (búsquedas sin resultados)
            cursor.execute('''
                SELECT COUNT(*) FROM search_history WHERE search_data IS NULL
            ''')
            failed_searches = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM search_history')
            total_searches = cursor.fetchone()[0]
            
            error_rate = (failed_searches / total_searches * 100) if total_searches > 0 else 0
            
            # Tiempo de respuesta promedio (simulado)
            avg_response_time = 150  # ms (en producción medir real)
            
            # Uptime (simulado)
            uptime_percentage = 99.9
            
            # Cache hit rate
            cursor.execute('SELECT COUNT(*) FROM api_cache WHERE expires_at > ?', 
                          (datetime.now().isoformat(),))
            cache_hits = cursor.fetchone()[0]
            
            return {
                'error_rate': error_rate,
                'avg_response_time_ms': avg_response_time,
                'uptime_percentage': uptime_percentage,
                'cache_hit_rate': 85.5,  # Simulado
                'total_cached_items': cache_hits,
                'status': 'healthy' if error_rate < 5 and uptime_percentage > 99 else 'degraded'
            }
    
    def get_compliance_report(self):
        """Reporte de cumplimiento de protección de menores"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Usuarios menores sin consentimiento parental
            cursor.execute('''
                SELECT COUNT(*) FROM users
                WHERE is_minor = 1 AND (parental_consent = 0 OR parental_consent IS NULL)
            ''')
            minors_without_consent = cursor.fetchone()[0]
            
            # Usuarios con verificación de edad pendiente
            cursor.execute('''
                SELECT COUNT(*) FROM users WHERE age_verified = 0
            ''')
            unverified_users = cursor.fetchone()[0]
            
            # Auditoría de acciones de menores (últimos 30 días)
            month_ago = (datetime.now() - timedelta(days=30)).isoformat()
            cursor.execute('''
                SELECT COUNT(*) FROM audit_log
                WHERE timestamp > ? AND user_id IN (SELECT id FROM users WHERE is_minor = 1)
            ''', (month_ago,))
            minor_actions_month = cursor.fetchone()[0]
            
            return {
                'minors_without_consent': minors_without_consent,
                'unverified_users': unverified_users,
                'minor_actions_last_30_days': minor_actions_month,
                'compliance_status': 'compliant' if minors_without_consent == 0 else 'action_required'
            }

# No instanciar aquí, se instancia en app.py con db
