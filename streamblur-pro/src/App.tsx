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
  const [previewEnabled, setPreviewEnabled] = useState(false);
  const [fps, setFps] = useState(0);
  
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
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
                <Monitor className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-semibold text-gray-900 dark:text-white">
                  StreamBlur Pro
                </h1>
                <p className="text-sm text-gray-500 dark:text-gray-400">AI Background Blur</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-3">
              <div className={`flex items-center space-x-2 px-3 py-1 rounded-full ${
                isActive ? 'bg-green-50 dark:bg-green-900/20' : 'bg-gray-100 dark:bg-gray-800'
              }`}>
                <div className={`w-2 h-2 rounded-full ${
                  isActive ? 'bg-green-500 animate-pulse' : 'bg-gray-400'
                }`}></div>
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  {isActive ? 'Active' : 'Ready'}
                </span>
              </div>
              
              {isActive && (
                <div className="text-sm font-mono text-gray-600 dark:text-gray-400">
                  {fps.toFixed(1)} FPS
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-4xl mx-auto p-6 space-y-6">
        
        {/* Camera Preview */}
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
          <div className="p-4 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Camera Preview</h2>
              <button
                onClick={() => setPreviewEnabled(!previewEnabled)}
                className={`flex items-center px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                  previewEnabled
                    ? 'bg-blue-500 text-white hover:bg-blue-600'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                }`}
              >
                {previewEnabled ? <Eye className="w-4 h-4 mr-1" /> : <EyeOff className="w-4 h-4 mr-1" />}
                {previewEnabled ? 'Hide Preview' : 'Show Preview'}
              </button>
            </div>
          </div>
          
          {previewEnabled ? (
            <div className="aspect-video bg-gray-100 dark:bg-gray-700 relative">
              {/* Simulated camera preview */}
              <div className="absolute inset-0 bg-gradient-to-br from-blue-500/20 to-purple-500/20 flex items-center justify-center">
                <div className="text-center">
                  <Monitor className="w-12 h-12 text-gray-400 dark:text-gray-500 mx-auto mb-2" />
                  <p className="text-gray-600 dark:text-gray-400 font-medium">Camera Preview</p>
                  <p className="text-sm text-gray-500 dark:text-gray-500 mt-1">
                    Blur Intensity: {blurIntensity}%
                  </p>
                </div>
              </div>
              
              {/* Blur intensity visual indicator */}
              <div className="absolute top-4 right-4">
                <div className={`px-2 py-1 rounded text-xs font-medium ${
                  blurIntensity < 10 ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' :
                  blurIntensity < 20 ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400' :
                  'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
                }`}>
                  {blurIntensity < 10 ? 'Subtle' : blurIntensity < 20 ? 'Moderate' : 'Intense'} Blur
                </div>
              </div>
            </div>
          ) : (
            <div className="aspect-video bg-gray-50 dark:bg-gray-800 flex items-center justify-center border-t border-gray-200 dark:border-gray-700">
              <div className="text-center">
                <EyeOff className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                <p className="text-gray-500 dark:text-gray-400">Preview disabled</p>
              </div>
            </div>
          )}
        </div>

        {/* Main Controls */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Controls */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* Start/Stop */}
            <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
              <button
                onClick={handleStart}
                className={`w-full py-4 px-6 rounded-xl font-semibold text-lg transition-all ${
                  isActive 
                    ? 'bg-red-500 hover:bg-red-600 text-white' 
                    : 'bg-blue-500 hover:bg-blue-600 text-white'
                } focus:ring-2 focus:ring-offset-2 ${
                  isActive ? 'focus:ring-red-500' : 'focus:ring-blue-500'
                }`}
              >
                {isActive ? (
                  <>
                    <Square className="inline w-5 h-5 mr-2" />
                    Stop StreamBlur Pro
                  </>
                ) : (
                  <>
                    <Play className="inline w-5 h-5 mr-2" />
                    Start StreamBlur Pro
                  </>
                )}
              </button>
              
              <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                <p className="text-sm text-blue-800 dark:text-blue-200">
                  {isActive 
                    ? "✓ Virtual camera active as 'OBS Virtual Camera'"
                    : "Select 'OBS Virtual Camera' in Discord, Teams, or OBS after starting"
                  }
                </p>
              </div>
            </div>

            {/* Blur Control */}
            <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">
                Blur Intensity: {blurIntensity}
              </label>
              
              <input
                type="range"
                min="1"
                max="25"
                value={blurIntensity}
                onChange={(e) => setBlurIntensity(parseInt(e.target.value))}
                className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              
              <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-2">
                <span>Subtle</span>
                <span>Moderate</span>
                <span>Intense</span>
              </div>
            </div>
          </div>

          {/* Settings */}
          <div className="space-y-6">
            
            {/* AI Settings */}
            <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
              <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">AI Enhancement</h3>
              
              <div className="space-y-4">
                {[
                  { state: edgeSmoothing, setter: setEdgeSmoothing, label: "Edge Smoothing", desc: "Softer edges" },
                  { state: temporalSmoothing, setter: setTemporalSmoothing, label: "Temporal Smoothing", desc: "Stable movement" },
                  { state: performanceMode, setter: setPerformanceMode, label: "Performance Mode", desc: "Faster processing" }
                ].map((setting, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-900 dark:text-white">{setting.label}</p>
                      <p className="text-xs text-gray-500 dark:text-gray-400">{setting.desc}</p>
                    </div>
                    <button
                      onClick={() => setting.setter(!setting.state)}
                      className={`relative inline-flex h-5 w-9 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                        setting.state ? 'bg-blue-500' : 'bg-gray-300 dark:bg-gray-600'
                      }`}
                    >
                      <span
                        className={`inline-block h-3 w-3 transform rounded-full bg-white transition-transform ${
                          setting.state ? 'translate-x-5' : 'translate-x-1'
                        }`}
                      />
                    </button>
                  </div>
                ))}
              </div>
            </div>

            {/* Performance */}
            <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
              <div className="flex items-center mb-3">
                <Activity className="w-4 h-4 text-gray-400 mr-2" />
                <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300">Performance</h3>
              </div>
              
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">FPS</span>
                  <span className="text-sm font-mono text-gray-900 dark:text-white">
                    {fps.toFixed(1)}
                  </span>
                </div>
                
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">Status</span>
                  <span className={`text-sm font-medium ${
                    fps >= 25 ? 'text-green-600 dark:text-green-400' : 
                    fps >= 20 ? 'text-yellow-600 dark:text-yellow-400' : 
                    'text-red-600 dark:text-red-400'
                  }`}>
                    {fps >= 25 ? 'Excellent' : fps >= 20 ? 'Good' : fps > 0 ? 'Fair' : 'Ready'}
                  </span>
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