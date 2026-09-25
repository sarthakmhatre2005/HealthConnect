import React, { useState, useEffect } from 'react';
import { notificationAPI } from '../services/api';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';
import { 
  Bell, 
  CheckCheck, 
  Trash2, 
  Calendar, 
  Activity, 
  Info, 
  Sparkles,
  CheckCircle2,
  Clock
} from 'lucide-react';

const Notifications = () => {
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [statusMsg, setStatusMsg] = useState(null);

  useEffect(() => {
    fetchNotifications();
  }, []);

  const fetchNotifications = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await notificationAPI.getNotifications();
      if (res.data?.notifications) {
        setNotifications(res.data.notifications);
        setUnreadCount(res.data.unread_count || 0);
      }
    } catch (err) {
      setError(err.message || 'Failed to load notifications.');
    } finally {
      setLoading(false);
    }
  };

  const handleMarkAsRead = async (id) => {
    try {
      await notificationAPI.markAsRead(id);
      setNotifications((prev) =>
        prev.map((n) => (n.id === id ? { ...n, read: true } : n))
      );
      setUnreadCount((prev) => Math.max(0, prev - 1));
    } catch (e) {
      console.error('Error marking as read:', e);
    }
  };

  const handleMarkAllAsRead = async () => {
    try {
      await notificationAPI.markAllAsRead();
      setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));
      setUnreadCount(0);
      setStatusMsg('All notifications marked as read.');
      setTimeout(() => setStatusMsg(null), 3000);
    } catch (e) {
      console.error('Error marking all read:', e);
    }
  };

  const handleClearAll = async () => {
    if (!window.confirm('Are you sure you want to clear all notifications?')) return;
    try {
      await notificationAPI.clearAll();
      setNotifications([]);
      setUnreadCount(0);
      setStatusMsg('All notifications cleared.');
      setTimeout(() => setStatusMsg(null), 3000);
    } catch (e) {
      console.error('Error clearing notifications:', e);
    }
  };

  const getIcon = (type) => {
    switch (type) {
      case 'appointment':
        return <Calendar className="w-5 h-5 text-health-600" />;
      case 'symptom_check':
        return <Activity className="w-5 h-5 text-tealAccent-600" />;
      default:
        return <Sparkles className="w-5 h-5 text-indigo-600" />;
    }
  };

  if (loading) {
    return <LoadingState message="Loading your notifications..." />;
  }

  if (error) {
    return <ErrorState message={error} onRetry={fetchNotifications} />;
  }

  return (
    <div className="min-h-screen bg-slate-50 py-10">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
        
        {/* Header Bar */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-health-100 text-health-800 text-xs font-bold uppercase tracking-wider mb-2">
              <Bell className="w-3.5 h-3.5" />
              Notification Center
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight flex items-center gap-3">
              Notifications
              {unreadCount > 0 && (
                <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-health-600 text-white shadow-sm">
                  {unreadCount} New
                </span>
              )}
            </h1>
          </div>

          {/* Action Buttons */}
          {notifications.length > 0 && (
            <div className="flex items-center gap-2">
              {unreadCount > 0 && (
                <button
                  onClick={handleMarkAllAsRead}
                  className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-white border border-slate-200 text-slate-700 hover:text-health-700 hover:border-health-300 text-xs font-semibold shadow-xs transition-all"
                >
                  <CheckCheck className="w-4 h-4 text-health-600" />
                  Mark All Read
                </button>
              )}
              <button
                onClick={handleClearAll}
                className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-white border border-slate-200 text-slate-700 hover:text-red-700 hover:border-red-300 text-xs font-semibold shadow-xs transition-all"
              >
                <Trash2 className="w-4 h-4 text-red-500" />
                Clear All
              </button>
            </div>
          )}
        </div>

        {/* Feedback message */}
        {statusMsg && (
          <div className="p-3.5 rounded-2xl bg-emerald-50 border border-emerald-200 text-xs font-semibold text-emerald-800 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span>{statusMsg}</span>
          </div>
        )}

        {/* Notifications List */}
        {notifications.length === 0 ? (
          <div className="bg-white rounded-3xl p-12 border border-slate-200/90 shadow-card text-center space-y-3">
            <div className="w-14 h-14 rounded-2xl bg-slate-100 text-slate-400 flex items-center justify-center mx-auto">
              <Bell className="w-7 h-7" />
            </div>
            <h3 className="text-base font-bold text-slate-800">You're All Caught Up</h3>
            <p className="text-xs text-slate-500 max-w-sm mx-auto leading-relaxed">
              No new notifications right now. System alerts, confirmed consultation reminders, and AI health check records will appear here.
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {notifications.map((notif) => (
              <div
                key={notif.id}
                className={`bg-white rounded-2xl p-5 border transition-all duration-200 flex items-start justify-between gap-4 ${
                  !notif.read
                    ? 'border-health-300 shadow-md bg-gradient-to-r from-health-50/40 via-white to-white ring-1 ring-health-200'
                    : 'border-slate-200/90 shadow-card opacity-90'
                }`}
              >
                <div className="flex items-start gap-4">
                  <div className={`p-2.5 rounded-xl shrink-0 ${
                    !notif.read ? 'bg-health-100 ring-2 ring-health-200' : 'bg-slate-100'
                  }`}>
                    {getIcon(notif.notification_type)}
                  </div>
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <h4 className={`text-sm font-bold ${!notif.read ? 'text-slate-900 font-extrabold' : 'text-slate-800'}`}>
                        {notif.title}
                      </h4>
                      {!notif.read && (
                        <span className="w-2 h-2 rounded-full bg-health-600 animate-pulse" />
                      )}
                    </div>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      {notif.message}
                    </p>
                    <div className="text-[11px] text-slate-400 flex items-center gap-1 pt-1">
                      <Clock className="w-3 h-3" />
                      <span>{notif.formatted_date || 'Recently'}</span>
                    </div>
                  </div>
                </div>

                {!notif.read && (
                  <button
                    onClick={() => handleMarkAsRead(notif.id)}
                    className="shrink-0 p-1.5 rounded-lg text-slate-400 hover:text-health-600 hover:bg-health-50 transition-colors"
                    title="Mark as read"
                  >
                    <CheckCircle2 className="w-4 h-4" />
                  </button>
                )}
              </div>
            ))}
          </div>
        )}

      </div>
    </div>
  );
};

export default Notifications;
