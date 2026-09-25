import React from 'react';
import { Link } from 'react-router-dom';
import { Activity, ShieldAlert, PhoneCall } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-slate-900 text-slate-300 pt-12 pb-8 border-t border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Medical Disclaimer Banner (Step 23) */}
        <div className="bg-slate-800/80 border border-slate-700/80 rounded-xl p-4 sm:p-5 mb-10 flex flex-col md:flex-row items-start md:items-center gap-4">
          <div className="p-2.5 rounded-lg bg-amber-500/10 text-amber-400 shrink-0">
            <ShieldAlert className="w-5 h-5" />
          </div>
          <div className="text-xs sm:text-sm text-slate-300 leading-relaxed flex-1">
            <strong className="text-white block sm:inline font-semibold mb-1 sm:mb-0">
              Important Medical Disclaimer:{' '}
            </strong>
            HealthConnect provides preliminary AI-assisted health information and is not a substitute for professional medical diagnosis or treatment. For emergency situations, seek immediate medical attention.
          </div>
          <div className="shrink-0 w-full md:w-auto">
            <a 
              href="tel:112" 
              className="inline-flex items-center justify-center gap-1.5 px-3 py-1.5 rounded-lg bg-red-600 hover:bg-red-700 text-white font-medium text-xs transition-colors w-full md:w-auto"
            >
              <PhoneCall className="w-3.5 h-3.5" />
              Emergency: 112
            </a>
          </div>
        </div>

        {/* Footer Navigation Columns */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8 pb-10 border-b border-slate-800">
          
          {/* Brand Info */}
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-health-600 flex items-center justify-center text-white">
                <Activity className="w-5 h-5" />
              </div>
              <span className="text-lg font-bold text-white tracking-tight">
                Health<span className="text-health-400">Connect</span>
              </span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Intelligent healthcare connected around you.
            </p>
          </div>

          {/* Services Column */}
          <div>
            <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-3">Healthcare Services</h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link to="/symptom-checker" className="hover:text-white transition-colors">
                  AI Health Insights
                </Link>
              </li>
              <li>
                <Link to="/doctors" className="hover:text-white transition-colors">
                  Find Doctors
                </Link>
              </li>
              <li>
                <Link to="/hospitals" className="hover:text-white transition-colors">
                  Hospitals
                </Link>
              </li>
              <li>
                <Link to="/appointments" className="hover:text-white transition-colors">
                  Appointments
                </Link>
              </li>
            </ul>
          </div>

          {/* Support Column */}
          <div>
            <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-3">Patient Support</h4>
            <ul className="space-y-2 text-xs">
              <li>
                <a href="mailto:support@healthconnect.platform" className="hover:text-white transition-colors">
                  Contact Support
                </a>
              </li>
              <li>
                <Link to="/hospitals" className="hover:text-white transition-colors">
                  Emergency Information
                </Link>
              </li>
              <li>
                <Link to="/symptom-checker" className="hover:text-white transition-colors">
                  Symptom Intake
                </Link>
              </li>
            </ul>
          </div>

        </div>

        {/* Copyright */}
        <div className="pt-6 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-3">
          <div>
            &copy; {new Date().getFullYear()} HealthConnect Platform. All rights reserved.
          </div>
          <div className="flex items-center gap-4 text-xs text-slate-500">
            <span>Confidential & Secure</span>
            <span>&bull;</span>
            <Link to="/symptom-checker" className="hover:text-slate-400">Check Symptoms</Link>
          </div>
        </div>

      </div>
    </footer>
  );
};

export default Footer;

