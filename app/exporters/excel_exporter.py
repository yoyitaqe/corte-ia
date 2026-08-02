import pandas as pd

def generar_excel(datos, ruta_salida="data/salida_cortes.xlsx"):
    """
    Recibe un diccionario (o lista de diccionarios) con los datos
    de cortes de luz, y genera un archivo Excel ordenado.
    """
    if isinstance(datos, dict):
        datos = [datos]

    tabla = pd.DataFrame(datos)

    tabla = tabla.rename(columns={
        "empresa": "Empresa",
        "fecha": "Fecha",
        "hora_inicio": "Hora Inicio",
        "hora_fin": "Hora Fin",
        "departamento": "Departamento",
        "provincia": "Provincia",
        "distrito": "Distrito",
        "referencia": "Referencia",
        "duracion_horas": "Duracion (h)",
        "CP>2": "CP>2",
        "archivo_origen": "Archivo",
        "distrito_fuente": "Fuente Distrito"
    })

    tabla.to_excel(ruta_salida, index=False)
    print(f"Excel generado correctamente en: {ruta_salida}")