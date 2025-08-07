# =============================================================================
# File 7: src/core/virtual_camera.py
# =============================================================================

import cv2
import numpy as np
import pyvirtualcam
import time
from threading import Thread, Lock
import queue
from typing import Optional, Dict, Any

from ..utils.config import StreamBlurConfig
from ..utils.performance import PerformanceMonitor

class VirtualCameraManager:
    """Gestione Virtual Camera per StreamBlur Pro"""
    
    def __init__(self, config: StreamBlurConfig, performance_monitor: PerformanceMonitor):
        self.config = config
        self.performance = performance_monitor
        
        # Configurazione con conversione sicura
        width = config.get('video.camera_width', 1280)
        self.width = width if isinstance(width, int) else 1280
        
        height = config.get('video.camera_height', 720)
        self.height = height if isinstance(height, int) else 720
        
        fps = config.get('video.fps', 30)
        self.fps = fps if isinstance(fps, (int, float)) else 30
        
        format_name = config.get('virtual_camera.format', 'BGR')
        self.format = getattr(pyvirtualcam.PixelFormat, 
                            format_name if isinstance(format_name, str) else 'BGR')
        
        # Virtual Camera
        self.virtual_cam: Optional[pyvirtualcam.Camera] = None
        self.is_active = False
        self.is_running = False
        
        # Threading
        self.output_thread: Optional[Thread] = None
        self.frame_queue = queue.Queue(maxsize=2)
        self.lock = Lock()
        
        # Stats
        self.frames_sent = 0
        self.frames_dropped = 0
        
    def initialize(self) -> bool:
        """Inizializza Virtual Camera"""
        print("📺 Inizializzando Virtual Camera...")
        
        try:
            self.virtual_cam = pyvirtualcam.Camera(
                width=int(self.width),
                height=int(self.height),
                fps=float(self.fps),
                fmt=self.format
            )
            
            device_name = getattr(self.virtual_cam, 'device', 'Virtual Camera')
            print(f"✅ Virtual Camera creata: {device_name}")
            print(f"📐 Risoluzione: {self.width}x{self.height} @ {self.fps} FPS")
            
            self.is_active = True
            return True
            
        except Exception as e:
            print(f"❌ Errore Virtual Camera: {e}")
            print("💡 Assicurati che OBS Virtual Camera sia installato")
            return False
    
    def start_streaming(self) -> bool:
        """Avvia streaming verso Virtual Camera"""
        if not self.is_active:
            print("❌ Virtual Camera non inizializzata")
            return False
            
        if self.is_running:
            print("⚠️ Streaming già attivo")
            return True
        
        self.is_running = True
        self.output_thread = Thread(target=self._output_loop, daemon=True)
        self.output_thread.start()
        
        print("📡 Streaming Virtual Camera avviato")
        return True
    
    def stop_streaming(self):
        """Ferma streaming"""
        self.is_running = False
        
        if self.output_thread and self.output_thread.is_alive():
            self.output_thread.join(timeout=1.0)
        
        print("⏹️ Streaming Virtual Camera fermato")
    
    def send_frame(self, frame: np.ndarray) -> bool:
        """Invia frame alla Virtual Camera"""
        if not self.is_running:
            return False
        
        try:
            # Ridimensiona se necessario
            target_size = (int(self.height), int(self.width))
            if frame.shape[:2] != target_size:
                frame = cv2.resize(frame, (int(self.width), int(self.height)))
            
            # Aggiungi alla queue
            if not self.frame_queue.full():
                self.frame_queue.put(frame.copy())
                return True
            else:
                # Queue piena, scarta frame
                with self.lock:
                    self.frames_dropped += 1
                return False
                
        except Exception as e:
            print(f"⚠️ Errore invio frame: {e}")
            return False
    
    def _output_loop(self):
        """Loop output Virtual Camera (thread separato)"""
        print("📺 Thread Virtual Camera avviato...")
        
        while self.is_running:
            try:
                # Ottieni frame dalla queue
                frame = self.frame_queue.get(timeout=0.1)
                
                if self.virtual_cam:
                    self.virtual_cam.send(frame)
                    
                    with self.lock:
                        self.frames_sent += 1
                    
                    # Aggiorna FPS counter
                    self.performance.update_fps()
                    
            except queue.Empty:
                continue
            except Exception as e:
                print(f"⚠️ Errore output loop: {e}")
                time.sleep(0.1)
        
        print("📺 Thread Virtual Camera terminato")
    
    def get_stats(self) -> Dict[str, Any]:
        """Ottieni statistiche Virtual Camera"""
        with self.lock:
            return {
                'is_active': self.is_active,
                'is_running': self.is_running,
                'frames_sent': self.frames_sent,
                'frames_dropped': self.frames_dropped,
                'queue_size': self.frame_queue.qsize(),
                'resolution': f"{self.width}x{self.height}",
                'fps_target': self.fps
            }
    
    def cleanup(self):
        """Pulizia risorse"""
        print("🧹 Cleanup Virtual Camera...")
        
        self.stop_streaming()
        
        if self.virtual_cam:
            self.virtual_cam.close()
            self.virtual_cam = None
        
        self.is_active = False
        
        # Svuota queue
        while not self.frame_queue.empty():
            try:
                self.frame_queue.get_nowait()
            except queue.Empty:
                break
        
        print("✅ Virtual Camera cleanup completato")