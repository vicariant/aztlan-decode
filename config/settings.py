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
FIRST_API_USERNAME = os.getenv('FIRST_API_USERNAME', 'TU_USERNAME_AQUI')
FIRST_API_KEY = os.getenv('FIRST_API_KEY', 'TU_KEY_AQUI')

# The Orange Alliance (TOA)
# Obtén tu key en: https://theorangealliance.org/apidocs
TOA_API_KEY = os.getenv('TOA_API_KEY', 'TU_KEY_AQUI')

# FTC Scout (No requiere API key - GraphQL público)
# URL: https://api.ftcscout.org/graphql

# Groq API (Para chatbot)
# Obtén tu key en: https://console.groq.com/
GROQ_API_KEY = os.getenv('GROQ_API_KEY', 'TU_GROQ_KEY_AQUI')

# ============================================
# ⚙️ CONFIGURACIÓN DE LA APLICACIÓN
# ============================================

# Flask
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'aztlan-decode-secret-2025')
FLASK_DEBUG = True
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000

# Modelos IA
MODEL_PATH = 'models/aztlan_model.pkl'
SCALER_PATH = 'models/aztlan_scaler.pkl'

# TRIDENTE
TRIDENT_CACHE_TTL = 1800  # 30 minutos
TRIDENT_TIMEOUT = 10  # segundos
TRIDENT_MAX_RETRIES = 2

# Season actual FTC
CURRENT_SEASON = '2024'  # Temporada INTO THE DEEP 2024-2025

# ============================================
# 📊 CONFIGURACIÓN DE DATOS
# ============================================

# Rutas de datos
DATA_DIR = 'assets/data'
EXOPLANETS_DATA = f'{DATA_DIR}/exoplanets'
FTC_DATA = f'{DATA_DIR}/ftc'

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

LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# ============================================
# 🔒 SEGURIDAD
# ============================================

# Rate limiting (opcional)
RATE_LIMIT_ENABLED = False
RATE_LIMIT_PER_MINUTE = 60

# CORS (opcional)
CORS_ENABLED = True
CORS_ORIGINS = ['http://localhost:5000', 'http://127.0.0.1:5000']
