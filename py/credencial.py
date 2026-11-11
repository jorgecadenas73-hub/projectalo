import os
import json
import re
from google.cloud import vision
from openai import OpenAI

# 1. Configurar los clientes de las APIs
# Asegúrate de tener tu archivo de credenciales de Google Cloud: GOOGLE_APPLICATION_CREDENTIALS
client_vision = vision.ImageAnnotatorClient()
client_openai = OpenAI(api_key="TU_API_KEY_DE_OPENAI")

def procesar_identificacion(ruta_imagen):
    # 2. Leer la imagen y enviarla a Google Cloud Vision (OCR)
    with open(ruta_imagen, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client_vision.text_detection(image=image)
    texts = response.text_annotations

    if not texts:
        return {"error": "No se detectó texto en la imagen"}

    texto_extraido = texts[0].description
    print("--- Texto detectado por el OCR ---")
    print(texto_extraido)
    print("---------------------------------")

    # 3. Extraer CURP directamente usando Regex (es muy exacto debido a su estructura fija)
    # Patrón oficial del CURP en México
    patron_curp = r"[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d"
    coincidencia_curp = re.search(patron_curp, texto_extraido)
    curp = coincidencia_curp.group(0) if coincidencia_curp else "No encontrado"

    # 4. Usar IA para estructurar Nombre y Domicilio basados en el desorden del OCR
    prompt = f"""
    Del siguiente texto extraído de una identificación oficial mexicana, estructura los siguientes datos en un formato JSON limpio.
    Si no encuentras el dato, pon "No encontrado".
    
    Texto:
    {texto_extraido}
    
    Formato de salida requerido:
    {{
        "nombre": "NOMBRE COMPLETO",
        "domicilio": "DIRECCIÓN COMPLETA CON CALLE, COLONIA, CP, ESTADO"
    }}
    """

    respuesta_ia = client_openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"} # Fuerza a la IA a responder solo en JSON
    )

    datos_finales = json.loads(respuesta_ia.choices[0].message.content)
    datos_finales["curp"] = curp  # Agregamos el CURP que obtuvimos por Regex

    return datos_finales

#Ejemplo
resultado = procesar_identificacion("mi_ine.jpg")
print(json.dumps(resultado, indent=4, ensure_ascii=False))
