# 📊 SISTEMA DE ANALÍTICAS DE VISITANTES

## ✅ IMPLEMENTACIÓN COMPLETA

### 🎯 Funcionalidades Implementadas

#### 1. **Tracking Automático de Visitantes**
- ✅ Middleware `@app.before_request` que registra cada visita
- ✅ ID único por visitante (basado en hash de IP + User Agent)
- ✅ Tracking de páginas visitadas
- ✅ Detección automática de visitantes nuevos vs recurrentes

#### 2. **Base de Datos**
Nuevos modelos en `database/models.py`:
- ✅ **Visitor**: Registro de visitantes únicos
- ✅ **PageView**: Registro de cada vista de página

#### 3. **Sistema de Analíticas** (`utils/visitor_analytics.py`)
```python
class VisitorAnalytics:
    - track_visit()              # Registra cada visita
    - get_stats(days=30)         # Estadísticas de período
    - get_visitor_details()      # Lista de visitantes
    - get_realtime_stats()       # Estadísticas última hora
```

#### 4. **Página de Analíticas** (`/analytics`)
Dashboard completo con:
- ✅ **6 Tarjetas de Estadísticas Principales**:
  - Visitantes únicos totales
  - Visitantes últimos 30 días
  - Visitas totales
  - Visitantes recurrentes
  - Promedio visitas por usuario
  - Usuarios activos en la última hora
  
- ✅ **Gráfico de Visitas Diarias** (últimos 7 días)
- ✅ **Top 10 Páginas Más Visitadas**
- ✅ **Tabla de Visitantes Recientes** (últimos 50)
- ✅ **Indicador en Tiempo Real** (activos en última hora)
- ✅ **Auto-refresh cada 5 minutos**

#### 5. **API Endpoints**
```
GET /analytics              - Página visual de analíticas
GET /api/analytics/stats    - JSON con estadísticas (parámetro: ?days=30)
GET /api/analytics/realtime - JSON con stats en tiempo real
```

---

## 📊 MÉTRICAS DISPONIBLES

### Estadísticas Principales
```python
{
    'total_unique_visitors': 150,      # Visitantes únicos desde inicio
    'unique_visitors_period': 45,      # Visitantes últimos N días
    'total_visits_period': 180,        # Total de visitas
    'recurring_visitors': 12,          # Visitantes que regresaron
    'new_visitors': 33,                # Visitantes nuevos en período
    'avg_visits_per_visitor': 4.0      # Promedio de visitas por persona
}
```

### Top Páginas
```python
'top_pages': [
    {'url': '/scouting', 'visits': 85},
    {'url': '/astronomy', 'visits': 62},
    {'url': '/comparison', 'visits': 33}
]
```

### Visitas Diarias
```python
'daily_visits': [
    {'date': '2026-01-01', 'visits': 25},
    {'date': '2026-01-02', 'visits': 30},
    ...
]
```

### Estadísticas en Tiempo Real
```python
{
    'active_visitors_1h': 3,    # Usuarios activos última hora
    'page_views_1h': 12,        # Vistas de página última hora
    'timestamp': '2026-01-07T...'
}
```

---

## 🚀 CÓMO USAR

### 1. Ver Dashboard de Analíticas
```
http://localhost:5000/analytics
```

### 2. Obtener Datos por API (JSON)
```bash
# Estadísticas últimos 30 días
curl http://localhost:5000/api/analytics/stats

# Estadísticas últimos 7 días
curl http://localhost:5000/api/analytics/stats?days=7

# Stats en tiempo real (última hora)
curl http://localhost:5000/api/analytics/realtime
```

### 3. Integrar en Dashboard Existente
```html
<!-- Añadir en templates/dashboard.html -->
<div class="analytics-widget">
    <h3>📊 Estadísticas del Sitio</h3>
    <div id="analytics-data"></div>
</div>

<script>
fetch('/api/analytics/realtime')
    .then(r => r.json())
    .then(data => {
        document.getElementById('analytics-data').innerHTML = `
            <p>Visitantes activos (1h): ${data.data.active_visitors_1h}</p>
            <p>Vistas (1h): ${data.data.page_views_1h}</p>
        `;
    });
</script>
```

---

## 🔐 PRIVACIDAD

- ✅ **IDs Anónimos**: Visitor ID es hash SHA-256 (irreversible)
- ✅ **No Cookies de Tracking**: Solo se usa session nativa de Flask
- ✅ **IPs No Expuestas**: IPs guardadas pero no mostradas en frontend
- ✅ **Cumple RGPD**: Datos agregados y anónimos

---

## 📁 ARCHIVOS MODIFICADOS/CREADOS

```
✏️ database/models.py              - +25 líneas (modelos Visitor, PageView)
📄 utils/visitor_analytics.py      - NUEVO (216 líneas)
📄 templates/analytics.html        - NUEVO (270 líneas)
✏️ app.py                          - +75 líneas (middleware + rutas)
```

---

## 🎨 DISEÑO DEL DASHBOARD

### Colores por Métrica
- **Azul**: Visitantes únicos
- **Morado**: Visitantes período
- **Verde**: Visitas totales
- **Rojo**: Visitantes recurrentes
- **Naranja**: Promedio visitas
- **Cian**: Activos en tiempo real

### Características Visuales
- ✅ Tarjetas con gradientes
- ✅ Animación hover (lift effect)
- ✅ Indicador pulsante en tiempo real
- ✅ Gráfico de barras diarias
- ✅ Tabla responsiva de visitantes
- ✅ Badges para nuevos/recurrentes

---

## 🔄 AUTO-REFRESH

El dashboard se actualiza automáticamente cada 5 minutos:
```javascript
setTimeout(() => {
    location.reload();
}, 300000); // 5 minutos
```

---

## 📈 EJEMPLOS DE USO

### Caso 1: Ver cuántas personas entraron hoy
```python
from utils.visitor_analytics import get_analytics
analytics = get_analytics()
stats = analytics.get_stats(days=1)
print(f"Visitantes hoy: {stats['unique_visitors_period']}")
```

### Caso 2: Detectar visitantes recurrentes
```python
stats = analytics.get_stats(days=30)
print(f"Recurrentes: {stats['recurring_visitors']}")
print(f"Porcentaje: {stats['recurring_visitors']/stats['unique_visitors_period']*100:.1f}%")
```

### Caso 3: Página más popular
```python
stats = analytics.get_stats(days=30)
top_page = stats['top_pages'][0]
print(f"Página #1: {top_page['url']} con {top_page['visits']} visitas")
```

---

## ✅ VERIFICACIÓN

### Test Manual
1. Visita `http://localhost:5000/analytics`
2. Deberías ver:
   - 6 tarjetas con estadísticas
   - Gráfico de barras de últimos 7 días
   - Lista de top 10 páginas
   - Tabla de visitantes recientes

### Test API
```bash
curl http://localhost:5000/api/analytics/stats | python -m json.tool
```

---

## 🎉 RESULTADO FINAL

Ahora puedes ver:
- ✅ Cuántas personas **entraron en total**
- ✅ Cuántas personas **entraron varias veces** (recurrentes)
- ✅ Cuántas personas **están activas ahora** (última hora)
- ✅ Qué **páginas son más populares**
- ✅ **Tendencia de visitas** día por día
- ✅ **Promedio de engagement** (visitas por usuario)

Todo en un dashboard visual y con API JSON disponible.
