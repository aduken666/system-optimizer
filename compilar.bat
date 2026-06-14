@echo off
REM Script para compilar Python a EXE
REM Requiere tener Python y PyInstaller instalados

echo Instalando dependencias...
pip install -q pyinstaller psutil

echo.
echo Compilando a EXE...
pyinstaller --onefile --windowed --icon=icon.ico --name=DiagnosticoOptimizador diagnostico_optimizador.py

echo.
echo Proceso completado!
echo El EXE esta en la carpeta: dist\DiagnosticoOptimizador.exe
pause
