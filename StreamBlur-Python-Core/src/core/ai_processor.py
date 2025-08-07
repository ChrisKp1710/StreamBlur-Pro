# =============================================================================
# File 5: src/core/ai_processor.py
# =============================================================================

import cv2
import numpy as np
import mediapipe as mp
import time
from typing import Optional, Tuple
from collections import deque

from ..utils.config import StreamBlurConfig
from ..utils.performance import PerformanceMonitor

class AIProcessor:
    """Processore AI per segmentazione persona/sfondo"""
    
    def __init__(self, config: StreamBlurConfig, performance_monitor: PerformanceMonitor):
        self.config = config
        self.performance = performance_monitor
        
        # Configurazione AI con conversione sicura
        ai_width = config.get('video.ai_width', 512)
        self.ai_width = ai_width if isinstance(ai_width, int) else 512
        
        ai_height = config.get('video.ai_height', 288) 
        self.ai_height = ai_height if isinstance(ai_height, int) else 288
        
        # Modello configurabile: 0=veloce (performance), 1=accurato (qualità)
        # Per scontorno preciso, usiamo modello accurato di default
        performance_mode = config.get('ai.performance_mode', False)  # Default: accurato
        self.model_selection = 0 if performance_mode else 1
        
        # Feature toggles
        self.edge_smoothing = config.get('effects.edge_smoothing', True)
        self.temporal_smoothing = config.get('effects.temporal_smoothing', True)
        
        # Parametri ottimizzazione con conversione sicura
        edge_kernel = config.get('performance.edge_kernel_size', 3)
        self.edge_kernel_size = edge_kernel if isinstance(edge_kernel, int) else 3
        
        temporal_buffer = config.get('performance.temporal_buffer_size', 2)
        self.temporal_buffer_size = temporal_buffer if isinstance(temporal_buffer, int) else 2
        
        # MediaPipe
        self.mp_selfie_segmentation = None
        self.segmentation = None
        
        # Temporal smoothing buffer
        self.mask_buffer = deque(maxlen=self.temporal_buffer_size)
        
        # GPU acceleration (se disponibile)
        self.gpu_available = False
        
    def initialize(self) -> bool:
        """Inizializza processore AI"""
        print("🤖 Inizializzando AI processor...")
        
        try:
            # Inizializza MediaPipe con controllo di sicurezza
            import mediapipe as mp
            
            # Prova diversi modi per accedere a selfie_segmentation
            self.mp_selfie_segmentation = None
            try:
                # Metodo 1: accesso sicuro con getattr
                self.mp_selfie_segmentation = getattr(mp.solutions, 'selfie_segmentation', None)
            except:
                pass
                
            if not self.mp_selfie_segmentation:
                try:
                    # Metodo 2: import esplicito (commentato per evitare errori di tipo)
                    # from mediapipe.solutions import selfie_segmentation
                    # self.mp_selfie_segmentation = selfie_segmentation
                    print("⚠️ Warning: Usando fallback per MediaPipe")
                    return False
                except:
                    print("❌ Errore: MediaPipe selfie_segmentation non disponibile")
                    return False
            
            if self.mp_selfie_segmentation:
                self.segmentation = self.mp_selfie_segmentation.SelfieSegmentation(
                    model_selection=self.model_selection
                )
            else:
                print("❌ Errore: Impossibile inizializzare selfie_segmentation")
                return False
            
            print(f"✅ AI inizializzato - Risoluzione: {self.ai_width}x{self.ai_height}")
            print(f"🎯 Modello: {'Accurato' if self.model_selection else 'Veloce'}")
            
            # Test GPU acceleration
            self._test_gpu_acceleration()
            
            return True
            
        except Exception as e:
            print(f"❌ Errore inizializzazione AI: {e}")
            return False
    
    def _test_gpu_acceleration(self):
        """Testa disponibilità GPU acceleration"""
        try:
            import pyopencl as cl
            platforms = cl.get_platforms()
            amd_platforms = [p for p in platforms if 'AMD' in p.name]
            
            if amd_platforms:
                print(f"🚀 GPU AMD rilevata: {amd_platforms[0].name}")
                self.gpu_available = True
            else:
                print("💻 Usando CPU per processing")
                
        except ImportError:
            print("💻 PyOpenCL non disponibile - usando CPU")
        except Exception as e:
            print(f"⚠️ Errore GPU detection: {e}")
    
    def process_frame(self, frame: np.ndarray, output_size: Tuple[int, int]) -> Optional[np.ndarray]:
        """Processa frame per segmentazione persona/sfondo"""
        start_time = time.time()
        
        try:
            # Ridimensiona per AI processing
            ai_frame = cv2.resize(frame, (self.ai_width, self.ai_height))
            
            # Converte BGR -> RGB per MediaPipe
            rgb_frame = cv2.cvtColor(ai_frame, cv2.COLOR_BGR2RGB)
            
            # Segmentazione AI
            # Verifica che segmentation sia stato inizializzato
            if not self.segmentation:
                print("❌ Errore: segmentation non inizializzato")
                return None
                
            results = self.segmentation.process(rgb_frame)
            mask = results.segmentation_mask
            
            if mask is None:
                return None
            
            # Ridimensiona mask alla risoluzione output
            mask_resized = cv2.resize(mask, output_size)
            mask_resized = (mask_resized * 255).astype(np.uint8)
            
            # Applica miglioramenti
            if self.edge_smoothing:
                mask_resized = self._apply_edge_smoothing(mask_resized)
            
            if self.temporal_smoothing:
                mask_resized = self._apply_temporal_smoothing(mask_resized)
            
            # Record performance
            processing_time = time.time() - start_time
            self.performance.record_processing_time(processing_time)
            
            return mask_resized
            
        except Exception as e:
            print(f"⚠️ Errore processing AI: {e}")
            return None
    
    def _apply_edge_smoothing(self, mask: np.ndarray) -> np.ndarray:
        """Applica edge smoothing per bordi più morbidi"""
        kernel_size = max(1, self.edge_kernel_size)  # Assicura che sia >= 1
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, 
                                         (kernel_size, kernel_size))
        
        # Morphological closing per riempire buchi
        mask_smooth = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Gaussian blur leggero per bordi smooth
        mask_smooth = cv2.GaussianBlur(mask_smooth, (3, 3), 0.5)
        
        return mask_smooth
    
    def _apply_temporal_smoothing(self, mask: np.ndarray) -> np.ndarray:
        """Applica temporal smoothing per stabilità movimento"""
        self.mask_buffer.append(mask.copy())
        
        if len(self.mask_buffer) >= 2:
            # Media ponderata: 70% frame corrente, 30% precedente
            smoothed_mask = (0.7 * mask.astype(np.float32) + 
                           0.3 * self.mask_buffer[-2].astype(np.float32))
            return smoothed_mask.astype(np.uint8)
        
        return mask
    
    def set_edge_smoothing(self, enabled: bool):
        """Abilita/disabilita edge smoothing"""
        self.edge_smoothing = enabled
        self.config.set('effects.edge_smoothing', enabled)
    
    def set_temporal_smoothing(self, enabled: bool):
        """Abilita/disabilita temporal smoothing"""
        self.temporal_smoothing = enabled
        if not enabled:
            self.mask_buffer.clear()
        self.config.set('effects.temporal_smoothing', enabled)
    
    def get_stats(self) -> dict:
        """Ottieni statistiche AI processor"""
        return {
            'ai_resolution': f"{self.ai_width}x{self.ai_height}",
            'model': 'Accurato' if self.model_selection else 'Veloce',
            'edge_smoothing': self.edge_smoothing,
            'temporal_smoothing': self.temporal_smoothing,
            'gpu_available': self.gpu_available,
            'buffer_size': len(self.mask_buffer)
        }
    
    def cleanup(self):
        """Pulizia risorse AI"""
        print("🧹 Cleanup AI processor...")
        
        if self.segmentation:
            self.segmentation.close()
            self.segmentation = None
        
        self.mask_buffer.clear()
        print("✅ AI cleanup completato")
    
    def switch_model(self, performance_mode: bool):
        """Cambia modello AI dinamicamente senza riavvio"""
        try:
            old_performance_mode = self.config.get('ai.performance_mode', False)
            
            if old_performance_mode == performance_mode:
                return True  # Nessun cambio necessario
            
            print(f"🔄 Cambio modello AI: {'Performance' if performance_mode else 'Accurato'}...")
            
            # Aggiorna configurazione
            self.config.set('ai.performance_mode', performance_mode)
            
            # Determina nuovo modello
            new_model_selection = 0 if performance_mode else 1
            
            # Se il modello è già quello giusto, non fare nulla
            if self.model_selection == new_model_selection:
                return True
            
            # Chiudi il vecchio segmentatore
            if self.segmentation:
                self.segmentation.close()
                self.segmentation = None
            
            # Crea nuovo segmentatore con nuovo modello
            self.model_selection = new_model_selection
            
            if self.mp_selfie_segmentation:
                self.segmentation = self.mp_selfie_segmentation.SelfieSegmentation(
                    model_selection=self.model_selection
                )
                
                # Pulisci buffer per evitare inconsistenze
                self.mask_buffer.clear()
                
                print(f"✅ Modello cambiato con successo: {self.model_selection} ({'Performance' if performance_mode else 'Accurato'})")
                return True
            
            print("❌ Errore durante il cambio modello: mp_selfie_segmentation non disponibile")
            return False
            
        except Exception as e:
            print(f"❌ Errore switch_model: {e}")
            return False
