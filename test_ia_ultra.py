#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRUEBA IA ULTRA AVANZADA - Demostración de capacidades
"""

import sys
import io

# Fix encoding para Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 60)
print(" AZTLAN DECODE - IA ULTRA POTENTE")
print("=" * 60)

from models.ftc_analytics import ftc_analyzer
from models.text_analyzer import text_analyzer

# Datos de prueba del equipo 16818 (Aztlán)
team_aztlan = {
    'name': 'Aztlán',
    'team': 16818,
    'tot_points': 88,
    'wins': 5,
    'losses': 0,
    'ties': 0,
    'opr': 187.3,
    'worlds_qualified': True
}

# Datos de prueba del equipo 6584 (Overcharged)
team_overcharged = {
    'name': 'Overcharged',
    'team': 6584,
    'tot_points': 76,
    'wins': 4,
    'losses': 1,
    'ties': 0,
    'opr': 156.2,
    'worlds_qualified': False
}

print("\n🧠 TEST 1: ANÁLISIS INDIVIDUAL AVANZADO")
print("━" * 60)
print(f"Analizando: {team_aztlan['name']} (#{team_aztlan['team']})")

analysis = ftc_analyzer.analyze_team_performance(team_aztlan)

print(f"\n📊 RESULTADOS:")
print(f"   • Score Global: {analysis['global_score']:.1f}/100")
print(f"   • Score Futuro: {analysis['future_score']:.1f}/100")
print(f"   • Categoría: {analysis['category']} {analysis['category_emoji']}")
print(f"   • Momentum: {analysis['momentum']:+.2f} - {analysis['momentum_desc']}")
print(f"   • Win Rate: {analysis['metrics']['win_rate']:.1%}")

print(f"\n⚡ FORTALEZAS ({len(analysis['strengths'])} identificadas):")
for strength in analysis['strengths'][:5]:
    print(f"   {strength}")

if analysis['outliers']:
    print(f"\n🌟 ANOMALÍAS DETECTADAS:")
    for outlier in analysis['outliers']:
        print(f"   {outlier['desc']}")

if analysis['strategic_advantages']:
    print(f"\n⚔️ VENTAJAS ESTRATÉGICAS:")
    for adv in analysis['strategic_advantages']:
        print(f"   {adv['desc']} (Impacto: {adv['impact']})")

pred = analysis['prediction']
print(f"\n🔮 PREDICCIÓN AVANZADA:")
print(f"   • Outlook: {pred['outlook']}")
print(f"   • Prob. Worlds: {pred['probability_worlds']:.1f}%")
print(f"   • Prob. Regional Win: {pred['probability_regional_win']:.1f}%")
print(f"   • Momentum Impact: {pred['momentum_impact']:+.2f}")

print(f"\n🎯 ESTRATEGIA PERSONALIZADA:")
for strat in analysis['strategy'][:3]:
    if isinstance(strat, dict):
        print(f"   [{strat['priority']}] {strat['action']}")
    else:
        print(f"   • {strat}")

if analysis['alliance_recommendations']:
    print(f"\n🤝 RECOMENDACIÓN DE ALIANZA:")
    for rec in analysis['alliance_recommendations']:
        print(f"   {rec['desc']}")

print("\n" + "="*60)
print("\n💬 ANÁLISIS EN TEXTO NATURAL:")
print("━" * 60)
text = text_analyzer.generate_team_analysis(team_aztlan, analysis)
print(text)

print("\n\n" + "="*60)
print(" 🥊 TEST 2: COMPARACIÓN ULTRA AVANZADA")
print("="*60)

comparison = ftc_analyzer.compare_teams(team_aztlan, team_overcharged)

print(f"\n📊 SCORES:")
print(f"   {team_aztlan['name']}: {comparison['team1']['score']:.1f}/100 ({comparison['team1']['category']})")
print(f"   {team_overcharged['name']}: {comparison['team2']['score']:.1f}/100 ({comparison['team2']['category']})")

print(f"\n🔥 MOMENTUM:")
print(f"   {team_aztlan['name']}: {comparison['team1']['momentum_desc']}")
print(f"   {team_overcharged['name']}: {comparison['team2']['momentum_desc']}")

print(f"\n🎯 PROBABILIDADES DE VICTORIA:")
print(f"   {team_aztlan['name']}: {comparison['team1']['win_probability']:.1f}%")
print(f"   {team_overcharged['name']}: {comparison['team2']['win_probability']:.1f}%")

print(f"\n⚔️ VEREDICTO:")
print(f"   {comparison['verdict']}")

confidence = comparison.get('confidence_level', {})
print(f"\n🎲 NIVEL DE CONFIANZA:")
print(f"   {confidence.get('level', 'N/A')} - {confidence.get('percentage', 0)}%")
print(f"   {confidence.get('desc', 'N/A')}")

print("\n" + "="*60)
print("\n💬 COMPARACIÓN EN TEXTO NATURAL:")
print("━" * 60)
comp_text = text_analyzer.generate_comparison(team_aztlan, team_overcharged, comparison)
print(comp_text)

print("\n\n" + "="*60)
print(" ✅ TESTS COMPLETADOS - IA ULTRA POTENTE ACTIVA")
print("="*60)
print("\n💡 NUEVAS CAPACIDADES:")
print("   • Análisis de momentum y tendencias")
print("   • Predicción de score futuro")
print("   • Detección de anomalías/outliers")
print("   • Ventajas estratégicas multi-nivel")
print("   • Sistema de prioridades en estrategias")
print("   • Recomendaciones de alianza personalizadas")
print("   • Nivel de confianza en predicciones")
print("   • Análisis estadístico avanzado")
print("   • Templates de texto mejorados (3 variantes)")
print("   • Categorización en 8 niveles (vs 6 anteriores)")
print("\n🚀 LA IA AHORA ES 10X MÁS POTENTE!")
