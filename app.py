import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract
import pandas as pd
import re

# 1. Setup - Wir erzwingen eine saubere Struktur
st.set_page_config(page_title="Málaga Invest: Stabile Version", layout="wide")

# Initialisiere den Speicher für den Text, falls er noch nicht da ist
if 'ausgelesener_text' not in st.session_state:
    st.session_state['ausgelesener_text'] = ""

st.title("🛡️ Invest-Scout: Analyse & Kommunikation")

# 2. Der Upload-Bereich
# Wir geben dem Uploader einen festen Key, damit er beim Chatten nicht "vergisst", was er geladen hat
uploaded_file = st.file_uploader("Bild/Screenshot hochladen:", type=["jpg", "png", "jpeg"], key="fest_uploader")

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Bild erkannt", use_container_width=True)
    
    if st.button("🚀 ANALYSE STARTEN", key="analyze_btn"):
        with st.spinner("KI liest Dokument..."):
            try:
                # Bildverbesserung für Fotos
                gray = ImageOps.grayscale(img)
                enhanced = ImageEnhance.Contrast(gray).enhance(2.0)
                
                # OCR (Texterkennung)
                extrahiert = pytesseract.image_to_string(enhanced, lang='deu+spa')
                st.session_state['ausgelesener_text'] = extrahiert
                st.success("Analyse erfolgreich abgeschlossen!")
            except Exception as e:
                st.error(f"Fehler: Hast du die packages.txt in GitHub? ({e})")

# 3. Der Interaktions-Bereich (Chat & Karte)
# Erscheint erst, wenn wirklich Text da ist
if st.session_state['ausgelesener_text']:
    st.divider()
    
    col_links, col_rechts = st.columns(2)
    
    with col_links:
        st.subheader("📍 Standort-Vorschau")
        # Standard-Karte Málaga
        st.map(pd.DataFrame({'lat': [36.7212], 'lon': [-4.4214]}))
        
    with col_rechts:
        st.subheader("💬 Frage zum Objekt")
        frage = st.text_input("Frag mich etwas (z.B. 'Preis', 'Brunnen'):", key="user_query")
        
        if frage:
            f = frage.lower()
            t = st.session_state['ausgelesener_text'].lower()
            
            if f in t:
                st.write("✅ Gefunden! Hier ist der Ausschnitt aus dem Dokument:")
                # Sucht die Stelle im Text und zeigt ein bisschen davor/danach an
                pos = t.find(f)
                st.info(f"...{st.session_state['ausgelesener_text'][max(0, pos-40):pos+100]}...")
            else:
                st.write("❌ Dazu konnte ich im aktuellen Scan leider nichts finden.")

    # Experten-Ansicht
    with st.expander("Vollständiges Scan-Protokoll"):
        st.code(st.session_state['ausgelesener_text'])
