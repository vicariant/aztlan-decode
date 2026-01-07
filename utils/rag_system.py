#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QUETZAL-BOT - SISTEMA RAG PARA MANUAL DE REGLAS
==============================================
Chatbot con RAG (Retrieval-Augmented Generation) usando Groq
Responde preguntas sobre el manual de reglas DECODE FTC
"""

import os
from typing import Dict, List, Optional
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class QuetzalBot:
    """Sistema RAG para consultar manual de reglas DECODE"""
    
    def __init__(self):
        """Inicializa el sistema RAG con Groq"""
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.client = None
        self.knowledge_base = self._load_knowledge_base()
        
        if self.groq_api_key:
            try:
                self.client = Groq(api_key=self.groq_api_key)
            except Exception as e:
                print(f"⚠️ Error inicializando Groq: {e}")
    
    def _load_knowledge_base(self) -> str:
        """Carga el conocimiento base del manual DECODE INTO THE DEEP 2025-2026"""
        # Base de conocimiento embebida del manual DECODE INTO THE DEEP
        return """
=== MANUAL DE REGLAS DECODE INTO THE DEEP 2025-2026 ===

OBJETIVO DEL JUEGO:
Los robots compiten en un campo de 12x12 pies, donde deben:
1. Colocar muestras (samples) en canastas (baskets)
2. Colgar especímenes (specimens) en cámaras de alto nivel (high chambers)
3. Trepar en la zona de ascenso (ascent zone) al final del match

PERIODOS:
- Periodo Autónomo: 30 segundos - El robot opera de forma autónoma
- Periodo TeleOp: 2 minutos - Controlado por drivers
- Periodo EndGame: Últimos 30 segundos del TeleOp - Ascenso permitido

ELEMENTOS DE JUEGO:
- Muestras (Samples): Piezas amarillas y azules que se colocan en canastas
- Especímenes (Specimens): Piezas que se cuelgan en cámaras de alto nivel
- Canastas (Baskets): Receptáculos para samples (baja y alta)
- Cámaras (Chambers): Donde se cuelgan specimens (niveles bajo, medio, alto)

PUNTUACIÓN AUTÓNOMO:
- Sample en basket bajo: 4 puntos
- Sample en basket alto: 8 puntos
- Specimen en chamber bajo: 6 puntos
- Specimen en chamber alto: 10 puntos
- Robot estacionado en zona de observación: 3 puntos

PUNTUACIÓN TELEOP:
- Sample en basket bajo: 2 puntos
- Sample en basket alto: 4 puntos
- Specimen en chamber bajo: 4 puntos
- Specimen en chamber alto: 6 puntos

PUNTUACIÓN ENDGAME:
- Nivel 1 (Low Rung): 3 puntos
- Nivel 2 (High Rung): 15 puntos
- Nivel 3 (Colgado completo): 15 puntos adicionales

REGLAS IMPORTANTES:
G14 - Bloquear Zona de Carga: PENALIZACIÓN MAYOR (30 puntos). No puedes bloquear el acceso de tu oponente a su zona de carga por más de 5 segundos.

G16 - Control de Robot: PENALIZACIÓN MAYOR. El robot debe estar bajo control en todo momento. Movimientos agresivos o descontrolados resultan en penalización.

G18 - Contacto con Oponente: PENALIZACIÓN MENOR (10 puntos). Contacto insignificante está permitido, pero contacto que afecte al oponente es penalizado.

G20 - Posesión Limitada: Solo puedes poseer 1 muestra o 1 espécimen a la vez. Poseer múltiples elementos es penalización.

G22 - Zona Restringida: Durante TeleOp, no puedes entrar en la zona submersible del oponente (área de 2x2 pies con specimens precargados).

RANKING POINTS (RP):
- Victoria: 2 RP
- Empate: 1 RP cada equipo
- Derrota: 0 RP
- Bonus RP: Se otorgan por objetivos cumplidos (varían por torneo)

CALIFICACIÓN A WORLDS:
Los equipos califican a campeonato mundial por:
1. Ranking Points (RP) acumulados en regionales
2. Top 2-7 equipos de cada regional (según tamaño del regional)
3. Los equipos con más RP de cada regional avanzan

ESTRATEGIA:
- Maximiza puntos en Autónomo (valen el doble que TeleOp)
- Prioriza chambers altas para specimens (más puntos)
- Planea tu ascenso con anticipación (EndGame es crucial)
- No bloquees zonas de carga del oponente

PENALIZACIONES COMUNES:
- Bloqueo de zona de carga: 30 puntos
- Contacto con oponente: 10-30 puntos según severidad
- Posesión múltiple: 10 puntos
- Robot fuera de control: 30 puntos + posible descalificación
- Entrada a zona restringida: 10 puntos

ZONA DE ASCENSO:
- Solo accesible durante EndGame (últimos 30 segundos)
- 3 niveles de ascenso disponibles
- Ambas alianzas pueden ascender simultáneamente
- El ascenso debe completarse antes del final del match
"""
    
    def query(self, user_question: str, conversation_history: Optional[List[Dict]] = None) -> Dict:
        """
        Consulta el manual usando RAG con Groq
        
        Args:
            user_question: Pregunta del usuario
            conversation_history: Historial de conversación previo
            
        Returns:
            Dict con 'response', 'success', 'sources'
        """
        try:
            if not self.client:
                return {
                    'success': False,
                    'response': '⚠️ Quetzal-Bot requiere configuración de GROQ_API_KEY en .env',
                    'sources': []
                }
            
            # Buscar información relevante en la base de conocimiento
            relevant_context = self._retrieve_relevant_context(user_question)
            
            # Construir prompt para Groq
            system_prompt = f"""Eres Quetzal-Bot, un experto en las reglas del juego FTC DECODE INTO THE DEEP 2025-2026.

CONOCIMIENTO BASE:
{relevant_context}

INSTRUCCIONES:
1. Responde SOLO basándote en el manual oficial
2. Si la pregunta es sobre una regla específica (ej: G14, G16), cita el número
3. Se claro y conciso, usa emojis relevantes
4. Si no sabes algo, admítelo y sugiere consultar el manual completo
5. Para preguntas de estrategia, proporciona consejos prácticos

Responde en español de manera profesional pero amigable."""

            # Preparar mensajes
            messages = [{"role": "system", "content": system_prompt}]
            
            # Agregar historial si existe
            if conversation_history:
                messages.extend(conversation_history[-4:])  # Últimos 4 mensajes
            
            # Agregar pregunta actual
            messages.append({"role": "user", "content": user_question})
            
            # Llamar a Groq
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.3,  # Baja temperatura para respuestas precisas
                max_tokens=500,
                top_p=1,
                stream=False
            )
            
            answer = response.choices[0].message.content
            
            return {
                'success': True,
                'response': answer,
                'sources': ['Manual DECODE INTO THE DEEP 2025-2026'],
                'model': 'Llama 3.3 70B'
            }
            
        except Exception as e:
            return {
                'success': False,
                'response': f'❌ Error procesando pregunta: {str(e)}',
                'sources': []
            }
    
    def _retrieve_relevant_context(self, query: str) -> str:
        """Recupera contexto relevante de la base de conocimiento"""
        # Búsqueda simple por keywords (en producción usar embeddings)
        query_lower = query.lower()
        
        # Mapeo de keywords a secciones relevantes
        relevant_sections = []
        
        # Detectar sección relevante
        if any(word in query_lower for word in ['puntos', 'score', 'puntua', 'cuanto vale']):
            relevant_sections.append('PUNTUACIÓN')
        
        if any(word in query_lower for word in ['regla', 'g14', 'g16', 'g18', 'g20', 'g22', 'penaliza']):
            relevant_sections.append('REGLAS IMPORTANTES')
            relevant_sections.append('PENALIZACIONES')
        
        if any(word in query_lower for word in ['autonomo', 'auto', 'autónomo']):
            relevant_sections.append('PERIODO')
            relevant_sections.append('AUTÓNOMO')
        
        if any(word in query_lower for word in ['endgame', 'ascen', 'trepar', 'colgar']):
            relevant_sections.append('ENDGAME')
            relevant_sections.append('ZONA DE ASCENSO')
        
        if any(word in query_lower for word in ['worlds', 'nacional', 'califica', 'ranking point', 'rp']):
            relevant_sections.append('CALIFICACIÓN')
            relevant_sections.append('RANKING POINTS')
        
        if any(word in query_lower for word in ['estrategia', 'consejo', 'tip', 'como']):
            relevant_sections.append('ESTRATEGIA')
        
        # Si hay secciones relevantes, filtrar conocimiento
        if relevant_sections:
            filtered_knowledge = []
            for line in self.knowledge_base.split('\n'):
                if any(section.upper() in line.upper() for section in relevant_sections):
                    # Incluir esta línea y las siguientes hasta la siguiente sección
                    filtered_knowledge.append(line)
            
            if filtered_knowledge:
                return '\n'.join(filtered_knowledge)
        
        # Si no se encontraron secciones específicas, devolver todo
        return self.knowledge_base
    
    def get_suggested_questions(self) -> List[str]:
        """Devuelve preguntas sugeridas para el usuario"""
        return [
            "¿Cuántos puntos vale un specimen en chamber alto?",
            "¿Es penalización bloquear la zona de carga?",
            "¿Cómo se califican equipos para Worlds?",
            "¿Qué es la regla G14?",
            "¿Cuántos puntos da el ascenso en EndGame?",
            "¿Puedo poseer múltiples samples?",
            "¿Cuánto dura el periodo autónomo?",
            "¿Cuál es la mejor estrategia para maximizar puntos?"
        ]

# Instancia global
quetzal_bot = QuetzalBot()
