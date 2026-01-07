#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AZTLAN DECODE - EL ORACULO
Simulador de Partidos con OPR, EPA y Predicciones IA
"""

import random
from typing import Dict, List, Optional, Tuple
import statistics

class MatchOracle:
    """Simulador avanzado de partidos FTC"""
    
    def __init__(self):
        self.confidence_threshold = 0.65
    
    def simulate_match(self, alliance_red: List[int], alliance_blue: List[int], 
                      team_stats: Dict) -> Dict:
        """
        Simular un match completo entre dos alianzas
        
        Args:
            alliance_red: Lista de 2 numeros de equipos (alianza roja)
            alliance_blue: Lista de 2 numeros de equipos (alianza azul)
            team_stats: Diccionario con estadisticas de equipos
        
        Returns:
            Diccionario con prediccion completa del match
        """
        # Calcular poder de cada alianza
        red_power = self._calculate_alliance_power(alliance_red, team_stats)
        blue_power = self._calculate_alliance_power(alliance_blue, team_stats)
        
        # Simular scores
        red_score = self._simulate_score(red_power, is_winning=(red_power['total'] > blue_power['total']))
        blue_score = self._simulate_score(blue_power, is_winning=(blue_power['total'] > red_power['total']))
        
        # Calcular probabilidad de victoria
        total_power = red_power['total'] + blue_power['total']
        red_win_prob = (red_power['total'] / total_power * 100) if total_power > 0 else 50
        blue_win_prob = 100 - red_win_prob
        
        # Determinar ganador
        winner = 'red' if red_score['total'] > blue_score['total'] else 'blue'
        margin = abs(red_score['total'] - blue_score['total'])
        
        # Nivel de confianza
        confidence = self._calculate_confidence(red_power, blue_power)
        
        return {
            'alliance_red': {
                'teams': alliance_red,
                'power': red_power,
                'predicted_score': red_score,
                'win_probability': round(red_win_prob, 1)
            },
            'alliance_blue': {
                'teams': alliance_blue,
                'power': blue_power,
                'predicted_score': blue_score,
                'win_probability': round(blue_win_prob, 1)
            },
            'prediction': {
                'winner': winner,
                'margin': margin,
                'confidence': confidence,
                'is_close_match': margin < 20,
                'upset_potential': confidence < self.confidence_threshold
            },
            'key_factors': self._identify_key_factors(red_power, blue_power),
            'strategy_tips': self._generate_strategy_tips(alliance_red, alliance_blue, team_stats, winner)
        }
    
    def _calculate_alliance_power(self, alliance: List[int], team_stats: Dict) -> Dict:
        """Calcular poder total de una alianza"""
        powers = {
            'opr': 0,
            'epa': 0,
            'auto_power': 0,
            'teleop_power': 0,
            'endgame_power': 0,
            'consistency': 0
        }
        
        valid_teams = 0
        for team_num in alliance:
            if team_num in team_stats:
                stats = team_stats[team_num]
                powers['opr'] += stats.get('opr', 30)
                powers['epa'] += stats.get('epa', 25)
                powers['auto_power'] += stats.get('auto_avg', 15)
                powers['teleop_power'] += stats.get('teleop_avg', 60)
                powers['endgame_power'] += stats.get('endgame_avg', 20)
                powers['consistency'] += stats.get('consistency', 0.7)
                valid_teams += 1
        
        # Promediar si hay equipos validos
        if valid_teams > 0:
            for key in powers:
                powers[key] = powers[key] / valid_teams
        
        # Calcular poder total (formula ponderada)
        powers['total'] = (
            powers['opr'] * 0.35 +
            powers['epa'] * 0.30 +
            powers['auto_power'] * 0.15 +
            powers['teleop_power'] * 0.10 +
            powers['endgame_power'] * 0.10
        )
        
        # Aplicar factor de consistencia
        powers['total'] *= powers['consistency']
        
        return powers
    
    def _simulate_score(self, alliance_power: Dict, is_winning: bool) -> Dict:
        """Simular score detallado de una alianza"""
        base_auto = alliance_power['auto_power']
        base_teleop = alliance_power['teleop_power']
        base_endgame = alliance_power['endgame_power']
        
        # Agregar variacion aleatoria basada en consistencia
        consistency = alliance_power['consistency']
        variance = (1 - consistency) * 0.3  # Hasta 30% de variacion
        
        auto = int(base_auto * random.uniform(1 - variance, 1 + variance))
        teleop = int(base_teleop * random.uniform(1 - variance, 1 + variance))
        endgame = int(base_endgame * random.uniform(1 - variance, 1 + variance))
        
        # Bonificacion si esta ganando (momentum)
        if is_winning:
            teleop += random.randint(5, 15)
            endgame += random.randint(3, 10)
        
        # Penalties (aleatorio, mas probable si losing)
        penalties = random.randint(0, 20) if not is_winning and random.random() < 0.3 else 0
        
        total = auto + teleop + endgame - penalties
        
        return {
            'auto': auto,
            'teleop': teleop,
            'endgame': endgame,
            'penalties': penalties,
            'total': max(0, total)
        }
    
    def _calculate_confidence(self, red_power: Dict, blue_power: Dict) -> str:
        """Calcular nivel de confianza en la prediccion"""
        diff = abs(red_power['total'] - blue_power['total'])
        avg = (red_power['total'] + blue_power['total']) / 2
        
        if avg == 0:
            return 'Low'
        
        diff_percentage = diff / avg
        
        # Considerar tambien la consistencia
        avg_consistency = (red_power['consistency'] + blue_power['consistency']) / 2
        
        confidence_score = diff_percentage * avg_consistency
        
        if confidence_score > 0.4:
            return 'Very High'
        elif confidence_score > 0.25:
            return 'High'
        elif confidence_score > 0.15:
            return 'Medium'
        else:
            return 'Low'
    
    def _identify_key_factors(self, red_power: Dict, blue_power: Dict) -> List[str]:
        """Identificar factores clave del match"""
        factors = []
        
        # Comparar autonomo
        if abs(red_power['auto_power'] - blue_power['auto_power']) > 10:
            stronger = 'Red' if red_power['auto_power'] > blue_power['auto_power'] else 'Blue'
            factors.append(f"🤖 {stronger} domina en AUTONOMO")
        
        # Comparar teleop
        if abs(red_power['teleop_power'] - blue_power['teleop_power']) > 20:
            stronger = 'Red' if red_power['teleop_power'] > blue_power['teleop_power'] else 'Blue'
            factors.append(f"🎮 {stronger} superior en TELEOP")
        
        # Comparar endgame
        if abs(red_power['endgame_power'] - blue_power['endgame_power']) > 8:
            stronger = 'Red' if red_power['endgame_power'] > blue_power['endgame_power'] else 'Blue'
            factors.append(f"🚀 {stronger} mas fuerte en ENDGAME")
        
        # Consistencia
        if abs(red_power['consistency'] - blue_power['consistency']) > 0.15:
            more_consistent = 'Red' if red_power['consistency'] > blue_power['consistency'] else 'Blue'
            factors.append(f"⚡ {more_consistent} es mas consistente")
        
        if not factors:
            factors.append("⚖️ Match muy parejo, puede decidirse por detalles")
        
        return factors
    
    def _generate_strategy_tips(self, red: List[int], blue: List[int], 
                                team_stats: Dict, predicted_winner: str) -> Dict:
        """Generar tips estrategicos para cada alianza"""
        return {
            'red': self._tips_for_alliance(red, blue, team_stats, predicted_winner == 'red'),
            'blue': self._tips_for_alliance(blue, red, team_stats, predicted_winner == 'blue')
        }
    
    def _tips_for_alliance(self, alliance: List[int], opponent: List[int], 
                          team_stats: Dict, is_favorite: bool) -> List[str]:
        """Generar tips para una alianza especifica"""
        tips = []
        
        if is_favorite:
            tips.append("🛡️ Juega seguro, minimiza errores")
            tips.append("⏱️ Controla el ritmo del partido")
            tips.append("🎯 Enfocate en ciclos consistentes")
        else:
            tips.append("⚡ Juega agresivo desde el inicio")
            tips.append("🎲 Toma riesgos calculados en autonomo")
            tips.append("🚀 El endgame sera crucial, ejecutalo perfectamente")
        
        tips.append("🤝 Comunicacion constante con tu alianza")
        tips.append("📊 Monitorea el score, ajusta estrategia si es necesario")
        
        return tips
    
    def simulate_elimination_bracket(self, alliances: List[Dict], 
                                     team_stats: Dict) -> Dict:
        """Simular bracket completo de eliminatorias"""
        results = {
            'semifinals': [],
            'finals': None,
            'champion': None
        }
        
        # Semifinales
        if len(alliances) >= 4:
            # Alliance 1 vs Alliance 4
            semi1 = self.simulate_match(
                alliances[0]['teams'], 
                alliances[3]['teams'], 
                team_stats
            )
            results['semifinals'].append({
                'match': 'Alliance 1 vs Alliance 4',
                'result': semi1
            })
            
            # Alliance 2 vs Alliance 3
            semi2 = self.simulate_match(
                alliances[1]['teams'], 
                alliances[2]['teams'], 
                team_stats
            )
            results['semifinals'].append({
                'match': 'Alliance 2 vs Alliance 3',
                'result': semi2
            })
            
            # Finales
            winner1_teams = (alliances[0]['teams'] if semi1['prediction']['winner'] == 'red' 
                           else alliances[3]['teams'])
            winner2_teams = (alliances[1]['teams'] if semi2['prediction']['winner'] == 'red' 
                           else alliances[2]['teams'])
            
            finals = self.simulate_match(winner1_teams, winner2_teams, team_stats)
            results['finals'] = finals
            
            # Campeon
            if finals['prediction']['winner'] == 'red':
                results['champion'] = {
                    'alliance': 'Winner of Semi 1',
                    'teams': winner1_teams
                }
            else:
                results['champion'] = {
                    'alliance': 'Winner of Semi 2',
                    'teams': winner2_teams
                }
        
        return results
    
    def predict_event_rankings(self, teams: List[int], team_stats: Dict, 
                              matches_per_team: int = 5) -> List[Dict]:
        """Predecir rankings finales de un evento"""
        rankings = []
        
        for team in teams:
            if team in team_stats:
                stats = team_stats[team]
                
                # Simular record estimado
                opr = stats.get('opr', 30)
                consistency = stats.get('consistency', 0.7)
                
                # Estimar victorias
                expected_wins = matches_per_team * (opr / 50) * consistency
                expected_wins = min(matches_per_team, max(0, expected_wins))
                
                wins = round(expected_wins)
                losses = matches_per_team - wins
                
                # Calcular ranking points y tiebreakers
                rp = wins * 2  # 2 RP por victoria
                tbp = int(opr * matches_per_team * consistency)
                
                rankings.append({
                    'team': team,
                    'rank': 0,  # Se asignara despues de ordenar
                    'record': f"{wins}-{losses}-0",
                    'rp': rp,
                    'tbp': tbp,
                    'opr': opr,
                    'projected_score': int(opr * 2)  # Score promedio estimado
                })
        
        # Ordenar por RP, luego TBP
        rankings.sort(key=lambda x: (x['rp'], x['tbp']), reverse=True)
        
        # Asignar ranks
        for i, team_rank in enumerate(rankings):
            team_rank['rank'] = i + 1
        
        return rankings


# Instancia global
oracle = MatchOracle()
