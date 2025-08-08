import { Zap } from 'lucide-react';

interface BlurControlProps {
  blurIntensity: number;
  setBlurIntensity: (value: number) => void;
}

export function BlurControl({ blurIntensity, setBlurIntensity }: BlurControlProps) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-3 flex-shrink-0">
      <div className="flex items-center mb-2">
        <Zap className="w-3 h-3 text-yellow-500 mr-2" />
        <h3 className="text-xs font-semibold text-gray-900 dark:text-white">Blur Intensity</h3>
      </div>
      
      <div>
        <div className="flex justify-between mb-1.5">
          <span className="text-xs text-gray-600 dark:text-gray-400">Current</span>
          <span className="text-xs font-mono text-blue-600 dark:text-blue-400">{blurIntensity}</span>
        </div>
        
        <input
          type="range"
          min="1"
          max="25"
          value={blurIntensity}
          onChange={(e) => setBlurIntensity(parseInt(e.target.value))}
          className="w-full h-1.5 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer"
        />
        
        <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
          <span>Low</span>
          <span>High</span>
        </div>
      </div>
    </div>
  );
}
