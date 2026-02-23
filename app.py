import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract
import pandas as pd
import re

# Seite konfigurieren
st.set_page_config(page_title="Málaga Invest: FIX", layout="wide")

# Titel
st.title("🛡️ Invest-Scout: Analyse & Chat")

# 1. BILD-UPLOAD (Muss ganz oben stehen und unabhängig sein)
file = st.file_uploader("Bild oder Screenshot hochladen:", type=["jpg", "png", "jpeg"], key="main_uploader")

if file:
    # Bild anzeigen
    img = Image.open(file)
    st.image(img, caption="Dokument geladen", use_container_width=True)
    
    # Analyse-Button
    if st.button("🚀 ANALYSE STARTEN"):
        with st.spinner("Lese Dokument..."):
            try:
                # Bildoptimierung
                gray = ImageOps.grayscale(img)
                enhanced = ImageEnhance.Contrast(gray).enhance(2.0)
                
                # Text extrahieren
                extracted_text = pytesseract.image_to_string(enhanced, lang='deu+spa')
                st.session_state['doc_text'] = extracted_text
                
                st.success("Analyse fertig! Du kannst jetzt unten Fragen stellen.")
                
                # Karte (Standard Málaga)
                st.map(pd.DataFrame({'lat': [36.7212], 'lon': [-4.4214]}))
            except Exception as e:
                st.error(f"Fehler bei der Analyse: {e}")

# 2. CHAT-BEREICH (Nur anzeigen, wenn Text vorhanden ist)
st.divider()
if 'doc_text' in st.session_state:
    st.subheader("💬 Fragen zum Objekt")
    user_query = st.text_input("Deine Frage (z.B. Preis, Brunnen, AFO):", key="chat_input")
    
    if user_query:
        # Einfache Suche im extrahierten Text
        q = user_query.lower()
        text = st.session_state['doc_text'].lower()
        
        if "preis" in q or "euro" in q or "€" in q:
            found = re.findall(r'\d+(?:\.\d+)?(?:\,\d+)?\s?€', st.session_state['doc_text'])
            st.write(f"Gefundene Beträge: {', '.join(found) if found else 'Keine gefunden.'}")
        elif "brunnen" in q or "pozo" in q:
            st.write("Suche nach Brunnen... " + ("Gefunden!" if "brunnen" in text or "pozo" in text else "Nichts gefunden."))
        else:
            st.write("Ich durchsuche den Scan... Bitte frage nach Preisen oder AFO für ein genaueres Ergebnis.")
else:
    st.info("Lade ein Bild hoch und klicke auf 'Analyse starten', um den Chat zu aktivieren.")
