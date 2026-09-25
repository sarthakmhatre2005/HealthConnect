import React from 'react';
import { Link } from 'react-router-dom';

const EmptyState = ({
  title = 'No records found',
  message = 'There is currently no information to display.',
  actionText,
  actionLink,
  onAction,
}) => {
  return (
    <div className="py-14 flex flex-col items-center justify-center text-center p-6 bg-white rounded-2xl border border-slate-200/80 shadow-sm max-w-md mx-auto my-6">
      <div className="w-40 h-28 mb-3 opacity-90">
        <img src="/assets/empty-state.svg" alt="Empty state" className="w-full h-full object-contain" />
      </div>
      <h3 className="text-base font-bold text-slate-900 mb-1">{title}</h3>
      <p className="text-xs text-slate-500 mb-5 max-w-xs leading-relaxed">{message}</p>
      
      {actionLink && actionText && (
        <Link
          to={actionLink}
          className="px-4 py-2 rounded-xl bg-health-600 hover:bg-health-700 text-white font-semibold text-xs shadow-sm transition-all"
        >
          {actionText}
        </Link>
      )}

      {onAction && actionText && !actionLink && (
        <button
          onClick={onAction}
          className="px-4 py-2 rounded-xl bg-health-600 hover:bg-health-700 text-white font-semibold text-xs shadow-sm transition-all"
        >
          {actionText}
        </button>
      )}
    </div>
  );
};

export default EmptyState;
