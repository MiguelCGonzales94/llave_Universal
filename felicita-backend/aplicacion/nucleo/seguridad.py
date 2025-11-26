from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración traída del .env
CLAVE_SECRETA = os.getenv("CLAVE_SECRETA_JWT", "secreto_por_defecto_inseguro")
ALGORITMO = os.getenv("ALGORITMO", "HS256")
MINUTOS_EXPIRACION = int(os.getenv("MINUTOS_EXPIRACION_TOKEN", 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_password(password_plano: str, password_hasheado: str) -> bool:
    return pwd_context.verify(password_plano, password_hasheado)

def obtener_hash_password(password: str) -> str:
    return pwd_context.hash(password)

def crear_token_acceso(datos: dict, tiempo_expiracion: Optional[timedelta] = None):
    """Crea un JWT firmado con nuestros datos"""
    datos_a_codificar = datos.copy()
    
    if tiempo_expiracion:
        expira = datetime.utcnow() + tiempo_expiracion
    else:
        expira = datetime.utcnow() + timedelta(minutes=MINUTOS_EXPIRACION)
    
    # Agregamos la fecha de expiración al token
    datos_a_codificar.update({"exp": expira})
    
    token_codificado = jwt.encode(datos_a_codificar, CLAVE_SECRETA, algorithm=ALGORITMO)
    return token_codificado