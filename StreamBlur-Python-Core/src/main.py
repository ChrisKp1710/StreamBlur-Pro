# =============================================================================
# File 9: src/main.py
# =============================================================================

#!/usr/bin/env python3
"""
StreamBlur Pro v4.0 - Modular Edition
Entry point principale dell'applicazione

Author: StreamBlur Pro Team
License: MIT
"""

import sys
import os
import time
from threading import Thread
from typing import Optional

# Aggiungi src al path per import relativi
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import assoluti per funzionare con python src/main.py
try:
    # Prova import relativi (se eseguito come modulo)
    from .utils.config import StreamBlurConfig
    from .utils.performance import PerformanceMonitor
    from .core.camera import CameraManager
    from .core.ai_processor import AIProcessor
    from .core.effects import EffectsProcessor
    from .core.virtual_camera import VirtualCameraManager
    from .api_server import get_api_server
except ImportError:
    # Fallback a import assoluti (se eseguito direttamente)
    from utils.config import StreamBlurConfig
    from utils.performance import PerformanceMonitor
    from core.camera import CameraManager
    from core.ai_processor import AIProcessor
    from core.effects import EffectsProcessor
    from core.virtual_camera import VirtualCameraManager
    from api_server import get_api_server

# Scegli quale UI utilizzare
USE_MODERN_UI = False  # Usa la UI classica MODERNIZZATA

if USE_MODERN_UI:
    try:
        from .gui.modern_control_panel import ModernStreamBlurPanel as ControlPanel
    except ImportError:
        from gui.modern_control_panel import ModernStreamBlurPanel as ControlPanel
else:
    try:
        from .gui.control_panel import StreamBlurControlPanel as ControlPanel
    except ImportError:
        from gui.control_panel import StreamBlurControlPanel as ControlPanel

class StreamBlurProApp:
    """Applicazione principale StreamBlur Pro"""
    
    def __init__(self):
        """Inizializza applicazione"""
        print("🚀 StreamBlur Pro v4.0 - Modular Edition")
        print("🎯 La tua alternativa open-source a NVIDIA Broadcast!")
        print()
        
        # Inizializza configurazione e monitoring
        self.config = StreamBlurConfig()
        self.performance = PerformanceMonitor()
        
        # Inizializza moduli core
        self.camera = CameraManager(self.config, self.performance)
        self.ai_processor = AIProcessor(self.config, self.performance)
        self.effects = EffectsProcessor(self.config)
        self.virtual_camera = VirtualCameraManager(self.config, self.performance)
        
        # API Server per comunicazione con Tauri
        self.api_server = get_api_server(8080)
        
        # GUI
        self.gui: Optional[ControlPanel] = None
        
        # Processing state
        self.is_processing = False
        self.processing_thread: Optional[Thread] = None
        self.preview_enabled = False
        
        print("✅ StreamBlur Pro inizializzato!")
    
    def initialize(self) -> bool:
        """Inizializza tutti i componenti"""
        print("🔧 Inizializzando componenti...")
        
        # Inizializza camera
        if not self.camera.initialize():
            return False
        
        # Inizializza AI
        if not self.ai_processor.initialize():
            return False
        
        # Inizializza virtual camera
        if not self.virtual_camera.initialize():
            return False
        
        # Configura API server con riferimenti ai componenti
        self.api_server.set_components(
            self.camera, 
            self.ai_processor, 
            self.effects, 
            self.virtual_camera, 
            self.performance
        )
        
        # Avvia API server
        self.api_server.start_server()
        
        print("✅ Tutti i componenti inizializzati!")
        print("🌐 API Server disponibile su http://127.0.0.1:8080")
        return True
    
    def start_processing(self) -> bool:
        """Avvia processing completo"""
        if self.is_processing:
            print("⚠️ Processing già attivo!")
            return False
        
        print("🎬 Avviando StreamBlur Pro...")
        
        # Avvia camera
        if not self.camera.start_capture():
            return False
        
        # Avvia virtual camera
        if not self.virtual_camera.start_streaming():
            return False
        
        # Avvia performance monitoring
        self.performance.start_monitoring()
        
        # Avvia processing thread
        self.is_processing = True
        self.processing_thread = Thread(target=self._processing_loop, daemon=True)
        self.processing_thread.start()
        
        # Aggiorna stato API
        self.api_server.update_running_state(True)
        
        print("✅ StreamBlur Pro attivo!")
        print("🎯 Ora puoi usare 'OBS Virtual Camera' nelle tue app!")
        
        return True
    
    def stop_processing(self):
        """Ferma processing"""
        if not self.is_processing:
            return
        
        print("⏹️ Fermando StreamBlur Pro...")
        
        self.is_processing = False
        
        # Ferma thread processing
        if self.processing_thread and self.processing_thread.is_alive():
            self.processing_thread.join(timeout=2.0)
        
        # Ferma componenti
        self.camera.stop_capture()
        self.virtual_camera.stop_streaming()
        self.performance.stop_monitoring()
        
        # Aggiorna stato API
        self.api_server.update_running_state(False)
        
        print("✅ StreamBlur Pro fermato!")
    
    def _processing_loop(self):
        """Loop principale processing (thread separato)"""
        print("🔄 Loop processing avviato...")
        
        while self.is_processing:
            start_time = time.time()
            
            try:
                # Ottieni frame dalla camera
                frame = self.camera.get_frame()
                if frame is None:
                    time.sleep(0.001)
                    continue
                
                # Applica noise reduction se abilitato
                processed_frame = self.effects.apply_noise_reduction(frame)
                
                # Processa con AI per ottenere mask
                output_size = (processed_frame.shape[1], processed_frame.shape[0])
                mask = self.ai_processor.process_frame(processed_frame, output_size)
                
                if mask is not None:
                    # Applica blur allo sfondo
                    final_frame = self.effects.apply_background_blur(processed_frame, mask)
                    
                    # Invia alla virtual camera
                    self.virtual_camera.send_frame(final_frame)
                    
                    # Preview se abilitato
                    if self.preview_enabled:
                        self._show_preview(final_frame)
                
                # Aggiorna metriche sistema periodicamente
                if int(time.time()) % 5 == 0:  # Ogni 5 secondi
                    self.performance.update_system_metrics()
                
            except Exception as e:
                print(f"⚠️ Errore processing loop: {e}")
                time.sleep(0.1)
            
            # Piccola pausa per non saturare CPU
            time.sleep(0.001)
        
        print("🔄 Loop processing terminato")
    
    def _show_preview(self, frame):
        """Mostra preview (se abilitato)"""
        import cv2
        
        # Ridimensiona per preview
        preview_frame = cv2.resize(frame, (640, 480))
        
        # Aggiungi info overlay
        fps = self.performance.current_fps
        cv2.putText(preview_frame, f"FPS: {fps:.1f}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.putText(preview_frame, "StreamBlur Pro v4.0 - Preview", 
                   (10, preview_frame.shape[0] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.imshow('StreamBlur Pro - Preview', preview_frame)
        cv2.waitKey(1)
    
    def toggle_preview(self):
        """Toggle preview window"""
        self.preview_enabled = not self.preview_enabled
        
        if not self.preview_enabled:
            try:
                import cv2
                cv2.destroyWindow('StreamBlur Pro - Preview')
            except Exception:
                # Finestra già chiusa o non esistente
                pass
    
    # Settings methods per GUI
    def set_blur_intensity(self, intensity: int):
        """Imposta intensità blur"""
        self.effects.set_blur_intensity(intensity)
    
    def set_edge_smoothing(self, enabled: bool):
        """Imposta edge smoothing"""
        self.ai_processor.set_edge_smoothing(enabled)
    
    def set_temporal_smoothing(self, enabled: bool):
        """Imposta temporal smoothing"""
        self.ai_processor.set_temporal_smoothing(enabled)
    
    def set_noise_reduction(self, enabled: bool):
        """Imposta noise reduction"""
        self.effects.set_noise_reduction(enabled)
    
    def get_stats(self) -> dict:
        """Ottieni statistiche complete applicazione"""
        perf_stats = self.performance.get_stats()
        camera_stats = self.camera.get_stats()
        virtual_cam_stats = self.virtual_camera.get_stats()
        ai_stats = self.ai_processor.get_stats()
        effects_stats = self.effects.get_stats()
        
        return {
            'is_processing': self.is_processing,
            'fps': perf_stats['fps']['current'],
            'processing_time_ms': perf_stats['processing']['current_ms'],
            'cpu_usage': perf_stats['system']['cpu_percent'],
            'memory_usage': perf_stats['system']['memory_percent'],
            'performance_grade': self.performance.get_performance_grade(),
            'frames_sent': virtual_cam_stats['frames_sent'],
            'frames_dropped': virtual_cam_stats['frames_dropped'],
            'camera_stats': camera_stats,
            'ai_stats': ai_stats,
            'effects_stats': effects_stats,
            'virtual_camera_stats': virtual_cam_stats
        }
    
    def cleanup(self):
        """Pulizia finale applicazione"""
        print("🧹 Cleanup StreamBlur Pro...")
        
        # Ferma processing
        self.stop_processing()
        
        # Cleanup moduli
        self.camera.cleanup()
        self.ai_processor.cleanup()
        self.virtual_camera.cleanup()
        
        # Chiudi preview se aperto
        if self.preview_enabled:
            import cv2
            cv2.destroyAllWindows()
        
        print("✅ StreamBlur Pro cleanup completato!")
    
    def run_gui(self):
        """Avvia con interfaccia grafica"""
        """Avvia GUI"""
        print("🖥️ Avvio interfaccia grafica...")
        self.gui = ControlPanel(self)
        self.gui.run()
    
    def run_cli(self):
        """Avvia in modalità command line"""
        print("🎮 Modalità Command Line")
        print("Controlli: [+/-] Blur, [e] Edge, [t] Temporal, [n] Noise, [p] Preview, [q] Esci")
        
        if not self.start_processing():
            return
        
        try:
            while True:
                cmd = input().lower().strip()
                
                if cmd == 'q':
                    break
                elif cmd == '+':
                    current = self.effects.blur_intensity
                    current_value = current if isinstance(current, int) else 15
                    self.set_blur_intensity(min(25, current_value + 2))
                    print(f"🔵 Blur: {self.effects.blur_intensity}")
                elif cmd == '-':
                    current = self.effects.blur_intensity  
                    current_value = current if isinstance(current, int) else 15
                    self.set_blur_intensity(max(1, current_value - 2))
                    print(f"🔵 Blur: {self.effects.blur_intensity}")
                elif cmd == 'e':
                    current = self.ai_processor.edge_smoothing
                    self.set_edge_smoothing(not current)
                    print(f"🎯 Edge Smoothing: {'ON' if not current else 'OFF'}")
                elif cmd == 't':
                    current = self.ai_processor.temporal_smoothing
                    self.set_temporal_smoothing(not current)
                    print(f"⏱️ Temporal Smoothing: {'ON' if not current else 'OFF'}")
                elif cmd == 'n':
                    current = self.effects.noise_reduction
                    self.set_noise_reduction(not current)
                    print(f"🔧 Noise Reduction: {'ON' if not current else 'OFF'}")
                elif cmd == 'p':
                    self.toggle_preview()
                    print(f"👁️ Preview: {'ON' if self.preview_enabled else 'OFF'}")
                elif cmd == 's':
                    stats = self.get_stats()
                    print(f"📊 Stats: {stats['fps']:.1f} FPS, {stats['processing_time_ms']:.1f}ms, {stats['performance_grade']}")
                
        except KeyboardInterrupt:
            pass
        
        self.stop_processing()

def main():
    """Entry point principale"""
    
    # Banner
    print("=" * 60)
    print("🎥 StreamBlur Pro v4.0 - Modular Edition")
    print("🎯 Open Source Alternative to NVIDIA Broadcast for AMD")
    print("⚡ Optimized for AMD RX 7900 XTX + Ryzen 9 5900X")
    print("=" * 60)
    print()
    
    # Crea applicazione
    try:
        app = StreamBlurProApp()
        
        # Inizializza componenti
        if not app.initialize():
            print("❌ Inizializzazione fallita!")
            return 1
        
        # Controlla argomenti command line
        if len(sys.argv) > 1 and sys.argv[1] == '--cli':
            app.run_cli()
        else:
            app.run_gui()
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⏹️ Interruzione utente")
        return 0
    except Exception as e:
        print(f"❌ Errore critico: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())