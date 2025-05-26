<template>
  <div class="login-container">
    <h1>Welcome to Playlist Curator</h1>
    <button @click="login" class="login-button" :disabled="loading">
      {{ loading ? 'Logging in...' : 'Login with Spotify' }}
    </button>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { AuthService } from '../services/auth';

export default {
  name: 'Login',
  setup() {
    const router = useRouter();
    const loading = ref(false);

    onMounted(() => {
      // Check if we're handling a callback from Spotify
      const urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get('code');
      const error = urlParams.get('error');

      if (code) {
        handleCallback(code);
      } else if (error) {
        console.error('Authentication error:', error);
      }
    });

    const login = async () => {
      loading.value = true;
      try {
        await AuthService.login();
      } catch (error) {
        console.error('Login failed:', error);
        loading.value = false;
      }
    };

    const handleCallback = async (code) => {
      loading.value = true;
      try {
        await AuthService.handleCallback(code);
        // Redirect to curator page after successful login
        router.push('/curator');
      } catch (error) {
        console.error('Failed to handle callback:', error);
      } finally {
        loading.value = false;
      }
    };

    return {
      loading,
      login
    };
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #121212;
  color: white;
}

.login-button {
  background-color: #1DB954;
  color: white;
  border: none;
  border-radius: 500px;
  padding: 16px 48px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 24px;
}

.login-button:hover:not(:disabled) {
  transform: scale(1.04);
  background-color: #1ed760;
}

.login-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style> 