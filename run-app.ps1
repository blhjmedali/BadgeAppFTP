$ErrorActionPreference = "Stop"

Set-Location -Path $PSScriptRoot

if (-not (Test-Path ".\requirements.txt")) {
  throw "requirements.txt not found in $PSScriptRoot"
}

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
  py -3 -m venv .venv
}

.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements.txt

.\.venv\Scripts\python manage.py migrate

# Seed demo admin + sample data (safe to re-run)
.\.venv\Scripts\python manage.py seed_demo

$port = 8000
if (Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue) {
  Write-Host "Warning: Port $port is already in use. If the server is already running, open http://127.0.0.1:$port/." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "App starting at http://127.0.0.1:8000/"
Write-Host "Login: admin  Password: admin123"
Write-Host ""
Write-Host "If PowerShell blocks scripts, run:" -ForegroundColor DarkGray
Write-Host "  powershell -ExecutionPolicy Bypass -File .\run-app.ps1" -ForegroundColor DarkGray
Write-Host ""

.\.venv\Scripts\python manage.py runserver 127.0.0.1:8000

