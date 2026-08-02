import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Cargar la clave secreta
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Leer la imagen desde el disco
ruta_imagen = "data/ejemplos/imagen_1.jpg"
with open(ruta_imagen, "rb") as archivo:
    imagen_bytes = archivo.read()

# Mandarle la imagen a Gemini, pidiéndole que la lea
respuesta = client.models.generate_content(
    model="gemini-flash-latest",
    contents=[
        types.Part.from_bytes(data=imagen_bytes, mime_type="image/jpeg"),
        "Describe qué información encuentras en esta imagen. Es un aviso de corte programado de energía eléctrica."
    ]
)

print(respuesta.text)