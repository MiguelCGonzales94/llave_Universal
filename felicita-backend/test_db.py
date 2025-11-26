# test_conexion.py
from aplicacion.base_datos import motor
from sqlalchemy import text

try:
    with motor.connect() as conexion:
        print("✅ Conexión exitosa a PostgreSQL")
        
        # Verificar columnas de la tabla usuarios
        resultado = conexion.execute(text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'usuarios'
            ORDER BY ordinal_position
        """))
        
        print("\n📋 Columnas de la tabla 'usuarios':")
        for fila in resultado:
            print(f"  - {fila.column_name}: {fila.data_type}")
            
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()