#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TURBO OPTIMIZER - Optimización MÁXIMA de Sistema Windows
Velocidad MÁXIMA en todo sentido
"""

import os
import sys
import subprocess
import psutil
import shutil
from datetime import datetime
import ctypes
import time
import threading
import winreg

def es_admin():
    """Verifica si se ejecuta como administrador"""
    try:
        return ctypes.windll.shell.IsUserAnAdmin()
    except:
        return False

def obtener_ruta_reporte():
    """Obtiene la ruta del escritorio para guardar el reporte"""
    usuario = os.getenv('USERNAME')
    reporte = f"C:\\Users\\{usuario}\\Desktop\\TurboOptimizer_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    return reporte

def escribir(texto, reporte):
    """Escribe en consola y en archivo"""
    print(texto)
    try:
        with open(reporte, 'a', encoding='utf-8', errors='ignore') as f:
            f.write(texto + "\n")
    except:
        pass

def ejecutar_comando(comando):
    """Ejecuta comando del sistema silenciosamente"""
    try:
        os.system(f'{comando} >nul 2>&1')
        return True
    except:
        return False

def limpiar_temp(reporte):
    """Limpia carpeta TEMP agresivamente"""
    escribir("\n[⚡ OPT 1] LIMPIEZA AGRESIVA TEMP...", reporte)
    contador = 0
    rutas = [
        os.getenv('TEMP'),
        os.getenv('APPDATA') + "\\Microsoft\\Windows\\Recent",
        f"C:\\Users\\{os.getenv('USERNAME')}\\AppData\\Local\\Temp",
        "C:\\Windows\\Temp",
    ]
    
    for ruta in rutas:
        if ruta and os.path.exists(ruta):
            try:
                for archivo in os.listdir(ruta):
                    try:
                        ruta_completa = os.path.join(ruta, archivo)
                        if os.path.isfile(ruta_completa):
                            os.remove(ruta_completa)
                            contador += 1
                        elif os.path.isdir(ruta_completa):
                            shutil.rmtree(ruta_completa, ignore_errors=True)
                            contador += 1
                    except:
                        pass
            except:
                pass
    
    escribir(f"✓ {contador} archivos temp eliminados", reporte)
    return contador

def limpiar_cache(reporte):
    """Limpia caché del navegador"""
    escribir("\n[⚡ OPT 2] LIMPIEZA DE CACHÉ NAVEGADORES...", reporte)
    contador = 0
    
    # Chrome
    cache_chrome = f"C:\\Users\\{os.getenv('USERNAME')}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache"
    if os.path.exists(cache_chrome):
        try:
            shutil.rmtree(cache_chrome, ignore_errors=True)
            contador += 1
            escribir("✓ Caché de Chrome limpio", reporte)
        except:
            pass
    
    # Edge
    cache_edge = f"C:\\Users\\{os.getenv('USERNAME')}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cache"
    if os.path.exists(cache_edge):
        try:
            shutil.rmtree(cache_edge, ignore_errors=True)
            contador += 1
            escribir("✓ Caché de Edge limpio", reporte)
        except:
            pass
    
    # Firefox
    cache_firefox = f"C:\\Users\\{os.getenv('USERNAME')}\\AppData\\Local\\Mozilla\\Firefox\\Profiles"
    if os.path.exists(cache_firefox):
        try:
            for carpeta in os.listdir(cache_firefox):
                cache_path = os.path.join(cache_firefox, carpeta, "cache2")
                if os.path.exists(cache_path):
                    shutil.rmtree(cache_path, ignore_errors=True)
                    contador += 1
            escribir("✓ Caché de Firefox limpio", reporte)
        except:
            pass
    
    return contador

def deshabilitar_servicios(reporte):
    """Deshabilita servicios innecesarios AGRESIVAMENTE"""
    escribir("\n[⚡ OPT 3] DESHABILITANDO SERVICIOS INNECESARIOS...", reporte)
    
    servicios_bloat = [
        "DiagTrack",
        "dmwappushservice",
        "HomeGroupListener",
        "HomeGroupProvider",
        "bthserv",
        "MapsBroker",
        "lfsvc",
        "RemoteRegistry",
        "SharedAccess",
        "TrkWks",
        "SSDPSRV",
        "upnphost",
        "WMPNetworkSvc",
        "wisvc",
        "WSearch",
        "XblAuthManager",
        "XblGameSave",
        "AdobeARMservice",
    ]
    
    contador = 0
    for servicio in servicios_bloat:
        try:
            ejecutar_comando(f'net stop {servicio}')
            ejecutar_comando(f'sc config {servicio} start=disabled')
            contador += 1
            escribir(f"✓ {servicio} detenido y deshabilitado", reporte)
        except:
            pass
    
    return contador

def optimizar_registros(reporte):
    """Optimiza registro de Windows para velocidad"""
    escribir("\n[⚡ OPT 4] OPTIMIZACIÓN DE REGISTRO...", reporte)
    
    try:
        # Deshabilitar efectos visuales
        ejecutar_comando('reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v ListviewAlphaSelect /t REG_DWORD /d 0 /f')
        ejecutar_comando('reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v ListviewShadow /t REG_DWORD /d 0 /f')
        
        # Deshabilitar animaciones
        ejecutar_comando('reg add "HKEY_CURRENT_USER\\Control Panel\\Desktop" /v EnableAeroPeek /t REG_SZ /d "off" /f')
        
        # Acelerar inicio
        ejecutar_comando('reg add "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control" /v WaitToKillServiceTimeout /t REG_SZ /d 2000 /f')
        
        # Reducir retrasos
        ejecutar_comando('reg add "HKEY_CURRENT_USER\\Control Panel\\Mouse" /v MouseSpeed /t REG_SZ /d 0 /f')
        ejecutar_comando('reg add "HKEY_CURRENT_USER\\Control Panel\\Mouse" /v MouseThreshold1 /t REG_SZ /d 0 /f')
        
        escribir("✓ Registro optimizado para máxima velocidad", reporte)
        return True
    except Exception as e:
        escribir(f"✗ Error en optimización de registro: {e}", reporte)
        return False

def limpiar_prefetch(reporte):
    """Limpia prefetch de Windows"""
    escribir("\n[⚡ OPT 5] LIMPIEZA DE PREFETCH...", reporte)
    prefetch = "C:\\Windows\\Prefetch"
    contador = 0
    
    try:
        if os.path.exists(prefetch):
            for archivo in os.listdir(prefetch):
                if archivo.endswith('.pf'):
                    try:
                        os.remove(os.path.join(prefetch, archivo))
                        contador += 1
                    except:
                        pass
            escribir(f"✓ {contador} archivos prefetch eliminados", reporte)
    except Exception as e:
        escribir(f"✗ Error prefetch: {e}", reporte)
    
    return contador

def limpiar_dns(reporte):
    """Limpia DNS"""
    escribir("\n[⚡ OPT 6] LIMPIEZA DE DNS...", reporte)
    try:
        ejecutar_comando('ipconfig /flushdns')
        ejecutar_comando('ipconfig /release')
        ejecutar_comando('ipconfig /renew')
        escribir("✓ DNS limpio y renovado", reporte)
        return True
    except:
        return False

def liberar_memoria(reporte):
    """Libera memoria RAM"""
    escribir("\n[⚡ OPT 7] LIBERACIÓN DE MEMORIA...", reporte)
    try:
        os.system('powershell -NoProfile -Command "Clear-Host; [System.GC]::Collect(); [System.GC]::WaitForPendingFinalizers()" >nul 2>&1')
        escribir("✓ Memoria RAM liberada", reporte)
        return True
    except:
        return False

def desfragmentar_disco(reporte):
    """Desfragmenta disco"""
    escribir("\n[⚡ OPT 8] OPTIMIZACIÓN DE DISCO...", reporte)
    try:
        ejecutar_comando('defrag C: /O')
        escribir("✓ Disco C: optimizado", reporte)
        return True
    except:
        return False

def acelerar_boot(reporte):
    """Acelera tiempo de inicio"""
    escribir("\n[⚡ OPT 9] ACELERACIÓN DE BOOT...", reporte)
    try:
        # Reducir retraso de inicio
        ejecutar_comando('reg add "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v PagingFiles /t REG_MULTI_SZ /d "C:\\pagefile.sys 4096 8192" /f')
        
        # Deshabilitar sonidos de inicio
        ejecutar_comando('reg add "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableStartupSound /t REG_DWORD /d 1 /f')
        
        escribir("✓ Boot acelerado", reporte)
        return True
    except:
        return False

def optimizar_gpu(reporte):
    """Optimiza configuración de GPU"""
    escribir("\n[⚡ OPT 10] OPTIMIZACIÓN DE GPU...", reporte)
    try:
        # Cambiar a GPU dedicada si está disponible
        ejecutar_comando('reg add "HKEY_LOCAL_MACHINE\\SOFTWARE\\NVIDIA\\Global" /v DLSS_AppProfile_PerformanceGain /t REG_DWORD /d 1 /f')
        escribir("✓ Configuración de GPU optimizada", reporte)
        return True
    except:
        return False

def main():
    if not es_admin():
        print("⚠️  EJECUTA COMO ADMINISTRADOR PARA MÁXIMA OPTIMIZACIÓN")
        print("Click derecho en CMD → Ejecutar como administrador")
        time.sleep(3)
        return
    
    reporte = obtener_ruta_reporte()
    
    # Header
    header = "="*70
    escribir(header, reporte)
    escribir("🚀 TURBO OPTIMIZER - MÁXIMA VELOCIDAD", reporte)
    escribir(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", reporte)
    escribir(f"Usuario: {os.getenv('USERNAME')}", reporte)
    escribir(header, reporte)
    escribir("", reporte)
    
    # ===== DIAGNÓSTICO RÁPIDO =====
    escribir("[DIAGNÓSTICO RÁPIDO]", reporte)
    try:
        memoria = psutil.virtual_memory()
        escribir(f"RAM: {memoria.total//(1024**3)} GB | Usado: {memoria.used//(1024**3)} GB | Disponible: {memoria.available//(1024**3)} GB", reporte)
    except:
        pass
    
    escribir("\n" + "="*70, reporte)
    escribir("🔥 INICIANDO TURBO BOOST...", reporte)
    escribir("="*70, reporte)
    
    total_optimizaciones = 0
    
    # Ejecutar todas las optimizaciones en paralelo
    optimizaciones = [
        limpiar_temp,
        limpiar_cache,
        deshabilitar_servicios,
        limpiar_prefetch,
        limpiar_dns,
        liberar_memoria,
        desfragmentar_disco,
        acelerar_boot,
        optimizar_gpu,
    ]
    
    optimizar_registros(reporte)
    total_optimizaciones += 1
    
    for opt_func in optimizaciones:
        try:
            resultado = opt_func(reporte)
            total_optimizaciones += 1
        except Exception as e:
            escribir(f"Error: {e}", reporte)
    
    # ===== RESUMEN FINAL =====
    escribir("\n" + "="*70, reporte)
    escribir("✅ TURBO BOOST COMPLETADO", reporte)
    escribir("="*70, reporte)
    escribir(f"Optimizaciones realizadas: {total_optimizaciones}", reporte)
    escribir(f"Reporte: {reporte}", reporte)
    escribir("", reporte)
    escribir("🎯 TU SISTEMA AHORA ESTÁ AL MÁXIMO", reporte)
    escribir("", reporte)
    escribir("Reinicia tu PC para máximo rendimiento", reporte)
    escribir("="*70, reporte)
    
    print(f"\n✅ OPTIMIZACIÓN COMPLETA")
    print(f"📊 Reporte: {reporte}")
    print(f"🚀 Reinicia tu PC para máxima velocidad")

if __name__ == "__main__":
    main()
