import { useState, useEffect } from "react";
import { invoke } from "@tauri-apps/api/tauri";
import { Header } from './components/Header';
import { CameraPreview } from './components/CameraPreview';
import { MainControl } from './components/MainControl';
import { Performance } from './components/Performance';
import { BlurControl } from './components/BlurControl';
import { AISettings } from './components/AISettings';

// Tipi per l'interfaccia con Tauri
interface StreamBlurStatus {
  running: boolean;
  fps: number;
  cpu_usage: number;
  memory_usage: number;
}

function App() {
  // States
  const [isActive, setIsActive] = useState(false);
  const [blurIntensity, setBlurIntensity] = useState(15);
  const [previewEnabled, setPreviewEnabled] = useState(false);
  const [fps, setFps] = useState(0);
  const [cpuUsage, setCpuUsage] = useState(0);
  const [memoryUsage, setMemoryUsage] = useState(0);
  
  // Settings
  const [edgeSmoothing, setEdgeSmoothing] = useState(true);
  const [temporalSmoothing, setTemporalSmoothing] = useState(true);
  const [performanceMode, setPerformanceMode] = useState(false);
  const [quality, setQuality] = useState('medium'); // NEW: AI quality control

  // Polling dello stato ogni secondo
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const status: StreamBlurStatus = await invoke("get_streamblur_status");
        setIsActive(status.running);
        setFps(status.fps);
        setCpuUsage(status.cpu_usage);
        setMemoryUsage(status.memory_usage);
      } catch (error) {
        console.error("Errore nel recuperare lo stato:", error);
      }
    }, 1000);
    
    return () => clearInterval(interval);
  }, []);

  // Gestione start/stop del motore
  const handleStart = async () => {
    try {
      if (isActive) {
        // Stop engine
        const message = await invoke("stop_streamblur_engine");
        console.log("✅", message);
      } else {
        // Start engine
        const message = await invoke("start_streamblur_engine");
        console.log("🚀", message);
      }
    } catch (error) {
      console.error("❌ Errore:", error);
      // Mostra notifica di errore all'utente se necessario
    }
  };

  // Aggiorna impostazioni blur
  const handleBlurChange = async (newIntensity: number) => {
    setBlurIntensity(newIntensity);
    
    try {
      await invoke("update_blur_settings", {
        intensity: newIntensity,
        enabled: newIntensity > 0
      });
    } catch (error) {
      console.error("❌ Errore aggiornamento blur:", error);
    }
  };

  // Aggiorna impostazioni AI
  const handleAISettingsChange = async () => {
    try {
      await invoke("update_ai_settings", {
        performanceMode,
        edgeSmoothing,
        temporalSmoothing,
        quality // NEW: Include quality in AI settings
      });
      console.log("🤖 Impostazioni AI aggiornate - Quality:", quality);
    } catch (error) {
      console.error("❌ Errore aggiornamento AI:", error);
    }
  };

  // Trigger aggiornamento AI quando cambiano le impostazioni
  useEffect(() => {
    if (isActive) {
      handleAISettingsChange();
    }
  }, [edgeSmoothing, temporalSmoothing, performanceMode, quality, isActive]); // NEW: Added quality to dependencies

  return (
    <div className="w-full h-full bg-white dark:bg-gray-900 flex flex-col overflow-hidden">
      <Header isActive={isActive} fps={fps} />

      {/* Main Content */}
      <div className="flex-1 p-4 grid grid-cols-3 gap-4 min-h-0">
        {/* Camera Preview - Ridotto ma mantenendo proporzioni */}
        <div className="col-span-2">
          <CameraPreview 
            previewEnabled={previewEnabled}
            setPreviewEnabled={setPreviewEnabled}
            isActive={isActive}
            blurIntensity={blurIntensity}
          />
        </div>

        {/* Control Panel - Più spazio per i controlli */}
        <div className="flex flex-col gap-3 h-full">
          <MainControl isActive={isActive} onToggle={handleStart} />
          <Performance fps={fps} cpuUsage={cpuUsage} memoryUsage={memoryUsage} />
          <BlurControl blurIntensity={blurIntensity} setBlurIntensity={handleBlurChange} />
          <AISettings 
            edgeSmoothing={edgeSmoothing}
            setEdgeSmoothing={setEdgeSmoothing}
            temporalSmoothing={temporalSmoothing}
            setTemporalSmoothing={setTemporalSmoothing}
            performanceMode={performanceMode}
            setPerformanceMode={setPerformanceMode}
            quality={quality}
            setQuality={setQuality}
          />
        </div>
      </div>
    </div>
  );
}

export default App;