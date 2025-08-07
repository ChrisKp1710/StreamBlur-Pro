# =============================================================================
# File 10: src/core/__init__.py
# =============================================================================

"""
StreamBlur Pro - Core Modules
Contiene i moduli principali per l'elaborazione video
"""

# Import compatibili sia per esecuzione diretta che come modulo
try:
    from .camera import CameraManager
    from .ai_processor import AIProcessor
    from .effects import EffectsProcessor
    from .virtual_camera import VirtualCameraManager
except ImportError:
    from camera import CameraManager
    from ai_processor import AIProcessor
    from effects import EffectsProcessor
    from virtual_camera import VirtualCameraManager

__all__ = [
    'CameraManager',
    'AIProcessor', 
    'EffectsProcessor',
    'VirtualCameraManager'
]