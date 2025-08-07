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
import mediapipe as mp
import pyvirtualcam

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
    """Motore principale StreamBlur Pro con AI Segmentation"""
    
    def __init__(self):
        self.is_running = False
        self.virtual_camera = None
        self.webcam = None
        self.selfie_segmentation = None
        
        # Stato del sistema
        self.status_info = {
            "is_running": False,
            "current_blur": 5.0,
            "current_ai_quality": "high",
            "frames_processed": 0,
            "fps": 30.0,
            "virtual_camera_active": False
        }
        
    def start_camera(self):
        """Avvia la webcam e MediaPipe"""
        if self.is_running:
            logger.info("StreamBlur Pro è già in esecuzione")
            return {"status": "already_running"}
        
        try:
            # Inizializza webcam
            self.webcam = cv2.VideoCapture(0)
            if not self.webcam.isOpened():
                raise Exception("Impossibile aprire la webcam")
            
            # Configura webcam per performance ottimali
            self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.webcam.set(cv2.CAP_PROP_FPS, 30)
            
            # Inizializza MediaPipe per segmentazione AI
            mp_selfie_segmentation = mp.solutions.selfie_segmentation
            self.selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(
                model_selection=1 if self.status_info["current_ai_quality"] == "high" else 0
            )
            
            # Inizializza virtual camera
            self.virtual_camera = pyvirtualcam.Camera(
                width=1280, 
                height=720, 
                fps=30, 
                fmt=pyvirtualcam.PixelFormat.RGB
            )
            
            self.is_running = True
            self.status_info["is_running"] = True
            self.status_info["virtual_camera_active"] = True
            self.status_info["frames_processed"] = 0
            
            logger.info("StreamBlur Pro avviato con successo con AI Segmentation")
            return {"status": "success", "message": "StreamBlur Pro avviato con AI Segmentation"}
            
        except Exception as e:
            logger.error(f"Errore nell'avvio di StreamBlur Pro: {e}")
            self.cleanup()
            return {"status": "error", "error": str(e)}
    
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
        """Applica effetto blur SOLO allo sfondo usando AI segmentation"""
        if self.status_info["current_blur"] <= 0:
            return frame
        
        try:
            # Converti frame per MediaPipe (RGB)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Ottieni la maschera di segmentazione della persona
            results = self.selfie_segmentation.process(rgb_frame)
            
            # La maschera: 1.0 = persona, 0.0 = sfondo
            segmentation_mask = results.segmentation_mask
            
            # Crea una maschera binaria per la persona (soglia 0.5)
            person_mask = (segmentation_mask > 0.5).astype('uint8') * 255
            
            # Inverti la maschera per ottenere solo lo sfondo
            background_mask = cv2.bitwise_not(person_mask)
            
            # Applica blur intenso al frame originale
            blur_intensity = int(self.status_info["current_blur"] * 2)
            if blur_intensity % 2 == 0:
                blur_intensity += 1  # Deve essere dispari
            
            blurred_frame = cv2.GaussianBlur(frame, (blur_intensity, blur_intensity), 0)
            
            # Converti le maschere in 3 canali per la fusione
            person_mask_3ch = cv2.cvtColor(person_mask, cv2.COLOR_GRAY2BGR)
            background_mask_3ch = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)
            
            # Normalizza le maschere (0-1)
            person_mask_3ch = person_mask_3ch.astype('float32') / 255.0
            background_mask_3ch = background_mask_3ch.astype('float32') / 255.0
            
            # Combina: persona originale + sfondo sfocato
            result = (frame.astype('float32') * person_mask_3ch + 
                     blurred_frame.astype('float32') * background_mask_3ch)
            
            return result.astype('uint8')
            
        except Exception as e:
            logger.error(f"Errore nell'applicazione del blur AI: {e}")
            # Fallback al blur tradizionale se AI fallisce
            blur_intensity = int(self.status_info["current_blur"] * 2)
            if blur_intensity > 0:
                if blur_intensity % 2 == 0:
                    blur_intensity += 1
                return cv2.GaussianBlur(frame, (blur_intensity, blur_intensity), 0)
            return frame
    
    def update_blur(self, strength: float, mode: str):
        """Aggiorna impostazioni blur"""
        self.status_info["current_blur"] = strength
        logger.info(f"🌀 Blur aggiornato: {strength} ({mode})")
        return {"success": True, "blur_strength": strength, "blur_mode": mode}
    
    def update_ai(self, quality: str, smoothing: float):
        """Aggiorna impostazioni AI e reinizializza MediaPipe se necessario"""
        old_quality = self.status_info["current_ai_quality"]
        self.status_info["current_ai_quality"] = quality
        
        # Se cambia la qualità e MediaPipe è attivo, reinizializza
        if (old_quality != quality and 
            self.selfie_segmentation is not None and 
            self.is_running):
            try:
                # Chiudi l'istanza corrente
                self.selfie_segmentation.close()
                
                # Crea nuova istanza con la qualità aggiornata
                mp_selfie_segmentation = mp.solutions.selfie_segmentation
                self.selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(
                    model_selection=1 if quality == "high" else 0
                )
                logger.info(f"🤖 MediaPipe reinizializzato con qualità: {quality}")
            except Exception as e:
                logger.error(f"Errore nel reinizializzare MediaPipe: {e}")
        
        logger.info(f"🤖 AI aggiornato: {quality}, smoothing: {smoothing}")
        return {"success": True, "ai_quality": quality, "ai_smoothing": smoothing}
    
    def get_status(self):
        """Ritorna stato del sistema"""
        return self.status_info
    
    def cleanup(self):
        """Pulisce tutte le risorse"""
        try:
            if self.webcam:
                self.webcam.release()
                self.webcam = None
                
            if self.virtual_camera:
                self.virtual_camera.close()
                self.virtual_camera = None
                
            if self.selfie_segmentation:
                self.selfie_segmentation.close()
                self.selfie_segmentation = None
                
            self.is_running = False
            self.status_info["is_running"] = False
            self.status_info["virtual_camera_active"] = False
            
            logger.info("Risorse rilasciate con successo")
        except Exception as e:
            logger.error(f"Errore nella pulizia delle risorse: {e}")

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
