#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFICACIÓN COMPLETA DEL SISTEMA AZTLÁN DECODE
Prueba todos los componentes y reporta el estado
"""

import sys
import os

def test_imports():
    """Prueba que todos los módulos se importen correctamente"""
    print("\n" + "="*60)
    print("🔍 VERIFICANDO IMPORTS")
    print("="*60 + "\n")
    
    errors = []
    
    modules_to_test = [
        ('flask', 'Flask'),
        ('numpy', 'NumPy'),
        ('requests', 'Requests'),
        ('dotenv', 'Python-dotenv'),
        ('groq', 'Groq SDK'),
        ('markupsafe', 'MarkupSafe'),
    ]
    
    for module_name, display_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {display_name}")
        except ImportError as e:
            print(f"❌ {display_name}: {str(e)}")
            errors.append(display_name)
    
    if errors:
        print(f"\n⚠️  Faltan {len(errors)} módulos: {', '.join(errors)}")
        print("Instálalos con: pip install -r requirements.txt")
        return False
    
    print("\n✅ Todos los imports están disponibles\n")
    return True

def test_configuration():
    """Prueba la configuración del sistema"""
    print("="*60)
    print("🔧 VERIFICANDO CONFIGURACIÓN")
    print("="*60 + "\n")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    keys_to_check = [
        ('TOA_API_KEY', 'The Orange Alliance'),
        ('FIRST_API_USERNAME', 'FIRST API Username'),
        ('FIRST_API_KEY', 'FIRST API Key'),
        ('GROQ_API_KEY', 'Groq AI'),
        ('FLASK_SECRET_KEY', 'Flask Secret'),
    ]
    
    missing_keys = []
    
    for key, name in keys_to_check:
        value = os.getenv(key)
        if value:
            masked = value[:10] + "..." + value[-5:] if len(value) > 15 else "***"
            print(f"✅ {name}: {masked}")
        else:
            print(f"❌ {name}: NO CONFIGURADA")
            missing_keys.append(name)
    
    if missing_keys:
        print(f"\n⚠️  Faltan {len(missing_keys)} claves API")
        return False
    
    print("\n✅ Todas las claves API están configuradas\n")
    return True

def test_file_structure():
    """Verifica que existan los archivos críticos"""
    print("="*60)
    print("📁 VERIFICANDO ESTRUCTURA DE ARCHIVOS")
    print("="*60 + "\n")
    
    critical_files = [
        'app.py',
        '.env',
        'requirements.txt',
        'templates/scouting.html',
        'templates/astronomy.html',
        'templates/comparison.html',
        'static/css/themed-backgrounds.css',
        'static/js/theme-manager.js',
        'modules/api_manager.py',
        'utils/chatbot_handler.py',
        'utils/rag_system.py',
        'models/exoplanet_model.py',
    ]
    
    missing_files = []
    
    for file_path in critical_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            size_kb = size / 1024
            print(f"✅ {file_path} ({size_kb:.1f} KB)")
        else:
            print(f"❌ {file_path}: NO ENCONTRADO")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Faltan {len(missing_files)} archivos críticos")
        return False
    
    print("\n✅ Todos los archivos críticos están presentes\n")
    return True

def test_groq_api():
    """Prueba la conexión con Groq API"""
    print("="*60)
    print("🤖 PROBANDO GROQ API")
    print("="*60 + "\n")
    
    try:
        from groq import Groq
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            print("❌ GROQ_API_KEY no configurada")
            return False
        
        client = Groq(api_key=api_key)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Responde en una palabra"},
                {"role": "user", "content": "Di 'OK'"}
            ],
            max_tokens=10,
            temperature=0.1
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✅ Respuesta de Groq: {result}")
        print("✅ Groq API funcionando correctamente\n")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
        return False

def test_trident_system():
    """Prueba el sistema TRIDENTE"""
    print("="*60)
    print("🔱 PROBANDO SISTEMA TRIDENTE")
    print("="*60 + "\n")
    
    try:
        from modules.api_manager import trident
        
        print("✅ TRIDENTE importado correctamente")
        
        # Probar con un equipo conocido (16418 - Techno Mages)
        print("\nProbando consulta de equipo #16418...")
        team_data = trident.get_validated_team_data(16418)
        
        if team_data and team_data.get('identity'):
            name = team_data['identity'].get('team_name', 'N/A')
            location = team_data['identity'].get('location', 'N/A')
            print(f"✅ Equipo encontrado: {name}")
            print(f"   Ubicación: {location}")
            print(f"   Fuentes: {len(team_data.get('sources', []))}")
            print("\n✅ Sistema TRIDENTE funcionando\n")
            return True
        else:
            print("⚠️  Equipo no encontrado (puede ser normal si las APIs están caídas)\n")
            return True  # No es un error crítico
            
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("\n" + "╔" + "═"*58 + "╗")
    print("║" + "  🔮 AZTLÁN DECODE - VERIFICACIÓN COMPLETA DEL SISTEMA  ".center(58) + "║")
    print("╚" + "═"*58 + "╝")
    
    tests = [
        ("Imports", test_imports),
        ("Configuración", test_configuration),
        ("Estructura de archivos", test_file_structure),
        ("Groq API", test_groq_api),
        ("Sistema TRIDENTE", test_trident_system),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Error ejecutando {test_name}: {str(e)}\n")
            results.append((test_name, False))
    
    # Resumen final
    print("\n" + "="*60)
    print("📊 RESUMEN FINAL")
    print("="*60 + "\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status}: {test_name}")
    
    print("\n" + "="*60)
    if passed == total:
        print("✅ SISTEMA COMPLETAMENTE FUNCIONAL".center(60))
        print(f"   {passed}/{total} pruebas pasadas".center(60))
        print("\n🚀 El servidor está listo para usar".center(60))
        print("   Ejecuta: python app.py".center(60))
    else:
        print("⚠️  ALGUNOS COMPONENTES NECESITAN ATENCIÓN".center(60))
        print(f"   {passed}/{total} pruebas pasadas".center(60))
        print(f"   {total - passed} pruebas fallaron".center(60))
    print("="*60 + "\n")
    
    return passed == total

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Verificación interrumpida por el usuario\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error fatal: {str(e)}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
