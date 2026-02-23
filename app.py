import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract
import pandas as pd
import re

st.set_page_config(page_title="Málaga Invest: PRO-CHECK", layout="wide")

st.title("🛡️ Invest-Scout: Foto-Analyse & Karte")

file = st.file_uploader("Foto oder Screenshot hochladen:", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, caption="Originalbild", use_container_width=True)
    
    if st.button("🚀 TIEFENANALYSE STARTEN"):
        with st.spinner("Extrahiere Daten aus Foto..."):
            try:
                # --- BILD OPTIMIEREN FÜR FOTOS ---
                gray = ImageOps.grayscale(img)
                enhanced = ImageEnhance.Contrast(gray).enhance(2.5) # Kontrast für Fotos hochdrehen
                
                # --- TEXT LESEN ---
                custom_config = r'--oem 3 --psm 6'
                text = pytesseract.image_to_string(enhanced, lang='deu+spa', config=custom_config)
                
                # --- DATEN EXTRAHIEREN ---
                # Suche nach AFO
                afo_found = "✅ AFO erwähnt" if "AFO" in text.upper() else "❌ Kein AFO gefunden"
                
                # Suche nach Preis (€)
                preise = re.findall(r'\d+(?:\.\d+)?(?:\,\d+)?\s?€', text)
                
                # Suche nach Fläche (m2)
                flaeche = re.findall(r'\d+(?:\.\d+)?\s?m2', text.lower())

                # --- KARTEN LOGIK ---
                # Wir setzen einen Standardpunkt in Malaga (Zentrum)
                # Falls eine Adresse wie 'Marbella' oder 'Estepona' im Text ist, 
                # könnte man die Koordinaten hier anpassen.
                map_coords = pd.DataFrame({'lat': [36.7212], 'lon': [-4.4214]})

                # --- ANZEIGE ---
                st.markdown("### 📊 Analyse-Ergebnisse")
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Preis-Check", preise[0] if preise else "n.a.")
                with c2:
                    st.metric("Fläche", flaeche[0] if flaeche else "n.a.")
                with c3:
                    st.info(f"**Status:** {afo_found}")

                st.markdown("### 📍 Ungefähre Lage")
                st.map(map_coords)
                
                with st.expander("Gelesener Text (Rohdaten)"):
                    st.code(text)

            except Exception as e:
                st.error(f"Fehler: {e}")
                st.info("Prüfe, ob die 'packages.txt' in GitHub korrekt hinterlegt ist.")
