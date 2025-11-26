from aplicacion.base_datos import SesionLocal
from aplicacion.modelos.usuario import Usuario
from aplicacion.nucleo.seguridad import obtener_hash_password

db = SesionLocal()

try:
    # Datos de prueba
    hash_seguro = obtener_hash_password("Password123!")
    
    nuevo_usuario = Usuario(
        dni="87654321",
        nombres="Test",
        apellido_paterno="Usuario",
        apellido_materno="Prueba",
        email="test.directo@gmail.com",
        telefono="999888777",
        hash_contrasena=hash_seguro,
        nivel_kyc="NINGUNO"
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    print("✅ Usuario creado exitosamente!")
    print(f"ID: {nuevo_usuario.id}")
    print(f"Email: {nuevo_usuario.email}")
    print(f"DNI: {nuevo_usuario.dni}")
    print(f"Activo: {nuevo_usuario.es_activo}")
    print(f"Fecha: {nuevo_usuario.fecha_creacion}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()