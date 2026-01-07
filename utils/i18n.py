# -*- coding: utf-8 -*-
"""
SISTEMA DE INTERNACIONALIZACIÓN - AZTLÁN DECODE
"""

import json
import os
from functools import wraps
from flask import session, request

class I18n:
    """Gestor de internacionalización"""
    
    def __init__(self, default_locale='es'):
        self.default_locale = default_locale
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """Carga todos los archivos de traducción"""
        locales_dir = os.path.join(os.path.dirname(__file__), '..', 'locales')
        
        for filename in os.listdir(locales_dir):
            if filename.endswith('.json'):
                locale = filename.replace('.json', '')
                filepath = os.path.join(locales_dir, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        self.translations[locale] = json.load(f)
                except Exception as e:
                    print(f"Error cargando traducciones {locale}: {e}")
    
    def get_locale(self):
        """Obtiene el idioma actual del usuario"""
        # 1. De la sesión
        if 'locale' in session:
            return session['locale']
        
        # 2. Del navegador
        best_match = request.accept_languages.best_match(['es', 'en'])
        if best_match:
            return best_match
        
        # 3. Por defecto
        return self.default_locale
    
    def set_locale(self, locale):
        """Establece el idioma del usuario"""
        if locale in self.translations:
            session['locale'] = locale
            return True
        return False
    
    def translate(self, key, locale=None, **kwargs):
        """
        Traduce una clave
        
        Args:
            key: Clave de traducción (ej: 'common.search')
            locale: Idioma (opcional, usa get_locale() si no se proporciona)
            **kwargs: Variables para interpolación
        
        Returns:
            Texto traducido
        """
        if locale is None:
            locale = self.get_locale()
        
        # Obtener traducciones del idioma
        translations = self.translations.get(locale, self.translations[self.default_locale])
        
        # Navegar por la estructura de keys (ej: 'common.search')
        keys = key.split('.')
        value = translations
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return key  # Si no se encuentra, devolver la clave
        
        if value is None:
            return key
        
        # Interpolación de variables
        if kwargs and isinstance(value, str):
            try:
                value = value.format(**kwargs)
            except KeyError:
                pass
        
        return value
    
    def get_available_locales(self):
        """Obtiene lista de idiomas disponibles"""
        return list(self.translations.keys())
    
    def get_translations_for_js(self, locale=None):
        """Obtiene traducciones para JavaScript"""
        if locale is None:
            locale = self.get_locale()
        
        return self.translations.get(locale, self.translations[self.default_locale])

# Instancia global
i18n = I18n()

# Decorador para traducir
def localize(key, **kwargs):
    """Función helper para usar en templates"""
    return i18n.translate(key, **kwargs)

# Alias corto
_ = localize
t = localize
