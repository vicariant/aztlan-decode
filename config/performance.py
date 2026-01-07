#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONFIGURACIÓN DE RENDIMIENTO Y OPTIMIZACIÓN
"""

# Cache configuration
CACHE_CONFIG = {
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300,  # 5 minutos
    'CACHE_THRESHOLD': 500  # Máximo items en cache
}

# Compression settings
COMPRESS_MIMETYPES = [
    'text/html',
    'text/css',
    'text/xml',
    'application/json',
    'application/javascript',
    'text/javascript'
]

COMPRESS_LEVEL = 6  # Nivel de compresión (1-9)
COMPRESS_MIN_SIZE = 500  # Comprimir solo > 500 bytes

# Static file caching (1 año)
SEND_FILE_MAX_AGE_DEFAULT = 31536000

# Security headers
SECURITY_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'SAMEORIGIN',
    'X-XSS-Protection': '1; mode=block'
}

# Rate limiting
RATE_LIMIT_STORAGE_URL = 'memory://'
RATELIMIT_DEFAULT = "100 per minute"

# Database connection pooling (si se usa)
DB_POOL_SIZE = 10
DB_MAX_OVERFLOW = 20
DB_POOL_TIMEOUT = 30
DB_POOL_RECYCLE = 3600

# Numpy optimization
import os
os.environ['OMP_NUM_THREADS'] = '4'  # Threads para numpy
os.environ['OPENBLAS_NUM_THREADS'] = '4'
os.environ['MKL_NUM_THREADS'] = '4'

# Logging optimization
import logging
logging.getLogger('werkzeug').setLevel(logging.WARNING)  # Solo warnings

# JSON optimization
JSON_SORT_KEYS = False  # No ordenar keys (más rápido)
JSON_AS_ASCII = False  # Soportar unicode directo

# Memory optimization
import gc
gc.set_threshold(700, 10, 10)  # Menos GC runs = más velocidad
