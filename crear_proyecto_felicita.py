import os

# Nombre del proyecto
NOMBRE_PROYECTO = "felicita-backend"

# Estructura de carpetas en ESPAÑOL
directorios = [
    f"{NOMBRE_PROYECTO}/aplicacion",
    f"{NOMBRE_PROYECTO}/aplicacion/modelos",      # Antes models
    f"{NOMBRE_PROYECTO}/aplicacion/esquemas",     # Antes schemas
    f"{NOMBRE_PROYECTO}/aplicacion/rutas",        # Antes routers
    f"{NOMBRE_PROYECTO}/aplicacion/nucleo",       # Antes core
]

# Contenido de los archivos (Con variables en Español)
archivos = {
    # 1. Dependencias
    f"{NOMBRE_PROYECTO}/requirements.txt": """fastapi
uvicorn
sqlalchemy
psycopg2-binary
pydantic
python-multipart
python-dotenv
python-jose[cryptography]
passlib[bcrypt]
email-validator
""",

    # 2. Variables de Entorno (.env)
    f"{NOMBRE_PROYECTO}/.env": """URL_BASE_DATOS=postgresql://postgres:tu_password_aqui@localhost/felicita_db
CLAVE_SECRETA_JWT=cambia_esto_por_una_frase_secreta_y_larga
ALGORITMO=HS256
MINUTOS_EXPIRACION_TOKEN=30
""",

    # 3. Archivo para ignorar basura en Git
    f"{NOMBRE_PROYECTO}/.gitignore": """entorno_virtual/
__pycache__/
.env
.DS_Store
""",

    # 4. Configuración de Base de Datos (base_datos.py)
    f"{NOMBRE_PROYECTO}/aplicacion/base_datos.py": """from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

URL_CONEXION = os.getenv("URL_BASE_DATOS")

# Crear el motor de conexión
motor = create_engine(URL_CONEXION)

# Crear la fábrica de sesiones
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor)

# Base para los modelos
Base = declarative_base()

# Función para obtener la base de datos en cada petición
def obtener_db():
    db = SesionLocal()
    try:
        yield db
    finally:
        db.close()
""",

    # 5. Modelos: Usuario e Institución (modelos/usuario.py)
    f"{NOMBRE_PROYECTO}/aplicacion/modelos/usuario.py": """import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, TIMESTAMP, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from aplicacion.base_datos import Base

class Institucion(Base):
    __tablename__ = "instituciones"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, nullable=False)
    ruc = Column(String, unique=True, nullable=False)
    llave_api = Column(String, unique=True, nullable=False)
    hash_secreto_api = Column(String, nullable=False)
    
    configuracion_portal = Column(JSONB, default={}) 
    es_activo = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relaciones
    documentos = relationship("Documento", back_populates="institucion")

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dni = Column(String, unique=True, nullable=False, index=True)
    nombres = Column(String, nullable=False)
    apellido_paterno = Column(String, nullable=False)
    apellido_materno = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hash_contrasena = Column(String, nullable=False)
    
    # Nivel de validación: 'NINGUNO', 'BASICO', 'BIOMETRICO'
    nivel_kyc = Column(String, default='NINGUNO') 
    
    terminos_aceptados = Column(Boolean, default=False)
    fecha_creacion = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relaciones
    documentos = relationship("Documento", back_populates="usuario")
""",

    # 6. Modelos: Documento (modelos/documento.py)
    f"{NOMBRE_PROYECTO}/aplicacion/modelos/documento.py": """import uuid
import enum
from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, Enum as SqEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from aplicacion.base_datos import Base

class EstadoDocumento(str, enum.Enum):
    PENDIENTE = "PENDIENTE"
    FIRMADO = "FIRMADO"
    RECHAZADO = "RECHAZADO"

class Documento(Base):
    __tablename__ = "documentos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_institucion = Column(UUID(as_uuid=True), ForeignKey("instituciones.id"))
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    
    nombre_archivo = Column(String, nullable=False)
    ruta_s3_original = Column(String, nullable=False)
    ruta_s3_final = Column(String, nullable=True)
    
    hash_original = Column(String, nullable=False)
    hash_final = Column(String, nullable=True)
    
    estado = Column(SqEnum(EstadoDocumento), default=EstadoDocumento.PENDIENTE)
    codigo_verificacion = Column(String, unique=True, index=True)
    
    fecha_creacion = Column(TIMESTAMP(timezone=True), server_default=func.now())

    institucion = relationship("Institucion", back_populates="documentos")
    usuario = relationship("Usuario", back_populates="documentos")
""",

    # 7. Archivo __init__ para exportar modelos
    f"{NOMBRE_PROYECTO}/aplicacion/modelos/__init__.py": """from .usuario import Usuario, Institucion
from .documento import Documento
""",

    # 8. Archivo Principal (inicio.py)
    f"{NOMBRE_PROYECTO}/aplicacion/inicio.py": """from fastapi import FastAPI
from aplicacion.base_datos import engine, Base
# Importar modelos para que SQLAlchemy los reconozca al iniciar
from aplicacion import modelos

# Crear tablas automáticamente (Solo para desarrollo)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Felicita API",
    description="Plataforma de Identidad Digital y Firma Electrónica",
    version="1.0.0"
)

@app.get("/")
def raiz():
    return {"mensaje": "Bienvenido a Felicita - Tu Identidad Digital Segura"}
""",

    # Archivos vacíos necesarios (__init__.py)
    f"{NOMBRE_PROYECTO}/aplicacion/__init__.py": "",
    f"{NOMBRE_PROYECTO}/aplicacion/esquemas/__init__.py": "",
    f"{NOMBRE_PROYECTO}/aplicacion/rutas/__init__.py": "",
    f"{NOMBRE_PROYECTO}/aplicacion/nucleo/__init__.py": "",
}

def crear_estructura():
    print(f"🚀 Iniciando creación de: {NOMBRE_PROYECTO} (Versión Español)...")
    
    # Crear Directorios
    for directorio in directorios:
        os.makedirs(directorio, exist_ok=True)
        print(f"   [CARPETA] {directorio}")

    # Crear Archivos
    for ruta, contenido in archivos.items():
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        print(f"   [ARCHIVO] {ruta}")

    print("\n✅ Estructura 'Felicita' creada correctamente.")

if __name__ == "__main__":
    crear_estructura()