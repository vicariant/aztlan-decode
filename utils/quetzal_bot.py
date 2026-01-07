#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AZTLAN DECODE - QUETZAL BOT
Asistente IA de reglas FTC con RAG (Retrieval-Augmented Generation)
"""

import os
from groq import Groq
from config.settings import GROQ_API_KEY
import json
from typing import List, Dict, Optional

class QuetzalBot:
    """Asistente inteligente para reglas y estrategia FTC"""
    
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = "mixtral-8x7b-32768"
        
        # Knowledge base de reglas FTC (simplificado)
        self.ftc_rules = self._load_ftc_rules()
        
        # Contexto del sistema
        self.system_prompt = """
        Eres Quetzal, el asistente experto en FIRST Tech Challenge (FTC).
        Tu mision es ayudar a equipos de robotica a entender las reglas del juego DECODE.
        
        Conocimiento:
        - Reglas oficiales de FTC temporada 2024-2025
        - Estrategias de juego
        - Mecanismos de puntuacion
        - Penalizaciones y faltas
        
        Estilo:
        - Respuestas claras y concisas
        - Cita el numero de regla cuando sea relevante
        - Usa analogias para explicar conceptos complejos
        - Se amigable pero profesional
        """
    
    def _load_ftc_rules(self) -> Dict:
        """Cargar base de conocimiento de reglas FTC"""
        return {
            "game_manual": {
                "G01": {
                    "title": "Safety First",
                    "description": "La seguridad es prioridad. Robots deben ser seguros para operadores y publico.",
                    "penalty": "Inhabilitacion"
                },
                "G14": {
                    "title": "Zona de Carga Bloqueada",
                    "description": "Robots no pueden bloquear la zona de carga del oponente.",
                    "penalty": "Falta Mayor (30 puntos)"
                },
                "G20": {
                    "title": "Contacto Robot-Robot",
                    "description": "Contacto de robot debe ser accidental y minimo.",
                    "penalty": "Falta Menor (10 puntos)"
                },
                "Autonomo": {
                    "duration": "30 segundos",
                    "points": {
                        "Navigation": "20 puntos",
                        "Sample Scoring": "6-10 puntos por muestra",
                        "Parking": "3 puntos"
                    }
                },
                "TeleOp": {
                    "duration": "2 minutos",
                    "scoring": {
                        "Low Basket": "4 puntos",
                        "High Basket": "8 puntos",
                        "Low Chamber": "6 puntos",
                        "High Chamber": "10 puntos"
                    }
                },
                "EndGame": {
                    "duration": "30 segundos",
                    "points": {
                        "Level 1 Ascent": "3 puntos",
                        "Level 2 Ascent": "15 puntos",
                        "Level 3 Ascent": "30 puntos"
                    }
                }
            },
            
            "strategy_tips": {
                "cycle_time": "Tiempo ideal de ciclo: 15-20 segundos",
                "autonomous_priority": "Priorizar: Navigation > Sample Scoring > Parking",
                "endgame_focus": "Practicar ascent repetidamente, vale muchos puntos",
                "defense": "Defensa legal: Bloquear muestras sin contacto directo"
            }
        }
    
    def ask(self, question: str, context: Optional[str] = None) -> Dict:
        """Hacer pregunta al asistente"""
        
        # Buscar reglas relevantes
        relevant_rules = self._search_relevant_rules(question)
        
        # Construir contexto
        context_text = self._build_context(relevant_rules, context)
        
        # Generar respuesta
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"""
            Contexto de reglas:
            {context_text}
            
            Pregunta del usuario:
            {question}
            
            Proporciona una respuesta clara y util. Si es relevante, cita el numero de regla.
            """}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=1000
            )
            
            answer = response.choices[0].message.content
            
            return {
                "success": True,
                "question": question,
                "answer": answer,
                "relevant_rules": relevant_rules,
                "tokens_used": response.usage.total_tokens if response.usage else 0
            }
        
        except Exception as e:
            return {
                "success": False,
                "question": question,
                "error": str(e),
                "answer": "Lo siento, no pude procesar tu pregunta. Intenta reformularla."
            }
    
    def _search_relevant_rules(self, question: str) -> List[Dict]:
        """Buscar reglas relevantes para la pregunta"""
        question_lower = question.lower()
        relevant = []
        
        # Keywords para busqueda simple
        keywords_map = {
            "autonomo": "Autonomo",
            "autonomous": "Autonomo",
            "teleop": "TeleOp",
            "endgame": "EndGame",
            "penalizacion": "G14",
            "penalty": "G14",
            "falta": "G20",
            "bloquear": "G14",
            "contacto": "G20",
            "seguridad": "G01",
            "safety": "G01",
            "puntos": "TeleOp",
            "scoring": "TeleOp",
            "ascent": "EndGame",
            "climb": "EndGame"
        }
        
        for keyword, rule_key in keywords_map.items():
            if keyword in question_lower:
                if rule_key in self.ftc_rules["game_manual"]:
                    rule = self.ftc_rules["game_manual"][rule_key]
                    relevant.append({
                        "rule_id": rule_key,
                        "rule": rule
                    })
        
        return relevant[:3]  # Top 3 reglas relevantes
    
    def _build_context(self, relevant_rules: List[Dict], additional_context: Optional[str] = None) -> str:
        """Construir texto de contexto"""
        context_parts = []
        
        # Agregar reglas relevantes
        for item in relevant_rules:
            rule_id = item["rule_id"]
            rule = item["rule"]
            
            if isinstance(rule, dict):
                if "title" in rule:
                    context_parts.append(f"{rule_id}: {rule['title']} - {rule.get('description', '')}")
                else:
                    context_parts.append(f"{rule_id}: {json.dumps(rule, indent=2)}")
        
        # Agregar contexto adicional si existe
        if additional_context:
            context_parts.append(f"Contexto adicional: {additional_context}")
        
        return "\n\n".join(context_parts)
    
    def get_quick_answer(self, query_type: str) -> str:
        """Respuestas rapidas para preguntas comunes"""
        quick_answers = {
            "scoring": """
            🎯 SISTEMA DE PUNTUACION DECODE:
            
            AUTONOMO (30 seg):
            • Navigation: 20 pts
            • Sample Scoring: 6-10 pts c/u
            • Parking: 3 pts
            
            TELEOP (2 min):
            • Low Basket: 4 pts
            • High Basket: 8 pts
            • Low Chamber: 6 pts
            • High Chamber: 10 pts
            
            ENDGAME (30 seg):
            • Level 1: 3 pts
            • Level 2: 15 pts
            • Level 3: 30 pts
            """,
            
            "penalties": """
            ⚠️ PENALIZACIONES COMUNES:
            
            • Falta Menor (10 pts): Contacto minimo, juego brusco leve
            • Falta Mayor (30 pts): Bloquear zona de carga, pinning excesivo
            • Tarjeta Amarilla: Comportamiento no deportivo
            • Tarjeta Roja: Violacion grave, posible inhabilitacion
            """,
            
            "strategy": """
            🧠 TIPS ESTRATEGICOS:
            
            1. Prioriza el autonomo - vale mucho
            2. Practica ciclos rapidos (15-20 seg)
            3. Endgame es critico - Level 3 = 30 pts
            4. Defensa legal sin contacto
            5. Comunicacion constante con alianza
            """,
            
            "timeline": """
            ⏱️ LINEA DE TIEMPO DEL MATCH:
            
            0:00 - 0:30: AUTONOMO (30 seg)
            0:30 - 2:30: TELEOP (2 min)
            2:00 - 2:30: ENDGAME (ultimos 30 seg)
            
            Total: 2 minutos 30 segundos
            """
        }
        
        return quick_answers.get(query_type, "Tipo de consulta no reconocido")
    
    def analyze_match_situation(self, situation: Dict) -> str:
        """Analizar situacion de match y dar recomendaciones"""
        time_remaining = situation.get('time_remaining', 0)
        score_diff = situation.get('score_diff', 0)
        robot_status = situation.get('robot_status', 'operational')
        
        if time_remaining > 120:  # TeleOp inicial
            return "🎯 Focus: Ciclos rapidos de scoring. Mantén ritmo constante."
        elif 30 < time_remaining <= 120:  # TeleOp medio
            if score_diff < -20:
                return "⚡ Situacion: Atras en puntos. Aumenta agresividad, busca high baskets."
            elif score_diff > 20:
                return "🛡️ Situacion: Adelante. Juega seguro, evita penalizaciones."
            else:
                return "⚖️ Situacion: Parejo. Mantén estrategia actual."
        else:  # EndGame
            return "🚀 ENDGAME! Preparate para ascent. Level 3 = 30 puntos!"


# Instancia global
quetzal = QuetzalBot()
