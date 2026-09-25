import React, { useState, useEffect } from 'react';
import { doctorAPI, appointmentAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';
import { 
  Stethoscope, 
  UserCheck, 
  Calendar, 
  Clock, 
  CheckCircle2, 
  XCircle, 
  Phone, 
  Award, 
  MapPin, 
  Activity,
  AlertCircle,
  FileText
} from 'lucide-react';

const DoctorDashboard = () => {
  const { user } = useAuth();
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [statusMsg, setStatusMsg] = useState(null);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await doctorAPI.getDashboard();
      if (res.data?.success) {
        setDashboardData(res.data);
      }
    } catch (err) {
      setError(err.message || 'Failed to load doctor dashboard.');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateStatus = async (appointmentId, newStatus) => {
    try {
      const res = await appointmentAPI.updateStatus(appointmentId, { status: newStatus });
      if (res.data?.success) {
        setStatusMsg(`Consultation marked as ${newStatus}.`);
        setTimeout(() => setStatusMsg(null), 4000);
        fetchDashboard();
      }
    } catch (err) {
      setError(err.message || 'Failed to update consultation status.');
    }
  };

  if (loading) {
    return <LoadingState message="Loading your clinical consultation schedule..." />;
  }

  if (error) {
    return <ErrorState message={error} onRetry={fetchDashboard} />;
  }

  const {
    doctor = {},
    today_appointments = [],
    upcoming_appointments = [],
    stats = {}
  } = dashboardData || {};

  return (
    <div className="min-h-screen bg-slate-50 py-8 lg:py-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        
        {/* Doctor Header Banner */}
        <div className="bg-gradient-to-r from-slate-900 via-health-950 to-health-900 rounded-3xl p-6 sm:p-8 text-white shadow-xl relative overflow-hidden">
          <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="flex items-start gap-4">
              <div className="w-16 h-16 rounded-2xl bg-health-600 border border-white/20 text-white flex items-center justify-center shrink-0 shadow-lg">
                <Stethoscope className="w-8 h-8" />
              </div>
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-tealAccent-500/20 text-tealAccent-300 border border-tealAccent-500/30">
                    {doctor.specialization || 'Clinical Specialist'}
                  </span>
                  <span className="text-xs text-slate-400">License: {doctor.license_number || 'REG-MED-2024'}</span>
                </div>
                <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
                  Dr. {doctor.name || user?.name}
                </h1>
                <p className="text-xs sm:text-sm text-slate-300 max-w-xl">
                  {doctor.bio || 'Dedicated medical practitioner delivering evidence-based clinical diagnostics.'}
                </p>
                <div className="flex flex-wrap items-center gap-4 text-xs text-slate-400 pt-1">
                  <span className="flex items-center gap-1">
                    <Award className="w-3.5 h-3.5 text-health-400" />
                    {doctor.experience_years || 5}+ Years Clinical Experience
                  </span>
                  <span className="flex items-center gap-1">
                    <MapPin className="w-3.5 h-3.5 text-health-400" />
                    {doctor.city || 'Central Clinic'}
                  </span>
                </div>
              </div>
            </div>

            <div className="p-4 rounded-2xl bg-white/10 backdrop-blur-md border border-white/10 text-right space-y-1">
              <span className="text-[11px] font-bold text-slate-300 uppercase tracking-wider block">Clinic Hours</span>
              <div className="text-sm font-bold text-white">Days: {doctor.available_days || 'Mon, Tue, Wed, Thu, Fri'}</div>
              <div className="text-xs text-health-300">
                Hours: {doctor.available_hours ? (typeof doctor.available_hours === 'string' ? JSON.parse(doctor.available_hours).start + ' - ' + JSON.parse(doctor.available_hours).end : '09:00 - 17:00') : '09:00 - 17:00'}
              </div>
            </div>
          </div>
        </div>

        {/* Status Message Alert */}
        {statusMsg && (
          <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-xs font-semibold text-emerald-800 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
            <span>{statusMsg}</span>
          </div>
        )}

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-5">
          <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-card">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Today's Patients</span>
              <div className="p-2 rounded-xl bg-health-50 text-health-600">
                <Clock className="w-4 h-4" />
              </div>
            </div>
            <div className="text-3xl font-extrabold text-slate-900">
              {stats.today_count || today_appointments.length}
            </div>
            <div className="text-[11px] text-slate-400 mt-1">Scheduled for today</div>
          </div>

          <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-card">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Total Consultations</span>
              <div className="p-2 rounded-xl bg-indigo-50 text-indigo-600">
                <Calendar className="w-4 h-4" />
              </div>
            </div>
            <div className="text-3xl font-extrabold text-slate-900">
              {stats.total_consultations || 0}
            </div>
            <div className="text-[11px] text-slate-400 mt-1">All recorded appointments</div>
          </div>

          <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-card">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Completed</span>
              <div className="p-2 rounded-xl bg-emerald-50 text-emerald-600">
                <CheckCircle2 className="w-4 h-4" />
              </div>
            </div>
            <div className="text-3xl font-extrabold text-slate-900">
              {stats.completed_consultations || 0}
            </div>
            <div className="text-[11px] text-slate-400 mt-1">Successfully fulfilled</div>
          </div>
        </div>

        {/* Today's Consultations List */}
        <div className="space-y-4">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Calendar className="w-4 h-4 text-health-600" />
            Today's Schedule & Consultations
          </h2>

          {today_appointments.length === 0 ? (
            <div className="bg-white rounded-2xl p-8 border border-slate-200/90 shadow-card text-center space-y-2">
              <CheckCircle2 className="w-8 h-8 text-slate-400 mx-auto" />
              <h3 className="text-sm font-bold text-slate-800">No Consultations Scheduled for Today</h3>
              <p className="text-xs text-slate-500">Upcoming appointments will appear here as patients book slots.</p>
            </div>
          ) : (
            <div className="space-y-3">
              {today_appointments.map((appt) => (
                <div
                  key={appt.id}
                  className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-card flex flex-col md:flex-row md:items-center justify-between gap-4"
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <h4 className="text-sm font-bold text-slate-900">
                        {appt.patient_name || 'Patient'}
                      </h4>
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase ${
                        appt.status === 'completed'
                          ? 'bg-emerald-50 text-emerald-700'
                          : appt.status === 'cancelled'
                          ? 'bg-red-50 text-red-700'
                          : 'bg-health-50 text-health-700'
                      }`}>
                        {appt.status}
                      </span>
                    </div>
                    <p className="text-xs text-slate-600">
                      <strong>Clinical Reason:</strong> {appt.reason}
                    </p>
                    <div className="flex items-center gap-4 text-xs text-slate-500 pt-1">
                      <span className="flex items-center gap-1 font-semibold text-slate-800">
                        <Clock className="w-3.5 h-3.5 text-health-600" />
                        {appt.formatted_time || appt.time}
                      </span>
                      {appt.patient_phone && (
                        <span className="flex items-center gap-1">
                          <Phone className="w-3.5 h-3.5 text-slate-400" />
                          {appt.patient_phone}
                        </span>
                      )}
                    </div>
                  </div>

                  {appt.status === 'scheduled' && (
                    <div className="flex items-center gap-2 shrink-0 border-t md:border-t-0 pt-3 md:pt-0 border-slate-100">
                      <button
                        onClick={() => handleUpdateStatus(appt.id, 'completed')}
                        className="px-3.5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs transition-colors flex items-center gap-1.5 shadow-sm"
                      >
                        <CheckCircle2 className="w-3.5 h-3.5" /> Mark Completed
                      </button>
                      <button
                        onClick={() => handleUpdateStatus(appt.id, 'cancelled')}
                        className="px-3 py-2 rounded-xl bg-slate-100 hover:bg-red-50 hover:text-red-700 text-slate-700 font-semibold text-xs transition-colors flex items-center gap-1.5"
                      >
                        <XCircle className="w-3.5 h-3.5" /> Cancel
                      </button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Upcoming Consultations */}
        <div className="space-y-4">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Clock className="w-4 h-4 text-health-600" />
            Upcoming Future Consultations
          </h2>

          {upcoming_appointments.length === 0 ? (
            <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-card text-center text-xs text-slate-500">
              No upcoming appointments in the schedule.
            </div>
          ) : (
            <div className="bg-white rounded-2xl border border-slate-200/90 shadow-card overflow-hidden">
              <div className="divide-y divide-slate-100">
                {upcoming_appointments.map((appt) => (
                  <div key={appt.id} className="p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:bg-slate-50/70 transition-colors">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-bold text-slate-900">{appt.patient_name}</span>
                        <span className="text-xs text-slate-400 font-mono">({appt.date})</span>
                      </div>
                      <p className="text-xs text-slate-500 mt-0.5">Reason: {appt.reason}</p>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="text-xs font-semibold text-slate-700 bg-slate-100 px-2.5 py-1 rounded-lg">
                        {appt.formatted_time || appt.time}
                      </span>
                      <span className="text-[11px] font-bold text-health-700 bg-health-50 px-2.5 py-1 rounded-full uppercase">
                        {appt.status}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

      </div>
    </div>
  );
};

export default DoctorDashboard;
