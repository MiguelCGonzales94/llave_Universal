import uuid
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
    fecha_firma = Column(TIMESTAMP(timezone=True), nullable=True)

    # Relaciones
    institucion = relationship("Institucion", back_populates="documentos")
    usuario = relationship("Usuario", back_populates="documentos")
    
    # ESTA ES LA LÍNEA QUE FALTABA:
    registros_auditoria = relationship("RegistroAuditoria", back_populates="documento")