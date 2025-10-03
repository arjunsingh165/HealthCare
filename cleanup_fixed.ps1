# Healthcare Management System - Git Cleanup Script (PowerShell)
# This script removes files that should be ignored by git

Write-Host "Cleaning up files that should not be in git..." -ForegroundColor Green

# Remove all __pycache__ directories
Write-Host "Removing __pycache__ directories..." -ForegroundColor Yellow
Get-ChildItem -Path . -Recurse -Directory -Name "__pycache__" | ForEach-Object {
    $fullPath = $_.FullName
    if (Test-Path $fullPath) {
        Remove-Item -Path $fullPath -Recurse -Force
        Write-Host "Removed: $fullPath" -ForegroundColor Gray
    }
}

# Remove all .pyc files
Write-Host "Removing .pyc files..." -ForegroundColor Yellow
Get-ChildItem -Path . -Recurse -File -Name "*.pyc" | ForEach-Object {
    Remove-Item -Path $_.FullName -Force
    Write-Host "Removed: $($_.Name)" -ForegroundColor Gray
}

# Remove temporary files
Write-Host "Removing temporary files..." -ForegroundColor Yellow
$tempFiles = Get-ChildItem -Path . -Recurse -File | Where-Object { $_.Extension -in @('.tmp', '.temp', '.bak', '.old') }
foreach ($file in $tempFiles) {
    Remove-Item -Path $file.FullName -Force
    Write-Host "Removed: $($file.Name)" -ForegroundColor Gray
}

# Remove log files
Write-Host "Removing log files..." -ForegroundColor Yellow
Get-ChildItem -Path . -Recurse -File -Name "*.log" | ForEach-Object {
    Remove-Item -Path $_.FullName -Force
    Write-Host "Removed: $($_.Name)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Cleanup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "- Removed __pycache__ directories" -ForegroundColor White
Write-Host "- Removed .pyc compiled files" -ForegroundColor White
Write-Host "- Removed temporary files" -ForegroundColor White
Write-Host "- Removed log files" -ForegroundColor White
Write-Host ""
Write-Host "Manual review needed for:" -ForegroundColor Yellow
Write-Host "- test_*.py files (currently preserved)" -ForegroundColor White
Write-Host "- .env file (contains sensitive data)" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Review the .gitignore file" -ForegroundColor White
Write-Host "2. Initialize git: git init" -ForegroundColor White
Write-Host "3. Add files: git add ." -ForegroundColor White
Write-Host "4. Commit: git commit -m Initial_commit" -ForegroundColor White