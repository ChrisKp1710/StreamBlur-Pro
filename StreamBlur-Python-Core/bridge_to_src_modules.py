#!/usr/bin/env python3
"""
🚀 BRIDGE FINALE AI TUOI MODULI ORIGINALI 🚀
Questo bridge importa e usa DIRETTAMENTE i tuoi moduli dalla cartella src/
Non ricrea nulla - usa solo il TUO codice professionale esistente!
"""

import sys
import os
from pathlib import Path
import uvicorn
from fastapi import FastAPI, HTTPException
import logging

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🎯 AGGIUNGI LA TUA CARTELLA SRC AL PATH PYTHON
streamblur_python_core_path = Path(r"c:\Users\chris\Documents\StreamBlur-Pro\StreamBlur-Python-Core")
src_path = streamblur_python_core_path / "src"

if src_path.exists():
    sys.path.insert(0, str(src_path))
    logger.info(f"✅ Aggiunto path TUOI moduli: {src_path}")
else:
    logger.error(f"❌ Cartella src non trovata: {src_path}")
    sys.exit(1)

# App FastAPI
app = FastAPI(title="Bridge ai TUOI moduli originali")

# Variabili globali per i TUOI oggetti
camera_manager = None
ai_processor = None
effects_processor = None
virtual_camera_manager = None
config = None

def initialize_your_modules():
    """Inizializza i TUOI moduli originali dalla cartella src/"""
    global camera_manager, ai_processor, effects_processor, virtual_camera_manager, config
    
    try:
        logger.info("🔧 Importando i TUOI moduli originali...")
        
        # Importa la TUA configurazione
        from utils.config import StreamBlurConfig
        config = StreamBlurConfig()
        logger.info("✅ TUA configurazione caricata")
        
        # Importa e inizializza il TUO CameraManager
        from core.camera import CameraManager
        camera_manager = CameraManager(config)
        logger.info("✅ TUO CameraManager inizializzato")
        
        # Importa e inizializza il TUO AIProcessor
        from core.ai_processor import AIProcessor
        ai_processor = AIProcessor(config)
        logger.info("✅ TUO AIProcessor inizializzato")
        
        # Importa e inizializza il TUO EffectsProcessor
        from core.effects import EffectsProcessor
        effects_processor = EffectsProcessor(config)
        logger.info("✅ TUO EffectsProcessor inizializzato")
        
        # Importa e inizializza il TUO VirtualCameraManager
        from core.virtual_camera import VirtualCameraManager
        virtual_camera_manager = VirtualCameraManager(config)
        logger.info("✅ TUO VirtualCameraManager inizializzato")
        
        logger.info("🎉 TUTTI I TUOI MODULI ORIGINALI SONO STATI CARICATI!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Errore nell'inizializzazione dei TUOI moduli: {e}")
        import traceback
        traceback.print_exc()
        return False

@app.get("/health")
async def health_check():
    """Controllo di salute del bridge"""
    modules_status = {
        "camera_manager": camera_manager is not None,
        "ai_processor": ai_processor is not None,
        "effects_processor": effects_processor is not None,
        "virtual_camera_manager": virtual_camera_manager is not None,
        "config": config is not None
    }
    
    all_loaded = all(modules_status.values())
    
    return {
        "status": "healthy" if all_loaded else "unhealthy",
        "message": "Bridge ai TUOI moduli originali",
        "modules": modules_status,
        "using_your_src_folder": True
    }

@app.post("/start")
async def start_streamblur():
    """Avvia StreamBlur usando i TUOI moduli originali"""
    try:
        if not all([camera_manager, ai_processor, effects_processor, virtual_camera_manager]):
            raise HTTPException(status_code=500, detail="Moduli non inizializzati")
        
        # Usa i TUOI metodi originali
        success = camera_manager.start()
        if not success:
            raise HTTPException(status_code=500, detail="Errore avvio camera")
        
        virtual_camera_manager.start()
        
        logger.info("🚀 StreamBlur avviato usando i TUOI moduli originali!")
        return {"status": "started", "using_your_modules": True}
        
    except Exception as e:
        logger.error(f"❌ Errore avvio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stop")
async def stop_streamblur():
    """Ferma StreamBlur usando i TUOI metodi originali"""
    try:
        if camera_manager:
            camera_manager.stop()
        if virtual_camera_manager:
            virtual_camera_manager.stop()
        
        logger.info("⏹️ StreamBlur fermato usando i TUOI moduli originali")
        return {"status": "stopped"}
        
    except Exception as e:
        logger.error(f"❌ Errore stop: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/settings")
async def update_settings(settings: dict):
    """Aggiorna impostazioni usando la TUA configurazione"""
    try:
        if not config:
            raise HTTPException(status_code=500, detail="Configurazione non caricata")
        
        # Aggiorna usando i TUOI metodi di configurazione
        for key, value in settings.items():
            if hasattr(config, key):
                setattr(config, key, value)
                logger.info(f"✅ Aggiornato {key} = {value} nella TUA configurazione")
        
        return {"status": "updated", "settings": settings}
        
    except Exception as e:
        logger.error(f"❌ Errore aggiornamento impostazioni: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info("🚀 Avviando bridge ai TUOI moduli originali...")
    
    # Inizializza i TUOI moduli
    if initialize_your_modules():
        logger.info("✅ Bridge pronto - usando i TUOI moduli dalla cartella src/")
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        logger.error("❌ Impossibile avviare - problemi con i TUOI moduli")
        sys.exit(1)
