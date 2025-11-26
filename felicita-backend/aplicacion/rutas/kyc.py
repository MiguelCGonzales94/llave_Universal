from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from aplicacion.base_datos import obtener_db
from aplicacion.modelos.usuario import Usuario, DatosBiometricos
from aplicacion.nucleo.dependencias import obtener_usuario_actual
from aplicacion.nucleo.biometria import comparar_rostros
import shutil
import os
import uuid

router = APIRouter(prefix="/kyc", tags=["Validación de Identidad (KYC)"])

CARPETA_KYC = "almacenamiento_kyc"
os.makedirs(CARPETA_KYC, exist_ok=True)

@router.post("/validar")
def validar_identidad(
    foto_dni: UploadFile = File(...),
    foto_selfie: UploadFile = File(...),
    db: Session = Depends(obtener_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    # 1. Guardar archivos temporalmente
    ext_dni = os.path.splitext(foto_dni.filename)[1]
    ext_selfie = os.path.splitext(foto_selfie.filename)[1]
    
    nombre_dni = f"{usuario_actual.id}_dni{ext_dni}"
    nombre_selfie = f"{usuario_actual.id}_selfie{ext_selfie}"
    
    ruta_dni = os.path.join(CARPETA_KYC, nombre_dni)
    ruta_selfie = os.path.join(CARPETA_KYC, nombre_selfie)

    with open(ruta_dni, "wb") as b1:
        shutil.copyfileobj(foto_dni.file, b1)
    with open(ruta_selfie, "wb") as b2:
        shutil.copyfileobj(foto_selfie.file, b2)

    # 2. Ejecutar el Motor Biométrico
    es_match, score, mensaje = comparar_rostros(ruta_dni, ruta_selfie)

    # 3. Guardar resultado en Base de Datos (aunque falle, guardamos el intento)
    nuevo_registro = DatosBiometricos(
        id_usuario=usuario_actual.id,
        ruta_s3_dni_frente=ruta_dni,
        ruta_s3_selfie=ruta_selfie,
        puntaje_coincidencia=score,
        prueba_vida_exitosa=es_match
    )
    db.add(nuevo_registro)

    if es_match:
        # Actualizamos el nivel del usuario a "BIOMETRICO" (VIP)
        usuario_actual.nivel_kyc = "BIOMETRICO"
        usuario_actual.fecha_ultima_verificacion = nuevo_registro.fecha_verificacion
        db.add(usuario_actual)
        db.commit()
        return {
            "resultado": "EXITO",
            "mensaje": f"Identidad verificada correctamente. Similitud: {score}%",
            "nivel_nuevo": "BIOMETRICO"
        }
    else:
        db.commit() # Guardamos el registro del fallo
        raise HTTPException(
            status_code=400, 
            detail=f"Validación fallida. El rostro no coincide lo suficiente ({score}%). {mensaje}"
        )