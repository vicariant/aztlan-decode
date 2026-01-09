#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para corregir encoding de templates"""

import os

# Mapa de reemplazos
replacements = {
    'MÃ"DULO': 'MÓDULO',
    'AZTLÃN': 'AZTLÁN',
    'Ãndice': 'Índice',
    'ðŸ§¬': '🧬',
    'ðŸ"‰': '📉',
    'mÃ©todo': 'método',
    'seÃ±ales': 'señales',
    'astronÃ³micas': 'astronómicas',
    'tÃ­pico': 'típico',
    'â­': '⭐',
    'ðŸ"„': '🔄',
    'dÃ­as': 'días',
    'ðŸŒ¡ï¸': '🌡️',
    '½': '🔮',
    '¯': '🎯',
    'ðŸ"Š': '📊',
    'ðŸŒ': '🌍',
    'JÃºpiter': 'Júpiter',
    'ðŸŒŽ': '🌎',
    'ðŸ"¥': '🔥',
    'REVELACIÃ"N': 'REVELACIÓN',
    'predicciÃ³n': 'predicción',
    'probabilÃ­sticos': 'probabilísticos',
    'ðŸ"¡': '📡',
    'ðŸ"­': '🔭',
    'AstrofÃ­sico': 'Astrofísico',
    'analisis': 'Análisis',
    'AsÃ­': 'Así',
    'cÃ³smicas': 'cósmicas',
    'parÃ¡metros': 'parámetros',
    'espectroscÃ³picas': 'espectroscópicas',
    'fotomÃ©tricas': 'fotométricas',
    'ðŸŒ±': '🌱',
    'regiÃ³n': 'región',
    'lÃ­quida': 'líquida',
    'podrÃ­a': 'podría',
    'ocÃ©anos': 'océanos',
    'corazÃ³n': 'corazón',
    'âš ï¸': '⚠️',
    'caracterÃ­sticas': 'características',
    'tÃ­picas': 'típicas',
    'contaminaciÃ³n': 'contaminación',
    'intrÃ­nseca': 'intrínseca',
    'ðŸ"': '🔍',
    'RecomendaciÃ³n': 'Recomendación',
    'espectrometrÃ­a': 'espectrometría',
    'fotometrÃ­a': 'fotometría',
    'transito': 'tránsito',
    'TRÃNSITO': 'TRÁNSITO',
    'ðŸŒŒ': '🌌',
    'RepresentaciÃ³n': 'Representación',
    'ÃNDICE': 'ÍNDICE',
    'idÃ©ntica': 'idéntica',
    'cÃ­rculo': 'círculo',
    'CÃ­rculo': 'Círculo',
    'cÃ³mo': 'cómo',
    'tamaÃ±o': 'tamaño',
    'AztlÃ¡n': 'Aztlán',
    'ðŸ¤–': '🤖',
    'SimulaciÃ³n': 'Simulación',
    'ðŸ"¤': '📤',
    'ESPECÃFICOS': 'ESPECÍFICOS',
    'ASTRONOMÃA': 'ASTRONOMÍA',
    'PREDICCIÃ"N': 'PREDICCIÓN',
    'InterpretaciÃ³n': 'Interpretación',
    'cientÃ­fica': 'científica',
    'â•'': '║',
    'âœ¦': '✦',
    'ðŸ›°ï¸': '🛰️',
    'âš¡': '⚡',
    'VÃA': 'VÍA',
    'LÃCTEA': 'LÁCTEA',
    'â"‚': '│',
    'ðŸŒ™': '🌙',
    'â˜€ï¸': '☀️',
    'segun': 'según',
}

def fix_encoding(filepath):
    """Corrige encoding de un archivo"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {filepath} - Corregido")
            return True
        else:
            print(f"ℹ️  {filepath} - Sin cambios")
            return False
    except Exception as e:
        print(f"❌ {filepath} - Error: {e}")
        return False

if __name__ == '__main__':
    files_to_fix = [
        'templates/astronomy.html',
        'templates/scouting.html',
    ]
    
    fixed_count = 0
    for filepath in files_to_fix:
        if os.path.exists(filepath):
            if fix_encoding(filepath):
                fixed_count += 1
        else:
            print(f"⚠️  {filepath} - No existe")
    
    print(f"\n✅ Archivos corregidos: {fixed_count}")
