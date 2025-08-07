# =============================================================================
# File 12: src/gui/__init__.py
# =============================================================================

"""
StreamBlur Pro - GUI Modules
Contiene moduli per l'interfaccia grafica utente
"""

# Import compatibili sia per esecuzione diretta che come modulo
try:
    from .control_panel import StreamBlurControlPanel
except ImportError:
    from control_panel import StreamBlurControlPanel

__all__ = [
    'StreamBlurControlPanel'
]
