# 🎥 StreamBlur Pro

<div align="center">
  <img src="public/tauri.svg" alt="StreamBlur Pro" width="120" height="120">
  <h3>Alternativa Professionale a NVIDIA Broadcast per GPU AMD</h3>
  <p>Virtual camera con AI background blur in tempo reale</p>

  <p>
    <img src="https://img.shields.io/badge/version-5.0.0-blue" alt="Version">
    <img src="https://img.shields.io/badge/platform-Windows-lightgrey" alt="Platform">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
    <img src="https://img.shields.io/badge/GPU-AMD%20Compatible-red" alt="GPU">
  </p>
</div>

---

## 🚀 Panoramica

**StreamBlur Pro** è un'applicazione desktop che porta le funzionalità professionali di NVIDIA Broadcast agli utenti con GPU AMD. Utilizzando l'intelligenza artificiale di MediaPipe, offre blur dello sfondo in tempo reale per videocall, streaming e registrazioni.

### ✨ Caratteristiche Principali

- **🎯 AI Background Blur**: Rimozione intelligente dello sfondo senza green screen  
- **🔧 AMD GPU Optimized**: Progettato specificamente per processori grafici AMD  
- **📹 Virtual Camera**: Integrazione diretta con Discord, OBS, Teams, Zoom  
- **⚡ Real-time Performance**: Monitoring CPU, memoria e FPS in tempo reale  
- **🎛️ Controlli Avanzati**: Intensità blur, qualità AI, smoothing temporale  
- **💾 Memory Smart**: Display dinamico memoria (MB/GB automatico)  

---

## 🎯 Perché StreamBlur Pro?

| NVIDIA Broadcast              | StreamBlur Pro               |
| ----------------------------- | ---------------------------- |
| ❌ Solo GPU NVIDIA            | ✅ **Supporto GPU AMD**      |
| ❌ Closed source              | ✅ **Open source**           |
| ❌ Limitato personalizzazione | ✅ **Controlli granulari**   |
| ❌ Performance opache         | ✅ **Monitoring trasparente**|

---

## 📦 Tecnologie

<div align="center">

| Frontend                                                                          | Backend                                                                 | AI Engine                                                                          | Desktop                                                                    |
| --------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| ![React](https://img.shields.io/badge/React-19.1.0-61DAFB?logo=react)             | ![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python) | ![MediaPipe](https://img.shields.io/badge/MediaPipe-AI-FF6B35)                     | ![Tauri](https://img.shields.io/badge/Tauri-1.5-24C8DB?logo=tauri)         |
| ![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript) | ![FastAPI](https://img.shields.io/badge/FastAPI-Bridge-009688)          | ![TensorFlow](https://img.shields.io/badge/TensorFlow-Lite-FF6F00?logo=tensorflow) | ![Rust](https://img.shields.io/badge/Rust-Native-000000?logo=rust)         |
| ![Tailwind](https://img.shields.io/badge/Tailwind-CSS-38B2AC?logo=tailwind-css)   | ![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8) |                                                                                    | ![Windows](https://img.shields.io/badge/Windows-10/11-0078D4?logo=windows) |

</div>

---

## 🛠️ Installazione

### 📋 Requisiti di Sistema

- **OS**: Windows 10/11 (64-bit)  
- **GPU**: AMD Radeon (qualsiasi generazione recente)  
- **RAM**: 4GB minimi, 8GB raccomandati  
- **Storage**: 2GB spazio libero  
- **Camera**: Webcam USB/integrata  

### 🚀 Installazione Rapida

1. **Scarica l'Installer**  
   📁 Vai a "Releases" → Scarica `StreamBlur-Pro-Setup.msi`  

2. **Installa l'App**  
   - Esegui il file `.msi` come amministratore  
   - Segui la procedura guidata  
   - L'app verrà installata in `Program Files`  

3. **Primo Avvio**  
   - Cerca "StreamBlur Pro" nel menu Start  
   - Autorizza l'accesso alla camera  
   - L'AI si inizializzerà automaticamente  

---

## 🎮 Come Usare

### 1. **Avvio Applicazione**
- Apri StreamBlur Pro dal menu Start
- L'interfaccia si caricherà con la preview camera

### 2. **Configurazione Virtual Camera**
- La virtual camera "OBS Virtual Camera" viene creata automaticamente
- Selezionala in Discord/Teams/Zoom come sorgente video

### 3. **Controlli Disponibili**

| Controllo              | Funzione                                 |
| ---------------------- | ---------------------------------------- |
| **Show/Hide Preview**  | Mostra/nascondi anteprima camera         |
| **Start/Stop**         | Avvia/ferma processamento AI             |
| **Blur Intensity**     | Regola intensità sfocatura (0-100)       |
| **AI Quality**         | Qualità elaborazione (Fast/Medium/High) |
| **Edge Smoothing**     | Bordi più fluidi                         |
| **Temporal Smoothing** | Riduce flickering tra frame              |

### 4. **Monitoring Performance**
- **FPS**: Frame al secondo elaborati  
- **CPU**: Utilizzo processore normalizzato  
- **Memory**: Uso RAM (smart MB/GB display)  
- **Status**: Stato generale sistema  

---

## 🏗️ Architettura

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

---

## 🤝 Contribuire

1. **Fork** il repository  
2. **Crea** branch feature (`git checkout -b feature/AmazingFeature`)  
3. **Commit** le modifiche (`git commit -m 'Add AmazingFeature'`)  
4. **Push** al branch (`git push origin feature/AmazingFeature`)  
5. **Apri** Pull Request  

### 🐛 Segnala Bug
- 📧 **Email**: christian@kodechris.dev  
- 💼 **LinkedIn**: [Christian Koscielniak Pinto](https://www.linkedin.com/in/christian-koscielniak-pinto)  

---

## 📜 Licenza
Distribuito sotto licenza MIT. Vedi `LICENSE` per maggiori informazioni.

---

<div align="center">
  <p>Sviluppato da <a href="https://kodechris.dev/">Christian @ KodeChris</a></p>
  <p>Fatto con ❤️ per la community AMD</p>
  <p>⭐ Se ti piace il progetto, lascia una stella!</p>
</div>

---

## 📞 Supporto
- 📧 **Email**: christian@kodechris.dev  
- 🌐 **Portfolio**: [kodechris.dev](https://kodechris.dev/)  
- 🐙 **GitHub Issues**: [Segnala problemi](https://github.com/ChrisKp1710/StreamBlur-Pro/issues)  
- 📖 **Wiki**: [Documentazione Completa](https://github.com/ChrisKp1710/StreamBlur-Pro/wiki)  
