# =============================================================================
# File 2: src/utils/config.py
# =============================================================================

import json
import os
from pathlib import Path
from typing import Dict, Any

class StreamBlurConfig:
    """Gestione configurazione StreamBlur Pro"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".streamblur_pro"
        self.config_file = self.config_dir / "config.json"
        
        # Crea directory se non esiste
        self.config_dir.mkdir(exist_ok=True)
        
        # Configurazione default
        self.default_config = {
            "video": {
                "camera_width": 1280,
                "camera_height": 720,
                "ai_width": 512,
                "ai_height": 288,
                "fps": 30
            },
            "effects": {
                "blur_intensity": 15,
                "edge_smoothing": True,
                "temporal_smoothing": True,
                "noise_reduction": False
            },
            "ai": {
                "performance_mode": False,  # False=accurato per scontorno preciso
                "fast_inference": True,
                "model_quality": "accurate"  # accurate/fast
            },
            "blur": {
                "algorithm": "optimized",  # optimized/quality
                "intensity_multiplier": 1.8,  # Per blur più intenso
                "use_gpu_acceleration": True
            },
            "performance": {
                "buffer_size": 2,
                "temporal_buffer_size": 2,
                "edge_kernel_size": 3
            },
            "gui": {
                "theme": "clam",
                "window_width": 520,
                "window_height": 450,
                "always_on_top": False
            },
            "virtual_camera": {
                "enabled": True,
                "format": "BGR"
            }
        }
        
        # Carica configurazione
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Carica configurazione da file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Merge con default per nuove opzioni
                    return self._merge_configs(self.default_config, config)
            except Exception as e:
                print(f"⚠️ Errore caricamento config: {e}")
                return self.default_config.copy()
        else:
            # Prima esecuzione, salva config default
            self._save_config(self.default_config)
            return self.default_config.copy()
    
    def _merge_configs(self, default: Dict, loaded: Dict) -> Dict:
        """Merge configurazioni mantenendo nuove opzioni"""
        result = default.copy()
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    def _save_config(self, config: Dict[str, Any]):
        """Salva configurazione su file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"⚠️ Errore salvataggio config: {e}")
    
    def get(self, key_path: str, default=None):
        """Ottieni valore configurazione (es: 'video.camera_width')"""
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any):
        """Imposta valore configurazione"""
        keys = key_path.split('.')
        config_ref = self.config
        
        # Naviga fino al parent
        for key in keys[:-1]:
            if key not in config_ref:
                config_ref[key] = {}
            config_ref = config_ref[key]
        
        # Imposta valore finale
        config_ref[keys[-1]] = value
        
        # Salva su file
        self._save_config(self.config)
    
    def reset_to_defaults(self):
        """Reset configurazione a default"""
        self.config = self.default_config.copy()
        self._save_config(self.config)