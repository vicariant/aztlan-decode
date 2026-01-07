#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PREDICTOR DE REGIONALES FTC
===========================
Predice resultados completos de un torneo: ranking, alianzas, ganadores
"""

import os
import logging
from typing import Dict, List, Optional, Tuple
from groq import Groq
from dotenv import load_dotenv
import random

load_dotenv()

# Configurar logger
logger = logging.getLogger(__name__)

class RegionalPredictor:
    """Predictor de resultados completos de torneos FTC"""
    
    def __init__(self, trident_handler):
        """
        Inicializa el predictor con acceso al sistema TRIDENTE
        
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
    
    def predict_regional(self, team_numbers: List[int], event_name: str = "Regional") -> Dict:
        """
        Predice resultados completos de un regional usando APIs + IA
        
        Args:
            team_numbers: Lista de números de equipos participantes
            event_name: Nombre del evento
            
        Returns:
            Dict con predicciones completas: ranking, alianzas, ganadores
        """
        try:
            # 1. OBTENER DATOS COMPLETOS DE TODAS LAS APIs
            teams_data = []
            for team in team_numbers:
                data = self._get_complete_team_data(team)
                teams_data.append(data)
            
            # 2. IA PREDICE RANKING COMPLETO (basado en datos reales)
            predicted_ranking = self._ai_predict_ranking(teams_data, event_name)
            
            # 3. IA PREDICE FORMACIÓN DE ALIANZAS (estrategia real)
            predicted_alliances = self._ai_predict_alliances(predicted_ranking, teams_data)
            
            # 4. IA PREDICE GANADOR DE ELIMINATORIAS
            winner_prediction = self._ai_predict_winner(predicted_alliances, teams_data)
            
            # 5. IA PREDICE PREMIOS ESPECIALES (análisis profundo)
            special_awards = self._ai_predict_awards(teams_data, predicted_ranking)
            
            # 6. IA GENERA ANÁLISIS COMPLETO DEL REGIONAL
            ai_analysis = self._generate_regional_analysis(
                event_name, predicted_ranking, predicted_alliances, 
                winner_prediction, special_awards, teams_data
            )
            
            return {
                'success': True,
                'event_name': event_name,
                'predicted_ranking': predicted_ranking,  # TODOS los equipos
                'predicted_alliances': predicted_alliances,
                'predicted_winner': winner_prediction,
                'special_awards': special_awards,
                'ai_analysis': ai_analysis,
                'total_teams': len(teams_data)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error prediciendo regional: {str(e)}'
            }
    
    def _get_complete_team_data(self, team_number: int) -> Dict:
        """Obtiene datos COMPLETOS del equipo desde APIs TRIDENT"""
        try:
            # Obtener reporte validado completo
            report = self.trident.get_validated_report(team_number)
            stats = report.get('stats', {})
            identity = report.get('identity', {})
            history = report.get('match_history', [])
            
            # Parsear OPR
            opr_str = stats.get('opr', '40')
            try:
                opr_numeric = float(str(opr_str).replace('~', '').strip())
            except (ValueError, TypeError, AttributeError):
                opr_numeric = 40
            
            # Parsear récord
            record_str = stats.get('record', '0-0-0')
            try:
                parts = record_str.split('-')
                wins = int(parts[0])
                losses = int(parts[1]) if len(parts) > 1 else 0
                ties = int(parts[2]) if len(parts) > 2 else 0
                total = wins + losses + ties
                win_rate = (wins / max(total, 1)) * 100
            except (ValueError, IndexError, AttributeError):
                wins = 0
                losses = 0
                ties = 0
                win_rate = 0
            
            # Analizar historial de matches (últimos 10)
            recent_performance = self._analyze_match_history(history[-10:]) if history else {
                'avg_score': opr_numeric,
                'consistency': 0.5,
                'trend': 'stable'
            }
            
            return {
                'team_number': team_number,
                'team_name': identity.get('team_name', f'Team {team_number}'),
                'opr_numeric': opr_numeric,
                'opr_display': opr_str,
                'record': record_str,
                'wins': wins,
                'losses': losses,
                'ties': ties,
                'win_rate': win_rate,
                'ranking': stats.get('ranking', 'N/A'),
                'worlds_qualified': report.get('worlds_qualified', False),
                'matches_played': len(history),
                'recent_performance': recent_performance,
                'highest_score': stats.get('highest_score', 0),
                'awards': report.get('awards', [])
            }
            
        except Exception as e:
            print(f"⚠️ Error obteniendo datos del equipo {team_number}: {e}")
            return {
                'team_number': team_number,
                'team_name': f'Team {team_number}',
                'opr_numeric': 35,
                'opr_display': 'N/A',
                'record': 'N/A',
                'wins': 0,
                'losses': 0,
                'ties': 0,
                'win_rate': 0,
                'ranking': 'N/A',
                'worlds_qualified': False,
                'matches_played': 0,
                'recent_performance': {'avg_score': 35, 'consistency': 0.5, 'trend': 'stable'},
                'highest_score': 0,
                'awards': []
            }
    
    def _analyze_match_history(self, matches: List[Dict]) -> Dict:
        """Analiza historial de matches para detectar tendencias"""
        if not matches:
            return {'avg_score': 0, 'consistency': 0, 'trend': 'stable'}
        
        scores = [m.get('score', 0) for m in matches]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # Calcular consistencia (desviación estándar)
        variance = sum((s - avg_score) ** 2 for s in scores) / len(scores) if scores else 0
        consistency = max(0, 1 - (variance ** 0.5) / max(avg_score, 1))
        
        # Detectar tendencia (primeros 5 vs últimos 5)
        if len(scores) >= 6:
            first_half = sum(scores[:len(scores)//2]) / (len(scores)//2)
            second_half = sum(scores[len(scores)//2:]) / (len(scores) - len(scores)//2)
            if second_half > first_half * 1.1:
                trend = 'improving'
            elif second_half < first_half * 0.9:
                trend = 'declining'
            else:
                trend = 'stable'
        else:
            trend = 'stable'
        
        return {
            'avg_score': avg_score,
            'consistency': consistency,
            'trend': trend
        }
    
    
    def _ai_predict_ranking(self, teams_data: List[Dict], event_name: str) -> List[Dict]:
        """USA IA PARA PREDECIR RANKING COMPLETO basado en datos reales de APIs"""
        if not self.client:
            # Fallback simple si no hay IA
            return self._fallback_ranking(teams_data)
        
        try:
            # Preparar datos para la IA
            teams_summary = "\n".join([
                f"#{t['team_number']} {t['team_name']}: OPR {t['opr_numeric']}, "
                f"Record {t['record']} ({t['win_rate']:.1f}% WR), "
                f"Tendencia: {t['recent_performance']['trend']}, "
                f"Consistencia: {t['recent_performance']['consistency']:.2f}, "
                f"Worlds: {'SÍ' if t['worlds_qualified'] else 'NO'}"
                for t in teams_data
            ])
            
            prompt = f"""Eres un experto analista de FTC. Analiza estos equipos para {event_name} y predice el ranking FINAL.

EQUIPOS PARTICIPANTES:
{teams_summary}

INSTRUCCIONES:
1. Analiza OPR, win rate, tendencia reciente y consistencia
2. Considera que equipos en ascenso pueden superar su OPR
3. Equipos Worlds-qualified suelen ser más consistentes
4. Predice Ranking Points (RP) realistas para 5-6 qualification matches
5. FORMATO EXACTO para cada equipo (una línea):
   RANK|TEAM_NUMBER|PREDICTED_RP|PREDICTED_WINS

Ejemplo: 1|16818|95|5
NO agregues texto adicional, solo las líneas de ranking."""

            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,  # Baja temperatura para predicciones consistentes
                max_tokens=800
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Parsear respuesta de la IA
            ranking = []
            for line in ai_response.split('\n'):
                line = line.strip()
                if '|' in line and not line.startswith('#'):
                    try:
                        parts = line.split('|')
                        if len(parts) >= 4:
                            rank = int(parts[0])
                            team_num = int(parts[1])
                            predicted_rp = int(parts[2])
                            predicted_wins = int(parts[3])
                            
                            # Encontrar datos del equipo
                            team_data = next((t for t in teams_data if t['team_number'] == team_num), None)
                            if team_data:
                                predicted_losses = 5 - predicted_wins
                                ranking.append({
                                    'rank': rank,
                                    'team_number': team_num,
                                    'team_name': team_data['team_name'],
                                    'predicted_rp': predicted_rp,
                                    'predicted_record': f"{predicted_wins}-{predicted_losses}-0",
                                    'opr': team_data['opr_display'],
                                    'worlds_qualified': team_data['worlds_qualified']
                                })
                    except (KeyError, ValueError, TypeError) as e:
                        logger.warning(f"Error procesando equipo en ranking: {e}")
                        continue
            
            # Si la IA falló, usar fallback
            if not ranking:
                return self._fallback_ranking(teams_data)
            
            # Ordenar por rank
            ranking.sort(key=lambda x: x['rank'])
            return ranking
            
        except Exception as e:
            print(f"⚠️ Error en predicción IA de ranking: {e}")
            return self._fallback_ranking(teams_data)
    
    def _fallback_ranking(self, teams_data: List[Dict]) -> List[Dict]:
        """Ranking de respaldo basado en matemáticas simples"""
        ranking = []
        
        # Ordenar por poder combinado
        sorted_teams = sorted(teams_data, 
                            key=lambda x: (x['opr_numeric'] * 0.7 + x['win_rate'] * 0.3), 
                            reverse=True)
        
        for i, team in enumerate(sorted_teams):
            predicted_rp = int(team['opr_numeric'] * 5 * (0.8 + team['recent_performance']['consistency'] * 0.4))
            predicted_wins = int(5 * team['win_rate'] / 100)
            predicted_losses = 5 - predicted_wins
            
            ranking.append({
                'rank': i + 1,
                'team_number': team['team_number'],
                'team_name': team['team_name'],
                'predicted_rp': predicted_rp,
                'predicted_record': f"{predicted_wins}-{predicted_losses}-0",
                'opr': team['opr_display'],
                'worlds_qualified': team['worlds_qualified']
            })
        
        return ranking
    
    def _ai_predict_alliances(self, ranking: List[Dict], teams_data: List[Dict]) -> List[Dict]:
        """USA IA PARA PREDECIR FORMACIÓN DE ALIANZAS (estrategia real)"""
        if not self.client or len(ranking) < 4:
            return self._fallback_alliances(ranking)
        
        try:
            # Top 4 son captains
            captains = ranking[:4]
            available = ranking[4:]
            
            captains_info = "\n".join([
                f"Alianza {i+1} - Capitán #{c['team_number']} {c['team_name']} (Rank {c['rank']}, {c['predicted_rp']} RP)"
                for i, c in enumerate(captains)
            ])
            
            available_info = "\n".join([
                f"#{t['team_number']} {t['team_name']} (Rank {t['rank']}, {t['predicted_rp']} RP, OPR {t['opr']})"
                for t in available[:12]  # Top 12 disponibles
            ])
            
            prompt = f"""Eres un experto estratega de FTC. Predice las selecciones de alianzas.

CAPITANES (Top 4):
{captains_info}

EQUIPOS DISPONIBLES:
{available_info}

ESTRATEGIA:
- Alianza 1 (mejor seed) escoge primero el mejor disponible
- Buscan complementar fortalezas (offense + defense)
- Evitan equipos inconsistentes para playoffs
- Prefieren equipos con experiencia (Worlds-qualified)

FORMATO EXACTO (una línea por pick):
ALLIANCE_NUM|PICK_NUM|TEAM_NUMBER

Ejemplo:
1|1|16818
1|2|28254
2|1|12345

NO agregues texto adicional."""

            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=600
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Parsear picks de la IA
            alliances = [{'alliance_number': i+1, 'captain': cap, 'pick1': None, 'pick2': None} 
                        for i, cap in enumerate(captains)]
            
            for line in ai_response.split('\n'):
                line = line.strip()
                if '|' in line:
                    try:
                        parts = line.split('|')
                        if len(parts) >= 3:
                            alliance_num = int(parts[0]) - 1
                            pick_num = int(parts[1])
                            team_num = int(parts[2])
                            
                            if 0 <= alliance_num < 4:
                                team_data = next((t for t in available if t['team_number'] == team_num), None)
                                if team_data:
                                    if pick_num == 1:
                                        alliances[alliance_num]['pick1'] = team_data
                                    elif pick_num == 2:
                                        alliances[alliance_num]['pick2'] = team_data
                    except (KeyError, StopIteration, ValueError) as e:
                        logger.warning(f"Error procesando alianza: {e}")
                        continue
            
            # Calcular combined_rp para cada alianza
            for alliance in alliances:
                alliance['combined_rp'] = (
                    alliance['captain']['predicted_rp'] + 
                    (alliance['pick1']['predicted_rp'] if alliance['pick1'] else 0) + 
                    (alliance['pick2']['predicted_rp'] if alliance['pick2'] else 0)
                )
            
            return alliances
            
        except Exception as e:
            print(f"⚠️ Error en predicción IA de alianzas: {e}")
            return self._fallback_alliances(ranking)
    
    def _fallback_alliances(self, ranking: List[Dict]) -> List[Dict]:
        """Alianzas de respaldo (picks automáticos)"""
        alliances = []
        used_teams = set()
        
        # Top 4 son captains
        for i in range(min(4, len(ranking))):
            captain = ranking[i]
            used_teams.add(captain['team_number'])
            
            # Pick 1: Mejor disponible
            pick1 = None
            pick2 = None
            
            for t in ranking[4:]:
                if t['team_number'] not in used_teams:
                    if pick1 is None:
                        pick1 = t
                        used_teams.add(t['team_number'])
                    elif pick2 is None:
                        pick2 = t
                        used_teams.add(t['team_number'])
                        break
            
            alliances.append({
                'alliance_number': i + 1,
                'captain': captain,
                'pick1': pick1,
                'pick2': pick2,
                'combined_rp': captain['predicted_rp'] + (pick1['predicted_rp'] if pick1 else 0) + (pick2['predicted_rp'] if pick2 else 0)
            })
        
        return alliances
    
    def _ai_predict_winner(self, alliances: List[Dict], teams_data: List[Dict]) -> Dict:
        """USA IA PARA PREDECIR GANADOR DE PLAYOFFS"""
        if not self.client or len(alliances) < 4:
            return self._fallback_winner(alliances)
        
        try:
            alliances_info = "\n".join([
                f"Alianza {a['alliance_number']}: Cap #{a['captain']['team_number']} + "
                f"{'#' + str(a['pick1']['team_number']) if a['pick1'] else 'N/A'} + "
                f"{'#' + str(a['pick2']['team_number']) if a['pick2'] else 'N/A'} "
                f"(RP Combinado: {a['combined_rp']})"
                for a in alliances
            ])
            
            prompt = f"""Eres un experto de FTC. Predice el ganador de playoffs.

ALIANZAS:
{alliances_info}

BRACKET: Semifinales → Alianza 1 vs 4, Alianza 2 vs 3 → Final

CONSIDERA:
- RP combinado (poder ofensivo)
- Experiencia de capitanes
- Complementariedad de los picks
- Consistencia en playoffs (presión)

FORMATO EXACTO:
WINNER|ALLIANCE_NUM
FINALIST|ALLIANCE_NUM

Ejemplo:
WINNER|1
FINALIST|2"""

            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=200
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            winner_alliance = None
            finalist_alliance = None
            
            for line in ai_response.split('\n'):
                if 'WINNER|' in line:
                    alliance_num = int(line.split('|')[1]) - 1
                    if 0 <= alliance_num < len(alliances):
                        winner_alliance = alliances[alliance_num]
                elif 'FINALIST|' in line:
                    alliance_num = int(line.split('|')[1]) - 1
                    if 0 <= alliance_num < len(alliances):
                        finalist_alliance = alliances[alliance_num]
            
            if not winner_alliance:
                return self._fallback_winner(alliances)
            
            return {
                'winner': winner_alliance,
                'finalist': finalist_alliance or alliances[1],
                'semifinalists': alliances[:4]
            }
            
        except Exception as e:
            print(f"⚠️ Error en predicción IA de ganador: {e}")
            return self._fallback_winner(alliances)
    
    def _fallback_winner(self, alliances: List[Dict]) -> Dict:
        """Ganador de respaldo (por RP combinado)"""
        if len(alliances) < 2:
            return {'winner': alliances[0] if alliances else None, 'finalist': None}
        
        # Simular playoffs por RP
        sorted_alliances = sorted(alliances, key=lambda a: a['combined_rp'], reverse=True)
        
        return {
            'winner': sorted_alliances[0],
            'finalist': sorted_alliances[1],
            'semifinalists': alliances[:4]
        }
    
    def _ai_predict_awards(self, teams_data: List[Dict], ranking: List[Dict]) -> Dict:
        """USA IA PARA PREDECIR PREMIOS ESPECIALES"""
        if not self.client or len(teams_data) < 3:
            return self._fallback_awards(teams_data)
        
        try:
            teams_info = "\n".join([
                f"#{t['team_number']} {t['team_name']}: Rank {i+1}, OPR {t['opr_numeric']}, "
                f"WR {t['win_rate']:.0f}%, Worlds: {'SÍ' if t['worlds_qualified'] else 'NO'}, "
                f"Premios previos: {len(t.get('awards', []))}"
                for i, t in enumerate(teams_data[:10])
            ])
            
            prompt = f"""Predice premios especiales de FTC basándote en datos reales.

EQUIPOS:
{teams_info}

PREMIOS:
1. INSPIRE AWARD: Mejor equipo overall (OPR + récord + Worlds + comunidad)
2. CONTROL AWARD: Mejor autonomía y sensores
3. INNOVATE AWARD: Diseño mecánico innovador

FORMATO EXACTO:
INSPIRE|TEAM_NUMBER
CONTROL|TEAM_NUMBER
INNOVATE|TEAM_NUMBER

Ejemplo:
INSPIRE|16818
CONTROL|28254
INNOVATE|12345"""

            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=200
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            awards = {'inspire_award': 'TBD', 'control_award': 'TBD', 'innovate_award': 'TBD'}
            
            for line in ai_response.split('\n'):
                if 'INSPIRE|' in line:
                    team_num = int(line.split('|')[1])
                    team = next((t for t in teams_data if t['team_number'] == team_num), None)
                    if team:
                        awards['inspire_award'] = f"#{team['team_number']} {team['team_name']}"
                elif 'CONTROL|' in line:
                    team_num = int(line.split('|')[1])
                    team = next((t for t in teams_data if t['team_number'] == team_num), None)
                    if team:
                        awards['control_award'] = f"#{team['team_number']} {team['team_name']}"
                elif 'INNOVATE|' in line:
                    team_num = int(line.split('|')[1])
                    team = next((t for t in teams_data if t['team_number'] == team_num), None)
                    if team:
                        awards['innovate_award'] = f"#{team['team_number']} {team['team_name']}"
            
            return awards
            
        except Exception as e:
            print(f"⚠️ Error en predicción IA de premios: {e}")
            return self._fallback_awards(teams_data)
    
    def _fallback_awards(self, teams_data: List[Dict]) -> Dict:
        """Premios de respaldo"""
        sorted_teams = sorted(teams_data, key=lambda t: t['opr_numeric'], reverse=True)
        
        return {
            'inspire_award': f"#{sorted_teams[0]['team_number']} {sorted_teams[0]['team_name']}" if sorted_teams else 'TBD',
            'control_award': f"#{sorted_teams[1]['team_number']} {sorted_teams[1]['team_name']}" if len(sorted_teams) > 1 else 'TBD',
            'innovate_award': f"#{sorted_teams[2]['team_number']} {sorted_teams[2]['team_name']}" if len(sorted_teams) > 2 else 'TBD'
        }
    
    def _generate_regional_analysis(self, event_name: str, ranking: List[Dict], 
                                   alliances: List[Dict], winner: Dict, awards: Dict, 
                                   teams_data: List[Dict]) -> Optional[str]:
        """Genera análisis completo del regional con IA usando DATOS REALES"""
        try:
            if not self.client or len(ranking) == 0:
                return "Análisis no disponible (IA no configurada)"
            
            # Preparar contexto completo
            top_teams = "\n".join([
                f"{t['rank']}. #{t['team_number']} {t['team_name']} - {t['predicted_rp']} RP (OPR: {t['opr']}, WR: {ranking[i-1]['predicted_record'] if i <= len(ranking) else 'N/A'})"
                for i, t in enumerate(ranking[:8], 1)
            ])
            
            winner_captain = winner['winner']['captain']
            finalist_captain = winner['finalist']['captain']
            
            # Incluir info detallada de equipos top
            detailed_info = []
            for i, team in enumerate(teams_data[:5]):
                info = f"#{team['team_number']} {team['team_name']}: OPR {team['opr_numeric']}, "
                info += f"Récord {team['record']}, Tendencia {team['recent_performance']['trend']}, "
                info += f"Consistencia {team['recent_performance']['consistency']:.2f}"
                if team['worlds_qualified']:
                    info += " [WORLDS QUALIFIED]"
                detailed_info.append(info)
            
            context = f"""Analiza este REGIONAL PREDICHO de FTC basándote en DATOS REALES de APIs:

📍 EVENTO: {event_name}
👥 EQUIPOS PARTICIPANTES: {len(ranking)}

🏆 RANKING PREDICHO (Top 8):
{top_teams}

📊 DATOS DETALLADOS (Top 5):
{chr(10).join(detailed_info)}

⚔️ ALIANZAS PREDICHAS:
1. Alianza #{alliances[0]['alliance_number']}: Capitán #{alliances[0]['captain']['team_number']} {alliances[0]['captain']['team_name']} ({alliances[0]['combined_rp']} RP total)
2. Alianza #{alliances[1]['alliance_number']}: Capitán #{alliances[1]['captain']['team_number']} {alliances[1]['captain']['team_name']} ({alliances[1]['combined_rp']} RP total)
3. Alianza #{alliances[2]['alliance_number']}: Capitán #{alliances[2]['captain']['team_number']} {alliances[2]['captain']['team_name']} ({alliances[2]['combined_rp']} RP total)
4. Alianza #{alliances[3]['alliance_number']}: Capitán #{alliances[3]['captain']['team_number']} {alliances[3]['captain']['team_name']} ({alliances[3]['combined_rp']} RP total)

🥇 GANADOR PREDICHO: #{winner_captain['team_number']} {winner_captain['team_name']} ({winner_captain['predicted_rp']} RP)
🥈 FINALISTA PREDICHO: #{finalist_captain['team_number']} {finalist_captain['team_name']} ({finalist_captain['predicted_rp']} RP)

🏅 PREMIOS ESPECIALES PREDICHOS:
- 🏆 Inspire Award: {awards['inspire_award']}
- 🎮 Control Award: {awards['control_award']}
- 💡 Innovate Award: {awards['innovate_award']}

INSTRUCCIONES:
Analiza este regional predicho en 5 secciones:

1. **FAVORITOS AL TÍTULO** (2-3 oraciones)
   - Analiza por qué la alianza ganadora dominará
   - Menciona sus fortalezas (OPR, consistencia, experiencia Worlds)

2. **DARK HORSES** (2-3 oraciones)
   - Equipos con tendencia "improving" que sorprenderán
   - Menciona equipos específicos con datos

3. **ESTRATEGIA DE PICKS** (2-3 oraciones)
   - Explica por qué se formaron así las alianzas
   - Qué buscan los captains (complementar offense/defense)

4. **PREMIOS ESPECIALES** (2 oraciones)
   - Justifica Inspire Award (OPR + Worlds + comunidad)
   - Justifica Control/Innovate

5. **PREDICCIÓN FINAL** (2 oraciones)
   - Ganador y margen de victoria
   - Momento clave que definirá el regional

Respuesta en español, datos específicos de equipos, emocionante, máximo 1200 tokens."""

            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Eres un analista experto de FTC con años de experiencia. Analizas datos REALES (OPR, récord, tendencias) de APIs para hacer predicciones fundamentadas. Menciona números de equipos específicos y datos concretos."},
                    {"role": "user", "content": context}
                ],
                temperature=0.6,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"⚠️ Error generando análisis IA: {e}")
            return f"❌ Error generando análisis: {str(e)}"

# Función helper
def create_regional_predictor(trident_handler):
    """Crea instancia del predictor"""
    return RegionalPredictor(trident_handler)
