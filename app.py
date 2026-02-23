import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract
import pandas as pd
import re

# ... (dein bisheriger Setup-Code) ...

if file:
    img = Image.open(file)
    st.image(img, caption="Bild/Foto empfangen", use_container_width=True)
    
    if st.button("🚀 TIEFENANALYSE STARTEN"):
        with st.spinner("Optimiere Foto für Analyse..."):
            try:
                # --- FOTO-OPTIMIERUNG ---
                # 1. In Graustufen umwandeln
                img_gray = ImageOps.grayscale(img)
                # 2. Kontrast extrem erhöhen (hilft bei Schatten auf Fotos)
                enhancer = ImageEnhance.Contrast(img_gray)
                img_final = enhancer.enhance(2.0)
                
                # --- TEXT EXTRAKTION ---
                # Wir geben Tesseract einen Hinweis, dass es nach Blöcken suchen soll
                custom_config = r'--oem 3 --psm 6'
                text = pytesseract.image_to_string(img_final, lang='deu+spa', config=custom_config)
                
                # --- DATEN-CHECK ---
                afo = "Ja" if "AFO" in text.upper() else "Nicht erkannt"
                # Suche nach Preisen (z.B. 250.000 €)
                preise = re.findall(r'\d+(?:\.\d+)?(?:\,\d+)?\s?€', text)
                
                # ANZEIGE
                st.markdown("### 📊 Extrahiert aus Foto/Screenshot")
                c1, c2 = st.columns(2)
                with c1:
                    st.metric("Preis-Schätzung", preise[0] if preise else "Prüfen...")
                with c2:
                    st.info(f"**Rechtlicher Hinweis:** {afo}")
                
                st.map(pd.DataFrame({'lat': [36.7212], 'lon': [-4.4214]}))
                
                with st.expander("Gelesenen Text anzeigen (Rohdaten)"):
                    st.write(text)

            except Exception as e:
                st.error(f"Fehler bei Foto-Analyse: {e}")
                st.info("Tipp: Halte das Handy beim Fotografieren möglichst parallel zum Papier.")
