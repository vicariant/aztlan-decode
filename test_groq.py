#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST DE GROQ API
Verifica que la API key funciona correctamente
"""

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def test_groq_connection():
    """Prueba la conexión con Groq API"""
    print("\n" + "="*60)
    print("🧪 TEST DE GROQ API")
    print("="*60)
    
    # Verificar API key
    api_key = os.getenv('GROQ_API_KEY')
    
    if not api_key:
        print("❌ ERROR: GROQ_API_KEY no encontrada en .env")
        return False
    
    print(f"✅ API Key encontrada: {api_key[:15]}...{api_key[-10:]}")
    
    try:
        # Inicializar cliente
        print("\n🔌 Inicializando cliente Groq...")
        client = Groq(api_key=api_key)
        print("✅ Cliente inicializado correctamente")
        
        # Hacer una prueba simple
        print("\n💬 Enviando mensaje de prueba...")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Eres un asistente conciso."},
                {"role": "user", "content": "Di 'Hola Aztlán' en una línea"}
            ],
            temperature=0.7,
            max_tokens=50
        )
        
        assistant_message = response.choices[0].message.content
        print(f"✅ Respuesta recibida: {assistant_message}")
        
        print("\n" + "="*60)
        print("✅ GROQ API FUNCIONANDO CORRECTAMENTE")
        print("="*60)
        print("\n🤖 Sistemas de IA disponibles:")
        print("   ✓ Chatbot con Llama 3.3 70B")
        print("   ✓ QuetzalBot RAG (Manual de reglas)")
        print("   ✓ Simulador de partidos")
        print("   ✓ Análisis estratégico de equipos")
        print("\n🌐 Prueba el chatbot en: http://localhost:5000\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\n🔧 Soluciones posibles:")
        print("   1. Verifica que la API key sea válida")
        print("   2. Revisa tu conexión a internet")
        print("   3. Confirma que tienes créditos en Groq")
        print("   4. Intenta generar una nueva key en: https://console.groq.com/")
        return False

if __name__ == '__main__':
    test_groq_connection()
