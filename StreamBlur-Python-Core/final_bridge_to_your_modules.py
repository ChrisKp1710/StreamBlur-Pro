#!/usr/bin/env python3
"""
🚀 BRIDGE FINALE CON PACKAGE SUPPORT 🚀
Questo bridge importa i TUOI moduli originali rispettando la struttura dei package Python
"""

import sys
import os
from pathlib import Path
import uvicorn
from fastapi import FastAPI, HTTPException
import logging
import threading
import time
import cv2
import numpy as np

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🎯 CONFIGURA PYTHON PATH per i TUOI moduli
current_dir = Path(__file__).parent
src_dir = current_dir / "src"

if src_dir.exists():
    # Aggiungi la directory che contiene il package 'src'
    sys.path.insert(0, str(current_dir))
    logger.info(f"✅ Aggiunto path package: {current_dir}")
    logger.info(f"✅ Directory src trovata: {src_dir}")
else:
    logger.error(f"❌ Directory src non trovata: {src_dir}")
    sys.exit(1)

# App FastAPI
app = FastAPI(title="Bridge ai TUOI moduli originali con package support")

# Variabili globali per i TUOI oggetti
camera_manager = None
ai_processor = None
effects_processor = None
virtual_camera_manager = None
performance_monitor = None
config = None

def main_processing_loop():
    """Loop principale che usa i TUOI moduli per processare i frame"""
    global main_loop_running
    
    logger.info("🔄 Avviato loop principale con i TUOI moduli originali!")
    
    while main_loop_running:
        try:
            # 1. Cattura frame usando il TUO CameraManager
            frame = camera_manager.get_frame()
            if frame is None:
                time.sleep(0.01)  # Aspetta un po' se non ci sono frame
                continue
            
            # Ottieni le dimensioni del frame
            height, width = frame.shape[:2]
            output_size = (width, height)
            
            # 2. Processa con il TUO AIProcessor per la segmentazione
            person_mask = ai_processor.process_frame(frame, output_size)
            
            # 3. Applica blur solo allo sfondo usando il TUO EffectsProcessor  
            if person_mask is not None:
                blurred_frame = effects_processor.apply_background_blur(frame, person_mask)
            else:
                # Se non c'è mask, invia il frame originale
                blurred_frame = frame
            
            # 4. Invia alla virtual camera usando il TUO VirtualCameraManager
            virtual_camera_manager.send_frame(blurred_frame)
            
            # 5. Aggiorna statistiche con il TUO PerformanceMonitor
            if hasattr(performance_monitor, 'frame_processed'):
                performance_monitor.frame_processed()
            
        except Exception as e:
            logger.error(f"❌ Errore nel loop principale: {e}")
            time.sleep(0.1)  # Aspetta un po' in caso di errore
    
    logger.info("⏹️ Loop principale fermato")

def initialize_your_modules():
    """Inizializza i TUOI moduli originali usando la struttura package corretta"""
    global camera_manager, ai_processor, effects_processor, virtual_camera_manager, performance_monitor, config
    
    try:
        logger.info("🔧 Importando i TUOI moduli originali come package...")
        
        # Importa la TUA configurazione
        from src.utils.config import StreamBlurConfig
        config = StreamBlurConfig()
        logger.info("✅ TUA configurazione caricata")
        
        # Importa il TUO performance monitor
        from src.utils.performance import PerformanceMonitor
        performance_monitor = PerformanceMonitor()
        logger.info("✅ TUO PerformanceMonitor inizializzato")
        
        # 🚀 CARICAMENTO MODULI SENZA PRE-INIZIALIZZAZIONE
        # Importa moduli ma NON li inizializza (lazy loading)
        from src.core.camera import CameraManager
        from src.core.ai_processor import AIProcessor
        from src.core.effects import EffectsProcessor  
        from src.core.virtual_camera import VirtualCameraManager
        
        # Crea istanze ma NON inizializza (per restart multipli)
        camera_manager = CameraManager(config, performance_monitor)
        ai_processor = AIProcessor(config, performance_monitor)
        effects_processor = EffectsProcessor(config)
        virtual_camera_manager = VirtualCameraManager(config, performance_monitor)
        
        logger.info("✅ Tutti i moduli caricati (lazy initialization)")
        logger.info("⚡ Sistema pronto per start/stop multipli!")
        
        logger.info("🎉 TUTTI I TUOI MODULI ORIGINALI SONO STATI CARICATI CORRETTAMENTE!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Errore nell'inizializzazione dei TUOI moduli: {e}")
        import traceback
        traceback.print_exc()
        return False

@app.get("/health")
async def health_check():
    """Controllo di salute del bridge"""
    modules_status = {
        "camera_manager": camera_manager is not None,
        "ai_processor": ai_processor is not None,
        "effects_processor": effects_processor is not None,
        "virtual_camera_manager": virtual_camera_manager is not None,
        "performance_monitor": performance_monitor is not None,
        "config": config is not None
    }
    
    all_loaded = all(modules_status.values())
    
    return {
        "status": "healthy" if all_loaded else "unhealthy",
        "message": "Bridge ai TUOI moduli originali con package support",
        "modules": modules_status,
        "using_your_src_folder": True,
        "src_path": str(src_dir)
    }

@app.post("/start")
async def start_streamblur():
    """Avvia StreamBlur usando i TUOI moduli originali"""
    global main_loop_running, main_loop_thread
    
    try:
        if not all([camera_manager, ai_processor, effects_processor, virtual_camera_manager]):
            raise HTTPException(status_code=500, detail="Moduli non inizializzati")

        # 🚀 SISTEMA RESTART-SAFE: Inizializza ogni volta per garantire funzionamento
        logger.info("🔄 Inizializzazione componenti (restart-safe)...")
        
        # Prima la camera
        init_success = camera_manager.initialize()
        if not init_success:
            raise HTTPException(status_code=500, detail="Errore inizializzazione camera")
        
        # Poi avvia cattura
        capture_success = camera_manager.start_capture()
        if not capture_success:
            raise HTTPException(status_code=500, detail="Errore avvio cattura camera")

        # 🤖 INIZIALIZZA L'AI PROCESSOR (MediaPipe)
        ai_init_success = ai_processor.initialize()
        if not ai_init_success:
            logger.warning("⚠️ Errore inizializzazione AI, continuo comunque...")

        # Avvia la virtual camera - prima inizializza
        virtual_init_success = virtual_camera_manager.initialize()
        if not virtual_init_success:
            logger.warning("⚠️ Errore inizializzazione virtual camera, continuo comunque...")
        
        # Poi avvia streaming
        virtual_start_success = virtual_camera_manager.start_streaming()
        if not virtual_start_success:
            logger.warning("⚠️ Errore avvio streaming virtual camera, continuo comunque...")

        # 🚀 AVVIA IL LOOP PRINCIPALE CHE USA I TUOI MODULI!
        main_loop_running = True
        main_loop_thread = threading.Thread(target=main_processing_loop, daemon=True)
        main_loop_thread.start()

        logger.info("🚀 StreamBlur avviato usando i TUOI moduli originali!")
        logger.info("🔄 Loop principale attivo - processamento frame in corso!")
        return {"status": "started", "using_your_modules": True, "main_loop_active": True, "restart_safe": True}
        
    except Exception as e:
        logger.error(f"❌ Errore avvio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stop")
async def stop_streamblur():
    """Ferma StreamBlur usando i TUOI metodi originali"""
    global main_loop_running, main_loop_thread
    
    try:
        # Ferma il loop principale
        main_loop_running = False
        if main_loop_thread and main_loop_thread.is_alive():
            main_loop_thread.join(timeout=2.0)
        
        logger.info("⏹️ Loop principale fermato")
        
        # 🧹 CLEANUP COMPLETO E RESET PER RESTART
        if camera_manager:
            camera_manager.stop_capture()
            camera_manager.cleanup()
            logger.info("✅ Camera cleanup completato")
            
        if virtual_camera_manager:
            virtual_camera_manager.stop_streaming()
            virtual_camera_manager.cleanup()
            logger.info("✅ Virtual Camera cleanup completato")
        
        # 🔄 RESET AI per restart pulito
        if ai_processor:
            # Reset interno per permettere restart
            if hasattr(ai_processor, 'reset_for_restart'):
                ai_processor.reset_for_restart()
            logger.info("✅ AI reset per restart")
        
        logger.info("⏹️ StreamBlur fermato usando i TUOI moduli originali")
        return {"status": "stopped", "reset_complete": True}
        
    except Exception as e:
        logger.error(f"❌ Errore stop: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/settings")
async def update_settings(settings: dict):
    """Aggiorna impostazioni usando la TUA configurazione"""
    try:
        if not config:
            raise HTTPException(status_code=500, detail="Configurazione non caricata")
        
        # Aggiorna usando i TUOI metodi di configurazione
        for key, value in settings.items():
            if hasattr(config, key):
                setattr(config, key, value)
                logger.info(f"✅ Aggiornato {key} = {value} nella TUA configurazione")
        
        return {"status": "updated", "settings": settings}
        
    except Exception as e:
        logger.error(f"❌ Errore aggiornamento impostazioni: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_status():
    """Stato dettagliato di StreamBlur usando i TUOI moduli"""
    try:
        status = {}
        
        if camera_manager:
            status["camera"] = {
                "active": camera_manager.is_active if hasattr(camera_manager, 'is_active') else False,
                "fps": camera_manager.fps if hasattr(camera_manager, 'fps') else 0
            }
        
        if performance_monitor:
            status["performance"] = performance_monitor.get_stats() if hasattr(performance_monitor, 'get_stats') else {}
        
        if config:
            status["config"] = {
                "blur_strength": config.blur_strength if hasattr(config, 'blur_strength') else 0,
                "ai_enabled": config.ai_enabled if hasattr(config, 'ai_enabled') else False
            }
        
        return status
        
    except Exception as e:
        logger.error(f"❌ Errore get status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info("🚀 Avviando bridge ai TUOI moduli originali con package support...")
    
    # Inizializza i TUOI moduli
    if initialize_your_modules():
        logger.info("✅ Bridge pronto - usando i TUOI moduli dalla cartella src/ con package support")
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        logger.error("❌ Impossibile avviare - problemi con i TUOI moduli")
        sys.exit(1)
