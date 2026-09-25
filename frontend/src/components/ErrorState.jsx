import React from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';

const ErrorState = ({ message = 'Unable to connect to HealthConnect.', onRetry }) => {
  return (
    <div className="py-12 flex flex-col items-center justify-center text-center p-6 bg-red-50/50 rounded-2xl border border-red-100 max-w-lg mx-auto my-6 animate-in fade-in">
      <div className="w-12 h-12 rounded-2xl bg-red-100 flex items-center justify-center text-red-600 mb-3">
        <AlertCircle className="w-6 h-6" />
      </div>
      <h3 className="text-base font-bold text-slate-900 mb-1">Service Notice</h3>
      <p className="text-xs text-slate-600 mb-4 max-w-sm leading-relaxed">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-white border border-slate-200 text-slate-700 font-semibold text-xs shadow-sm hover:bg-slate-50 transition-all"
        >
          <RefreshCw className="w-3.5 h-3.5 text-slate-500" />
          Try Again
        </button>
      )}
    </div>
  );
};

export default ErrorState;
