import pandas as pd

def generar_excel(datos, ruta_salida="data/salida_cortes.xlsx"):
    """
    Recibe un diccionario (o lista de diccionarios) con los datos
    de cortes de luz, y genera un archivo Excel ordenado.
    """
    # Si recibimos un solo diccionario, lo convertimos en una lista de 1 elemento
    if isinstance(datos, dict):
        datos = [datos]

    # Convertir la lista de diccionarios en una tabla (DataFrame)
    tabla = pd.DataFrame(datos)

    # Renombrar las columnas a nombres más presentables para el Excel
    tabla = tabla.rename(columns={
        "empresa": "Empresa",
        "fecha": "Fecha",
        "hora_inicio": "Hora Inicio",
        "hora_fin": "Hora Fin",
        "departamento": "Departamento",
        "provincia": "Provincia",
        "distrito": "Distrito",
        "referencia": "Referencia",
        "duracion_horas": "Duración (h)",
        "CP>2": "CP>2"
    })

    # Guardar como archivo Excel
    tabla.to_excel(ruta_salida, index=False)
    print(f"Excel generado correctamente en: {ruta_salida}")