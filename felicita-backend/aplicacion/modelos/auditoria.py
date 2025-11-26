import uuid
from sqlalchemy import Column, String, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from aplicacion.base_datos import Base

class RegistroAuditoria(Base):
    __tablename__ = "registros_auditoria"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_documento = Column(UUID(as_uuid=True), ForeignKey("documentos.id"), nullable=True)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=True)
    id_institucion = Column(UUID(as_uuid=True), ForeignKey("instituciones.id"), nullable=True)
    
    # Eventos: 'LOGIN', 'FIRMA', etc.
    tipo_evento = Column(String, nullable=False) 
    
    # Evidencia Técnica
    direccion_ip = Column(String, nullable=False)
    user_agent = Column(String, nullable=True)
    geolocalizacion = Column(String, nullable=True)
    
    # Detalles extra (JSON)
    detalles = Column(JSONB, default={})
    
    fecha_creacion = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relaciones (Para que funcionen los back_populates de los otros archivos)
    documento = relationship("Documento", back_populates="registros_auditoria")
    usuario = relationship("Usuario", back_populates="registros_auditoria")
    institucion = relationship("Institucion", back_populates="registros_auditoria")