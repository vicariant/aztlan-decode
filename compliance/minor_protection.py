#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AZTLÁN DECODE - SISTEMA DE PROTECCIÓN DE MENORES
Cumplimiento con UK Online Safety Act, California AADC, COPPA, etc.
"""

from datetime import datetime, timedelta
from functools import wraps
import hashlib
import json
import re

class MinorProtectionSystem:
    """
    Sistema completo de protección de menores según regulaciones internacionales
    """
    
    # Configuración de edades según jurisdicción
    AGE_LIMITS = {
        'coppa': 13,        # USA Federal (COPPA)
        'uk': 18,           # UK Online Safety Act
        'california': 18,   # California AADC
        'gdpr': 16,         # EU GDPR (varía por país)
        'default': 18       # Más restrictivo
    }
    
    def __init__(self, jurisdiction='default'):
        self.jurisdiction = jurisdiction
        self.age_limit = self.AGE_LIMITS.get(jurisdiction, 18)
        self.protection_level = 'high'
    
    # ============================================
    # 1. EVALUACIÓN DE IMPACTO JUVENIL
    # ============================================
    
    def assess_youth_impact(self, feature_name, data_collected, risks):
        """
        Realizar evaluación de impacto juvenil para cada funcionalidad
        
        Args:
            feature_name: Nombre de la funcionalidad
            data_collected: Lista de datos que se recopilan
            risks: Diccionario con riesgos potenciales
        
        Returns:
            Reporte de evaluación con recomendaciones
        """
        assessment = {
            'feature': feature_name,
            'timestamp': datetime.now().isoformat(),
            'data_collected': data_collected,
            'risk_level': 'low',
            'risks_identified': [],
            'mitigations': [],
            'approved_for_minors': True
        }
        
        # Analizar riesgos
        high_risk_data = ['location', 'biometric', 'health', 'financial', 'contact_info']
        for data_type in data_collected:
            if data_type in high_risk_data:
                assessment['risk_level'] = 'high'
                assessment['risks_identified'].append(f'Recopila datos sensibles: {data_type}')
        
        # Evaluar riesgos de adicción
        if risks.get('addictive_patterns'):
            assessment['risks_identified'].append('Posible patrón de adicción')
            assessment['mitigations'].append('Implementar límites de tiempo de uso')
        
        # Evaluar riesgos de acoso
        if risks.get('social_interaction'):
            assessment['risks_identified'].append('Interacción social puede facilitar acoso')
            assessment['mitigations'].append('Implementar moderación y reportes')
        
        # Evaluar contenido inapropiado
        if risks.get('user_generated_content'):
            assessment['risks_identified'].append('Contenido generado por usuarios')
            assessment['mitigations'].append('Filtros de contenido apropiado para edad')
        
        # Determinar aprobación
        if assessment['risk_level'] == 'high' and not assessment['mitigations']:
            assessment['approved_for_minors'] = False
        
        return assessment
    
    # ============================================
    # 2. VERIFICACIÓN DE EDAD ROBUSTA
    # ============================================
    
    def verify_age(self, birth_date, method='date_input', verification_data=None):
        """
        Verificar edad con múltiples métodos
        
        Methods:
            - date_input: Fecha de nacimiento simple
            - document: Verificación con documento (ID, pasaporte)
            - biometric: Estimación por IA (facial)
            - behavioral: Análisis de comportamiento
            - third_party: Servicio de verificación externo
        """
        result = {
            'verified': False,
            'method': method,
            'age': None,
            'is_minor': None,
            'confidence': 0,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            birth = datetime.strptime(birth_date, '%Y-%m-%d')
            age = (datetime.now() - birth).days // 365
            
            result['age'] = age
            result['is_minor'] = age < self.age_limit
            
            # Diferentes niveles de confianza según método
            confidence_levels = {
                'date_input': 0.6,
                'document': 0.95,
                'biometric': 0.85,
                'behavioral': 0.7,
                'third_party': 0.99
            }
            
            result['confidence'] = confidence_levels.get(method, 0.5)
            
            # Validaciones adicionales
            if method == 'document' and verification_data:
                # Verificar que el documento sea válido
                result['verified'] = self._validate_document(verification_data)
            else:
                result['verified'] = True
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _validate_document(self, doc_data):
        """Validar documento de identidad (placeholder)"""
        # En producción, integrar con servicios como Onfido, Jumio, Veriff
        return doc_data.get('valid', False)
    
    # ============================================
    # 3. CONFIGURACIÓN DE ALTA PRIVACIDAD POR DEFECTO
    # ============================================
    
    def get_default_privacy_settings(self, is_minor=True):
        """
        Configuración de privacidad por defecto para menores
        Según UK Online Safety Act y California AADC
        """
        if is_minor:
            return {
                'profile_visibility': 'private',
                'location_tracking': False,
                'targeted_advertising': False,
                'profiling': False,
                'data_sharing': False,
                'social_features': 'restricted',
                'content_recommendations': 'age_appropriate',
                'video_audio_enabled': False,
                'contact_by_strangers': False,
                'public_posts': False,
                'search_visibility': False,
                'data_retention': 'minimal',
                'parental_monitoring': True,
                'time_limits': {'daily': 120, 'enabled': True},  # 2 horas
                'content_filters': ['violence', 'adult', 'drugs', 'weapons']
            }
        else:
            return {
                'profile_visibility': 'friends',
                'location_tracking': False,
                'targeted_advertising': 'opt_in',
                'profiling': 'opt_in',
                'data_sharing': 'opt_in',
                'social_features': 'enabled',
                'content_recommendations': 'personalized',
                'video_audio_enabled': True,
                'contact_by_strangers': 'opt_in',
                'public_posts': 'opt_in',
                'search_visibility': True,
                'data_retention': 'standard'
            }
    
    # ============================================
    # 4. LENGUAJE LEGAL CLARO Y COMPRENSIBLE
    # ============================================
    
    def get_child_friendly_terms(self, section):
        """
        Términos de servicio y avisos en lenguaje apropiado para menores
        """
        child_friendly_terms = {
            'data_collection': {
                'title': '📊 ¿Qué información guardamos?',
                'content': '''
                    Solo guardamos lo necesario para que la app funcione:
                    • Tu nombre de usuario (no tu nombre real)
                    • Tu equipo de robótica favorito
                    • Los robots que buscas
                    
                    ❌ NO guardamos: Tu ubicación, fotos, ni información personal
                '''
            },
            'privacy': {
                'title': '🔒 Tu privacidad está protegida',
                'content': '''
                    • Tu información es privada
                    • No la compartimos con nadie
                    • Tus padres pueden ver lo que haces
                    • Puedes borrar tu cuenta cuando quieras
                '''
            },
            'safety': {
                'title': '🛡️ Cómo te mantenemos seguro',
                'content': '''
                    • No hay chat con extraños
                    • Todo el contenido es apropiado para tu edad
                    • Si ves algo raro, repórtalo
                    • Tus padres reciben alertas de actividad
                '''
            },
            'parental_monitoring': {
                'title': '👨‍👩‍👧 Aviso: Tus padres pueden ver esto',
                'content': '''
                    🔔 Tus padres han activado el monitoreo parental.
                    Esto significa que pueden ver:
                    • Qué equipos buscas
                    • Cuánto tiempo usas la app
                    • Tu actividad general
                    
                    Esto es para mantenerte seguro 😊
                '''
            }
        }
        
        return child_friendly_terms.get(section, {})
    
    # ============================================
    # 5. MINIMIZACIÓN DE DATOS
    # ============================================
    
    def validate_data_collection(self, data_fields, purpose):
        """
        Validar que solo se recopilen datos estrictamente necesarios
        """
        # Datos necesarios según propósito
        necessary_data = {
            'scouting': ['team_number', 'user_id'],
            'analysis': ['team_number', 'match_data'],
            'favorites': ['team_number', 'user_id'],
            'export': ['team_number', 'analysis_data']
        }
        
        # Datos prohibidos para menores
        prohibited_for_minors = [
            'physical_address',
            'phone_number',
            'precise_location',
            'biometric_data',
            'health_data',
            'financial_data',
            'browsing_history',
            'device_identifiers'
        ]
        
        validation = {
            'approved': True,
            'necessary': [],
            'unnecessary': [],
            'prohibited': []
        }
        
        necessary = necessary_data.get(purpose, [])
        
        for field in data_fields:
            if field in necessary:
                validation['necessary'].append(field)
            elif field in prohibited_for_minors:
                validation['prohibited'].append(field)
                validation['approved'] = False
            else:
                validation['unnecessary'].append(field)
        
        return validation
    
    # ============================================
    # 6. USO RESPONSABLE DE ALGORITMOS E IA
    # ============================================
    
    def evaluate_algorithm_impact(self, algorithm_name, features, outcomes):
        """
        Evaluar si un algoritmo puede causar daño a menores
        Según California AADC
        """
        evaluation = {
            'algorithm': algorithm_name,
            'risk_level': 'low',
            'concerns': [],
            'recommendations': [],
            'approved_for_minors': True
        }
        
        # Detectar patrones de adicción
        addictive_features = ['infinite_scroll', 'auto_play', 'push_notifications', 'streaks']
        if any(f in features for f in addictive_features):
            evaluation['concerns'].append('Posible patrón de adicción')
            evaluation['recommendations'].append('Implementar límites de tiempo')
            evaluation['risk_level'] = 'medium'
        
        # Detectar amplificación de contenido dañino
        if 'content_recommendation' in features:
            evaluation['concerns'].append('Puede recomendar contenido inapropiado')
            evaluation['recommendations'].append('Filtros por edad obligatorios')
        
        # Detectar discriminación
        if any('demographic' in f for f in features):
            evaluation['concerns'].append('Riesgo de sesgo/discriminación')
            evaluation['recommendations'].append('Auditoría de equidad algorítmica')
        
        # Evaluar resultados negativos
        negative_outcomes = ['increased_screen_time', 'social_comparison', 'fomo']
        if any(o in outcomes for o in negative_outcomes):
            evaluation['risk_level'] = 'high'
            evaluation['approved_for_minors'] = False
        
        return evaluation
    
    # ============================================
    # 7. CONTROLES PARENTALES
    # ============================================
    
    def get_parental_controls(self):
        """
        Herramientas para control parental
        """
        return {
            'time_limits': {
                'enabled': True,
                'daily_limit_minutes': 120,
                'weekly_limit_minutes': 600,
                'quiet_hours': {'start': '22:00', 'end': '07:00'},
                'break_reminders': True
            },
            'content_filters': {
                'enabled': True,
                'block_categories': ['violence', 'adult', 'drugs'],
                'safe_search': True,
                'age_appropriate_only': True
            },
            'monitoring': {
                'activity_reports': 'weekly',
                'real_time_alerts': True,
                'notify_child_when_monitored': True,  # California requirement
                'view_search_history': True,
                'view_favorites': True
            },
            'restrictions': {
                'social_features': 'disabled',
                'external_links': 'blocked',
                'downloads': 'require_approval',
                'in_app_purchases': 'blocked'
            }
        }
    
    def notify_child_of_monitoring(self, child_user_id):
        """
        Notificar al menor que está siendo monitoreado
        Requerimiento de California
        """
        return {
            'notification_type': 'parental_monitoring',
            'title': '👨‍👩‍👧 Monitoreo Parental Activo',
            'message': '''
                Tus padres han activado el monitoreo de tu actividad.
                Ellos pueden ver:
                • Qué equipos buscas
                • Cuánto tiempo usas la app
                • Tu actividad general
                
                Esto es para mantenerte seguro. Si tienes dudas, habla con ellos.
            ''',
            'dismissible': False,
            'show_on_every_login': True
        }
    
    # ============================================
    # 8. MEDIDAS DE SEGURIDAD ROBUSTAS
    # ============================================
    
    def get_security_requirements(self):
        """
        Requisitos de seguridad para datos de menores
        """
        return {
            'encryption': {
                'at_rest': 'AES-256',
                'in_transit': 'TLS 1.3',
                'database': 'encrypted',
                'backups': 'encrypted'
            },
            'authentication': {
                'password_requirements': {
                    'min_length': 12,
                    'require_uppercase': True,
                    'require_lowercase': True,
                    'require_numbers': True,
                    'require_symbols': True
                },
                'two_factor': 'recommended',
                'session_timeout': 30  # minutos
            },
            'access_control': {
                'principle': 'least_privilege',
                'role_based': True,
                'audit_all_access': True
            },
            'auditing': {
                'log_all_minor_access': True,
                'retention_period': '7 years',
                'regular_reviews': 'quarterly',
                'breach_notification': '72 hours'
            },
            'vulnerability_management': {
                'regular_scans': 'weekly',
                'penetration_testing': 'quarterly',
                'dependency_updates': 'automatic',
                'security_patches': 'within_24h'
            }
        }
    
    def check_consent_requirements(self, user_age, user_location='US'):
        """
        Verificar requisitos de consentimiento según edad y ubicación
        """
        consent = {
            'required': False,
            'type': None,
            'who': None,
            'method': None
        }
        
        if user_age < 13:  # COPPA
            consent['required'] = True
            consent['type'] = 'parental_consent'
            consent['who'] = 'parent_or_guardian'
            consent['method'] = 'verifiable'  # Email, firma, llamada, etc.
        
        elif user_age < self.age_limit:
            if self.jurisdiction in ['uk', 'california']:
                consent['required'] = True
                consent['type'] = 'parental_awareness'
                consent['who'] = 'parent_or_guardian'
                consent['method'] = 'notification'
        
        return consent

# Instancia global
minor_protection = MinorProtectionSystem(jurisdiction='default')
