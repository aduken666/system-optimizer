@echo off
REM TURBO OPTIMIZER - Ejecución rápida
REM Click derecho y "Ejecutar como administrador"

cls
echo.
echo ======================================================================
echo                   🚀 TURBO OPTIMIZER v1.0
echo ======================================================================
echo.
echo Iniciando optimización MÁXIMA del sistema...
echo.
timeout /t 3 /nobreak

cd /d %~dp0
python turbo_optimizer.py

pause
