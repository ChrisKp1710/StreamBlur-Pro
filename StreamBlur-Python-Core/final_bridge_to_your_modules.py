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

# Variabili per il controllo del loop e statistiche
main_loop_running = False
main_loop_thread = None
current_real_fps = 0.0  # 📊 FPS reali per il card Performance (NO spam log)

def main_processing_loop():
    """Loop principale che usa i TUOI moduli per processare i frame"""
    global main_loop_running, current_real_fps
    
    logger.info("🔄 Avviato loop principale con i TUOI moduli originali!")
    
    # 📊 Variabili per calcolo FPS reali (SENZA spam log)
    frame_count = 0
    start_time = time.time()
    last_fps_update = time.time()
    
    while main_loop_running:
        try:
            # 1. Cattura frame usando il TUO CameraManager
            frame = camera_manager.get_frame()
            if frame is None:
                time.sleep(0.01)  # Aspetta un po' se non ci sono frame
                continue
            
            # 📊 Conta frame processati per FPS reali
            frame_count += 1
            current_time = time.time()
            
            # Calcola FPS reali ogni secondo (SILENZIOSO)
            if current_time - last_fps_update >= 1.0:
                elapsed = current_time - start_time
                if elapsed > 0:
                    current_real_fps = frame_count / elapsed
                frame_count = 0
                start_time = current_time
                last_fps_update = current_time
            
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
    
    # Reset FPS quando il loop si ferma
    current_real_fps = 0.0
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
        
        # 🔍 DEBUG: Log di tutto quello che arriva (solo se diverso da blur)
        if "strength" not in settings:
            logger.info(f"🔧 Settings ricevuti: {settings}")
        
        # 🎛️ AGGIORNA IMPOSTAZIONI CON PROPAGAZIONE AI MODULI
        for key, value in settings.items():
            # Skip log verboso per blur updates
            if key not in ["strength", "mode"]:
                logger.info(f"🔄 Processando {key} = {value}")
            
            # Aggiorna config principale
            if hasattr(config, key):
                setattr(config, key, value)
                logger.info(f"✅ Aggiornato {key} = {value} nella TUA configurazione")
            
            # 🔥 PROPAGA BLUR INTENSITY AI MODULI ATTIVI
            if key in ["blur_strength", "blur_intensity", "blurStrength", "blurIntensity", "strength", "intensity"] and effects_processor:
                try:
                    # Usa il metodo del TUO EffectsProcessor
                    if hasattr(effects_processor, 'set_blur_intensity'):
                        effects_processor.set_blur_intensity(int(value))
                        # Log solo significativi (ogni 5 unità)
                        if int(value) % 5 == 0:
                            logger.info(f"🎛️ Blur intensity: {value}")
                    elif hasattr(effects_processor, 'blur_intensity'):
                        effects_processor.blur_intensity = int(value)
                        if int(value) % 5 == 0:
                            logger.info(f"🎛️ Blur intensity: {value}")
                    else:
                        logger.warning(f"⚠️ TUO EffectsProcessor non supporta blur_intensity")
                except Exception as e:
                    logger.error(f"❌ Errore aggiornamento blur intensity: {e}")
            
            # 🤖 PROPAGA AI SETTINGS AI TUOI MODULI
            if key in ["ai_enabled", "performance_mode", "edgeSmoothing", "edge_smoothing", "temporalSmoothing", "temporal_smoothing"] and ai_processor:
                try:
                    # Performance Mode (solo se AI è già inizializzato)
                    if key in ["performance_mode", "performanceMode"]:
                        if hasattr(ai_processor, 'switch_model') and hasattr(ai_processor, 'segmentation') and ai_processor.segmentation:
                            ai_processor.switch_model(bool(value))
                            logger.info(f"🤖 Performance mode aggiornato nel TUO AIProcessor: {value}")
                        else:
                            logger.info(f"🤖 Performance mode salvato per dopo l'inizializzazione: {value}")
                    
                    # Edge Smoothing
                    elif key in ["edgeSmoothing", "edge_smoothing"]:
                        if hasattr(ai_processor, 'set_edge_smoothing'):
                            ai_processor.set_edge_smoothing(bool(value))
                            logger.info(f"🎯 Edge smoothing aggiornato nel TUO AIProcessor: {value}")
                    
                    # Temporal Smoothing  
                    elif key in ["temporalSmoothing", "temporal_smoothing"]:
                        if hasattr(ai_processor, 'set_temporal_smoothing'):
                            ai_processor.set_temporal_smoothing(bool(value))
                            logger.info(f"⏱️ Temporal smoothing aggiornato nel TUO AIProcessor: {value}")
                    
                    # Generic AI settings
                    elif hasattr(ai_processor, key):
                        setattr(ai_processor, key, value)
                        logger.info(f"🤖 AI setting {key} aggiornato: {value}")
                        
                except Exception as e:
                    logger.error(f"❌ Errore aggiornamento AI {key}: {e}")
            
            # 🎛️ LEGACY: Supporto per quality/smoothing (mappatura vecchia)
            if key == "quality" and ai_processor:
                # Mappa quality a performance mode con logging amplificato
                # 🔧 FISSO: low=VELOCE, medium/high=ACCURATO
                performance_mode = value == "low"  # low = performance mode = più FPS
                try:
                    # Solo se AI è inizializzato
                    if hasattr(ai_processor, 'switch_model') and hasattr(ai_processor, 'segmentation') and ai_processor.segmentation:
                        ai_processor.switch_model(performance_mode)
                        quality_desc = "🚀 VELOCE (meno accurato)" if performance_mode else "🎯 ACCURATO (più lento)"
                        logger.info(f"🤖 Quality→Performance mode applicato: {performance_mode} → {quality_desc}")
                    else:
                        logger.info(f"🤖 Quality→Performance mode salvato: {performance_mode}")
                except Exception as e:
                    logger.error(f"❌ Errore quality mapping: {e}")
                    
            if key == "smoothing" and ai_processor:
                # Mappa smoothing a temporal smoothing 
                temporal_enabled = float(value) > 0.5
                try:
                    if hasattr(ai_processor, 'set_temporal_smoothing'):
                        ai_processor.set_temporal_smoothing(temporal_enabled)
                        logger.info(f"⏱️ Smoothing→Temporal: {temporal_enabled}")
                except Exception as e:
                    logger.error(f"❌ Errore smoothing mapping: {e}")
        
        return {"status": "updated", "settings": settings, "propagated": True}
        
    except Exception as e:
        logger.error(f"❌ Errore aggiornamento impostazioni: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# 🤖 AI SETTINGS UPDATE ENDPOINT
@app.post("/api/ai-settings")
async def update_ai_settings(settings: dict):
    """Aggiorna specificamente le impostazioni AI"""
    logger.info(f"🤖 Aggiornamento AI settings: {settings}")
    
    try:
        # Propaga tutte le impostazioni tramite update_settings esistente
        result = await update_settings(settings)
        
        # Log dettagliato per debug
        logger.info(f"🤖 AI settings aggiornate con successo: {result}")
        
        return {
            "status": "ai_settings_updated", 
            "settings": settings, 
            "quality_mode": settings.get('quality', 'unknown'),
            "propagated": True
        }
        
    except Exception as e:
        logger.error(f"❌ Errore aggiornamento AI settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_status():
    """Stato dettagliato di StreamBlur usando i TUOI moduli"""
    global main_loop_running, current_real_fps
    try:
        # 📊 Struttura che si aspetta il frontend Tauri
        # FPS = 0 quando spento, FPS reali quando attivo
        fps_value = current_real_fps if main_loop_running else 0.0
        
        # Metriche sistema (opzionali)
        cpu_usage = 0.0
        memory_usage = 0.0
        
        try:
            import psutil
            cpu_usage = psutil.cpu_percent(interval=0.1)
            memory_info = psutil.virtual_memory()
            memory_usage = memory_info.used / (1024 * 1024)  # MB
        except:
            pass
        
        # Struttura esatta per il frontend
        status_response = {
            "running": main_loop_running,
            "fps": round(fps_value, 1),
            "cpu_usage": round(cpu_usage, 1), 
            "memory_usage": round(memory_usage, 1)
        }
        
        return status_response
        
    except Exception as e:
        logger.error(f"❌ Errore get status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info("🚀 Avviando bridge ai TUOI moduli originali con package support...")
    
    # Inizializza i TUOI moduli
    if initialize_your_modules():
        logger.info("✅ Bridge pronto - usando i TUOI moduli dalla cartella src/ con package support")
        
        # Configurazione server ottimizzata per ridurre errori di connessione
        config_server = {
            "host": "127.0.0.1",
            "port": 8000,
            "log_level": "warning",  # Riduce log verbosi
            "access_log": False,     # Disabilita access log per ridurre spam
            "timeout_keep_alive": 5  # Timeout più breve per evitare connessioni stagnanti
        }
        
        uvicorn.run(app, **config_server)
    else:
        logger.error("❌ Impossibile avviare - problemi con i TUOI moduli")
        sys.exit(1)
