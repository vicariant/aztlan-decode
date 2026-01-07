#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AZTLÁN DECODE - CONFIGURACIÓN
=============================
Archivo de configuración para API keys y settings
"""

import os

# ============================================
# 🔑 CONFIGURACIÓN DE API KEYS
# ============================================
# Coloca tus API keys aquí o usa variables de entorno

# FIRST API (FTC/FRC Oficial)
# Obtén tu key en: https://frc-events.firstinspires.org/services/API
FIRST_API_USERNAME = os.getenv('FIRST_API_USERNAME', '')
FIRST_API_KEY = os.getenv('FIRST_API_KEY', '')
FIRST_API_BASE_URL = os.getenv('FIRST_API_BASE_URL', 'https://ftc-events.firstinspires.org')

# The Orange Alliance (TOA)
# Obtén tu key en: https://theorangealliance.org/apidocs
TOA_API_KEY = os.getenv('TOA_API_KEY', '')

# FTC Scout (No requiere API key - GraphQL público)
# URL: https://api.ftcscout.org/graphql
FTC_SCOUT_URL = 'https://api.ftcscout.org/graphql'

# Groq API (Para chatbot)
# Obtén tu key en: https://console.groq.com/
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')

# ============================================
# ⚙️ CONFIGURACIÓN DE LA APLICACIÓN
# ============================================

# Flask
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'aztlan-decode-secret-2025')
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('PORT', os.getenv('FLASK_PORT', '5000')))

# Modelos IA
MODEL_PATH = os.getenv('MODEL_PATH', 'models/aztlan_model.pkl')
SCALER_PATH = os.getenv('SCALER_PATH', 'models/aztlan_scaler.pkl')

# TRIDENTE (Sistema de APIs)
TRIDENT_CACHE_TTL = int(os.getenv('TRIDENT_CACHE_TTL', '1800'))  # 30 minutos
TRIDENT_TIMEOUT = int(os.getenv('TRIDENT_TIMEOUT', '10'))  # segundos
TRIDENT_MAX_RETRIES = int(os.getenv('TRIDENT_MAX_RETRIES', '3'))

# Season actual FTC
CURRENT_SEASON = os.getenv('CURRENT_SEASON', '2024')  # Temporada INTO THE DEEP 2024-2025

# Base de datos
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///aztlan_decode.db')
DATABASE_ECHO = os.getenv('DATABASE_ECHO', 'False').lower() == 'true'

# ============================================
# 📊 CONFIGURACIÓN DE DATOS
# ============================================

# Rutas de datos
DATA_DIR = os.getenv('DATA_DIR', 'data')
EXPORTS_DIR = os.getenv('EXPORTS_DIR', 'exports')
EXOPLANETS_DATA = f'{DATA_DIR}/exoplanets'
FTC_DATA = f'{DATA_DIR}/ftc'

# Crear directorios si no existen
for directory in [DATA_DIR, EXPORTS_DIR, 'models', 'database']:
    os.makedirs(directory, exist_ok=True)

# ============================================
# 🎨 CONFIGURACIÓN VISUAL
# ============================================

# Tema Cyber-Azteca
THEME_COLORS = {
    'jade': '#00A86B',
    'oro': '#FFD700',
    'turquesa': '#00F3FF',
    'obsidiana': '#0B0C10',
    'plata': '#C0C0C0',
    'cobre': '#B87333'
}

# ============================================
# 📝 LOGGING
# ============================================

import logging

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Configurar logging global
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('aztlan_decode.log', encoding='utf-8')
    ]
)

# ============================================
# 🔒 SEGURIDAD
# ============================================

# Rate limiting
RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'False').lower() == 'true'
RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', '60'))

# CORS
CORS_ENABLED = os.getenv('CORS_ENABLED', 'True').lower() == 'true'
CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5000,http://127.0.0.1:5000').split(',')

# Session
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Protección de menores (COPPA/UK/CA/EU)
MINOR_PROTECTION_ENABLED = True
MINOR_AGE_LIMIT = 13  # COPPA compliance
