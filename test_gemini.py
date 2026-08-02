import os
from dotenv import load_dotenv
from google import genai

# Cargar la clave secreta desde el archivo .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Crear el cliente de conexión con Gemini
client = genai.Client(api_key=api_key)

# Hacerle una pregunta simple, de prueba
respuesta = client.models.generate_content(
    model="gemini-flash-latest",
    contents="Responde solo con: Conexión exitosa con Gemini"
)

print(respuesta.text)