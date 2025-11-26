import { useState } from 'react';
import api from '../services/api'; // Importamos nuestro puente
import { useNavigate } from 'react-router-dom'; // Para cambiar de página
import { KeyRound, Fingerprint } from 'lucide-react'; // Iconos bonitos

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

const handleLogin = async (e) => {
    e.preventDefault();
    setError(''); // Limpiar errores previos

    try {
      console.log("Intentando conectar con:", email); // Debug

      // FastAPI espera x-www-form-urlencoded
      const params = new URLSearchParams();
      params.append('username', email); // OJO: FastAPI exige que el campo se llame 'username'
      params.append('password', password);

      const response = await api.post('/auth/login', params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });

      console.log("Respuesta del servidor:", response.data); // Debug

      const token = response.data.access_token;
      localStorage.setItem('felicita_token', token);
      
      // Forzar la navegación
      console.log("Redirigiendo al dashboard...");
      navigate('/dashboard');// Usamos esto por si navigate falla

    } catch (err) {
      console.error("ERROR DETALLADO:", err);
      if (err.response) {
        // El servidor respondió con un error (ej. 401 Credenciales malas)
        setError(`Error del servidor: ${err.response.data.detail || 'Revisa tus datos'}`);
      } else if (err.request) {
        // No hubo respuesta (servidor apagado)
        setError('No se puede conectar con el servidor. ¿Está encendido?');
      } else {
        setError('Error desconocido. Revisa la consola.');
      }
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100 p-4">
      <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md border border-slate-200">
        
        {/* Encabezado */}
        <div className="text-center mb-8">
          <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
             <Fingerprint className="text-felicita-blue w-8 h-8" />
          </div>
          <h2 className="text-2xl font-bold text-felicita-dark">Bienvenido a Felicita</h2>
          <p className="text-gray-500 text-sm">Tu identidad digital segura</p>
        </div>

        {/* Formulario */}
        <form onSubmit={handleLogin} className="space-y-6">
          {error && (
            <div className="bg-red-50 text-red-600 p-3 rounded-lg text-sm text-center border border-red-100">
              {error}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Correo Electrónico</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
              placeholder="ejemplo@correo.com"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Contraseña</label>
            <div className="relative">
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
                placeholder="••••••••"
                required
              />
              <KeyRound className="absolute right-3 top-3.5 text-gray-400 w-5 h-5" />
            </div>
          </div>

          <button
            type="submit"
            className="w-full bg-felicita-blue hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition duration-200 shadow-lg shadow-blue-500/30"
          >
            Iniciar Sesión
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;