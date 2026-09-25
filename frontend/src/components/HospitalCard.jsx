import React from 'react';
import { Link } from 'react-router-dom';
import { Building2, MapPin, Phone, Globe, ShieldCheck, Siren, Eye } from 'lucide-react';

const HospitalCard = ({ hospital }) => {
  return (
    <div className="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-card hover:shadow-card-hover transition-all duration-200 flex flex-col justify-between group">
      <div>
        {/* Header with Hospital Name and Emergency Badge */}
        <div className="flex items-start justify-between gap-3 mb-3">
          <div className="flex items-center gap-3">
            <Link to={`/hospitals/${hospital.id}`} className="w-12 h-12 rounded-xl bg-health-50 border border-health-200 flex items-center justify-center text-health-600 shrink-0 group-hover:scale-105 transition-transform">
              <Building2 className="w-6 h-6" />
            </Link>
            <div>
              <Link to={`/hospitals/${hospital.id}`}>
                <h3 className="text-base font-bold text-slate-900 group-hover:text-health-600 transition-colors line-clamp-1">
                  {hospital.name}
                </h3>
              </Link>
              <p className="text-xs text-slate-500 flex items-center gap-1 mt-0.5">
                <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                <span>{hospital.city}, {hospital.state}</span>
              </p>
            </div>
          </div>

          {hospital.emergency_services && (
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-bold bg-red-50 text-red-700 border border-red-200 shrink-0 animate-pulse">
              <Siren className="w-3 h-3 text-red-600" />
              24/7 ER
            </span>
          )}
        </div>

        {/* Description */}
        <p className="text-xs text-slate-600 mb-4 line-clamp-2 leading-relaxed">
          {hospital.description}
        </p>

        {/* Specialties Badges */}
        {hospital.specialties && hospital.specialties.length > 0 && (
          <div className="mb-4">
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">
              Accredited Departments
            </span>
            <div className="flex flex-wrap gap-1.5">
              {hospital.specialties.slice(0, 4).map((spec, i) => (
                <span
                  key={i}
                  className="px-2 py-0.5 rounded-md text-[11px] font-medium bg-slate-100 text-slate-700 border border-slate-200"
                >
                  {spec}
                </span>
              ))}
              {hospital.specialties.length > 4 && (
                <span className="px-2 py-0.5 rounded-md text-[11px] font-medium bg-slate-50 text-slate-500">
                  +{hospital.specialties.length - 4} more
                </span>
              )}
            </div>
          </div>
        )}

        {/* Contact Info */}
        <div className="space-y-1.5 py-3 border-t border-slate-100 text-xs text-slate-600">
          <div className="flex items-start gap-2">
            <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0 mt-0.5" />
            <span className="line-clamp-2">{hospital.address}</span>
          </div>

          {hospital.phone && (
            <div className="flex items-center gap-2">
              <Phone className="w-3.5 h-3.5 text-slate-400 shrink-0" />
              <a href={`tel:${hospital.phone}`} className="hover:text-health-600 font-medium">
                {hospital.phone}
              </a>
            </div>
          )}

          {hospital.website && (
            <div className="flex items-center gap-2">
              <Globe className="w-3.5 h-3.5 text-slate-400 shrink-0" />
              <a
                href={hospital.website}
                target="_blank"
                rel="noreferrer"
                className="text-health-600 hover:underline truncate"
              >
                {hospital.website.replace('https://', '')}
              </a>
            </div>
          )}
        </div>
      </div>

      {/* Hospital Action CTAs */}
      <div className="pt-3 border-t border-slate-100 mt-2 flex flex-wrap gap-2">
        <Link
          to={`/hospitals/${hospital.id}`}
          className="flex-1 flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold text-xs transition-colors"
        >
          <Eye className="w-3.5 h-3.5" />
          View Details
        </Link>
        <a
          href={`tel:${hospital.phone}`}
          className="flex-1 flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl bg-health-50 hover:bg-health-100 text-health-700 font-semibold text-xs transition-colors border border-health-200/60"
        >
          <Phone className="w-3.5 h-3.5" />
          Call
        </a>
        {hospital.emergency_services && (
          <a
            href="tel:108"
            className="flex-1 flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl bg-red-600 hover:bg-red-700 text-white font-semibold text-xs transition-colors shadow-xs"
          >
            <Siren className="w-3.5 h-3.5" />
            108
          </a>
        )}
      </div>
    </div>
  );
};

export default HospitalCard;
