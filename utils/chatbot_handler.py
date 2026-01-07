#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHATBOT HANDLER CON GROQ AI
Sistema de asistencia inteligente para Aztlán Decode
"""

import os
import logging
import re
import requests
from typing import Dict, Optional, List
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class AztlanChatbot:
    """Chatbot inteligente con Groq AI para asistencia en FTC y AstronomIA"""
    
    def __init__(self):
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.client = None
        self.context_history = []
        self.max_history = 10
        
        # System prompt para el chatbot
        self.system_prompt = """Eres AZTLÁN AI, un asistente experto con ACCESO REAL a:
1. Base de datos FTC en tiempo real (TOA, FTC Scout) - puedes consultar cualquier equipo
2. NASA Exoplanet Archive - datos astronómicos actualizados
3. Sistema TRIDENTE para validación de datos

Capacidades:
- Buscar equipos FTC específicos (ej: "equipo 16418")
- Consultar exoplanetas en NASA Archive
- Interpretar estadísticas WLT, OPR, rankings
- Explicar conceptos técnicos

Cuando el usuario mencione un número de equipo FTC (ej: 254, 16418, 28254), automáticamente buscarás sus datos reales.
Cuando pregunten sobre exoplanetas específicos, consultarás NASA Archive.

Respuestas concisas (3-4 líneas) con datos reales cuando sea posible."""
        
        self._initialize_groq()
    
    def _extract_team_number(self, message: str) -> Optional[int]:
        """Extrae número de equipo del mensaje (ej: 'equipo 16418', 'team 254', '#28254')"""
        patterns = [
            r'equipo\s+(\d+)',
            r'team\s+(\d+)',
            r'#(\d+)',
            r'\b(\d{4,5})\b'  # Número de 4-5 dígitos
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message.lower())
            if match:
                team_num = int(match.group(1))
                if 1 <= team_num <= 99999:  # Rango válido de equipos FTC
                    return team_num
        return None
    
    def _search_ftc_team(self, team_num: int) -> Optional[Dict]:
        """Busca datos reales de un equipo FTC"""
        try:
            # Importar aquí para evitar circular imports
            from modules.api_manager import trident
            
            logger.info(f"🔍 Chatbot consultando equipo FTC #{team_num}")
            team_data = trident.get_validated_team_data(team_num)
            
            if team_data and team_data.get('identity'):
                return {
                    'found': True,
                    'number': team_num,
                    'name': team_data['identity'].get('team_name', 'N/A'),
                    'location': team_data['identity'].get('location', 'N/A'),
                    'record': team_data['stats'].get('record', 'N/A'),
                    'trust_level': team_data.get('trust_level', 'N/A'),
                    'awards_count': len(team_data.get('awards', [])),
                    'sources': team_data.get('sources_status', {})
                }
            return None
        except Exception as e:
            logger.error(f"❌ Error buscando equipo {team_num}: {e}")
            return None
    
    def _search_nasa_exoplanet(self, planet_name: str) -> Optional[Dict]:
        """Busca exoplaneta en NASA Archive"""
        try:
            query = f"SELECT TOP 5 pl_name, hostname, pl_rade, pl_orbper, sy_dist FROM ps WHERE pl_name LIKE '%{planet_name}%'"
            
            response = requests.get(
                'https://exoplanetarchive.ipac.caltech.edu/TAP/sync',
                params={
                    'request': 'doQuery',
                    'lang': 'ADQL',
                    'format': 'json',
                    'query': query
                },
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    return {
                        'found': True,
                        'results': data[:3]  # Primeros 3 resultados
                    }
            return None
        except Exception as e:
            logger.error(f"❌ Error buscando exoplaneta {planet_name}: {e}")
            return None
    
    def _initialize_groq(self) -> bool:
        """Inicializa el cliente de Groq"""
        try:
            if not self.groq_api_key or self.groq_api_key == '':
                logger.warning("⚠️ GROQ_API_KEY no configurada")
                return False
            
            from groq import Groq
            self.client = Groq(api_key=self.groq_api_key)
            logger.info("🤖 Groq AI inicializado correctamente")
            return True
            
        except ImportError:
            logger.error("❌ Error: Módulo 'groq' no instalado. Ejecuta: pip install groq")
            return False
        except Exception as e:
            logger.error(f"❌ Error inicializando Groq: {str(e)}")
            return False
    
    def chat(self, user_message: str, context: Optional[Dict] = None) -> Dict:
        """
        Procesa un mensaje del usuario y devuelve respuesta
        
        Args:
            user_message: Mensaje del usuario
            context: Contexto adicional (datos de equipo, exoplaneta, etc.)
            
        Returns:
            Dict con 'response', 'success', 'error'
        """
        try:
            if not self.client:
                return {
                    'success': False,
                    'error': 'Chatbot no disponible. Configura GROQ_API_KEY en .env',
                    'response': '⚠️ El chatbot requiere configuración de API. Consulta CONFIGURAR_API_KEYS.md'
                }
            
            # BÚSQUEDA AUTOMÁTICA: Detectar si el usuario pregunta por un equipo FTC
            team_num = self._extract_team_number(user_message)
            real_data_context = ""
            
            if team_num:
                logger.info(f"🔍 Detectado equipo #{team_num} en mensaje")
                team_info = self._search_ftc_team(team_num)
                
                if team_info and team_info.get('found'):
                    # Construir contexto con datos reales
                    toa_status = team_info['sources'].get('toa_api', 'N/A')
                    scout_status = team_info['sources'].get('scout_api', 'N/A')
                    
                    real_data_context = f"""
DATOS REALES del equipo #{team_num} (desde TRIDENT):
- Nombre: {team_info['name']}
- Ubicación: {team_info['location']}
- Récord: {team_info['record']}
- Premios: {team_info['awards_count']}
- Confianza: {team_info['trust_level']}
- Fuentes: TOA={toa_status}, Scout={scout_status}

Usa ESTOS DATOS REALES para responder. No inventes información.
"""
                    logger.info(f"✅ Datos reales encontrados para #{team_num}")
                else:
                    real_data_context = f"No se encontraron datos para el equipo #{team_num}. Puede ser un equipo nuevo o el número es incorrecto."
            
            # Construir contexto adicional si se proporciona
            enhanced_message = user_message
            if real_data_context:
                enhanced_message = f"{real_data_context}\n\nPregunta del usuario: {user_message}"
            elif context:
                context_str = self._format_context(context)
                enhanced_message = f"{context_str}\n\nPregunta del usuario: {user_message}"
            
            # Preparar mensajes para Groq
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # Agregar historial reciente
            for msg in self.context_history[-self.max_history:]:
                messages.append(msg)
            
            # Agregar mensaje actual
            messages.append({"role": "user", "content": enhanced_message})
            
            # Llamar a Groq API
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Modelo rápido y eficiente
                messages=messages,
                temperature=0.7,
                max_tokens=300,  # Respuestas concisas
                top_p=1,
                stream=False
            )
            
            assistant_message = response.choices[0].message.content
            
            # Actualizar historial
            self.context_history.append({"role": "user", "content": user_message})
            self.context_history.append({"role": "assistant", "content": assistant_message})
            
            # Limitar tamaño del historial
            if len(self.context_history) > self.max_history * 2:
                self.context_history = self.context_history[-self.max_history * 2:]
            
            return {
                'success': True,
                'response': assistant_message,
                'model': 'llama-3.3-70b-versatile'
            }
            
        except Exception as e:
            logger.error(f"❌ Error en chatbot: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'response': f'Error procesando mensaje: {str(e)}'
            }
    
    def _format_context(self, context: Dict) -> str:
        """Formatea el contexto para incluir en el prompt"""
        context_parts = []
        
        if 'team_data' in context:
            team = context['team_data']
            context_parts.append(f"Datos del equipo FTC #{team.get('team_number', 'N/A')}: {team.get('team_name', 'N/A')}")
            
        if 'exoplanet_data' in context:
            exo = context['exoplanet_data']
            context_parts.append(f"Análisis de exoplaneta: Radio {exo.get('koi_prad', 'N/A')} R⊕, Periodo {exo.get('koi_period', 'N/A')} días")
        
        if 'stats' in context:
            stats = context['stats']
            context_parts.append(f"Estadísticas: {stats}")
        
        return "Contexto actual:\n" + "\n".join(context_parts) if context_parts else ""
    
    def clear_history(self):
        """Limpia el historial de conversación"""
        self.context_history = []
        logger.info("🧹 Historial del chatbot limpiado")

# Instancia global del chatbot (inicialización lazy)
_chatbot_instance = None

def get_chatbot_response(message: str, context: Optional[Dict] = None) -> Dict:
    """
    Función helper para obtener respuesta del chatbot
    
    Args:
        message: Mensaje del usuario
        context: Contexto opcional (datos de equipo, etc.)
        
    Returns:
        Dict con respuesta del chatbot
    """
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = AztlanChatbot()
    return _chatbot_instance.chat(message, context)

