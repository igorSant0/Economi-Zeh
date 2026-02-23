import axios from "axios";

const baseURL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const api = axios.create({
    baseURL,
    headers: {
        "Content-Type": "application/json",
    },
});

// Interceptor de requisição
api.interceptors.request.use(
    (config) => {
        // Futuramente, adicione o token aqui se necessário
        // const token = localStorage.getItem("token");
        // if (token) {
        //     config.headers.Authorization = `Bearer ${token}`;
        // }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Interceptor de resposta para tratamento de erros
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response) {
            // Erros da API (4xx, 5xx)
            console.error("Erro da API:", error.response.data);
        } else if (error.request) {
            // Sem resposta do servidor
            console.error("Sem resposta do servidor");
        } else {
            console.error("Erro:", error.message);
        }
        return Promise.reject(error);
    }
);
