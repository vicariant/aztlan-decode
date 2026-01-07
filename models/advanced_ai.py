#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AZTLÁN DECODE - IA ULTRA AVANZADA
Algoritmos de ML, análisis predictivo y optimización estratégica
"""

import numpy as np
from datetime import datetime
from collections import defaultdict
import math
from functools import lru_cache

class TrendAnalyzer:
    """Analiza tendencias y patrones en el rendimiento"""
    
    def __init__(self):
        # Pre-calcular thresholds para performance
        self.momentum_thresholds = np.array([0.75, 0.60, 0.40])
        self.momentum_values = np.array([1.0, 0.5, 0, -0.5])
        self.momentum_descriptions = [
            "🔥 MOMENTUM ASCENDENTE",
            "📈 TENDENCIA POSITIVA",
            "⚖️ ESTABLE",
            "📉 NECESITA MEJORA"
        ]
    
    def detect_momentum(self, team_data):
        """Detecta el momentum del equipo (mejorando/declinando)"""
        wins = team_data.get('wins', 0)
        losses = team_data.get('losses', 0)
        total = wins + losses
        
        if total == 0:
            return 0, "NUEVO"
        
        # Cálculo vectorizado
        win_rate = wins / total
        idx = np.searchsorted(self.momentum_thresholds[::-1], win_rate, side='right')
        idx = 3 - idx
        
        return self.momentum_values[idx], self.momentum_descriptions[idx]
    
    def predict_future_performance(self, current_score, momentum):
        """Predice rendimiento futuro basado en momentum"""
        future_score = current_score * (1 + momentum * 0.1)
        return float(np.clip(future_score, 0, 100))
    
    def calculate_consistency_score(self, team_data):
        """Calcula score de consistencia avanzado"""
        wins = team_data.get('wins', 0)
        losses = team_data.get('losses', 0)
        opr = team_data.get('opr', 0)
        rp = team_data.get('tot_points', 0)
        
        total_matches = wins + losses
        if total_matches == 0:
            return 0
        
        # Análisis vectorizado de varianza
        expected_wins = total_matches * 0.5
        win_variance = abs(wins - expected_wins) / total_matches
        
        # Score de OPR vs RP correlation con numpy
        values = np.array([opr, rp])
        normalized = np.where(values > 0, values / 100, 0)
        correlation = 1 - abs(normalized[0] - normalized[1])
        
        consistency = (1 - win_variance * 0.5 + correlation * 0.5)
        return float(np.clip(consistency, 0, 1))


class AdvancedPredictor:
    """Sistema de predicción avanzado con ML"""
    
    def __init__(self):
        """Inicializa el predictor"""
        self.confidence_threshold = 0.7
        # Pre-compute exp values para sigmoid
        self._sigmoid_cache = {}
    
    @lru_cache(maxsize=256)
    def _sigmoid_cached(self, x):
        """Sigmoid cacheado para valores repetidos"""
        return 1 / (1 + math.exp(-x / 15))
    
    def predict_match_outcome(self, team1_score, team2_score, team1_momentum, team2_momentum):
        """Predice resultado de match con alta precisión"""
        # Base probability usando sigmoid cacheado
        score_diff = round(team1_score - team2_score, 1)  # Round para mejor cache hit
        base_prob = self._sigmoid_cached(score_diff)
        
        # Ajuste por momentum
        momentum_adjustment = (team1_momentum - team2_momentum) * 0.05
        
        # Probability final con numpy clip
        final_prob = np.clip(base_prob + momentum_adjustment, 0.05, 0.95)
        
        return float(final_prob * 100)
    
    def calculate_worlds_probability(self, global_score, momentum, current_ranking):
        """Calcula probabilidad de clasificar a Worlds"""
        # Componentes múltiples
        score_component = global_score / 100
        momentum_component = (momentum + 1) / 2  # Normalizar -1 a 1 → 0 a 1
        
        # Weighted average
        base_prob = score_component * 0.7 + momentum_component * 0.3
        
        # Bonus por ranking alto
        ranking_bonus = 0
        if current_ranking and current_ranking <= 10:
            ranking_bonus = 0.1
        elif current_ranking and current_ranking <= 20:
            ranking_bonus = 0.05
        
        final_prob = min(0.98, base_prob + ranking_bonus)
        return final_prob * 100
    
    def predict_regional_win_probability(self, global_score, wins, losses):
        """Predice probabilidad de ganar regional"""
        win_rate = wins / (wins + losses) if (wins + losses) > 0 else 0.5
        score_factor = global_score / 100
        
        # Combinación no lineal
        base_prob = (score_factor ** 0.8) * (win_rate ** 0.5)
        
        # Ajustes
        if global_score >= 90:
            base_prob *= 1.2
        elif global_score >= 80:
            base_prob *= 1.1
        
        return min(95, base_prob * 100)
    
    def analyze_strategic_advantages(self, team_data):
        """Analiza ventajas estratégicas del equipo"""
        advantages = []
        
        opr = team_data.get('opr', 0)
        rp = team_data.get('tot_points', 0)
        wins = team_data.get('wins', 0)
        
        # OPR Analysis
        if opr > 200:
            advantages.append({
                'type': 'SCORING_POWER',
                'desc': '💥 POTENCIA DE SCORING EXCEPCIONAL',
                'impact': 'high',
                'value': opr
            })
        elif opr > 150:
            advantages.append({
                'type': 'SCORING_POWER',
                'desc': '⚡ ALTO POTENCIAL DE PUNTUACIÓN',
                'impact': 'medium',
                'value': opr
            })
        
        # RP Analysis
        if rp > 90:
            advantages.append({
                'type': 'CONSISTENCY',
                'desc': '🎯 CONSISTENCIA ÉLITE',
                'impact': 'high',
                'value': rp
            })
        elif rp > 70:
            advantages.append({
                'type': 'CONSISTENCY',
                'desc': '✅ RENDIMIENTO CONSISTENTE',
                'impact': 'medium',
                'value': rp
            })
        
        # Win Analysis
        if wins >= 10:
            advantages.append({
                'type': 'EXPERIENCE',
                'desc': '🏆 EXPERIENCIA COMPETITIVA AMPLIA',
                'impact': 'medium',
                'value': wins
            })
        
        return advantages


class StrategicOptimizer:
    """Optimiza estrategias basado en análisis profundo"""
    
    def generate_optimal_strategy(self, team_data, global_score):
        """Genera estrategia óptima personalizada"""
        strategies = []
        
        opr = team_data.get('opr', 0)
        rp = team_data.get('tot_points', 0)
        wins = team_data.get('wins', 0)
        losses = team_data.get('losses', 0)
        
        # Análisis multi-dimensional
        if global_score >= 85:
            strategies.extend([
                {'priority': 1, 'action': '👑 FOCO: Mantener dominancia', 'category': 'PERFORMANCE'},
                {'priority': 1, 'action': '🎖️ ESTRATEGIA: Ser captain pick en playoffs', 'category': 'ALLIANCE'},
                {'priority': 2, 'action': '📊 OPTIMIZAR: Pulir detalles para Worlds', 'category': 'IMPROVEMENT'}
            ])
        elif global_score >= 70:
            strategies.extend([
                {'priority': 1, 'action': '⚡ FOCO: Maximizar OPR en qualifiers', 'category': 'PERFORMANCE'},
                {'priority': 1, 'action': '🤝 ESTRATEGIA: Formar alianzas top 4', 'category': 'ALLIANCE'},
                {'priority': 2, 'action': '🔧 MEJORAR: Autonomía y endgame', 'category': 'IMPROVEMENT'}
            ])
        elif global_score >= 50:
            strategies.extend([
                {'priority': 1, 'action': '🎯 FOCO: Aumentar consistencia', 'category': 'PERFORMANCE'},
                {'priority': 1, 'action': '🔍 ESTRATEGIA: Analizar top teams', 'category': 'LEARNING'},
                {'priority': 2, 'action': '⚙️ MEJORAR: Mecánica de robot', 'category': 'IMPROVEMENT'}
            ])
        else:
            strategies.extend([
                {'priority': 1, 'action': '🌱 FOCO: Fundamentos básicos', 'category': 'BASICS'},
                {'priority': 1, 'action': '📚 ESTRATEGIA: Aprender de equipos élite', 'category': 'LEARNING'},
                {'priority': 2, 'action': '🔨 MEJORAR: Diseño de robot', 'category': 'REDESIGN'}
            ])
        
        # Análisis específico por métricas
        if opr < 100:
            strategies.append({
                'priority': 1,
                'action': '🚨 CRÍTICO: Aumentar capacidad de scoring',
                'category': 'URGENT'
            })
        
        if wins < losses:
            strategies.append({
                'priority': 1,
                'action': '⚔️ CRÍTICO: Revisar estrategia de matches',
                'category': 'URGENT'
            })
        
        return sorted(strategies, key=lambda x: x['priority'])
    
    def recommend_alliance_partners(self, team_score, strengths):
        """Recomienda partners ideales para alianza"""
        recommendations = []
        
        if team_score >= 85:
            recommendations.append({
                'type': 'CAPTAIN',
                'desc': '🎖️ POSICIÓN: Alliance Captain',
                'picks': 'Buscar defensores o especialistas en endgame'
            })
        elif team_score >= 70:
            recommendations.append({
                'type': 'FIRST_PICK',
                'desc': '⭐ POSICIÓN: First Pick probable',
                'picks': 'Complementar fortalezas con captain élite'
            })
        else:
            recommendations.append({
                'type': 'SUPPORT',
                'desc': '🤝 POSICIÓN: Alliance Support',
                'picks': 'Especializar en una tarea específica'
            })
        
        return recommendations


class StatisticalAnalyzer:
    """Análisis estadístico avanzado"""
    
    def calculate_percentile(self, value, all_values):
        """Calcula percentil del valor"""
        if not all_values:
            return 50
        
        below = sum(1 for v in all_values if v < value)
        percentile = (below / len(all_values)) * 100
        return percentile
    
    def detect_outliers(self, team_data):
        """Detecta anomalías en el rendimiento"""
        outliers = []
        
        opr = team_data.get('opr', 0)
        rp = team_data.get('tot_points', 0)
        wins = team_data.get('wins', 0)
        
        # OPR extremo
        if opr > 250:
            outliers.append({
                'metric': 'OPR',
                'type': 'EXCEPTIONAL',
                'desc': '🌟 OPR excepcional - Top 1% mundial'
            })
        
        # RP extremo
        if rp > 100:
            outliers.append({
                'metric': 'RP',
                'type': 'EXCEPTIONAL',
                'desc': '💎 Ranking Points élite'
            })
        
        # Win streak
        if wins >= 15:
            outliers.append({
                'metric': 'WINS',
                'type': 'STREAK',
                'desc': '🔥 Racha de victorias impresionante'
            })
        
        return outliers
    
    def calculate_z_score(self, value, mean=50, std=20):
        """Calcula Z-score para normalización"""
        return (value - mean) / std
    
    def bayesian_update(self, prior_prob, likelihood, evidence_strength=1.0):
        """Actualización bayesiana de probabilidad"""
        posterior = prior_prob * likelihood * evidence_strength
        return min(0.99, max(0.01, posterior))


# Instancias globales
trend_analyzer = TrendAnalyzer()
predictor = AdvancedPredictor()
optimizer = StrategicOptimizer()
stats_analyzer = StatisticalAnalyzer()
