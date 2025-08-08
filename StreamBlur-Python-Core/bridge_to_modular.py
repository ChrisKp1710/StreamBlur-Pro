"""
StreamBlur Pro - FastAPI Bridge alla Struttura Modulare Esistente
Usa il VERO sistema modulare dalla cartella src/
"""

import sys
import os
from pathlib import Path

# === CONFIGURAZIONE PATH PER MODULI SRC ===
# Aggiungi src al path per import
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

# Cambia directory di lavoro per supportare import relativi
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

# === IMPORT DEL TUO SISTEMA MODULARE ===
try:
    # Import dalla TUA struttura modulare perfetta!
    from utils.config import StreamBlurConfig
    from utils.performance import PerformanceMonitor
    from core.camera import CameraManager
    from core.ai_processor import AIProcessor
    from core.effects import EffectsProcessor
    from core.virtual_camera import VirtualCameraManager
    
    print("✅ Moduli caricati dalla TUA struttura src/!")
    print("🎯 Usando la tua architettura modulare esistente!")
    
except ImportError as e:
    print(f"❌ Errore import dalla struttura src/: {e}")
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

# === ENGINE CHE USA I TUOI MODULI ===

class StreamBlurProEngine:
    """Engine che usa la TUA architettura modulare esistente"""
    
    def __init__(self):
        logger.info("🚀 StreamBlur Pro - Bridge alla TUA struttura modulare")
        logger.info("🎯 Caricamento dei TUOI moduli esistenti...")
        
        # Configurazione dalla TUA struttura
        self.config = StreamBlurConfig()
        self.performance = PerformanceMonitor()
        
        # I TUOI componenti modulari
        self.camera = None
        self.ai_processor = None
        self.effects = None
        self.virtual_camera = None
        
        # Stato del sistema
        self.is_running = False
        self.processing_thread = None
        
        # Status per API
        self.status_info = {
            "is_running": False,
            "current_blur": 5.0,
            "current_ai_quality": "high",
            "frames_processed": 0,
            "fps": 30.0,
            "virtual_camera_active": False,
            "performance_grade": "A",
            "processing_time_ms": 0.0,
            "using_modular_architecture": True,
            "modules_loaded": ["camera", "ai_processor", "effects", "virtual_camera"]
        }
        
        logger.info("✅ Engine inizializzato con la TUA architettura!")
    
    def start(self):
        """Avvia il sistema usando i TUOI moduli"""
        if self.is_running:
            return {"status": "already_running", "message": "Sistema già attivo"}
        
        try:
            logger.info("🚀 Avvio sistema con MODULI ESISTENTI...")
            
            # Inizializza i TUOI componenti modulari
            logger.info("📹 Inizializzando il TUO CameraManager...")
            self.camera = CameraManager(self.config, self.performance)
            
            logger.info("🤖 Inizializzando il TUO AIProcessor...")
            self.ai_processor = AIProcessor(self.config, self.performance)
            
            logger.info("🎨 Inizializzando il TUO EffectsProcessor...")
            self.effects = EffectsProcessor(self.config, self.performance)
            
            logger.info("📺 Inizializzando il TUO VirtualCameraManager...")
            self.virtual_camera = VirtualCameraManager(self.config, self.performance)
            
            # Avvia componenti con i TUOI metodi
            if not self.camera.initialize():
                raise Exception("Errore inizializzazione CameraManager")
            
            if not self.ai_processor.initialize():
                raise Exception("Errore inizializzazione AIProcessor")
            
            if not self.virtual_camera.initialize():
                raise Exception("Errore inizializzazione VirtualCameraManager")
            
            # Avvia processing con la TUA logica
            self.is_running = True
            self.status_info["is_running"] = True
            self.status_info["virtual_camera_active"] = True
            
            self.processing_thread = threading.Thread(target=self._processing_loop_with_your_modules, daemon=True)
            self.processing_thread.start()
            
            logger.info("✅ Sistema avviato con la TUA architettura modulare!")
            logger.info("🎯 Tutti i TUOI moduli sono attivi e funzionanti!")
            
            return {
                "status": "success", 
                "message": "Sistema avviato con architettura modulare esistente",
                "modules_used": self.status_info["modules_loaded"],
                "architecture": "your_modular_src"
            }
            
        except Exception as e:
            logger.error(f"❌ Errore avvio: {e}")
            self.cleanup()
            return {"status": "error", "error": str(e)}
    
    def _processing_loop_with_your_modules(self):
        """Loop di processing che usa i TUOI moduli esistenti"""
        logger.info("🔄 Avvio loop con i TUOI moduli...")
        
        while self.is_running:
            try:
                start_time = time.time()
                
                # 1. Cattura frame dal TUO CameraManager
                frame = self.camera.get_frame()
                if frame is None:
                    time.sleep(0.01)
                    continue
                
                # 2. Elaborazione AI con il TUO AIProcessor
                mask = self.ai_processor.process_frame(frame)
                
                # 3. Applica effetti con il TUO EffectsProcessor
                processed_frame = self.effects.apply_effects(frame, mask)
                
                # 4. Invia al TUO VirtualCameraManager
                self.virtual_camera.send_frame(processed_frame)
                
                # 5. Aggiorna statistiche con il TUO PerformanceMonitor
                processing_time = (time.time() - start_time) * 1000
                self.status_info["frames_processed"] += 1
                self.status_info["processing_time_ms"] = processing_time
                
                # Aggiorna stats ogni 30 frame
                if self.status_info["frames_processed"] % 30 == 0:
                    current_stats = self.performance.get_current_stats()
                    self.status_info.update(current_stats)
                
            except Exception as e:
                logger.error(f"❌ Errore nel loop: {e}")
                time.sleep(0.1)
    
    def stop(self):
        """Ferma il sistema"""
        if not self.is_running:
            return {"success": True, "message": "Sistema già fermato"}
        
        try:
            self.is_running = False
            self.status_info["is_running"] = False
            
            if self.processing_thread and self.processing_thread.is_alive():
                self.processing_thread.join(timeout=2.0)
            
            self.cleanup()
            logger.info("⏹️ Sistema fermato correttamente")
            return {"success": True, "message": "Sistema fermato"}
            
        except Exception as e:
            logger.error(f"❌ Errore stop: {e}")
            return {"success": False, "error": str(e)}
    
    def update_blur(self, strength: float, mode: str):
        """Aggiorna blur usando il TUO EffectsProcessor"""
        self.status_info["current_blur"] = strength
        
        if self.effects:
            # Usa i metodi del TUO modulo effects
            if hasattr(self.effects, 'set_blur_intensity'):
                self.effects.set_blur_intensity(int(strength))
            elif hasattr(self.effects, 'update_blur'):
                self.effects.update_blur(strength, mode)
        
        logger.info(f"🌀 Blur aggiornato con TUO modulo: {strength} ({mode})")
        return {"success": True, "blur_strength": strength, "blur_mode": mode}
    
    def update_ai(self, quality: str, smoothing: float):
        """Aggiorna AI usando il TUO AIProcessor"""
        self.status_info["current_ai_quality"] = quality
        
        if self.ai_processor:
            # Aggiorna configurazione nel TUO AIProcessor
            performance_mode = (quality != "high")
            self.config.set('ai.performance_mode', performance_mode)
            
            # Reinizializza se il TUO modulo lo supporta
            if hasattr(self.ai_processor, 'reinitialize') and self.is_running:
                self.ai_processor.reinitialize()
        
        logger.info(f"🤖 AI aggiornato con TUO modulo: {quality}, smoothing: {smoothing}")
        return {"success": True, "ai_quality": quality, "ai_smoothing": smoothing}
    
    def get_status(self):
        """Stato del sistema con info sui TUOI moduli"""
        if self.performance:
            current_stats = self.performance.get_current_stats()
            self.status_info.update(current_stats)
        
        return self.status_info
    
    def cleanup(self):
        """Pulizia usando i TUOI metodi di cleanup"""
        try:
            if self.virtual_camera and hasattr(self.virtual_camera, 'cleanup'):
                self.virtual_camera.cleanup()
                self.virtual_camera = None
                
            if self.ai_processor and hasattr(self.ai_processor, 'cleanup'):
                self.ai_processor.cleanup()
                self.ai_processor = None
                
            if self.camera and hasattr(self.camera, 'cleanup'):
                self.camera.cleanup()
                self.camera = None
                
            self.effects = None
            
            self.status_info["is_running"] = False
            self.status_info["virtual_camera_active"] = False
            
            logger.info("🧹 Risorse pulite usando i TUOI metodi")
            
        except Exception as e:
            logger.error(f"❌ Errore cleanup: {e}")

# === ISTANZA GLOBALE ===
engine = StreamBlurProEngine()

# === FASTAPI APP ===
app = FastAPI(
    title="StreamBlur Pro - Bridge Modulare", 
    version="4.0", 
    description="Bridge alla TUA architettura modulare esistente in src/"
)

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
    """Avvia usando i TUOI moduli"""
    result = engine.start()
    return JSONResponse(content=result)

@app.post("/api/stop")
async def stop_engine():
    """Ferma il sistema"""
    result = engine.stop()
    return JSONResponse(content=result)

@app.get("/api/status")
async def get_status():
    """Stato con info sui TUOI moduli"""
    return JSONResponse(content=engine.get_status())

@app.post("/api/blur")
async def update_blur_settings(settings: BlurSettings):
    """Aggiorna blur con TUO EffectsProcessor"""
    result = engine.update_blur(settings.strength, settings.mode)
    return JSONResponse(content=result)

@app.post("/api/ai")
async def update_ai_settings(settings: AISettings):
    """Aggiorna AI con TUO AIProcessor"""
    result = engine.update_ai(settings.quality, settings.smoothing)
    return JSONResponse(content=result)

@app.get("/api/health")
async def health_check():
    """Health check con info moduli"""
    return {
        "status": "healthy", 
        "version": "4.0", 
        "architecture": "your_modular_src",
        "modules_loaded": engine.status_info["modules_loaded"]
    }

# === AVVIO SERVER ===

if __name__ == "__main__":
    logger.info("🚀 StreamBlur Pro Bridge - USA LA TUA STRUTTURA MODULARE!")
    logger.info("🎯 Caricamento dai TUOI moduli in src/")
    logger.info("✅ CameraManager, AIProcessor, EffectsProcessor, VirtualCameraManager")
    logger.info("🌐 Server in avvio su http://127.0.0.1:8080")
    logger.info("🔗 Bridge attivo per Tauri!")
    
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8080, 
        log_level="info"
    )
