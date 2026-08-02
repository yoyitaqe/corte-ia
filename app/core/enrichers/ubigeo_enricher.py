import pandas as pd
import unicodedata
from app.core.enrichers.nominatim_enricher import buscar_con_nominatim

_tabla_ubigeo = pd.read_csv("data/ubigeo_peru.csv")

def _normalizar(texto):
    """Quita tildes y pasa a minúsculas, para comparar sin errores de acentos."""
    if not texto:
        return ""
    texto = str(texto).lower().strip()
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("utf-8")
    return texto

def enriquecer_con_ubigeo(datos):
    """
    Recibe el diccionario de datos de un corte y, si falta distrito,
    provincia o departamento, intenta completarlo usando la tabla Ubigeo,
    y si no encuentra nada, usa Nominatim como respaldo.
    """
    distrito = datos.get("distrito", "")
    provincia = datos.get("provincia", "")
    departamento = datos.get("departamento", "")
    referencia = datos.get("referencia", "")

    if distrito and (not provincia or not departamento):
        coincidencia = _tabla_ubigeo[
            _tabla_ubigeo["Distrito"].apply(_normalizar) == _normalizar(distrito)
        ]
        if not coincidencia.empty:
            fila = coincidencia.iloc[0]
            datos["provincia"] = datos["provincia"] or fila["Provincia"]
            datos["departamento"] = datos["departamento"] or fila["Departamento"]
            datos["distrito_fuente"] = "Ubigeo (exacto)"

    elif provincia and not distrito:
        distritos_de_la_provincia = _tabla_ubigeo[
            _tabla_ubigeo["Provincia"].apply(_normalizar) == _normalizar(provincia)
        ]

        referencia_normalizada = _normalizar(referencia)
        encontrado = None

        for _, fila in distritos_de_la_provincia.iterrows():
            if _normalizar(fila["Distrito"]) in referencia_normalizada:
                encontrado = fila
                break

        if encontrado is not None:
            datos["distrito"] = encontrado["Distrito"]
            datos["departamento"] = datos["departamento"] or encontrado["Departamento"]
            datos["distrito_fuente"] = "Ubigeo (coincidencia en referencia)"
        else:
            resultado_nominatim = buscar_con_nominatim(referencia, provincia, departamento)
            if resultado_nominatim["distrito"]:
                datos["distrito"] = resultado_nominatim["distrito"]
                datos["distrito_fuente"] = resultado_nominatim["fuente"]
            else:
                datos["distrito_fuente"] = "No encontrado (Ubigeo ni Nominatim)"

    return datos