import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { doctorAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import BookAppointmentModal from '../components/BookAppointmentModal';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';
import { 
  Stethoscope, 
  MapPin, 
  Calendar, 
  Clock, 
  Award, 
  Phone, 
  Mail, 
  ArrowLeft, 
  ShieldCheck, 
  CheckCircle2 
} from 'lucide-react';

const DoctorProfile = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const [doctor, setDoctor] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [bookingSuccessAlert, setBookingSuccessAlert] = useState(false);

  useEffect(() => {
    fetchDoctor();
  }, [id]);

  const fetchDoctor = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await doctorAPI.getDoctorById(id);
      if (res.data?.doctor) {
        setDoctor(res.data.doctor);
      } else {
        setError('Doctor details not found.');
      }
    } catch (err) {
      setError(err.message || 'Failed to load doctor profile.');
    } finally {
      setLoading(false);
    }
  };

  const handleBookClick = () => {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: { pathname: `/doctors/${id}` } } });
      return;
    }
    setIsModalOpen(true);
  };

  const handleBookingSuccess = () => {
    setBookingSuccessAlert(true);
    setTimeout(() => setBookingSuccessAlert(false), 5000);
  };

  if (loading) {
    return <LoadingState message="Loading specialist profile..." />;
  }

  if (error || !doctor) {
    return <ErrorState message={error || 'Doctor not found.'} onRetry={fetchDoctor} />;
  }

  let hoursDisplay = "09:00 AM - 05:00 PM";
  if (doctor.available_hours) {
    try {
      const parsed = typeof doctor.available_hours === 'string' ? JSON.parse(doctor.available_hours) : doctor.available_hours;
      if (parsed.start && parsed.end) {
        hoursDisplay = `${parsed.start} - ${parsed.end}`;
      }
    } catch (e) {}
  }

  return (
    <div className="min-h-screen bg-slate-50 py-10">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
        
        {/* Back Link */}
        <Link
          to="/doctors"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-800 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" /> Back to All Doctors
        </Link>

        {/* Success Alert */}
        {bookingSuccessAlert && (
          <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-xs font-semibold text-emerald-800 flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
            <span>Your appointment has been confirmed! View it in your dashboard.</span>
          </div>
        )}

        {/* Main Doctor Profile Card */}
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200/90 shadow-card space-y-6">
          
          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-6">
            <div className="w-24 h-24 rounded-3xl bg-gradient-to-tr from-health-100 to-tealAccent-100 border border-health-200 flex items-center justify-center shrink-0 shadow-inner overflow-hidden">
              <img
                src="/assets/doctor-avatar.svg"
                alt={doctor.name}
                className="w-full h-full object-cover"
              />
            </div>

            <div className="space-y-1.5 flex-1">
              <div className="flex flex-wrap items-center gap-2">
                <span className="px-3 py-0.5 rounded-full text-xs font-bold bg-health-50 text-health-700 border border-health-200">
                  {doctor.specialization}
                </span>
                <span className="inline-flex items-center gap-1 text-xs text-slate-400 font-mono">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" />
                  Verified Specialist
                </span>
              </div>

              <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
                {doctor.name}
              </h1>

              <p className="text-xs sm:text-sm text-slate-500 flex items-center gap-2">
                <Award className="w-4 h-4 text-slate-400" />
                <span>{doctor.experience_years ? `${doctor.experience_years} Years Experience` : 'Experienced Practitioner'}</span>
                <span>•</span>
                <span>Reg. License: {doctor.license_number || 'MED-REG-2024'}</span>
              </p>
            </div>

            <button
              onClick={handleBookClick}
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-health-600 hover:bg-health-700 text-white font-bold text-xs sm:text-sm shadow-md transition-all active:scale-95 shrink-0"
            >
              <Calendar className="w-4 h-4" />
              Book Appointment
            </button>
          </div>

          {/* Bio Section */}
          <div className="border-t border-slate-100 pt-6">
            <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-2">
              Clinical Background & Biography
            </h3>
            <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
              {doctor.bio || `Dr. ${doctor.name} is an experienced medical specialist in ${doctor.specialization}. Dedicated to evidence-based healthcare, preventive guidance, and patient-centered clinical practice.`}
            </p>
          </div>

          {/* Practice & Schedule Details Grid */}
          <div className="border-t border-slate-100 pt-6 grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs text-slate-600">
            <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200/60 space-y-2">
              <span className="font-bold text-slate-700 uppercase tracking-wider block">Clinic Location</span>
              <div className="flex items-start gap-2">
                <MapPin className="w-4 h-4 text-health-600 shrink-0 mt-0.5" />
                <span>{doctor.address ? `${doctor.address}, ${doctor.city}, ${doctor.state}` : (doctor.city || 'Central Medical Hub')}</span>
              </div>
              {doctor.phone && (
                <div className="flex items-center gap-2 pt-1">
                  <Phone className="w-4 h-4 text-health-600 shrink-0" />
                  <span>{doctor.phone}</span>
                </div>
              )}
            </div>

            <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200/60 space-y-2">
              <span className="font-bold text-slate-700 uppercase tracking-wider block">Availability & Hours</span>
              <div className="flex items-center gap-2">
                <Calendar className="w-4 h-4 text-tealAccent-600 shrink-0" />
                <span>Working Days: {doctor.available_days || 'Mon, Tue, Wed, Thu, Fri'}</span>
              </div>
              <div className="flex items-center gap-2 pt-1">
                <Clock className="w-4 h-4 text-tealAccent-600 shrink-0" />
                <span>Working Hours: {hoursDisplay}</span>
              </div>
            </div>
          </div>

        </div>

        {/* Modal Booking */}
        {isModalOpen && (
          <BookAppointmentModal
            doctor={doctor}
            isOpen={isModalOpen}
            onClose={() => setIsModalOpen(false)}
            onSuccess={handleBookingSuccess}
          />
        )}

      </div>
    </div>
  );
};

export default DoctorProfile;
