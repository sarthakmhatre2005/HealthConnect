import axios from 'axios';

// Use the Vite proxy in development so the browser does not need to reach the
// Flask host directly. In production, set VITE_API_BASE_URL if the API lives
// on a separate origin; otherwise requests use the same-origin /api path.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
});

// Response interceptor for clear error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    let message = error.response?.data?.error || error.response?.data?.message;
    if (!message) {
      if (!error.response) {
        message = 'Unable to connect to HealthConnect backend.';
      } else if (error.response.status === 404) {
        message = 'Requested service was not found.';
      } else if (error.response.status === 401) {
        message = 'Please sign in to continue.';
      } else if (error.response.status === 403) {
        // The login route is public and never returns 403 in this app. A 403
        // here usually means the request was rejected by the configured API
        // host or proxy before it reached Flask, so don't present it as a
        // user permission problem.
        const requestUrl = error.config?.url || '';
        if (requestUrl.includes('/auth/login')) {
          const base = (error.config?.baseURL || '').replace(/\/+$/, '');
          const path = requestUrl.replace(/^\/+/, '');
          const target = new URL(`${base}/${path}`, window.location.origin).href;
          message = `Login request to ${target} was rejected with HTTP 403. The HealthConnect login route does not return 403; verify this URL points to the running Flask backend.`;
        } else {
          message = "You don't have permission to perform this action.";
        }
      } else if (error.response.status >= 500) {
        message = 'HealthConnect encountered a server error.';
      } else {
        message = 'An unexpected error occurred.';
      }
    }
    const customError = {
      message,
      status: error.response?.status,
      data: error.response?.data,
    };
    return Promise.reject(customError);
  }
);

// 1. AUTH API
export const authAPI = {
  login: (email, password) => apiClient.post('/auth/login', { email, password }),
  register: (userData) => apiClient.post('/auth/register', userData),
  logout: () => apiClient.post('/auth/logout'),
  getCurrentUser: () => apiClient.get('/auth/me'),
};

// 2. PATIENT API
export const patientAPI = {
  getProfile: () => apiClient.get('/patient/profile'),
  updateProfile: (profileData) => apiClient.put('/patient/profile', profileData),
  getDashboard: () => apiClient.get('/patient/dashboard'),
};

// 3. DOCTOR API
export const doctorAPI = {
  getDoctors: (params) => apiClient.get('/doctors', { params }),
  getDoctorById: (id) => apiClient.get(`/doctors/${id}`),
  getSpecializations: () => apiClient.get('/doctors/specializations'),
  getDoctorAvailability: (doctorId, date) =>
    apiClient.get('/doctor-availability', {
      params: { doctor_id: doctorId, date },
    }),
  getDashboard: () => apiClient.get('/doctor/dashboard'),
};

// 4. HOSPITAL API
export const hospitalAPI = {
  getHospitals: (params) => apiClient.get('/hospitals', { params }),
  getHospitalById: (id) => apiClient.get(`/hospitals/${id}`),
};

// 5. APPOINTMENTS API
export const appointmentAPI = {
  getAppointments: () => apiClient.get('/appointments'),
  bookAppointment: (appointmentData) => apiClient.post('/appointments', appointmentData),
  updateStatus: (appointmentId, statusData) =>
    apiClient.put(`/appointments/${appointmentId}/status`, statusData),
  cancelAppointment: (appointmentId) => apiClient.delete(`/appointments/${appointmentId}`),
};

// 6. NOTIFICATIONS API
export const notificationAPI = {
  getNotifications: () => apiClient.get('/notifications'),
  markAsRead: (notificationId) => apiClient.post(`/notifications/${notificationId}/read`),
  markAllAsRead: () => apiClient.post('/notifications/mark-all-read'),
  clearAll: () => apiClient.post('/notifications/clear-all'),
};

// 7. SYMPTOM ANALYSIS & ML API
export const symptomAPI = {
  getSymptomsList: () => apiClient.get('/symptoms/list'),
  getParameterMetadata: (symptom) => apiClient.get('/symptoms/parameters/metadata', { params: { symptom } }),
  extractNlp: (text) => apiClient.post('/symptoms/extract-nlp', { text }),
  analyzeSymptoms: (analysisData, isFormData = false) => {
    if (isFormData) {
      return apiClient.post('/symptoms/analyze', analysisData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
    }
    return apiClient.post('/symptoms/analyze', analysisData);
  },
  getHistory: () => apiClient.get('/symptoms/history'),
};

export default apiClient;
