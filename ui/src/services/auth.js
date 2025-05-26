//dont forget to add the VITE_SPOTIFTY_CLIENT_ID
// VITE_REDIRECT_URI to the environment
import axios from 'axios';

const AUTH_API_URL = 'http://localhost:8000/auth_spotify';
const TOKEN_STORAGE_KEY = 'spotify_token';

export class AuthService {
    static async generateCodeVerifier() {
        const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        const randomValues = crypto.getRandomValues(new Uint8Array(64));
        const randomString = randomValues.reduce((acc, x) => acc + possible[x % possible.length], "");
        return randomString;
    }

    static async generateCodeChallenge(verifier) {
        const data = new TextEncoder().encode(verifier);
        const hashed = await crypto.subtle.digest('SHA-256', data);
        
        return btoa(String.fromCharCode(...new Uint8Array(hashed)))
            .replace(/=/g, '')
            .replace(/\+/g, '-')
            .replace(/\//g, '_');
    }

    static async login() {
        try {
            // Generate PKCE code verifier and challenge
            const codeVerifier = await this.generateCodeVerifier();
            const codeChallenge = await this.generateCodeChallenge(codeVerifier);
            
            // Store code verifier for later use
            localStorage.setItem('code_verifier', codeVerifier);
            
            // Get authorization URL from backend
            const response = await axios.get(`${AUTH_API_URL}/login`, {
                params: { code_challenge: codeChallenge }
            });
            
            // Redirect to Spotify authorization page
            window.location.href = response.data.auth_url;
        } catch (error) {
            console.error('Login failed:', error);
            throw error;
        }
    }

    static async handleCallback(code) {
        try {
            const codeVerifier = localStorage.getItem('code_verifier');
            if (!codeVerifier) {
                throw new Error('No code verifier found');
            }

            // Exchange code for tokens
            const response = await axios.post(`${AUTH_API_URL}/token`, {
                code,
                code_verifier: codeVerifier
            });

            // Clear code verifier
            localStorage.removeItem('code_verifier');

            // Store tokens
            this.setTokens(response.data);

            return response.data;
        } catch (error) {
            console.error('Token exchange failed:', error);
            throw error;
        }
    }

    static async refreshToken() {
        try {
            const tokens = this.getTokens();
            if (!tokens?.refresh_token) {
                throw new Error('No refresh token available');
            }

            const response = await axios.post(`${AUTH_API_URL}/refresh`, {
                refresh_token: tokens.refresh_token
            });

            this.setTokens(response.data);
            return response.data;
        } catch (error) {
            console.error('Token refresh failed:', error);
            throw error;
        }
    }

    static setTokens(tokens) {
        const { access_token, refresh_token, expires_in } = tokens;
        const now = new Date();
        const expires = new Date(now.getTime() + (expires_in * 1000));
        
        localStorage.setItem(TOKEN_STORAGE_KEY, JSON.stringify({
            access_token,
            refresh_token,
            expires_in,
            expires
        }));
    }

    static getTokens() {
        const tokens = localStorage.getItem(TOKEN_STORAGE_KEY);
        return tokens ? JSON.parse(tokens) : null;
    }

    static isAuthenticated() {
        const tokens = this.getTokens();
        if (!tokens) return false;
        
        const expires = new Date(tokens.expires);
        return tokens && expires > new Date();
    }

    static logout() {
        localStorage.removeItem(TOKEN_STORAGE_KEY);
        localStorage.removeItem('code_verifier');
    }
} 