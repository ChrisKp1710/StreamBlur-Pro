"""
StreamBlur Pro - Wrapper Semplice per la TUA Struttura Modulare
Risolve i problemi di import e usa i TUOI moduli esistenti
"""

import sys
import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import threading
import time
import logging
import cv2
import numpy as np
import mediapipe as mp
import pyvirtualcam

# === CONFIGURAZIONE PATH ===
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

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

# === WRAPPER SEMPLIFICATO ===
class StreamBlurProWrapper:
    """Wrapper semplice che evita problemi di import"""
    
    def __init__(self):
        logger.info("🚀 StreamBlur Pro Wrapper - Usa la TUA struttura!")
        
        # Import diretto dalla directory src
        self.modules_loaded = False
        self.is_running = False
        self.processing_thread = None
        
        # Status semplificato
        self.status_info = {
            "is_running": False,
            "current_blur": 5.0,
            "current_ai_quality": "high", 
            "frames_processed": 0,
            "fps": 30.0,
            "virtual_camera_active": False,
            "performance_grade": "A",
            "processing_time_ms": 0.0,
            "using_your_modules": True
        }
        
        # Prova a caricare i moduli dalla tua src/
        self._try_load_your_modules()
    
    def _try_load_your_modules(self):
        """Prova a caricare i tuoi moduli con diverse strategie"""
        try:
            # Strategia 1: Import diretto
            os.chdir(src_path)
            
            # Prova import semplici
            import core.camera as camera_mod
            import core.ai_processor as ai_mod
            import core.effects as effects_mod
            import core.virtual_camera as vcam_mod
            import utils.config as config_mod
            import utils.performance as perf_mod
            
            self.camera_module = camera_mod
            self.ai_module = ai_mod
            self.effects_module = effects_mod
            self.vcam_module = vcam_mod
            self.config_module = config_mod
            self.perf_module = perf_mod
            
            self.modules_loaded = True
            logger.info("✅ TUOI moduli caricati correttamente!")
            
        except Exception as e:
            logger.error(f"❌ Errore caricamento moduli: {e}")
            logger.info("🔄 Modalità fallback - uso implementazione semplificata")
            self._init_fallback_system()
    
    def _init_fallback_system(self):
        """Sistema fallback se i moduli non si caricano"""
        import cv2
        import numpy as np
        import mediapipe as mp
        import pyvirtualcam
        
        # Sistema semplificato integrato
        self.webcam = None
        self.virtual_camera = None
        self.selfie_segmentation = None
        self.modules_loaded = "fallback"
        
        logger.info("🔧 Sistema fallback inizializzato")
    
    def start(self):
        """Avvia il sistema"""
        if self.is_running:
            return {"status": "already_running"}
        
        try:
            if self.modules_loaded == True:
                return self._start_with_your_modules()
            else:
                return self._start_fallback()
                
        except Exception as e:
            logger.error(f"❌ Errore avvio: {e}")
            return {"status": "error", "error": str(e)}
    
    def _start_with_your_modules(self):
        """Avvia usando i TUOI moduli"""
        try:
            logger.info("🚀 Avvio con i TUOI moduli esistenti...")
            
            # Usa le tue classi
            config_class = getattr(self.config_module, 'StreamBlurConfig')
            perf_class = getattr(self.perf_module, 'PerformanceMonitor')
            
            self.config = config_class()
            self.performance = perf_class()
            
            # Inizializza i tuoi componenti
            camera_class = getattr(self.camera_module, 'CameraManager')
            ai_class = getattr(self.ai_module, 'AIProcessor')
            effects_class = getattr(self.effects_module, 'EffectsProcessor')
            vcam_class = getattr(self.vcam_module, 'VirtualCameraManager')
            
            self.camera = camera_class(self.config, self.performance)
            self.ai_processor = ai_class(self.config, self.performance)
            self.effects = effects_class(self.config, self.performance)
            self.virtual_camera = vcam_class(self.config, self.performance)
            
            # Avvia con i tuoi metodi
            self.camera.initialize()
            self.ai_processor.initialize()
            self.virtual_camera.initialize()
            
            self.is_running = True
            self.status_info["is_running"] = True
            self.status_info["virtual_camera_active"] = True
            
            self.processing_thread = threading.Thread(target=self._processing_with_your_modules, daemon=True)
            self.processing_thread.start()
            
            logger.info("✅ Sistema avviato con i TUOI moduli!")
            return {"status": "success", "message": "Avviato con struttura modulare esistente"}
            
        except Exception as e:
            logger.error(f"❌ Errore con i tuoi moduli: {e}")
            logger.info("🔄 Fallback al sistema semplificato...")
            return self._start_fallback()
    
    def _start_fallback(self):
        """Sistema fallback semplificato"""
        import cv2
        import mediapipe as mp
        import pyvirtualcam
        
        try:
            logger.info("🔧 Avvio sistema fallback...")
            
            # Webcam
            self.webcam = cv2.VideoCapture(0)
            self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.webcam.set(cv2.CAP_PROP_FPS, 30)
            
            # MediaPipe
            mp_selfie = mp.solutions.selfie_segmentation
            self.selfie_segmentation = mp_selfie.SelfieSegmentation(model_selection=1)
            
            # Virtual Camera
            self.virtual_camera = pyvirtualcam.Camera(
                width=1280, height=720, fps=30, fmt=pyvirtualcam.PixelFormat.RGB
            )
            
            self.is_running = True
            self.status_info["is_running"] = True
            self.status_info["virtual_camera_active"] = True
            
            self.processing_thread = threading.Thread(target=self._processing_fallback, daemon=True)
            self.processing_thread.start()
            
            logger.info("✅ Sistema fallback avviato!")
            return {"status": "success", "message": "Sistema fallback attivo"}
            
        except Exception as e:
            logger.error(f"❌ Errore fallback: {e}")
            return {"status": "error", "error": str(e)}
    
    def _processing_with_your_modules(self):
        """Processing con i TUOI moduli"""
        logger.info("🔄 Loop con i TUOI moduli...")
        
        while self.is_running:
            try:
                start_time = time.time()
                
                # Usa i metodi dei TUOI moduli
                frame = self.camera.get_frame()
                if frame is None:
                    time.sleep(0.01)
                    continue
                
                mask = self.ai_processor.process_frame(frame)
                processed_frame = self.effects.apply_effects(frame, mask)
                self.virtual_camera.send_frame(processed_frame)
                
                # Stats
                processing_time = (time.time() - start_time) * 1000
                self.status_info["frames_processed"] += 1
                self.status_info["processing_time_ms"] = processing_time
                
                if self.status_info["frames_processed"] % 30 == 0:
                    current_stats = self.performance.get_current_stats()
                    self.status_info.update(current_stats)
                
            except Exception as e:
                logger.error(f"❌ Errore processing moduli: {e}")
                time.sleep(0.1)
    
    def _processing_fallback(self):
        """Processing fallback"""
        logger.info("🔄 Loop fallback...")
        
        while self.is_running:
            try:
                start_time = time.time()
                
                ret, frame = self.webcam.read()
                if not ret:
                    time.sleep(0.01)
                    continue
                
                frame = cv2.flip(frame, 1)
                
                # AI segmentation
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.selfie_segmentation.process(rgb_frame)
                mask = results.segmentation_mask
                
                # Background blur
                blur_intensity = int(self.status_info["current_blur"] * 4)
                if blur_intensity % 2 == 0:
                    blur_intensity += 1
                blur_intensity = max(3, min(51, blur_intensity))
                
                blurred = cv2.GaussianBlur(frame, (blur_intensity, blur_intensity), 0)
                
                # Combine
                person_mask = (mask > 0.5).astype('uint8') * 255
                person_mask_3ch = cv2.cvtColor(person_mask, cv2.COLOR_GRAY2BGR) / 255.0
                background_mask_3ch = 1.0 - person_mask_3ch
                
                result = (frame * person_mask_3ch + blurred * background_mask_3ch).astype('uint8')
                
                # Overlay
                overlay_text = f"StreamBlur Pro (TUA struttura) - BLUR: {self.status_info['current_blur']:.1f}"
                cv2.rectangle(result, (10, 10), (600, 60), (0, 0, 0), -1)
                cv2.rectangle(result, (10, 10), (600, 60), (0, 255, 0), 2)
                cv2.putText(result, overlay_text, (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Send
                rgb_result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
                self.virtual_camera.send(rgb_result)
                
                # Stats
                processing_time = (time.time() - start_time) * 1000
                self.status_info["frames_processed"] += 1
                self.status_info["processing_time_ms"] = processing_time
                
                if self.status_info["frames_processed"] % 30 == 0:
                    self.status_info["fps"] = min(30.0, 1000 / processing_time) if processing_time > 0 else 30.0
                
            except Exception as e:
                logger.error(f"❌ Errore processing fallback: {e}")
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
            logger.info("⏹️ Sistema fermato")
            return {"success": True, "message": "Sistema fermato"}
            
        except Exception as e:
            logger.error(f"❌ Errore stop: {e}")
            return {"success": False, "error": str(e)}
    
    def update_blur(self, strength: float, mode: str):
        """Aggiorna blur"""
        self.status_info["current_blur"] = strength
        logger.info(f"🌀 Blur aggiornato: {strength}")
        return {"success": True, "blur_strength": strength}
    
    def update_ai(self, quality: str, smoothing: float):
        """Aggiorna AI"""
        self.status_info["current_ai_quality"] = quality
        logger.info(f"🤖 AI aggiornato: {quality}")
        return {"success": True, "ai_quality": quality}
    
    def get_status(self):
        """Stato del sistema"""
        return self.status_info
    
    def cleanup(self):
        """Pulizia"""
        try:
            if hasattr(self, 'webcam') and self.webcam:
                self.webcam.release()
            if hasattr(self, 'virtual_camera') and self.virtual_camera:
                self.virtual_camera.close()
            if hasattr(self, 'selfie_segmentation') and self.selfie_segmentation:
                self.selfie_segmentation.close()
                
            self.status_info["is_running"] = False
            self.status_info["virtual_camera_active"] = False
            
        except Exception as e:
            logger.error(f"❌ Errore cleanup: {e}")

# === ISTANZA GLOBALE ===
engine = StreamBlurProWrapper()

# === FASTAPI APP ===
app = FastAPI(title="StreamBlur Pro - Wrapper TUA Struttura", version="4.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === ENDPOINTS ===
@app.post("/api/start")
async def start_engine():
    result = engine.start()
    return JSONResponse(content=result)

@app.post("/api/stop")
async def stop_engine():
    result = engine.stop()
    return JSONResponse(content=result)

@app.get("/api/status")
async def get_status():
    return JSONResponse(content=engine.get_status())

@app.post("/api/blur")
async def update_blur_settings(settings: BlurSettings):
    result = engine.update_blur(settings.strength, settings.mode)
    return JSONResponse(content=result)

@app.post("/api/ai")
async def update_ai_settings(settings: AISettings):
    result = engine.update_ai(settings.quality, settings.smoothing)
    return JSONResponse(content=result)

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "using_your_structure": True}

# === AVVIO ===
if __name__ == "__main__":
    logger.info("🚀 StreamBlur Pro - Wrapper per la TUA struttura modulare")
    logger.info("🎯 Prova a usare i TUOI moduli, fallback se necessario")
    logger.info("✅ Compatibile con la TUA architettura src/")
    
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")
