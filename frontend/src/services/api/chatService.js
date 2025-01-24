import axiosBackend from './axiosBackend';

export const chatService = {
  createChat: async (chatData) => {
    const response = await axiosBackend.post('/chats', chatData);
    return response.data;
  },

  getChat: async (chatId) => {
    const response = await axiosBackend.get(`/chats/${chatId}`);
    return response.data;
  },

  getChatByUsername: async (username) => {
    const response = await axiosBackend.get(`/chats/u/${username}`);
    return response.data;
  },

  updateChat: async (chatId, chatData) => {
    const response = await axiosBackend.put(`/chats/${chatId}`, chatData);
    return response.data;
  },

  deleteChat: async (chatId) => {
    const response = await axiosBackend.delete(`/chats/${chatId}`);
    return response.data;
  },
}; 