import axiosBackend from './axiosBackend';

export const userService = {
  getCurrentUser: async () => {
    const response = await axiosBackend.get('/users/me');
    return response.data;
  },
}; 