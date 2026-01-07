# -*- coding: utf-8 -*-
"""
TESTS AUTOMATIZADOS - AZTLÁN DECODE
"""

import pytest
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.models import init_db, Base
from database.db_operations import DatabaseManager
from utils.report_exporter import ReportExporter
import tempfile

# =====================================================
# FIXTURES
# =====================================================

@pytest.fixture
def temp_db():
    """Crea una base de datos temporal para tests"""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_path = temp_file.name
    temp_file.close()
    
    engine, Session = init_db(temp_path)
    
    yield temp_path
    
    # Cleanup
    try:
        os.unlink(temp_path)
    except:
        pass

@pytest.fixture
def db_manager(temp_db):
    """Crea un DatabaseManager con DB temporal"""
    return DatabaseManager(temp_db)

@pytest.fixture
def report_exporter():
    """Crea un ReportExporter"""
    return ReportExporter()

@pytest.fixture
def sample_team_data():
    """Datos de ejemplo de un equipo"""
    return {
        'team_number': 28254,
        'team_name': 'Aztlán Decode',
        'city': 'Mexico City',
        'state': 'CDMX',
        'country': 'Mexico',
        'ranking': 5,
        'opr': 125.5,
        'win_rate': 85.5,
        'matches_played': 20,
        'ai_analysis': 'Equipo muy competitivo con excelente desempeño en autónomo.',
        'recommendations': 'Enfocarse en mejorar la recolección de elementos.',
        'consensus': 'Consenso de 3 fuentes: equipo tier 1'
    }

# =====================================================
# TESTS DE BASE DE DATOS
# =====================================================

class TestDatabaseOperations:
    """Tests para operaciones de base de datos"""
    
    def test_save_team_search(self, db_manager):
        """Test guardar búsqueda de equipo"""
        result = db_manager.save_team_search(28254, 'scouting', '127.0.0.1')
        assert result == True
        
        history = db_manager.get_search_history(limit=10)
        assert len(history) == 1
        assert history[0]['team_number'] == 28254
    
    def test_get_most_searched_teams(self, db_manager):
        """Test obtener equipos más buscados"""
        # Guardar múltiples búsquedas
        db_manager.save_team_search(28254, 'scouting')
        db_manager.save_team_search(28254, 'scouting')
        db_manager.save_team_search(16418, 'scouting')
        
        most_searched = db_manager.get_most_searched_teams(limit=5)
        assert len(most_searched) > 0
        assert most_searched[0]['team'] == 28254
        assert most_searched[0]['searches'] == 2
    
    def test_save_and_get_team_analysis(self, db_manager, sample_team_data):
        """Test guardar y obtener análisis"""
        result = db_manager.save_team_analysis(28254, sample_team_data)
        assert result == True
        
        analysis = db_manager.get_team_analysis(28254)
        assert analysis is not None
        assert analysis['team_number'] == 28254
        assert analysis['team_name'] == 'Aztlán Decode'
        assert analysis['opr'] == 125.5
    
    def test_api_cache(self, db_manager):
        """Test cache de APIs"""
        api_name = 'test_api'
        params = {'team': 28254, 'season': 2024}
        response_data = {'data': 'test data', 'status': 'success'}
        
        # Guardar en cache
        result = db_manager.save_to_cache(api_name, params, response_data, cache_hours=1)
        assert result == True
        
        # Obtener de cache
        cached = db_manager.get_cached_response(api_name, params, max_age_hours=2)
        assert cached is not None
        assert cached['data'] == 'test data'
    
    def test_favorites(self, db_manager):
        """Test sistema de favoritos"""
        user_ip = '127.0.0.1'
        team_number = 28254
        
        # Agregar favorito
        result = db_manager.add_favorite(user_ip, team_number, 'Equipo excelente')
        assert result == True
        
        # Obtener favoritos
        favorites = db_manager.get_favorites(user_ip)
        assert len(favorites) == 1
        assert favorites[0]['team_number'] == team_number
        
        # Eliminar favorito
        result = db_manager.remove_favorite(user_ip, team_number)
        assert result == True
        
        favorites = db_manager.get_favorites(user_ip)
        assert len(favorites) == 0
    
    def test_global_stats(self, db_manager):
        """Test estadísticas globales"""
        # Crear algunos datos
        db_manager.save_team_search(28254, 'scouting')
        db_manager.save_team_search(16418, 'comparison')
        
        stats = db_manager.get_stats()
        assert stats['total_searches'] >= 2
        assert 'total_analyses' in stats
        assert 'cached_items' in stats

# =====================================================
# TESTS DE EXPORTACIÓN
# =====================================================

class TestReportExporter:
    """Tests para exportación de reportes"""
    
    def test_export_team_analysis_pdf(self, report_exporter, sample_team_data):
        """Test exportar análisis a PDF"""
        pdf_buffer = report_exporter.export_team_analysis_pdf(sample_team_data)
        assert pdf_buffer is not None
        assert pdf_buffer.tell() > 0  # Tiene contenido
    
    def test_export_team_analysis_csv(self, report_exporter, sample_team_data):
        """Test exportar análisis a CSV"""
        csv_string = report_exporter.export_team_analysis_csv(sample_team_data)
        assert csv_string is not None
        assert 'team_number' in csv_string
        assert '28254' in csv_string
    
    def test_export_comparison_pdf(self, report_exporter, sample_team_data):
        """Test exportar comparación a PDF"""
        team1_data = sample_team_data.copy()
        team2_data = sample_team_data.copy()
        team2_data['team_number'] = 16418
        team2_data['team_name'] = 'Otro Equipo'
        
        comparison_data = {
            'ai_analysis': 'El equipo 28254 tiene ventaja en autónomo.'
        }
        
        pdf_buffer = report_exporter.export_comparison_pdf(
            team1_data, team2_data, comparison_data
        )
        assert pdf_buffer is not None
        assert pdf_buffer.tell() > 0
    
    def test_export_multiple_teams_csv(self, report_exporter):
        """Test exportar múltiples equipos a CSV"""
        teams_data = [
            {'team_number': 28254, 'team_name': 'Aztlán', 'opr': 125.5},
            {'team_number': 16418, 'team_name': 'Other', 'opr': 115.0}
        ]
        
        csv_string = report_exporter.export_multiple_teams_csv(teams_data)
        assert csv_string is not None
        assert '28254' in csv_string
        assert '16418' in csv_string

# =====================================================
# TESTS DE UTILIDADES
# =====================================================

class TestUtilities:
    """Tests para funciones de utilidad"""
    
    def test_import_modules(self):
        """Test que todos los módulos se importen correctamente"""
        try:
            from database import models, db_operations
            from utils import report_exporter
            assert True
        except ImportError as e:
            pytest.fail(f"Error importando módulos: {e}")
    
    def test_database_models_exist(self):
        """Test que los modelos de DB existan"""
        from database.models import (
            TeamSearch, TeamAnalysis, ExoplanetSimulation,
            APICache, UserFavorite, MatchPrediction
        )
        assert TeamSearch is not None
        assert TeamAnalysis is not None
        assert ExoplanetSimulation is not None
    
    def test_db_manager_methods_exist(self):
        """Test que DatabaseManager tenga todos los métodos necesarios"""
        from database.db_operations import DatabaseManager
        
        required_methods = [
            'save_team_search', 'get_search_history',
            'save_team_analysis', 'get_team_analysis',
            'get_cached_response', 'save_to_cache',
            'add_favorite', 'get_favorites', 'remove_favorite',
            'get_stats'
        ]
        
        for method in required_methods:
            assert hasattr(DatabaseManager, method), f"Falta método: {method}"

# =====================================================
# TESTS DE INTEGRACIÓN
# =====================================================

class TestIntegration:
    """Tests de integración de múltiples componentes"""
    
    def test_full_workflow(self, db_manager, report_exporter, sample_team_data):
        """Test flujo completo: buscar, analizar, exportar"""
        # 1. Guardar búsqueda
        db_manager.save_team_search(28254, 'scouting', '127.0.0.1')
        
        # 2. Guardar análisis
        db_manager.save_team_analysis(28254, sample_team_data)
        
        # 3. Obtener análisis
        analysis = db_manager.get_team_analysis(28254)
        assert analysis is not None
        
        # 4. Exportar a PDF
        pdf = report_exporter.export_team_analysis_pdf(analysis)
        assert pdf is not None
        
        # 5. Exportar a CSV
        csv = report_exporter.export_team_analysis_csv(analysis)
        assert csv is not None
        
        # 6. Verificar estadísticas
        stats = db_manager.get_stats()
        assert stats['total_searches'] > 0
        assert stats['total_analyses'] > 0

# =====================================================
# EJECUCIÓN DE TESTS
# =====================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
