import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/accounts/token/refresh/`, {
            refresh: refreshToken,
          });
          
          const { access } = response.data;
          localStorage.setItem('access_token', access);
          
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/accounts/login/', credentials),
  register: (userData) => api.post('/accounts/register/', userData),
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  },
  getProfile: () => api.get('/accounts/profile/'),
  updateProfile: (data) => api.patch('/accounts/profile/', data),
  changePassword: (data) => api.post('/accounts/change-password/', data),
};

// Patients API
export const patientsAPI = {
  getPatients: (params) => api.get('/patients/', { params }),
  getPatient: (id) => api.get(`/patients/${id}/`),
  createPatient: (data) => api.post('/patients/', data),
  updatePatient: (id, data) => api.patch(`/patients/${id}/`, data),
  deletePatient: (id) => api.delete(`/patients/${id}/`),
  getProfile: () => api.get('/patients/profile/'),
  getStats: () => api.get('/patients/stats/'),
};

// Doctors API
export const doctorsAPI = {
  getDoctors: (params) => api.get('/doctors/', { params }),
  getDoctor: (id) => api.get(`/doctors/${id}/`),
  createDoctor: (data) => api.post('/doctors/', data),
  updateDoctor: (id, data) => api.patch(`/doctors/${id}/`, data),
  deleteDoctor: (id) => api.delete(`/doctors/${id}/`),
  getProfile: () => api.get('/doctors/profile/'),
  getAvailableDoctors: (params) => api.get('/doctors/available/', { params }),
  getDoctorsBySpecialization: (specialization, params) => 
    api.get(`/doctors/specialization/${specialization}/`, { params }),
  getStats: () => api.get('/doctors/stats/'),
};

// Appointments API
export const appointmentsAPI = {
  getAppointments: (params) => api.get('/appointments/', { params }),
  getAppointment: (id) => api.get(`/appointments/${id}/`),
  createAppointment: (data) => api.post('/appointments/', data),
  updateAppointment: (id, data) => api.patch(`/appointments/${id}/`, data),
  deleteAppointment: (id) => api.delete(`/appointments/${id}/`),
  acceptAppointment: (id) => api.post(`/appointments/${id}/accept/`),
  rejectAppointment: (id, data) => api.post(`/appointments/${id}/reject/`, data),
  completeAppointment: (id, data) => api.post(`/appointments/${id}/complete/`, data),
  getDoctorAppointments: (params) => api.get('/appointments/doctor/', { params }),
  getPatientAppointments: (params) => api.get('/appointments/patient/', { params }),
  getStats: () => api.get('/appointments/stats/'),
};

// Reviews API
export const reviewsAPI = {
  getReviews: (params) => api.get('/appointments/reviews/', { params }),
  createReview: (data) => api.post('/appointments/reviews/', data),
  getDoctorReviews: (doctorId, params) => 
    api.get(`/appointments/reviews/doctor/${doctorId}/`, { params }),
};

// Chat API
export const chatAPI = {
  getChatRooms: (params) => api.get('/chat/rooms/', { params }),
  getChatRoom: (id) => api.get(`/chat/rooms/${id}/`),
  createChatRoom: (data) => api.post('/chat/rooms/', data),
  getMessages: (chatRoomId, params) => 
    api.get(`/chat/rooms/${chatRoomId}/messages/`, { params }),
  sendMessage: (chatRoomId, data) => 
    api.post(`/chat/rooms/${chatRoomId}/messages/`, data),
  markMessagesRead: (chatRoomId) => 
    api.post(`/chat/rooms/${chatRoomId}/mark-read/`),
};

// Users API (Admin only)
export const usersAPI = {
  getUsers: (params) => api.get('/accounts/users/', { params }),
  getUser: (id) => api.get(`/accounts/users/${id}/`),
  updateUser: (id, data) => api.patch(`/accounts/users/${id}/`, data),
  deleteUser: (id) => api.delete(`/accounts/users/${id}/`),
  getStats: () => api.get('/accounts/stats/'),
};

export default api;