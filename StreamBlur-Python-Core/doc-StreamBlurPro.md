# StreamBlur Pro - Documentazione Completa

## Panoramica del Progetto

**StreamBlur Pro** è un software di virtual camera con AI per la rimozione automatica dello sfondo e applicazione di effetti blur in tempo reale. Progettato per sfruttare al massimo hardware AMD (RX 7900 XTX + Ryzen 9 5900X).

### Obiettivi Principali

* Segmentazione persona/sfondo in tempo reale usando AI
* Applicazione blur professionale allo sfondo
* Creazione virtual camera per OBS, Google Meet, Teams, etc.
* Interfaccia utente semplice e intuitiva
* Performance ottimizzate per hardware AMD

---

## Requisiti Sistema

### Hardware Minimo

* **GPU**: AMD RX 6000 series o superiore
* **CPU**: AMD Ryzen 5 o Intel i5 equivalente
* **RAM**: 8GB minimo, 16GB consigliati
* **Webcam**: Qualsiasi webcam USB o integrata

### Hardware Consigliato (Setup Target)

* **GPU**: AMD RX 7900 XTX (24GB VRAM)
* **CPU**: AMD Ryzen 9 5900X (12 core, 24 thread)
* **RAM**: 64GB DDR4
* **Webcam**: 1080p o superiore

---

## Stack Tecnologico

### Linguaggio Principale

* **Python 3.9+** - Linguaggio principale del progetto

### Librerie Core

```bash
# Computer Vision e AI
opencv-python==4.8.0
mediapipe==0.10.3
numpy==1.24.3

# Interfaccia e Utility
pillow==10.0.0
tkinter (incluso in Python)
pyvirtualcam==0.10.0

# Performance e GPU
pyopencl  # Per accelerazione AMD GPU (opzionale)
```

### Tools di Sviluppo

* **VS Code** / **PyCharm Community** - IDE
* **Git** - Version control
* **pip** - Package manager

---

## Architettura del Software

### Componenti Principali

#### 1. Video Capture Module

```python
# Responsabilità:
- Cattura video da webcam
- Gestione risoluzione e framerate
- Buffering frame
```

#### 2. AI Segmentation Engine

```python
# Responsabilità:
- Caricamento modelli MediaPipe
- Segmentazione persona/sfondo
- Ottimizzazione GPU AMD
```

#### 3. Effect Processing Module

```python
# Responsabilità:
- Applicazione blur allo sfondo
- Sostituzione sfondo (opzionale)
- Regolazione intensità effetti
```

#### 4. Virtual Camera Driver

```python
# Responsabilità:
- Creazione virtual camera device
- Stream output verso applicazioni esterne
- Compatibilità OBS/Meet/Teams
```

#### 5. User Interface

```python
# Responsabilità:
- GUI per controlli utente
- Anteprima video in tempo reale
- Salvataggio impostazioni
```

---

## Installazione e Setup

### Step 1: Installazione Python

```bash
# Download Python 3.9+ da python.org
# Durante installazione, selezionare "Add to PATH"
```

### Step 2: Verifica Installazione

```bash
python --version
pip --version
```

### Step 3: Installazione Dipendenze

```bash
# Creare virtual environment (consigliato)
python -m venv streamblur_env
streamblur_env\Scripts\activate  # Windows

# Installare librerie
pip install opencv-python
pip install mediapipe
pip install numpy
pip install pillow
pip install pyvirtualcam
```

### Step 4: Test Installazione

```python
# test_install.py
import cv2
import mediapipe as mp
import numpy as np
print("Tutte le librerie installate correttamente!")
```

---

## Struttura del Progetto

```
StreamBlurPro/
├── src/
│   ├── main.py              # Entry point applicazione
│   ├── video_capture.py     # Gestione webcam
│   ├── ai_segmentation.py   # AI per segmentazione
│   ├── effects.py           # Applicazione effetti
│   ├── virtual_camera.py    # Virtual camera driver
│   └── gui.py              # Interfaccia utente
├── models/                  # Modelli AI pre-addestrati
├── assets/                  # Risorse (icone, sfondi)
├── config/                  # File configurazione
├── docs/                    # Documentazione
└── requirements.txt         # Dipendenze Python
```

---

## Funzionalità Core

### 1. Real-time Background Segmentation

* **Tecnologia**: MediaPipe Selfie Segmentation
* **Performance**: 30+ FPS @ 1080p
* **Accuratezza**: >95% su buona illuminazione

### 2. Background Effects

* **Blur Gaussiano**: Intensità regolabile (1-50)
* **Blur Bokeh**: Effetto sfocatura professionale
* **Sostituzione Sfondo**: Immagini custom
* **Verde/Chroma Key**: Per streaming professionale

### 3. Virtual Camera Integration

* **Compatibilità**: OBS, Google Meet, Teams, Zoom, Discord
* **Risoluzione**: 480p, 720p, 1080p, 4K (se supportato)
* **Framerate**: 15, 24, 30, 60 FPS

### 4. Performance Optimization

* **GPU Acceleration**: Supporto OpenCL per AMD
* **Multi-threading**: Separazione capture/processing
* **Memory Management**: Ottimizzazione uso VRAM/RAM

---

## Roadmap Sviluppo

### Fase 1: MVP (2-3 settimane)

* [X]  Setup progetto e dipendenze
* [ ]  Video capture basico
* [ ]  Segmentazione AI semplice
* [ ]  Blur sfondo basico
* [ ]  Virtual camera output
* [ ]  GUI minimale

### Fase 2: Ottimizzazioni (2 settimane)

* [ ]  GPU acceleration AMD
* [ ]  Multi-threading
* [ ]  Ottimizzazione performance
* [ ]  Interfaccia migliorata

### Fase 3: Features Avanzate (3 settimane)

* [ ]  Sostituzione sfondi custom
* [ ]  Presets effetti
* [ ]  Salvataggio configurazioni
* [ ]  Edge detection migliorato

### Fase 4: Polish e Distribuzione (1 settimana)

* [ ]  Testing completo
* [ ]  Documentazione utente
* [ ]  Installer automatico
* [ ]  Logo e branding

---

## Note Tecniche

### Performance Target

* **Latenza**: <50ms end-to-end
* **CPU Usage**: <30% su Ryzen 9 5900X
* **GPU Usage**: <20% su RX 7900 XTX
* **RAM Usage**: <2GB per 1080p stream

### Ottimizzazioni AMD Specifiche

```python
# Esempio configurazione OpenCL per AMD
import pyopencl as cl
platforms = cl.get_platforms()
amd_platform = [p for p in platforms if 'AMD' in p.name][0]
context = cl.Context(dev_type=cl.device_type.GPU, 
                    properties=[(cl.context_properties.PLATFORM, amd_platform)])
```

### Gestione Errori

* **Camera non disponibile**: Fallback su camera integrata
* **GPU non supportata**: Fallback su CPU processing
* **Memoria insufficiente**: Riduzione automatica risoluzione

---

## Licenza e Distribuzione

### Licenza

* **Open Source**: MIT License (per uso personale)
* **Librerie**: Rispetto licenze MediaPipe (Apache 2.0), OpenCV (Apache 2.0)

### Distribuzione

* **GitHub**: Repository pubblico
* **Installer**: PyInstaller per eseguibile Windows
* **Portable**: Versione zip standalone

---

## Supporto e Community

### Documentazione

* **README**: Setup veloce
* **Wiki**: Guide approfondite
* **API Reference**: Documentazione codice

### Issues e Feature Request

* **GitHub Issues**: Bug reporting
* **Discussions**: Feature request e aiuto
* **Discord**: Community in tempo reale (opzionale)

---

## Changelog

### v0.1.0 (In sviluppo)

* Setup iniziale progetto
* Documentazione base
* Struttura moduli core

---

*Ultimo aggiornamento: Agosto 2025**Versione documento: 1.0*
