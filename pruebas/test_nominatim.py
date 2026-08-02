from app.core.enrichers.nominatim_enricher import buscar_con_nominatim
from app.core.enrichers.ubigeo_enricher import enriquecer_con_ubigeo

# Simulamos los datos que ya sabemos que Gemini extrajo
datos_prueba = {
    "empresa": "Electro Dunas",
    "fecha": "31/07/2026",
    "hora_inicio": "08:00",
    "hora_fin": "18:00",
    "departamento": "Ica",
    "provincia": "Ica",
    "distrito": "",
    "referencia": "Asociación De Vivienda San Luis Gonzaga De Ica, Habilitación Urbana Chacarilla, Urb. Chacarilla S/N, Urbanización Casuarinas – Etapas (I, II, III, IV, V, VI), Las Casuarinas (Techo Propio), Urbanización El Haras – Etapas (I, II, III, IV, V, VI), C.P. Cachiche – Parque, A.V. Ricardo Palma (I y II) – Cachiche"
}

print("=== Probando Nominatim directamente ===")
resultado_directo = buscar_con_nominatim(
    datos_prueba["referencia"],
    datos_prueba["provincia"],
    datos_prueba["departamento"]
)
print(resultado_directo)

print("\n=== Probando el enriquecedor completo ===")
resultado_completo = enriquecer_con_ubigeo(datos_prueba.copy())
print(resultado_completo)
from app.exporters.excel_exporter import generar_excel
import pandas as pd

print("\n=== Generando Excel de prueba ===")
generar_excel(resultado_completo, "data/prueba_directa.xlsx")

# Leer el Excel recién creado para confirmar su contenido
verificacion = pd.read_excel("data/prueba_directa.xlsx")
print(verificacion)