# =============================================================================
# File 3: src/utils/performance.py  
# =============================================================================

import time
import psutil
from threading import Lock
from collections import deque
from typing import Dict, List

class PerformanceMonitor:
    """Monitor performance per StreamBlur Pro"""
    
    def __init__(self, history_size: int = 100):
        self.history_size = history_size
        self.lock = Lock()
        
        # Metriche FPS
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.current_fps = 0.0
        self.fps_history = deque(maxlen=history_size)
        
        # Metriche processing time
        self.processing_times = deque(maxlen=history_size)
        self.current_processing_time = 0.0
        
        # Metriche sistema
        self.cpu_usage = 0.0
        self.memory_usage = 0.0
        self.gpu_usage = 0.0  # Se disponibile
        
        # Stati
        self.is_monitoring = False
        
    def start_monitoring(self):
        """Avvia monitoring"""
        self.is_monitoring = True
        self.fps_start_time = time.time()
        self.fps_counter = 0
    
    def stop_monitoring(self):
        """Ferma monitoring"""
        self.is_monitoring = False
    
    def update_fps(self):
        """Aggiorna contatore FPS"""
        if not self.is_monitoring:
            return
            
        with self.lock:
            self.fps_counter += 1
            
            current_time = time.time()
            elapsed = current_time - self.fps_start_time
            
            if elapsed >= 1.0:
                self.current_fps = self.fps_counter / elapsed
                self.fps_history.append(self.current_fps)
                self.fps_counter = 0
                self.fps_start_time = current_time
    
    def record_processing_time(self, processing_time: float):
        """Registra tempo di processing"""
        with self.lock:
            self.current_processing_time = processing_time
            self.processing_times.append(processing_time)
    
    def update_system_metrics(self):
        """Aggiorna metriche sistema"""
        try:
            self.cpu_usage = psutil.cpu_percent(interval=None)
            self.memory_usage = psutil.virtual_memory().percent
        except Exception as e:
            print(f"⚠️ Errore metriche sistema: {e}")
    
    def get_stats(self) -> Dict:
        """Ottieni statistiche complete"""
        with self.lock:
            avg_fps = sum(self.fps_history) / len(self.fps_history) if self.fps_history else 0
            avg_processing = sum(self.processing_times) / len(self.processing_times) if self.processing_times else 0
            
            return {
                'fps': {
                    'current': self.current_fps,
                    'average': avg_fps,
                    'min': min(self.fps_history) if self.fps_history else 0,
                    'max': max(self.fps_history) if self.fps_history else 0
                },
                'processing': {
                    'current_ms': self.current_processing_time * 1000,
                    'average_ms': avg_processing * 1000,
                    'min_ms': min(self.processing_times) * 1000 if self.processing_times else 0,
                    'max_ms': max(self.processing_times) * 1000 if self.processing_times else 0
                },
                'system': {
                    'cpu_percent': self.cpu_usage,
                    'memory_percent': self.memory_usage,
                    'gpu_percent': self.gpu_usage
                }
            }
    
    def get_performance_grade(self) -> str:
        """Ottieni valutazione performance"""
        stats = self.get_stats()
        fps = stats['fps']['current']
        processing_ms = stats['processing']['current_ms']
        
        if fps >= 25 and processing_ms <= 40:
            return "🟢 Eccellente"
        elif fps >= 20 and processing_ms <= 60:
            return "🟡 Buono"
        elif fps >= 15 and processing_ms <= 80:
            return "🟠 Accettabile"
        else:
            return "🔴 Scadente"