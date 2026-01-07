#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OPTIMIZACIONES FINALES - POST-RESPONSE HANDLER
"""

def optimize_response(response):
    """Optimiza las respuestas HTTP agregando headers de performance"""
    # Cache headers para assets estáticos
    if request.path.startswith('/static'):
        response.cache_control.max_age = 31536000  # 1 año
        response.cache_control.public = True
        
    # Compression hint
    response.headers['Vary'] = 'Accept-Encoding'
    
    # Security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    return response

def preload_critical_resources(response):
    """Agrega preload hints para recursos críticos"""
    if request.path == '/':
        response.headers['Link'] = '</static/css/main.css>; rel=preload; as=style, </static/js/main.js>; rel=preload; as=script'
    
    return response
