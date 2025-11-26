import { useState } from 'react';
import api from '../services/api';
import { useNavigate } from 'react-router-dom';
import { Camera, UserCheck, ShieldAlert, Loader2, Upload } from 'lucide-react';

const KYC = () => {
  const navigate = useNavigate();
  const [dniFile, setDniFile] = useState(null);
  const [selfieFile, setSelfieFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(null); // 'success', 'error'
  const [message, setMessage] = useState('');

  const handleValidation = async (e) => {
    e.preventDefault();
    if (!dniFile || !selfieFile) {
      alert("Debes subir ambas fotos");
      return;
    }

    setLoading(true);
    setStatus(null);

    const formData = new FormData();
    formData.append('foto_dni', dniFile);
    formData.append('foto_selfie', selfieFile);

    try {
      // Llamamos al cerebro de IA que instalamos
      const response = await api.post('/kyc/validar', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      setStatus('success');
      setMessage(`¡Identidad Verificada! Nivel de confianza: ${response.data.mensaje}`);
      
      // Esperamos 2 segundos y volvemos al dashboard
      setTimeout(() => navigate('/dashboard'), 3000);

    } catch (error) {
      console.error(error);
      setStatus('error');
      setMessage(error.response?.data?.detail || "No pudimos validar tu identidad. Intenta con fotos más claras.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
      <div className="bg-white max-w-2xl w-full rounded-2xl shadow-xl overflow-hidden flex flex-col md:flex-row">
        
        {/* Barra Lateral Visual */}
        <div className="bg-felicita-blue p-8 flex flex-col justify-center items-center text-white md:w-1/3 text-center">
          <UserCheck size={64} className="mb-4" />
          <h2 className="text-2xl font-bold mb-2">Validación de Identidad</h2>
          <p className="text-blue-100 text-sm">Por seguridad, necesitamos confirmar que eres quien dices ser.</p>
        </div>

        {/* Formulario */}
        <div className="p-8 md:w-2/3">
          <h1 className="text-xl font-bold text-slate-800 mb-6">Sube tus evidencias</h1>
          
          <form onSubmit={handleValidation} className="space-y-6">
            
            {/* Input DNI */}
            <div className="border-2 border-dashed border-slate-200 rounded-xl p-4 hover:bg-slate-50 transition relative">
              <input 
                type="file" 
                accept="image/*" 
                onChange={(e) => setDniFile(e.target.files[0])}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              />
              <div className="flex items-center gap-4">
                <div className="bg-blue-100 p-3 rounded-full text-blue-600">
                  <Upload size={24} />
                </div>
                <div>
                  <p className="font-bold text-slate-700">Foto del DNI</p>
                  <p className="text-xs text-slate-500">{dniFile ? dniFile.name : "Toca para subir foto frontal"}</p>
                </div>
              </div>
            </div>

            {/* Input Selfie */}
            <div className="border-2 border-dashed border-slate-200 rounded-xl p-4 hover:bg-slate-50 transition relative">
              <input 
                type="file" 
                accept="image/*" 
                onChange={(e) => setSelfieFile(e.target.files[0])}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              />
              <div className="flex items-center gap-4">
                <div className="bg-purple-100 p-3 rounded-full text-purple-600">
                  <Camera size={24} />
                </div>
                <div>
                  <p className="font-bold text-slate-700">Tu Selfie</p>
                  <p className="text-xs text-slate-500">{selfieFile ? selfieFile.name : "Toca para subir una selfie actual"}</p>
                </div>
              </div>
            </div>

            {/* Mensajes de Estado */}
            {status === 'error' && (
              <div className="bg-red-50 text-red-700 p-3 rounded-lg flex items-center gap-2 text-sm">
                <ShieldAlert size={18} /> {message}
              </div>
            )}
            
            {status === 'success' && (
              <div className="bg-green-50 text-green-700 p-3 rounded-lg flex items-center gap-2 text-sm">
                <UserCheck size={18} /> {message}
              </div>
            )}

            {/* Botón de Acción */}
            <button
              type="submit"
              disabled={loading}
              className={`w-full py-3 rounded-lg font-bold text-white transition flex justify-center items-center gap-2
                ${loading ? 'bg-slate-400 cursor-not-allowed' : 'bg-felicita-dark hover:bg-slate-800'}
              `}
            >
              {loading && <Loader2 className="animate-spin" />}
              {loading ? "Analizando Rostros con IA..." : "Validar Biometría"}
            </button>
            
            <button 
              type="button"
              onClick={() => navigate('/dashboard')}
              className="w-full text-slate-400 text-sm hover:text-slate-600"
            >
              Cancelar y volver
            </button>

          </form>
        </div>
      </div>
    </div>
  );
};

export default KYC;