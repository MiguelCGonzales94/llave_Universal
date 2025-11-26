from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from aplicacion.base_datos import motor, Base
from aplicacion import modelos
from aplicacion.rutas import autenticacion 
from aplicacion.rutas import autenticacion, documentos, publico, kyc

import traceback

Base.metadata.create_all(bind=motor)

app = FastAPI(
    title="Felicita API",
    description="Plataforma de Identidad Digital y Firma Electrónica",
    version="1.0.0"
)

# --- CONFIGURACIÓN CORS (PERMISOS) ---
origenes = [
    "http://localhost:5173", # El puerto de Vite (Frontend)
    "http://127.0.0.1:5173",
    "http://192.168.18.16:5173", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origenes,
    allow_credentials=True,
    allow_methods=["*"], # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"], # Permitir todos los headers
)
# -------------------------------------


# MIDDLEWARE PARA CAPTURAR ERRORES DETALLADOS
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        # Imprimir el error completo en consola
        print("=" * 80)
        print("❌ ERROR CAPTURADO:")
        print(traceback.format_exc())
        print("=" * 80)
        return JSONResponse(
            status_code=500,
            content={
                "detail": str(e),
                "type": type(e).__name__,
                "traceback": traceback.format_exc()
            }
        )

app.include_router(autenticacion.router)
app.include_router(documentos.router)
app.include_router(publico.router)
app.include_router(kyc.router)

@app.get("/")
def raiz():
    return {"mensaje": "Bienvenido a Felicita - Tu Identidad Digital Segura"}