#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SISTEMA DE ANALÍTICAS DE VISITANTES
====================================
Tracking de visitantes, visitas y estadísticas de uso
"""

import os
import hashlib
from datetime import datetime, timedelta
from flask import request, session
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database.models import Base, Visitor, PageView
import logging

logger = logging.getLogger(__name__)

class VisitorAnalytics:
    """Sistema de analíticas de visitantes"""
    
    def __init__(self, db_path='database/analytics.db'):
        """Inicializa el sistema de analíticas"""
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def _get_visitor_id(self):
        """Genera ID único para visitante basado en IP + User Agent"""
        ip = request.remote_addr or 'unknown'
        user_agent = request.headers.get('User-Agent', 'unknown')
        
        # Hash para privacidad
        unique_string = f"{ip}:{user_agent}"
        visitor_id = hashlib.sha256(unique_string.encode()).hexdigest()[:32]
        
        return visitor_id, ip, user_agent
    
    def track_visit(self, page_url, page_title=''):
        """Registra una visita a una página"""
        try:
            visitor_id, ip, user_agent = self._get_visitor_id()
            
            # Buscar o crear visitante
            visitor = self.session.query(Visitor).filter_by(visitor_id=visitor_id).first()
            
            if visitor:
                # Visitante recurrente
                visitor.last_visit = datetime.utcnow()
                visitor.total_visits += 1
            else:
                # Nuevo visitante
                visitor = Visitor(
                    visitor_id=visitor_id,
                    user_ip=ip,
                    user_agent=user_agent[:500],
                    first_visit=datetime.utcnow(),
                    last_visit=datetime.utcnow(),
                    total_visits=1
                )
                self.session.add(visitor)
            
            # Registrar vista de página
            page_view = PageView(
                visitor_id=visitor_id,
                page_url=page_url[:500],
                page_title=page_title[:200],
                visit_date=datetime.utcnow(),
                session_id=session.get('session_id', 'unknown')[:100],
                referrer=request.referrer[:500] if request.referrer else None
            )
            self.session.add(page_view)
            
            self.session.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error tracking visit: {e}")
            self.session.rollback()
            return False
    
    def get_stats(self, days=30):
        """Obtiene estadísticas de visitantes"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Visitantes únicos totales
            total_unique = self.session.query(func.count(Visitor.id)).scalar() or 0
            
            # Visitantes únicos en período
            unique_period = self.session.query(func.count(Visitor.id)).filter(
                Visitor.last_visit >= cutoff_date
            ).scalar() or 0
            
            # Total de visitas (page views) en período
            total_visits = self.session.query(func.count(PageView.id)).filter(
                PageView.visit_date >= cutoff_date
            ).scalar() or 0
            
            # Visitantes recurrentes (más de 1 visita)
            recurring = self.session.query(func.count(Visitor.id)).filter(
                Visitor.total_visits > 1,
                Visitor.last_visit >= cutoff_date
            ).scalar() or 0
            
            # Visitantes nuevos en período
            new_visitors = self.session.query(func.count(Visitor.id)).filter(
                Visitor.first_visit >= cutoff_date
            ).scalar() or 0
            
            # Páginas más visitadas
            top_pages = self.session.query(
                PageView.page_url,
                func.count(PageView.id).label('visits')
            ).filter(
                PageView.visit_date >= cutoff_date
            ).group_by(PageView.page_url).order_by(
                func.count(PageView.id).desc()
            ).limit(10).all()
            
            # Visitas por día (últimos 7 días)
            daily_visits = []
            for i in range(7):
                day_start = datetime.utcnow().replace(hour=0, minute=0, second=0) - timedelta(days=i)
                day_end = day_start + timedelta(days=1)
                
                count = self.session.query(func.count(PageView.id)).filter(
                    PageView.visit_date >= day_start,
                    PageView.visit_date < day_end
                ).scalar() or 0
                
                daily_visits.append({
                    'date': day_start.strftime('%Y-%m-%d'),
                    'visits': count
                })
            
            daily_visits.reverse()
            
            return {
                'period_days': days,
                'total_unique_visitors': total_unique,
                'unique_visitors_period': unique_period,
                'total_visits_period': total_visits,
                'recurring_visitors': recurring,
                'new_visitors': new_visitors,
                'avg_visits_per_visitor': round(total_visits / unique_period, 2) if unique_period > 0 else 0,
                'top_pages': [{'url': url, 'visits': visits} for url, visits in top_pages],
                'daily_visits': daily_visits
            }
            
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return None
    
    def get_visitor_details(self):
        """Obtiene detalles de visitantes recientes"""
        try:
            visitors = self.session.query(Visitor).order_by(
                Visitor.last_visit.desc()
            ).limit(50).all()
            
            visitor_list = []
            for v in visitors:
                visitor_list.append({
                    'visitor_id': v.visitor_id[:8] + '...',  # ID corto para privacidad
                    'first_visit': v.first_visit.strftime('%Y-%m-%d %H:%M'),
                    'last_visit': v.last_visit.strftime('%Y-%m-%d %H:%M'),
                    'total_visits': v.total_visits,
                    'user_agent': v.user_agent[:100] if v.user_agent else 'Unknown'
                })
            
            return visitor_list
            
        except Exception as e:
            logger.error(f"Error getting visitor details: {e}")
            return []
    
    def get_realtime_stats(self):
        """Obtiene estadísticas en tiempo real (última hora)"""
        try:
            cutoff = datetime.utcnow() - timedelta(hours=1)
            
            active_visitors = self.session.query(func.count(func.distinct(PageView.visitor_id))).filter(
                PageView.visit_date >= cutoff
            ).scalar() or 0
            
            recent_views = self.session.query(func.count(PageView.id)).filter(
                PageView.visit_date >= cutoff
            ).scalar() or 0
            
            return {
                'active_visitors_1h': active_visitors,
                'page_views_1h': recent_views,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting realtime stats: {e}")
            return None

# Instancia global
_analytics_instance = None

def get_analytics():
    """Obtiene instancia de analytics"""
    global _analytics_instance
    if _analytics_instance is None:
        _analytics_instance = VisitorAnalytics()
    return _analytics_instance
