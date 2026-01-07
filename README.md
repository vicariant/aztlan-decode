# 🏺 AZTLÁN DECODE - Sistema de Scouting FTC

Sistema avanzado de análisis y predicción para equipos de FIRST Tech Challenge, con inteligencia artificial, fondos animados inmersivos y base de datos persistente.

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Características

### 📊 Módulos Principales

1. **🏛️ SCOUTING (Excavación Digital)**
   - Sistema TRIDENTE de triple validación (TOA, Scout, FIRST)
   - Análisis completo de equipos FTC
   - Fondos animados de oasis arqueológico
   - 🆕 Historial de búsquedas permanente
   - 🆕 Sistema de favoritos

2. **🌌 ASTRONOMÍA (Exploración de Exoplanetas)**
   - Simulación de búsqueda de exoplanetas
   - Análisis de zonas habitables
   - Fondo cósmico con nebulosas y galaxias
   - 🆕 Simulaciones guardadas en DB

3. **⚔️ COMPARACIÓN (Campo de Batalla)**
   - Comparación directa entre 2 equipos
   - Análisis estratégico con IA
   - Predicción de resultados
   - 🆕 Exportar a PDF/CSV

### 🆕 NUEVAS FUNCIONALIDADES

#### 🗄️ Base de Datos Persistente
- SQLite con SQLAlchemy
- 7 modelos de datos (búsquedas, análisis, cache, favoritos, predicciones)
- Persistencia permanente
- Cache inteligente de APIs (24h)

#### 📥 Exportación de Datos
- PDF profesional con ReportLab
- CSV/Excel con Pandas  
- Tablas formateadas y gráficos
- Exportar análisis individuales o comparaciones

#### 📱 PWA (Progressive Web App)
- Instalable en móvil y desktop
- Funcionamiento offline
- Cache de recursos
- Notificaciones push ready

#### 🧪 Tests Automatizados
- pytest configurado
- 20+ tests (DB, exportación, integración)
- Coverage > 80%

#### 🌍 Internacionalización
- Español/Inglés implementado
- Detección automática de idioma
- Cambio dinámico

#### 🎨 Temas Visuales Inmersivos
- 3 fondos animados únicos por módulo
- Modo Día/Noche con un botón
- Transiciones suaves CSS

## 🚀 Instalación Local

### Requisitos

- Python 3.11 o superior
- pip

### Pasos

```bash
# 1. Clonar repositorio
git clone https://github.com/TU_USUARIO/aztlan-decode.git
cd aztlan-decode

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
# Crear archivo .env:
FLASK_SECRET_KEY=tu-clave-secreta
GROQ_API_KEY=tu-clave-groq

# 4. Inicializar base de datos
python -c "from database.models import init_db; init_db()"

# 5. Ejecutar servidor
python app.py
```

Abre http://localhost:5000

## 🧪 Ejecutar Tests

```bash
# Todos los tests
pytest tests/ -v

# Tests específicos
pytest tests/test_comprehensive.py -v

# Con coverage
pytest --cov=. tests/
```

## 📦 Despliegue en Heroku

Ver [DEPLOYMENT.md](DEPLOYMENT.md) para instrucciones completas.

Resumen:
```bash
git push heroku main
```

## 🛠️ Tecnologías

- **Backend:** Flask 3.1.2
- **IA:** Groq (Llama 3.3 70B), scikit-learn
- **DB:** SQLite/PostgreSQL con SQLAlchemy
- **Exportación:** ReportLab, Pandas, openpyxl
- **Tests:** pytest
- **PWA:** Service Worker, manifest.json
- **APIs:** TOA, Scout, FIRST

## 📁 Estructura

```
aztlan-decode/
├── app.py                    # Servidor Flask
├── database/
│   ├── models.py             # 7 modelos SQLAlchemy
│   └── db_operations.py      # CRUD operations
├── utils/
│   ├── report_exporter.py    # Exportar PDF/CSV
│   └── i18n.py               # Internacionalización
├── static/
│   ├── css/themed-backgrounds.css
│   ├── js/theme-manager.js
│   ├── manifest.json         # PWA config
│   └── sw.js                 # Service Worker
├── locales/
│   ├── es.json               # Traducciones español
│   └── en.json               # Traducciones inglés
├── tests/
│   └── test_comprehensive.py # 20+ tests
├── requirements.txt
├── Procfile                  # Heroku config
└── ROADMAP.md               # Hoja de ruta
```

## 🎮 Uso

### Módulo Scouting
1. Ve a `/scouting`
2. Ingresa número de equipo FTC
3. Click "Analizar Equipo"
4. Exporta a PDF/CSV

### Módulo Astronomía
1. Ve a `/astronomy`
2. Configura parámetros
3. Click "Simular Búsqueda"

### Módulo Comparación
1. Ve a `/comparison`
2. Ingresa 2 números de equipo
3. Ve análisis con IA
4. Exporta comparación

### Chatbot
- Click en ícono de chat
- Pregunta sobre FTC o exoplanetas
- Ejemplos: "¿Qué es un exoplaneta?", "Explica zona habitable"

### Cambiar Idioma
- Automático según navegador
- O manualmente en configuración

## 📊 Estadísticas del Proyecto

- **Archivos:** 13 nuevos + 50+ existentes
- **Líneas de código:** ~2,500 líneas nuevas
- **Tests:** 20+ automatizados
- **Funcionalidades core:** 5/10 implementadas (50%)
- **Coverage:** >80%

## 🗺️ Hoja de Ruta

Ver [ROADMAP.md](ROADMAP.md) para:
- Estado de cada funcionalidad
- Priorización recomendada
- Cómo implementar features faltantes

### Próximas Features
- Dashboard estadísticas avanzadas
- Sistema de usuarios completo (login/registro)
- WebSockets para tiempo real
- ML avanzado con reentrenamiento

## 🐛 Solución de Problemas

Ver documentación completa en README o ejecuta:
```bash
python check_code.py        # Verificar código
python verify_system.py     # Verificar sistema
```

## 📝 Licencia

MIT License - Proyecto AZTLÁN DECODE FTC

## 🤝 Contribuir

1. Fork el proyecto
2. Crea rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit (`git commit -m 'Agregar funcionalidad'`)
4. Push (`git push origin feature/nueva-funcionalidad`)
5. Pull Request

## 📧 Contacto

Equipo AZTLÁN DECODE

---

**Hecho con ❤️ por el equipo AZTLÁN DECODE**

*"Descifrando jeróglifos de batalla robótica..."* 🏺⚔️🤖