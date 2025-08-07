"""
StreamBlur Pro - Server API Principale
Backend FastAPI per comunicazione con frontend Tauri
"""

import sys
import os
from pathlib import Path
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

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Modelli per API
class BlurSettings(BaseModel):
    strength: float
    mode: str

class AISettings(BaseModel):
    quality: str
    smoothing: float

class StreamBlurEngine:
    """Motore principale StreamBlur Pro"""
    
    def __init__(self):
        self.is_running = False
        self.virtual_camera = None
        self.webcam = None
        
        # Stato del sistema
        self.status_info = {
            "is_running": False,
            "current_blur": 5.0,
            "current_ai_quality": "high",
            "frames_processed": 0,
            "fps": 30.0,
            "virtual_camera_active": False
        }
        
    def start(self):
        """Avvia il motore StreamBlur"""
        if self.is_running:
            return {"success": True, "message": "Motore già attivo"}
            
        try:
            import pyvirtualcam
            
            logger.info("🚀 Inizializzazione StreamBlur Pro...")
            
            # Inizializza webcam
            self.webcam = cv2.VideoCapture(0)
            if not self.webcam.isOpened():
                raise Exception("Impossibile aprire la webcam")
            
            # Configura webcam
            self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.webcam.set(cv2.CAP_PROP_FPS, 30)
            
            logger.info("📷 Webcam inizializzata")
            
            # Crea virtual camera
            self.virtual_camera = pyvirtualcam.Camera(
                width=1280, 
                height=720, 
                fps=30,
                fmt=pyvirtualcam.PixelFormat.BGR
            )
            
            logger.info(f"🎥 Virtual Camera creata: {self.virtual_camera.device}")
            
            # Avvia processing loop
            self._start_processing_loop()
            
            self.is_running = True
            self.status_info["is_running"] = True
            self.status_info["virtual_camera_active"] = True
            
            logger.info("✅ StreamBlur Pro ATTIVO!")
            return {"success": True, "message": "StreamBlur avviato con successo"}
            
        except Exception as e:
            logger.error(f"❌ Errore avvio: {e}")
            return {"success": False, "message": f"Errore: {str(e)}"}
    
    def stop(self):
        """Ferma il motore StreamBlur"""
        if not self.is_running:
            return {"success": True, "message": "Motore già fermato"}
            
        try:
            self.is_running = False
            
            if self.webcam:
                self.webcam.release()
                self.webcam = None
                logger.info("📷 Webcam fermata")
            
            if self.virtual_camera:
                self.virtual_camera.close()
                self.virtual_camera = None
                logger.info("🎥 Virtual camera fermata")
                
            self.status_info["is_running"] = False
            self.status_info["virtual_camera_active"] = False
            
            logger.info("⏹️ StreamBlur Pro FERMATO!")
            return {"success": True, "message": "StreamBlur fermato"}
            
        except Exception as e:
            logger.error(f"❌ Errore stop: {e}")
            return {"success": False, "message": f"Errore: {str(e)}"}
    
    def _start_processing_loop(self):
        """Avvia il loop di elaborazione video"""
        def processing_loop():
            logger.info("🔄 Processing loop avviato")
            
            while self.is_running and self.virtual_camera and self.webcam:
                try:
                    # Cattura frame dalla webcam
                    ret, frame = self.webcam.read()
                    if not ret or frame is None:
                        time.sleep(0.1)
                        continue
                    
                    # Ridimensiona se necessario
                    frame = cv2.resize(frame, (1280, 720))
                    
                    # Applica blur
                    processed_frame = self._apply_blur_effect(frame)
                    
                    # Invia a virtual camera
                    self.virtual_camera.send(processed_frame)
                    
                    # Aggiorna stats
                    self.status_info["frames_processed"] += 1
                    
                    # Log ogni 100 frames
                    if self.status_info["frames_processed"] % 100 == 0:
                        logger.info(f"📊 Frames: {self.status_info['frames_processed']}")
                    
                    # Mantieni 30 FPS
                    time.sleep(1/30)
                    
                except Exception as e:
                    logger.error(f"❌ Errore processing: {e}")
                    time.sleep(0.1)
                    
            logger.info("🔄 Processing loop terminato")
        
        # Avvia in thread separato
        processing_thread = threading.Thread(target=processing_loop, daemon=True)
        processing_thread.start()
    
    def _apply_blur_effect(self, frame):
        """Applica effetto blur al frame"""
        blur_strength = int(self.status_info["current_blur"])
        
        if blur_strength > 0:
            # Calcola kernel size (deve essere dispari)
            kernel_size = max(1, blur_strength * 4 + 1)
            if kernel_size % 2 == 0:
                kernel_size += 1
            
            # Applica blur gaussiano
            blurred_frame = cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)
            
            # Aggiungi overlay
            cv2.putText(blurred_frame, f"StreamBlur Pro - BLUR: {blur_strength}", 
                       (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(blurred_frame, f"Frame: {self.status_info['frames_processed']}", 
                       (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            return blurred_frame
        else:
            # Nessun blur
            cv2.putText(frame, f"StreamBlur Pro - NO BLUR", 
                       (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, f"Frame: {self.status_info['frames_processed']}", 
                       (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            return frame
    
    def update_blur(self, strength: float, mode: str):
        """Aggiorna impostazioni blur"""
        self.status_info["current_blur"] = strength
        logger.info(f"🌀 Blur aggiornato: {strength} ({mode})")
        return {"success": True, "blur_strength": strength, "blur_mode": mode}
    
    def update_ai(self, quality: str, smoothing: float):
        """Aggiorna impostazioni AI"""
        self.status_info["current_ai_quality"] = quality
        logger.info(f"🤖 AI aggiornato: {quality}, smoothing: {smoothing}")
        return {"success": True, "ai_quality": quality, "ai_smoothing": smoothing}
    
    def get_status(self):
        """Ritorna stato del sistema"""
        return self.status_info

# Istanza globale del motore
engine = StreamBlurEngine()

# FastAPI app
app = FastAPI(title="StreamBlur Pro", version="1.0", description="NVIDIA Broadcast Alternative")

# CORS per comunicazione con Tauri
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
    """Avvia il motore StreamBlur"""
    result = engine.start()
    return JSONResponse(content=result)

@app.post("/api/stop")
async def stop_engine():
    """Ferma il motore StreamBlur"""
    result = engine.stop()
    return JSONResponse(content=result)

@app.get("/api/status")
async def get_status():
    """Stato del sistema"""
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
    return {"status": "ok", "message": "StreamBlur Pro API attivo"}

# === AVVIO SERVER ===

def main():
    """Avvia il server StreamBlur Pro"""
    logger.info("🚀 StreamBlur Pro - Server API")
    logger.info("🎯 NVIDIA Broadcast Alternative")
    logger.info("🌐 Server in avvio su http://127.0.0.1:8080")
    logger.info("✅ Pronto per Tauri!")
    
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8080, 
        log_level="info"
    )

if __name__ == "__main__":
    main()
