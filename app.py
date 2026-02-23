import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract
import pandas as pd

# 1. Seite konfigurieren
st.set_page_config(page_title="Málaga Invest: Hard Reset", layout="wide")

st.title("🛡️ Invest-Scout: Foto-Fix & Analyse")

# 2. DER SPEICHER-PUTZTRUPP
# Wenn ein neues File hochgeladen wird, löschen wir den alten Text sofort
if 'doc_text' not in st.session_state:
    st.session_state['doc_text'] = ""

def reset_data():
    st.session_state['doc_text'] = ""

# 3. DER UPLOADER (mit Reset-Funktion)
file = st.file_uploader("Bild oder Foto hochladen:", 
                         type=["jpg", "png", "jpeg"], 
                         key="stable_up_v3",
                         on_change=reset_data) # Löscht alten Text bei neuem Bild

if file:
    img = Image.open(file)
    
    # FOTO-VERKLEINERUNG (Bleibt drin!)
    if img.width > 1800 or img.height > 1800:
        img.thumbnail((1500, 1500))
    
    st.image(img, caption="Datei bereit", use_container_width=True)
    
    if st.button("🚀 ANALYSE STARTEN"):
        with st.spinner("KI verarbeitet Bild..."):
            try:
                # Bildoptimierung
                proc = ImageOps.grayscale(img)
                proc = ImageEnhance.Contrast(proc).enhance(2.0)
                
                # Texterkennung
                text = pytesseract.image_to_string(proc, lang='deu+spa')
                st.session_state['doc_text'] = text
                st.success("Analyse erfolgreich!")
            except Exception as e:
                st.error(f"Fehler: {e}")

# 4. ANZEIGE & KOMMUNIKATION (Nur wenn Text existiert)
if st.session_state['doc_text']:
    st.divider()
    
    # Karte anzeigen
    st.map(pd.DataFrame({'lat': [36.7212], 'lon': [-4.4214]}))
    
    # Einfache Abfrage
    query = st.text_input("Frag nach Details (z.B. Bohrbrunnen):")
    if query:
        t = st.session_state['doc_text'].lower()
        if query.lower() in t:
            st.success(f"Gefunden!")
            st.write(st.session_state['doc_text'])
