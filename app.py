import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd
import re

st.set_page_config(page_title="Málaga Invest: FULL ANALYSE", layout="wide")

st.title("🛡️ Invest-Scout: Analyse & Karte")

file = st.file_uploader("Screenshot hochladen:", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, caption="Bild erkannt", use_container_width=True)
    
    if st.button("🚀 ANALYSE STARTEN"):
        with st.spinner("Lese Daten aus dem Bild..."):
            try:
                # 1. TEXT LESEN
                text = pytesseract.image_to_string(img, lang='deu')
                
                # 2. ANALYSE (Wir suchen nach Keywords im Text)
                afo = "Ja (im Text gefunden)" if "AFO" in text.upper() else "Nicht explizit erwähnt"
                preis = re.findall(r'\d+[\d.,]*\s?€', text) # Sucht nach € Beträgen
                m2 = re.findall(r'\d+[\d.,]*\s?m2', text.lower()) # Sucht nach m2
                
                # 3. KARTEN-VORSCHAU (Málaga Zentrum als Startpunkt)
                # Später können wir hier Adressen suchen
                df = pd.DataFrame({'lat': [36.7212], 'lon': [-4.4214]})

                # ANZEIGE
                st.markdown("### 📊 Analyse-Ergebnisse")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Gefundene Preise", preis[0] if preis else "n.a.")
                    st.metric("Fläche", m2[0] if m2 else "n.a.")
                with col2:
                    st.info(f"**AFO Status:** {afo}")
                    st.warning("**Boden:** Rústico Check empfohlen!")

                st.markdown("### 📍 Lage (Vorschau)")
                st.map(df)
                
                st.markdown("### 📝 Extrahierter Text")
                st.code(text)
                
            except Exception as e:
                st.error("Bitte erst die 'packages.txt' in GitHub erstellen!")
                st.info(f"Technischer Fehler: {e}")

