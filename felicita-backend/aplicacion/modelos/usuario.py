import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, TIMESTAMP, JSON, DECIMAL
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
    registros_auditoria = relationship("RegistroAuditoria", back_populates="institucion")


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dni = Column(String, unique=True, nullable=False, index=True)
    nombres = Column(String, nullable=False)
    apellido_paterno = Column(String, nullable=False)
    apellido_materno = Column(String, nullable=False)
    
    email = Column(String, unique=True, nullable=False, index=True)
    telefono = Column(String, nullable=True)
    hash_contrasena = Column(String, nullable=False)
    
    # Nivel de validación: 'NINGUNO', 'BASICO', 'BIOMETRICO'
    nivel_kyc = Column(String, default='NINGUNO') 
    fecha_ultima_verificacion = Column(TIMESTAMP(timezone=True), nullable=True)
    
    terminos_aceptados = Column(Boolean, default=False)
    fecha_creacion = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relaciones
    documentos = relationship("Documento", back_populates="usuario")
    registros_auditoria = relationship("RegistroAuditoria", back_populates="usuario")
    # Relación con la tabla que faltaba
    datos_biometricos = relationship("DatosBiometricos", back_populates="usuario", uselist=False)

class DatosBiometricos(Base):
    """
    Esta es la clase que faltaba y causaba el error.
    """
    __tablename__ = "datos_biometricos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    
    # Rutas a las imágenes
    ruta_s3_dni_frente = Column(String, nullable=True)
    ruta_s3_dni_dorso = Column(String, nullable=True)
    ruta_s3_selfie = Column(String, nullable=True)
    
    # Resultado de DeepFace
    puntaje_coincidencia = Column(DECIMAL(5, 2), nullable=True) 
    prueba_vida_exitosa = Column(Boolean, default=False)
    
    fecha_verificacion = Column(TIMESTAMP(timezone=True), server_default=func.now())

    usuario = relationship("Usuario", back_populates="datos_biometricos")