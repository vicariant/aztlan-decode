# ================================================================
# CONVERTIR AZTLÁN DECODE EN REPOSITORIO GIT
# ================================================================

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "   INICIALIZANDO REPOSITORIO GIT LOCAL" -ForegroundColor Yellow -BackgroundColor Black
Write-Host "================================================================`n" -ForegroundColor Cyan

# Verificar Git
try {
    $null = git --version 2>&1
    Write-Host " [OK] Git detectado`n" -ForegroundColor Green
} catch {
    Write-Host " [ERROR] Git no instalado`n" -ForegroundColor Red
    Write-Host " Instala Git primero:" -ForegroundColor Yellow
    Write-Host "   1. Ejecuta: winget install Git.Git" -ForegroundColor White
    Write-Host "   2. Reinicia PowerShell" -ForegroundColor White
    Write-Host "   3. Vuelve a ejecutar este script`n" -ForegroundColor White
    pause
    exit 1
}

# Inicializar repo
if (Test-Path .git) {
    Write-Host " [INFO] Repositorio ya existe`n" -ForegroundColor Yellow
} else {
    Write-Host " [1/5] Inicializando repositorio..." -ForegroundColor Cyan
    git init
    Write-Host " [OK] Repositorio creado`n" -ForegroundColor Green
}

# Configurar usuario si es necesario
$userName = git config user.name
if (-not $userName) {
    Write-Host " [CONFIG] Primera vez usando Git" -ForegroundColor Yellow
    Write-Host ""
    $name = Read-Host " Ingresa tu nombre para Git"
    $email = Read-Host " Ingresa tu email para Git"
    git config --global user.name "$name"
    git config --global user.email "$email"
    Write-Host " [OK] Git configurado`n" -ForegroundColor Green
}

# Mostrar archivos que se agregarán
Write-Host " [2/5] Archivos a subir (incluyendo i18n):" -ForegroundColor Cyan
Write-Host ""
Write-Host "   locales/es.json              - Español" -ForegroundColor Green
Write-Host "   locales/en.json              - Inglés" -ForegroundColor Green
Write-Host "   utils/i18n.py                - Sistema i18n" -ForegroundColor Green
Write-Host "   database/models.py           - 7 modelos DB" -ForegroundColor White
Write-Host "   utils/report_exporter.py     - Export PDF/CSV" -ForegroundColor White
Write-Host "   static/manifest.json, sw.js  - PWA" -ForegroundColor White
Write-Host "   tests/test_comprehensive.py  - Tests" -ForegroundColor White
Write-Host "   README.md, ROADMAP.md        - Docs" -ForegroundColor White
Write-Host "   ... y 60+ archivos más" -ForegroundColor Gray
Write-Host ""

# Agregar archivos
Write-Host " [3/5] Agregando archivos..." -ForegroundColor Cyan
git add .
Write-Host " [OK] Archivos agregados`n" -ForegroundColor Green

# Crear commit
Write-Host " [4/5] Creando commit inicial..." -ForegroundColor Cyan
git commit -m "feat: Sistema completo Aztlan Decode

✨ Funcionalidades implementadas:
- 🌍 Sistema de internacionalización completo (ES/EN)
- 🗄️ Base de datos SQLite con 7 modelos
- 📥 Exportación PDF/CSV/Excel profesional
- 📱 PWA instalable con Service Worker
- 🧪 Tests automatizados con pytest (20+)
- 🚀 Configuración Heroku deployment
- 📚 Documentación completa (README, ROADMAP)
- 🎨 Temas visuales inmersivos animados
- 🤖 Chatbot con IA integrado

📊 Estadísticas:
- 70+ archivos
- 2,500+ líneas de código nuevo
- 200+ traducciones por idioma
- 5/10 features críticas implementadas (50%)"

if ($LASTEXITCODE -eq 0) {
    Write-Host " [OK] Commit creado`n" -ForegroundColor Green
} else {
    Write-Host " [ERROR] No se pudo crear commit`n" -ForegroundColor Red
    pause
    exit 1
}

# Configurar rama main
Write-Host " [5/5] Configurando rama principal..." -ForegroundColor Cyan
git branch -M main
Write-Host " [OK] Rama 'main' configurada`n" -ForegroundColor Green

# Configurar remote
Write-Host " [REMOTE] Conectando con GitHub..." -ForegroundColor Cyan
$remoteExists = git remote | Select-String "origin"
if ($remoteExists) {
    git remote set-url origin https://github.com/vicariant/aztlanfinal.git
    Write-Host " [OK] Remote actualizado`n" -ForegroundColor Green
} else {
    git remote add origin https://github.com/vicariant/aztlanfinal.git
    Write-Host " [OK] Remote agregado`n" -ForegroundColor Green
}

# Resumen
Write-Host "================================================================" -ForegroundColor Green
Write-Host "   REPOSITORIO LOCAL LISTO" -ForegroundColor Green -BackgroundColor Black
Write-Host "================================================================`n" -ForegroundColor Green

Write-Host " Ahora ejecuta para subir a GitHub:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host " O si el repo ya tiene contenido:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   git pull origin main --rebase" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "================================================================`n" -ForegroundColor Green

# Preguntar si quiere hacer push ahora
$push = Read-Host " ¿Quieres hacer push ahora? (s/n)"
if ($push -eq "s" -or $push -eq "S") {
    Write-Host "`n [PUSH] Subiendo a GitHub..." -ForegroundColor Cyan
    Write-Host " (Puede pedir autenticación)`n" -ForegroundColor Gray
    
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n================================================================" -ForegroundColor Green
        Write-Host "   ✅ ÉXITO - CÓDIGO SUBIDO A GITHUB" -ForegroundColor Green -BackgroundColor Black
        Write-Host "================================================================`n" -ForegroundColor Green
        Write-Host " Tu repositorio:" -ForegroundColor Cyan
        Write-Host " https://github.com/vicariant/aztlanfinal`n" -ForegroundColor White
    } else {
        Write-Host "`n [INFO] Si hay conflictos, ejecuta:" -ForegroundColor Yellow
        Write-Host " git pull origin main --rebase" -ForegroundColor White
        Write-Host " git push -u origin main`n" -ForegroundColor White
    }
}

Write-Host " Presiona cualquier tecla para cerrar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
