from deepface import DeepFace
import os

def comparar_rostros(ruta_foto_dni: str, ruta_foto_selfie: str):
    """
    Usa DeepFace para comparar dos imágenes.
    Retorna: (es_match: bool, score: float, mensaje: str)
    """
    try:
        # DeepFace descarga los modelos la primera vez, así que la primera ejecución será lenta.
        # Usamos el modelo "VGG-Face" por defecto, es muy preciso.
        resultado = DeepFace.verify(
            img1_path=ruta_foto_dni,
            img2_path=ruta_foto_selfie,
            model_name="VGG-Face",
            detector_backend="opencv", # Usamos OpenCV que es rápido y no requiere C++
            enforce_detection=False    # Si no encuentra cara, que no explote, lo manejamos abajo
        )

        # DeepFace devuelve un diccionario con 'verified' (True/False) y 'distance'
        es_match = resultado['verified']
        distancia = resultado['distance']
        
        # Invertimos la distancia para que parezca un score (0 a 100%)
        # En VGG-Face, el umbral suele ser 0.40. Si distancia es 0, coincidencia es 100.
        score = max(0, (1.0 - distancia) * 100)

        # Mensaje personalizado
        mensaje = "Validación exitosa" if es_match else "Los rostros no coinciden"

        return es_match, round(score, 2), mensaje

    except Exception as e:
        print(f"Error DeepFace: {e}")
        # Si el error es raro, devolvemos False
        return False, 0.0, f"Error procesando imágenes: {str(e)}"