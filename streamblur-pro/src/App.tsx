import { useState, useEffect } from "react";
import { invoke } from "@tauri-apps/api/tauri";
import { Header } from './components/Header';
import { CameraPreview } from './components/CameraPreview';
import { MainControl } from './components/MainControl';
import { Performance } from './components/Performance';
import { BlurControl } from './components/BlurControl';
import { AISettings } from './components/AISettings';

function App() {
  // States
  const [isActive, setIsActive] = useState(false);
  const [blurIntensity, setBlurIntensity] = useState(15);
  const [previewEnabled, setPreviewEnabled] = useState(true);
  const [fps, setFps] = useState(26.2);
  
  // Settings
  const [edgeSmoothing, setEdgeSmoothing] = useState(true);
  const [temporalSmoothing, setTemporalSmoothing] = useState(true);
  const [performanceMode, setPerformanceMode] = useState(false);

  // Simulate performance metrics
  useEffect(() => {
    const interval = setInterval(() => {
      if (isActive) {
        setFps(Math.random() * 8 + 25); // 25-33 FPS
      }
    }, 1000);
    
    return () => clearInterval(interval);
  }, [isActive]);

  const handleStart = async () => {
    try {
      const message = await invoke("greet", { name: "StreamBlur Pro" });
      console.log(message);
      setIsActive(!isActive);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="w-full h-full bg-white dark:bg-gray-900 flex flex-col overflow-hidden">
      <Header isActive={isActive} fps={fps} />

      {/* Main Content */}
      <div className="flex-1 p-5 grid grid-cols-3 gap-5 min-h-0">
        <CameraPreview 
          previewEnabled={previewEnabled}
          setPreviewEnabled={setPreviewEnabled}
          isActive={isActive}
          blurIntensity={blurIntensity}
        />

        {/* Control Panel */}
        <div className="flex flex-col h-full">
          <MainControl isActive={isActive} onToggle={handleStart} />
          <Performance fps={fps} />
          <BlurControl blurIntensity={blurIntensity} setBlurIntensity={setBlurIntensity} />
          <AISettings 
            edgeSmoothing={edgeSmoothing}
            setEdgeSmoothing={setEdgeSmoothing}
            temporalSmoothing={temporalSmoothing}
            setTemporalSmoothing={setTemporalSmoothing}
            performanceMode={performanceMode}
            setPerformanceMode={setPerformanceMode}
          />
        </div>
      </div>
    </div>
  );
}

export default App;