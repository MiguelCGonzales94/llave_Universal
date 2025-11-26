from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from aplicacion.base_datos import obtener_db
from aplicacion.modelos.documento import Documento, EstadoDocumento
from aplicacion.modelos.usuario import Usuario

router = APIRouter(prefix="/publico", tags=["Verificación Pública (QR)"])

@router.get("/verificar/{codigo_qr}")
def verificar_documento_qr(codigo_qr: str, db: Session = Depends(obtener_db)):
    """
    Este endpoint es el que consulta el QR. 
    Devuelve los datos del documento SIN exponer el archivo físico si no es necesario.
    """
    # 1. Buscar el documento por su código único
    doc = db.query(Documento).filter(Documento.codigo_verificacion == codigo_qr).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado o código inválido")

    # 2. Buscar datos del firmante
    firmante = db.query(Usuario).filter(Usuario.id == doc.id_usuario).first()

    # 3. Responder con la "Verdad Oficial"
    return {
        "estado": doc.estado,
        "documento": doc.nombre_archivo,
        "firmado_por": f"{firmante.nombres} {firmante.apellido_paterno} {firmante.apellido_materno}",
        "dni_firmante": firmante.dni,
        "fecha_firma": doc.fecha_firma,
        "hash_integridad": doc.hash_final,
        "mensaje_legal": "Documento firmado digitalmente bajo la infraestructura de Felicita."
    }