import streamlit as st
import cv2
import numpy as np
from PIL import Image

# --- CONFIGURACIÓN ---
# Medida real de una tarjeta de crédito estándar en mm
ANCHO_REFERENCIA_MM = 85.6 

def procesar_medidas(imagen_array):
    # 1. Convertir a escala de grises y detectar bordes
    gray = cv2.cvtColor(imagen_array, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blur, 50, 150)
    
    # 2. Encontrar todos los contornos
    cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(cnts) < 2:
        return None, "Coloca el liner junto a una tarjeta de referencia."

    # Ordenar contornos por tamaño (de mayor a menor)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    
    # El más grande suele ser el LINER, el segundo la REFERENCIA (tarjeta)
    liner_cnt = cnts[0]
    ref_cnt = cnts[1]
    
    # Calcular píxeles por mm basándose en la referencia
    ref_rect = cv2.minAreaRect(ref_cnt)
    (x, y), (w_ref_px, h_ref_px), angle = ref_rect
    pixels_per_mm = max(w_ref_px, h_ref_px) / ANCHO_REFERENCIA_MM
    
    # Medir el liner
    liner_rect = cv2.minAreaRect(liner_cnt)
    (lx, ly), (w_liner_px, h_liner_px), langle = liner_rect
    
    largo_mm = round(max(w_liner_px, h_liner_px) / pixels_per_mm, 1)
    ancho_mm = round(min(w_liner_px, h_liner_px) / pixels_per_mm, 1)
    
    return (largo_mm, ancho_mm), None
