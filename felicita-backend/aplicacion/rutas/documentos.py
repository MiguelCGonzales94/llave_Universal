from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from aplicacion.base_datos import obtener_db
from aplicacion.modelos.documento import Documento, EstadoDocumento
from aplicacion.modelos.usuario import Usuario
from aplicacion.nucleo.dependencias import obtener_usuario_actual
from fastapi import Request
from datetime import datetime
from aplicacion.nucleo.motor_firma import procesar_firma_pdf

import shutil
import os
import hashlib
import uuid

router = APIRouter(prefix="/documentos", tags=["Gestión de Documentos"])

# Carpeta local para simular S3 (Ahorro de costos)
CARPETA_ALMACENAMIENTO = "almacenamiento_local"
os.makedirs(CARPETA_ALMACENAMIENTO, exist_ok=True)

def calcular_hash_sha256(ruta_archivo: str) -> str:
    """Genera la huella digital única del archivo (Legalmente vinculante)"""
    sha256_hash = hashlib.sha256()
    with open(ruta_archivo, "rb") as f:
        # Leemos el archivo en bloques de 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

@router.post("/subir")
def subir_documento(
    archivo: UploadFile = File(...),
    db: Session = Depends(obtener_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    # 1. Validar que sea PDF
    if archivo.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")

    # 2. Generar nombre único para no sobrescribir
    extension = os.path.splitext(archivo.filename)[1]
    nombre_seguro = f"{uuid.uuid4()}{extension}"
    ruta_guardado = os.path.join(CARPETA_ALMACENAMIENTO, nombre_seguro)

    # 3. Guardar archivo en disco
    with open(ruta_guardado, "wb") as buffer:
        shutil.copyfileobj(archivo.file, buffer)

    # 4. Calcular HASH ORIGINAL (Integridad)
    hash_doc = calcular_hash_sha256(ruta_guardado)

    # 5. Crear registro en Base de Datos
    # Generamos un código corto para el futuro QR
    codigo_qr = str(uuid.uuid4())[:8].upper()

    nuevo_doc = Documento(
        id_usuario=usuario_actual.id,
        nombre_archivo=archivo.filename,
        ruta_s3_original=ruta_guardado, # Guardamos la ruta local por ahora
        hash_original=hash_doc,
        estado=EstadoDocumento.PENDIENTE,
        codigo_verificacion=codigo_qr
    )

    db.add(nuevo_doc)
    db.commit()
    db.refresh(nuevo_doc)

    return {
        "mensaje": "Documento subido y protegido exitosamente",
        "id_documento": nuevo_doc.id,
        "hash_seguridad": nuevo_doc.hash_original,
        "codigo_verificacion": nuevo_doc.codigo_verificacion
    }
    
@router.post("/firmar/{id_documento}")
def firmar_documento(
    id_documento: str,
    request: Request, # Para obtener la IP
    db: Session = Depends(obtener_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    # 1. Buscar el documento
    doc = db.query(Documento).filter(Documento.id == id_documento).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
        
    if doc.id_usuario != usuario_actual.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para firmar este documento")
        
    if doc.estado == EstadoDocumento.FIRMADO:
        raise HTTPException(status_code=400, detail="El documento ya ha sido firmado")

    # 2. Definir rutas
    nombre_final = f"firmado_{doc.nombre_archivo}"
    ruta_final = os.path.join(CARPETA_ALMACENAMIENTO, nombre_final)
    
    # URL que tendrá el QR (Por ahora simulada local)
    url_qr = f"https://felicita.pe/verificar/{doc.codigo_verificacion}"
    
    # 3. Datos para el Motor de Firma
    datos_firma = {
        "nombre": f"{usuario_actual.nombres} {usuario_actual.apellido_paterno}",
        "dni": usuario_actual.dni,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hash_original": doc.hash_original,
        "nombre_archivo": doc.nombre_archivo,
        "codigo_verificacion": doc.codigo_verificacion,
        "ip": request.client.host
    }
    
    try:
        # --- LLAMADA AL MOTOR DE FIRMA ---
        hash_final_calculado = procesar_firma_pdf(
            ruta_entrada=doc.ruta_s3_original,
            ruta_salida=ruta_final,
            datos_firma=datos_firma,
            url_validacion=url_qr
        )
        
        # 4. Actualizar Base de Datos
        doc.ruta_s3_final = ruta_final
        doc.hash_final = hash_final_calculado
        doc.estado = EstadoDocumento.FIRMADO
        doc.fecha_firma = datetime.now()
        
        db.commit()
        
        return {
            "mensaje": "Documento firmado exitosamente",
            "estado": "FIRMADO",
            "url_descarga": ruta_final, # En producción esto sería una URL pre-firmada de S3
            "hash_final": hash_final_calculado
        }
        
    except Exception as e:
        print(f"Error firmando: {e}")
        raise HTTPException(status_code=500, detail="Error interno al procesar la firma del PDF")