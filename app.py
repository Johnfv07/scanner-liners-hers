import streamlit as st
import pandas as pd

st.set_page_config(page_title="Scanner HERS", page_icon="🛠️")

st.title("🛠️ Buscador de Materiales HERS")
st.write("Ingresa las medidas obtenidas con la app **Medición** de tu iPhone.")

# Entradas manuales para mayor precisión
col1, col2 = st.columns(2)
with col1:
    largo_manual = st.number_input("Largo (mm)", min_value=0.0, step=0.1, format="%.1f")
with col2:
    ancho_manual = st.number_input("Ancho (mm)", min_value=0.0, step=0.1, format="%.1f")

if st.button("Identificar Pieza"):
    if largo_manual > 0 and ancho_manual > 0:
        try:
            # Cargamos el CSV usando punto y coma como separador
            df = pd.read_csv('inventario.csv', sep=';')
            
            # Buscamos con una tolerancia de 5mm para cubrir pequeñas variaciones
            tolerancia = 5.0
            
            match = df[
                (df['Largo_Nominal'].astype(float).between(largo_manual - tolerancia, largo_manual + tolerancia)) &
                (df['Ancho_Nominal'].astype(float).between(ancho_manual - tolerancia, ancho_manual + tolerancia))
            ]
            
            if not match.empty:
                res = match.iloc[0]
                st.success(f"✅ **Material Encontrado:** {res['ID_Material (HERS)']}")
                st.info(f"**Detalles:** Forma {res['Forma']} | Medida en base: {res['Largo_Nominal']}x{res['Ancho_Nominal']} mm")
            else:
                st.warning("No se encontró una coincidencia exacta. Revisa las medidas o la base de datos.")
                
        except Exception as e:
            st.error(f"Error al leer la base de datos: {e}")
            st.info("Asegúrate de que el archivo 'inventario.csv' en GitHub use puntos y coma (;) para separar las columnas.")
    else:
        st.error("Por favor, ingresa ambas medidas.")

st.divider()
st.caption("Recuerda que puedes avisarme aquí en el chat si algo no funciona o si necesitas ajustar la tolerancia.")
