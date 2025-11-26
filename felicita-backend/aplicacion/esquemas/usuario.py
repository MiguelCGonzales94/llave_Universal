from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

# Esquema base (datos comunes)
class UsuarioBase(BaseModel):
    email: EmailStr
    dni: str
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    telefono: Optional[str] = None

# Datos necesarios para crear un usuario (el Frontend envía esto)
class UsuarioCrear(UsuarioBase):
    password: str  # Aquí recibimos la contraseña plana, pero NO la devolveremos

# Datos que devolvemos al cliente (la respuesta)
class UsuarioRespuesta(UsuarioBase):
    id: UUID
    nivel_kyc: str
    es_activo: bool
    fecha_creacion: datetime

    class Config:
        from_attributes = True # Permite leer desde los modelos de SQLAlchemy