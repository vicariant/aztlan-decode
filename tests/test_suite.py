#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AZTLÁN DECODE - TESTS AUTOMATIZADOS
Suite completa de tests unitarios y de integración
"""

import unittest
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager
from compliance.minor_protection import MinorProtectionSystem
from models.ftc_analytics import FTCAnalyzer
from datetime import datetime

class TestDatabaseManager(unittest.TestCase):
    """Tests para el gestor de base de datos"""
    
    def setUp(self):
        """Configurar base de datos de prueba"""
        self.db = DatabaseManager('database/test_aztlan.db')
    
    def tearDown(self):
        """Limpiar después de cada test"""
        if os.path.exists('database/test_aztlan.db'):
            os.remove('database/test_aztlan.db')
    
    def test_create_user(self):
        """Test: Crear usuario"""
        user_id = self.db.create_user(
            username='test_user',
            email='test@example.com',
            password='SecurePass123!',
            birth_date='2010-01-01'
        )
        self.assertIsNotNone(user_id)
        self.assertGreater(user_id, 0)
    
    def test_create_minor_user(self):
        """Test: Crear usuario menor de edad"""
        user_id = self.db.create_user(
            username='minor_user',
            email='minor@example.com',
            password='SecurePass123!',
            birth_date='2015-01-01',
            parent_email='parent@example.com'
        )
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT is_minor FROM users WHERE id = ?', (user_id,))
            is_minor = cursor.fetchone()['is_minor']
            self.assertTrue(is_minor)
    
    def test_authenticate_user(self):
        """Test: Autenticar usuario"""
        # Crear usuario
        self.db.create_user(
            username='auth_test',
            email='auth@example.com',
            password='TestPass123!',
            birth_date='2000-01-01'
        )
        
        # Autenticar
        session = self.db.authenticate_user('auth@example.com', 'TestPass123!')
        self.assertIsNotNone(session)
        self.assertIn('session_token', session)
    
    def test_search_history(self):
        """Test: Historial de búsquedas"""
        user_id = self.db.create_user('searcher', 'search@example.com', 'Pass123!', '2000-01-01')
        
        # Agregar búsquedas
        self.db.add_search_history(user_id, 'team', '16818', {'score': 100})
        self.db.add_search_history(user_id, 'team', '6584', {'score': 95})
        
        # Obtener historial
        history = self.db.get_search_history(user_id)
        self.assertEqual(len(history), 2)
    
    def test_api_cache(self):
        """Test: Cache de APIs"""
        # Guardar en cache
        self.db.cache_api_data('team_16818', {'name': 'Aztlán', 'score': 100}, ttl_hours=1)
        
        # Recuperar de cache
        cached = self.db.get_cached_api_data('team_16818')
        self.assertIsNotNone(cached)
        self.assertEqual(cached['score'], 100)

class TestMinorProtection(unittest.TestCase):
    """Tests para protección de menores"""
    
    def setUp(self):
        self.protection = MinorProtectionSystem(jurisdiction='california')
    
    def test_age_verification(self):
        """Test: Verificación de edad"""
        result = self.protection.verify_age('2015-01-01', method='date_input')
        self.assertTrue(result['is_minor'])
        self.assertLess(result['age'], 18)
    
    def test_privacy_settings_minor(self):
        """Test: Configuración de privacidad para menores"""
        settings = self.protection.get_default_privacy_settings(is_minor=True)
        self.assertEqual(settings['profile_visibility'], 'private')
        self.assertFalse(settings['location_tracking'])
        self.assertFalse(settings['targeted_advertising'])
    
    def test_privacy_settings_adult(self):
        """Test: Configuración de privacidad para adultos"""
        settings = self.protection.get_default_privacy_settings(is_minor=False)
        self.assertEqual(settings['profile_visibility'], 'friends')
        self.assertTrue(settings['video_audio_enabled'])
    
    def test_data_collection_validation(self):
        """Test: Validación de recopilación de datos"""
        validation = self.protection.validate_data_collection(
            data_fields=['team_number', 'user_id', 'physical_address'],
            purpose='scouting'
        )
        self.assertFalse(validation['approved'])
        self.assertIn('physical_address', validation['prohibited'])
    
    def test_consent_requirements(self):
        """Test: Requisitos de consentimiento"""
        # Menor de 13 años (COPPA)
        consent = self.protection.check_consent_requirements(user_age=10)
        self.assertTrue(consent['required'])
        self.assertEqual(consent['type'], 'parental_consent')
        
        # Mayor de 18
        consent = self.protection.check_consent_requirements(user_age=20)
        self.assertFalse(consent['required'])
    
    def test_algorithm_evaluation(self):
        """Test: Evaluación de algoritmos"""
        evaluation = self.protection.evaluate_algorithm_impact(
            algorithm_name='content_recommender',
            features=['infinite_scroll', 'auto_play'],
            outcomes=['increased_screen_time']
        )
        self.assertEqual(evaluation['risk_level'], 'high')
        self.assertFalse(evaluation['approved_for_minors'])

class TestFTCAnalytics(unittest.TestCase):
    """Tests para análisis FTC"""
    
    def setUp(self):
        self.analyzer = FTCAnalyzer()
    
    def test_analyze_team_structure(self):
        """Test: Estructura del análisis de equipo"""
        team_data = {
            'team_number': '16818',
            'wins': 10,
            'losses': 0,
            'ties': 0,
            'ranking_points': 88,
            'opr': 180,
            'high_score': 250,
            'worlds_qualified': True
        }
        
        analysis = self.analyzer.analyze_team_performance(team_data)
        
        # Verificar campos obligatorios
        self.assertIn('global_score', analysis)
        self.assertIn('future_score', analysis)
        self.assertIn('momentum', analysis)
        self.assertIn('category', analysis)
        self.assertIn('strengths', analysis)
        self.assertIn('weaknesses', analysis)
    
    def test_high_performance_team(self):
        """Test: Equipo de alto rendimiento"""
        team_data = {
            'wins': 15,
            'losses': 0,
            'ranking_points': 95,
            'opr': 250,
            'high_score': 300,
            'worlds_qualified': True
        }
        
        analysis = self.analyzer.analyze_team_performance(team_data)
        self.assertGreater(analysis['global_score'], 90)
        self.assertGreater(len(analysis['strengths']), 3)
    
    def test_compare_teams(self):
        """Test: Comparación de equipos"""
        team1 = {'wins': 10, 'losses': 5, 'opr': 180}
        team2 = {'wins': 5, 'losses': 10, 'opr': 120}
        
        analysis1 = self.analyzer.analyze_team_performance(team1)
        analysis2 = self.analyzer.analyze_team_performance(team2)
        
        comparison = self.analyzer.compare_teams(analysis1, analysis2)
        
        self.assertIn('team1', comparison)
        self.assertIn('team2', comparison)
        self.assertIn('winner', comparison)

def run_all_tests():
    """Ejecutar todos los tests"""
    print("\n" + "="*70)
    print("🧪 AZTLÁN DECODE - SUITE DE TESTS AUTOMATIZADOS")
    print("="*70 + "\n")
    
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar tests
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseManager))
    suite.addTests(loader.loadTestsFromTestCase(TestMinorProtection))
    suite.addTests(loader.loadTestsFromTestCase(TestFTCAnalytics))
    
    # Ejecutar tests con verbose
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\n" + "="*70)
    print(f"✅ Tests exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Tests fallidos: {len(result.failures)}")
    print(f"💥 Errores: {len(result.errors)}")
    print(f"📊 Cobertura: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("="*70 + "\n")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
