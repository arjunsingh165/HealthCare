# Healthcare Management System - Git Cleanup Script (PowerShell)
# This script removes files that should be ignored by git

Write-Host "🧹 Cleaning up files that should not be in git..." -ForegroundColor Green

# Remove all __pycache__ directories
Write-Host "Removing __pycache__ directories..." -ForegroundColor Yellow
Get-ChildItem -Path . -Recurse -Directory -Name "__pycache__" | ForEach-Object {
    $path = Join-Path -Path (Get-Location) -ChildPath $_
    if (Test-Path $path) {
        Remove-Item -Path $path -Recurse -Force
        Write-Host "  Removed: $_" -ForegroundColor Gray
    }
}

# Remove all .pyc files
Write-Host "Removing .pyc files..." -ForegroundColor Yellow
Get-ChildItem -Path . -Recurse -File -Name "*.pyc" | ForEach-Object {
    $path = Join-Path -Path (Get-Location) -ChildPath $_
    if (Test-Path $path) {
        Remove-Item -Path $path -Force
        Write-Host "  Removed: $_" -ForegroundColor Gray
    }
}

# Remove test files (optional - comment out if you want to keep them)
Write-Host "Test files found (not removed automatically):" -ForegroundColor Yellow
Get-ChildItem -Path . -File -Name "test_*.py" | ForEach-Object {
    Write-Host "  Found: $_" -ForegroundColor Gray
}

# Remove temporary files
Write-Host "Removing temporary files..." -ForegroundColor Yellow
$tempPatterns = @("*.tmp", "*.temp", "*.bak", "*.old")
foreach ($pattern in $tempPatterns) {
    Get-ChildItem -Path . -Recurse -File -Name $pattern | ForEach-Object {
        $path = Join-Path -Path (Get-Location) -ChildPath $_
        if (Test-Path $path) {
            Remove-Item -Path $path -Force
            Write-Host "  Removed: $_" -ForegroundColor Gray
        }
    }
}

# Remove log files
Write-Host "Removing log files..." -ForegroundColor Yellow
Get-ChildItem -Path . -Recurse -File -Name "*.log" | ForEach-Object {
    $path = Join-Path -Path (Get-Location) -ChildPath $_
    if (Test-Path $path) {
        Remove-Item -Path $path -Force
        Write-Host "  Removed: $_" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "✅ Cleanup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Summary:" -ForegroundColor Cyan
Write-Host "   - Removed __pycache__ directories" -ForegroundColor White
Write-Host "   - Removed .pyc compiled files" -ForegroundColor White
Write-Host "   - Removed temporary files (tmp, temp, bak, old)" -ForegroundColor White
Write-Host "   - Removed log files" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  Manual review needed for:" -ForegroundColor Yellow
Write-Host "   - test_*.py files (currently preserved)" -ForegroundColor White
Write-Host "   - .env file (contains sensitive data)" -ForegroundColor White
Write-Host "   - Database files (if any)" -ForegroundColor White
Write-Host "   - Media/upload directories" -ForegroundColor White
Write-Host ""
Write-Host "🔧 To remove test files manually, run:" -ForegroundColor Cyan
Write-Host "   Remove-Item test_*.py" -ForegroundColor Gray
Write-Host ""
Write-Host "📝 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Review the .gitignore file" -ForegroundColor White
Write-Host "   2. Initialize git: git init" -ForegroundColor White
Write-Host "   3. Add files: git add ." -ForegroundColor White
Write-Host "   4. Commit: git commit -m `"Initial commit`"" -ForegroundColor White