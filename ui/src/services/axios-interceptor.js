import axios from 'axios';
import { AuthService } from './auth';

// Create axios instance
const axiosInstance = axios.create();

// Request interceptor
axiosInstance.interceptors.request.use(
    async config => {
        if (AuthService.isAuthenticated()) {
            const tokens = AuthService.getTokens();
            config.headers.Authorization = `Bearer ${tokens.access_token}`;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

// Response interceptor
axiosInstance.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config;

        // If the error is 401 and we haven't already tried to refresh the token
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                // Try to refresh the token
                const tokens = await AuthService.refreshToken();
                
                // Update the request with the new token
                originalRequest.headers.Authorization = `Bearer ${tokens.access_token}`;
                
                // Retry the original request
                return axiosInstance(originalRequest);
            } catch (refreshError) {
                // If refresh fails, logout and redirect to login page
                AuthService.logout();
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export default axiosInstance; 