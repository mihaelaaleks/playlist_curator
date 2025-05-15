import axios from './axios-interceptor';

const API_URL = 'http://localhost:8000/spotify';

export class SpotifyApiService {
    static async getPlaylists() {
        const response = await axios.get(`${API_URL}/get_playlists/me`);
        return response.data;
    }

    static async getRecommendationAttributes() {
        const response = await axios.get(`${API_URL}/get_recommendation_attributes/number_range`);
        return response.data;
    }

    static async getGenres() {
        const response = await axios.get(`${API_URL}/get_genres`);
        return response.data;
    }

    static async getRecommendations(params) {
        const response = await axios.post(`${API_URL}/curate`, params);
        return response.data;
    }

    static async createPlaylist(name, tracks) {
        const response = await axios.post(`${API_URL}/create_playlist`, {
            name,
            tracks
        });
        return response.data;
    }

    static async deletePlaylist(playlistId) {
        const response = await axios.post(`${API_URL}/delete`, {
            id: playlistId
        });
        return response.data;
    }
} 