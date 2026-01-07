#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AZTLÁN DECODE - IA AVANZADA DE ANÁLISIS FTC
Sistema de análisis con algoritmos de Machine Learning y estadística avanzada
OPTIMIZADO PARA MÁXIMO RENDIMIENTO
"""

import numpy as np
import joblib
import os
from datetime import datetime
from collections import defaultdict
from functools import lru_cache, wraps
import hashlib

# Importar módulos avanzados
try:
    from models.advanced_ai import TrendAnalyzer, AdvancedPredictor, StrategicOptimizer, StatisticalAnalyzer
except ImportError:
    # Fallback si no se puede importar
    class TrendAnalyzer:
        def detect_momentum(self, team_data):
            return 0, "ESTABLE"
        def predict_future_performance(self, score, momentum):
            return score
        def calculate_consistency_score(self, team_data):
            return 0.5
    
    class AdvancedPredictor:
        def predict_match_outcome(self, s1, s2, m1, m2):
            return 50
        def calculate_worlds_probability(self, score, momentum, ranking):
            return score * 0.8
        def predict_regional_win_probability(self, score, wins, losses):
            return score * 0.6
        def analyze_strategic_advantages(self, team_data):
            return []
    
    class StrategicOptimizer:
        def generate_optimal_strategy(self, team_data, score):
            return []
        def recommend_alliance_partners(self, score, strengths):
            return []
    
    class StatisticalAnalyzer:
        def detect_outliers(self, team_data):
            return []

class FTCAnalyzer:
    """Analizador avanzado de equipos FTC con IA de última generación"""
    
    def __init__(self):
        """Inicializa el analizador FTC con modelos avanzados"""
        self.model_loaded = False
        
        # Cache de análisis para equipos frecuentes
        self._analysis_cache = {}
        self._cache_max_size = 100
        
        # Sistema de categorías mejorado con más granularidad
        self.categories = {
            'legendary': {'min': 95, 'desc': '🏆 LEYENDA MUNDIAL', 'emoji': '👑'},
            'elite': {'min': 85, 'desc': '⭐ ÉLITE GLOBAL', 'emoji': '💎'},
            'excelente': {'min': 75, 'desc': '🔥 EXCELENTE', 'emoji': '🚀'},
            'muy_bueno': {'min': 65, 'desc': '⚡ MUY BUENO', 'emoji': '💪'},
            'bueno': {'min': 50, 'desc': '✅ BUENO', 'emoji': '👍'},
            'competitivo': {'min': 35, 'desc': '📈 COMPETITIVO', 'emoji': '⚙️'},
            'promedio': {'min': 20, 'desc': '📊 PROMEDIO', 'emoji': '📉'},
            'desarrollo': {'min': 0, 'desc': '🌱 EN DESARROLLO', 'emoji': '🔧'}
        }
        
        # Pesos dinámicos para diferentes métricas
        self.metric_weights = {
            'ranking_points': 0.35,
            'win_rate': 0.25,
            'opr': 0.25,
            'consistency': 0.10,
            'worlds_bonus': 0.05
        }
        
        # Sistema de detección de tendencias
        self.trend_analyzer = TrendAnalyzer()
        
        # Sistema de predicción avanzado
        self.predictor = AdvancedPredictor()
        
        # Optimizador estratégico
        self.optimizer = StrategicOptimizer()
        
        # Analizador estadístico
        self.stats_analyzer = StatisticalAnalyzer()
    
    def _get_cache_key(self, team_data):
        """Genera key de cache basada en datos del equipo"""
        key_str = f"{team_data.get('team_number', 0)}_{team_data.get('wins', 0)}_{team_data.get('losses', 0)}_{team_data.get('tot_points', 0)}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _clear_cache_if_needed(self):
        """Limpia cache si excede tamaño máximo"""
        if len(self._analysis_cache) > self._cache_max_size:
            # Eliminar 20% más viejos
            to_remove = len(self._analysis_cache) // 5
            for _ in range(to_remove):
                self._analysis_cache.pop(next(iter(self._analysis_cache)))
    
    def analyze_team_performance(self, team_data):
        """
        Analiza el rendimiento con ALGORITMOS AVANZADOS + CACHE
        
        Args:
            team_data: Diccionario con datos del equipo
            
        Returns:
            dict: Análisis ultra completo del equipo
        """
        # Check cache primero
        cache_key = self._get_cache_key(team_data)
        if cache_key in self._analysis_cache:
            return self._analysis_cache[cache_key].copy()
        
        try:
            # Extraer métricas clave con numpy para velocidad
            # FIXED: Leer ranking_points correctamente de múltiples fuentes
            ranking_points = (
                team_data.get('ranking_points', 0) or 
                team_data.get('tot_points', 0) or 
                team_data.get('rp', 0) or 0
            )
            
            metrics = np.array([
                ranking_points,
                team_data.get('wins', 0) or 0,
                team_data.get('losses', 0) or 0,
                team_data.get('ties', 0) or 0,
                team_data.get('opr', 0) or team_data.get('highest_score', 0) or 0
            ], dtype=np.float32)
            
            ranking_points, wins, losses, ties, high_score = metrics
            
            # Calcular puntuación global MEJORADA
            global_score = self._calculate_advanced_score(
                ranking_points, wins, losses, ties, high_score, team_data
            )
            
            # Detectar MOMENTUM (nuevo)
            momentum, momentum_desc = self.trend_analyzer.detect_momentum(team_data)
            
            # Score de consistencia AVANZADO
            consistency_score = self.trend_analyzer.calculate_consistency_score(team_data)
            
            # Predicción de rendimiento FUTURO
            future_score = self.trend_analyzer.predict_future_performance(global_score, momentum)
            
            # Clasificar al equipo
            category = self._classify_team(global_score)
            cat_emoji = self._get_category_emoji(global_score)
            
            # Analizar fortalezas y debilidades MEJORADO
            strengths, weaknesses = self._analyze_strengths_weaknesses_advanced(team_data, global_score)
            
            # Detección de outliers/anomalías
            outliers = self.stats_analyzer.detect_outliers(team_data)
            
            # Ventajas estratégicas AVANZADAS
            strategic_advantages = self.predictor.analyze_strategic_advantages(team_data)
            
            # Generar predicción ULTRA PRECISA
            prediction = self._predict_performance_advanced(
                team_data, global_score, momentum, consistency_score
            )
            
            # Análisis estratégico PERSONALIZADO
            strategy = self.optimizer.generate_optimal_strategy(team_data, global_score)
            
            # Recomendaciones de alianza
            alliance_recs = self.optimizer.recommend_alliance_partners(global_score, strengths)
            
            result = {
                'global_score': round(global_score, 2),
                'future_score': round(future_score, 2),
                'momentum': momentum,
                'momentum_desc': momentum_desc,
                'category': category,
                'category_emoji': cat_emoji,
                'strengths': strengths,
                'weaknesses': weaknesses,
                'outliers': outliers,
                'strategic_advantages': strategic_advantages,
                'prediction': prediction,
                'strategy': strategy,
                'alliance_recommendations': alliance_recs,
                'metrics': {
                    'ranking_points': int(ranking_points),
                    'win_rate': self._calculate_win_rate(int(wins), int(losses), int(ties)),
                    'consistency': round(consistency_score, 3),
                    'peak_performance': int(high_score),
                    'momentum_factor': momentum
                }
            }
            
            # Guardar en cache
            self._clear_cache_if_needed()
            self._analysis_cache[cache_key] = result.copy()
            
            return result
            
        except Exception as e:
            return {
                'error': f'Error en análisis: {str(e)}',
                'global_score': 0,
                'category': 'DATOS INSUFICIENTES'
            }
    
    def compare_teams(self, team1_data, team2_data):
        """
        Compara dos equipos FTC con ANÁLISIS ULTRA AVANZADO
        
        Args:
            team1_data: Datos del primer equipo
            team2_data: Datos del segundo equipo
            
        Returns:
            dict: Comparación súper detallada
        """
        try:
            # Analizar ambos equipos con IA avanzada
            analysis1 = self.analyze_team_performance(team1_data)
            analysis2 = self.analyze_team_performance(team2_data)
            
            # Determinar ventajas AVANZADAS
            advantages_team1 = []
            advantages_team2 = []
            
            # Comparar puntuación global
            score_diff = analysis1['global_score'] - analysis2['global_score']
            if abs(score_diff) > 5:
                if score_diff > 0:
                    advantages_team1.append(f"💪 Puntuación superior (+{score_diff:.1f} puntos)")
                else:
                    advantages_team2.append(f"💪 Puntuación superior (+{abs(score_diff):.1f} puntos)")
            
            # Comparar MOMENTUM (nuevo)
            momentum1 = analysis1.get('momentum', 0)
            momentum2 = analysis2.get('momentum', 0)
            if momentum1 > momentum2 + 0.2:
                advantages_team1.append(f"🔥 {analysis1.get('momentum_desc', 'Mejor momentum')}")
            elif momentum2 > momentum1 + 0.2:
                advantages_team2.append(f"🔥 {analysis2.get('momentum_desc', 'Mejor momentum')}")
            
            # Comparar métricas
            if analysis1['metrics']['win_rate'] > analysis2['metrics']['win_rate']:
                diff = (analysis1['metrics']['win_rate'] - analysis2['metrics']['win_rate']) * 100
                advantages_team1.append(f"🏆 Mayor win rate (+{diff:.1f}%)")
            elif analysis2['metrics']['win_rate'] > analysis1['metrics']['win_rate']:
                diff = (analysis2['metrics']['win_rate'] - analysis1['metrics']['win_rate']) * 100
                advantages_team2.append(f"🏆 Mayor win rate (+{diff:.1f}%)")
            
            # Comparar consistencia
            cons1 = analysis1['metrics']['consistency']
            cons2 = analysis2['metrics']['consistency']
            if cons1 > cons2 + 0.1:
                advantages_team1.append(f"✅ Más consistente ({cons1:.1%})")
            elif cons2 > cons1 + 0.1:
                advantages_team2.append(f"✅ Más consistente ({cons2:.1%})")
            
            # Predicción de enfrentamiento con IA AVANZADA
            win_probability = self.predictor.predict_match_outcome(
                analysis1['global_score'],
                analysis2['global_score'],
                momentum1,
                momentum2
            )
            
            # Análisis de ventajas estratégicas
            strategic_analysis = self._compare_strategic_advantages(analysis1, analysis2)
            
            return {
                'team1': {
                    'score': analysis1['global_score'],
                    'future_score': analysis1.get('future_score', analysis1['global_score']),
                    'momentum': momentum1,
                    'momentum_desc': analysis1.get('momentum_desc', 'N/A'),
                    'category': analysis1['category'],
                    'emoji': analysis1.get('category_emoji', ''),
                    'advantages': advantages_team1,
                    'strategic_advantages': analysis1.get('strategic_advantages', []),
                    'win_probability': win_probability
                },
                'team2': {
                    'score': analysis2['global_score'],
                    'future_score': analysis2.get('future_score', analysis2['global_score']),
                    'momentum': momentum2,
                    'momentum_desc': analysis2.get('momentum_desc', 'N/A'),
                    'category': analysis2['category'],
                    'emoji': analysis2.get('category_emoji', ''),
                    'advantages': advantages_team2,
                    'strategic_advantages': analysis2.get('strategic_advantages', []),
                    'win_probability': 100 - win_probability
                },
                'verdict': self._generate_comparison_verdict(analysis1, analysis2, win_probability),
                'recommendation': self._generate_matchup_recommendation(analysis1, analysis2),
                'strategic_analysis': strategic_analysis,
                'confidence_level': self._calculate_prediction_confidence(analysis1, analysis2)
            }
            
        except Exception as e:
            return {
                'error': f'Error en comparación: {str(e)}'
            }
    
    def _calculate_advanced_score(self, rp, wins, losses, ties, high_score, team_data):
        """Calcula score global con algoritmo avanzado VECTORIZADO"""
        total_matches = wins + losses + ties
        
        if total_matches == 0:
            return 0
        
        # Cálculo vectorizado con numpy
        components = np.array([
            ((wins * 3 + ties * 1) / total_matches) * 25,  # Win component
            min((rp / 8), 35),  # RP component
            min((high_score / 4), 30),  # Performance component
            min((wins / total_matches) * 10, 10),  # Consistency
            5 if team_data.get('worlds_qualified') else 0,  # Worlds bonus
            -5 if losses > wins * 1.5 else 0  # Loss penalty
        ])
        
        total = float(np.sum(components))
        return float(np.clip(total, 0, 100))
        """Calcula puntuación global AVANZADA con algoritmos mejorados"""
        total_matches = wins + losses + ties
        if total_matches == 0:
            total_matches = 1
        
        # Componentes MEJORADOS con pesos dinámicos
        win_component = ((wins * 3 + ties * 1) / total_matches) * 25  # Increased weight
        rp_component = min((rp / 8), 35)  # More aggressive scaling
        performance_component = min((high_score / 4), 30)  # Better scaling
        consistency_component = min((wins / total_matches) * 10, 10)
        
        # BONUS por calificación a Worlds
        worlds_bonus = 5 if team_data.get('worlds_qualified') else 0
        
        # PENALTY por muchas derrotas
        loss_penalty = 0
        if losses > wins * 1.5:
            loss_penalty = -5
        
        total = win_component + rp_component + performance_component + consistency_component + worlds_bonus + loss_penalty
        
        return max(0, min(100, total))
    
    def _calculate_global_score(self, rp, wins, losses, ties, high_score):
        """Método legacy - mantener para compatibilidad"""
        total_matches = wins + losses + ties
        if total_matches == 0:
            total_matches = 1
        
        # Componentes de la puntuación
        win_component = (wins * 3 + ties * 1) / total_matches * 20
        rp_component = min(rp / 10, 40)  # Máximo 40 puntos
        performance_component = min(high_score / 5, 30)  # Máximo 30 puntos
        consistency_component = min((wins / total_matches) * 10, 10)  # Máximo 10 puntos
        
        return win_component + rp_component + performance_component + consistency_component
    
    def _classify_team(self, score):
        """Clasifica al equipo según su puntuación MEJORADA"""
        for category, info in self.categories.items():
            if score >= info['min']:
                return info['desc']
        return '❓ SIN CLASIFICACIÓN'
    
    def _get_category_emoji(self, score):
        """Obtiene emoji de la categoría"""
        for category, info in self.categories.items():
            if score >= info['min']:
                return info.get('emoji', '📊')
        return '❓'
    
    def _analyze_strengths_weaknesses_advanced(self, team_data, global_score):
        """Análisis AVANZADO de fortalezas y debilidades"""
        strengths = []
        weaknesses = []
        
        rp = team_data.get('tot_points', 0) or 0
        wins = team_data.get('wins', 0) or 0
        losses = team_data.get('losses', 0) or 0
        opr = team_data.get('opr', 0) or 0
        
        # Análisis MULTI-NIVEL de RP
        if rp >= 95:
            strengths.append("👑 RANKING POINTS LEGENDARIOS - Top 1%")
        elif rp >= 85:
            strengths.append("💎 Ranking Points élite mundial")
        elif rp >= 70:
            strengths.append("⭐ Ranking Points excelentes")
        elif rp >= 50:
            strengths.append("✅ Ranking Points sólidos")
        elif rp < 25:
            weaknesses.append("⚠️ Ranking Points muy bajos")
        
        # Análisis de RÉCORD mejorado
        total = wins + losses
        if total > 0:
            win_rate = wins / total
            if win_rate >= 0.85:
                strengths.append("🔥 DOMINIO ABSOLUTO - Win rate excepcional")
            elif win_rate >= 0.70:
                strengths.append("🏆 Win rate élite")
            elif win_rate >= 0.55:
                strengths.append("💪 Win rate competitivo")
            elif win_rate < 0.35:
                weaknesses.append("📉 Win rate bajo - Necesita mejorar estrategia")
        
        # Análisis PROFUNDO de OPR
        if opr >= 250:
            strengths.append("💥 OPR EXCEPCIONAL - Potencia de scoring brutal")
        elif opr >= 200:
            strengths.append("🚀 OPR muy alto - Top tier scoring")
        elif opr >= 150:
            strengths.append("⚡ OPR sólido - Buen scoring")
        elif opr < 80:
            weaknesses.append("🔧 OPR bajo - Mejorar capacidad de scoring")
        
        # Análisis de calificación
        if team_data.get('worlds_qualified'):
            strengths.append("🌍 ⭐ CLASIFICADO A CAMPEONATO MUNDIAL ⭐")
        
        # Análisis de NIVEL GLOBAL
        if global_score >= 90:
            strengths.append("👑 NIVEL LEGENDARIO - Candidato a campeón")
        elif global_score >= 80:
            strengths.append("💎 NIVEL ÉLITE - Alliance captain material")
        
        return strengths if strengths else ["📊 Rendimiento estándar"], weaknesses
    
    def _predict_performance_advanced(self, team_data, global_score, momentum, consistency):
        """Predicción AVANZADA con múltiples factores"""
        wins = team_data.get('wins', 0) or 0
        losses = team_data.get('losses', 0) or 0
        
        # Probabilidad de Worlds con IA avanzada
        worlds_prob = self.predictor.calculate_worlds_probability(
            global_score,
            momentum,
            team_data.get('ranking', None)
        )
        
        # Probabilidad de ganar regional
        regional_win_prob = self.predictor.predict_regional_win_probability(
            global_score, wins, losses
        )
        
        # Outlook mejorado
        if global_score >= 90:
            outlook = "🌟 EXCEPCIONAL - Candidato serio a campeón"
        elif global_score >= 80:
            outlook = "🔥 EXCELENTE - Top tier competitivo"
        elif global_score >= 70:
            outlook = "⚡ MUY BUENO - Sólido contendiente"
        elif global_score >= 60:
            outlook = "✅ BUENO - Competitivo con potencial"
        elif global_score >= 50:
            outlook = "📈 PROMEDIO+ - Margen de mejora"
        else:
            outlook = "🌱 EN DESARROLLO - Construyendo bases"
        
        return {
            'outlook': outlook,
            'probability_worlds': round(worlds_prob, 1),
            'probability_regional_win': round(regional_win_prob, 1),
            'momentum_impact': momentum,
            'consistency_rating': f"{consistency:.1%}",
            'recommendation': self._get_performance_recommendation(global_score, momentum)
        }
    
    def _get_performance_recommendation(self, score, momentum):
        """Genera recomendación basada en score y momentum"""
        if score >= 85 and momentum > 0:
            return "🏆 Mantener el nivel élite y prepararse para Worlds"
        elif score >= 85 and momentum < 0:
            return "⚠️ Recuperar momentum - Revisar estrategia reciente"
        elif score >= 70:
            return "⚡ Pulir detalles para alcanzar nivel élite"
        elif score >= 55:
            return "📈 Enfocarse en consistencia y optimización"
        else:
            return "🔧 Trabajar fundamentos y mejorar diseño"
    
    def _compare_strategic_advantages(self, analysis1, analysis2):
        """Compara ventajas estratégicas entre equipos"""
        comparison = {
            'overall': '',
            'key_factors': []
        }
        
        adv1 = len(analysis1.get('strategic_advantages', []))
        adv2 = len(analysis2.get('strategic_advantages', []))
        
        if adv1 > adv2:
            comparison['overall'] = f"Equipo 1 tiene {adv1} ventajas estratégicas vs {adv2}"
        elif adv2 > adv1:
            comparison['overall'] = f"Equipo 2 tiene {adv2} ventajas estratégicas vs {adv1}"
        else:
            comparison['overall'] = "Ventajas estratégicas equilibradas"
        
        return comparison
    
    def _calculate_prediction_confidence(self, analysis1, analysis2):
        """Calcula nivel de confianza en la predicción"""
        score_diff = abs(analysis1['global_score'] - analysis2['global_score'])
        
        if score_diff >= 20:
            return {'level': 'ALTA', 'percentage': 95, 'desc': '✅ Predicción muy confiable'}
        elif score_diff >= 10:
            return {'level': 'MEDIA-ALTA', 'percentage': 80, 'desc': '⚡ Predicción confiable'}
        elif score_diff >= 5:
            return {'level': 'MEDIA', 'percentage': 65, 'desc': '📊 Predicción moderada'}
        else:
            return {'level': 'BAJA', 'percentage': 50, 'desc': '⚖️ Match muy parejo'}
    
    def _calculate_win_rate(self, wins, losses, ties):
        """Calcula ratio de victorias"""
        total = wins + losses + ties
        if total == 0:
            return 0
        return (wins + ties * 0.5) / total
    
    def _calculate_consistency(self, team_data):
        """Calcula consistencia del equipo"""
        # Basado en desviación de puntuaciones
        high_score = team_data.get('opr', 0) or 0
        avg_points = team_data.get('tot_points', 0) / max(team_data.get('wins', 1) + team_data.get('losses', 1), 1)
        
        if high_score == 0:
            return 0
        
        variance = abs(high_score - avg_points) / high_score
        return max(0, 1 - variance)
    
    def _analyze_strengths_weaknesses(self, team_data):
        """Analiza fortalezas y debilidades"""
        strengths = []
        weaknesses = []
        
        # Análisis de ranking points
        rp = team_data.get('tot_points', 0) or 0
        if rp > 80:
            strengths.append("⭐ Ranking Points excepcionales")
        elif rp < 30:
            weaknesses.append("⚠️ Pocos Ranking Points acumulados")
        
        # Análisis de victorias
        wins = team_data.get('wins', 0) or 0
        losses = team_data.get('losses', 0) or 0
        if wins > losses * 2:
            strengths.append("🏆 Excelente ratio victoria/derrota")
        elif losses > wins * 2:
            weaknesses.append("⚠️ Más derrotas que victorias")
        
        # Análisis de desempeño
        high_score = team_data.get('opr', 0) or 0
        if high_score > 200:
            strengths.append("🚀 Puntuaciones muy altas")
        elif high_score < 50:
            weaknesses.append("⚠️ Puntuaciones bajas")
        
        # Análisis de calificación a Worlds
        if team_data.get('worlds_qualified'):
            strengths.append("🌍 CLASIFICADO A CAMPEONATO MUNDIAL")
        
        return strengths if strengths else ["📊 Rendimiento estándar"], weaknesses
    
    def _predict_performance(self, team_data, global_score):
        """Predice rendimiento futuro"""
        if global_score >= 85:
            return {
                'outlook': 'EXCELENTE',
                'probability_worlds': 95,
                'probability_regional_win': 75,
                'recommendation': 'Equipo de élite con alta probabilidad de éxito'
            }
        elif global_score >= 70:
            return {
                'outlook': 'MUY POSITIVO',
                'probability_worlds': 70,
                'probability_regional_win': 50,
                'recommendation': 'Equipo sólido con buenas posibilidades'
            }
        elif global_score >= 55:
            return {
                'outlook': 'POSITIVO',
                'probability_worlds': 40,
                'probability_regional_win': 30,
                'recommendation': 'Equipo competitivo con potencial de mejora'
            }
        else:
            return {
                'outlook': 'EN DESARROLLO',
                'probability_worlds': 15,
                'probability_regional_win': 10,
                'recommendation': 'Enfocarse en mejorar fundamentos'
            }
    
    def _generate_strategy(self, team_data, global_score):
        """Genera recomendaciones estratégicas"""
        strategies = []
        
        # Basado en puntuación
        if global_score < 50:
            strategies.append("🎯 Prioridad: Mejorar consistencia en puntuación")
            strategies.append("🔧 Optimizar robot para tareas de alto valor")
        else:
            strategies.append("⚡ Mantener nivel actual y pulir detalles")
            strategies.append("🎖️ Enfocarse en estrategia de playoffs")
        
        # Basado en victorias
        wins = team_data.get('wins', 0) or 0
        losses = team_data.get('losses', 0) or 0
        if losses > wins:
            strategies.append("🤝 Mejorar selección de alianzas")
            strategies.append("📋 Revisar estrategia de matches")
        
        # Basado en OPR
        opr = team_data.get('opr', 0) or 0
        if opr > 150:
            strategies.append("🏆 Potencial pick #1 en playoffs")
        
        return strategies
    
    def _calculate_matchup_probability(self, analysis1, analysis2):
        """Calcula probabilidad de victoria en enfrentamiento"""
        score1 = analysis1['global_score']
        score2 = analysis2['global_score']
        
        diff = score1 - score2
        
        # Función sigmoide para probabilidad
        probability = 50 + (diff * 2)  # Cada punto de diferencia = 2% probabilidad
        
        return max(10, min(90, probability))  # Entre 10% y 90%
    
    def _generate_comparison_verdict(self, analysis1, analysis2, win_prob):
        """Genera veredicto de comparación"""
        if win_prob >= 70:
            return "⚔️ VICTORIA PROBABLE para Equipo 1 - Ventaja significativa"
        elif win_prob >= 55:
            return "🎯 LIGERA VENTAJA para Equipo 1 - Match competitivo"
        elif win_prob >= 45:
            return "⚖️ MATCH PAREJO - Cualquiera puede ganar"
        elif win_prob >= 30:
            return "🎯 LIGERA VENTAJA para Equipo 2 - Match competitivo"
        else:
            return "⚔️ VICTORIA PROBABLE para Equipo 2 - Ventaja significativa"
    
    def _generate_matchup_recommendation(self, analysis1, analysis2):
        """Genera recomendación para el enfrentamiento"""
        recommendations = []
        
        # Comparar fortalezas
        if len(analysis1['strengths']) > len(analysis2['strengths']):
            recommendations.append("Equipo 1 tiene más fortalezas identificadas")
        elif len(analysis2['strengths']) > len(analysis1['strengths']):
            recommendations.append("Equipo 2 tiene más fortalezas identificadas")
        
        # Comparar categorías
        if analysis1['category'] != analysis2['category']:
            recommendations.append(f"Diferencia de nivel: {analysis1['category']} vs {analysis2['category']}")
        
        # Recomendación general
        recommendations.append("🎲 En FTC, la estrategia y ejecución pueden superar diferencias estadísticas")
        
        return recommendations

# Instancia global
ftc_analyzer = FTCAnalyzer()
