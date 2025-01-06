import axios from "axios";
import { API_URL } from "../config";

const axiosBackend = axios.create({
    baseURL: API_URL,
    headers: {
        "Content-Type": "application/json",
    },
});

export const api = {
    makeRequest: async (method, url, data, options) => {
        return axiosBackend.request({
            method: method,
            url: url,
            data: data,
            ...options,
        });
    },
    login: async (credentials, login_type = "tg_login_widget") => {        
        const response = await api.makeRequest("post", "/auth/login", {
            credentials: credentials,
            login_type: login_type
        });
        return response.data;
    },
    
    getProfile: async (userId) => {
        const response = await api.makeRequest("get", `/auth/profile?user_id=${userId}`);
        return response.data;
    }
}

export default api;