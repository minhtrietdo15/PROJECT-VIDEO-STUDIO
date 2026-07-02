import axios, { type AxiosError, type AxiosInstance } from 'axios';

/**
 * API base URL.
 * Reads from NEXT_PUBLIC_API_URL set in env.
 * Falls back to "/api" which will be proxied by Next.js to the backend.
 */
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  (typeof window === 'undefined' ? 'http://backend:8000' : '/api');

/**
 * Pre-configured Axios instance for talking to the FastAPI backend.
 *
 * Interceptors:
 *  - Request: attach Authorization header if a token is stored
 *  - Response: unwrap the { success, data, error } envelope to return `data` directly
 */
export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30_000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ---------- Request interceptor ----------
apiClient.interceptors.request.use(
  (config) => {
    if (typeof window !== 'undefined') {
      const token = window.localStorage.getItem('auth_token');
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ---------- Response interceptor ----------
export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}

export class ApiClientError extends Error {
  code: string;
  status: number;
  details?: Record<string, unknown>;

  constructor(
    message: string,
    code: string,
    status: number,
    details?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'ApiClientError';
    this.code = code;
    this.status = status;
    this.details = details;
  }
}

apiClient.interceptors.response.use(
  (response) => {
    // Unwrap { success, data, error, meta } envelope
    const body = response.data;
    if (body && typeof body === 'object' && 'success' in body) {
      if (body.success === false && body.error) {
        const err = body.error as ApiError;
        return Promise.reject(
          new ApiClientError(
            err.message,
            err.code,
            response.status,
            err.details
          )
        );
      }
      return body.data !== undefined ? body.data : body;
    }
    return body;
  },
  (error: AxiosError<{ error?: ApiError }>) => {
    if (error.response?.data?.error) {
      const err = error.response.data.error;
      return Promise.reject(
        new ApiClientError(
          err.message,
          err.code,
          error.response.status,
          err.details
        )
      );
    }
    return Promise.reject(
      new ApiClientError(
        error.message || 'Network error',
        'NETWORK_ERROR',
        error.response?.status ?? 0
      )
    );
  }
);

export default apiClient;
