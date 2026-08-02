import os
import json
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types
from app.exporters.excel_exporter import generar_excel

# Cargar la clave secreta
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Leer la imagen
ruta_imagen = "data/ejemplos/imagen_1.jpg"
with open(ruta_imagen, "rb") as archivo:
    imagen_bytes = archivo.read()

instruccion = """
Analiza esta imagen de un aviso de corte programado de energía eléctrica en Perú.
Devuelve SOLO un JSON (sin texto adicional, sin explicaciones) con esta estructura exacta:

{
  "empresa": "",
  "fecha": "",
  "hora_inicio": "",
  "hora_fin": "",
  "departamento": "",
  "provincia": "",
  "distrito": "",
  "referencia": ""
}

Instrucciones para cada campo:
- fecha: formato DD/MM/AAAA
- hora_inicio y hora_fin: formato HH:MM en 24 horas
- referencia: copia textual de la ubicación/zona/sector tal como aparece escrita en la imagen
- Si algún dato no aparece en la imagen, deja el valor como cadena vacía ""
"""

respuesta = client.models.generate_content(
    model="gemini-flash-latest",
    contents=[
        types.Part.from_bytes(data=imagen_bytes, mime_type="image/jpeg"),
        instruccion
    ]
)

texto_limpio = respuesta.text.strip().replace("```json", "").replace("```", "")
datos = json.loads(texto_limpio)

try:
    hora_inicio = datetime.strptime(datos["hora_inicio"], "%H:%M")
    hora_fin = datetime.strptime(datos["hora_fin"], "%H:%M")
    duracion_horas = (hora_fin - hora_inicio).total_seconds() / 3600
    if duracion_horas < 0:
        duracion_horas += 24
    datos["duracion_horas"] = round(duracion_horas, 1)
    datos["CP>2"] = "Sí" if duracion_horas > 2 else "No"
except (ValueError, KeyError):
    datos["duracion_horas"] = None
    datos["CP>2"] = "No se pudo calcular"

# Generar el Excel con estos datos
generar_excel(datos)