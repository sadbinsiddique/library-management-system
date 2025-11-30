@echo off
setlocal

REM Build single-file executable with PyInstaller (Windows cmd)

REM Ensure pyinstaller is installed in your active Python environment
where pyinstaller >nul 2>nul
if errorlevel 1 (
  echo Installing pyinstaller...
  pip install pyinstaller || goto :error
)

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
REM Keep existing spec if present; we'll build from CLI args

REM Build the executable
pyinstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --name library-management-system ^
  --add-data "database;database" ^
  main.py || goto :error

echo.
echo Build complete. Find the exe at .\dist\library-management-system.exe
exit /b 0

:error
echo Build failed. See output above for details.
exit /b 1
