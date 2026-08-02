import streamlit as st
from app.core.extractors.gemini_extractor import extraer_datos_imagen
from app.exporters.excel_exporter import generar_excel

st.title("Corte IA")
st.write("Sube imágenes de avisos de cortes programados y genera un Excel automáticamente.")

archivos = st.file_uploader(
    "Sube una o varias imágenes",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if archivos:
    if st.button("Procesar archivos"):
        resultados = []
        barra = st.progress(0)
        total = len(archivos)

        for i, archivo in enumerate(archivos):
            imagen_bytes = archivo.read()
            datos = extraer_datos_imagen(imagen_bytes, nombre_archivo=archivo.name)
            resultados.append(datos)
            barra.progress((i + 1) / total)

        st.success(f"Se procesaron {total} archivo(s) correctamente.")
        st.dataframe(resultados)

        ruta_salida = "data/salida_cortes.xlsx"
        generar_excel(resultados, ruta_salida)

        with open(ruta_salida, "rb") as f:
            st.download_button(
                label="Descargar Excel",
                data=f,
                file_name="cortes_programados.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )