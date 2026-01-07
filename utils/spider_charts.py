#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AZTLAN DECODE - SPIDER CHARTS
Graficas de radar para comparacion visual de robots
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Optional
import json

class SpiderChartGenerator:
    """Generador de graficas de radar para comparar equipos"""
    
    def __init__(self):
        # Categorias de evaluacion
        self.categories = [
            'Autonomo',
            'TeleOp',
            'EndGame',
            'Fiabilidad',
            'Defensa'
        ]
        
        # Colores para diferentes equipos
        self.colors = [
            '#FFD700',  # Oro
            '#4A90E2',  # Azul
            '#FF6B35',  # Rojo
            '#00D9FF',  # Cyan
            '#B620E0'   # Purpura
        ]
    
    def create_single_team_radar(self, team_data: Dict, team_number: int) -> str:
        """Crear grafica de radar para un solo equipo"""
        
        # Extraer valores (0-100)
        values = [
            team_data.get('auto_score', 50),
            team_data.get('teleop_score', 50),
            team_data.get('endgame_score', 50),
            team_data.get('reliability', 50),
            team_data.get('defense', 50)
        ]
        
        # Cerrar el poligono
        values_closed = values + [values[0]]
        categories_closed = self.categories + [self.categories[0]]
        
        # Crear figura
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values_closed,
            theta=categories_closed,
            fill='toself',
            fillcolor='rgba(255, 215, 0, 0.3)',
            line=dict(color='#FFD700', width=3),
            name=f'Team {team_number}',
            hovertemplate='<b>%{theta}</b><br>Score: %{r}/100<extra></extra>'
        ))
        
        # Layout
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=12, color='white'),
                    gridcolor='rgba(255, 255, 255, 0.2)'
                ),
                angularaxis=dict(
                    tickfont=dict(size=14, color='#FFD700'),
                    gridcolor='rgba(255, 255, 255, 0.2)'
                ),
                bgcolor='rgba(0, 0, 0, 0.5)'
            ),
            showlegend=True,
            legend=dict(
                font=dict(size=14, color='white'),
                bgcolor='rgba(0, 0, 0, 0.5)'
            ),
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            title=dict(
                text=f'🏛️ Analisis Multidimensional - Team {team_number}',
                font=dict(size=20, color='#FFD700'),
                x=0.5,
                xanchor='center'
            ),
            height=500,
            margin=dict(t=100, b=50, l=50, r=50)
        )
        
        # Convertir a JSON para JavaScript
        return fig.to_json()
    
    def create_comparison_radar(self, teams_data: List[Dict]) -> str:
        """Crear grafica de radar comparando multiples equipos"""
        
        fig = go.Figure()
        
        # Agregar cada equipo
        for i, team in enumerate(teams_data[:5]):  # Maximo 5 equipos
            team_number = team['number']
            
            values = [
                team.get('auto_score', 50),
                team.get('teleop_score', 50),
                team.get('endgame_score', 50),
                team.get('reliability', 50),
                team.get('defense', 50)
            ]
            
            # Cerrar el poligono
            values_closed = values + [values[0]]
            categories_closed = self.categories + [self.categories[0]]
            
            color = self.colors[i % len(self.colors)]
            
            fig.add_trace(go.Scatterpolar(
                r=values_closed,
                theta=categories_closed,
                fill='toself',
                fillcolor=f'rgba{self._hex_to_rgba(color, 0.2)}',
                line=dict(color=color, width=2),
                name=f'Team {team_number}',
                hovertemplate=f'<b>Team {team_number}</b><br>%{{theta}}: %{{r}}/100<extra></extra>'
            ))
        
        # Layout
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=12, color='white'),
                    gridcolor='rgba(255, 255, 255, 0.2)'
                ),
                angularaxis=dict(
                    tickfont=dict(size=14, color='#FFD700'),
                    gridcolor='rgba(255, 255, 255, 0.2)'
                ),
                bgcolor='rgba(0, 0, 0, 0.5)'
            ),
            showlegend=True,
            legend=dict(
                font=dict(size=12, color='white'),
                bgcolor='rgba(0, 0, 0, 0.5)',
                orientation='v',
                x=1.1,
                y=0.5
            ),
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            title=dict(
                text='🕸️ Comparacion Multidimensional de Equipos',
                font=dict(size=20, color='#FFD700'),
                x=0.5,
                xanchor='center'
            ),
            height=600,
            margin=dict(t=100, b=50, l=50, r=150)
        )
        
        return fig.to_json()
    
    def create_alliance_radar(self, alliance_teams: List[Dict], 
                            alliance_name: str = 'Alliance') -> str:
        """Crear grafica de radar para una alianza (promedio de equipos)"""
        
        if not alliance_teams:
            return json.dumps({})
        
        # Calcular promedios
        avg_values = [0] * len(self.categories)
        
        for team in alliance_teams:
            avg_values[0] += team.get('auto_score', 50)
            avg_values[1] += team.get('teleop_score', 50)
            avg_values[2] += team.get('endgame_score', 50)
            avg_values[3] += team.get('reliability', 50)
            avg_values[4] += team.get('defense', 50)
        
        # Promediar
        num_teams = len(alliance_teams)
        avg_values = [v / num_teams for v in avg_values]
        
        # Cerrar poligono
        avg_values_closed = avg_values + [avg_values[0]]
        categories_closed = self.categories + [self.categories[0]]
        
        # Crear figura
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=avg_values_closed,
            theta=categories_closed,
            fill='toself',
            fillcolor='rgba(74, 144, 226, 0.4)',
            line=dict(color='#4A90E2', width=3),
            name=alliance_name,
            hovertemplate='<b>%{theta}</b><br>Promedio: %{r:.1f}/100<extra></extra>'
        ))
        
        # Layout
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=12, color='white'),
                    gridcolor='rgba(255, 255, 255, 0.2)'
                ),
                angularaxis=dict(
                    tickfont=dict(size=14, color='#FFD700'),
                    gridcolor='rgba(255, 255, 255, 0.2)'
                ),
                bgcolor='rgba(0, 0, 0, 0.5)'
            ),
            showlegend=True,
            legend=dict(
                font=dict(size=14, color='white'),
                bgcolor='rgba(0, 0, 0, 0.5)'
            ),
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            title=dict(
                text=f'🏛️ Poder de {alliance_name}',
                font=dict(size=20, color='#FFD700'),
                x=0.5,
                xanchor='center'
            ),
            height=500,
            margin=dict(t=100, b=50, l=50, r=50)
        )
        
        return fig.to_json()
    
    def create_historical_radar(self, team_history: List[Dict], 
                               team_number: int) -> str:
        """Crear grafica mostrando evolucion del equipo en el tiempo"""
        
        fig = go.Figure()
        
        # Agregar cada periodo (ej: cada evento)
        for i, period in enumerate(team_history[-5:]):  # Ultimos 5 periodos
            values = [
                period.get('auto_score', 50),
                period.get('teleop_score', 50),
                period.get('endgame_score', 50),
                period.get('reliability', 50),
                period.get('defense', 50)
            ]
            
            values_closed = values + [values[0]]
            categories_closed = self.categories + [self.categories[0]]
            
            # Opacidad incrementa con el tiempo (mas reciente = mas opaco)
            opacity = 0.3 + (i * 0.15)
            
            fig.add_trace(go.Scatterpolar(
                r=values_closed,
                theta=categories_closed,
                fill='toself',
                fillcolor=f'rgba(255, 215, 0, {opacity})',
                line=dict(color='#FFD700', width=2),
                name=period.get('label', f'Periodo {i+1}'),
                hovertemplate=f'<b>{period.get("label", f"Periodo {i+1}")}</b><br>%{{theta}}: %{{r}}/100<extra></extra>'
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=12, color='white'),
                    gridcolor='rgba(255, 255, 255, 0.2)'
                ),
                angularaxis=dict(
                    tickfont=dict(size=14, color='#FFD700'),
                    gridcolor='rgba(255, 255, 255, 0.2)'
                ),
                bgcolor='rgba(0, 0, 0, 0.5)'
            ),
            showlegend=True,
            legend=dict(
                font=dict(size=12, color='white'),
                bgcolor='rgba(0, 0, 0, 0.5)'
            ),
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            title=dict(
                text=f'📈 Evolucion Team {team_number}',
                font=dict(size=20, color='#FFD700'),
                x=0.5,
                xanchor='center'
            ),
            height=500,
            margin=dict(t=100, b=50, l=50, r=50)
        )
        
        return fig.to_json()
    
    def _hex_to_rgba(self, hex_color: str, alpha: float) -> str:
        """Convertir color hex a rgba"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f'({r}, {g}, {b}, {alpha})'
    
    def generate_team_scores(self, team_stats: Dict) -> Dict:
        """Generar scores de 0-100 para cada categoria desde stats reales"""
        
        # Normalizar valores a escala 0-100
        def normalize(value, min_val, max_val):
            if max_val == min_val:
                return 50
            return int(((value - min_val) / (max_val - min_val)) * 100)
        
        # Valores tipicos de FTC
        return {
            'auto_score': min(100, int((team_stats.get('auto_avg', 15) / 40) * 100)),
            'teleop_score': min(100, int((team_stats.get('teleop_avg', 60) / 120) * 100)),
            'endgame_score': min(100, int((team_stats.get('endgame_avg', 20) / 45) * 100)),
            'reliability': int(team_stats.get('consistency', 0.7) * 100),
            'defense': int(team_stats.get('defense_rating', 5) * 10)  # 0-10 scale
        }


# Instancia global
spider_charts = SpiderChartGenerator()
