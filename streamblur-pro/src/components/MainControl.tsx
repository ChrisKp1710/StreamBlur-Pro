import { Play, Square } from 'lucide-react';

interface MainControlProps {
  isActive: boolean;
  onToggle: () => void;
}

export function MainControl({ isActive, onToggle }: MainControlProps) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-3 flex-shrink-0">
      <button
        onClick={onToggle}
        className={`w-full py-2.5 px-4 rounded-lg font-semibold transition-all text-sm ${
          isActive 
            ? 'bg-red-500 hover:bg-red-600 text-white' 
            : 'bg-blue-500 hover:bg-blue-600 text-white'
        }`}
      >
        {isActive ? (
          <>
            <Square className="inline w-3 h-3 mr-2" />
            Stop
          </>
        ) : (
          <>
            <Play className="inline w-3 h-3 mr-2" />
            Start
          </>
        )}
      </button>
      
      <div className={`mt-2 p-1.5 rounded text-xs text-center ${
        isActive 
          ? "bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400"
          : "bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400"
      }`}>
        {isActive ? "✓ Virtual Camera Active" : "Select 'OBS Virtual Camera' in apps"}
      </div>
    </div>
  );
}
