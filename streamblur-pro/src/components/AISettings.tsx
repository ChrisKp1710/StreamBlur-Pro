import { Settings } from 'lucide-react';

interface ToggleProps {
  state: boolean;
  setState: (value: boolean) => void;
  label: string;
}

function Toggle({ state, setState, label }: ToggleProps) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-xs text-gray-900 dark:text-white">{label}</span>
      <button
        onClick={() => setState(!state)}
        className={`relative inline-flex h-3 w-6 items-center rounded-full transition-colors ${
          state ? 'bg-blue-500' : 'bg-gray-300 dark:bg-gray-600'
        }`}
      >
        <span
          className={`inline-block h-2 w-2 transform rounded-full bg-white transition-transform ${
            state ? 'translate-x-3.5' : 'translate-x-0.5'
          }`}
        />
      </button>
    </div>
  );
}

interface QualitySelectProps {
  quality: string;
  setQuality: (value: string) => void;
  label: string;
}

function QualitySelect({ quality, setQuality, label }: QualitySelectProps) {
  const qualities = [
    { value: 'low', label: 'Low (Fast)', description: 'Performance mode - più veloce' },
    { value: 'medium', label: 'Medium', description: 'Bilanciato' },
    { value: 'high', label: 'High (Accurate)', description: 'Accuracy mode - più preciso' }
  ];

  return (
    <div className="space-y-1">
      <span className="text-xs text-gray-900 dark:text-white">{label}</span>
      <select
        value={quality}
        onChange={(e) => setQuality(e.target.value)}
        className="w-full text-xs bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded px-1 py-0.5 text-gray-900 dark:text-white"
      >
        {qualities.map((q) => (
          <option key={q.value} value={q.value}>
            {q.label}
          </option>
        ))}
      </select>
      <div className="text-xs text-gray-500 dark:text-gray-400 leading-tight">
        {qualities.find(q => q.value === quality)?.description}
      </div>
    </div>
  );
}

interface AISettingsProps {
  edgeSmoothing: boolean;
  setEdgeSmoothing: (value: boolean) => void;
  temporalSmoothing: boolean;
  setTemporalSmoothing: (value: boolean) => void;
  performanceMode: boolean;
  setPerformanceMode: (value: boolean) => void;
  quality?: string;
  setQuality?: (value: string) => void;
}

export function AISettings({ 
  edgeSmoothing, 
  setEdgeSmoothing, 
  temporalSmoothing, 
  setTemporalSmoothing, 
  performanceMode, 
  setPerformanceMode,
  quality = 'medium',
  setQuality 
}: AISettingsProps) {
  const toggleSettings = [
    { state: edgeSmoothing, setter: setEdgeSmoothing, label: "Edge Smoothing" },
    { state: temporalSmoothing, setter: setTemporalSmoothing, label: "Temporal Smoothing" },
    { state: performanceMode, setter: setPerformanceMode, label: "Performance Mode (Legacy)" }
  ];

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-3 flex-shrink-0">
      <div>
        <div className="flex items-center mb-2">
          <Settings className="w-3 h-3 text-gray-500 mr-2" />
          <h3 className="text-xs font-semibold text-gray-900 dark:text-white">AI Settings</h3>
        </div>
        
        <div className="space-y-2">
          {/* Quality Selector - NEW */}
          {setQuality && (
            <QualitySelect
              quality={quality}
              setQuality={setQuality}
              label="AI Quality"
            />
          )}
          
          {/* Toggle Settings */}
          {toggleSettings.map((setting, index) => (
            <Toggle
              key={index}
              state={setting.state}
              setState={setting.setter}
              label={setting.label}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
