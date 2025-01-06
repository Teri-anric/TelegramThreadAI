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
    login: async (user) => {
        return {status: 200, ...JSON.parse(user)} // TODO: remove this
        return api.makeRequest("post", "/login", user);
    },
    logout: async () => {
        return true; // TODO: remove this
        return api.makeRequest("post", "/logout");
    },
    getProfile: async () => {
        return {status: 200, ...JSON.parse(user)} // TODO: remove this
        return api.makeRequest("get", "/profile");  
    }
}

export default api;