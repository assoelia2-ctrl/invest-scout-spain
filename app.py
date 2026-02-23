import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract
import pandas as pd
import re

# 1. Seiteneinstellungen
st.set_page_config(page_title="Málaga Invest: EXPERT", layout="wide")

# Initialisiere den Speicher, damit die App nicht abstürzt
if 'doc_text' not in st.session_state:
    st.session_state['doc_text'] = None

st.title("🛡️ Invest-Scout: Analyse & Chat")

# 2. Upload-Bereich (isoliert)
file = st.file_uploader("Bild/Screenshot hochladen:", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, caption="Bild erkannt", use_container_width=True)
    
    if st.button("🚀 ANALYSE STARTEN"):
        with st.spinner("Lese Daten aus..."):
            try:
                # Bildverbesserung
                gray = ImageOps.grayscale(img)
                enhanced = ImageEnhance.Contrast(gray).enhance(2.0)
                
                # Texterkennung (OCR)
                text = pytesseract.image_to_string(enhanced, lang='deu+spa')
                st.session_state['doc_text'] = text
                st.success("Analyse erfolgreich!")
            except Exception as e:
                st.error("Fehler: Hast du die packages.txt in GitHub erstellt?")

# 3. Anzeige & Chat (Nur wenn Analyse fertig ist)
if st.session_state['doc_text']:
    st.divider()
    
    # Karte anzeigen
    st.map(pd.DataFrame({'lat': [36.7212], 'lon': [-4.4214]}))
    
    # Der Chat
    st.subheader("💬 Fragen an das Dokument")
    query = st.text_input("Frag etwas zum Text (z.B. Preis):")
    
    if query:
        if query.lower() in st.session_state['doc_text'].lower():
            st.write("✅ Das wurde im Text gefunden.")
        else:
            st.write("❌ Dazu finde ich nichts im Scan.")
