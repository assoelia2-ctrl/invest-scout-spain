import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract
import pandas as pd
import re

# 1. SEITE INITIALISIEREN
st.set_page_config(page_title="Málaga Invest: Final", layout="wide")

# Speicher für Daten fest anlegen (Schutz vor NameError)
if 'text_inhalt' not in st.session_state:
    st.session_state['text_inhalt'] = ""

st.title("🛡️ Invest-Scout: Analyse & Recherche")

# 2. DER STABILE UPLOAD (isoliert mit eigenem Key)
uploaded_file = st.file_uploader("Bild oder Screenshot hochladen:", type=["jpg", "png", "jpeg"], key="final_uploader_99")

if uploaded_file:
    img = Image.open(uploaded_file)
    
    # Foto-Optimierung (Verhindert Abstürze bei großen Dateien)
    if img.width > 1800 or img.height > 1800:
        img.thumbnail((1500, 1500))
    
    st.image(img, caption="Datei bereit", use_container_width=True)
    
    # Buttons in einer Reihe
    col_anal, col_rech = st.columns(2)
    
    with col_anal:
        if st.button("🚀 ANALYSE STARTEN"):
            with st.spinner("KI liest Daten..."):
                try:
                    # Bildverbesserung für OCR
                    proc = ImageOps.grayscale(img)
                    proc = ImageEnhance.Contrast(proc).enhance(2.0)
                    text = pytesseract.image_to_string(proc, lang='deu+spa')
                    st.session_state['text_inhalt'] = text
                    st.success("Analyse erfolgreich!")
                except Exception as e:
                    st.error(f"Fehler: {e}")

    with col_rech:
        # Recherche-Link (Dublettenprüfung)
        st.markdown(f"### [🔍 Dubletten-Check im Internet](https://www.google.com/search?q=Málaga+Immobilie+Recherche)")

# 3. INTERAKTION (Nur wenn Text da ist)
if st.session_state['text_inhalt']:
    st.divider()
    
    # Automatische Highlights anzeigen
    t = st.session_state['text_inhalt']
    flaeche = re.findall(r'\d+[\d.,]*\s?m2', t)
    
    c1, c2 = st.columns(2)
    with c1:
        st.info(f"📏 **Gefundene Fläche:** {flaeche[0] if flaeche else 'n.a.'}")
        st.write("📍 **Standort:** Málaga Region")
        st.map(pd.DataFrame({'lat': [36.7212], 'lon': [-4.4214]}))
    
    with c2:
        st.subheader("💬 Frage zum Objekt")
        frage = st.text_input("z.B. 'Bohrbrunnen?'")
        if frage:
            if frage.lower() in t.lower():
                pos = t.lower().find(frage.lower())
                st.success(f"Gefunden: ...{t[max(0, pos-50):pos+100]}...")
            else:
                st.warning("Kein Treffer im Scan.")
