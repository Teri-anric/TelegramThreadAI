import axiosBackend from './axiosBackend';

export const authService = {
  loginByTelegramWidget: async (credentials) => {
    return this.login(credentials, 'tg_login_widget');
  },

  login: async (credentials, login_type) => {
    try {
      const response = await axiosBackend.post('/auth/login', {
        login_type,
        credentials,
      });
      
      // Store access token
      if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
      }
      
      return response.data;
    } catch (error) {
      console.error('Login failed', error);
      throw error;
    }
  },

  logout: () => {
    localStorage.removeItem('access_token');
  },
}; 