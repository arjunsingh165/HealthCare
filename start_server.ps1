# Healthcare Management System - Server Startup Script
Write-Host "🏥 Healthcare Management System" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Change to project directory
Set-Location "c:\Users\singh\OneDrive\Desktop\CODING\healthcare_management"

Write-Host "📂 Current directory: $PWD" -ForegroundColor Yellow

# Check if manage.py exists
if (Test-Path "manage.py") {
    Write-Host "✅ manage.py found" -ForegroundColor Green
} else {
    Write-Host "❌ manage.py not found" -ForegroundColor Red
    exit 1
}

# Run Django checks
Write-Host "🔍 Running Django checks..." -ForegroundColor Yellow
python manage.py check

# Start Django development server
Write-Host "🚀 Starting Django development server..." -ForegroundColor Green
Write-Host "📝 Backend will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📝 Admin panel at: http://localhost:8000/admin" -ForegroundColor Cyan
Write-Host "📝 Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver 0.0.0.0:8000