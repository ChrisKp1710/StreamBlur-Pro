import { useState, useEffect } from "react";
import { invoke } from "@tauri-apps/api/tauri";
import { 
  Play, 
  Square, 
  Eye, 
  EyeOff,
  Monitor,
  Activity,
  Camera,
  Settings,
  Zap
} from 'lucide-react';

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
      {/* Header - Compatto */}
      <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-5 py-3 flex-shrink-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
              <Camera className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-gray-900 dark:text-white">StreamBlur Pro</h1>
              <p className="text-xs text-gray-500 dark:text-gray-400">AI Background Blur</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <div className={`flex items-center space-x-2 px-3 py-1 rounded-full text-sm ${
              isActive 
                ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400' 
                : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400'
            }`}>
              <div className={`w-2 h-2 rounded-full ${isActive ? 'bg-green-500 animate-pulse' : 'bg-gray-400'}`}></div>
              <span className="font-medium">{isActive ? 'Active' : 'Ready'}</span>
            </div>
            
            {isActive && (
              <div className="text-sm font-mono text-gray-600 dark:text-gray-400 bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded">
                {fps.toFixed(0)} FPS
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content - Layout Fisso */}
      <div className="flex-1 p-5 grid grid-cols-3 gap-5 min-h-0">
        
        {/* Camera Preview - 2 colonne */}
        <div className="col-span-2 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 flex flex-col">
          <div className="p-3 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
            <h2 className="text-sm font-semibold text-gray-900 dark:text-white flex items-center">
              <Monitor className="w-4 h-4 mr-2 text-gray-500" />
              Camera Preview
            </h2>
            <button
              onClick={() => setPreviewEnabled(!previewEnabled)}
              className={`flex items-center px-2 py-1 rounded text-xs font-medium transition-colors ${
                previewEnabled
                  ? 'bg-blue-500 text-white hover:bg-blue-600'
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300'
              }`}
            >
              {previewEnabled ? <Eye className="w-3 h-3 mr-1" /> : <EyeOff className="w-3 h-3 mr-1" />}
              {previewEnabled ? 'Hide' : 'Show'}
            </button>
          </div>
          
          <div className="flex-1 relative">
            {previewEnabled ? (
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center">
                  <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center mx-auto mb-3">
                    <Camera className="w-8 h-8 text-blue-600 dark:text-blue-400" />
                  </div>
                  <h3 className="text-base font-medium text-gray-900 dark:text-white mb-2">Live Camera Feed</h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400 mb-3">
                    Blur: {blurIntensity}%
                  </p>
                  
                  {isActive && (
                    <div className="inline-flex items-center px-2 py-1 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 rounded-full text-xs font-medium">
                      <div className="w-1.5 h-1.5 bg-red-500 rounded-full animate-pulse mr-1.5"></div>
                      LIVE
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-blue-900/20 dark:to-indigo-900/30">
                <div className="text-center">
                  <div className="w-16 h-16 bg-blue-100 dark:bg-blue-800/50 rounded-full flex items-center justify-center mx-auto mb-3">
                    <EyeOff className="w-8 h-8 text-blue-500 dark:text-blue-400" />
                  </div>
                  <p className="text-sm font-medium text-blue-700 dark:text-blue-300">Preview Disabled</p>
                  <p className="text-xs text-blue-500 dark:text-blue-400 mt-1">Click "Show" to enable camera preview</p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Control Panel - 1 colonna */}
        <div className="flex flex-col h-full">
          
          {/* Main Control */}
          <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 mb-4">
            <button
              onClick={handleStart}
              className={`w-full py-3 px-4 rounded-lg font-semibold transition-all ${
                isActive 
                  ? 'bg-red-500 hover:bg-red-600 text-white' 
                  : 'bg-blue-500 hover:bg-blue-600 text-white'
              }`}
            >
              {isActive ? (
                <>
                  <Square className="inline w-4 h-4 mr-2" />
                  Stop
                </>
              ) : (
                <>
                  <Play className="inline w-4 h-4 mr-2" />
                  Start
                </>
              )}
            </button>
            
            <div className={`mt-3 p-2 rounded text-xs text-center ${
              isActive 
                ? "bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400"
                : "bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400"
            }`}>
              {isActive ? "✓ Virtual Camera Active" : "Select 'OBS Virtual Camera' in apps"}
            </div>
          </div>

          {/* Performance */}
          <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 mb-4">
            <div className="flex items-center mb-3">
              <Activity className="w-4 h-4 text-blue-500 mr-2" />
              <h3 className="text-sm font-semibold text-gray-900 dark:text-white">Performance</h3>
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-xs text-gray-600 dark:text-gray-400">FPS</span>
                <span className="text-sm font-mono font-bold text-blue-600 dark:text-blue-400">
                  {fps.toFixed(0)}
                </span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-xs text-gray-600 dark:text-gray-400">Status</span>
                <span className={`text-xs font-medium ${
                  fps >= 25 ? 'text-green-600 dark:text-green-400' : 
                  fps >= 20 ? 'text-yellow-600 dark:text-yellow-400' : 
                  'text-orange-600 dark:text-orange-400'
                }`}>
                  {fps >= 25 ? 'Excellent' : fps >= 20 ? 'Good' : 'Fair'}
                </span>
              </div>
            </div>
          </div>

          {/* Blur Control */}
          <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 mb-4">
            <div className="flex items-center mb-3">
              <Zap className="w-4 h-4 text-yellow-500 mr-2" />
              <h3 className="text-sm font-semibold text-gray-900 dark:text-white">Blur Intensity</h3>
            </div>
            
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-xs text-gray-600 dark:text-gray-400">Current</span>
                <span className="text-xs font-mono text-blue-600 dark:text-blue-400">{blurIntensity}</span>
              </div>
              
              <input
                type="range"
                min="1"
                max="25"
                value={blurIntensity}
                onChange={(e) => setBlurIntensity(parseInt(e.target.value))}
                className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer"
              />
              
              <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
                <span>Low</span>
                <span>High</span>
              </div>
            </div>
          </div>

          {/* AI Settings - Allineato con la base della camera */}
          <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 flex-1 flex flex-col justify-end">
            <div>
              <div className="flex items-center mb-3">
                <Settings className="w-4 h-4 text-gray-500 mr-2" />
                <h3 className="text-sm font-semibold text-gray-900 dark:text-white">AI Settings</h3>
              </div>
              
              <div className="space-y-3">
                {[
                  { state: edgeSmoothing, setter: setEdgeSmoothing, label: "Edge Smoothing" },
                  { state: temporalSmoothing, setter: setTemporalSmoothing, label: "Temporal Smoothing" },
                  { state: performanceMode, setter: setPerformanceMode, label: "Performance Mode" }
                ].map((setting, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <span className="text-xs text-gray-900 dark:text-white">{setting.label}</span>
                    <button
                      onClick={() => setting.setter(!setting.state)}
                      className={`relative inline-flex h-4 w-8 items-center rounded-full transition-colors ${
                        setting.state ? 'bg-blue-500' : 'bg-gray-300 dark:bg-gray-600'
                      }`}
                    >
                      <span
                        className={`inline-block h-3 w-3 transform rounded-full bg-white transition-transform ${
                          setting.state ? 'translate-x-4' : 'translate-x-0.5'
                        }`}
                      />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;