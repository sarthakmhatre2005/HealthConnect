import React from 'react';
import { AlertOctagon, PhoneCall, Building2, ShieldAlert } from 'lucide-react';
import { Link } from 'react-router-dom';

const EmergencyAlert = ({ message, emergencyEvent }) => {
  return (
    <div className="rounded-2xl bg-gradient-to-br from-red-600 to-rose-700 text-white p-5 sm:p-6 shadow-xl border-2 border-red-400/40 relative overflow-hidden animate-in fade-in zoom-in-95">
      {/* Background visual watermarks */}
      <div className="absolute -right-8 -bottom-8 text-white/10 pointer-events-none">
        <AlertOctagon className="w-48 h-48" />
      </div>

      <div className="relative z-10">
        <div className="flex items-center gap-2.5 mb-3">
          <div className="p-2 rounded-xl bg-white text-red-600 shadow-md">
            <AlertOctagon className="w-6 h-6 animate-bounce" />
          </div>
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-red-200">
              URGENT CLINICAL TRIAGE ALERT
            </span>
            <h3 className="text-lg sm:text-xl font-extrabold text-white">
              {emergencyEvent || 'High Risk Symptoms Detected'}
            </h3>
          </div>
        </div>

        <p className="text-sm sm:text-base text-red-50 leading-relaxed mb-4 max-w-2xl font-medium">
          {message || 'These reported symptoms may indicate an acute condition requiring urgent, in-person clinical evaluation. Please seek emergency medical care without delay.'}
        </p>

        <div className="flex flex-wrap items-center gap-3 pt-2">
          <a
            href="tel:112"
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-white text-red-700 font-bold text-sm shadow-md hover:bg-red-50 transition-all active:scale-95"
          >
            <PhoneCall className="w-4 h-4" />
            Call National Emergency (112)
          </a>

          <a
            href="tel:108"
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-red-900/50 hover:bg-red-900/70 text-white font-semibold text-sm border border-red-300/30 transition-all"
          >
            <PhoneCall className="w-4 h-4" />
            Medical Ambulance (108)
          </a>

          <Link
            to="/hospitals?emergency=true"
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-red-800/60 hover:bg-red-800/90 text-white font-semibold text-sm border border-red-300/30 transition-all"
          >
            <Building2 className="w-4 h-4" />
            Find 24/7 Emergency Hospitals
          </Link>
        </div>

        <div className="mt-4 pt-3 border-t border-red-500/40 text-[11px] text-red-200 flex items-center gap-1.5">
          <ShieldAlert className="w-3.5 h-3.5" />
          <span>If someone is unconscious or unable to breathe, begin CPR if trained and call 112 immediately.</span>
        </div>
      </div>
    </div>
  );
};

export default EmergencyAlert;
