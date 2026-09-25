import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { doctorAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import DoctorCard from '../components/DoctorCard';
import BookAppointmentModal from '../components/BookAppointmentModal';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';
import EmptyState from '../components/EmptyState';
import { Search, Stethoscope, Filter, UserCheck, CheckCircle2 } from 'lucide-react';

const Doctors = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialSpec = searchParams.get('specialization') || '';

  const [doctors, setDoctors] = useState([]);
  const [specializations, setSpecializations] = useState([]);
  const [selectedSpecialty, setSelectedSpecialty] = useState(initialSpec);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Modal State
  const [selectedDoctor, setSelectedDoctor] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [bookingSuccessAlert, setBookingSuccessAlert] = useState(false);

  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    fetchSpecializations();
  }, []);

  useEffect(() => {
    fetchDoctors();
  }, [selectedSpecialty]);

  const fetchSpecializations = async () => {
    try {
      const res = await doctorAPI.getSpecializations();
      if (res.data?.specializations) {
        setSpecializations(res.data.specializations);
      }
    } catch (e) {
      console.error('Error fetching specializations:', e);
    }
  };

  const fetchDoctors = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = {};
      if (selectedSpecialty) params.specialization = selectedSpecialty;
      const res = await doctorAPI.getDoctors(params);
      if (res.data?.doctors) {
        setDoctors(res.data.doctors);
      }
    } catch (err) {
      setError(err.message || 'Unable to retrieve verified doctors.');
    } finally {
      setLoading(false);
    }
  };

  const handleBookClick = (doctor) => {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: { pathname: '/doctors' } } });
      return;
    }
    setSelectedDoctor(doctor);
    setIsModalOpen(true);
  };

  const handleBookingSuccess = (appt) => {
    setBookingSuccessAlert(true);
    setTimeout(() => setBookingSuccessAlert(false), 5000);
  };

  // Local filter for search query
  const filteredDoctors = doctors.filter((doc) => {
    if (!searchQuery.trim()) return true;
    const q = searchQuery.toLowerCase();
    const str = `${doc.name} ${doc.specialization} ${doc.city} ${doc.bio}`.toLowerCase();
    return str.includes(q);
  });

  return (
    <div className="min-h-screen bg-slate-50 py-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Page Header */}
        <div className="text-center max-w-2xl mx-auto mb-8">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-health-100 text-health-800 text-xs font-bold uppercase tracking-wider mb-2">
            <UserCheck className="w-3.5 h-3.5" />
            Verified Medical Specialists
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
            Find the Right Doctor
          </h1>
          <p className="text-sm text-slate-600 mt-2">
            Search healthcare professionals by name, specialty, or location.
          </p>
        </div>

        {bookingSuccessAlert && (
          <div className="mb-6 max-w-lg mx-auto p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 flex items-center gap-3 shadow-sm animate-in fade-in">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
            <div>
              <span className="font-bold block">Appointment Confirmed!</span>
              <span>Your appointment request has been scheduled. View it on your dashboard.</span>
            </div>
          </div>
        )}

        {/* Filter & Search Bar */}
        <div className="bg-white rounded-3xl p-4 sm:p-5 shadow-card border border-slate-200/90 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-4 items-center">
            
            {/* Search Input */}
            <div className="md:col-span-7 relative">
              <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search by doctor name, specialty, or clinic location..."
                className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 text-slate-900 text-sm focus:ring-2 focus:ring-health-500 outline-none"
              />
            </div>

            {/* Specialty Dropdown */}
            <div className="md:col-span-5 relative">
              <select
                value={selectedSpecialty}
                onChange={(e) => {
                  setSelectedSpecialty(e.target.value);
                  setSearchParams(e.target.value ? { specialization: e.target.value } : {});
                }}
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-slate-900 text-sm focus:ring-2 focus:ring-health-500 outline-none bg-white font-medium"
              >
                <option value="">All Medical Disciplines ({specializations.length})</option>
                {specializations.map((spec) => (
                  <option key={spec} value={spec}>
                    {spec}
                  </option>
                ))}
              </select>
            </div>

          </div>

          {/* Quick Filter Specialty Pills */}
          <div className="mt-3 pt-3 border-t border-slate-100 flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none">
            <button
              onClick={() => {
                setSelectedSpecialty('');
                setSearchParams({});
              }}
              className={`px-3 py-1 rounded-lg text-xs font-semibold shrink-0 transition-colors ${
                !selectedSpecialty
                  ? 'bg-slate-900 text-white'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              All
            </button>
            {specializations.map((spec) => (
              <button
                key={spec}
                onClick={() => {
                  setSelectedSpecialty(spec);
                  setSearchParams({ specialization: spec });
                }}
                className={`px-3 py-1 rounded-lg text-xs font-semibold shrink-0 transition-colors ${
                  selectedSpecialty === spec
                    ? 'bg-health-600 text-white shadow-xs'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                {spec}
              </button>
            ))}
          </div>
        </div>

        {/* Doctor Cards Grid */}
        {loading ? (
          <LoadingState message="Finding verified specialist doctors..." />
        ) : error ? (
          <ErrorState message={error} onRetry={fetchDoctors} />
        ) : filteredDoctors.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredDoctors.map((doc) => (
              <DoctorCard
                key={doc.id}
                doctor={doc}
                onBook={handleBookClick}
              />
            ))}
          </div>
        ) : (
          <EmptyState
            title="No doctors are currently available."
            message={
              searchQuery || selectedSpecialty
                ? `No specialist matching "${searchQuery || selectedSpecialty}". Try resetting your filters.`
                : "No doctors are currently available."
            }
            actionText="Clear Filters"
            onAction={() => {
              setSearchQuery('');
              setSelectedSpecialty('');
              setSearchParams({});
            }}
          />
        )}

      </div>

      {/* Booking Modal */}
      <BookAppointmentModal
        doctor={selectedDoctor}
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSuccess={handleBookingSuccess}
      />
    </div>
  );
};

export default Doctors;
