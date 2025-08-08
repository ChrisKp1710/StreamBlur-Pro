import { Activity } from 'lucide-react';

interface PerformanceProps {
  fps: number;
  cpuUsage?: number;
  memoryUsage?: number;
}

export function Performance({ fps, cpuUsage = 0, memoryUsage = 0 }: PerformanceProps) {
  const getStatusColor = () => {
    if (fps >= 25) return 'text-green-600 dark:text-green-400';
    if (fps >= 20) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-orange-600 dark:text-orange-400';
  };

  const getStatusText = () => {
    if (fps >= 25) return 'Excellent';
    if (fps >= 20) return 'Good';
    return 'Fair';
  };

  const getCpuColor = () => {
    if (cpuUsage <= 30) return 'text-green-600 dark:text-green-400';
    if (cpuUsage <= 60) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  const getMemoryColor = () => {
    if (memoryUsage <= 512) return 'text-green-600 dark:text-green-400';
    if (memoryUsage <= 1024) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-3 flex-shrink-0">
      <div className="flex items-center mb-2">
        <Activity className="w-3 h-3 text-blue-500 mr-2" />
        <h3 className="text-xs font-semibold text-gray-900 dark:text-white">Performance</h3>
      </div>
      
      <div className="space-y-1.5">
        <div className="flex justify-between items-center">
          <span className="text-xs text-gray-600 dark:text-gray-400">FPS</span>
          <span className="text-sm font-mono font-bold text-blue-600 dark:text-blue-400">
            {fps.toFixed(0)}
          </span>
        </div>
        
        <div className="flex justify-between items-center">
          <span className="text-xs text-gray-600 dark:text-gray-400">CPU</span>
          <span className={`text-xs font-medium ${getCpuColor()}`}>
            {cpuUsage.toFixed(1)}%
          </span>
        </div>
        
        <div className="flex justify-between items-center">
          <span className="text-xs text-gray-600 dark:text-gray-400">Memory</span>
          <span className={`text-xs font-medium ${getMemoryColor()}`}>
            {memoryUsage.toFixed(0)} MB
          </span>
        </div>
        
        <div className="flex justify-between items-center">
          <span className="text-xs text-gray-600 dark:text-gray-400">Status</span>
          <span className={`text-xs font-medium ${getStatusColor()}`}>
            {getStatusText()}
          </span>
        </div>
      </div>
    </div>
  );
}
