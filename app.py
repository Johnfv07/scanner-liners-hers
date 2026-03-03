import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Scanner HERS", layout="centered")
st.title("📏 Medidor de Liners Metálicos")

foto = st.camera_input("Capturar")

if foto:
    # Procesar imagen
    img = Image.open(foto)
    img_array = np.array(img.convert('RGB'))
    
    # 1. Filtros para metal (brillo alto)
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    blur = cv2.bilateralFilter(gray, 9, 75, 75) # Limpia ruido sin borrar bordes
    edged = cv2.Canny(blur, 40, 120) 
    
    # 2. Encontrar contornos
    cnts, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(cnts) >= 2:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        
        # REFERENCIA (Tarjeta = 85.6mm)
        rect_ref = cv2.minAreaRect(cnts[1])
        px_per_mm = max(rect_ref[1]) / 85.6
        
        # LINER
        rect_liner = cv2.minAreaRect(cnts[0])
        largo = max(rect_liner[1]) / px_per_mm
        ancho = min(rect_liner[1]) / px_per_mm
        
        st.metric("Largo Detectado", f"{round(largo, 1)} mm")
        st.metric("Ancho Detectado", f"{round(ancho, 1)} mm")
        
        # 3. Cruce con inventario.csv
        try:
            df = pd.read_csv('inventario.csv')
            # Tolerancia de 10mm por seguridad
            match = df[(df['Largo_Nominal'].between(largo-10, largo+10))]
            if not match.empty:
                st.success(f"🆔 Identificado: **{match.iloc[0]['ID_Material']}**")
            else:
                st.warning("No hay coincidencias exactas en el inventario.")
        except:
            st.error("Error al leer inventario.csv")
    else:
        st.warning("⚠️ No se detectan dos objetos. Pon la tarjeta al lado del liner.")
