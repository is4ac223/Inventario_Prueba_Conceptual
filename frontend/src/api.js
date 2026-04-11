/**
 * API Configuration
 * This module provides the base URL for API requests
 * The URL can be set via environment variable or defaults to localhost
 */

// Get API URL from window object or environment
export const API_BASE_URL =
    typeof window !== 'undefined' && window.__API_URL__
        ? window.__API_URL__
        : (typeof process !== 'undefined' && process.env.API_URL)
            ? process.env.API_URL
            : 'http://localhost:8000/api';

export default API_BASE_URL;
