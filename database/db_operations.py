# -*- coding: utf-8 -*-
"""
OPERACIONES DE BASE DE DATOS - AZTLÁN DECODE
"""

from datetime import datetime, timedelta
from database.models import (
    get_session, TeamSearch, TeamAnalysis, ExoplanetSimulation,
    APICache, UserFavorite, MatchPrediction
)
import hashlib
import json

class DatabaseManager:
    """Gestor de operaciones de base de datos"""
    
    def __init__(self, db_path='aztlan_decode.db'):
        self.db_path = db_path
    
    def _get_session(self):
        """Obtiene sesión de DB"""
        return get_session(self.db_path)
    
    # =====================================================
    # HISTORIAL DE BÚSQUEDAS
    # =====================================================
    
    def save_team_search(self, team_number, module='scouting', user_ip='unknown'):
        """Guarda una búsqueda de equipo"""
        session = self._get_session()
        try:
            search = TeamSearch(
                team_number=team_number,
                module=module,
                user_ip=user_ip
            )
            session.add(search)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error guardando búsqueda: {e}")
            return False
        finally:
            session.close()
    
    def get_search_history(self, limit=50):
        """Obtiene historial de búsquedas"""
        session = self._get_session()
        try:
            searches = session.query(TeamSearch)\
                .order_by(TeamSearch.search_date.desc())\
                .limit(limit)\
                .all()
            return [{
                'team_number': s.team_number,
                'module': s.module,
                'date': s.search_date.isoformat()
            } for s in searches]
        except Exception as e:
            print(f"Error obteniendo historial: {e}")
            return []
        finally:
            session.close()
    
    def get_most_searched_teams(self, limit=10):
        """Obtiene equipos más buscados"""
        session = self._get_session()
        try:
            from sqlalchemy import func
            results = session.query(
                TeamSearch.team_number,
                func.count(TeamSearch.id).label('count')
            ).group_by(TeamSearch.team_number)\
             .order_by(func.count(TeamSearch.id).desc())\
             .limit(limit)\
             .all()
            return [{'team': r[0], 'searches': r[1]} for r in results]
        except Exception as e:
            print(f"Error obteniendo equipos populares: {e}")
            return []
        finally:
            session.close()
    
    # =====================================================
    # ANÁLISIS DE EQUIPOS
    # =====================================================
    
    def save_team_analysis(self, team_number, analysis_data):
        """Guarda análisis completo de un equipo"""
        session = self._get_session()
        try:
            analysis = TeamAnalysis(
                team_number=team_number,
                team_name=analysis_data.get('team_name'),
                city=analysis_data.get('city'),
                state=analysis_data.get('state'),
                country=analysis_data.get('country'),
                toa_data=analysis_data.get('toa_data'),
                scout_data=analysis_data.get('scout_data'),
                first_data=analysis_data.get('first_data'),
                consensus=analysis_data.get('consensus'),
                ranking=analysis_data.get('ranking'),
                opr=analysis_data.get('opr'),
                win_rate=analysis_data.get('win_rate'),
                matches_played=analysis_data.get('matches_played'),
                ai_analysis=analysis_data.get('ai_analysis'),
                strategic_recommendations=analysis_data.get('recommendations')
            )
            session.add(analysis)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error guardando análisis: {e}")
            return False
        finally:
            session.close()
    
    def get_team_analysis(self, team_number):
        """Obtiene el análisis más reciente de un equipo"""
        session = self._get_session()
        try:
            analysis = session.query(TeamAnalysis)\
                .filter_by(team_number=team_number)\
                .order_by(TeamAnalysis.analysis_date.desc())\
                .first()
            
            if analysis:
                return {
                    'team_number': analysis.team_number,
                    'team_name': analysis.team_name,
                    'city': analysis.city,
                    'state': analysis.state,
                    'country': analysis.country,
                    'date': analysis.analysis_date.isoformat(),
                    'ranking': analysis.ranking,
                    'opr': analysis.opr,
                    'win_rate': analysis.win_rate,
                    'matches_played': analysis.matches_played,
                    'ai_analysis': analysis.ai_analysis,
                    'recommendations': analysis.strategic_recommendations
                }
            return None
        except Exception as e:
            print(f"Error obteniendo análisis: {e}")
            return None
        finally:
            session.close()
    
    # =====================================================
    # CACHE DE APIS
    # =====================================================
    
    def get_cache_key(self, api_name, params):
        """Genera clave única para cache"""
        key_str = f"{api_name}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get_cached_response(self, api_name, params, max_age_hours=24):
        """Obtiene respuesta cacheada si existe y no ha expirado"""
        session = self._get_session()
        try:
            cache_key = self.get_cache_key(api_name, params)
            cached = session.query(APICache)\
                .filter_by(cache_key=cache_key)\
                .first()
            
            if cached:
                # Verificar si no ha expirado
                if cached.expiry_date > datetime.utcnow():
                    return cached.response_data
            return None
        except Exception as e:
            print(f"Error obteniendo cache: {e}")
            return None
        finally:
            session.close()
    
    def save_to_cache(self, api_name, params, response_data, cache_hours=24):
        """Guarda respuesta en cache"""
        session = self._get_session()
        try:
            cache_key = self.get_cache_key(api_name, params)
            
            # Verificar si ya existe
            existing = session.query(APICache)\
                .filter_by(cache_key=cache_key)\
                .first()
            
            expiry = datetime.utcnow() + timedelta(hours=cache_hours)
            
            if existing:
                # Actualizar
                existing.response_data = response_data
                existing.cache_date = datetime.utcnow()
                existing.expiry_date = expiry
            else:
                # Crear nuevo
                cache = APICache(
                    cache_key=cache_key,
                    api_name=api_name,
                    cache_date=datetime.utcnow(),
                    expiry_date=expiry,
                    request_params=params,
                    response_data=response_data
                )
                session.add(cache)
            
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error guardando en cache: {e}")
            return False
        finally:
            session.close()
    
    def clear_expired_cache(self):
        """Limpia cache expirado"""
        session = self._get_session()
        try:
            deleted = session.query(APICache)\
                .filter(APICache.expiry_date < datetime.utcnow())\
                .delete()
            session.commit()
            return deleted
        except Exception as e:
            session.rollback()
            print(f"Error limpiando cache: {e}")
            return 0
        finally:
            session.close()
    
    # =====================================================
    # FAVORITOS
    # =====================================================
    
    def add_favorite(self, user_ip, team_number, notes=''):
        """Agrega equipo a favoritos"""
        session = self._get_session()
        try:
            # Verificar si ya existe
            existing = session.query(UserFavorite)\
                .filter_by(user_ip=user_ip, team_number=team_number)\
                .first()
            
            if existing:
                return False  # Ya existe
            
            favorite = UserFavorite(
                user_ip=user_ip,
                team_number=team_number,
                notes=notes
            )
            session.add(favorite)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error agregando favorito: {e}")
            return False
        finally:
            session.close()
    
    def get_favorites(self, user_ip):
        """Obtiene favoritos de un usuario"""
        session = self._get_session()
        try:
            favorites = session.query(UserFavorite)\
                .filter_by(user_ip=user_ip)\
                .order_by(UserFavorite.added_date.desc())\
                .all()
            return [{
                'team_number': f.team_number,
                'notes': f.notes,
                'added_date': f.added_date.isoformat()
            } for f in favorites]
        except Exception as e:
            print(f"Error obteniendo favoritos: {e}")
            return []
        finally:
            session.close()
    
    def remove_favorite(self, user_ip, team_number):
        """Elimina equipo de favoritos"""
        session = self._get_session()
        try:
            deleted = session.query(UserFavorite)\
                .filter_by(user_ip=user_ip, team_number=team_number)\
                .delete()
            session.commit()
            return deleted > 0
        except Exception as e:
            session.rollback()
            print(f"Error eliminando favorito: {e}")
            return False
        finally:
            session.close()
    
    # =====================================================
    # ESTADÍSTICAS GLOBALES
    # =====================================================
    
    def get_stats(self):
        """Obtiene estadísticas globales del sistema"""
        session = self._get_session()
        try:
            from sqlalchemy import func
            
            total_searches = session.query(func.count(TeamSearch.id)).scalar()
            total_analyses = session.query(func.count(TeamAnalysis.id)).scalar()
            total_predictions = session.query(func.count(MatchPrediction.id)).scalar()
            cached_items = session.query(func.count(APICache.id)).scalar()
            
            # Búsquedas últimas 24 horas
            yesterday = datetime.utcnow() - timedelta(days=1)
            recent_searches = session.query(func.count(TeamSearch.id))\
                .filter(TeamSearch.search_date > yesterday)\
                .scalar()
            
            return {
                'total_searches': total_searches or 0,
                'total_analyses': total_analyses or 0,
                'total_predictions': total_predictions or 0,
                'cached_items': cached_items or 0,
                'searches_24h': recent_searches or 0
            }
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            return {}
        finally:
            session.close()
