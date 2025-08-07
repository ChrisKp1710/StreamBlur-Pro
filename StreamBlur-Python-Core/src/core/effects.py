# =============================================================================
# File 6: src/core/effects.py
# =============================================================================

import cv2
import numpy as np
from typing import Optional, Tuple
from ..utils.config import StreamBlurConfig

class EffectsProcessor:
    """Processore effetti per StreamBlur Pro"""
    
    def __init__(self, config: StreamBlurConfig):
        self.config = config
        
        # Configurazione effetti con conversione sicura
        blur_intensity = config.get('effects.blur_intensity', 15)
        self.blur_intensity = blur_intensity if isinstance(blur_intensity, int) else 15
        
        noise_reduction = config.get('effects.noise_reduction', False)
        self.noise_reduction = noise_reduction if isinstance(noise_reduction, bool) else False
        
        # Nuove configurazioni per blur ottimizzato
        intensity_mult = config.get('blur.intensity_multiplier', 1.8)
        self.intensity_multiplier = intensity_mult if isinstance(intensity_mult, (int, float)) else 1.8
        
        algorithm = config.get('blur.algorithm', 'optimized')
        self.algorithm = algorithm if isinstance(algorithm, str) else 'optimized'
        
        use_gpu = config.get('blur.use_gpu_acceleration', True)
        self.use_gpu = use_gpu if isinstance(use_gpu, bool) else True
        
    def apply_background_blur(self, frame: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """Applica blur ibrido - AI accurato + blur ottimizzato per intensità alta"""
        
        # Normalizza mask (0-1 range)
        mask_normalized = mask.astype(np.float32) / 255.0
        
        if self.algorithm == 'optimized':
            return self._apply_optimized_blur(frame, mask_normalized)
        else:
            return self._apply_quality_blur(frame, mask_normalized)
    
    def _apply_optimized_blur(self, frame: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """Blur ottimizzato per intensità alta con prestazioni buone"""
        
        # Calcola intensità effettiva con moltiplicatore
        effective_intensity = int(self.blur_intensity * self.intensity_multiplier)
        
        # Algoritmo a cascata per blur intenso ma efficiente
        if effective_intensity <= 15:
            # Blur leggero - singolo passaggio Gaussian
            kernel_size = max(3, effective_intensity + 1)
            if kernel_size % 2 == 0:
                kernel_size += 1
            blurred_bg = cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)
            
        elif effective_intensity <= 25:
            # Blur medio - doppio passaggio ottimizzato
            kernel1 = max(5, int(effective_intensity * 0.6) + 1)
            if kernel1 % 2 == 0:
                kernel1 += 1
            
            # Primo passaggio con kernel più piccolo
            blurred_bg = cv2.GaussianBlur(frame, (kernel1, kernel1), 0)
            
            # Secondo passaggio con kernel leggermente più grande
            kernel2 = max(7, int(effective_intensity * 0.8) + 1)
            if kernel2 % 2 == 0:
                kernel2 += 1
            blurred_bg = cv2.GaussianBlur(blurred_bg, (kernel2, kernel2), 0)
            
        else:
            # Blur intenso - triplo passaggio con downsampling
            # Ridimensiona per performance
            h, w = frame.shape[:2]
            small_frame = cv2.resize(frame, (w//2, h//2))
            
            # Blur su immagine più piccola
            kernel = max(7, int(effective_intensity * 0.4) + 1)
            if kernel % 2 == 0:
                kernel += 1
            
            small_blurred = cv2.GaussianBlur(small_frame, (kernel, kernel), 0)
            small_blurred = cv2.GaussianBlur(small_blurred, (kernel, kernel), 0)
            
            # Ripristina dimensioni originali
            blurred_bg = cv2.resize(small_blurred, (w, h))
            
            # Passaggio finale per smoothing
            final_kernel = max(5, int(effective_intensity * 0.3) + 1)
            if final_kernel % 2 == 0:
                final_kernel += 1
            blurred_bg = cv2.GaussianBlur(blurred_bg, (final_kernel, final_kernel), 0)
        
                # Applica mask con blur soft per transizioni smooth
        mask_3ch = np.stack([mask] * 3, axis=-1)
        mask_blurred = cv2.GaussianBlur(mask_3ch, (5, 5), 1.5)
        
        # Componi risultato finale
        result = frame * mask_blurred + blurred_bg * (1 - mask_blurred)
        return result.astype(np.uint8)
    
    def _apply_quality_blur(self, frame: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """Blur di qualità massima (per confronto)"""
        # Implementazione blur di qualità (più lenta)
        kernel_size = max(3, self.blur_intensity * 2 + 1)
        if kernel_size % 2 == 0:
            kernel_size += 1
        
        blurred_bg = cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)
        
        if self.blur_intensity > 20:
            kernel_size_bokeh = min(kernel_size, 15)
            if kernel_size_bokeh % 2 == 0:
                kernel_size_bokeh += 1
            blurred_bg = cv2.medianBlur(blurred_bg, kernel_size_bokeh)
        
        # Mask a 3 canali con blur per transizioni smooth
        mask_3ch = np.stack([mask] * 3, axis=-1)
        mask_blurred = cv2.GaussianBlur(mask_3ch, (3, 3), 1)
        
        # Componi risultato finale
        result = frame * mask_blurred + blurred_bg * (1 - mask_blurred)
        return result.astype(np.uint8)
        
        # Mask a 3 canali con blur per transizioni smooth
        mask_3ch = np.stack([mask_normalized] * 3, axis=-1)
        mask_blurred = cv2.GaussianBlur(mask_3ch, (3, 3), 1)
        
        # Componi risultato finale
        result = frame * mask_blurred + blurred_bg * (1 - mask_blurred)
        return result.astype(np.uint8)
    
    def apply_noise_reduction(self, frame: np.ndarray) -> np.ndarray:
        """Applica riduzione rumore (opzionale)"""
        if not self.noise_reduction:
            return frame
            
        # Bilateral filter per riduzione rumore veloce
        return cv2.bilateralFilter(frame, 5, 50, 50)
    
    def set_blur_intensity(self, intensity: int):
        """Imposta intensità blur"""
        self.blur_intensity = max(1, min(25, intensity))
        self.config.set('effects.blur_intensity', intensity)
    
    def set_noise_reduction(self, enabled: bool):
        """Abilita/disabilita noise reduction"""
        self.noise_reduction = enabled
        self.config.set('effects.noise_reduction', enabled)
    
    def get_stats(self) -> dict:
        """Ottieni statistiche effetti"""
        return {
            'blur_intensity': self.blur_intensity,
            'noise_reduction': self.noise_reduction
        }
