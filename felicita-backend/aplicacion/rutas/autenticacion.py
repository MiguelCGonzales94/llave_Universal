from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from aplicacion.base_datos import obtener_db
from aplicacion.modelos.usuario import Usuario
from aplicacion.esquemas.usuario import UsuarioCrear, UsuarioRespuesta
from aplicacion.nucleo.seguridad import obtener_hash_password
from aplicacion.esquemas.token import Token
from aplicacion.nucleo.seguridad import obtener_hash_password, verificar_password, crear_token_acceso
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)

@router.post("/registro", response_model=UsuarioRespuesta)
def registrar_usuario(usuario: UsuarioCrear, db: Session = Depends(obtener_db)):
    # 1. Verificar si el email ya existe
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado."
        )

    # 2. Verificar si el DNI ya existe
    dni_existente = db.query(Usuario).filter(Usuario.dni == usuario.dni).first()
    if dni_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El DNI ya está registrado en el sistema."
        )

    # 3. Encriptar contraseña
    hash_seguro = obtener_hash_password(usuario.password)

    # 4. Crear el nuevo usuario
    nuevo_usuario = Usuario(
        dni=usuario.dni,
        nombres=usuario.nombres,
        apellido_paterno=usuario.apellido_paterno,
        apellido_materno=usuario.apellido_materno,
        email=usuario.email,
        telefono=usuario.telefono,
        hash_contrasena=hash_seguro, # Guardamos el hash, NO la pass plana
        nivel_kyc="NINGUNO"
    )

    # 5. Guardar en BD
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario

@router.post("/login", response_model=Token)
def login_para_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(obtener_db)):
    """
    Recibe 'username' (que será el email) y 'password'.
    Devuelve un Token JWT de acceso.
    """
    # 1. Buscar usuario por email (OAuth2 usa el campo 'username' para el login)
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    
    # 2. Validaciones
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas (Email no existe)",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verificar_password(form_data.password, usuario.hash_contrasena):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas (Contraseña errónea)",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Crear el Token
    token_acceso = crear_token_acceso(datos={"sub": usuario.email})
    
    return {"access_token": token_acceso, "token_type": "bearer"}