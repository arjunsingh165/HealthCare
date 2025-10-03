#!/usr/bin/env bash

# Healthcare Management System - Git Cleanup Script
# This script removes files that should be ignored by git

echo "🧹 Cleaning up files that should not be in git..."

# Remove all __pycache__ directories
echo "Removing __pycache__ directories..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Remove all .pyc files
echo "Removing .pyc files..."
find . -name "*.pyc" -delete 2>/dev/null

# Remove test files (optional - comment out if you want to keep them)
echo "Removing test files..."
# rm -f test_*.py 2>/dev/null

# Remove temporary files
echo "Removing temporary files..."
rm -f *.tmp *.temp 2>/dev/null

# Remove log files
echo "Removing log files..."
rm -f *.log 2>/dev/null

# Remove database files (if using SQLite for development)
echo "Removing SQLite database files..."
# rm -f db.sqlite3 *.db 2>/dev/null

# Remove static collected files
echo "Removing collected static files..."
# rm -rf staticfiles/ static_root/ 2>/dev/null

# Remove media uploads (be careful with this!)
echo "Note: Media files NOT removed automatically - review manually"
# rm -rf media/ uploads/ 2>/dev/null

echo "✅ Cleanup complete!"
echo ""
echo "📋 Files removed:"
echo "   - __pycache__ directories"
echo "   - .pyc compiled files"
echo "   - Temporary files"
echo "   - Log files"
echo ""
echo "⚠️  Manual review needed for:"
echo "   - test_*.py files (currently preserved)"
echo "   - database files (currently preserved)"
echo "   - media/upload files (currently preserved)"
echo ""
echo "🔧 To remove test files, uncomment the test removal line in this script"
echo "🔧 To remove database, uncomment the database removal line in this script"