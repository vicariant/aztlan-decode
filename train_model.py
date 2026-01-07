#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AZTLÁN DECODE - ENTRENAMIENTO DE MODELO IA
Entrena el modelo de clasificación de exoplanetas
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os

def generate_synthetic_data(n_samples=1000):
    """Genera datos sintéticos basados en características de exoplanetas reales"""
    print(f"🔬 Generando {n_samples} muestras sintéticas...")
    
    np.random.seed(42)
    
    # Datos para PLANETAS CONFIRMADOS (label = 1)
    n_planets = n_samples // 2
    
    # Planetas terrestres y super-tierras
    terrestrial = n_planets // 3
    koi_prad_terr = np.random.uniform(0.5, 2.5, terrestrial)
    koi_srad_terr = np.random.uniform(0.7, 1.3, terrestrial)
    koi_period_terr = np.random.uniform(1, 500, terrestrial)
    koi_steff_terr = np.random.uniform(4000, 6500, terrestrial)
    
    # Gigantes gaseosos
    gas_giants = n_planets // 3
    koi_prad_gas = np.random.uniform(4.0, 15.0, gas_giants)
    koi_srad_gas = np.random.uniform(0.8, 2.0, gas_giants)
    koi_period_gas = np.random.uniform(50, 4000, gas_giants)
    koi_steff_gas = np.random.uniform(3500, 7000, gas_giants)
    
    # Neptunos y sub-neptunos
    neptunes = n_planets - terrestrial - gas_giants
    koi_prad_nep = np.random.uniform(2.5, 6.0, neptunes)
    koi_srad_nep = np.random.uniform(0.7, 1.5, neptunes)
    koi_period_nep = np.random.uniform(5, 1000, neptunes)
    koi_steff_nep = np.random.uniform(3800, 6800, neptunes)
    
    # Combinar planetas
    planets_data = np.column_stack([
        np.concatenate([koi_prad_terr, koi_prad_gas, koi_prad_nep]),
        np.concatenate([koi_srad_terr, koi_srad_gas, koi_srad_nep]),
        np.concatenate([koi_period_terr, koi_period_gas, koi_period_nep]),
        np.concatenate([koi_steff_terr, koi_steff_gas, koi_steff_nep])
    ])
    planets_labels = np.ones(n_planets)
    
    # Datos para FALSOS POSITIVOS (label = 0)
    n_false = n_samples - n_planets
    
    # Características anómalas que indican falsos positivos
    # Dividir en tres grupos
    n_small = n_false // 3
    n_large = n_false // 3
    n_inter = n_false - n_small - n_large
    
    koi_prad_false = np.concatenate([
        np.random.uniform(0.1, 0.5, n_small),  # Muy pequeños
        np.random.uniform(20, 50, n_large),    # Muy grandes
        np.random.uniform(1.0, 3.0, n_inter)   # Intermedios con otras anomalías
    ])
    koi_srad_false = np.random.uniform(0.3, 3.0, n_false)
    
    # Períodos anómalos
    n_short = n_false // 2
    n_long = n_false - n_short
    koi_period_false = np.concatenate([
        np.random.uniform(0.1, 0.5, n_short),   # Períodos muy cortos
        np.random.uniform(5000, 10000, n_long)  # Períodos muy largos
    ])
    koi_steff_false = np.random.uniform(2000, 10000, n_false)
    
    false_data = np.column_stack([
        koi_prad_false,
        koi_srad_false,
        koi_period_false,
        koi_steff_false
    ])
    false_labels = np.zeros(n_false)
    
    # Combinar todo
    X = np.vstack([planets_data, false_data])
    y = np.concatenate([planets_labels, false_labels])
    
    # Mezclar datos
    indices = np.random.permutation(len(X))
    X = X[indices]
    y = y[indices]
    
    print(f"✅ Datos generados: {len(X)} muestras")
    print(f"   - Planetas: {int(y.sum())} ({y.sum()/len(y)*100:.1f}%)")
    print(f"   - Falsos positivos: {int((1-y).sum())} ({(1-y).sum()/len(y)*100:.1f}%)")
    
    return X, y

def train_model():
    """Entrena el modelo de Random Forest"""
    print("\n🚀 INICIANDO ENTRENAMIENTO DEL MODELO AZTLÁN IA")
    print("=" * 60)
    
    # Generar datos
    X, y = generate_synthetic_data(n_samples=2000)
    
    # Dividir en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\n📊 División de datos:")
    print(f"   - Entrenamiento: {len(X_train)} muestras")
    print(f"   - Prueba: {len(X_test)} muestras")
    
    # Normalizar datos
    print("\n⚙️ Normalizando características...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Entrenar modelo
    print("\n🧠 Entrenando Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train_scaled, y_train)
    
    # Evaluar
    train_score = model.score(X_train_scaled, y_train)
    test_score = model.score(X_test_scaled, y_test)
    
    print("\n📈 RESULTADOS DEL ENTRENAMIENTO:")
    print("=" * 60)
    print(f"   ✅ Precisión en entrenamiento: {train_score*100:.2f}%")
    print(f"   ✅ Precisión en prueba: {test_score*100:.2f}%")
    
    # Importancia de características
    feature_names = ['Radio Planeta', 'Radio Estrella', 'Periodo Orbital', 'Temp. Estelar']
    importances = model.feature_importances_
    print("\n🔍 Importancia de características:")
    for name, importance in zip(feature_names, importances):
        print(f"   - {name}: {importance*100:.2f}%")
    
    # Guardar modelos
    print("\n💾 Guardando modelos...")
    os.makedirs('models', exist_ok=True)
    
    joblib.dump(model, 'models/aztlan_model.pkl')
    joblib.dump(scaler, 'models/aztlan_scaler.pkl')
    
    print("\n✅ MODELOS GUARDADOS EXITOSAMENTE")
    print("=" * 60)
    print("📁 Archivos creados:")
    print("   - models/aztlan_model.pkl")
    print("   - models/aztlan_scaler.pkl")
    print("\n🎉 ¡Modelo entrenado y listo para usar!")
    
    # Ejemplo de predicción
    print("\n🧪 PRUEBA DEL MODELO:")
    print("-" * 60)
    test_cases = [
        ([1.0, 1.0, 365.25, 5778], "🌍 Tipo Tierra"),
        ([11.2, 1.0, 4333, 5778], "🪐 Tipo Júpiter"),
        ([2.5, 0.8, 180, 4800], "🌎 Super-Tierra"),
        ([0.3, 2.5, 0.2, 8000], "❌ Falso Positivo")
    ]
    
    for features, description in test_cases:
        features_scaled = scaler.transform([features])
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0]
        result = "PLANETA CONFIRMADO" if prediction == 1 else "FALSO POSITIVO"
        confidence = max(probability) * 100
        
        print(f"{description}")
        print(f"   Predicción: {result} ({confidence:.1f}% confianza)")
    
    print("=" * 60)

if __name__ == "__main__":
    train_model()
