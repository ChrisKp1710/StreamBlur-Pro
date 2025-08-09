<h1 align="center">🎥 StreamBlur Pro</h1>

<div align="center">
  <img src="public/tauri.svg" alt="StreamBlur Pro logo" width="120" height="120" style="max-width:100%;height:auto;">
  <h3>Alternativa Professionale a NVIDIA Broadcast per GPU AMD</h3>
  <p>Virtual camera con AI background blur in tempo reale</p>
  <p>
    <img src="https://img.shields.io/badge/version-5.0.0-blue" alt="Version">
    <img src="https://img.shields.io/badge/platform-Windows-lightgrey" alt="Platform">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
    <img src="https://img.shields.io/badge/GPU-AMD%20Compatible-red" alt="GPU">
  </p>
</div>

<hr />

<h2 align="center">🚀 Panoramica</h2>

<div align="center" style="text-align:center">
  <p><strong>StreamBlur Pro</strong> è un'applicazione desktop che porta le funzionalità professionali di NVIDIA Broadcast agli utenti con GPU AMD. Utilizzando l'intelligenza artificiale di MediaPipe, offre blur dello sfondo in tempo reale per videocall, streaming e registrazioni.</p>
</div>

<h3 align="center">✨ Caratteristiche Principali</h3>

<div align="center" style="text-align:center">
  <ul style="list-style-position:inside; padding-left:0; margin:0 auto;">
    <li><strong>🎯 AI Background Blur</strong>: Rimozione intelligente dello sfondo senza green screen</li>
    <li><strong>🔧 AMD GPU Optimized</strong>: Progettato specificamente per processori grafici AMD</li>
    <li><strong>📹 Virtual Camera</strong>: Integrazione diretta con Discord, OBS, Teams, Zoom</li>
    <li><strong>⚡ Real-time Performance</strong>: Monitoring CPU, memoria e FPS in tempo reale</li>
    <li><strong>🎛️ Controlli Avanzati</strong>: Intensità blur, qualità AI, smoothing temporale</li>
    <li><strong>💾 Memory Smart</strong>: Display dinamico memoria (MB/GB automatico)</li>
  </ul>
</div>

<hr />

<h2 align="center">🎯 Perché StreamBlur Pro?</h2>

<div align="center">

| NVIDIA Broadcast              | StreamBlur Pro               |
| ----------------------------- | ---------------------------- |
| ❌ Solo GPU NVIDIA            | ✅ **Supporto GPU AMD**      |
| ❌ Closed source              | ✅ **Open source**           |
| ❌ Limitato personalizzazione | ✅ **Controlli granulari**   |
| ❌ Performance opache         | ✅ **Monitoring trasparente**|

</div>

<hr />

<h2 align="center">📦 Tecnologie</h2>

<div align="center">

| Frontend                                                                          | Backend                                                                 | AI Engine                                                                          | Desktop                                                                    |
| --------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| ![React](https://img.shields.io/badge/React-19.1.0-61DAFB?logo=react)             | ![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python) | ![MediaPipe](https://img.shields.io/badge/MediaPipe-AI-FF6B35)                     | ![Tauri](https://img.shields.io/badge/Tauri-1.5-24C8DB?logo=tauri)         |
| ![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript) | ![FastAPI](https://img.shields.io/badge/FastAPI-Bridge-009688)          | ![TensorFlow](https://img.shields.io/badge/TensorFlow-Lite-FF6F00?logo=tensorflow) | ![Rust](https://img.shields.io/badge/Rust-Native-000000?logo=rust)         |
| ![Tailwind](https://img.shields.io/badge/Tailwind-CSS-38B2AC?logo=tailwind-css)   | ![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8) |                                                                                    | ![Windows](https://img.shields.io/badge/Windows-10/11-0078D4?logo=windows) |

</div>

<hr />

<h2 align="center">🛠️ Installazione</h2>

<h3 align="center">📋 Requisiti di Sistema</h3>

<div align="center" style="text-align:center">
  <ul style="list-style-position:inside; padding-left:0; margin:0 auto;">
    <li><strong>OS</strong>: Windows 10/11 (64-bit)</li>
    <li><strong>GPU</strong>: AMD Radeon (qualsiasi generazione recente)</li>
    <li><strong>RAM</strong>: 4GB minimi, 8GB raccomandati</li>
    <li><strong>Storage</strong>: 2GB spazio libero</li>
    <li><strong>Camera</strong>: Webcam USB/integrata</li>
  </ul>
</div>

<h3 align="center">🚀 Installazione Rapida</h3>

<div align="center" style="text-align:center">
  <ol style="padding-left:0; list-style-position:inside; margin:0 auto;">
    <li><strong>Scarica l'Installer</strong><br/>📁 Vai a "Releases" → Scarica <code>StreamBlur-Pro-Setup.msi</code></li>
    <li><strong>Installa l'App</strong><br/>Esegui il file <code>.msi</code> come amministratore → segui la procedura guidata → l'app verrà installata in <code>Program Files</code></li>
    <li><strong>Primo Avvio</strong><br/>Cerca "StreamBlur Pro" nel menu Start → autorizza l'accesso alla camera → l'AI si inizializzerà automaticamente</li>
  </ol>
</div>

<hr />

<h2 align="center">🎮 Come Usare</h2>

<h3 align="center">1) Avvio Applicazione</h3>
<div align="center" style="text-align:center">
  <p>Apri StreamBlur Pro dal menu Start — l'interfaccia si caricherà con la preview camera.</p>
</div>

<h3 align="center">2) Configurazione Virtual Camera</h3>
<div align="center" style="text-align:center">
  <p>La virtual camera <strong>OBS Virtual Camera</strong> viene creata automaticamente.<br/>Selezionala in Discord/Teams/Zoom come sorgente video.</p>
</div>

<h3 align="center">3) Controlli Disponibili</h3>

<div align="center">

| Controllo              | Funzione                                 |
| ---------------------- | ---------------------------------------- |
| **Show/Hide Preview**  | Mostra/nascondi anteprima camera         |
| **Start/Stop**         | Avvia/ferma processamento AI             |
| **Blur Intensity**     | Regola intensità sfocatura (0–100)       |
| **AI Quality**         | Qualità elaborazione (Fast/Medium/High)  |
| **Edge Smoothing**     | Bordi più fluidi                         |
| **Temporal Smoothing** | Riduce flickering tra frame              |

</div>

<h3 align="center">4) Monitoring Performance</h3>
<div align="center" style="text-align:center">
  <ul style="list-style-position:inside; padding-left:0; margin:0 auto;">
    <li><strong>FPS</strong>: Frame al secondo elaborati</li>
    <li><strong>CPU</strong>: Utilizzo processore normalizzato</li>
    <li><strong>Memory</strong>: Uso RAM (smart MB/GB display)</li>
    <li><strong>Status</strong>: Stato generale sistema</li>
  </ul>
</div>

<hr />

<h2 align="center">🏗️ Architettura</h2>

<div align="center">

```
StreamBlur Pro
├── 🖥️ Desktop App (Tauri + React)
│   ├── Interfaccia utente moderna
│   ├── Controlli real-time
│   └── Performance monitoring
│
├── 🧠 AI Engine (Python + MediaPipe)
│   ├── Background segmentation
│   ├── Real-time processing
│   └── GPU acceleration
│
├── 📹 Virtual Camera (OpenCV)
│   ├── Video stream capture
│   ├── Frame processing pipeline
│   └── Output to virtual device
│
└── 🔗 Bridge Layer (FastAPI + Rust)
    ├── Settings synchronization
    ├── Performance metrics
    └── System integration
```
</div>

<hr />

<h2 align="center">🤝 Contribuire</h2>

<div align="center" style="text-align:center">
  <ol style="padding-left:0; list-style-position:inside; margin:0 auto;">
    <li><strong>Fork</strong> il repository</li>
    <li><strong>Crea</strong> branch feature (<code>git checkout -b feature/AmazingFeature</code>)</li>
    <li><strong>Commit</strong> le modifiche (<code>git commit -m 'Add AmazingFeature'</code>)</li>
    <li><strong>Push</strong> al branch (<code>git push origin feature/AmazingFeature</code>)</li>
    <li><strong>Apri</strong> Pull Request</li>
  </ol>
</div>

<h3 align="center">🐛 Segnala Bug</h3>

<div align="center" style="text-align:center">
  <p>📧 <strong>Email</strong>: <a href="mailto:christian@kodechris.dev">christian@kodechris.dev</a><br/>
  💼 <strong>LinkedIn</strong>: <a href="https://www.linkedin.com/in/christian-koscielniak-pinto/">Christian Koscielniak Pinto</a></p>
</div>

<hr />

<h2 align="center">📜 Licenza</h2>

<div align="center" style="text-align:center">
  <p>Distribuito sotto licenza MIT. Vedi <code>LICENSE</code> per maggiori informazioni.</p>
</div>

<hr />

<div align="center">
  <p>Sviluppato da <a href="https://kodechris.dev/">Christian @ KodeChris</a><br/>
  Fatto con ❤️ per la community AMD<br/>
  ⭐ Se ti piace il progetto, lascia una stella!</p>
</div>

<hr />

<h2 align="center">📞 Supporto</h2>

<div align="center" style="text-align:center">
  <p>
    📧 <strong>Email</strong>: <a href="mailto:christian@kodechris.dev">christian@kodechris.dev</a><br/>
    🌐 <strong>Portfolio</strong>: <a href="https://kodechris.dev/">kodechris.dev</a><br/>
    🐙 <strong>GitHub Issues</strong>: <a href="https://github.com/ChrisKp1710/StreamBlur-Pro/issues">Segnala problemi</a><br/>
    📖 <strong>Wiki</strong>: <a href="https://github.com/ChrisKp1710/StreamBlur-Pro/wiki">Documentazione Completa</a>
  </p>
</div>
