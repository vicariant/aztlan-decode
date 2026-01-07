# AZTLÁN DECODE - Deployment Guide

## Desplegar en Heroku

### Pasos para subir a Heroku desde GitHub:

1. **Subir código a GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Aztlan Decode FTC Scouting System"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/aztlan-decode.git
   git push -u origin main
   ```

2. **Crear app en Heroku:**
   - Ve a https://dashboard.heroku.com/apps
   - Click en "New" → "Create new app"
   - Nombre: `aztlan-decode` (o el que prefieras)
   - Región: United States

3. **Conectar GitHub a Heroku:**
   - En tu app de Heroku, ve a "Deploy" tab
   - Deployment method: Selecciona "GitHub"
   - Busca tu repositorio `aztlan-decode`
   - Click "Connect"

4. **Configurar variables de entorno:**
   - Ve a "Settings" tab
   - Click "Reveal Config Vars"
   - Agrega las siguientes variables:
     ```
     FLASK_SECRET_KEY=tu-clave-secreta-muy-segura-aqui
     GROQ_API_KEY=tu-groq-api-key-aqui
     TOA_API_KEY=tu-clave-toa (si tienes)
     SCOUT_API_KEY=tu-clave-scout (si tienes)
     FIRST_API_KEY=tu-clave-first (si tienes)
     ```

5. **Desplegar:**
   - En "Deploy" tab, sección "Manual deploy"
   - Selecciona branch `main`
   - Click "Deploy Branch"
   - Espera a que termine (tarda 2-3 minutos)

6. **Verificar:**
   - Click en "Open app" o ve a: https://aztlan-decode.herokuapp.com
   - Todas las funciones deberían funcionar igual que en local

### Desplegar actualizaciones:

Cada vez que hagas cambios y los subas a GitHub:
```bash
git add .
git commit -m "Descripción de cambios"
git push origin main
```

Luego en Heroku:
- Ve a "Deploy" tab
- Click "Deploy Branch" en la sección Manual deploy
- O activa "Automatic deploys" para que se despliegue automáticamente

### Archivos necesarios para Heroku:

✅ **Procfile** - Comando para iniciar el servidor
✅ **runtime.txt** - Versión de Python
✅ **requirements.txt** - Dependencias de Python
✅ **.gitignore** - Archivos a ignorar

Todos estos archivos ya están creados en tu proyecto.

### Notas importantes:

- **Base de datos:** Heroku usa un sistema de archivos efímero. Si quieres persistencia de datos, considera usar PostgreSQL (addon gratuito de Heroku)
- **Archivos subidos:** Los archivos que los usuarios suban se borrarán cada 24 horas. Para persistencia, usa AWS S3
- **Memoria:** El plan gratuito de Heroku tiene 512 MB RAM. Tu app usa ~76 MB, así que está bien
- **Dyno hours:** El plan gratuito tiene 1000 horas/mes (suficiente si solo tú lo usas)

### Solución de problemas:

Ver logs en tiempo real:
```bash
heroku logs --tail -a aztlan-decode
```

Reiniciar la app:
```bash
heroku restart -a aztlan-decode
```

## Desplegar en otras plataformas:

### Railway.app (alternativa gratuita):
1. Conecta tu GitHub en railway.app
2. Selecciona el repo
3. Railway detecta automáticamente Flask
4. Agrega las variables de entorno
5. Deploy automático

### Render.com (alternativa gratuita):
1. Conecta GitHub en render.com
2. New Web Service
3. Selecciona el repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn app:app`
6. Agrega variables de entorno

¡Listo! Tu sistema estará en línea 🚀
