# -*- coding: utf-8 -*-
"""
MODELOS DE BASE DE DATOS - AZTLÁN DECODE
"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class TeamSearch(Base):
    """Historial de búsquedas de equipos"""
    __tablename__ = 'team_searches'
    
    id = Column(Integer, primary_key=True)
    team_number = Column(Integer, nullable=False, index=True)
    search_date = Column(DateTime, default=datetime.utcnow)
    module = Column(String(50))  # 'scouting', 'comparison'
    user_ip = Column(String(50))
    
class TeamAnalysis(Base):
    """Análisis guardados de equipos"""
    __tablename__ = 'team_analyses'
    
    id = Column(Integer, primary_key=True)
    team_number = Column(Integer, nullable=False, index=True)
    analysis_date = Column(DateTime, default=datetime.utcnow)
    
    # Datos del equipo
    team_name = Column(String(200))
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    
    # Análisis TRIDENTE
    toa_data = Column(JSON)  # Datos de TOA API
    scout_data = Column(JSON)  # Datos de Scout API
    first_data = Column(JSON)  # Datos de FIRST API
    consensus = Column(Text)  # Análisis consensuado
    
    # Métricas
    ranking = Column(Integer)
    opr = Column(Float)
    win_rate = Column(Float)
    matches_played = Column(Integer)
    
    # IA Analysis
    ai_analysis = Column(Text)
    strategic_recommendations = Column(Text)

class ExoplanetSimulation(Base):
    """Simulaciones de exoplanetas guardadas"""
    __tablename__ = 'exoplanet_simulations'
    
    id = Column(Integer, primary_key=True)
    simulation_date = Column(DateTime, default=datetime.utcnow)
    
    # Parámetros
    distance = Column(Float)
    radius = Column(Float)
    temperature = Column(Float)
    orbital_period = Column(Float)
    
    # Resultados
    is_habitable = Column(Boolean)
    habitability_score = Column(Float)
    confidence = Column(Float)
    details = Column(JSON)

class APICache(Base):
    """Cache de llamadas a APIs externas"""
    __tablename__ = 'api_cache'
    
    id = Column(Integer, primary_key=True)
    cache_key = Column(String(200), unique=True, index=True)
    api_name = Column(String(50))  # 'toa', 'scout', 'first', 'groq'
    cache_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime)
    
    # Datos cacheados
    request_params = Column(JSON)
    response_data = Column(JSON)
    status_code = Column(Integer)

class UserFavorite(Base):
    """Equipos favoritos de usuarios"""
    __tablename__ = 'user_favorites'
    
    id = Column(Integer, primary_key=True)
    user_ip = Column(String(50), index=True)
    team_number = Column(Integer, nullable=False)
    added_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)

class Visitor(Base):
    """Registro de visitantes únicos"""
    __tablename__ = 'visitors'
    
    id = Column(Integer, primary_key=True)
    visitor_id = Column(String(100), unique=True, index=True)  # Hash de IP + User Agent
    first_visit = Column(DateTime, default=datetime.utcnow)
    last_visit = Column(DateTime, default=datetime.utcnow)
    total_visits = Column(Integer, default=1)
    user_ip = Column(String(50))
    user_agent = Column(String(500))
    country = Column(String(100))
    city = Column(String(100))

class PageView(Base):
    """Registro de vistas de páginas"""
    __tablename__ = 'page_views'
    
    id = Column(Integer, primary_key=True)
    visitor_id = Column(String(100), index=True)
    page_url = Column(String(500))
    page_title = Column(String(200))
    visit_date = Column(DateTime, default=datetime.utcnow)
    session_id = Column(String(100))
    referrer = Column(String(500))
    duration_seconds = Column(Integer, default=0)

class MatchPrediction(Base):
    """Predicciones de matches guardadas"""
    __tablename__ = 'match_predictions'
    
    id = Column(Integer, primary_key=True)
    prediction_date = Column(DateTime, default=datetime.utcnow)
    
    # Match info
    team1 = Column(Integer, nullable=False)
    team2 = Column(Integer, nullable=False)
    
    # Predicción
    predicted_winner = Column(Integer)
    win_probability = Column(Float)
    predicted_score_diff = Column(Float)
    
    # Resultado real (si está disponible)
    actual_winner = Column(Integer)
    actual_score_diff = Column(Float)
    prediction_correct = Column(Boolean)

# Inicialización de la base de datos
def init_db(db_path='aztlan_decode.db'):
    """Inicializa la base de datos"""
    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return engine, Session

def get_session(db_path='aztlan_decode.db'):
    """Obtiene una sesión de base de datos"""
    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    Session = sessionmaker(bind=engine)
    return Session()
