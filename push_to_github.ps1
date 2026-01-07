# ====================================================================
# SCRIPT PARA SUBIR AZTLÁN DECODE A GITHUB
# ====================================================================
# Ejecuta este script después de instalar Git
# ====================================================================

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "   SUBIENDO AZTLÁN DECODE A GITHUB" -ForegroundColor Yellow -BackgroundColor Black
Write-Host "================================================================`n" -ForegroundColor Cyan

# Verificar si Git está instalado
try {
    $gitVersion = git --version
    Write-Host " [OK] Git instalado: $gitVersion`n" -ForegroundColor Green
} catch {
    Write-Host " [ERROR] Git no está instalado" -ForegroundColor Red
    Write-Host "`n Instala Git primero:" -ForegroundColor Yellow
    Write-Host "   winget install Git.Git`n" -ForegroundColor White
    exit 1
}

# Verificar si ya hay un repositorio
if (Test-Path .git) {
    Write-Host " [INFO] Repositorio Git ya existe`n" -ForegroundColor Yellow
} else {
    Write-Host " [1/6] Inicializando repositorio..." -ForegroundColor Cyan
    git init
    Write-Host " [OK] Repositorio inicializado`n" -ForegroundColor Green
}

# Configurar usuario (si es primera vez)
$userName = git config user.name
if (-not $userName) {
    Write-Host " [CONFIG] Configurando Git por primera vez..." -ForegroundColor Yellow
    $name = Read-Host "   Ingresa tu nombre"
    $email = Read-Host "   Ingresa tu email"
    git config --global user.name "$name"
    git config --global user.email "$email"
    Write-Host " [OK] Git configurado`n" -ForegroundColor Green
}

# Verificar archivos críticos
Write-Host " [2/6] Verificando archivos..." -ForegroundColor Cyan
$criticalFiles = @(
    "README.md",
    "ROADMAP.md",
    "requirements.txt",
    "Procfile",
    "locales/es.json",
    "locales/en.json",
    "database/models.py",
    "utils/i18n.py"
)

$allExist = $true
foreach ($file in $criticalFiles) {
    if (Test-Path $file) {
        Write-Host "   [OK] $file" -ForegroundColor Green
    } else {
        Write-Host "   [FALTA] $file" -ForegroundColor Red
        $allExist = $false
    }
}

if (-not $allExist) {
    Write-Host "`n [ERROR] Faltan archivos críticos" -ForegroundColor Red
    exit 1
}

Write-Host "`n [OK] Todos los archivos presentes`n" -ForegroundColor Green

# Agregar archivos
Write-Host " [3/6] Agregando archivos al commit..." -ForegroundColor Cyan
git add .
Write-Host " [OK] Archivos agregados`n" -ForegroundColor Green

# Ver qué se va a subir
Write-Host " [INFO] Archivos que se subirán:" -ForegroundColor Yellow
git status --short | ForEach-Object { Write-Host "   $_" -ForegroundColor Gray }
Write-Host ""

# Crear commit
Write-Host " [4/6] Creando commit..." -ForegroundColor Cyan
git commit -m "feat: Sistema completo Aztlan Decode

- Sistema de internacionalización (ES/EN)
- Base de datos SQLite con 7 modelos
- Exportación PDF/CSV/Excel
- PWA instalable con Service Worker
- Tests automatizados con pytest
- Configuración Heroku deployment
- Documentación completa (README, ROADMAP)"

Write-Host " [OK] Commit creado`n" -ForegroundColor Green

# Renombrar rama a main
Write-Host " [5/6] Configurando rama main..." -ForegroundColor Cyan
git branch -M main
Write-Host " [OK] Rama configurada`n" -ForegroundColor Green

# Verificar si ya existe el remote
$remoteExists = git remote | Select-String "origin"
if ($remoteExists) {
    Write-Host " [INFO] Remote 'origin' ya existe, actualizando URL..." -ForegroundColor Yellow
    git remote set-url origin https://github.com/vicariant/aztlanfinal.git
} else {
    Write-Host " [INFO] Agregando remote 'origin'..." -ForegroundColor Cyan
    git remote add origin https://github.com/vicariant/aztlanfinal.git
}
Write-Host " [OK] Remote configurado`n" -ForegroundColor Green

# Push a GitHub
Write-Host " [6/6] Subiendo a GitHub..." -ForegroundColor Cyan
Write-Host "`n [IMPORTANTE] Se te pedirá autenticación de GitHub" -ForegroundColor Yellow
Write-Host "              Usa tu Personal Access Token como contraseña`n" -ForegroundColor Gray

try {
    git push -u origin main
    Write-Host "`n================================================================" -ForegroundColor Green
    Write-Host "   ÉXITO - PROYECTO SUBIDO A GITHUB" -ForegroundColor Green -BackgroundColor Black
    Write-Host "================================================================`n" -ForegroundColor Green
    Write-Host " Tu repositorio está en:" -ForegroundColor Cyan
    Write-Host " https://github.com/vicariant/aztlanfinal`n" -ForegroundColor White
    Write-Host " Próximos pasos:" -ForegroundColor Yellow
    Write-Host "   1. Ve a tu repo en GitHub" -ForegroundColor White
    Write-Host "   2. Verifica que todos los archivos estén" -ForegroundColor White
    Write-Host "   3. Para Heroku: Conecta GitHub desde Heroku Dashboard`n" -ForegroundColor White
} catch {
    Write-Host "`n [ERROR] No se pudo subir a GitHub" -ForegroundColor Red
    Write-Host "`n Posibles causas:" -ForegroundColor Yellow
    Write-Host "   1. No has creado un Personal Access Token" -ForegroundColor White
    Write-Host "   2. El token no tiene permisos 'repo'" -ForegroundColor White
    Write-Host "   3. El repositorio ya tiene contenido`n" -ForegroundColor White
    Write-Host " Para crear un token:" -ForegroundColor Cyan
    Write-Host "   GitHub > Settings > Developer settings > Personal access tokens > Tokens (classic)`n" -ForegroundColor Gray
}

Write-Host "================================================================`n" -ForegroundColor Cyan
