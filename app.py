import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import pytesseract
import pandas as pd

st.set_page_config(page_title="Málaga Invest: Foto-Fix", layout="wide")

if 'doc_text' not in st.session_state:
    st.session_state['doc_text'] = ""

st.title("🛡️ Invest-Scout: Screenshot & Foto-Analyse")

# Fester Uploader-Key gegen Abstürze
file = st.file_uploader("Bild oder Foto hochladen:", type=["jpg", "png", "jpeg"], key="stable_up")

if file:
    img = Image.open(file)
    
    # NEU: Foto-Kompression (Verhindert den 'NameError' durch Speicherüberlastung)
    if img.width > 1800 or img.height > 1800:
        img.thumbnail((1500, 1500))
    
    st.image(img, caption="Datei bereit", use_container_width=True)
    
    if st.button("🚀 ANALYSE STARTEN"):
        with st.spinner("Optimiere Bild für KI..."):
            try:
                # Vorverarbeitung für Fotos (Graustufen + extremer Kontrast)
                proc = ImageOps.grayscale(img)
                proc = ImageEnhance.Contrast(proc).enhance(2.5)
                
                # Texterkennung (Deutsch & Spanisch kombiniert)
                text = pytesseract.image_to_string(proc, lang='deu+spa')
                st.session_state['doc_text'] = text
                st.success("Analyse erfolgreich!")
            except Exception as e:
                st.error(f"Fehler: {e}")

if st.session_state['doc_text']:
    st.divider()
    st.subheader("💬 Frage zum Objekt")
    q = st.text_input("Frag nach Details (z.B. Bohrbrunnen):")
    if q and q.lower() in st.session_state['doc_text'].lower():
        st.success(f"Gefunden! Textstelle: ...{st.session_state['doc_text'][st.session_state['doc_text'].lower().find(q.lower())-50:200]}...")
    
    st.map(pd.DataFrame({'lat': [36.7212], 'lon': [-4.4214]}))
    with st.expander("Gelesener Text (Rohdaten)"):
        st.code(st.session_state['doc_text'])
