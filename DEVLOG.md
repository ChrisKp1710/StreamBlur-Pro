# StreamBlur Pro — Development Log

**Alternativa open-source ad NVIDIA Broadcast per AMD RX 7900 XTX + Ryzen 9 5900X**

---

## Stato attuale: FUNZIONANTE ✅

Data ultimo aggiornamento: 2026-04-29

### Cosa funziona oggi

| Feature | Stato |
|---------|-------|
| Avvio app Tauri | ✅ Funzionante |
| Camera capture (webcam) | ✅ Funzionante |
| AI segmentazione persona (MediaPipe) | ✅ Funzionante |
| Blur sfondo | ✅ Funzionante |
| OBS Virtual Camera output | ✅ Funzionante |
| Preview live nell'app | ✅ Funzionante (polling JPEG ~10 FPS) |
| Controllo blur intensity (slider 1-25) | ✅ Funzionante |
| Edge Smoothing | ✅ Funzionante |
| Temporal Smoothing | ✅ Funzionante |
| Performance monitor (FPS, CPU, RAM) | ✅ Funzionante |
| AI Quality selector (Low/Medium/High) | ✅ Funzionante |
| Start/Stop engine | ✅ Funzionante |

---

## Architettura del progetto

```
StreamBlur-Pro/
├── StreamBlur-Python-Core/        ← Backend Python
│   ├── final_bridge_to_your_modules.py   ← Entry point: FastAPI server porta 8000
│   ├── requirements.txt
│   ├── streamblur_env/            ← Virtual environment Python (NON in git)
│   └── src/
│       ├── core/
│       │   ├── camera.py          ← Cattura webcam con threading
│       │   ├── ai_processor.py    ← MediaPipe selfie segmentation
│       │   ├── effects.py         ← Gaussian blur algoritmo a cascata
│       │   └── virtual_camera.py  ← Output su OBS Virtual Camera
│       └── utils/
│           ├── config.py          ← Configurazione (salva in ~/.streamblur_pro/)
│           └── performance.py     ← Monitoraggio FPS/CPU/RAM
│
└── streamblur-pro/                ← Frontend Tauri
    ├── src-tauri/src/main.rs      ← Rust: lancia Python, espone comandi Tauri
    └── src/
        ├── App.tsx                ← Root React: polling stato ogni 1s
        └── components/
            ├── Header.tsx         ← Status indicator + FPS
            ├── CameraPreview.tsx  ← Preview live via polling /preview/frame
            ├── MainControl.tsx    ← Pulsante Start/Stop
            ├── Performance.tsx    ← Card FPS/CPU/Memory
            ├── BlurControl.tsx    ← Slider blur 1-25
            └── AISettings.tsx     ← Toggle edge/temporal + quality selector
```

### Flusso dati

```
Webcam → CameraManager → AIProcessor (MediaPipe) → EffectsProcessor (Gaussian blur)
                                                           ↓
                                              VirtualCameraManager → OBS Virtual Camera
                                                           ↓
                                              last_preview_frame → /preview/frame (JPEG)
                                                           ↓
                                              React polling ogni 100ms → CameraPreview UI
```

### Comunicazione Tauri ↔ Python

```
Tauri UI (React) → invoke() → Rust (main.rs) → HTTP → FastAPI (porta 8000)

Endpoint Python:
  GET  /health          → verifica moduli caricati
  GET  /status          → FPS, CPU, RAM, running state
  POST /start           → avvia camera + AI + virtual cam + loop
  POST /stop            → ferma tutto e resetta per restart
  POST /settings        → aggiorna blur intensity, AI quality, smoothing
  GET  /preview/frame   → singolo frame JPEG blurrato (per preview UI)
```

---

## Setup iniziale (clone fresco)

### 1. Prerequisiti
- Python 3.11
- Node.js + npm
- Rust + Cargo
- OBS Studio con Virtual Camera plugin installato
- **Smart App Control DISABILITATO** (Impostazioni → Privacy e sicurezza → Sicurezza di Windows → Controllo app e browser → Off)

### 2. Backend Python
```bash
cd StreamBlur-Python-Core
python -m venv streamblur_env
streamblur_env\Scripts\pip install -r requirements.txt
```

### 3. Frontend Tauri
```bash
cd streamblur-pro
npm install
```

### 4. Avvio sviluppo
```bash
cd streamblur-pro
npm run tauri dev
```
L'app lancia automaticamente il backend Python. Se il bridge non parte, avviarlo manualmente:
```bash
cd StreamBlur-Python-Core
streamblur_env\Scripts\python.exe final_bridge_to_your_modules.py
```

---

## Problemi noti e risolti

### ✅ Path hardcoded in main.rs
- **Problema:** path puntava a `Documents\StreamBlur-Pro\` (vecchia posizione)
- **Fix:** aggiornato a `Documents\code\StreamBlur-Pro\` in `main.rs`

### ✅ MediaPipe 0.10.35 incompatibile
- **Problema:** MediaPipe 0.10.35+ ha rimosso `mp.solutions.selfie_segmentation`
- **Fix:** downgrade a `mediapipe==0.10.14` (ultima versione con solutions)

### ✅ Encoding emoji su Windows
- **Problema:** `print()` con emoji crashava il bridge su Windows (charmap codec)
- **Fix:** aggiunto fix UTF-8 in `final_bridge_to_your_modules.py` + env vars in Rust

### ✅ Smart App Control blocca i binari compilati
- **Problema:** Windows 11 Smart App Control bloccava gli eseguibili Rust compilati
- **Fix:** disabilitare Smart App Control nelle impostazioni Windows (one-time)
- **Nota per distribuzione:** firmare il binario con certificato code signing EV/OV

### ✅ Preview camera finta
- **Problema:** CameraPreview mostrava solo un placeholder grafico
- **Fix:** aggiunto endpoint `/preview/frame` nel bridge + polling React ogni 100ms

### ✅ CORS blocca fetch dal WebView
- **Problema:** WebView2 (Tauri) non riusciva a fare fetch su `127.0.0.1:8000`
- **Fix:** aggiunto `CORSMiddleware` con `allow_origins=["*"]` in FastAPI

### ✅ Porta 8000 già occupata (Start multipli)
- **Problema:** premere Start più volte lancia più processi Python in conflitto
- **Stato:** il secondo processo fallisce silenziosamente, il primo resta attivo
- **TODO:** aggiungere controllo "engine già attivo" nella UI prima di ri-lanciare

---

## Sessione 2026-04-29 — Audit completo e ottimizzazioni

### Bug critici corretti

#### ✅ Quality selector (Low/Medium/High) ignorato da Tauri
- **Problema:** Il parametro `quality` mandato dalla UI via `invoke()` veniva scartato da Tauri perché il comando Rust `update_ai_settings` non lo dichiarava come parametro. Il Python riceveva sempre `quality="high"` o `"medium"` hardcoded in Rust.
- **Fix:** Aggiunto `quality: String` alla firma del comando Rust; il valore reale della UI ora arriva correttamente a Python.
- **File:** `streamblur-pro/src-tauri/src/main.rs`

#### ✅ Logica Quality invertita in Rust
- **Problema:** `performance_mode=true` mandava `quality="high"` (modalità accurata) invece di `"low"` (veloce) — esatto contrario di quello che l'utente si aspettava.
- **Fix:** Il payload Rust ora forwarda direttamente il `quality` dalla UI senza logica hardcoded.
- **File:** `streamblur-pro/src-tauri/src/main.rs`

#### ✅ NameError su memory_usage_mb in /status
- **Problema:** Se `psutil` falliva per qualsiasi motivo, `memory_usage_mb` non veniva mai definita ma era referenziata nella response → crash silenzioso dell'endpoint `/status`.
- **Fix:** Inizializzata `memory_usage_mb = 0.0` accanto a `memory_usage_gb = 0.0` prima del blocco try/except.
- **File:** `StreamBlur-Python-Core/final_bridge_to_your_modules.py`

#### ✅ Dead code irraggiungibile in effects.py
- **Problema:** Nella funzione `_apply_quality_blur`, dopo il `return result.astype(np.uint8)` c'erano 7 righe di codice morto che referenziavano `mask_normalized` (variabile inesistente in quello scope) — copia/incolla dimenticata.
- **Fix:** Rimosso il blocco dead code; fixata anche l'indentazione anomala del commento a riga 96.
- **File:** `StreamBlur-Python-Core/src/core/effects.py`

### Ottimizzazioni performance

#### ✅ Main loop capped a 30 FPS
- **Problema:** Il loop principale girava alla massima velocità possibile, bruciando CPU senza motivo quando l'AI era più veloce del necessario.
- **Fix:** Aggiunto `target_interval = 1/30` con sleep sul tempo rimanente di ogni iterazione. Se un frame impiega 20ms, il loop aspetta i 13ms rimanenti per restare a 30fps.
- **File:** `StreamBlur-Python-Core/final_bridge_to_your_modules.py`

#### ✅ Preview JPEG downscalato a 640×360
- **Problema:** L'endpoint `/preview/frame` codificava il frame a piena risoluzione 1280×720 come JPEG per ogni polling del frontend — 4× i byte necessari.
- **Fix:** Prima della codifica JPEG, il frame viene ridimensionato a metà (640×360). Il preview nell'app non mostra differenza visiva ma il transfer è 4× più leggero.
- **File:** `StreamBlur-Python-Core/final_bridge_to_your_modules.py`

#### ✅ Risoluzione AI adattiva per quality level (nuovo metodo update_quality)
- **Problema:** Anche in modalità Low (performance), l'AI girava sempre a 512×288 — stessa risoluzione di High. I tre livelli di quality non avevano alcun effetto sulla risoluzione.
- **Fix:** Aggiunto metodo `AIProcessor.update_quality(quality: str)` che imposta risoluzione E modello in base al livello:
  - `"low"`    → 256×144 + modello 0 (veloce)
  - `"medium"` → 384×216 + modello 0 (bilanciato)
  - `"high"`   → 512×288 + modello 1 (accurato)
- **File:** `StreamBlur-Python-Core/src/core/ai_processor.py`

#### ✅ edgeSmoothing e temporalSmoothing come booleani separati
- **Problema:** Il payload Rust mandava a Python `smoothing: 0.8/0.3` (un numero) che Python convertiva in solo temporal smoothing tramite threshold. L'edge smoothing veniva perso completamente.
- **Fix:** Il payload ora manda `edgeSmoothing: bool` e `temporalSmoothing: bool` separati, che Python gestisce già correttamente nei due handler distinti.
- **File:** `streamblur-pro/src-tauri/src/main.rs`

---

## Roadmap / TODO

### Alta priorità
- [ ] **Code signing** del binario Tauri per distribuzione (evita Smart App Control per gli utenti)
- [ ] **Gestione errore "Start multiplo"** — mostrare feedback se engine già attivo
- [ ] **Installer** — `npm run tauri build` per creare .exe/.msi distribuibile

### Media priorità
- [ ] **Feedback visivo** durante inizializzazione AI (loading spinner)
- [ ] **Selezione webcam** — dropdown per scegliere tra più webcam
- [ ] **Sfondi virtuali** — supporto immagini di sfondo oltre al blur

### Bassa priorità
- [ ] **GPU acceleration** — utilizzare PyOpenCL per processing su AMD RX 7900 XTX
- [ ] **Noise reduction audio** — integrazione con filtri audio
- [ ] **Auto-aggiornamento** — Tauri updater

---

## Dipendenze principali

### Python
| Pacchetto | Versione | Motivo |
|-----------|----------|--------|
| mediapipe | ==0.10.14 | Segmentazione AI (versioni >0.10.14 rompono l'API) |
| opencv-python | >=4.8.0 | Cattura webcam e processing immagini |
| pyvirtualcam | >=0.10.0 | Output su OBS Virtual Camera |
| fastapi + uvicorn | >=0.100.0 | Server HTTP per comunicazione con Tauri |
| psutil | >=5.9.0 | Metriche CPU/RAM |

### Rust/Tauri
| Crate | Versione |
|-------|----------|
| tauri | 1.5 |
| reqwest | 0.11 |
| tokio | 1.0 |

### Frontend
| Pacchetto | Versione |
|-----------|----------|
| @tauri-apps/api | ^1.5.0 |
| react | ^19.1.0 |
| tailwindcss | ^3.3.0 |
| lucide-react | ^0.537.0 |
