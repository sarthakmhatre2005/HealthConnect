import React from 'react';
import { Link } from 'react-router-dom';
import { Stethoscope, MapPin, Calendar, Clock, Award, Phone, User } from 'lucide-react';

const DoctorCard = ({ doctor, onBook }) => {
  let availableHoursDisplay = "09:00 AM - 05:00 PM";
  if (doctor.available_hours) {
    try {
      const hours = typeof doctor.available_hours === 'string' ? JSON.parse(doctor.available_hours) : doctor.available_hours;
      if (hours.start && hours.end) {
        availableHoursDisplay = `${hours.start} - ${hours.end}`;
      }
    } catch (e) {}
  }

  return (
    <div className="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-card hover:shadow-card-hover transition-all duration-200 flex flex-col justify-between group">
      <div>
        {/* Top Header with Avatar & Specialty */}
        <div className="flex items-start gap-4 mb-4">
          <Link to={`/doctors/${doctor.id}`} className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-health-100 to-tealAccent-100 border border-health-200 flex items-center justify-center text-health-700 shrink-0 shadow-inner group-hover:scale-105 transition-transform overflow-hidden">
            <img 
              src="/assets/doctor-avatar.svg" 
              alt={doctor.name} 
              className="w-full h-full object-cover" 
            />
          </Link>
          
          <div className="min-w-0 flex-1">
            <span className="inline-block px-2.5 py-0.5 rounded-full text-xs font-semibold bg-health-50 text-health-700 border border-health-200/60 mb-1">
              {doctor.specialization}
            </span>
            <Link to={`/doctors/${doctor.id}`} className="block">
              <h3 className="text-base font-bold text-slate-900 truncate group-hover:text-health-600 transition-colors">
                {doctor.name}
              </h3>
            </Link>
            <p className="text-xs text-slate-500 flex items-center gap-1 mt-0.5">
              <Award className="w-3.5 h-3.5 text-slate-400" />
              <span>{doctor.experience_years ? `${doctor.experience_years} Years Clinical Exp.` : 'Verified Specialist'}</span>
            </p>
          </div>
        </div>

        {/* Bio */}
        <p className="text-xs text-slate-600 line-clamp-2 mb-4 leading-relaxed">
          {doctor.bio}
        </p>

        {/* Details list */}
        <div className="space-y-2 py-3 border-t border-slate-100 text-xs text-slate-600">
          <div className="flex items-center gap-2">
            <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
            <span className="truncate">{doctor.address ? `${doctor.address}, ${doctor.city}` : (doctor.city || 'Central Medical Clinic')}</span>
          </div>

          <div className="flex items-center gap-2">
            <Calendar className="w-3.5 h-3.5 text-slate-400 shrink-0" />
            <span className="truncate">Days: {doctor.available_days || 'Mon, Tue, Wed, Thu, Fri'}</span>
          </div>

          <div className="flex items-center gap-2">
            <Clock className="w-3.5 h-3.5 text-slate-400 shrink-0" />
            <span>Hours: {availableHoursDisplay}</span>
          </div>

          {doctor.phone && (
            <div className="flex items-center gap-2">
              <Phone className="w-3.5 h-3.5 text-slate-400 shrink-0" />
              <span>{doctor.phone}</span>
            </div>
          )}
        </div>
      </div>

      {/* Action Buttons: View Profile & Book Consultation */}
      <div className="pt-4 border-t border-slate-100 mt-2 flex gap-2">
        <Link
          to={`/doctors/${doctor.id}`}
          className="flex-1 flex items-center justify-center gap-1.5 px-3 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold text-xs transition-colors"
        >
          <User className="w-3.5 h-3.5" />
          View Profile
        </Link>
        <button
          onClick={() => onBook(doctor)}
          className="flex-1 flex items-center justify-center gap-1.5 px-3 py-2.5 rounded-xl bg-health-600 hover:bg-health-700 text-white font-semibold text-xs shadow-sm transition-all active:scale-[0.98]"
        >
          <Calendar className="w-3.5 h-3.5" />
          Book Now
        </button>
      </div>
    </div>
  );
};

export default DoctorCard;
