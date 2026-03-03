import streamlit as st
import pandas as pd

st.title("🛠️ Buscador de Materiales HERS")

# 1. Instrucción para el usuario
st.info("💡 Usa la app 'Medición' de tu iPhone para obtener el largo y ancho exacto, luego ingrésalos aquí.")

# 2. Entradas manuales de alta precisión
col1, col2 = st.columns(2)
with col1:
    largo_manual = st.number_input("Largo (mm)", min_value=0.0, step=1.0)
with col2:
    ancho_manual = st.number_input("Ancho (mm)", min_value=0.0, step=1.0)

if largo_manual > 0 and ancho_manual > 0:
    # 3. Botón para identificar
    if st.button("Identificar Material"):
        try:
            df = pd.read_csv('inventario.csv')
            # Tolerancia pequeña de 3mm porque la regla del iPhone es muy exacta
            match = df[
                (df['Largo_Nominal'].between(largo_manual - 3, largo_manual + 3)) &
                (df['Ancho_Nominal'].between(ancho_manual - 3, ancho_manual + 3))
            ]
            
            if not match.empty:
                res = match.iloc[0]
                st.success(f"✅ Coincidencia: **{res['ID_Material']}**")
                st.write(f"Forma: {res['Forma']}")
            else:
                st.warning("No se encontró un material con esas medidas exactas.")
        except:
            st.error("Asegúrate de que 'inventario.csv' esté subido en GitHub.")
