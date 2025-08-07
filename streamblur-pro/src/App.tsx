import { useState } from "react";
import { invoke } from "@tauri-apps/api/tauri";
import { 
  Play, 
  Square, 
  Eye, 
  EyeOff,
  Monitor,
  Activity
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

  const handleStart = async () => {
    try {
      const message = await invoke("greet", { name: "StreamBlur Pro" });
      console.log(message);
      setIsActive(!isActive);
      
      // Simulate FPS counter
      if (!isActive) {
        const interval = setInterval(() => {
          setFps(Math.random() * 8 + 25); // 25-33 FPS
        }, 1000);
        return () => clearInterval(interval);
      } else {
        setFps(0);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="h-screen bg-gray-50 dark:bg-gray-900 flex flex-col overflow-hidden">
      {/* Header - Compatto */}
      <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-4 py-3 flex-shrink-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-6 h-6 bg-blue-500 rounded-md flex items-center justify-center">
              <Monitor className="w-3.5 h-3.5 text-white" />
            </div>
            <div>
              <h1 className="text-base font-semibold text-gray-900 dark:text-white">
                StreamBlur Pro
              </h1>
              <p className="text-xs text-gray-500 dark:text-gray-400">AI Background Blur</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <div className={`flex items-center space-x-1.5 px-2 py-1 rounded-full text-xs ${
              isActive ? 'bg-green-50 dark:bg-green-900/20' : 'bg-gray-100 dark:bg-gray-800'
            }`}>
              <div className={`w-1.5 h-1.5 rounded-full ${
                isActive ? 'bg-green-500 animate-pulse' : 'bg-gray-400'
              }`}></div>
              <span className="font-medium text-gray-700 dark:text-gray-300">
                {isActive ? 'Active' : 'Ready'}
              </span>
            </div>
            
            {isActive && (
              <div className="text-xs font-mono text-gray-600 dark:text-gray-400">
                {fps.toFixed(1)} FPS
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content - Una singola vista compatta */}
      <div className="flex-1 p-4 min-h-0">
        <div className="h-full max-w-5xl mx-auto grid grid-cols-4 gap-4">
          
          {/* Camera Preview - Colonna 1-2 */}
          <div className="col-span-2 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 flex flex-col">
            <div className="p-3 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
              <h2 className="text-sm font-semibold text-gray-900 dark:text-white">Camera Preview</h2>
              <button
                onClick={() => setPreviewEnabled(!previewEnabled)}
                className={`flex items-center px-2 py-1 rounded text-xs font-medium transition-colors ${
                  previewEnabled
                    ? 'bg-blue-500 text-white hover:bg-blue-600'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200'
                }`}
              >
                {previewEnabled ? <Eye className="w-3 h-3 mr-1" /> : <EyeOff className="w-3 h-3 mr-1" />}
                {previewEnabled ? 'Hide' : 'Show'}
              </button>
            </div>
            
            <div className="flex-1 relative">
              {previewEnabled ? (
                <div className="absolute inset-0 bg-gradient-to-br from-blue-500/20 to-purple-500/20 flex items-center justify-center">
                  <div className="text-center">
                    <Monitor className="w-8 h-8 text-gray-400 dark:text-gray-500 mx-auto mb-2" />
                    <p className="text-gray-600 dark:text-gray-400 font-medium text-sm">Camera Preview</p>
                    <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                      Blur: {blurIntensity}%
                    </p>
                  </div>
                  
                  {/* Blur indicator */}
                  <div className="absolute top-2 right-2">
                    <div className={`px-1.5 py-0.5 rounded text-xs font-medium ${
                      blurIntensity < 10 ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' :
                      blurIntensity < 20 ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400' :
                      'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
                    }`}>
                      {blurIntensity < 10 ? 'Subtle' : blurIntensity < 20 ? 'Moderate' : 'Intense'}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="absolute inset-0 bg-gray-50 dark:bg-gray-800 flex items-center justify-center">
                  <div className="text-center">
                    <EyeOff className="w-6 h-6 text-gray-400 mx-auto mb-1" />
                    <p className="text-gray-500 dark:text-gray-400 text-sm">Preview disabled</p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Controls - Colonna 3-4 */}
          <div className="col-span-2 space-y-4">
            
            {/* Start/Stop Button */}
            <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
              <button
                onClick={handleStart}
                className={`w-full py-3 px-4 rounded-lg font-semibold transition-all ${
                  isActive 
                    ? 'bg-red-500 hover:bg-red-600 text-white' 
                    : 'bg-blue-500 hover:bg-blue-600 text-white'
                } focus:ring-2 focus:ring-offset-2 ${
                  isActive ? 'focus:ring-red-500' : 'focus:ring-blue-500'
                }`}
              >
                {isActive ? (
                  <>
                    <Square className="inline w-4 h-4 mr-2" />
                    Stop StreamBlur Pro
                  </>
                ) : (
                  <>
                    <Play className="inline w-4 h-4 mr-2" />
                    Start StreamBlur Pro
                  </>
                )}
              </button>
              
              <div className="mt-2 p-2 bg-blue-50 dark:bg-blue-900/20 rounded text-xs text-blue-800 dark:text-blue-200">
                {isActive 
                  ? "✓ Virtual camera active as 'OBS Virtual Camera'"
                  : "Select 'OBS Virtual Camera' in Discord, Teams, or OBS"
                }
              </div>
            </div>

            {/* Blur Control */}
            <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
              <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-2">
                Blur Intensity: {blurIntensity}
              </label>
              
              <input
                type="range"
                min="1"
                max="25"
                value={blurIntensity}
                onChange={(e) => setBlurIntensity(parseInt(e.target.value))}
                className="w-full h-1.5 bg-gray-200 dark:bg-gray-700 rounded appearance-none cursor-pointer"
              />
              
              <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
                <span>Subtle</span>
                <span>Intense</span>
              </div>
            </div>

            {/* Settings & Performance - Side by side */}
            <div className="grid grid-cols-2 gap-4">
              
              {/* AI Settings */}
              <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-3">
                <h3 className="text-xs font-medium text-gray-700 dark:text-gray-300 mb-2">AI Enhancement</h3>
                
                <div className="space-y-2">
                  {[
                    { state: edgeSmoothing, setter: setEdgeSmoothing, label: "Edge Smoothing" },
                    { state: temporalSmoothing, setter: setTemporalSmoothing, label: "Temporal Smoothing" },
                    { state: performanceMode, setter: setPerformanceMode, label: "Performance Mode" }
                  ].map((setting, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <span className="text-xs text-gray-900 dark:text-white">{setting.label}</span>
                      <button
                        onClick={() => setting.setter(!setting.state)}
                        className={`relative inline-flex h-3 w-6 items-center rounded-full transition-colors ${
                          setting.state ? 'bg-blue-500' : 'bg-gray-300 dark:bg-gray-600'
                        }`}
                      >
                        <span
                          className={`inline-block h-2 w-2 transform rounded-full bg-white transition-transform ${
                            setting.state ? 'translate-x-3.5' : 'translate-x-0.5'
                          }`}
                        />
                      </button>
                    </div>
                  ))}
                </div>
              </div>

              {/* Performance */}
              <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-3">
                <div className="flex items-center mb-2">
                  <Activity className="w-3 h-3 text-gray-400 mr-1" />
                  <h3 className="text-xs font-medium text-gray-700 dark:text-gray-300">Performance</h3>
                </div>
                
                <div className="space-y-1.5">
                  <div className="flex justify-between">
                    <span className="text-xs text-gray-600 dark:text-gray-400">FPS</span>
                    <span className="text-xs font-mono text-gray-900 dark:text-white">
                      {fps.toFixed(1)}
                    </span>
                  </div>
                  
                  <div className="flex justify-between">
                    <span className="text-xs text-gray-600 dark:text-gray-400">Status</span>
                    <span className={`text-xs font-medium ${
                      fps >= 25 ? 'text-green-600 dark:text-green-400' : 
                      fps >= 20 ? 'text-yellow-600 dark:text-yellow-400' : 
                      'text-red-600 dark:text-red-400'
                    }`}>
                      {fps >= 25 ? 'Excellent' : fps >= 20 ? 'Good' : fps > 0 ? 'Fair' : 'Ready'}
                    </span>
                  </div>
                  
                  <div className="flex justify-between">
                    <span className="text-xs text-gray-600 dark:text-gray-400">CPU</span>
                    <span className="text-xs font-mono text-gray-900 dark:text-white">23.5%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;