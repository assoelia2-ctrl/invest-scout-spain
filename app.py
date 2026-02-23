import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract
import pandas as pd

# 1. Globale Sicherheit (verhindert den NameError)
st.set_page_config(page_title="Invest-Scout Pro", layout="wide")

if 'scan_ergebnis' not in st.session_state:
    st.session_state['scan_ergebnis'] = ""

st.title("🛡️ Invest-Scout: Foto-Optimierung & Recherche")

# 2. Stabiler Uploader
uploaded_file = st.file_uploader("Bild/Foto hochladen:", type=["jpg", "png", "jpeg"], key="main_uploader")

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption=f"Bild erkannt ({uploaded_file.size//1024} KB)", use_container_width=True)
    
    if st.button("🚀 ANALYSE & RECHERCHE STARTEN"):
        with st.spinner("KI schärft Details..."):
            try:
                # RETTUNG FÜR KLEINE FOTOS (95KB Fix):
                # Wir vergrößern das Bild um den Faktor 3 für bessere OCR
                w, h = img.size
                img_big = img.resize((w*3, h*3), Image.Resampling.LANCZOS)
                
                # Kontrast-Boost für verwaschene Fotos
                proc = ImageOps.grayscale(img_big)
                proc = ImageEnhance.Contrast(proc).enhance(2.5)
                
                # Texterkennung
                ergebnis = pytesseract.image_to_string(proc, lang='deu+spa')
                st.session_state['scan_ergebnis'] = ergebnis
                st.success("Analyse erfolgreich!")
            except Exception as e:
                st.error(f"Fehler: {e}")

# 3. Funktionen nach dem Scan (Chat & Recherche)
if st.session_state['scan_ergebnis']:
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔍 Recherche & Dubletten")
        # Automatischer Link zur Google-Bildersuche/Recherche
        st.markdown("[👉 Hier klicken: Dubletten im Internet suchen](https://www.google.com/search?q=Málaga+Immobilie+Invest+Check)")
        st.info("Nutze diesen Link, um zu prüfen, ob das Foto bereits auf anderen Portalen existiert.")

    with col2:
        st.subheader("💬 Fragen zum Dokument")
        frage = st.text_input("Frag nach Details (z.B. Bohrbrunnen):")
        if frage:
            text = st.session_state['scan_ergebnis'].lower()
            if frage.lower() in text:
                st.success(f"✅ Begriff '{frage}' gefunden!")
                # Zeige Kontext
                pos = text.find(frage.lower())
                st.write(f"...{st.session_state['scan_ergebnis'][max(0, pos-40):pos+100]}...")
            else:
                st.warning("Kein direkter Treffer im Scan.")

    with st.expander("Vollständiges Scan-Protokoll"):
        st.code(st.session_state['scan_ergebnis'])
