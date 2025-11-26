from sqlalchemy import create_engine
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
