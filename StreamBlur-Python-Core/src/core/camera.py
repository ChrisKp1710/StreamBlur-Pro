# =============================================================================
# File 4: src/core/camera.py
# =============================================================================

import cv2
import numpy as np
from threading import Thread, Lock
import queue
import time
from typing import Optional, Tuple, Dict, Any

from ..utils.config import StreamBlurConfig
from ..utils.performance import PerformanceMonitor

class CameraManager:
    """Gestione webcam per StreamBlur Pro"""
    
    def __init__(self, config: StreamBlurConfig, performance_monitor: PerformanceMonitor):
        self.config = config
        self.performance = performance_monitor
        
        # Configurazione camera con conversione sicura
        width = config.get('video.camera_width', 1280)
        self.width = width if isinstance(width, int) else 1280
        
        height = config.get('video.camera_height', 720)
        self.height = height if isinstance(height, int) else 720
        
        fps = config.get('video.fps', 30)
        self.fps = fps if isinstance(fps, (int, float)) else 30
        
        buffer_size = config.get('performance.buffer_size', 2)
        self.buffer_size = buffer_size if isinstance(buffer_size, int) else 2
        
        # Camera
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_running = False
        
        # Threading
        self.capture_thread: Optional[Thread] = None
        self.frame_queue = queue.Queue(maxsize=self.buffer_size)
        self.lock = Lock()
        
        # Stats
        self.frames_captured = 0
        self.frames_dropped = 0
        
    def initialize(self) -> bool:
        """Inizializza camera"""
        print("📹 Inizializzando camera...")
        
        try:
            self.cap = cv2.VideoCapture(0)
            
            if not self.cap.isOpened():
                print("❌ Impossibile aprire la webcam")
                return False
            
            # Configurazione camera
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, float(self.width))
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, float(self.height))
            self.cap.set(cv2.CAP_PROP_FPS, float(self.fps))
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Riduce latenza
            
            # Ottimizzazioni per qualità AI
            self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
            self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
            
            # Verifica configurazione effettiva
            actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            actual_fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            
            print(f"✅ Camera OK - {actual_width}x{actual_height} @ {actual_fps} FPS")
            
            return True
            
        except Exception as e:
            print(f"❌ Errore inizializzazione camera: {e}")
            return False
    
    def start_capture(self) -> bool:
        """Avvia cattura frame"""
        if not self.cap or not self.cap.isOpened():
            print("❌ Camera non inizializzata")
            return False
        
        if self.is_running:
            print("⚠️ Cattura già attiva")
            return True
        
        self.is_running = True
        self.capture_thread = Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()
        
        print("▶️ Cattura frame avviata")
        return True
    
    def stop_capture(self):
        """Ferma cattura frame"""
        self.is_running = False
        
        if self.capture_thread and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=1.0)
        
        print("⏹️ Cattura frame fermata")
    
    def _capture_loop(self):
        """Loop cattura frame (thread separato)"""
        print("📹 Thread cattura avviato...")
        
        while self.is_running:
            if not self.cap or not self.cap.isOpened():
                break
                
            ret, frame = self.cap.read()
            
            if ret:
                with self.lock:
                    self.frames_captured += 1
                    
                    # Aggiungi frame alla queue
                    if not self.frame_queue.full():
                        self.frame_queue.put(frame.copy())
                    else:
                        # Queue piena, scarta frame
                        self.frames_dropped += 1
                        try:
                            self.frame_queue.get_nowait()  # Rimuovi frame vecchio
                            self.frame_queue.put(frame.copy())  # Aggiungi nuovo
                        except queue.Empty:
                            pass
            
            # Piccola pausa per non saturare CPU
            time.sleep(0.001)
        
        print("📹 Thread cattura terminato")
    
    def get_frame(self) -> Optional[np.ndarray]:
        """Ottieni frame più recente"""
        try:
            return self.frame_queue.get_nowait()
        except queue.Empty:
            return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Ottieni statistiche camera"""
        with self.lock:
            return {
                'frames_captured': self.frames_captured,
                'frames_dropped': self.frames_dropped,
                'queue_size': self.frame_queue.qsize(),
                'drop_rate': self.frames_dropped / max(self.frames_captured, 1) * 100
            }
    
    def cleanup(self):
        """Pulizia risorse"""
        print("🧹 Cleanup camera...")
        
        self.stop_capture()
        
        if self.cap and self.cap.isOpened():
            self.cap.release()
            self.cap = None
        
        # Svuota queue
        while not self.frame_queue.empty():
            try:
                self.frame_queue.get_nowait()
            except queue.Empty:
                break
        
        print("✅ Camera cleanup completato")
