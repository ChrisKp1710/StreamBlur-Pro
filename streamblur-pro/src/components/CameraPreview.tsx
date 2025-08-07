import { Camera, Monitor, Eye, EyeOff } from 'lucide-react';

interface CameraPreviewProps {
  previewEnabled: boolean;
  setPreviewEnabled: (enabled: boolean) => void;
  isActive: boolean;
  blurIntensity: number;
}

export function CameraPreview({ previewEnabled, setPreviewEnabled, isActive, blurIntensity }: CameraPreviewProps) {
  return (
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
  );
}
