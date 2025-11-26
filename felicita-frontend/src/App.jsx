import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import './App.css'
import Dashboard from './pages/Dashboard';
import KYC from './pages/KYC';

// Un componente temporal para probar la redirección
const DashboardPlaceholder = () => (
  <div className="p-10 text-center">
    <h1 className="text-3xl text-green-600 font-bold">¡Estás dentro del sistema! 🎉</h1>
    <button 
      onClick={() => {
        localStorage.removeItem('felicita_token');
        window.location.href = '/';
      }}
      className="mt-4 bg-red-500 text-white px-4 py-2 rounded"
    >
      Cerrar Sesión
    </button>
  </div>
);

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        {/* Usamos el componente Dashboard real */}
        <Route path="/dashboard" element={<Dashboard />} /> 
        <Route path="*" element={<Navigate to="/" />} />
        <Route path="/kyc" element={<KYC />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

