#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test rápido de la IA ultra potente"""

from models.ftc_analytics import FTCAnalyzer
from models.advanced_ai import TrendAnalyzer, AdvancedPredictor

print("\n" + "="*50)
print("  VERIFICACIÓN DE IA ULTRA POTENTE")
print("="*50 + "\n")

try:
    # 1. Importar módulos
    print("✓ Módulos importados correctamente")
    
    # 2. Crear analizador
    analyzer = FTCAnalyzer()
    print("✓ FTCAnalyzer creado correctamente")
    
    # 3. Datos de prueba
    test_data = {
        'wins': 10,
        'losses': 0,
        'ties': 0,
        'ranking_points': 88,
        'opr': 180,
        'high_score': 250,
        'worlds_qualified': True
    }
    
    # 4. Analizar equipo
    result = analyzer.analyze_team_performance(test_data)
    print("✓ Análisis completado exitosamente\n")
    
    # 5. Mostrar resultados
    print("📊 RESULTADOS DEL ANÁLISIS:")
    print(f"   Score Global: {result['global_score']}/100")
    print(f"   Score Futuro: {result['future_score']}/100")
    print(f"   Categoría: {result['category']}")
    print(f"   Momentum: {result['momentum_desc']}")
    print(f"   Fortalezas: {len(result['strengths'])} encontradas")
    print(f"   Ventajas Estratégicas: {len(result.get('strategic_advantages', []))}")
    
    print("\n" + "="*50)
    print("  ✅ LA IA FUNCIONA PERFECTAMENTE!")
    print("="*50 + "\n")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}\n")
    import traceback
    traceback.print_exc()
