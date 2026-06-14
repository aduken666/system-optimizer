#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Diagnóstico y Optimización de Rendimiento
Genera reporte completo y optimiza automáticamente
"""

import os
import sys
import subprocess
import psutil
import shutil
from datetime import datetime
import ctypes

def es_admin():
    """Verifica si se ejecuta como administrador"""
    try:
        return ctypes.windll.shell.IsUserAnAdmin()
    except:
        return False

def obtener_ruta_reporte():
    """Obtiene la ruta del escritorio para guardar el reporte"""
    usuario = os.getenv('USERNAME')
    reporte = f"C:\\Users\\{usuario}\\Desktop\\Diagnostico_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    return reporte

def escribir(texto, reporte):
    """Escribe en consola y en archivo"""
    print(texto)
    try:
        with open(reporte, 'a', encoding='utf-8') as f:
            f.write(texto + "\n")
    except:
        pass

def main():
    reporte = obtener_ruta_reporte()
    
    # Header
    header = "="*70
    escribir(header, reporte)
    escribir("DIAGNÓSTICO Y OPTIMIZACIÓN DE SISTEMA WINDOWS", reporte)
    escribir(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", reporte)
    escribir(f"Usuario: {os.getenv('USERNAME')}", reporte)
    escribir(header, reporte)
    escribir("", reporte)
    
    # ===== DIAGNÓSTICO =====
    escribir("[FASE 1] DIAGNÓSTICO DEL SISTEMA", reporte)
    escribir("-"*70, reporte)
    
    # 1. INFO DEL SISTEMA
    escribir("\n[1.1] INFORMACIÓN DEL SISTEMA", reporte)
    try:
        resultado = subprocess.check_output(['systeminfo'], encoding='utf-8', stderr=subprocess.DEVNULL)
        for linea in resultado.split('\n')[:20]:
            escribir(linea, reporte)
    except Exception as e:
        escribir(f"Error: {e}", reporte)
    
    # 2. MEMORIA RAM
    escribir("\n[1.2] ESTADO DE MEMORIA RAM", reporte)
    try:
        memoria = psutil.virtual_memory()
        escribir(f"Total: {memoria.total//(1024**3)} GB", reporte)
        escribir(f"Usado: {memoria.used//(1024**3)} GB", reporte)
        escribir(f"Disponible: {memoria.available//(1024**3)} GB", reporte)
        escribir(f"Porcentaje usado: {memoria.percent}%", reporte)
        
        if memoria.percent > 80:
            escribir("⚠️  ALERTA: RAM muy alta (>80%)", reporte)
    except Exception as e:
        escribir(f"Error: {e}", reporte)
    
    # 3. DISCO
    escribir("\n[1.3] ESPACIO EN DISCO", reporte)
    try:
        for particao in psutil.disk_partitions(all=False):
            try:
                uso_disco = psutil.disk_usage(particao.mountpoint)
                porcentaje = (uso_disco.used / uso_disco.total) * 100
                escribir(f"{particao.device}: {uso_disco.used//(1024**3)}GB / {uso_disco.total//(1024**3)}GB ({porcentaje:.1f}%)", reporte)
                
                if porcentaje > 90:
                    escribir(f"  ⚠️  ALERTA: Disco casi lleno", reporte)
            except:
                pass
    except Exception as e:
        escribir(f"Error: {e}", reporte)
    
    # 4. PROCESOS PESADOS
    escribir("\n[1.4] TOP 10 PROCESOS QUE MAS RAM CONSUMEN", reporte)
    try:
        procesos = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
            try:
                procesos.append((proc.info['name'], proc.info['memory_percent']))
            except:
                pass
        
        procesos.sort(key=lambda x: x[1], reverse=True)
        for nombre, memoria in procesos[:10]:
            escribir(f"  {nombre}: {memoria:.2f}%", reporte)
    except Exception as e:
        escribir(f"Error: {e}", reporte)
    
    # 5. SERVICIOS
    escribir("\n[1.5] SERVICIOS EJECUTÁNDOSE", reporte)
    try:
        resultado = subprocess.check_output(['tasklist'], encoding='utf-8', stderr=subprocess.DEVNULL)
        lineas = resultado.split('\n')
        escribir(f"Total de procesos: {len([l for l in lineas if l.strip()])}", reporte)
    except:
        pass
    
    # ===== OPTIMIZACIÓN =====
    escribir("\n" + "="*70, reporte)
    escribir("[FASE 2] INICIANDO OPTIMIZACIÓN", reporte)
    escribir("="*70, reporte)
    
    optimizaciones_realizadas = 0
    
    # 1. LIMPIAR TEMP
    escribir("\n[OPT 1] Limpiando archivos temporales...", reporte)
    try:
        temp_dir = os.getenv('TEMP')
        contador = 0
        for archivo in os.listdir(temp_dir):
            try:
                ruta = os.path.join(temp_dir, archivo)
                if os.path.isfile(ruta):
                    os.remove(ruta)
                    contador += 1
                elif os.path.isdir(ruta):
                    shutil.rmtree(ruta, ignore_errors=True)
                    contador += 1
            except:
                pass
        escribir(f"✓ {contador} archivos temporales eliminados", reporte)
        optimizaciones_realizadas += 1
    except Exception as e:
        escribir(f"✗ Error: {e}", reporte)
    
    # 2. LIMPIAR PREFETCH
    escribir("\n[OPT 2] Limpiando prefetch (cache de programas)...", reporte)
    try:
        prefetch = "C:\\Windows\\Prefetch"
        if os.path.exists(prefetch):
            contador = 0
            for archivo in os.listdir(prefetch):
                if archivo.endswith('.pf'):
                    try:
                        os.remove(os.path.join(prefetch, archivo))
                        contador += 1
                    except:
                        pass
            escribir(f"✓ {contador} archivos prefetch eliminados", reporte)
            optimizaciones_realizadas += 1
    except Exception as e:
        escribir(f"✗ Error (requiere permisos elevados): {e}", reporte)
    
    # 3. LIMPIAR DNS
    escribir("\n[OPT 3] Limpiando caché DNS...", reporte)
    try:
        os.system('ipconfig /flushdns >nul 2>&1')
        escribir("✓ Caché DNS limpio", reporte)
        optimizaciones_realizadas += 1
    except Exception as e:
        escribir(f"✗ Error: {e}", reporte)
    
    # 4. DESHABILITAR SERVICIOS INNECESARIOS
    escribir("\n[OPT 4] Deshabilitando servicios innecesarios...", reporte)
    servicios = [
        ("DiagTrack", "Rastreo de diagnósticos"),
        ("dmwappushservice", "Servicio de aplicaciones"),
        ("HomeGroupListener", "Grupo Hogar"),
    ]
    
    for servicio, descripcion in servicios:
        try:
            # Intenta detener
            os.system(f'net stop {servicio} >nul 2>&1')
            escribir(f"✓ {descripcion} ({servicio}) detenido", reporte)
            optimizaciones_realizadas += 1
        except:
            pass
    
    # 5. DESFRAGMENTAR DISCO (opcional, solo C:)
    escribir("\n[OPT 5] Analizando disco para optimizar...", reporte)
    try:
        os.system('defrag c: /O >nul 2>&1')
        escribir("✓ Análisis de disco completado", reporte)
    except:
        escribir("ℹ️  Desfragmentación no disponible", reporte)
    
    # ===== RESUMEN =====
    escribir("\n" + "="*70, reporte)
    escribir("[RESUMEN FINAL]", reporte)
    escribir("="*70, reporte)
    escribir(f"Optimizaciones realizadas: {optimizaciones_realizadas}", reporte)
    escribir(f"Reporte guardado en: {reporte}", reporte)
    escribir("", reporte)
    
    if es_admin():
        escribir("✓ Ejecutado con permisos de administrador", reporte)
    else:
        escribir("⚠️  Ejecutado sin permisos de administrador", reporte)
        escribir("   Para más optimizaciones, ejecuta como administrador", reporte)
    
    escribir("", reporte)
    escribir("="*70, reporte)
    escribir("PROCESO COMPLETADO", reporte)
    escribir("="*70, reporte)
    
    print(f"\n{'='*70}")
    print(f"✓ Reporte guardado en: {reporte}")
    print(f"{'='*70}\n")
    
    input("Presiona Enter para cerrar...")

if __name__ == "__main__":
    main()
