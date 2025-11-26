from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from aplicacion.base_datos import obtener_db
from aplicacion.nucleo.seguridad import CLAVE_SECRETA, ALGORITMO
from aplicacion.modelos.usuario import Usuario

# Esto le dice a Swagger que el login está en /auth/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def obtener_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(obtener_db)):
    """
    Decodifica el token, extrae el email y busca al usuario en la BD.
    """
    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
        email: str = payload.get("sub")
        if email is None:
            raise credenciales_exception
    except JWTError:
        raise credenciales_exception
    
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None:
        raise credenciales_exception
        
    return usuario