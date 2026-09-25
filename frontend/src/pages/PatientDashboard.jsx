import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { patientAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import SeverityBadge from '../components/SeverityBadge';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';
import EmptyState from '../components/EmptyState';
import { 
  Stethoscope, 
  UserCheck, 
  Building2, 
  Calendar, 
  Activity, 
  Bell, 
  Clock, 
  CheckCircle2, 
  ArrowRight, 
  ChevronRight,
  Sparkles,
  AlertTriangle,
  User,
  HeartPulse
} from 'lucide-react';

const PatientDashboard = () => {
  const { user } = useAuth();
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await patientAPI.getDashboard();
      if (res.data?.success) {
        setDashboardData(res.data);
      }
    } catch (err) {
      setError(err.message || 'Failed to load patient dashboard.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingState message="Loading your personalized healthcare dashboard..." />;
  }

  if (error) {
    return <ErrorState message={error} onRetry={fetchDashboard} />;
  }

  const {
    patient = {},
    upcoming_appointments = [],
    recent_symptom_checks = [],
    unread_notifications = 0,
    stats = {}
  } = dashboardData || {};

  return (
    <div className="min-h-screen bg-slate-50 py-8 lg:py-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        
        {/* Welcome Header */}
        <div className="bg-gradient-to-r from-health-900 via-health-800 to-slate-900 rounded-3xl p-6 sm:p-8 text-white shadow-xl relative overflow-hidden">
          {/* Subtle Background Glows */}
          <div className="absolute -right-10 -bottom-10 w-80 h-80 bg-tealAccent-500/10 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute top-0 right-1/4 w-60 h-60 bg-health-400/10 rounded-full blur-2xl pointer-events-none" />

          <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="space-y-2">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 text-health-300 text-xs font-semibold backdrop-blur-sm border border-white/15">
                <Sparkles className="w-3.5 h-3.5 text-tealAccent-400" />
                <span>Patient Health Portal</span>
              </div>
              <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight">
                Welcome back, {user?.name || 'Patient'}
              </h1>
              <p className="text-slate-300 text-xs sm:text-sm max-w-xl leading-relaxed">
                Track your health consultations, run AI-assisted symptom triage, and coordinate with verified medical specialists.
              </p>
            </div>

            <div className="flex flex-wrap gap-3 shrink-0">
              <Link
                to="/symptom-checker"
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-health-500 to-tealAccent-600 hover:from-health-600 hover:to-tealAccent-700 text-white font-bold text-xs sm:text-sm shadow-md transition-all active:scale-95"
              >
                <Stethoscope className="w-4 h-4" />
                Check Symptoms
              </Link>
              <Link
                to="/doctors"
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-white/10 hover:bg-white/15 text-white font-semibold text-xs sm:text-sm border border-white/20 backdrop-blur-sm transition-all"
              >
                <UserCheck className="w-4 h-4 text-health-300" />
                Find Doctor
              </Link>
            </div>
          </div>
        </div>

        {/* Quick Metrics Bar */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
          <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-card">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Appointments</span>
              <div className="p-2 rounded-xl bg-health-50 text-health-600">
                <Calendar className="w-4 h-4" />
              </div>
            </div>
            <div className="text-2xl sm:text-3xl font-extrabold text-slate-900">
              {stats.total_appointments || 0}
            </div>
            <div className="text-[11px] text-slate-400 mt-1 flex items-center gap-1">
              <span>Scheduled: {upcoming_appointments.length}</span>
            </div>
          </div>

          <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-card">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Completed</span>
              <div className="p-2 rounded-xl bg-emerald-50 text-emerald-600">
                <CheckCircle2 className="w-4 h-4" />
              </div>
            </div>
            <div className="text-2xl sm:text-3xl font-extrabold text-slate-900">
              {stats.completed_appointments || 0}
            </div>
            <div className="text-[11px] text-slate-400 mt-1">Consultations finished</div>
          </div>

          <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-card">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Health Checks</span>
              <div className="p-2 rounded-xl bg-tealAccent-50 text-tealAccent-600">
                <Activity className="w-4 h-4" />
              </div>
            </div>
            <div className="text-2xl sm:text-3xl font-extrabold text-slate-900">
              {stats.total_health_checks || 0}
            </div>
            <div className="text-[11px] text-slate-400 mt-1">Local ML analyses run</div>
          </div>

          <div className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-card">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Notifications</span>
              <div className="p-2 rounded-xl bg-amber-50 text-amber-600">
                <Bell className="w-4 h-4" />
              </div>
            </div>
            <div className="text-2xl sm:text-3xl font-extrabold text-slate-900">
              {unread_notifications}
            </div>
            <div className="text-[11px] text-slate-400 mt-1">
              <Link to="/notifications" className="text-health-600 hover:underline">
                View notification center
              </Link>
            </div>
          </div>
        </div>

        {/* Quick Action Navigation Grid */}
        <div>
          <h2 className="text-base font-bold text-slate-900 mb-4 flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-health-600" />
            Quick Health Services
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            
            <Link
              to="/symptom-checker"
              className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-card hover:shadow-card-hover hover:border-health-300 transition-all duration-200 group flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="w-10 h-10 rounded-xl bg-health-100 text-health-700 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <Stethoscope className="w-5 h-5" />
                </div>
                <h3 className="text-sm font-bold text-slate-900 group-hover:text-health-600 transition-colors">
                  AI Symptom Checker
                </h3>
                <p className="text-xs text-slate-500 leading-relaxed">
                  Get preliminary health insights from your symptoms with intelligent analysis.
                </p>
              </div>
              <div className="pt-4 mt-2 text-xs font-bold text-health-600 flex items-center gap-1">
                <span>Start Health Check</span>
                <ChevronRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
              </div>
            </Link>

            <Link
              to="/doctors"
              className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-card hover:shadow-card-hover hover:border-health-300 transition-all duration-200 group flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="w-10 h-10 rounded-xl bg-tealAccent-100 text-tealAccent-700 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <UserCheck className="w-5 h-5" />
                </div>
                <h3 className="text-sm font-bold text-slate-900 group-hover:text-health-600 transition-colors">
                  Find Specialists
                </h3>
                <p className="text-xs text-slate-500 leading-relaxed">
                  Browse cardiologists, dermatologists, neurologists, and general physicians.
                </p>
              </div>
              <div className="pt-4 mt-2 text-xs font-bold text-tealAccent-600 flex items-center gap-1">
                <span>Discover Doctors</span>
                <ChevronRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
              </div>
            </Link>

            <Link
              to="/hospitals"
              className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-card hover:shadow-card-hover hover:border-health-300 transition-all duration-200 group flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="w-10 h-10 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <Building2 className="w-5 h-5" />
                </div>
                <h3 className="text-sm font-bold text-slate-900 group-hover:text-health-600 transition-colors">
                  Emergency Hospitals
                </h3>
                <p className="text-xs text-slate-500 leading-relaxed">
                  Locate accredited hospitals, trauma centers, and 24x7 emergency medical units.
                </p>
              </div>
              <div className="pt-4 mt-2 text-xs font-bold text-blue-600 flex items-center gap-1">
                <span>Locate Centers</span>
                <ChevronRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
              </div>
            </Link>

            <Link
              to="/appointments"
              className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-card hover:shadow-card-hover hover:border-health-300 transition-all duration-200 group flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="w-10 h-10 rounded-xl bg-indigo-100 text-indigo-700 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <Calendar className="w-5 h-5" />
                </div>
                <h3 className="text-sm font-bold text-slate-900 group-hover:text-health-600 transition-colors">
                  My Consultations
                </h3>
                <p className="text-xs text-slate-500 leading-relaxed">
                  Manage confirmed appointments, view consultation slots, or cancel visits.
                </p>
              </div>
              <div className="pt-4 mt-2 text-xs font-bold text-indigo-600 flex items-center gap-1">
                <span>View Schedule</span>
                <ChevronRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
              </div>
            </Link>

          </div>
        </div>

        {/* Main 2-Column Content: Upcoming Appointments & Recent Health Analyses */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Upcoming Appointments Column */}
          <div className="lg:col-span-7 space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <Calendar className="w-4 h-4 text-health-600" />
                Upcoming Consultations
              </h2>
              <Link to="/appointments" className="text-xs font-semibold text-health-600 hover:text-health-700">
                View all ({upcoming_appointments.length})
              </Link>
            </div>

            {upcoming_appointments.length === 0 ? (
              <div className="bg-white rounded-2xl p-8 border border-slate-200/90 shadow-card text-center space-y-3">
                <div className="w-12 h-12 rounded-2xl bg-slate-100 text-slate-400 flex items-center justify-center mx-auto">
                  <Calendar className="w-6 h-6" />
                </div>
                <h3 className="text-sm font-bold text-slate-800">No Upcoming Appointments</h3>
                <p className="text-xs text-slate-500 max-w-sm mx-auto">
                  You do not have any pending or scheduled consultations with specialists.
                </p>
                <div className="pt-2">
                  <Link
                    to="/doctors"
                    className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-health-600 hover:bg-health-700 text-white font-semibold text-xs transition-colors"
                  >
                    <UserCheck className="w-3.5 h-3.5" /> Book a Consultation
                  </Link>
                </div>
              </div>
            ) : (
              <div className="space-y-3">
                {upcoming_appointments.map((appt) => (
                  <div
                    key={appt.id}
                    className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-card hover:shadow-card-hover transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4"
                  >
                    <div className="flex items-start gap-3.5">
                      <div className="w-11 h-11 rounded-xl bg-health-50 border border-health-200 text-health-700 flex items-center justify-center shrink-0 font-bold">
                        <Stethoscope className="w-5 h-5" />
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <h4 className="text-sm font-bold text-slate-900">
                            Dr. {appt.doctor_name}
                          </h4>
                          <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-health-100 text-health-800">
                            {appt.doctor_specialization}
                          </span>
                        </div>
                        <p className="text-xs text-slate-500 mt-1 line-clamp-1">
                          Reason: {appt.reason}
                        </p>
                        <div className="flex items-center gap-3 text-xs text-slate-600 mt-2">
                          <span className="flex items-center gap-1 font-medium">
                            <Clock className="w-3.5 h-3.5 text-slate-400" />
                            {appt.date} at {appt.formatted_time || appt.time}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="flex sm:flex-col items-center sm:items-end justify-between gap-2 border-t sm:border-t-0 pt-3 sm:pt-0 border-slate-100">
                      <span className={`px-2.5 py-1 rounded-full text-[11px] font-bold capitalize ${
                        appt.status === 'scheduled'
                          ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                          : 'bg-amber-50 text-amber-700 border border-amber-200'
                      }`}>
                        {appt.status}
                      </span>
                      <Link
                        to="/appointments"
                        className="text-xs font-semibold text-health-600 hover:underline"
                      >
                        Manage Details
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Recent Symptom Analyses Column */}
          <div className="lg:col-span-5 space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <HeartPulse className="w-4 h-4 text-health-600" />
                Recent Health Checks
              </h2>
              <Link to="/symptom-checker" className="text-xs font-semibold text-health-600 hover:text-health-700">
                New Check
              </Link>
            </div>

            {recent_symptom_checks.length === 0 ? (
              <div className="bg-white rounded-2xl p-8 border border-slate-200/90 shadow-card text-center space-y-3">
                <div className="w-12 h-12 rounded-2xl bg-slate-100 text-slate-400 flex items-center justify-center mx-auto">
                  <Activity className="w-6 h-6" />
                </div>
                <h3 className="text-sm font-bold text-slate-800">No Past Analyses</h3>
                <p className="text-xs text-slate-500 max-w-xs mx-auto">
                  Use the ML symptom triage tool to check clinical indicators and receive preliminary insights.
                </p>
                <div className="pt-2">
                  <Link
                    to="/symptom-checker"
                    className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-health-600 hover:bg-health-700 text-white font-semibold text-xs transition-colors"
                  >
                    <Stethoscope className="w-3.5 h-3.5" /> Check Symptoms Now
                  </Link>
                </div>
              </div>
            ) : (
              <div className="space-y-3">
                {recent_symptom_checks.map((check) => {
                  const topCondition = check.analysis?.top_condition || 'Clinical Assessment';
                  const conf = check.analysis?.confidence_percent || 0;
                  const specialist = check.analysis?.specialist || 'General Physician';
                  
                  return (
                    <div
                      key={check.id}
                      className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-card hover:shadow-card-hover transition-all space-y-3"
                    >
                      <div className="flex items-start justify-between gap-2">
                        <div>
                          <span className="text-[11px] text-slate-400 block mb-0.5">
                            {check.formatted_date}
                          </span>
                          <h4 className="text-sm font-bold text-slate-900">
                            {topCondition}
                          </h4>
                        </div>
                        <SeverityBadge severity={check.severity} size="sm" />
                      </div>

                      <div className="flex flex-wrap gap-1">
                        {(check.symptoms || []).slice(0, 3).map((sym, idx) => (
                          <span
                            key={idx}
                            className="px-2 py-0.5 rounded-md text-[10px] font-medium bg-slate-100 text-slate-700"
                          >
                            {sym}
                          </span>
                        ))}
                        {(check.symptoms || []).length > 3 && (
                          <span className="px-2 py-0.5 rounded-md text-[10px] font-medium bg-slate-50 text-slate-400">
                            +{(check.symptoms || []).length - 3} more
                          </span>
                        )}
                      </div>

                      <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs">
                        <span className="text-slate-500">
                          Rec. Specialist: <strong className="text-slate-800 font-semibold">{specialist}</strong>
                        </span>
                        <Link
                          to={`/doctors?specialization=${encodeURIComponent(specialist)}`}
                          className="text-health-600 font-bold hover:underline flex items-center gap-0.5"
                        >
                          Find {specialist} <ArrowRight className="w-3 h-3" />
                        </Link>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

        </div>

      </div>
    </div>
  );
};

export default PatientDashboard;
