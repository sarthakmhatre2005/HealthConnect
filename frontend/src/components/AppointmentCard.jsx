import React from 'react';
import { Calendar, Clock, MapPin, CheckCircle, XCircle, AlertCircle } from 'lucide-react';

const AppointmentCard = ({ appointment, onStatusChange, isDoctor = false }) => {
  const getStatusBadge = (status) => {
    switch (status?.toLowerCase()) {
      case 'scheduled':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
            <CheckCircle className="w-3.5 h-3.5" />
            Confirmed
          </span>
        );
      case 'completed':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200">
            <CheckCircle className="w-3.5 h-3.5" />
            Completed
          </span>
        );
      case 'cancelled':
      case 'rejected':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-600 border border-slate-200">
            <XCircle className="w-3.5 h-3.5" />
            Cancelled
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-50 text-amber-700 border border-amber-200">
            <AlertCircle className="w-3.5 h-3.5" />
            Pending Review
          </span>
        );
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-card hover:shadow-card-hover transition-all flex flex-col justify-between">
      <div>
        <div className="flex items-start justify-between gap-3 mb-3">
          <div>
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
              {isDoctor ? 'Patient Name' : 'Attending Specialist'}
            </span>
            <h4 className="text-base font-bold text-slate-900">
              {isDoctor ? appointment.patient_name : appointment.doctor_name}
            </h4>
            <p className="text-xs text-health-600 font-medium">
              {isDoctor ? (appointment.patient_phone || 'Registered Patient') : appointment.doctor_specialization}
            </p>
          </div>
          {getStatusBadge(appointment.status)}
        </div>

        {/* Reason */}
        <div className="p-3 rounded-xl bg-slate-50 border border-slate-100 text-xs text-slate-700 mb-4">
          <span className="font-semibold text-slate-500 block mb-0.5">Clinical Reason / Notes:</span>
          <p className="line-clamp-2">{appointment.reason || 'General Health Consultation'}</p>
        </div>

        {/* Date, Time, Location Grid */}
        <div className="grid grid-cols-2 gap-2 text-xs text-slate-600 py-2 border-t border-slate-100 mb-2">
          <div className="flex items-center gap-2">
            <Calendar className="w-3.5 h-3.5 text-health-600 shrink-0" />
            <span className="font-medium">{appointment.date}</span>
          </div>
          <div className="flex items-center gap-2">
            <Clock className="w-3.5 h-3.5 text-health-600 shrink-0" />
            <span className="font-medium">{appointment.formatted_time || appointment.time}</span>
          </div>
          {appointment.doctor_city && (
            <div className="col-span-2 flex items-center gap-2 text-slate-500">
              <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
              <span>{appointment.doctor_city}</span>
            </div>
          )}
        </div>
      </div>

      {/* Action buttons if scheduled */}
      {appointment.status === 'scheduled' && onStatusChange && (
        <div className="pt-3 border-t border-slate-100 mt-2 flex gap-2">
          {isDoctor ? (
            <button
              onClick={() => onStatusChange(appointment.id, 'completed')}
              className="flex-1 py-1.5 px-3 rounded-xl bg-health-600 hover:bg-health-700 text-white font-medium text-xs transition-colors"
            >
              Mark Completed
            </button>
          ) : null}

          <button
            onClick={() => onStatusChange(appointment.id, 'cancelled')}
            className="flex-1 py-1.5 px-3 rounded-xl bg-red-50 hover:bg-red-100 text-red-700 font-medium text-xs border border-red-200 transition-colors"
          >
            Cancel Appointment
          </button>
        </div>
      )}
    </div>
  );
};

export default AppointmentCard;
