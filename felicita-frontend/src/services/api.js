import axios from 'axios';

// Creamos una instancia de conexión
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000', // La dirección de tu Backend
});

// Interceptor Mágico:
// Antes de enviar cualquier petición, revisa si tenemos un Token guardado.
// Si lo tenemos, lo pega en la cabecera automáticamente.
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('felicita_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;