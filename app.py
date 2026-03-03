import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image

# Título e Interfaz
st.title("🛠️ Escáner de Liners HERS")
st.write("Coloca una **tarjeta** al lado del liner para medir.")

foto = st.camera_input("Tomar foto")

if foto:
    img = Image.open(foto)
    img_array = np.array(img.convert('RGB'))
    
    # Procesamiento de imagen
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    blur = cv2.medianBlur(gray, 5)
    edged = cv2.Canny(blur, 30, 150) # Más sensible a bordes
    
    cnts, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(cnts) >= 2:
        # Ordenar por área para encontrar los dos objetos más grandes
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        
        # Objeto 1: Liner | Objeto 2: Tarjeta (Referencia)
        # 85.6mm es el ancho estándar de una tarjeta
        rect_ref = cv2.minAreaRect(cnts[1])
        px_per_mm = max(rect_ref[1]) / 85.6
        
        rect_liner = cv2.minAreaRect(cnts[0])
        largo = max(rect_liner[1]) / px_per_mm
        ancho = min(rect_liner[1]) / px_per_mm
        
        st.success(f"📏 Medida: {round(largo, 1)}mm x {round(ancho, 1)}mm")
        
        # Buscar en inventario.csv
        try:
            df = pd.read_csv('inventario.csv')
            # Buscamos coincidencias (tolerancia 8mm)
            match = df[(df['Largo_Nominal'].between(largo-8, largo+8))]
            if not match.empty:
                st.info(f"✅ Identificado como: **{match.iloc[0]['ID_Material']}**")
            else:
                st.warning("⚠️ No se encontró en el inventario.")
        except:
            st.error("No se pudo leer el archivo inventario.csv")
    else:
        st.error("No detecto suficientes objetos. Asegúrate de que el liner y la tarjeta se vean claramente.")
