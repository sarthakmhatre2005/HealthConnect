import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Activity } from 'lucide-react';

const ProtectedRoute = ({ children, requiredRole = null }) => {
  const { user, loading, isAuthenticated } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center p-6 text-center">
        <div className="w-12 h-12 rounded-2xl bg-health-50 border border-health-200 flex items-center justify-center text-health-600 animate-pulse mb-3">
          <Activity className="w-6 h-6 animate-spin" />
        </div>
        <p className="text-sm font-medium text-slate-600">Verifying session credentials...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (requiredRole && user?.user_type !== requiredRole) {
    // Redirect to proper dashboard based on actual role
    return <Navigate to={user?.user_type === 'doctor' ? '/doctor/dashboard' : '/dashboard'} replace />;
  }

  return children;
};

export default ProtectedRoute;
