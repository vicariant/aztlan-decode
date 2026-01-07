#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EL ORÁCULO - SIMULADOR DE PARTIDOS FTC
=====================================
Predice resultados de matches usando OPR/EPA del sistema TRIDENTE
"""

import os
from typing import Dict, List, Optional, Tuple
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class MatchOracle:
    """Simulador de partidos con predicción de victoria usando TRIDENTE"""
    
    def __init__(self, trident_handler):
        """
        Inicializa el oráculo con acceso al sistema TRIDENTE
        
        Args:
            trident_handler: Instancia de TridentHandler para obtener datos
        """
        self.trident = trident_handler
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.client = None
        
        if self.groq_api_key:
            try:
                self.client = Groq(api_key=self.groq_api_key)
            except Exception as e:
                print(f"⚠️ Error inicializando Groq: {e}")
    
    def simulate_match(self, red_alliance: List[int], blue_alliance: List[int]) -> Dict:
        """
        Simula un match entre dos alianzas
        
        Args:
            red_alliance: Lista de 2 números de equipos (alianza roja)
            blue_alliance: Lista de 2 números de equipos (alianza azul)
            
        Returns:
            Dict con predicción, probabilidades, scores estimados y análisis IA
        """
        try:
            # Obtener datos de todos los equipos
            red_teams_data = [self._get_team_stats(team) for team in red_alliance]
            blue_teams_data = [self._get_team_stats(team) for team in blue_alliance]
            
            # Calcular poder ofensivo combinado (OPR/EPA)
            red_total_opr = sum(team['opr_numeric'] for team in red_teams_data)
            blue_total_opr = sum(team['opr_numeric'] for team in blue_teams_data)
            
            # Calcular factores adicionales (win rate, experiencia)
            red_avg_winrate = sum(team['win_rate'] for team in red_teams_data) / len(red_teams_data)
            blue_avg_winrate = sum(team['win_rate'] for team in blue_teams_data) / len(blue_teams_data)
            
            # Calcular score estimado con factor de win rate
            red_estimated_score = int(red_total_opr * 1.5 * (1 + red_avg_winrate / 200))
            blue_estimated_score = int(blue_total_opr * 1.5 * (1 + blue_avg_winrate / 200))
            
            # CÁLCULO MEJORADO DE PROBABILIDADES
            # Factor 1: Diferencia de OPR (70% peso)
            opr_differential = red_total_opr - blue_total_opr
            
            # Factor 2: Diferencia de Win Rate (20% peso)
            winrate_differential = red_avg_winrate - blue_avg_winrate
            
            # Factor 3: Consistencia de equipo (10% peso)
            red_consistency = min([t['win_rate'] for t in red_teams_data]) / max([t['win_rate'] for t in red_teams_data] + [1])
            blue_consistency = min([t['win_rate'] for t in blue_teams_data]) / max([t['win_rate'] for t in blue_teams_data] + [1])
            consistency_diff = (red_consistency - blue_consistency) * 100
            
            # Combinar factores con pesos
            import math
            combined_diff = (opr_differential * 0.7) + (winrate_differential * 0.2) + (consistency_diff * 0.1)
            
            # Función logística mejorada (más sensible a diferencias)
            red_win_probability = 50 + (combined_diff / (abs(combined_diff) + 20)) * 50
            red_win_probability = max(10, min(90, red_win_probability))  # Limitar entre 10-90%
            blue_win_probability = 100 - red_win_probability
            
            # Determinar ganador predicho
            predicted_winner = 'red' if red_win_probability > 50 else 'blue'
            
            # Generar análisis con IA
            ai_analysis = self._generate_ai_analysis(
                red_alliance, blue_alliance,
                red_teams_data, blue_teams_data,
                red_estimated_score, blue_estimated_score,
                red_win_probability, blue_win_probability
            )
            
            # Calcular nivel de confianza basado en diferencia combinada
            confidence_score = abs(combined_diff)
            confidence = 'Muy Alta' if confidence_score > 30 else 'Alta' if confidence_score > 15 else 'Media' if confidence_score > 7 else 'Baja'
            
            return {
                'success': True,
                'prediction': {
                    'winner': predicted_winner,
                    'red_win_probability': round(red_win_probability, 1),
                    'blue_win_probability': round(blue_win_probability, 1),
                    'red_estimated_score': red_estimated_score,
                    'blue_estimated_score': blue_estimated_score,
                    'confidence': confidence
                },
                'red_alliance': {
                    'teams': red_alliance,
                    'total_opr': round(red_total_opr, 2),
                    'avg_winrate': round(red_avg_winrate, 1),
                    'teams_data': red_teams_data
                },
                'blue_alliance': {
                    'teams': blue_alliance,
                    'total_opr': round(blue_total_opr, 2),
                    'avg_winrate': round(blue_avg_winrate, 1),
                    'teams_data': blue_teams_data
                },
                'ai_analysis': ai_analysis,
                'factors': self._calculate_match_factors(red_teams_data, blue_teams_data)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error simulando match: {str(e)}'
            }
    
    def _get_team_stats(self, team_number: int) -> Dict:
        """Obtiene estadísticas de un equipo desde TRIDENTE"""
        try:
            # Usar TRIDENTE para obtener datos validados
            report = self.trident.get_validated_report(team_number)
            
            # Extraer OPR (convertir a numérico)
            opr_str = report.get('stats', {}).get('opr', '0')
            opr_numeric = self._parse_opr(opr_str)
            
            # Extraer récord
            record_str = report.get('stats', {}).get('record', '0-0-0')
            wins, losses, ties = self._parse_record(record_str)
            win_rate = (wins / max(wins + losses + ties, 1)) * 100
            
            # Extraer ranking
            ranking = report.get('stats', {}).get('ranking', 'N/A')
            
            return {
                'team_number': team_number,
                'team_name': report.get('identity', {}).get('team_name', f'Team {team_number}'),
                'opr_numeric': opr_numeric,
                'opr_display': opr_str,
                'record': record_str,
                'wins': wins,
                'losses': losses,
                'win_rate': round(win_rate, 1),
                'ranking': ranking,
                'trust_level': report.get('trust_level', 'SILVER'),
                'worlds_qualified': report.get('worlds_qualified', False)
            }
            
        except Exception as e:
            # Fallback con datos mínimos
            return {
                'team_number': team_number,
                'team_name': f'Team {team_number}',
                'opr_numeric': 40,  # OPR promedio estimado
                'opr_display': 'N/A',
                'record': 'N/A',
                'wins': 0,
                'losses': 0,
                'win_rate': 0,
                'ranking': 'N/A',
                'trust_level': 'FALLBACK',
                'worlds_qualified': False,
                'error': str(e)
            }
    
    def _parse_opr(self, opr_str: str) -> float:
        """Convierte string de OPR a número"""
        try:
            if opr_str == 'N/A' or not opr_str:
                return 40.0  # OPR promedio estimado
            
            # Remover cualquier texto extra
            opr_clean = str(opr_str).replace('~', '').strip()
            return float(opr_clean)
        except (ValueError, TypeError, AttributeError):
            return 40.0
    
    def _parse_record(self, record_str: str) -> Tuple[int, int, int]:
        """Parsea string de récord W-L-T"""
        try:
            if record_str == 'N/A' or not record_str:
                return (0, 0, 0)
            
            parts = record_str.split('-')
            if len(parts) >= 2:
                wins = int(parts[0])
                losses = int(parts[1])
                ties = int(parts[2]) if len(parts) > 2 else 0
                return (wins, losses, ties)
        except (ValueError, IndexError, AttributeError):
            pass
        return (0, 0, 0)
    
    def _calculate_match_factors(self, red_teams: List[Dict], blue_teams: List[Dict]) -> Dict:
        """Calcula factores que influyen en el match"""
        team_count = len(red_teams)  # Ahora es dinámico (2 equipos)
        
        # Factor experiencia (% equipos con récord positivo)
        red_experienced = sum(1 for t in red_teams if t['win_rate'] > 50) / team_count
        blue_experienced = sum(1 for t in blue_teams if t['win_rate'] > 50) / team_count
        
        # Factor elite (equipos calificados a Worlds)
        red_worlds_teams = sum(1 for t in red_teams if t.get('worlds_qualified', False))
        blue_worlds_teams = sum(1 for t in blue_teams if t.get('worlds_qualified', False))
        
        # Factor consistencia (trust level PLATINUM/GOLD)
        red_reliable = sum(1 for t in red_teams if t['trust_level'] in ['PLATINUM', 'GOLD']) / team_count
        blue_reliable = sum(1 for t in blue_teams if t['trust_level'] in ['PLATINUM', 'GOLD']) / team_count
        
        return {
            'red_experience': round(red_experienced * 100, 1),
            'blue_experience': round(blue_experienced * 100, 1),
            'red_worlds_teams': red_worlds_teams,
            'blue_worlds_teams': blue_worlds_teams,
            'red_data_reliability': round(red_reliable * 100, 1),
            'blue_data_reliability': round(blue_reliable * 100, 1)
        }
    
    def _generate_ai_analysis(self, red_alliance: List[int], blue_alliance: List[int],
                             red_data: List[Dict], blue_data: List[Dict],
                             red_score: int, blue_score: int,
                             red_prob: float, blue_prob: float) -> Optional[str]:
        """Genera análisis del match con IA"""
        try:
            if not self.client:
                return None
            
            # Preparar contexto mejorado para IA
            context = f"""Analiza este match simulado de FTC con DATOS REALES:

🔴 ALIANZA ROJA (Probabilidad: {red_prob:.1f}%):
{self._format_alliance_data(red_alliance, red_data)}
Score Estimado: {red_score} puntos

🔵 ALIANZA AZUL (Probabilidad: {blue_prob:.1f}%):
{self._format_alliance_data(blue_alliance, blue_data)}
Score Estimado: {blue_score} puntos

IMPORTANTE: Menciona los equipos por su NÚMERO y NOMBRE correcto según los datos arriba.

Proporciona análisis profesional en 3 puntos:
1. ¿Qué alianza es favorita? Explica usando OPR, Win Rate y récord real de CADA equipo
2. Fortalezas específicas: Analiza el historial, premios WORLDS, y récord de victorias de cada equipo
3. Factores decisivos: ¿Qué podría inclinar la balanza? Considera experiencia y consistencia

Respuesta en español, profesional y emocionante. Sé específico con los números de equipo y estadísticas reales.

Respuesta en español, profesional pero emocionante."""

            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Eres un analista experto de FTC con acceso a datos estadísticos reales. Analiza matches basándote ÚNICAMENTE en los datos proporcionados: números de equipo, nombres, OPR, récord de victorias, y calificación a WORLDS. Menciona SIEMPRE los equipos por su número correcto. Usa las estadísticas reales para fundamentar tu análisis. Sé preciso y verifica que menciones correctamente qué equipos están en qué alianza."},
                    {"role": "user", "content": context}
                ],
                temperature=0.5,
                max_tokens=1200
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Error generando análisis: {str(e)}"
    
    def _format_alliance_data(self, alliance: List[int], data: List[Dict]) -> str:
        """Formatea datos de alianza para IA con detalles completos"""
        formatted = []
        for i, team in enumerate(data):
            worlds_badge = ' 🏆 WORLDS QUALIFIED' if team['worlds_qualified'] else ''
            wins = team['wins']
            losses = team['losses']
            
            # Resumen de experiencia
            experience_level = 'Élite' if team['win_rate'] > 70 else 'Experimentado' if team['win_rate'] > 50 else 'Competitivo' if team['win_rate'] > 30 else 'Emergente'
            
            formatted.append(
                f"  Equipo #{team['team_number']} - {team['team_name']}\n"
                f"    • OPR: {team['opr_display']} (Poder ofensivo)\n"
                f"    • Récord: {team['record']} ({wins} victorias, {losses} derrotas)\n"
                f"    • Win Rate: {team['win_rate']}% - Nivel {experience_level}\n"
                f"    • Ranking: {team['ranking']}{worlds_badge}"
            )
        return '\n'.join(formatted)

# Función helper para crear instancia
def create_oracle(trident_handler):
    """Crea instancia del oráculo con TRIDENTE"""
    return MatchOracle(trident_handler)
