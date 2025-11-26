import os
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from pypdf import PdfReader, PdfWriter
import io
import hashlib
from datetime import datetime

def generar_imagen_qr(datos_qr: str):
    """Crea una imagen QR en memoria"""
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(datos_qr)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def calcular_hash_sha256(ruta_archivo: str) -> str:
    """Calcula el hash de un archivo en disco"""
    sha256_hash = hashlib.sha256()
    with open(ruta_archivo, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def procesar_firma_pdf(
    ruta_entrada: str, 
    ruta_salida: str, 
    datos_firma: dict, 
    url_validacion: str
):
    """
    Toma un PDF, le estampa la firma visual, agrega hoja de auditoría y guarda el resultado.
    """
    
    # 1. Preparar el QR y textos
    texto_firma = f"Firmado digitalmente por: {datos_firma['nombre']}"
    texto_fecha = f"Fecha: {datos_firma['fecha']}"
    texto_hash = f"Hash Original: {datos_firma['hash_original'][:20]}..."
    
    # --- PASO A: Crear la "Estampa Visual" (Watermark) ---
    packet = io.BytesIO()
    # Usamos canvas para dibujar sobre un PDF transparente
    c = canvas.Canvas(packet, pagesize=letter)
    width, height = letter
    
    # Dibujar caja de firma en la esquina inferior izquierda
    c.setStrokeColor(colors.blue)
    c.rect(10, 10, 250, 60, fill=0) # Caja
    
    # Texto
    c.setFont("Helvetica-Bold", 8)
    c.drawString(20, 55, "FIRMADO CON FELICITA")
    c.setFont("Helvetica", 7)
    c.drawString(20, 45, texto_firma)
    c.drawString(20, 35, texto_fecha)
    c.drawString(20, 25, texto_hash)
    
    # Generar y dibujar QR
    img_qr = generar_imagen_qr(url_validacion)
    # Guardamos QR temporalmente para que reportlab lo lea
    qr_temp_path = "temp_qr.png"
    img_qr.save(qr_temp_path)
    c.drawImage(qr_temp_path, 200, 15, width=50, height=50)
    
    c.save()
    packet.seek(0)
    os.remove(qr_temp_path) # Limpieza

    # --- PASO B: Fusionar Estampa con PDF Original ---
    nuevo_pdf_watermark = PdfReader(packet)
    pdf_original = PdfReader(ruta_entrada)
    escritor_pdf = PdfWriter()

    # Recorremos todas las páginas
    for i in range(len(pdf_original.pages)):
        pagina = pdf_original.pages[i]
        # Solo estampamos la firma en la PRIMERA página (o puedes elegir la última)
        if i == 0: 
            pagina.merge_page(nuevo_pdf_watermark.pages[0])
        escritor_pdf.add_page(pagina)

    # --- PASO C: Crear Hoja de Auditoría (Página Extra) ---
    packet_audit = io.BytesIO()
    c_audit = canvas.Canvas(packet_audit, pagesize=letter)
    
    # Título
    c_audit.setFont("Helvetica-Bold", 16)
    c_audit.drawString(50, 750, "CERTIFICADO DE AUDITORÍA DE FIRMA ELECTRÓNICA")
    
    # Línea separadora
    c_audit.line(50, 740, 550, 740)
    
    c_audit.setFont("Helvetica", 10)
    y = 700
    linea_alto = 20
    
    datos_mostrar = [
        f"Documento: {datos_firma['nombre_archivo']}",
        f"Firmante: {datos_firma['nombre']}",
        f"DNI: {datos_firma['dni']}",
        f"Fecha de Firma: {datos_firma['fecha']}",
        f"IP de Origen: {datos_firma['ip']}",
        "--- SEGURIDAD ---",
        f"Hash Original (SHA-256): {datos_firma['hash_original']}",
        f"Código de Verificación: {datos_firma['codigo_verificacion']}",
        "Este documento ha sido firmado electrónicamente bajo la Ley N° 27269."
    ]
    
    for linea in datos_mostrar:
        c_audit.drawString(50, y, linea)
        y -= linea_alto

    c_audit.save()
    packet_audit.seek(0)
    
    # Agregar la hoja de auditoría al final
    pdf_auditoria = PdfReader(packet_audit)
    escritor_pdf.add_page(pdf_auditoria.pages[0])

    # --- PASO D: Guardar Archivo Final ---
    with open(ruta_salida, "wb") as f_out:
        escritor_pdf.write(f_out)
        
    # Calcular hash del documento final (ya firmado)
    return calcular_hash_sha256(ruta_salida)