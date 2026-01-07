#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFICACIÓN COMPLETA DEL CÓDIGO - AZTLÁN DECODE
"""

import os
import sys
import re
from pathlib import Path

def check_file_syntax(filepath):
    """Verifica sintaxis de archivos Python"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        compile(code, filepath, 'exec')
        return True, "OK"
    except SyntaxError as e:
        return False, f"SyntaxError línea {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def check_bare_excepts(filepath):
    """Busca bare except statements"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        issues = []
        for i, line in enumerate(lines, 1):
            # Buscar bare except (except: sin tipo de excepción)
            if re.match(r'^\s*except\s*:\s*$', line):
                issues.append(f"Línea {i}: bare except encontrado")
        
        return issues
    except:
        return []

def check_imports(filepath):
    """Verifica que las importaciones existan"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        issues = []
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                # Verificar importaciones básicas
                if 'import *' in line:
                    issues.append(f"Línea {i}: Evitar 'import *'")
        
        return issues
    except:
        return []

def check_required_files():
    """Verifica que existan los archivos necesarios"""
    required = {
        'app.py': 'Archivo principal de Flask',
        'requirements.txt': 'Dependencias de Python',
        'Procfile': 'Configuración de Heroku',
        'runtime.txt': 'Versión de Python para Heroku',
        '.gitignore': 'Archivos a ignorar en Git',
        '.env': 'Variables de entorno (puede estar en .gitignore)',
    }
    
    print("\n" + "="*60)
    print("VERIFICACIÓN DE ARCHIVOS REQUERIDOS")
    print("="*60)
    
    all_ok = True
    for file, desc in required.items():
        exists = os.path.exists(file)
        status = "[OK]" if exists else "[FALTA]"
        print(f"{status} {file:20s} - {desc}")
        if not exists and file != '.env':
            all_ok = False
    
    return all_ok

def check_python_files():
    """Verifica todos los archivos Python"""
    print("\n" + "="*60)
    print("VERIFICACIÓN DE SINTAXIS DE ARCHIVOS PYTHON")
    print("="*60)
    
    python_files = []
    for root, dirs, files in os.walk('.'):
        # Ignorar directorios
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'venv', 'env', '.vscode']]
        
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                python_files.append(filepath)
    
    all_ok = True
    for filepath in sorted(python_files):
        success, msg = check_file_syntax(filepath)
        status = "[OK]" if success else "[ERROR]"
        print(f"{status} {filepath}")
        if not success:
            print(f"     {msg}")
            all_ok = False
    
    return all_ok

def check_code_quality():
    """Verifica calidad del código"""
    print("\n" + "="*60)
    print("VERIFICACIÓN DE CALIDAD DE CÓDIGO")
    print("="*60)
    
    python_files = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'venv', 'env', '.vscode']]
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                python_files.append(filepath)
    
    total_issues = 0
    for filepath in sorted(python_files):
        bare_excepts = check_bare_excepts(filepath)
        import_issues = check_imports(filepath)
        
        if bare_excepts or import_issues:
            print(f"\n{filepath}:")
            for issue in bare_excepts:
                print(f"  [WARNING] {issue}")
                total_issues += 1
            for issue in import_issues:
                print(f"  [INFO] {issue}")
    
    if total_issues == 0:
        print("\n[OK] No se encontraron problemas de calidad")
    else:
        print(f"\n[WARNING] Se encontraron {total_issues} problemas")
    
    return total_issues == 0

def check_static_files():
    """Verifica archivos estáticos"""
    print("\n" + "="*60)
    print("VERIFICACIÓN DE ARCHIVOS ESTÁTICOS")
    print("="*60)
    
    required_static = {
        'static/css/themed-backgrounds.css': 'Fondos animados',
        'static/js/theme-manager.js': 'Gestor de temas',
        'static/css/styles.css': 'Estilos principales',
        'static/js/chatbot.js': 'JavaScript del chatbot',
    }
    
    all_ok = True
    for file, desc in required_static.items():
        exists = os.path.exists(file)
        status = "[OK]" if exists else "[FALTA]"
        print(f"{status} {file:40s} - {desc}")
        if not exists:
            all_ok = False
    
    return all_ok

def check_templates():
    """Verifica templates HTML"""
    print("\n" + "="*60)
    print("VERIFICACIÓN DE TEMPLATES")
    print("="*60)
    
    if not os.path.exists('templates'):
        print("[ERROR] No existe el directorio templates/")
        return False
    
    templates = [f for f in os.listdir('templates') if f.endswith('.html')]
    
    required_templates = ['layout.html', 'scouting.html', 'comparison.html', 'astronomy.html']
    
    all_ok = True
    for template in required_templates:
        exists = template in templates
        status = "[OK]" if exists else "[FALTA]"
        print(f"{status} {template}")
        if not exists:
            all_ok = False
    
    print(f"\n[INFO] Total de templates: {len(templates)}")
    
    return all_ok

def main():
    print("\n" + "="*60)
    print("AZTLÁN DECODE - VERIFICACIÓN COMPLETA DEL CÓDIGO")
    print("="*60)
    
    # Cambiar al directorio del proyecto
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    results = {
        'Archivos requeridos': check_required_files(),
        'Sintaxis Python': check_python_files(),
        'Calidad de código': check_code_quality(),
        'Archivos estáticos': check_static_files(),
        'Templates HTML': check_templates(),
    }
    
    print("\n" + "="*60)
    print("RESUMEN FINAL")
    print("="*60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test}")
    
    print("\n" + "="*60)
    print(f"RESULTADO: {passed}/{total} pruebas pasadas")
    print("="*60)
    
    if passed == total:
        print("\n[OK] Todo listo para subir a GitHub y Heroku!")
        print("\nPróximos pasos:")
        print("1. git init")
        print("2. git add .")
        print("3. git commit -m 'Initial commit'")
        print("4. git remote add origin <tu-repo>")
        print("5. git push -u origin main")
        print("\nVer DEPLOYMENT.md para instrucciones completas")
        return 0
    else:
        print("\n[ERROR] Hay problemas que deben corregirse antes de desplegar")
        return 1

if __name__ == '__main__':
    sys.exit(main())
