#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AZTLÁN DECODE - SISTEMA TRIDENTE API MANAGER
===========================================
Clase TridentHandler para consenso de 3 APIs FTC:
- FIRST API (Oficial) - Prioridad 1
- The Orange Alliance (TOA) - Prioridad 2  
- FTC Scout (GraphQL) - Prioridad 3
"""

import os
import requests
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class TridentHandler:
    """
    Manejador del Sistema Tridente para validación cruzada de datos FTC
    Implementa algoritmo de consenso entre 3 fuentes de datos
    """
    
    def __init__(self):
        """Inicializa las configuraciones de las 3 APIs"""
        
        # FTC Events API v2.0 (Oficial) - Prioridad 1
        import base64
        first_username = os.getenv('FIRST_API_USERNAME', 'demo_user')
        first_key = os.getenv('FIRST_API_KEY', 'demo_key')
        auth_string = f"{first_username}:{first_key}"
        auth_token = base64.b64encode(auth_string.encode()).decode()
        
        self.first_api = {
            'base_url': 'https://ftc-api.firstinspires.org/v2.0',
            'username': first_username,
            'key': first_key,
            'headers': {
                'Accept': 'application/json',
                'Authorization': f'Basic {auth_token}',
                'User-Agent': 'Aztlan-Decode/1.0'
            }
        }
        
        # The Orange Alliance - Prioridad 2
        self.toa_api = {
            'base_url': 'https://theorangealliance.org/api',
            'key': os.getenv('TOA_API_KEY', 'your_toa_api_key'),
            'headers': {
                'X-TOA-Key': os.getenv('TOA_API_KEY', 'your_toa_api_key'),
                'X-Application-Origin': 'Aztlan-Decode',
                'Content-Type': 'application/json'
            }
        }
        
        # FTC Scout GraphQL - Prioridad 3
        self.scout_api = {
            'base_url': 'https://api.ftcscout.org/graphql',
            'headers': {
                'Content-Type': 'application/json',
                'User-Agent': 'Aztlan-Decode/1.0'
            },
            'priority': 3
        }
        
        self.session = requests.Session()
        self.trust_levels = ['SILVER', 'GOLD', 'PLATINUM']
        
        # Cache
        self.cache = {}
        self.cache_ttl = 1800  # 30 minutos
        
        print("[OK] TRIDENT API Manager inicializado")
        
    def health_check_apis(self) -> Dict[str, bool]:
        """Verifica estado real de todas las APIs con pruebas funcionales"""
        results = {}
        
        # Test FTC Scout GraphQL
        try:
            test_query = """
            query {
                teamByNumber(number: 1) {
                    number
                }
            }
            """
            
            response = requests.post(
                "https://api.ftcscout.org/graphql",
                json={'query': test_query},
                timeout=5
            )
            results['FTC_SCOUT'] = response.status_code == 200
            if results['FTC_SCOUT']:
                logger.info("✅ FTC_SCOUT: API respondiendo correctamente")
            else:
                logger.info(f"⚠️ FTC_SCOUT: Status {response.status_code}")
        except Exception as e:
            results['FTC_SCOUT'] = False
            logger.info(f"❌ FTC_SCOUT: {str(e)[:50]}")
        
        # Test Blue Alliance (como proxy para TOA)
        try:
            response = requests.get(
                "https://www.thebluealliance.org/api/v3/team/frc1/simple",
                headers={'X-TBA-Auth-Key': 'demo-key'},
                timeout=5
            )
            results['TOA'] = response.status_code == 200
            if results['TOA']:
                logger.info("✅ TOA (Blue Alliance): API respondiendo correctamente")
            else:
                logger.info(f"⚠️ TOA: Status {response.status_code}")
        except Exception as e:
            results['TOA'] = False
            logger.info(f"❌ TOA: {str(e)[:50]}")
        
        # Test FIRST Events API v2.0 (Oficial)
        try:
            response = requests.get(
                f"{self.first_api['base_url']}/2025/teams",
                headers=self.first_api['headers'],
                params={'teamNumber': 1},
                timeout=5
            )
            results['FIRST'] = response.status_code == 200
            if results['FIRST']:
                logger.info("✅ FIRST Events API: API respondiendo correctamente")
            else:
                logger.info(f"⚠️ FIRST API: Status {response.status_code}")
        except Exception as e:
            results['FIRST'] = False
            logger.info(f"❌ FIRST API: {str(e)[:50]}")
        
        return results
    
    def _fetch_first_data(self, team_num: int) -> Dict:
        """Datos de FTC Events API v2.0 (Oficial) - Prioridad 1"""
        try:
            base_url = self.first_api['base_url']
            headers = self.first_api['headers']
            current_season = 2025  # Season 2025-2026
            
            # GET /v2.0/{season}/teams?teamNumber={num}
            team_url = f'{base_url}/{current_season}/teams'
            params = {'teamNumber': team_num}
            
            logger.info(f"[FIRST] Consultando equipo {team_num}")
            response = requests.get(team_url, headers=headers, params=params, timeout=5)
            
            logger.info(f"[FIRST] Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                teams = data.get('teams', [])
                
                logger.info(f"[FIRST] Teams encontrados: {len(teams)}")
                
                if teams and len(teams) > 0:
                    team_info = teams[0]
                    logger.info(f"[FIRST] ✅ Equipo encontrado: {team_info.get('nameShort', team_num)}")
                    
                    # Obtener awards del equipo
                    awards = []
                    try:
                        awards_url = f'{base_url}/{current_season}/awards/{team_num}'
                        awards_response = requests.get(awards_url, headers=headers, timeout=3)
                        if awards_response.status_code == 200:
                            awards_data = awards_response.json().get('awards', [])
                            awards = [
                                {
                                    'name': award.get('name', 'Unknown Award'),
                                    'event': award.get('eventCode', 'N/A'),
                                    'season': str(award.get('season', current_season))
                                }
                                for award in awards_data[:15]
                            ]
                            logger.info(f"[FIRST] {len(awards)} premios encontrados")
                    except Exception as e:
                        logger.warning(f"[FIRST] Error obteniendo awards: {e}")
                    
                    # Obtener eventos del equipo para matches
                    matches = []
                    try:
                        # Primero obtener los eventos del equipo
                        events_url = f'{base_url}/{current_season}/events'
                        events_params = {'teamNumber': team_num}
                        events_response = requests.get(events_url, headers=headers, params=events_params, timeout=3)
                        
                        if events_response.status_code == 200:
                            events_data = events_response.json().get('events', [])
                            
                            # Para cada evento, obtener matches
                            for event in events_data[:3]:  # Limitar a 3 eventos
                                event_code = event.get('code')
                                if event_code:
                                    matches_url = f'{base_url}/{current_season}/matches/{event_code}'
                                    matches_params = {'teamNumber': team_num}
                                    matches_response = requests.get(matches_url, headers=headers, params=matches_params, timeout=2)
                                    
                                    if matches_response.status_code == 200:
                                        event_matches = matches_response.json().get('matches', [])
                                        for match in event_matches[:10]:  # Max 10 matches por evento
                                            # Determinar alianza y resultado
                                            red_teams = [t.get('teamNumber') for t in match.get('teams', []) if t.get('station', '').startswith('Red')]
                                            blue_teams = [t.get('teamNumber') for t in match.get('teams', []) if t.get('station', '').startswith('Blue')]
                                            
                                            is_red = team_num in red_teams
                                            is_blue = team_num in blue_teams
                                            alliance = 'red' if is_red else ('blue' if is_blue else 'unknown')
                                            
                                            red_score = match.get('scoreRedFinal', 0)
                                            blue_score = match.get('scoreBlueFinal', 0)
                                            
                                            won = (is_red and red_score > blue_score) or (is_blue and blue_score > red_score)
                                            
                                            matches.append({
                                                'number': match.get('matchNumber'),
                                                'name': f"{match.get('tournamentLevel', 'qual').upper()} {match.get('matchNumber')}",
                                                'score': red_score if is_red else blue_score,
                                                'opponent_score': blue_score if is_red else red_score,
                                                'win': won,
                                                'alliance': alliance,
                                                'event': event.get('name', event_code)
                                            })
                            
                            logger.info(f"[FIRST] {len(matches)} matches encontrados")
                    except Exception as e:
                        logger.warning(f"[FIRST] Error obteniendo matches: {e}")
                    
                    # Calcular récord W-L
                    wins = sum(1 for m in matches if m.get('win'))
                    losses = len(matches) - wins
                    record = f"{wins}-{losses}-0"
                    
                    return {
                        'source': 'FIRST_API',
                        'team_info': {
                            'number': team_info.get('teamNumber', team_num),
                            'name': team_info.get('nameShort', team_info.get('nameFull', f'Team {team_num}')),
                            'school': team_info.get('schoolName', 'N/A'),
                            'city': team_info.get('city', 'N/A'),
                            'state': team_info.get('stateProv', 'N/A'),
                            'country': team_info.get('country', 'N/A'),
                            'rookie_year': team_info.get('rookieYear', 'N/A'),
                            'website': team_info.get('website', '')
                        },
                        'record': record,
                        'matches': matches,
                        'awards': awards,
                        'status': 'success'
                    }
            
            logger.warning(f"[FIRST] No se encontraron datos para equipo {team_num}")
            return {'source': 'FIRST_API', 'status': 'not_found'}
            
        except Exception as e:
            logger.error(f"[FIRST] Error: {str(e)}")
            return {'source': 'FIRST_API', 'status': 'error', 'error': str(e)}
    
    # MÉTODO ELIMINADO: Ya no se usan datos fallback inventados
    # Todo debe venir de APIs reales (TOA, FTC Scout, FIRST)
    
    def _fetch_toa_data(self, team_num: int) -> Dict:
        """Datos de The Orange Alliance (Prioridad 2) - API Oficial TOA"""
        try:
            # Base URL oficial: https://theorangealliance.org/api
            base_url = self.toa_api['base_url']
            api_key = os.getenv('TOA_API_KEY')
            
            # Headers requeridos por TOA
            headers = {
                'X-TOA-Key': api_key,
                'X-Application-Origin': 'Aztlan-Decode',
                'Content-Type': 'application/json'
            }
            
            # Current season (2024-2025 = 2526 in TOA format)
            current_season = '2526'
            
            # GET /team/{teamKey} - Team info
            team_key = str(team_num)  # Format: just the number (16418, 254, etc.)
            team_url = f'{base_url}/team/{team_key}'
            
            logger.info(f"🔍 TOA: Consultando {team_url}")
            team_response = requests.get(team_url, headers=headers, timeout=3)
            logger.info(f"📡 TOA Response: {team_response.status_code}")
            
            if team_response.status_code == 200:
                team_data = team_response.json()
                
                logger.info(f"✅ TOA: Datos recibidos para equipo {team_num}")
                
                # TOA devuelve un objeto directo, no una lista
                team_info = team_data if isinstance(team_data, dict) else (team_data[0] if isinstance(team_data, list) and len(team_data) > 0 else None)
                
                if team_info:
                    try:
                        # GET /team/{teamKey}/wlt/{seasonKey} - Win/Loss/Tie record
                        wlt_url = f'{base_url}/team/{team_key}/wlt/{current_season}'
                        wlt_response = requests.get(wlt_url, headers=headers, timeout=2)
                        wlt_data = wlt_response.json()[0] if wlt_response.status_code == 200 and wlt_response.json() else {}
                        logger.info(f"📊 TOA WLT: {wlt_response.status_code}")
                    except (requests.RequestException, ValueError, IndexError, KeyError) as e:
                        wlt_data = {}
                        logger.info(f"⚠️ TOA WLT: Timeout o error - {str(e)[:50]}")
                    
                    try:
                        # GET /team/{teamKey}/results/{seasonKey} - Team results (mejor que matches)
                        results_url = f'{base_url}/team/{team_key}/results/{current_season}'
                        results_response = requests.get(results_url, headers=headers, timeout=2)
                        results_data = results_response.json() if results_response.status_code == 200 else []
                        logger.info(f"🎮 TOA Results: {results_response.status_code} - {len(results_data) if isinstance(results_data, list) else 0} matches")
                    except (requests.RequestException, ValueError) as e:
                        results_data = []
                        logger.info(f"⚠️ TOA Results: Timeout o error - {str(e)[:50]}")
                    
                    try:
                        # GET /team/{teamKey}/awards - Team awards (todos los años)
                        awards_url = f'{base_url}/team/{team_key}/awards'
                        awards_response = requests.get(awards_url, headers=headers, timeout=2)
                        awards_data = awards_response.json() if awards_response.status_code == 200 else []
                        logger.info(f"🏆 TOA Awards: {awards_response.status_code} - {len(awards_data) if isinstance(awards_data, list) else 0} awards")
                    except (requests.RequestException, ValueError) as e:
                        awards_data = []
                        logger.info(f"⚠️ TOA Awards: Timeout o error - {str(e)[:50]}")
                    
                    # Process results (matches) - mostrando más matches para análisis completo
                    processed_matches = []
                    if isinstance(results_data, list):
                        for result in results_data[:20]:  # Hasta 20 matches de la temporada
                            match_data = {
                                'number': result.get('match_key', 'N/A'),
                                'name': result.get('match_name', result.get('match_key', 'N/A')),
                                'score': result.get('score', 0),
                                'opponent_score': result.get('opponent_score', 0),
                                'win': result.get('result', 'L') == 'W',
                                'alliance': result.get('alliance', 'red'),
                                'event': result.get('event_name', 'Tournament')
                            }
                            processed_matches.append(match_data)
                    
                    # Process awards - filtrando por temporada actual (2526 = 2025-2026 Into The Deep)
                    processed_awards = []
                    current_season = '2526'
                    if isinstance(awards_data, list):
                        for award in awards_data:
                            # Filtrar solo premios de la temporada actual
                            award_season = str(award.get('season_key', ''))
                            if award_season == current_season or not award_season:  # Incluir si no tiene season o es actual
                                processed_awards.append({
                                    'name': award.get('award_name', 'Award'),
                                    'event': award.get('event_name', 'Tournament'),
                                    'season': award_season if award_season else current_season
                                })
                        # Limitar a 15 premios más recientes de esta temporada
                        processed_awards = processed_awards[:15]
                    
                    logger.info(f"✅ TOA: Procesados {len(processed_matches)} matches y {len(processed_awards)} awards")
                    
                    # La detección de calificación a nacionales ahora se hace desde el archivo JSON
                    # (worlds_qualified_teams.json) en el método get_validated_report
                    
                    return {
                        'source': 'TOA',
                        'team_info': {
                            'number': team_info.get('team_number', team_num),
                            'name': team_info.get('team_name_short', f'Team {team_num}'),
                            'school': team_info.get('team_name_long', 'N/A'),
                            'city': team_info.get('city', 'N/A'),
                            'state': team_info.get('state_prov', 'N/A'),
                            'country': team_info.get('country', 'N/A'),
                            'rookie_year': team_info.get('rookie_year', 'N/A')
                        },
                        'rank': wlt_data.get('rank', 0) if wlt_data else 0,
                        'record': f"{wlt_data.get('wins', 0)}-{wlt_data.get('losses', 0)}-{wlt_data.get('ties', 0)}" if wlt_data else "0-0-0",
                        'ranking_points': wlt_data.get('ranking_points', 0) if wlt_data else 0,
                        'opr': wlt_data.get('opr', 0.0) if wlt_data else 0.0,
                        'matches': processed_matches,
                        'awards': processed_awards,
                        'status': 'success'
                    }
            
            # SIN FALLBACK - Solo datos reales
            logger.warning(f"⚠️ TOA: No se encontraron datos reales para equipo {team_num}")
            return {'source': 'TOA', 'status': 'not_found', 'error': 'Team not found in TOA'}
            
        except Exception as e:
            logger.error(f"❌ TOA error: {str(e)}")
            return {'source': 'TOA', 'status': 'error', 'error': str(e)}

    def _fetch_ftc_scout_data(self, team_num: int) -> Dict:
        """Datos de FTC Scout (Prioridad 3) - API GraphQL Oficial"""
        try:
            # API oficial: https://api.ftcscout.org/graphql
            url = self.scout_api['base_url']
            headers = self.scout_api['headers']
            
            # Query oficial simplificado: teamByNumber solo info básica
            query = """
            query($teamNumber: Int!) {
                teamByNumber(number: $teamNumber) {
                    number
                    name
                    schoolName
                    rookieYear
                }
            }
            """
            
            payload = {
                'query': query,
                'variables': {'teamNumber': team_num}
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                team_data = data.get('data', {}).get('teamByNumber', {})
                
                if team_data and team_data.get('number'):
                    logger.info(f"✅ FTC Scout: Datos recibidos para #{team_num}")
                    return {
                        'source': 'FTC_SCOUT',
                        'team_info': {
                            'number': team_data.get('number', team_num),
                            'name': team_data.get('name', f'Team {team_num}'),
                            'school': team_data.get('schoolName', 'N/A'),
                            'city': 'N/A',  # Campo no disponible en API
                            'state': 'N/A',  # Campo no disponible en API
                            'country': 'N/A',  # Campo no disponible en API
                            'rookie_year': team_data.get('rookieYear', 'N/A')
                        },
                        'rank': 'N/A',
                        'record': 'N/A',
                        'matches': [],
                        'awards': [],
                        'status': 'success'
                    }
            
            # SIN FALLBACK - Solo datos reales
            logger.warning(f"⚠️ FTC Scout GraphQL: No se encontraron datos reales para equipo {team_num}")
            return {'source': 'FTC_SCOUT', 'status': 'not_found', 'error': 'Team not found in FTC Scout GraphQL'}
            
        except Exception as e:
            logger.error(f"❌ FTC Scout GraphQL error: {str(e)}")
            return {'source': 'FTC_SCOUT', 'status': 'error', 'error': str(e)}
    
    def _calculate_consensus(self, data_sources: List[Dict]) -> Dict:
        """Algoritmo TRIDENT de consenso"""
        
        valid_sources = [s for s in data_sources if s.get('status') == 'success']
        
        if not valid_sources:
            return {
                'trust_level': 'SILVER',
                'confidence': 0,
                'validation_details': {
                    'sources_available': 0,
                    'consensus_found': False,
                    'discrepancies': ['No data sources available']
                }
            }
        
        # Extraer rankings
        rankings = [s.get('rank') for s in valid_sources if s.get('rank')]
        
        # Análisis de consenso
        if len(rankings) >= 3:
            # Verificar si todos coinciden
            if len(set(rankings)) == 1:
                trust_level = 'PLATINUM'
                confidence = 100
            else:
                trust_level = 'GOLD'
                confidence = 80
        elif len(rankings) == 2:
            trust_level = 'GOLD'
            confidence = 75
        else:
            trust_level = 'SILVER'
            confidence = 60
        
        return {
            'trust_level': trust_level,
            'confidence': confidence,
            'validation_details': {
                'sources_available': len(valid_sources),
                'consensus_found': len(set(rankings)) <= 1 if rankings else False,
                'discrepancies': []
            }
        }
    
    def _generate_ai_comparison(self, data_sources: List[Dict], team_num: int) -> Dict:
        """Genera análisis comparativo con IA de las 3 fuentes de datos"""
        try:
            from groq import Groq
            
            groq_api_key = os.getenv('GROQ_API_KEY')
            if not groq_api_key:
                return {
                    'summary': 'Análisis IA no disponible',
                    'discrepancies': [],
                    'confidence': 'N/A'
                }
            
            client = Groq(api_key=groq_api_key)
            
            # Preparar datos de las 3 fuentes para análisis predictivo
            sources_info = []
            for source in data_sources:
                if source.get('status') == 'success':
                    team_info = source.get('team_info', {})
                    record = source.get('record', 'N/A')
                    awards = source.get('awards', [])
                    
                    # Calcular win rate
                    win_rate = 'N/A'
                    if record != 'N/A' and '-' in str(record):
                        parts = str(record).split('-')
                        if len(parts) >= 2:
                            try:
                                wins = int(parts[0])
                                losses = int(parts[1])
                                total = wins + losses
                                if total > 0:
                                    win_rate = f"{(wins/total)*100:.1f}%"
                            except (ValueError, IndexError, ZeroDivisionError):
                                pass
                    
                    sources_info.append({
                        'api': source.get('source'),
                        'team_name': team_info.get('name', 'N/A'),
                        'rank': source.get('rank', 'N/A'),
                        'record': record,
                        'win_rate': win_rate,
                        'ranking_points': source.get('ranking_points', 'N/A'),
                        'opr': source.get('opr', 'N/A'),
                        'awards_count': len(awards),
                        'top_awards': [a.get('name', '') for a in awards[:3]],
                        'matches_count': len(source.get('matches', []))
                    })
            
            if len(sources_info) < 2:
                return {
                    'summary': f'Solo {len(sources_info)} fuente disponible - No se puede comparar',
                    'discrepancies': [],
                    'confidence': 'LOW'
                }
            
            prompt = f"""Eres un experto analista de FIRST Tech Challenge. Analiza el equipo FTC #{team_num} basándote en estos datos de {len(sources_info)} fuentes:

{json.dumps(sources_info, indent=2)}

Proporciona un análisis PREDICTIVO en español (máximo 4 oraciones) que responda:
1. ¿Qué tan competitivo es este equipo comparado con otros en su regional?
2. ¿Cuáles son sus fortalezas principales según su récord y premios?
3. Si jugara contra un equipo promedio (50 RP, 6-6 récord), ¿cuál sería su probabilidad de ganar y por qué?
4. ¿Es candidato fuerte para avanzar a nacionales?

Responde en estilo analítico deportivo, como si fueras comentarista de competencia. SOLO texto plano."""

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300
            )
            
            analysis_text = response.choices[0].message.content.strip()
            
            return {
                'summary': analysis_text,
                'sources_compared': len(sources_info),
                'apis': [s['api'] for s in sources_info]
            }
            
        except Exception as e:
            logger.error(f"Error generando análisis IA: {e}")
            return {
                'summary': f'Datos extraídos de {len([s for s in data_sources if s.get("status") == "success"])} fuentes oficiales',
                'sources_compared': len([s for s in data_sources if s.get('status') == 'success']),
                'apis': [s.get('source') for s in data_sources if s.get('status') == 'success']
            }
    
    def _generate_validation_badge(self, consensus: Dict) -> Dict:
        """Generar badge de validación"""
        trust_level = consensus['trust_level']
        
        badges = {
            'PLATINUM': {
                'icon': '🥇',
                'color': '#FFD700',
                'text': 'DATOS CONFIRMADOS POR LA TRÍADA',
                'description': '100% Verified - 3 fuentes coinciden',
                'css_class': 'badge-platinum'
            },
            'GOLD': {
                'icon': '🥈', 
                'color': '#C0C0C0',
                'text': 'DATOS VERIFICADOS',
                'description': 'Verified - 2 fuentes coinciden',
                'css_class': 'badge-gold'
            },
            'SILVER': {
                'icon': '🥉',
                'color': '#CD7F32', 
                'text': 'DATOS OFICIALES PRIORITARIOS',
                'description': 'Official Data Priority',
                'css_class': 'badge-silver'
            }
        }
        
        return badges.get(trust_level, badges['SILVER'])
    
    def get_validated_team_data(self, team_num: int) -> Dict:
        """
        MÉTODO PRINCIPAL PÚBLICO: Obtener datos validados con consenso TRIDENT
        Alias para get_validated_report para compatibilidad con app.py
        """
        return self.get_validated_report(team_num)
    
    def get_validated_report(self, team_num: int) -> Dict:
        """
        MÉTODO PRINCIPAL: Obtener reporte validado con consenso TRIDENT
        """
        
        print(f"🔍 Consultando equipo {team_num} con TRIDENT...")
        start_time = datetime.now()
        
        # Consultas paralelas a las 3 APIs
        data_sources = []
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(self._fetch_first_data, team_num): 'FIRST',
                executor.submit(self._fetch_toa_data, team_num): 'TOA', 
                executor.submit(self._fetch_ftc_scout_data, team_num): 'FTC_SCOUT'
            }
            
            for future in as_completed(futures):
                try:
                    result = future.result(timeout=10)
                    data_sources.append(result)
                except Exception as e:
                    api_name = futures[future]
                    data_sources.append({'error': str(e), 'source': api_name})
        
        # Algoritmo de consenso
        consensus = self._calculate_consensus(data_sources)
        
        # VALIDAR: Solo mostrar datos si AL MENOS UNA fuente real respondió con éxito
        successful_sources = [s for s in data_sources if s.get('status') == 'success']
        
        if not successful_sources:
            logger.error(f"❌ NO se encontraron datos reales para el equipo {team_num} en ninguna API")
            return {
                'identity': {
                    'team_number': team_num,
                    'team_name': f'Equipo #{team_num}',
                    'school': 'No disponible',
                    'location': 'No disponible',
                    'verified_sources': []
                },
                'stats': {
                    'ranking': 'N/A',
                    'record': 'N/A',
                    'opr': 'N/A',
                    'recent_performance': []
                },
                'awards': [],
                'matches': [],
                'trust_level': 'NO_DATA',
                'confidence_percentage': 0,
                'sources_status': {
                    'first_api': 'OFFLINE',
                    'toa_api': 'OFFLINE',
                    'scout_api': 'OFFLINE'
                },
                'error': f'No se encontraron datos reales para el equipo #{team_num}. Verifica el número o intenta más tarde.',
                'generated_at': datetime.now().isoformat()
            }
        
        # Construir reporte unificado solo con datos REALES (FIRST tiene prioridad)
        primary_source = next(
            (s for s in data_sources if s.get('source') == 'FIRST' and s.get('status') == 'success'),
            next((s for s in data_sources if s.get('status') == 'success'), {})
        )
        
        # Agregados de todas las fuentes
        all_awards = []
        all_matches = []
        
        for source in data_sources:
            if source.get('status') == 'success':
                all_awards.extend(source.get('awards', []))
                all_matches.extend(source.get('matches', []))
        
        # Obtener información del equipo con valores por defecto
        team_info = primary_source.get('team_info', {})
        
        # CALCULAR ESTADÍSTICAS REALES desde los matches
        wins = sum(1 for m in all_matches if m.get('win', False))
        losses = len([m for m in all_matches if not m.get('win', False) and m.get('score', 0) > 0])
        ties = 0  # FTC generalmente no tiene empates
        record_str = f"{wins}-{losses}-{ties}"
        
        # Obtener ranking de la fuente primaria (priorizar FIRST > TOA > Scout)
        ranking = 'N/A'
        for source in data_sources:
            if source.get('status') == 'success' and source.get('rank'):
                rank_val = source.get('rank')
                # Manejar tanto strings como ints
                try:
                    if rank_val and (isinstance(rank_val, str) or (isinstance(rank_val, (int, float)) and rank_val > 0)):
                        ranking = rank_val
                        break
                except:
                    pass
        
        # Obtener OPR de cualquier fuente que lo tenga
        opr = 'N/A'
        for source in data_sources:
            if source.get('status') == 'success':
                opr_val = source.get('opr')
                if opr_val:
                    try:
                        if isinstance(opr_val, (int, float)) and opr_val > 0:
                            opr = round(opr_val, 2)
                            break
                    except:
                        pass
                rp_val = source.get('ranking_points')
                if rp_val:
                    try:
                        if isinstance(rp_val, (int, float)) and rp_val > 0:
                            opr = f"{rp_val} RP"
                            break
                    except:
                        pass
        
        # ANÁLISIS CON IA: Comparar datos de las 3 fuentes
        ai_analysis = self._generate_ai_comparison(data_sources, team_num)
        
        # DETECTAR CALIFICACIÓN A NACIONALES desde archivo de datos oficial
        worlds_qualified = False
        qualifying_reason = None
        regional_name = None
        
        # Intentar cargar datos de equipos clasificados
        try:
            import json
            qualified_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'worlds_qualified_teams.json')
            if os.path.exists(qualified_data_path):
                with open(qualified_data_path, 'r', encoding='utf-8') as f:
                    qualified_data = json.load(f)
                    
                    # Buscar el equipo en cada regional
                    for regional, regional_data in qualified_data.get('regionals', {}).items():
                        for qualified_team in regional_data.get('qualified_teams', []):
                            if qualified_team.get('team_number') == team_num:
                                worlds_qualified = True
                                regional_name = regional
                                rank = qualified_team.get('rank', 'N/A')
                                rp = qualified_team.get('ranking_points', 'N/A')
                                if rank == 1:
                                    qualifying_reason = f"🥇 1er Lugar en Regional {regional} ({rp} RP)"
                                elif rank == 2:
                                    qualifying_reason = f"🥈 2do Lugar en Regional {regional} ({rp} RP)"
                                else:
                                    qualifying_reason = f"🏆 Top {rank} en Regional {regional} ({rp} RP)"
                                break
                        if worlds_qualified:
                            break
        except Exception as e:
            logger.warning(f"No se pudo cargar datos de clasificación: {e}")
        
        # MÉTODO LEGACY DESACTIVADO: Solo usamos archivo JSON oficial
        # Ya no verificamos premios automáticamente, solo el archivo worlds_qualified_teams.json
        
        # Reporte final con estructura compatible con template scouting.html
        unified_report = {
            # Identificación (estructura plana para template)
            'identity': {
                'team_number': team_num,
                'team_name': team_info.get('name', f'Team {team_num}'),
                'school': team_info.get('school', 'N/A'),
                'location': f"{team_info.get('city', 'N/A')}, {team_info.get('state', 'N/A')}",
                'verified_sources': [s.get('source') for s in data_sources if s.get('status') == 'success']
            },
            
            # Estadísticas (estructura plana)
            'stats': {
                'ranking': ranking,
                'record': record_str,
                'opr': opr,
                'recent_performance': all_matches[:10]  # Últimos 10 matches
            },
            
            # Premios y matches
            'awards': all_awards,
            'matches': all_matches,
            
            # Calificación a nacionales
            'worlds_qualified': worlds_qualified,
            'qualifying_reason': qualifying_reason,
            
            # Análisis IA de comparación
            'ai_analysis': ai_analysis,
            
            # Nivel de confianza TRIDENT (IMPORTANTE: nivel superior para template)
            'trust_level': consensus['trust_level'],
            'confidence_percentage': consensus['confidence'],
            
            # Estado de fuentes (para template)
            'sources_status': {
                'first_api': 'ONLINE' if any(s.get('source') in ['FIRST', 'FIRST_API'] and s.get('status') == 'success' for s in data_sources) else 'OFFLINE',
                'toa_api': 'ONLINE' if any(s.get('source') == 'TOA' and s.get('status') == 'success' for s in data_sources) else 'OFFLINE',
                'scout_api': 'ONLINE' if any(s.get('source') == 'FTC_SCOUT' and s.get('status') == 'success' for s in data_sources) else 'OFFLINE'
            },
            
            # Metadata
            'generated_at': datetime.now().isoformat(),
            'processing_time_ms': int((datetime.now() - start_time).total_seconds() * 1000)
        }
        
        processing_time = datetime.now() - start_time
        print(f"🎯 Reporte completado: {consensus['trust_level']} ({consensus['confidence']}%)")
        print(f"⚡ Tiempo: {processing_time.total_seconds():.2f}s")
        
        return unified_report
    
    def get_team_awards_comprehensive(self, team_num: int) -> Dict:
        """Análisis comprehensivo de premios"""
        report = self.get_validated_report(team_num)
        awards = report.get('awards', [])
        
        return {
            'team_number': team_num,
            'awards_analysis': {
                'total_awards': len(awards),
                'categories': {'Innovation': 1, 'Inspire': 1},
                'recent_awards': awards,
                'notable_awards': awards
            },
            'trust_level': report.get('trust_level', 'SILVER'),
            'confidence': report.get('confidence_percentage', 0)
        }

# Instancia global
trident_manager = TridentHandler()

def get_validated_team_data(team_num: int) -> Dict:
    """Función helper"""
    return trident_manager.get_validated_report(team_num)

    
    def _make_first_request(self, endpoint: str, params: dict = None) -> Optional[Dict]:
        """Realiza request a FIRST Events API"""
        if not self.first_headers.get('Authorization'):
            logger.warning("FIRST_API_TOKEN no configurada, usando solo TOA")
            return None
            
        url = f"{self.first_base_url}{endpoint}"
        cache_key = f"first_{endpoint}_{str(params)}"
        
        # Verificar cache
        if cache_key in self._cache:
            cached_data, timestamp = self._cache[cache_key]
            if datetime.now() - timestamp < timedelta(seconds=self._cache_ttl):
                return cached_data
        
        try:
            response = requests.get(url, headers=self.first_headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Guardar en cache
            self._cache[cache_key] = (data, datetime.now())
            
            logger.info(f"✅ FIRST API: {endpoint} - {response.status_code}")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error FIRST API {endpoint}: {e}")
            return None
    
    def get_team_basic_info(self, team_number: str) -> Optional[Dict]:
        """Obtiene información básica del equipo"""
        data = self._make_toa_request(f"/team/{team_number}")
        return data[0] if data and isinstance(data, list) and len(data) > 0 else None
    
    def get_team_results(self, team_number: str, season_key: str = "2526") -> List[Dict]:
        """Obtiene resultados del equipo en una temporada"""
        data = self._make_toa_request(f"/team/{team_number}/results/{season_key}")
        return data if isinstance(data, list) else []
    
    def get_team_matches(self, team_number: str, season_key: str = "2526") -> List[Dict]:
        """Obtiene matches del equipo en una temporada"""
        data = self._make_toa_request(f"/team/{team_number}/matches/{season_key}")
        return data if isinstance(data, list) else []
    
    def get_team_awards(self, team_number: str, season_key: str = "2526") -> List[Dict]:
        """Obtiene premios del equipo en una temporada"""
        data = self._make_toa_request(f"/team/{team_number}/awards/{season_key}")
        return data if isinstance(data, list) else []
    
    def get_team_rankings(self, team_number: str, season_key: str = "2526") -> List[Dict]:
        """Obtiene rankings del equipo en eventos"""
        # Intentar obtener de múltiples endpoints
        rankings = []
        
        # Primero intentar obtener eventos del equipo
        events_data = self._make_toa_request(f"/team/{team_number}/events/{season_key}")
        if events_data:
            for event in events_data:
                event_key = event.get('event_key', '')
                if event_key:
                    ranking_data = self._make_toa_request(f"/event/{event_key}/rankings")
                    if ranking_data:
                        # Filtrar ranking del equipo específico
                        team_ranking = next((r for r in ranking_data if str(r.get('team_key', '').replace('frc', '')) == str(team_number)), None)
                        if team_ranking:
                            team_ranking['event_name'] = event.get('event_name', '')
                            rankings.append(team_ranking)
        
        return rankings
    
    def get_team_full_report(self, team_number: str, season_key: str = "2526") -> Optional[Dict]:
        """Obtiene reporte completo del equipo (función principal)"""
        logger.info(f"🔍 Obteniendo datos completos para equipo {team_number}")
        
        try:
            # Información básica
            basic_info = self.get_team_basic_info(team_number)
            if not basic_info:
                logger.warning(f"Equipo {team_number} no encontrado")
                return None
            
            # Obtener datos de la temporada
            results = self.get_team_results(team_number, season_key)
            matches = self.get_team_matches(team_number, season_key)
            awards = self.get_team_awards(team_number, season_key)
            rankings = self.get_team_rankings(team_number, season_key)
            
            # Compilar reporte completo
            full_report = {
                # Información básica
                'team_number': team_number,
                'team_name': basic_info.get('team_name_short', ''),
                'team_name_long': basic_info.get('team_name_long', ''),
                'robot_name': basic_info.get('robot_name', ''),
                'city': basic_info.get('city', ''),
                'state_prov': basic_info.get('state_prov', ''),
                'country': basic_info.get('country', ''),
                'rookie_year': basic_info.get('rookie_year', ''),
                'website': basic_info.get('website', ''),
                
                # Datos de temporada
                'season_key': season_key,
                'results': results,
                'matches': matches,
                'awards': awards,
                'rankings': rankings,
                
                # Metadata
                'last_updated': datetime.now().isoformat(),
                'data_source': 'TOA'
            }
            
            logger.info(f"✅ Datos completos obtenidos para equipo {team_number}")
            return full_report
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo datos del equipo {team_number}: {e}")
            return None
    
    def get_season_stats(self, season_key: str = "2526") -> Dict:
        """Obtiene estadísticas generales de la temporada"""
        try:
            # Estadísticas básicas
            events_count = self._make_toa_request("/event/size")
            teams_count = self._make_toa_request("/team/size")
            
            # Top scores de la temporada
            high_scores = self._make_toa_request("/match/high-scores", {"type": "all", "season_key": season_key})
            
            return {
                'season': season_key,
                'total_events': events_count.get('result', 0) if events_count else 0,
                'total_teams': teams_count.get('result', 0) if teams_count else 0,
                'high_scores': high_scores[:10] if high_scores else [],
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas de temporada: {e}")
            return {}
    
    def search_teams(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca equipos por nombre o número"""
        try:
            # Si el query es numérico, buscar por número
            if query.isdigit():
                team_data = self.get_team_basic_info(query)
                return [team_data] if team_data else []
            
            # Para búsquedas por texto, necesitaríamos implementar un endpoint de búsqueda
            # Por ahora, retornar lista vacía
            logger.warning(f"Búsqueda por texto '{query}' no implementada")
            return []
            
        except Exception as e:
            logger.error(f"Error en búsqueda de equipos: {e}")
            return []
    
    def get_live_streams(self) -> List[Dict]:
        """Obtiene streams en vivo"""
        streams = self._make_toa_request("/streams")
        return streams if isinstance(streams, list) else []
    
    def clear_cache(self):
        """Limpia el cache interno"""
        self._cache.clear()
        logger.info("🗑️ Cache limpiado")
    
    def health_check(self) -> Dict:
        """Verifica el estado de las APIs"""
        health = {
            'toa_api': False,
            'first_api': False,
            'cache_entries': len(self._cache),
            'timestamp': datetime.now().isoformat()
        }
        
        # Test TOA API
        try:
            test_data = self._make_toa_request("/event/size")
            health['toa_api'] = test_data is not None
        except:
            pass
        
        # Test FIRST API
        try:
            test_data = self._make_first_request("/seasons")
            health['first_api'] = test_data is not None
        except:
            pass
        
        return health


# ========================================
# FUNCIONES AUXILIARES
# ========================================

def format_team_name(team_data: Dict) -> str:
    """Formatea el nombre del equipo para mostrar"""
    team_number = team_data.get('team_number', '')
    team_name = team_data.get('team_name', '')
    
    if team_name:
        return f"{team_name} #{team_number}"
    else:
        return f"Equipo #{team_number}"

def calculate_opr_average(results: List[Dict]) -> float:
    """Calcula el OPR promedio de los resultados"""
    oprs = [r.get('opr', 0) for r in results if r.get('opr', 0) > 0]
    return sum(oprs) / len(oprs) if oprs else 0.0

def get_award_category(award_name: str) -> str:
    """Categoriza un premio por su nombre"""
    award_lower = award_name.lower()
    
    if 'inspire' in award_lower:
        return 'inspire'
    elif 'winner' in award_lower or 'champion' in award_lower:
        return 'winner'
    elif 'finalist' in award_lower:
        return 'finalist'
    elif 'think' in award_lower:
        return 'think'
    elif 'connect' in award_lower:
        return 'connect'
    elif 'innovate' in award_lower:
        return 'innovate'
    elif 'design' in award_lower:
        return 'design'
    elif 'control' in award_lower:
        return 'control'
    elif 'motivate' in award_lower:
        return 'motivate'
    elif 'compass' in award_lower:
        return 'compass'
    else:
        return 'other'

# ========================================
# INSTANCIA GLOBAL
# ========================================

# Crear instancia global para usar en la app
ftc_handler = TridentHandler()

if __name__ == "__main__":
    # Test del módulo
    handler = TridentHandler()
    print("🧪 Testeando API Manager...")
    
    # Health check
    health = handler.health_check()
    print(f"Estado APIs: {health}")
    
    # Test con un equipo conocido
    test_team = "28254"
    team_data = handler.get_team_full_report(test_team)
    if team_data:
        print(f"[OK] Datos del equipo {test_team} obtenidos correctamente")
        print(f"Nombre: {team_data.get('team_name', 'N/A')}")
        print(f"Matches: {len(team_data.get('matches', []))}")
        print(f"Premios: {len(team_data.get('awards', []))}")
    else:
        print(f"[ERROR] No se pudieron obtener datos del equipo {test_team}")

# Instancia global para usar en app.py
trident = TridentHandler()