import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { hospitalAPI } from '../services/api';
import HospitalCard from '../components/HospitalCard';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';
import EmptyState from '../components/EmptyState';
import { Building2, Search, Siren, ShieldCheck } from 'lucide-react';

const Hospitals = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialEmergency = searchParams.get('emergency') === 'true';

  const [hospitals, setHospitals] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [emergencyOnly, setEmergencyOnly] = useState(initialEmergency);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchHospitals();
  }, [emergencyOnly]);

  const fetchHospitals = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = {};
      if (emergencyOnly) params.emergency = 'true';
      const res = await hospitalAPI.getHospitals(params);
      if (res.data?.hospitals) {
        setHospitals(res.data.hospitals);
      }
    } catch (err) {
      setError(err.message || 'Unable to retrieve hospitals.');
    } finally {
      setLoading(false);
    }
  };

  const filteredHospitals = hospitals.filter((h) => {
    if (!searchQuery.trim()) return true;
    const q = searchQuery.toLowerCase();
    const str = `${h.name} ${h.city} ${h.state} ${h.description} ${(h.specialties || []).join(' ')}`.toLowerCase();
    return str.includes(q);
  });

  return (
    <div className="min-h-screen bg-slate-50 py-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="text-center max-w-2xl mx-auto mb-8">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-health-100 text-health-800 text-xs font-bold uppercase tracking-wider mb-2">
            <Building2 className="w-3.5 h-3.5" />
            Accredited Medical Centers
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
            Find a Hospital
          </h1>
          <p className="text-sm text-slate-600 mt-2">
            Explore healthcare facilities and services available around you.
          </p>
        </div>

        {/* Filter Controls */}
        <div className="bg-white rounded-3xl p-4 sm:p-5 shadow-card border border-slate-200/90 mb-8">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            
            {/* Search */}
            <div className="relative flex-1 w-full">
              <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search hospitals by name, city, or medical specialties..."
                className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 text-slate-900 text-sm focus:ring-2 focus:ring-health-500 outline-none"
              />
            </div>

            {/* 24/7 Emergency Toggle */}
            <button
              type="button"
              onClick={() => {
                const next = !emergencyOnly;
                setEmergencyOnly(next);
                setSearchParams(next ? { emergency: 'true' } : {});
              }}
              className={`px-4 py-2.5 rounded-xl text-xs font-bold transition-all border flex items-center gap-2 shrink-0 ${
                emergencyOnly
                  ? 'bg-red-600 text-white border-red-600 shadow-sm'
                  : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
              }`}
            >
              <Siren className={`w-4 h-4 ${emergencyOnly ? 'text-white' : 'text-red-600'}`} />
              24/7 Emergency Facilities Only
            </button>

          </div>
        </div>

        {/* Hospital Grid */}
        {loading ? (
          <LoadingState message="Locating accredited hospitals..." />
        ) : error ? (
          <ErrorState message={error} onRetry={fetchHospitals} />
        ) : filteredHospitals.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredHospitals.map((h) => (
              <HospitalCard key={h.id} hospital={h} />
            ))}
          </div>
        ) : (
          <EmptyState
            title="No hospitals are currently available."
            message={
              searchQuery
                ? `No hospitals match your search criteria "${searchQuery}".`
                : "No hospitals are currently available."
            }
            actionText="Reset Search"
            onAction={() => {
              setSearchQuery('');
              setEmergencyOnly(false);
              setSearchParams({});
            }}
          />
        )}

      </div>
    </div>
  );
};

export default Hospitals;
