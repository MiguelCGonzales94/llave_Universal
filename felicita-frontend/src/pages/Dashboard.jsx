import { useState } from 'react';
import api from '../services/api';
import { UploadCloud, FileSignature, CheckCircle, LogOut, FileText, ExternalLink, UserCheck } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const navigate = useNavigate();

  // Estados de la aplicación
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(1); // 1: Subir, 2: Firmar, 3: Resultado
  const [docData, setDocData] = useState(null); // Datos del documento subido
  const [signedData, setSignedData] = useState(null); // Datos tras firmar

  // Función para Cerrar Sesión
  const handleLogout = () => {
    localStorage.removeItem('felicita_token');
    navigate('/');
  };

  // 1. Manejar la selección del archivo
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  // 2. Enviar el archivo al Backend
  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);

    const formData = new FormData();
    formData.append('archivo', file);

    try {
      const response = await api.post('/documentos/subir', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      setDocData(response.data);
      setStep(2); // Pasamos al paso de firma
    } catch (error) {
      alert("Error subiendo el archivo. Verifica que sea un PDF.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  // 3. Ordenar la firma del documento
  const handleSign = async () => {
    setLoading(true);
    try {
      // Llamamos al endpoint de firmar usando el ID que nos dio el paso anterior
      const response = await api.post(`/documentos/firmar/${docData.id_documento}`);
      setSignedData(response.data);
      setStep(3); // Pasamos al resultado final
    } catch (error) {
      alert("Error al firmar el documento.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* --- BARRA SUPERIOR --- */}
      <nav className="bg-white shadow-sm border-b border-slate-200 px-6 py-4 flex justify-between items-center">
        <div className="flex items-center gap-4">
          <div className="bg-felicita-blue text-white p-2 rounded-lg">
            <FileSignature size={24} />
          </div>
          <span className="text-xl font-bold text-slate-800">Felicita</span>
        </div>
        <button
          onClick={() => navigate('/kyc')}
          className="flex items-center gap-2 bg-purple-100 text-purple-700 px-4 py-2 rounded-lg hover:bg-purple-200 transition font-medium text-sm"
        >
          <UserCheck size={18} /> Validar Identidad
        </button>

        <button
          onClick={handleLogout}
          className="flex items-center gap-2 text-slate-500 hover:text-red-500 transition"
        >
          <LogOut size={18} /> Salir
        </button>
      </nav>

      {/* --- CONTENIDO PRINCIPAL --- */}
      <main className="max-w-4xl mx-auto mt-10 p-6">

        <h1 className="text-3xl font-bold text-slate-800 mb-2">Panel de Firma</h1>
        <p className="text-slate-500 mb-8">Sigue los pasos para proteger legalmente tus documentos.</p>

        {/* TARJETA PRINCIPAL */}
        <div className="bg-white rounded-2xl shadow-xl border border-slate-100 overflow-hidden">

          {/* PASO 1: SUBIDA */}
          {step === 1 && (
            <div className="p-10 text-center">
              <div className="border-2 border-dashed border-slate-300 rounded-xl p-10 hover:bg-slate-50 transition cursor-pointer relative">
                <input
                  type="file"
                  accept="application/pdf"
                  onChange={handleFileChange}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                />
                <UploadCloud className="mx-auto text-felicita-blue mb-4" size={64} />
                <p className="text-lg font-medium text-slate-700">
                  {file ? file.name : "Arrastra tu PDF aquí o haz clic para buscar"}
                </p>
                <p className="text-sm text-slate-400 mt-2">Solo archivos PDF</p>
              </div>

              {file && (
                <button
                  onClick={handleUpload}
                  disabled={loading}
                  className="mt-6 bg-felicita-blue text-white px-8 py-3 rounded-lg font-bold hover:bg-blue-700 transition w-full md:w-auto"
                >
                  {loading ? "Subiendo..." : "Continuar"}
                </button>
              )}
            </div>
          )}

          {/* PASO 2: CONFIRMACIÓN Y FIRMA */}
          {step === 2 && docData && (
            <div className="p-10">
              <div className="bg-blue-50 border border-blue-100 rounded-lg p-4 mb-6 flex items-start gap-4">
                <FileText className="text-blue-600 mt-1" />
                <div>
                  <h3 className="font-bold text-blue-900">Documento Listo para Firmar</h3>
                  <p className="text-sm text-blue-700">{file.name}</p>
                  <p className="text-xs text-blue-500 mt-1 font-mono">Hash Original: {docData.hash_seguridad.substring(0, 20)}...</p>
                </div>
              </div>

              <div className="text-center">
                <p className="mb-6 text-slate-600">Al firmar, se estampará tu identidad digital y un sello de tiempo.</p>
                <button
                  onClick={handleSign}
                  disabled={loading}
                  className="bg-green-600 text-white px-8 py-3 rounded-lg font-bold hover:bg-green-700 transition w-full md:w-auto flex items-center justify-center gap-2 mx-auto"
                >
                  <FileSignature />
                  {loading ? "Firmando..." : "Firmar Documento Ahora"}
                </button>
              </div>
            </div>
          )}

          {/* PASO 3: ÉXITO */}
          {step === 3 && signedData && (
            <div className="p-10 text-center">
              <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <CheckCircle className="text-green-600" size={40} />
              </div>

              <h2 className="text-2xl font-bold text-slate-800 mb-2">¡Documento Firmado con Éxito!</h2>
              <p className="text-slate-500 mb-8">Tu documento ha sido sellado criptográficamente.</p>

              <div className="grid md:grid-cols-2 gap-4 max-w-2xl mx-auto">
                <div className="p-4 border rounded-lg bg-slate-50 text-left">
                  <span className="text-xs font-bold text-slate-400 uppercase">Ubicación Local</span>
                  <p className="text-sm text-slate-800 break-all mt-1">{signedData.url_descarga}</p>
                  <p className="text-xs text-amber-600 mt-2">*(Busca este archivo en la carpeta 'almacenamiento_local' de tu backend)*</p>
                </div>

                <div className="p-4 border rounded-lg bg-slate-50 text-left">
                  <span className="text-xs font-bold text-slate-400 uppercase">Verificación Pública</span>
                  <p className="text-sm text-slate-800 mt-1">Cualquiera puede validar este documento escaneando el QR.</p>
                  <a
                    href={`http://127.0.0.1:8000/publico/verificar/${docData.codigo_verificacion}`}
                    target="_blank"
                    rel="noreferrer"
                    className="mt-3 inline-flex items-center gap-1 text-felicita-blue font-bold text-sm hover:underline"
                  >
                    Probar Enlace de Verificación <ExternalLink size={14} />
                  </a>
                </div>
              </div>

              <button
                onClick={() => { setStep(1); setFile(null); }}
                className="mt-8 text-slate-500 hover:text-slate-800 underline"
              >
                Firmar otro documento
              </button>
            </div>
          )}

        </div>
      </main>
    </div>
  );
};

export default Dashboard;