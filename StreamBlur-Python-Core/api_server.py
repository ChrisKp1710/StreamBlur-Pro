"""
StreamBlur Pro - FastAPI Server con Architettura Modulare
Server API che utilizza il sistema modulare src/ per Tauri
"""

import sys
import os
from pathlib import Path

# Aggiungi src al path e cambia directory di lavoro
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

# Cambia la directory di lavoro per i moduli relativi
original_cwd = os.getcwd()
os.chdir(src_path)

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import threading
import time
import logging

# Import dal sistema modulare (ora funzionano perché siamo in src/)
try:
    from utils.config import StreamBlurConfig
    from utils.performance import PerformanceMonitor  
    from core.camera import CameraManager
    from core.ai_processor import AIProcessor
    from core.effects import EffectsProcessor
    from core.virtual_camera import VirtualCameraManager
except ImportError as e:
    print(f"❌ Errore import moduli: {e}")
    print(f"📂 Directory corrente: {os.getcwd()}")
    print(f"📂 Path src: {src_path}")
    sys.exit(1)

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === MODELLI PYDANTIC ===

class BlurSettings(BaseModel):
    strength: float
    mode: str = "gaussian"

class AISettings(BaseModel):
    quality: str = "high"
    smoothing: float = 0.5

# === CLASSE PRINCIPALE ===

class StreamBlurProEngine:
    """Motore StreamBlur Pro con architettura modulare"""
    
    def __init__(self):
        # Configurazione
        self.config = StreamBlurConfig()
        self.performance = PerformanceMonitor()
        
        # Componenti core
        self.camera = None
        self.ai_processor = None
        self.effects = None
        self.virtual_camera = None
        
        # Stato
        self.is_running = False
        self.processing_thread = None
        
        # Status info per API
        self.status_info = {
            "is_running": False,
            "current_blur": 5.0,
            "current_ai_quality": "high",
            "frames_processed": 0,
            "fps": 30.0,
            "virtual_camera_active": False,
            "performance_grade": "A",
            "processing_time_ms": 0.0
        }
        
        logger.info("🚀 StreamBlur Pro Engine - Architettura Modulare")
        logger.info("🎯 Sistema professionale con AI avanzato")
    
    def start(self):
        """Avvia il sistema completo"""
        if self.is_running:
            return {"status": "already_running"}
        
        try:
            logger.info("🚀 Inizializzazione componenti modulari...")
            
            # Inizializza componenti in ordine
            self.camera = CameraManager(self.config, self.performance)
            self.ai_processor = AIProcessor(self.config, self.performance)
            self.effects = EffectsProcessor(self.config, self.performance)
            self.virtual_camera = VirtualCameraManager(self.config, self.performance)
            
            # Avvia camera
            if not self.camera.initialize():
                raise Exception("Impossibile inizializzare la camera")
            
            # Avvia AI processor
            if not self.ai_processor.initialize():
                raise Exception("Impossibile inizializzare AI processor")
            
            # Avvia virtual camera
            if not self.virtual_camera.initialize():
                raise Exception("Impossibile inizializzare virtual camera")
            
            # Avvia thread di processing
            self.is_running = True
            self.status_info["is_running"] = True
            self.status_info["virtual_camera_active"] = True
            
            self.processing_thread = threading.Thread(target=self._processing_loop, daemon=True)
            self.processing_thread.start()
            
            logger.info("✅ StreamBlur Pro avviato con sistema modulare!")
            return {"status": "success", "message": "Sistema modulare attivato"}
            
        except Exception as e:
            logger.error(f"❌ Errore avvio: {e}")
            self.cleanup()
            return {"status": "error", "error": str(e)}
    
    def stop(self):
        """Ferma il sistema"""
        if not self.is_running:
            return {"success": True, "message": "Sistema già fermato"}
        
        try:
            self.is_running = False
            self.status_info["is_running"] = False
            
            # Aspetta che il thread finisca
            if self.processing_thread and self.processing_thread.is_alive():
                self.processing_thread.join(timeout=2.0)
            
            self.cleanup()
            logger.info("⏹️ Sistema fermato correttamente")
            return {"success": True, "message": "Sistema fermato"}
            
        except Exception as e:
            logger.error(f"❌ Errore stop: {e}")
            return {"success": False, "error": str(e)}
    
    def _processing_loop(self):
        """Loop principale di elaborazione"""
        logger.info("🔄 Avvio loop di elaborazione...")
        
        while self.is_running:
            try:
                start_time = time.time()
                
                # Cattura frame dalla camera
                frame = self.camera.get_frame()
                if frame is None:
                    time.sleep(0.01)
                    continue
                
                # Elaborazione AI
                mask = self.ai_processor.process_frame(frame)
                
                # Applica effetti
                processed_frame = self.effects.apply_effects(frame, mask)
                
                # Invia a virtual camera
                self.virtual_camera.send_frame(processed_frame)
                
                # Aggiorna statistiche
                processing_time = (time.time() - start_time) * 1000
                self.status_info["frames_processed"] += 1
                self.status_info["processing_time_ms"] = processing_time
                
                # Calcola FPS
                if self.status_info["frames_processed"] % 30 == 0:
                    stats = self.performance.get_current_stats()
                    self.status_info["fps"] = stats.get("fps", 30.0)
                    self.status_info["performance_grade"] = stats.get("performance_grade", "A")
                
                # Aggiorna overlay di sistema
                self._update_overlay()
                
            except Exception as e:
                logger.error(f"❌ Errore nel loop: {e}")
                time.sleep(0.1)
    
    def _update_overlay(self):
        """Aggiorna overlay di stato"""
        # Il virtual camera manager gestisce l'overlay automaticamente
        pass
    
    def update_blur(self, strength: float, mode: str):
        """Aggiorna impostazioni blur"""
        self.status_info["current_blur"] = strength
        
        if self.effects:
            self.effects.set_blur_intensity(int(strength))
            
        logger.info(f"🌀 Blur aggiornato: {strength} ({mode})")
        return {"success": True, "blur_strength": strength, "blur_mode": mode}
    
    def update_ai(self, quality: str, smoothing: float):
        """Aggiorna impostazioni AI"""
        self.status_info["current_ai_quality"] = quality
        
        if self.ai_processor:
            # Aggiorna qualità AI
            performance_mode = (quality != "high")
            self.ai_processor.config.set('ai.performance_mode', performance_mode)
            
            # Reinizializza se necessario
            if self.is_running:
                self.ai_processor.reinitialize()
        
        logger.info(f"🤖 AI aggiornato: {quality}, smoothing: {smoothing}")
        return {"success": True, "ai_quality": quality, "ai_smoothing": smoothing}
    
    def get_status(self):
        """Ritorna stato dettagliato del sistema"""
        if self.performance:
            stats = self.performance.get_current_stats()
            self.status_info.update(stats)
        
        return self.status_info
    
    def cleanup(self):
        """Pulizia risorse"""
        try:
            if self.virtual_camera:
                self.virtual_camera.cleanup()
                self.virtual_camera = None
                
            if self.ai_processor:
                self.ai_processor.cleanup()
                self.ai_processor = None
                
            if self.camera:
                self.camera.cleanup()
                self.camera = None
                
            if self.effects:
                self.effects = None
                
            self.status_info["is_running"] = False
            self.status_info["virtual_camera_active"] = False
            
            logger.info("🧹 Risorse pulite")
            
        except Exception as e:
            logger.error(f"❌ Errore cleanup: {e}")

# Istanza globale
engine = StreamBlurProEngine()

# FastAPI app
app = FastAPI(
    title="StreamBlur Pro - Modular API", 
    version="4.0", 
    description="Professional NVIDIA Broadcast Alternative with Modular Architecture"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === ENDPOINTS API ===

@app.post("/api/start")
async def start_engine():
    """Avvia il motore modulare"""
    result = engine.start()
    return JSONResponse(content=result)

@app.post("/api/stop")
async def stop_engine():
    """Ferma il motore"""
    result = engine.stop()
    return JSONResponse(content=result)

@app.get("/api/status")
async def get_status():
    """Stato dettagliato del sistema"""
    return JSONResponse(content=engine.get_status())

@app.post("/api/blur")
async def update_blur_settings(settings: BlurSettings):
    """Aggiorna impostazioni blur"""
    result = engine.update_blur(settings.strength, settings.mode)
    return JSONResponse(content=result)

@app.post("/api/ai")
async def update_ai_settings(settings: AISettings):
    """Aggiorna impostazioni AI"""
    result = engine.update_ai(settings.quality, settings.smoothing)
    return JSONResponse(content=result)

@app.get("/api/health")
async def health_check():
    """Health check"""
    return {"status": "healthy", "version": "4.0", "architecture": "modular"}

# === AVVIO SERVER ===

if __name__ == "__main__":
    logger.info("🚀 StreamBlur Pro API - Sistema Modulare")
    logger.info("🎯 Architettura professionale attiva")
    logger.info("🌐 Server in avvio su http://127.0.0.1:8080")
    logger.info("✅ Pronto per Tauri!")
    
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8080, 
        log_level="info"
    )
