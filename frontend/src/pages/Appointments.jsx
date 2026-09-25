import React, { useState, useEffect } from 'react';
import { appointmentAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import AppointmentCard from '../components/AppointmentCard';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';
import EmptyState from '../components/EmptyState';
import { Calendar, CheckCircle2, Clock, XCircle, Plus } from 'lucide-react';
import { Link } from 'react-router-dom';

const Appointments = () => {
  const [appointments, setAppointments] = useState([]);
  const [activeTab, setActiveTab] = useState('upcoming');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [actionSuccessMsg, setActionSuccessMsg] = useState(null);

  const { user, isDoctor } = useAuth();

  useEffect(() => {
    fetchAppointments();
  }, []);

  const fetchAppointments = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await appointmentAPI.getAppointments();
      if (res.data?.appointments) {
        setAppointments(res.data.appointments);
      }
    } catch (err) {
      setError(err.message || 'Unable to retrieve your appointments.');
    } finally {
      setLoading(false);
    }
  };

  const handleStatusChange = async (appointmentId, newStatus) => {
    try {
      const res = await appointmentAPI.updateStatus(appointmentId, { status: newStatus });
      if (res.data?.success) {
        setActionSuccessMsg(`Appointment status updated to ${newStatus}.`);
        setTimeout(() => setActionSuccessMsg(null), 4000);
        // Refresh appointment list
        fetchAppointments();
      }
    } catch (err) {
      setError(err.message || 'Failed to update appointment.');
    }
  };

  // Filter based on active tab
  const getFilteredAppointments = () => {
    const todayStr = new Date().toISOString().split('T')[0];

    if (activeTab === 'upcoming') {
      return appointments.filter(
        (a) => a.status === 'scheduled' || a.status === 'pending'
      );
    }
    if (activeTab === 'completed') {
      return appointments.filter((a) => a.status === 'completed');
    }
    if (activeTab === 'cancelled') {
      return appointments.filter((a) => a.status === 'cancelled' || a.status === 'rejected');
    }
    return appointments;
  };

  const filteredAppointments = getFilteredAppointments();

  return (
    <div className="min-h-screen bg-slate-50 py-10">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-health-100 text-health-800 text-xs font-bold uppercase tracking-wider mb-2">
              <Calendar className="w-3.5 h-3.5" />
              Schedule Management
            </div>
            <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
              {isDoctor ? 'Doctor Consultation Schedule' : 'My Medical Appointments'}
            </h1>
          </div>

          {!isDoctor && (
            <Link
              to="/doctors"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-health-600 hover:bg-health-700 text-white font-bold text-xs sm:text-sm shadow-md transition-all active:scale-[0.98]"
            >
              <Plus className="w-4 h-4" />
              Book New Appointment
            </Link>
          )}
        </div>

        {actionSuccessMsg && (
          <div className="mb-6 p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 flex items-center gap-2.5 animate-in fade-in">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
            <span>{actionSuccessMsg}</span>
          </div>
        )}

        {/* Tab Navigation */}
        <div className="flex items-center gap-2 p-1 rounded-2xl bg-white border border-slate-200/90 shadow-sm max-w-md mb-8">
          <button
            onClick={() => setActiveTab('upcoming')}
            className={`flex-1 py-2 px-3 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-1.5 ${
              activeTab === 'upcoming'
                ? 'bg-health-600 text-white shadow-xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Clock className="w-3.5 h-3.5" />
            Upcoming
          </button>

          <button
            onClick={() => setActiveTab('completed')}
            className={`flex-1 py-2 px-3 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-1.5 ${
              activeTab === 'completed'
                ? 'bg-health-600 text-white shadow-xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <CheckCircle2 className="w-3.5 h-3.5" />
            Completed
          </button>

          <button
            onClick={() => setActiveTab('cancelled')}
            className={`flex-1 py-2 px-3 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-1.5 ${
              activeTab === 'cancelled'
                ? 'bg-health-600 text-white shadow-xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <XCircle className="w-3.5 h-3.5" />
            Cancelled
          </button>
        </div>

        {/* Content */}
        {loading ? (
          <LoadingState message="Loading your appointments..." />
        ) : error ? (
          <ErrorState message={error} onRetry={fetchAppointments} />
        ) : filteredAppointments.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredAppointments.map((appt) => (
              <AppointmentCard
                key={appt.id}
                appointment={appt}
                isDoctor={isDoctor}
                onStatusChange={handleStatusChange}
              />
            ))}
          </div>
        ) : (
          <EmptyState
            title={`No ${activeTab} appointments`}
            message={
              activeTab === 'upcoming'
                ? 'You have no pending or scheduled consultations.'
                : `No ${activeTab} consultations found in your history.`
            }
            actionText={!isDoctor && activeTab === 'upcoming' ? 'Find a Specialist' : null}
            actionLink="/doctors"
          />
        )}

      </div>
    </div>
  );
};

export default Appointments;
