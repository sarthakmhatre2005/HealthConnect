import React from 'react';
import { Activity } from 'lucide-react';

const LoadingState = ({ message = 'Loading healthcare information...' }) => {
  return (
    <div className="py-16 flex flex-col items-center justify-center text-center p-4 animate-in fade-in">
      <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-health-50 to-tealAccent-50 border border-health-200/80 flex items-center justify-center text-health-600 shadow-inner mb-4">
        <Activity className="w-8 h-8 animate-spin text-health-600" />
      </div>
      <h3 className="text-base font-bold text-slate-800 mb-1">{message}</h3>
      <p className="text-xs text-slate-500 max-w-sm">
        Please wait while HealthConnect retrieves data from the verified clinical backend.
      </p>
    </div>
  );
};

export default LoadingState;
