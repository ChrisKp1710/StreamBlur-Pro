<div align="center">

<img src="streamblur-pro/public/tauri.svg" alt="StreamBlur Pro" width="96" height="96">

# StreamBlur Pro

**AI background blur for AMD GPUs — the open-source NVIDIA Broadcast alternative**

[![Version](https://img.shields.io/badge/version-1.0.0-6366f1?style=flat-square)](https://github.com/ChrisKp1710/StreamBlur-Pro/releases)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-0078D4?style=flat-square&logo=windows&logoColor=white)](https://github.com/ChrisKp1710/StreamBlur-Pro)
[![License](https://img.shields.io/badge/license-MIT-22c55e?style=flat-square)](LICENSE)
[![AMD](https://img.shields.io/badge/GPU-AMD%20Optimized-ED1C24?style=flat-square&logo=amd&logoColor=white)](https://github.com/ChrisKp1710/StreamBlur-Pro)
[![Built with Tauri](https://img.shields.io/badge/built%20with-Tauri-24C8DB?style=flat-square&logo=tauri&logoColor=white)](https://tauri.app)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)

</div>

---

<div align="center">
  <img src="assets/preview.png" alt="StreamBlur Pro — App Screenshot" width="720" style="border-radius:12px; box-shadow:0 8px 32px rgba(0,0,0,0.3);">
  <br/>
  <sub><i>StreamBlur Pro in action — real-time AI background blur on AMD hardware</i></sub>
</div>

---

## What is StreamBlur Pro?

StreamBlur Pro brings professional-grade AI background blur to AMD GPU users — no green screen, no NVIDIA required. It hooks directly into your webcam, runs MediaPipe AI segmentation, and outputs a blurred background stream through OBS Virtual Camera, making it instantly available in **Discord, Teams, Zoom, and OBS**.

> Built on AMD Ryzen 9 5900X + RX 7900 XTX. Runs great on any modern AMD system.

---

## Features

| | Feature | Description |
|---|---|---|
| 🤖 | **AI Segmentation** | MediaPipe-powered person detection — no green screen needed |
| 🎥 | **Virtual Camera Output** | Works natively with Discord, Teams, Zoom, OBS, and any app that supports webcam input |
| 🎛️ | **Adjustable Blur** | Intensity slider from subtle to cinematic (1–25 levels with cascade algorithm) |
| ⚡ | **Three Quality Modes** | Low (256×144, 30fps+), Medium (384×216), High (512×288 accurate model) |
| 🧊 | **Edge Smoothing** | Morphological + Gaussian mask refinement for clean person outlines |
| 🎞️ | **Temporal Smoothing** | Frame-averaged mask to eliminate flickering between frames |
| 📊 | **Performance Monitor** | Real-time FPS, CPU %, and RAM display inside the app |
| 🔄 | **Hot Reload Settings** | Change blur intensity and AI quality live — no restart needed |

---

## StreamBlur Pro vs NVIDIA Broadcast

| | NVIDIA Broadcast | StreamBlur Pro |
|---|---|---|
| **GPU Support** | NVIDIA only | ✅ AMD (any modern GPU) |
| **Source Code** | Closed source | ✅ Fully open source |
| **AI Quality Control** | Fixed | ✅ Low / Medium / High |
| **Performance Visibility** | None | ✅ FPS + CPU + RAM monitor |
| **Virtual Camera** | Proprietary | ✅ OBS Virtual Camera |
| **Customization** | Limited | ✅ Full control |
| **Cost** | Free (NVIDIA required) | ✅ Free, no hardware lock |

---

## Tech Stack

<div align="center">

| Layer | Technology |
|---|---|
| **Desktop Shell** | [Tauri 1.5](https://tauri.app) (Rust) + WebView2 |
| **Frontend** | React 19 + TypeScript + Tailwind CSS |
| **AI Backend** | Python 3.11 + MediaPipe 0.10.14 |
| **HTTP Bridge** | FastAPI + Uvicorn (port 8000) |
| **Video Processing** | OpenCV 4.8+ |
| **Virtual Camera** | pyvirtualcam + OBS Virtual Camera |
| **System Metrics** | psutil |

</div>

---

## Quick Start

### Prerequisites

- Windows 10 / 11 (64-bit)
- [Python 3.11](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org)
- [Rust + Cargo](https://rustup.rs)
- [OBS Studio](https://obsproject.com) with Virtual Camera enabled
- **Smart App Control disabled** — Windows Security → App & browser control → Off *(required for unsigned dev builds)*

### 1 — Clone & install

```bash
git clone https://github.com/ChrisKp1710/StreamBlur-Pro.git
cd StreamBlur-Pro
```

**Python backend:**
```bash
cd StreamBlur-Python-Core
python -m venv streamblur_env
streamblur_env\Scripts\pip install -r requirements.txt
```

**Frontend:**
```bash
cd ../streamblur-pro
npm install
```

### 2 — Run in development

```bash
cd streamblur-pro
npm run tauri dev
```

The Tauri app automatically launches the Python bridge on startup. If it doesn't, start it manually:

```bash
cd StreamBlur-Python-Core
streamblur_env\Scripts\python.exe final_bridge_to_your_modules.py
```

### 3 — Use it

1. Click **Start** in the app
2. Open Discord / Teams / Zoom
3. Select **"OBS Virtual Camera"** as your video source
4. Done — your background is blurred in real time

---

## How It Works

```
Webcam
  │
  ▼
CameraManager          ← Threaded capture at 1280×720, buffer size 2
  │
  ▼
AIProcessor            ← MediaPipe SelfieSegmentation (model 0 or 1)
  │                       Resize frame to AI resolution (256–512px wide)
  │                       → Edge smoothing (morphology + Gaussian)
  │                       → Temporal smoothing (3-frame weighted average)
  ▼
EffectsProcessor       ← Cascade Gaussian blur on background only
  │                       Light (1 pass) / Medium (2 pass) / Heavy (downsample + 3 pass)
  ▼
VirtualCameraManager   ← pyvirtualcam → OBS Virtual Camera → Discord/Teams/Zoom
  │
  ▼
preview_frame (JPEG)   ← 640×360 downscaled, polled every 100ms by the React UI
```

**Communication flow:**

```
React UI → invoke() → Rust (Tauri) → HTTP POST → FastAPI (Python :8000)

Endpoints:
  GET  /health          check all modules loaded
  GET  /status          fps, cpu, ram, running state
  POST /start           init camera + AI + virtual cam + start loop
  POST /stop            stop loop + full cleanup (restart-safe)
  POST /settings        live-update blur, quality, edge/temporal smoothing
  GET  /preview/frame   single JPEG frame for UI preview polling
```

---

## Project Structure

```
StreamBlur-Pro/
├── StreamBlur-Python-Core/
│   ├── final_bridge_to_your_modules.py   ← FastAPI server + main processing loop
│   ├── requirements.txt
│   └── src/
│       ├── core/
│       │   ├── camera.py          webcam capture (threaded, queue-based)
│       │   ├── ai_processor.py    MediaPipe segmentation + smoothing
│       │   ├── effects.py         cascade Gaussian blur
│       │   └── virtual_camera.py  OBS Virtual Camera output
│       └── utils/
│           ├── config.py          JSON config (~/.streamblur_pro/)
│           └── performance.py     FPS / CPU / RAM metrics
│
└── streamblur-pro/
    ├── src-tauri/src/main.rs      Rust: spawn Python, expose Tauri commands
    └── src/
        ├── App.tsx                root — status polling every 1s
        └── components/
            ├── Header.tsx         status badge + FPS
            ├── CameraPreview.tsx  live preview via JPEG polling
            ├── MainControl.tsx    Start / Stop button
            ├── Performance.tsx    FPS / CPU / Memory cards
            ├── BlurControl.tsx    intensity slider
            └── AISettings.tsx     quality selector + toggles
```

---

## Contributing

Contributions are welcome. Here's how:

1. Fork the repository
2. Create your branch: `git checkout -b feature/my-feature`
3. Commit with a clear message: `git commit -m "Add my feature"`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

**Open issues / roadmap:**

- [ ] Code signing for distribution (eliminates Smart App Control prompt)
- [ ] Installer (`.msi`) via `npm run tauri build`
- [ ] Guard against multiple Start clicks (port 8000 conflict)
- [ ] Webcam selector dropdown
- [ ] Virtual background images (beyond blur)
- [ ] GPU acceleration via PyOpenCL (AMD RX series)

Report bugs on [GitHub Issues](https://github.com/ChrisKp1710/StreamBlur-Pro/issues).

---

## License

Distributed under the **MIT License** — see [`LICENSE`](LICENSE) for details.

---

<div align="center">

Made with ❤️ by [Christian @ KodeChris](https://kodechris.dev) for the AMD community

[![GitHub stars](https://img.shields.io/github/stars/ChrisKp1710/StreamBlur-Pro?style=social)](https://github.com/ChrisKp1710/StreamBlur-Pro)
&nbsp;
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Christian%20Koscielniak%20Pinto-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/christian-koscielniak-pinto/)
&nbsp;
[![Portfolio](https://img.shields.io/badge/Portfolio-kodechris.dev-6366f1?style=flat-square)](https://kodechris.dev)

</div>
