import requests
import time

def buscar_con_nominatim(referencia, provincia="", departamento=""):
    """
    Busca una referencia de ubicación usando Nominatim (OpenStreetMap),
    como respaldo cuando la tabla Ubigeo no encuentra coincidencia.
    Devuelve un diccionario con distrito, provincia y departamento (lo que logre encontrar).
    """
    # Tomamos solo la primera zona mencionada en la referencia, para no confundir la búsqueda
    primera_zona = referencia.split(",")[0].strip()
    consulta = f"{primera_zona}, {provincia}, {departamento}, Peru"

    url = "https://nominatim.openstreetmap.org/search"
    parametros = {
        "q": consulta,
        "format": "jsonv2",
        "addressdetails": 1,
        "countrycodes": "pe",
        "limit": 1
    }
    # Nominatim exige identificarse con un User-Agent propio (política de uso justo)
    encabezados = {"User-Agent": "CorteIA-App/1.0"}

    try:
        respuesta = requests.get(url, params=parametros, headers=encabezados, timeout=10)
        time.sleep(1)  # respetar el límite de 1 solicitud por segundo

        resultados = respuesta.json()
        if not resultados:
            return {"distrito": "", "provincia": "", "departamento": "", "fuente": "Nominatim (sin resultados)"}

        direccion = resultados[0].get("address", {})

        # Nominatim no siempre usa las mismas etiquetas; probamos varias posibles
        distrito_encontrado = (
            direccion.get("city_district")
            or direccion.get("suburb")
            or direccion.get("town")
            or direccion.get("city")
            or direccion.get("village")
            or ""
        )
        provincia_encontrada = direccion.get("county", "")
        departamento_encontrado = direccion.get("state", "")

        return {
            "distrito": distrito_encontrado,
            "provincia": provincia_encontrada,
            "departamento": departamento_encontrado,
            "fuente": "Nominatim"
        }

    except Exception as e:
        return {"distrito": "", "provincia": "", "departamento": "", "fuente": f"Error Nominatim: {str(e)}"}