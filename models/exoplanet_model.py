#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AZTLÁN DECODE - MODELO DE EXOPLANETAS
Módulo para clasificación de exoplanetas usando IA
"""

import numpy as np
import joblib
import os
from datetime import datetime

class ExoplanetClassifier:
    """Clasificador de exoplanetas usando Random Forest"""
    
    def __init__(self, model_path='models/aztlan_model.pkl', scaler_path='models/aztlan_scaler.pkl'):
        """
        Inicializa el clasificador
        
        Args:
            model_path: Ruta al modelo entrenado
            scaler_path: Ruta al escalador de características
        """
        self.model = None
        self.scaler = None
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.load_models()
    
    def load_models(self):
        """Carga los modelos desde disco"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                return True
            else:
                print(f"⚠️ Modelos no encontrados. Entrena el modelo con train_model.py")
                return False
        except Exception as e:
            print(f"❌ Error al cargar modelos: {str(e)}")
            return False
    
    def predict(self, koi_prad, koi_srad, koi_period, koi_steff):
        """
        Realiza una predicción sobre un candidato a exoplaneta
        
        Args:
            koi_prad: Radio del planeta (Earth radii)
            koi_srad: Radio de la estrella (Solar radii)
            koi_period: Periodo orbital (días)
            koi_steff: Temperatura estelar (Kelvin)
        
        Returns:
            dict: Diccionario con los resultados de la predicción
        """
        if self.model is None or self.scaler is None:
            return {
                'error': 'Modelos no disponibles. Ejecuta train_model.py primero.',
                'success': False
            }
        
        try:
            # Preparar características
            features = np.array([[koi_prad, koi_srad, koi_period, koi_steff]])
            features_scaled = self.scaler.transform(features)
            
            # Predicción
            prediction = self.model.predict(features_scaled)[0]
            probability = self.model.predict_proba(features_scaled)[0]
            
            # Resultados
            result = "PLANETA CONFIRMADO" if prediction == 1 else "FALSO POSITIVO"
            confidence = max(probability) * 100
            
            planet_prob = probability[1] if len(probability) > 1 else (probability[0] if prediction == 1 else 0)
            false_positive_prob = probability[0] if len(probability) > 1 else (probability[0] if prediction == 0 else 0)
            
            return {
                'success': True,
                'prediction': result,
                'confidence': round(confidence, 2),
                'planet_probability': round(planet_prob * 100, 2),
                'false_positive_probability': round(false_positive_prob * 100, 2),
                'input_data': {
                    'koi_prad': koi_prad,
                    'koi_srad': koi_srad,
                    'koi_period': koi_period,
                    'koi_steff': koi_steff
                },
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'error': f'Error en predicción: {str(e)}',
                'success': False
            }
    
    def get_feature_importance(self):
        """Retorna la importancia de cada característica"""
        if self.model is None:
            return None
        
        try:
            feature_names = ['Radio Planeta', 'Radio Estrella', 'Periodo Orbital', 'Temp. Estelar']
            importances = self.model.feature_importances_
            
            return {
                name: round(importance * 100, 2)
                for name, importance in zip(feature_names, importances)
            }
        except (AttributeError, ValueError, TypeError):
            return None
    
    def classify_planet_type(self, koi_prad):
        """
        Clasifica el tipo de planeta basado en su radio
        
        Args:
            koi_prad: Radio del planeta (Earth radii)
        
        Returns:
            str: Tipo de planeta
        """
        if koi_prad < 1.5:
            return "🌍 Planeta Terrestre"
        elif koi_prad < 2.5:
            return "🌎 Super-Tierra"
        elif koi_prad < 6.0:
            return "🪐 Neptuno/Sub-Neptuno"
        else:
            return "🪐 Gigante Gaseoso"
    
    def is_habitable_zone(self, koi_period):
        """
        Verifica si el periodo orbital sugiere zona habitable
        
        Args:
            koi_period: Periodo orbital (días)
        
        Returns:
            bool: True si está en zona potencialmente habitable
        """
        # Zona habitable aproximada: 200-400 días para estrellas tipo Sol
        return 200 <= koi_period <= 400

# Instancia global del clasificador
classifier = ExoplanetClassifier()

def predict_exoplanet(koi_prad, koi_srad, koi_period, koi_steff):
    """Función de conveniencia para predicción"""
    return classifier.predict(koi_prad, koi_srad, koi_period, koi_steff)

def get_classifier():
    """Retorna la instancia del clasificador"""
    return classifier
