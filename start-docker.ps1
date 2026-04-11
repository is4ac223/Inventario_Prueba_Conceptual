# Script para ejecutar el proyecto con Docker Compose
# Uso: .\start-docker.ps1

param(
    [string]$command = "up",
    [switch]$build = $false,
    [switch]$detach = $true,
    [switch]$logs = $false
)

$projectPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
Set-Location $projectPath

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Docker Compose - Sistema Inventario" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Validar que Docker está instalado
try {
    $dockerVersion = docker --version
    Write-Host "✓ Docker encontrado: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker no está instalado o no está en el PATH" -ForegroundColor Red
    exit 1
}

# Validar que Docker Compose está instalado
try {
    $composeVersion = docker-compose --version
    Write-Host "✓ Docker Compose encontrado: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker Compose no está instalado" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Procesar comandos
switch ($command) {
    "up" {
        Write-Host "Iniciando contenedores..." -ForegroundColor Yellow
        $args = @("up")
        if ($build) { $args += "--build" }
        if ($detach) { $args += "-d" }
        docker-compose @args
        
        if ($detach) {
            Write-Host "✓ Contenedores iniciados en segundo plano" -ForegroundColor Green
            Write-Host ""
            Write-Host "Aplicación disponible en:" -ForegroundColor Cyan
            Write-Host "  - Frontend: http://localhost:5000" -ForegroundColor White
            Write-Host "  - Backend API: http://localhost:8000/api/" -ForegroundColor White
            Write-Host "  - Admin Django: http://localhost:8000/admin/" -ForegroundColor White
            Write-Host ""
            Write-Host "Ver logs: docker-compose logs -f" -ForegroundColor Gray
        }
        break
    }
    
    "down" {
        Write-Host "Deteniendo contenedores..." -ForegroundColor Yellow
        docker-compose down
        Write-Host "✓ Contenedores detenidos" -ForegroundColor Green
        break
    }
    
    "restart" {
        Write-Host "Reiniciando contenedores..." -ForegroundColor Yellow
        docker-compose restart
        Write-Host "✓ Contenedores reiniciados" -ForegroundColor Green
        break
    }
    
    "logs" {
        Write-Host "Mostrando logs (Ctrl+C para salir)..." -ForegroundColor Yellow
        docker-compose logs -f
        break
    }
    
    "build" {
        Write-Host "Construyendo imágenes..." -ForegroundColor Yellow
        docker-compose build --no-cache
        Write-Host "✓ Imágenes construidas" -ForegroundColor Green
        break
    }
    
    "status" {
        Write-Host "Estado de los contenedores:" -ForegroundColor Yellow
        docker-compose ps
        break
    }
    
    "clean" {
        Write-Host "Limpiando contenedores, volúmenes y datos..." -ForegroundColor Yellow
        Write-Host "⚠️  Advertencia: Esto eliminará la base de datos SQLite" -ForegroundColor Red
        $confirm = Read-Host "¿Deseas continuar? (s/n)"
        if ($confirm -eq "s" -or $confirm -eq "S") {
            docker-compose down -v
            Write-Host "✓ Limpieza completada" -ForegroundColor Green
        } else {
            Write-Host "Operación cancelada" -ForegroundColor Yellow
        }
        break
    }
    
    "test" {
        Write-Host "Probando conexión a los servicios..." -ForegroundColor Yellow
        Write-Host ""
        
        $backendUrl = "http://localhost:8000/api/"
        $frontendUrl = "http://localhost:5000"
        
        Write-Host "Probando Backend..." -ForegroundColor Cyan
        try {
            $response = Invoke-WebRequest -Uri $backendUrl -ErrorAction Stop
            Write-Host "✓ Backend disponible ($($response.StatusCode))" -ForegroundColor Green
        } catch {
            Write-Host "✗ Backend no responde" -ForegroundColor Red
        }
        
        Write-Host "Probando Frontend..." -ForegroundColor Cyan
        try {
            $response = Invoke-WebRequest -Uri $frontendUrl -ErrorAction Stop
            Write-Host "✓ Frontend disponible ($($response.StatusCode))" -ForegroundColor Green
        } catch {
            Write-Host "✗ Frontend no responde" -ForegroundColor Red
        }
        break
    }
    
    "help" {
        Write-Host "Comandos disponibles:" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "  up              - Inicia los contenedores" -ForegroundColor White
        Write-Host "  down            - Detiene los contenedores" -ForegroundColor White
        Write-Host "  restart         - Reinicia los contenedores" -ForegroundColor White
        Write-Host "  logs            - Muestra logs en tiempo real" -ForegroundColor White
        Write-Host "  build           - Construye las imágenes" -ForegroundColor White
        Write-Host "  status          - Muestra estado de contenedores" -ForegroundColor White
        Write-Host "  clean           - Elimina contenedores y volúmenes" -ForegroundColor White
        Write-Host "  test            - Prueba la conexión a los servicios" -ForegroundColor White
        Write-Host "  help            - Muestra esta ayuda" -ForegroundColor White
        Write-Host ""
        Write-Host "Ejemplos:" -ForegroundColor Cyan
        Write-Host "  .\start-docker.ps1                     # Inicia los contenedores" -ForegroundColor Gray
        Write-Host "  .\start-docker.ps1 up -build           # Construye e inicia" -ForegroundColor Gray
        Write-Host "  .\start-docker.ps1 logs                # Muestra logs" -ForegroundColor Gray
        Write-Host "  .\start-docker.ps1 down                # Detiene los contenedores" -ForegroundColor Gray
        break
    }
    
    default {
        Write-Host "Comando no reconocido: $command" -ForegroundColor Red
        Write-Host "Usa: .\start-docker.ps1 help" -ForegroundColor Yellow
    }
}

Write-Host ""
