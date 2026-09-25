import React from 'react';
import { AlertCircle, AlertTriangle, ShieldCheck, Flame } from 'lucide-react';

const SeverityBadge = ({ severity = 'MODERATE', size = 'md' }) => {
  const norm = (severity || 'MODERATE').toUpperCase();

  const config = {
    MILD: {
      bg: 'bg-emerald-50 text-emerald-700 border-emerald-200',
      icon: ShieldCheck,
      label: 'Mild Condition',
    },
    MODERATE: {
      bg: 'bg-amber-50 text-amber-700 border-amber-200',
      icon: AlertTriangle,
      label: 'Moderate Severity',
    },
    SEVERE: {
      bg: 'bg-orange-50 text-orange-700 border-orange-200',
      icon: AlertCircle,
      label: 'Severe Attention Needed',
    },
    CRITICAL: {
      bg: 'bg-red-50 text-red-700 border-red-300 ring-2 ring-red-400/20',
      icon: Flame,
      label: 'Critical / Emergency',
    },
  }[norm] || {
    bg: 'bg-slate-50 text-slate-700 border-slate-200',
    icon: AlertCircle,
    label: norm,
  };

  const IconComponent = config.icon;
  const sizeClasses = size === 'sm' ? 'px-2 py-0.5 text-xs' : 'px-3 py-1.5 text-sm font-semibold';

  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full border ${config.bg} ${sizeClasses}`}>
      <IconComponent className={size === 'sm' ? 'w-3.5 h-3.5' : 'w-4 h-4'} />
      <span>{config.label}</span>
      {norm === 'CRITICAL' && (
        <span className="w-2 h-2 rounded-full bg-red-500 animate-ping" />
      )}
    </span>
  );
};

export default SeverityBadge;
