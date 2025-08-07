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
        className={`relative inline-flex h-4 w-8 items-center rounded-full transition-colors ${
          state ? 'bg-blue-500' : 'bg-gray-300 dark:bg-gray-600'
        }`}
      >
        <span
          className={`inline-block h-3 w-3 transform rounded-full bg-white transition-transform ${
            state ? 'translate-x-4' : 'translate-x-0.5'
          }`}
        />
      </button>
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
}

export function AISettings({ 
  edgeSmoothing, 
  setEdgeSmoothing, 
  temporalSmoothing, 
  setTemporalSmoothing, 
  performanceMode, 
  setPerformanceMode 
}: AISettingsProps) {
  const settings = [
    { state: edgeSmoothing, setter: setEdgeSmoothing, label: "Edge Smoothing" },
    { state: temporalSmoothing, setter: setTemporalSmoothing, label: "Temporal Smoothing" },
    { state: performanceMode, setter: setPerformanceMode, label: "Performance Mode" }
  ];

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 flex-1 flex flex-col justify-end">
      <div>
        <div className="flex items-center mb-3">
          <Settings className="w-4 h-4 text-gray-500 mr-2" />
          <h3 className="text-sm font-semibold text-gray-900 dark:text-white">AI Settings</h3>
        </div>
        
        <div className="space-y-3">
          {settings.map((setting, index) => (
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
