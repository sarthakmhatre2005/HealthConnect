import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { hospitalAPI } from '../services/api';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';
import { 
  Building2, 
  MapPin, 
  Phone, 
  Mail, 
  Globe, 
  Siren, 
  ShieldCheck, 
  ArrowLeft,
  CheckCircle2
} from 'lucide-react';

const HospitalProfile = () => {
  const { id } = useParams();
  const [hospital, setHospital] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchHospital();
  }, [id]);

  const fetchHospital = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await hospitalAPI.getHospitalById(id);
      if (res.data?.hospital) {
        setHospital(res.data.hospital);
      } else {
        setError('Hospital details not found.');
      }
    } catch (err) {
      setError(err.message || 'Failed to load hospital details.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingState message="Loading hospital information..." />;
  }

  if (error || !hospital) {
    return <ErrorState message={error || 'Hospital not found.'} onRetry={fetchHospital} />;
  }

  return (
    <div className="min-h-screen bg-slate-50 py-10">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
        
        {/* Back Navigation */}
        <Link
          to="/hospitals"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-800 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" /> Back to All Hospitals
        </Link>

        {/* Hospital Card */}
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200/90 shadow-card space-y-6">
          
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div className="flex items-start gap-4">
              <div className="w-16 h-16 rounded-2xl bg-health-50 border border-health-200 text-health-600 flex items-center justify-center shrink-0">
                <Building2 className="w-8 h-8" />
              </div>
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                    {hospital.city}, {hospital.state}
                  </span>
                  {hospital.emergency_services && (
                    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-red-50 text-red-700 border border-red-200">
                      <Siren className="w-3 h-3 text-red-600" />
                      24/7 Trauma & Emergency
                    </span>
                  )}
                </div>
                <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
                  {hospital.name}
                </h1>
                <p className="text-xs text-slate-500 flex items-center gap-1">
                  <MapPin className="w-3.5 h-3.5 text-slate-400" />
                  {hospital.address}
                </p>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row items-center gap-2 w-full sm:w-auto">
              <a
                href={`tel:${hospital.phone}`}
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold text-xs shadow-xs transition-colors"
              >
                <Phone className="w-4 h-4 text-health-600" />
                Call Reception
              </a>
              {hospital.emergency_services && (
                <a
                  href="tel:108"
                  className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-red-600 hover:bg-red-700 text-white font-bold text-xs shadow-md transition-colors"
                >
                  <Siren className="w-4 h-4" />
                  Ambulance: 108
                </a>
              )}
            </div>
          </div>

          {/* About Hospital */}
          <div className="border-t border-slate-100 pt-6">
            <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-2">
              About This Healthcare Facility
            </h3>
            <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
              {hospital.description || `${hospital.name} is an accredited tertiary medical center providing 24/7 acute clinical services, surgical suites, and specialized outpatient care.`}
            </p>
          </div>

          {/* Accredited Departments / Specialties */}
          {hospital.specialties && hospital.specialties.length > 0 && (
            <div className="border-t border-slate-100 pt-6">
              <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-3">
                Accredited Medical Departments
              </h3>
              <div className="flex flex-wrap gap-2">
                {hospital.specialties.map((dept, i) => (
                  <span
                    key={i}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold bg-health-50 text-health-700 border border-health-200/60"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5 text-health-600" />
                    {dept}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Contact Details Grid */}
          <div className="border-t border-slate-100 pt-6 grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs text-slate-600">
            {hospital.phone && (
              <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200/60 space-y-1">
                <span className="font-bold text-slate-700 uppercase tracking-wider block">Phone Contact</span>
                <a href={`tel:${hospital.phone}`} className="text-health-600 hover:underline font-semibold block">
                  {hospital.phone}
                </a>
              </div>
            )}

            {hospital.email && (
              <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200/60 space-y-1">
                <span className="font-bold text-slate-700 uppercase tracking-wider block">Official Email</span>
                <span className="text-slate-800">{hospital.email}</span>
              </div>
            )}

            {hospital.website && (
              <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200/60 space-y-1">
                <span className="font-bold text-slate-700 uppercase tracking-wider block">Website</span>
                <a
                  href={hospital.website}
                  target="_blank"
                  rel="noreferrer"
                  className="text-health-600 hover:underline truncate block"
                >
                  {hospital.website}
                </a>
              </div>
            )}
          </div>

        </div>

      </div>
    </div>
  );
};

export default HospitalProfile;
