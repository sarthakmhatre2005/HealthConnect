import React, { useState, useEffect } from 'react';
import { doctorAPI, appointmentAPI } from '../services/api';
import { X, Calendar, Clock, AlertCircle, CheckCircle, Stethoscope } from 'lucide-react';

const BookAppointmentModal = ({ doctor, isOpen, onClose, onSuccess }) => {
  // Default tomorrow's date
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  const defaultDateStr = tomorrow.toISOString().split('T')[0];

  const [date, setDate] = useState(defaultDateStr);
  const [selectedSlot, setSelectedSlot] = useState('');
  const [availableSlots, setAvailableSlots] = useState([]);
  const [reason, setReason] = useState('Routine Medical Consultation');
  const [loadingSlots, setLoadingSlots] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [successMsg, setSuccessMsg] = useState(null);

  useEffect(() => {
    if (isOpen && doctor?.id && date) {
      fetchAvailability();
    }
  }, [isOpen, doctor?.id, date]);

  const fetchAvailability = async () => {
    setLoadingSlots(true);
    setError(null);
    setSelectedSlot('');
    try {
      const res = await doctorAPI.getDoctorAvailability(doctor.id, date);
      if (res.data?.available && res.data?.available_slots) {
        setAvailableSlots(res.data.available_slots);
        if (res.data.available_slots.length > 0) {
          setSelectedSlot(res.data.available_slots[0].value);
        }
      } else {
        setAvailableSlots([]);
        setError(res.data?.message || 'No consultation slots available on this date.');
      }
    } catch (e) {
      setAvailableSlots([]);
      setError('Could not retrieve slot availability. Please try another date.');
    } finally {
      setLoadingSlots(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedSlot) {
      setError('Please select an available consultation time slot.');
      return;
    }

    setSubmitting(true);
    setError(null);
    try {
      const res = await appointmentAPI.bookAppointment({
        doctor_id: doctor.id,
        date: date,
        time: selectedSlot,
        reason: reason,
      });

      if (res.data?.success) {
        setSuccessMsg('Appointment booked successfully!');
        setTimeout(() => {
          if (onSuccess) onSuccess(res.data.appointment);
          onClose();
        }, 1200);
      }
    } catch (err) {
      setError(err.message || 'Failed to book appointment. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  if (!isOpen || !doctor) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl border border-slate-200 animate-in fade-in zoom-in-95 relative">
        
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-full text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Header */}
        <div className="flex items-center gap-3 mb-5 pr-8">
          <div className="w-12 h-12 rounded-2xl bg-health-50 border border-health-200 flex items-center justify-center text-health-600 shrink-0">
            <Stethoscope className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-slate-900 leading-tight">
              Book Appointment
            </h3>
            <p className="text-xs text-slate-500">
              {doctor.name} • <span className="text-health-600 font-semibold">{doctor.specialization}</span>
            </p>
          </div>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-xl bg-red-50 border border-red-200 text-xs text-red-700 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {successMsg && (
          <div className="mb-4 p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-700 flex items-center gap-2">
            <CheckCircle className="w-4 h-4 shrink-0" />
            <span>{successMsg}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          
          {/* Select Date */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
              Consultation Date
            </label>
            <div className="relative">
              <input
                type="date"
                min={new Date().toISOString().split('T')[0]}
                value={date}
                onChange={(e) => setDate(e.target.value)}
                required
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-slate-900 text-sm focus:ring-2 focus:ring-health-500 focus:border-health-500 outline-none"
              />
            </div>
          </div>

          {/* Time Slot Selector */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5 flex items-center justify-between">
              <span>Available Time Slots</span>
              {loadingSlots && <span className="text-slate-400 font-normal lowercase">checking slots...</span>}
            </label>

            {loadingSlots ? (
              <div className="py-6 text-center text-xs text-slate-400">Loading doctor schedule...</div>
            ) : availableSlots.length > 0 ? (
              <div className="grid grid-cols-3 gap-2 max-h-40 overflow-y-auto p-1">
                {availableSlots.map((slot) => (
                  <button
                    key={slot.value}
                    type="button"
                    onClick={() => setSelectedSlot(slot.value)}
                    className={`py-2 px-2.5 rounded-xl text-xs font-semibold transition-all border ${
                      selectedSlot === slot.value
                        ? 'bg-health-600 text-white border-health-600 shadow-sm'
                        : 'bg-slate-50 hover:bg-slate-100 text-slate-700 border-slate-200'
                    }`}
                  >
                    {slot.display}
                  </button>
                ))}
              </div>
            ) : (
              <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 text-xs text-amber-800 text-center">
                No slots available on this day. Please select another date.
              </div>
            )}
          </div>

          {/* Consultation Reason */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
              Reason / Chief Complaint
            </label>
            <textarea
              rows="2"
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              placeholder="E.g., Follow-up on persistent headache, routine heart checkup..."
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-slate-900 text-sm focus:ring-2 focus:ring-health-500 focus:border-health-500 outline-none"
            />
          </div>

          {/* Action Buttons */}
          <div className="pt-3 flex items-center gap-3 border-t border-slate-100">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 py-2.5 px-4 rounded-xl text-sm font-semibold text-slate-600 hover:bg-slate-100 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting || !selectedSlot || loadingSlots}
              className="flex-1 py-2.5 px-4 rounded-xl text-sm font-semibold text-white bg-health-600 hover:bg-health-700 disabled:opacity-50 shadow-md transition-all active:scale-[0.98]"
            >
              {submitting ? 'Confirming...' : 'Confirm Booking'}
            </button>
          </div>

        </form>

      </div>
    </div>
  );
};

export default BookAppointmentModal;
